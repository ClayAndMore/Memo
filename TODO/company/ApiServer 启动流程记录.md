
---
title: "ApiServer 启动流程记录.md"
date: 2020-03-17 18:47:27 +0800
lastmod: 2020-03-17 18:47:27 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## ApiServer 启动流程记录



### main.go

我们从main.go 的 main 函数 看起：

``` go
func main() {

	modelManagers := map[int]elemental.ModelManager{
		0: gaia.Manager(),
		1: gaia.Manager(),
	}

	//subVersion := map[string]interface{}{"v":"1"}
	opts := []bahamut.Option{
		bahamut.OptRestServer(":12345"),
		bahamut.OptModel(modelManagers),
		bahamut.OptCustomRootHandler(rootHandler),
		//bahamut.OptServiceInfo("test", "1", subVersion),
	}

	server := bahamut.New(opts...)

	// RegisterProcessor registers a new Processor for a particular Identity.
	err := server.RegisterProcessor(&processor.NamespaceProcessor{}, gaia.NamespaceIdentity)	// ---> server.processors[identity.Name] = processor
	if err != nil {
		fmt.Println("server.RegisterProcessor err: ", err)
	}

..

	v := server.VersionsInfo()
	routesInfo := server.RoutesInfo()

	fmt.Println("server.RoutesInfo: ", routesInfo)
	fmt.Println("server.VersionsInfo: ", v)

	server.Run(context.Background())
}
```



### ModelManager

``` go
	modelManagers := map[int]elemental.ModelManager{
		0: gaia.Manager(), // moderManager 结构体
		1: gaia.Manager(),
	}
```

emental 模块 的 manager.go 中定义了 ModeManger 接口：

``` go
// An ModelManager is the interface that allows to search Identities
// and create Identifiable and Identifiables from Identities.
type ModelManager interface {

	Identifiable(Identity) Identifiable
	SparseIdentifiable(Identity) SparseIdentifiable
	...

	// Relationships return the model's elemental.RelationshipsRegistry.
	Relationships() RelationshipsRegistry
}
```



Gaia identities_registry.go 中 的 Manager() 函数：

``` go
func Manager() elemental.ModelManager { return manager }
// manager 返回的是 moderManager 结构体：
var manager = modelManager{}
```

当然  gaia 模块 中的 modelManger结构体 实现了 ModeManger 接口：

``` go
// gaia/identities_registry.go
type modelManager struct{}

func (f modelManager) IdentityFromName(name string) elemental.Identity {

	return identityNamesMap[name]
}

func (f modelManager) IdentityFromCategory(category string) elemental.Identity {

	return identitycategoriesMap[category]
}
...
```



### bahamut.Option

``` go
opts := []bahamut.Option{
  bahamut.OptRestServer(":12345"),
  bahamut.OptModel(modelManagers),
  bahamut.OptCustomRootHandler(rootHandler),
}

```

Bahamut options.go  有 Option 的定义：

``` go
type Option func(*config) // 函数结构体, 指定传入参数为 config结构体
```

接下来看config, config 的 定义在 bahamut 中 的config.go:

``` go
type config struct {
	general struct {
		panicRecoveryDisabled bool
	}

	restServer struct {
		listenAddress         string
		readTimeout           time.Duration
		writeTimeout          time.Duration
		idleTimeout           time.Duration
		disableCompression    bool
		disableKeepalive      bool
		enabled               bool
		customRootHandlerFunc http.HandlerFunc
		customListener        net.Listener
	}

	pushServer struct {   // websocket 推送服务
...
	}

	healthServer struct {
...
	}

	profilingServer struct {
...
	}

...
	model struct {
		modelManagers              map[int]elemental.ModelManager
		readOnly                   bool
		readOnlyExcludedIdentities []elemental.Identity
		unmarshallers              map[elemental.Identity]CustomUmarshaller
		marshallers                map[elemental.Identity]CustomMarshaller
		retriever                  IdentifiableRetriever
	}
...
}

```

... 的地方为省略，后续看需要补充。 



接下来看下 Option 结构体里的每个函数：

#### bahamut.OptRestServer

Options.go 中定义了 OptRestServer 函数：

``` go
func OptRestServer(listen string) Option {
	return func(c *config) {
		c.restServer.enabled = true   // 开启enable, 意为服务可用状态
		c.restServer.listenAddress = listen // 监听地址
	}
}
```



#### bahamut.OptModel

``` go
func OptModel(modelManagers map[int]elemental.ModelManager) Option {
	return func(c *config) {
		c.model.modelManagers = modelManagers
	}
}
```

将 之前初始化的 moderManager 结构体 赋值给 config mode.



#### bahamut.OptCustomRootHandler

``` go
// bahamut.OptCustomRootHandler(rootHandler),
func rootHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusTeapot)
	_, _ = w.Write([]byte("hello world"))
}

// options.go: 
// 定义 访问 根路由 (/) 的 handler
func OptCustomRootHandler(handler http.HandlerFunc) Option {
	return func(c *config) {
		c.restServer.customRootHandlerFunc = handler
	}
}
```



### 服务的初始化

服务由 `server := bahamut.New(opts...)` , 使用上方的opt初始化。

new 函数在 bahamut/bahamut.go 中定义：

``` go
func New(options ...Option) Server {

	c := config{}
	for _, opt := range options {
		opt(&c)   // 执行 options 中的每个函数，使用同一config
	}

  // 省略了一些日志警告

	return NewServer(c)
}
```

NewServer:

``` go
// NewServer returns a new Bahamut Server.
func NewServer(cfg config) Server { 

	mux := bone.New()  // bone 库是一个轻量的 HTTP Multiplexer 多路由器
	srv := &server{
		multiplexer: mux,
		processors:  make(map[string]Processor), // Processor 后面说
		cfg:         cfg,
	}

	if cfg.restServer.enabled {  // 注意这里，上方的enable开启后这里用到
		srv.restServer = newRestServer(cfg, mux, srv.ProcessorForIdentity, srv.Push)
	}

	if cfg.pushServer.enabled {
		srv.pushServer = newPushServer(cfg, mux, srv.ProcessorForIdentity)
	}

	if cfg.healthServer.enabled {
		srv.healthServer = newHealthServer(cfg)
	}

	if cfg.profilingServer.enabled {
		srv.profilingServer = newProfilingServer(cfg)
	}

	return srv
}
```

**注意这里函数定义返回的是Server接口(大写）， 而内部返回的实际上是 server(小写)结构体，**那么，server 肯定实现了Server 方法， Server:

``` go
// interfaces.go
// Server is the interface of a bahamut server.
type Server interface {
	RegisterProcessor(Processor, elemental.Identity) error // 注册 Processor
	UnregisterProcessor(elemental.Identity) error // 取消注册 Processor
	ProcessorForIdentity(elemental.Identity) (Processor, error) // 返回注册过的Processor
	ProcessorsCount() int // 注册的Processor 数量
	Push(...*elemental.Event)  // 推送 event 给所有活跃的session
	RoutesInfo() map[int][]RouteInfo // 所有的服务路由信息
	VersionsInfo() map[string]interface{} // 版本信息
	PushEndpoint() string // 返回所有配置的 推送端点， 如果没有返回空字符串
	Run(context.Context)  // 跑服务，用关闭 context 的方式来停止。
}
```

Processor 在 bahamut/interfaces.go 中 被定义成一个空接口：

`type Processor interface{}` 

我在这里先把它想象成一种处理单元，因为是接口类型，可以容纳各种数据类型。



再看下返回的这个 server 定义：

``` go
// bahamut/bahamut.go:
type server struct {
	multiplexer     *bone.Mux
	processors      map[string]Processor
	cfg             config
	restServer      *restServer
	pushServer      *pushServer
	healthServer    *healthServer
	profilingServer *profilingServer
}

// 额外看下 server 结构体实现的 RegisterProcessor 方法，后面会用到
func (b *server) RegisterProcessor(processor Processor, identity elemental.Identity) error {

	if _, ok := b.processors[identity.Name]; ok {
		return fmt.Errorf("identity %s already has a registered processor", identity)
	}

	b.processors[identity.Name] = processor
	return nil
}
```

server 的 proccessor 用 map 类型 以 elemental.Identity 的 name 存储各种 Process.

那么 elemantal.Identity 如何定义的：

``` go
// elemantal identity.go:
type Identity struct {
	Name     string `msgpack:"name" json:"name"`
	Category string `msgpack:"category" json:"category"`
	Private  bool   `msgpack:"-" json:"-"`
	Package  string `msgpack:"-" json:"-"`
}
```

一个 Identity(身份）是一个包括有关 Identifiable 必要信息的结构， 目前 Identifiable 可以理解为一种加密通信组件。



### 注册 Processor

``` go
// 用具体的 Identity 去注册 Processor
// ---> server.processors[identity.Name] = processor
err := server.RegisterProcessor(&processor.NamespaceProcessor{}, gaia.NamespaceIdentity)	

err = server.RegisterProcessor(&processor.HostServiceProcessor{}, gaia.HostServiceIdentity)	

err = server.RegisterProcessor(&processor.ExternalNetworkProcessor{}, gaia.ExternalNetworkIdentity)

err = server.RegisterProcessor(&processor.NetworkAccessPolicyProcessor{}, gaia.NetworkAccessPolicyIdentity)

err = server.RegisterProcessor(&processor.ServiceProcessor{}, gaia.ServiceIdentity)
```

这些 Identity 映射了 各种资源， 如 NamespaceIdentity:

```go
var NamespaceIdentity = elemental.Identity{
	Name:     "namespace",
	Category: "namespaces", // 分类
	Package:  "squall",  // 对应的是gaia 中的 squall 包
	Private:  false,
}
```



### Server Run

最后一句 ` server.Run(context.Background)` 开启服务：

bahamut/bahamut.go:

``` go
func (b *server) Run(ctx context.Context) {
	// 走这里
	if b.restServer != nil {
		go b.restServer.start(ctx, b.RoutesInfo())
	}
 // 其他服务的判断。。
	if b.pushServer != nil {
		go b.pushServer.start(ctx)
	}

	if b.healthServer != nil {
		go b.healthServer.start(ctx)
	}

	if hook := b.cfg.hooks.postStart; hook != nil {
		if err := hook(b); err != nil {
			zap.L().Fatal("Unable to execute bahamut postStart hook", zap.Error(err))
		}
	}

	<-ctx.Done()

	if hook := b.cfg.hooks.preStop; hook != nil {
		if err := hook(b); err != nil {
			zap.L().Error("Unable to execute bahamut preStop hook", zap.Error(err))
		}
	}

  // 停服务的处理：
	// Stop the health server first so we become unhealthy.
	if b.healthServer != nil {
		<-b.healthServer.stop().Done()
	}

	// Stop the push server to disconnect everybody.
	if b.pushServer != nil {
		b.pushServer.stop()
	}

	// Stop the restserver and wait for current requests to complete.
	if b.restServer != nil {
		<-b.restServer.stop().Done()
	}

	// Stop the profiling server.
	if b.profilingServer != nil {
		b.profilingServer.stop()
	}
}
```

目前的设置 只会走 restServer start, 它的函数定义在 bahamut/rest_server.go:

``` go
func (a *restServer) start(ctx context.Context, routesInfo map[int][]RouteInfo) {

	a.installRoutes(routesInfo)  // 初始化路由

	var err error
  // 安全认证，证书 token 等。
	if a.cfg.tls.serverCertificates != nil || a.cfg.tls.serverCertificatesRetrieverFunc != nil {
		a.server = a.createSecureHTTPServer(a.cfg.restServer.listenAddress)
	} else {
		a.server = a.createUnsecureHTTPServer(a.cfg.restServer.listenAddress)
	}

	a.server.Handler = a.multiplexer

	go func() {

		listener := a.cfg.restServer.customListener
		if listener == nil {
			listener, err = net.Listen("tcp", a.server.Addr)
			if err != nil {
				zap.L().Fatal("Unable to dial", zap.Error(err))
			}
		}

		if a.cfg.tls.serverCertificates != nil || a.cfg.tls.serverCertificatesRetrieverFunc != nil {
			err = a.server.ServeTLS(listener, "", "")
		} else {
      // 这里其实是使用 net/http server 开启服务
			err = a.server.Serve(listener)
		}

		if err != nil {
			if err == http.ErrServerClosed {
				return
			}
			zap.L().Fatal("Unable to start api server", zap.Error(err))
		}
	}()

	zap.L().Info("API server started", zap.String("address", a.cfg.restServer.listenAddress))

	<-ctx.Done()
}
```

这些就是apiserver(bahamute demo) 服务主要启动流程。

后续有重要的细节会补充。

这里是 流程图 可参考：https://www.jianguoyun.com/p/DXZpHdUQwuLZBhjckNkC