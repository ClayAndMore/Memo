版本： 1.18

入口 ： k8s.io\kubernetes\cmd\kube-apiserver\apiserver.go



### 1  先配置命令行

cmd\kube-apiserver\app\server.go：NewAPIServerCommand() 函数 使用 cobra 库配置命令行。



### 2  NewServerRunOptions() 

cmd\kube-apiserver\app\options\options.go 初始化了一个 ServerRunOptions 结构体：

``` go
func NewAPIServerCommand() *cobra.Command {
	s := options.NewServerRunOptions() // 
	cmd := &cobra.Command{
		Use: "kube-apiserver",
		Long: `....`,
		RunE: func(cmd *cobra.Command, args []string) error {
			verflag.PrintAndExitIfRequested()
			utilflag.PrintFlags(cmd.Flags())

			// set default options, 这里为一些结构体赋值默认值
			completedOptions, err := Complete(s)  // completedOptions 实际上就是上方的s,包了一层结构体
			if err != nil {
				return err
			}

			// validate options
			if errs := completedOptions.Validate(); len(errs) != 0 {
				return utilerrors.NewAggregate(errs)
			}

			return Run(completedOptions, genericapiserver.SetupSignalHandler())
		},
	}

 func Run(completeOptions completedServerRunOptions, stopCh <-chan struct{}) error {
	// To help debugging, immediately log version
	klog.Infof("Version: %+v", version.Get())

	server, err := CreateServerChain(completeOptions, stopCh)
	if err != nil {
		return err
	}

	prepared, err := server.PrepareRun()
	if err != nil {
		return err
	}

	return prepared.Run(stopCh)
}
```



### 3 CreateServerChain:

``` go
func CreateServerChain(completedOptions completedServerRunOptions, stopCh <-chan struct{}) (*aggregatorapiserver.APIAggregator, error) 
	CreateNodeDialer(completedOptions)  // 创建 http.Transport, ssh 隧道等连接
    CreateKubeAPIServerConfig() // api配置
	createAPIExtensionsConfig() // 额外api配置
	createAPIExtensionsServer() // 额外api服务
	CreateKubeAPIServer() // api服务
	createAggregatorConfig() // 聚合配置
	createAggregatorServer() //  聚合服务，包含api服务和额外api服务
// 最后返回 聚合服务
```

结构如下：

![image-20210324153054480](https://gitee.com/ClayAndMore/image/raw/master/k8s-read-code-apiserver-CreateServerChain.png)



### 4  server.PrepareRun():

``` go
func (s *APIAggregator) PrepareRun() (preparedAPIAggregator, error) {
	// add post start hook before generic PrepareRun in order to be before /healthz installation
	if s.openAPIConfig != nil {
		s.GenericAPIServer.AddPostStartHookOrDie("apiservice-openapi-controller", func(context genericapiserver.PostStartHookContext) error {
			go s.openAPIAggregationController.Run(context.StopCh)
			return nil
		})
	}

	prepared := s.GenericAPIServer.PrepareRun()
	return preparedAPIAggregator{APIAggregator: s, runnable: prepared}, nil
```

主要配置 apiservice-openapi-controller 的路由和 一些健康检查

注意返回的结构是 preparedAPIAggregator:

``` go
type runnable interface {
	Run(stopCh <-chan struct{}) error
}

type preparedAPIAggregator struct {
	*APIAggregator
	runnable runnable
}
```

runnable 其实就是 APIAggregator.GenericatAPIServer, 只不过又封装了一层：

``` go
// kubernetes\staging\src\k8s.io\apiserver\pkg\server\genericapiserver.go
type preparedGenericAPIServer struct {
	*GenericAPIServer
}

func (s *GenericAPIServer) PrepareRun() preparedGenericAPIServer {
	s.delegationTarget.PrepareRun()
...
	return preparedGenericAPIServer{s}
}
```



### 5. prepared.Run(stopCh)

到了最后一行return prepared.Run(stopCh)， 这里会调用  preparedGenericAPIServer(如上) 的run:

``` go
func (s preparedGenericAPIServer) Run(stopCh <-chan struct{}) error {
	delayedStopCh := make(chan struct{})

	go func() {   // 处理停止信号
		defer close(delayedStopCh)
		<-stopCh
		close(s.readinessStopCh)
		time.Sleep(s.ShutdownDelayDuration)
	}()

	// close socket after delayed stopCh
	err := s.NonBlockingRun(delayedStopCh)  
	if err != nil {
		return err
	}

	<-stopCh // 在这里就会停住，等待退出的信号

	// run shutdown hooks directly. This includes deregistering from the kubernetes endpoint in case of kube-apiserver.
	err = s.RunPreShutdownHooks() 
	if err != nil {
		return err
	}

	// wait for the delayed stopCh before closing the handler chain (it rejects everything after Wait has been called).
	<-delayedStopCh

	// Wait for all requests to finish, which are bounded by the RequestTimeout variable.
	s.HandlerChainWaitGroup.Wait()

	return nil
}
```



NonBlockingRun：

``` go
// NonBlockingRun spawns the secure http server. An error is
// returned if the secure port cannot be listened on.
func (s preparedGenericAPIServer) NonBlockingRun(stopCh <-chan struct{}) error {
	// Use an stop channel to allow graceful shutdown without dropping audit events
	// after http server shutdown.
	auditStopCh := make(chan struct{})

	// Start the audit backend before any request comes in. This means we must call Backend.Run
	// before http server start serving. Otherwise the Backend.ProcessEvents call might block.
	if s.AuditBackend != nil {  //这里是不走的
		if err := s.AuditBackend.Run(auditStopCh); err != nil {
			return fmt.Errorf("failed to run the audit backend: %v", err)
		}
	}

	// Use an internal stop channel to allow cleanup of the listeners on error.
	internalStopCh := make(chan struct{})
	var stoppedCh <-chan struct{}
	if s.SecureServingInfo != nil && s.Handler != nil {
		var err error
        // 这里启动 SecureServing 的监听
		stoppedCh, err = s.SecureServingInfo.Serve(s.Handler, s.ShutdownTimeout, internalStopCh)
		if err != nil {
			close(internalStopCh)
			close(auditStopCh)
			return err
		}
	}

	// Now that listener have bound successfully, it is the
	// responsibility of the caller to close the provided channel to
	// ensure cleanup.
	go func() {
		<-stopCh
		close(internalStopCh)
		if stoppedCh != nil {
			<-stoppedCh
		}
		s.HandlerChainWaitGroup.Wait()
		close(auditStopCh)
	}()

	s.RunPostStartHooks(stopCh) // 注意这里

	if _, err := systemd.SdNotify(true, "READY=1\n"); err != nil {
		klog.Errorf("Unable to send systemd daemon successful start message: %v\n", err)
	}

	return nil
}
```



### 6 RunPreShutdownHooks

RunPreShutdownHooks（k8s.io\apiserver\pkg\server\hooks.go）：

``` go
func (s *GenericAPIServer) RunPostStartHooks(stopCh <-chan struct{}) {
	s.postStartHookLock.Lock()
	defer s.postStartHookLock.Unlock()
	s.postStartHooksCalled = true

	context := PostStartHookContext{
		LoopbackClientConfig: s.LoopbackClientConfig,
		StopCh:               stopCh,
	}

	for hookName, hookEntry := range s.postStartHooks {
		go runPostStartHook(hookName, hookEntry, context)
	}
}
```

这里hook了很多路由的注册和启动监听：

![image-20210324164905880](https://gitee.com/ClayAndMore/image/raw/master/k8s-read-code-apiserver-runPostStartHooks.png)

到这里大体就结束了。



### 其他

监听主要是用的http库，还有http2的库, 用 go-restful 处理的路由。



s.ServerCert.CertKey 

- CertFile /var/run/kubernetes/apiserver.crt 
- KeyFile /var/run/kubernetes/apiserver.key 

这两个文件调试时居然显示可读的，windows 哪来的这两个文件呢，linux 下k8s 环境下也没有找到。



在创建ApiserverConfig（kubernetes\cmd\kube-apiserver\app\server.go，CreateKubeAPIServerConfig()的 buildGenericConfig）时， 设置了一些map, kubernetes\pkg\master\master.go：

``` go
admissionregistrationv1 "k8s.io/api/admissionregistration/v1"
.
func DefaultAPIResourceConfigSource() *serverstorage.ResourceConfig {
	ret := serverstorage.NewResourceConfig()
	// NOTE: GroupVersions listed here will be enabled by default. Don't put alpha versions in the list.
	ret.EnableVersions(
		admissionregistrationv1.SchemeGroupVersion, 
		admissionregistrationv1beta1.SchemeGroupVersion,
		apiv1.SchemeGroupVersion,
		appsv1.SchemeGroupVersion,
		authenticationv1.SchemeGroupVersion,
		authenticationv1beta1.SchemeGroupVersion,
		authorizationapiv1.SchemeGroupVersion,
		authorizationapiv1beta1.SchemeGroupVersion,
		autoscalingapiv1.SchemeGroupVersion,
		autoscalingapiv2beta1.SchemeGroupVersion,
		autoscalingapiv2beta2.SchemeGroupVersion,
		batchapiv1.SchemeGroupVersion,
		batchapiv1beta1.SchemeGroupVersion,
		certificatesapiv1beta1.SchemeGroupVersion,
		coordinationapiv1.SchemeGroupVersion,
		coordinationapiv1beta1.SchemeGroupVersion,
		discoveryv1beta1.SchemeGroupVersion,
		eventsv1beta1.SchemeGroupVersion,
		extensionsapiv1beta1.SchemeGroupVersion,
		networkingapiv1.SchemeGroupVersion,
		networkingapiv1beta1.SchemeGroupVersion,
		nodev1beta1.SchemeGroupVersion,
		policyapiv1beta1.SchemeGroupVersion,
		rbacv1.SchemeGroupVersion,
		rbacv1beta1.SchemeGroupVersion,
		storageapiv1.SchemeGroupVersion,
		storageapiv1beta1.SchemeGroupVersion,
		schedulingapiv1beta1.SchemeGroupVersion,
		schedulingapiv1.SchemeGroupVersion,
	)
```

注册对应的大部分是 k8s.io api 里的包：

![image-20210324115055486](https://gitee.com/ClayAndMore/image/raw/master/k8s-read-code-apiserver-ApiConfigSource.png)

