Tags:[k8s]

官方提供了 CLI 工具 `kubectl` 用于完成大多数集群管理相关的功能。当然凡是你可以通过 `kubectl`完成的与集群交互的功能，都可以直接通过 API 完成。

一般的用法 `kubectl [flags] [options]` 

``` 
[root@master131 ~]# kubectl --help
kubectl controls the Kubernetes cluster manager.

 Find more information at: https://kubernetes.io/docs/reference/kubectl/overview/

Basic Commands (Beginner):
  create         Create a resource from a file or from stdin.
  expose         使用 replication controller, service, deployment 或者 pod 并暴露它作为一个 新的
Kubernetes Service
  run            在集群中运行一个指定的镜像
  set            为 objects 设置一个指定的特征

Basic Commands (Intermediate):
  explain        查看资源的文档
  get            显示一个或更多 resources
  edit           在服务器上编辑一个资源
  delete         Delete resources by filenames, stdin, resources and names, or by resources and label selector

Deploy Commands:
  rollout        Manage the rollout of a resource
  scale          Set a new size for a Deployment, ReplicaSet or Replication Controller
  autoscale      自动调整一个 Deployment, ReplicaSet, 或者 ReplicationController 的副本数量

Cluster Management Commands:
  certificate    修改 certificate 资源.
  cluster-info   显示集群信息
  top            Display Resource (CPU/Memory/Storage) usage.
  cordon         标记 node 为 unschedulable
  uncordon       标记 node 为 schedulable
  drain          Drain node in preparation for maintenance
  taint          更新一个或者多个 node 上的 taints

Troubleshooting and Debugging Commands:
  describe       显示一个指定 resource 或者 group 的 resources 详情
  logs           输出容器在 pod 中的日志
  attach         Attach 到一个运行中的 container
  exec           在一个 container 中执行一个命令
  port-forward   Forward one or more local ports to a pod
  proxy          运行一个 proxy 到 Kubernetes API server
  cp             复制 files 和 directories 到 containers 和从容器中复制 files 和 directories.
  auth           Inspect authorization

Advanced Commands:
  diff           Diff live version against would-be applied version
  apply          通过文件名或标准输入流(stdin)对资源进行配置
  patch          使用 strategic merge patch 更新一个资源的 field(s)
  replace        通过 filename 或者 stdin替换一个资源
  wait           Experimental: Wait for a specific condition on one or many resources.
  convert        在不同的 API versions 转换配置文件
  kustomize      Build a kustomization target from a directory or a remote url.

Settings Commands:
  label          更新在这个资源上的 labels
  annotate       更新一个资源的注解
  completion     Output shell completion code for the specified shell (bash or zsh)

Other Commands:
  api-resources  Print the supported API resources on the server
  api-versions   Print the supported API versions on the server, in the form of "group/version"
  config         修改 kubeconfig 文件
  plugin         Provides utilities for interacting with plugins.
  version        输出 client 和 server 的版本信息
```



使用 `kubectl options` 可以看到所有全局可用的配置项。

在我们的用户家目录，可以看到一个名为 `.kube/config` 的配置文件，主要包含

- K8S 集群的 API 地址
- 用于认证的证书地址

``` yaml
[root@master131 ~]# cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1C...3T3FrSHY1ZW9Raz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    server: https://192.168.145.131:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiB...NBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBSU0Eg...WHZRUVVXcFcvTGFWRUpjRC9BRVpQMFh1Qm0rNgpRVWJjVzZaV05ZSktseGNUUG
```

另外如果你并不想使用配置文件的话，你也可以通过使用直接传递相关参数来使用，例如：

```
➜  ~ kubectl --client-key='/home/tao/.minikube/client.key' --client-certificate='/home/tao/.minikube/client.crt' --server='https://192.168.99.101:8443'  get nodes
NAME       STATUS    ROLES     AGE       VERSION
minikube   Ready     master    2d        v1.11.3
```





### get

kubectl get nodes, 可以获得集群信息

如果我们想要看到更详细的信息呢？可以通过传递 `-o` 参数以得到不同格式的输出。

```
➜  ~ kubectl get nodes -o wide 
NAME       STATUS    ROLES     AGE       VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE            KERNEL-VERSION   CONTAINER-RUNTIME
minikube   Ready     master    2d        v1.11.3   10.0.2.15     <none>        Buildroot 2018.05   4.15.0           docker://17.12.1-ce
```

当然也可以传递 `-o yaml` 或者 `-o json` 得到更加详尽的信息。

使用 `-o json` 将内容以 JSON 格式输出时，可以配合 [`jq`](https://link.juejin.im/?target=https%3A%2F%2Fstedolan.github.io%2Fjq%2F) 进行内容提取。例如：

```
➜  ~ kubectl get nodes -o json | jq ".items[] | {name: .metadata.name} + .status.nodeInfo"
{
  "name": "minikube",
  "architecture": "amd64",
  "bootID": "d675d75b-e58e-40db-8910-6e5dda9e7cf9",
  "containerRuntimeVersion": "docker://17.12.1-ce",
  "kernelVersion": "4.15.0",
  "kubeProxyVersion": "v1.11.3",
  "kubeletVersion": "v1.11.3",
  "machineID": "078e2d22629747178397e29cf1c96cc7",
  "operatingSystem": "linux",
  "osImage": "Buildroot 2018.05",
  "systemUUID": "4073906D-69A1-46EE-A08C-0252D9F79893"
}
```



其他用法：

``` 
  # List a single replication controller with specified NAME in ps output format.
  kubectl get replicationcontroller web

  # List deployments in JSON output format, in the "v1" version of the "apps" API group:
  kubectl get deployments.v1.apps -o json

  # List a single pod in JSON output format.
  kubectl get -o json pod web-pod-13je7

  # List a pod identified by type and name specified in "pod.yaml" in JSON output format.
  kubectl get -f pod.yaml -o json

  # List resources from a directory with kustomization.yaml - e.g. dir/kustomization.yaml.
  kubectl get -k dir/

  # Return only the phase value of the specified pod.
  kubectl get -o template pod/web-pod-13je7 --template={{.status.phase}}

  # List resource information in custom columns.
  kubectl get pod test-pod -o custom-columns=CONTAINER:.spec.containers[0].name,IMAGE:.spec.containers[0].image

  # List all replication controllers and services together in ps output format.
  kubectl get rc,services

  # List one or more resources by their type and names.
  kubectl get rc/web service/frontend pods/web-pod-13je7
```





### explain

通过 `kubectl api-resources` 查看服务端支持的 API 资源及别名和描述等信息。拿到所有支持的 API 资源列表后，虽然后面基本都有一个简单的说明，是不是仍然感觉一头雾水？

使用 `kubectl` 的时候，我们除了 `--help` 外还有 `explain` 可帮我们进行说明。 例如：

``` 
root@master131 ~]# kubectl explain node
KIND:     Node
VERSION:  v1

DESCRIPTION:
     Node is a worker node in Kubernetes. Each node will have a unique
     identifier in the cache (i.e. in etcd).

FIELDS:
   apiVersion	<string>
     APIVersion defines the versioned schema of this representation of an
     object. Servers should convert recognized schemas to the latest internal
     value, and may reject unrecognized values. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

   kind	<string>
     Kind is a string value representing the REST resource this object
     represents. Servers may infer this from the endpoint the client submits
     requests to. Cannot be updated. In CamelCase. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

   metadata	<Object>
     Standard object's metadata. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

   spec	<Object>
     Spec defines the behavior of a node.
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

   status	<Object>
     Most recently observed status of the node. Populated by the system.
     Read-only. More info:
     https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

```



### run

kubectl run 用来在集群中运行一个指定的镜像

```
Usage:
  kubectl run NAME --image=image [--env="key=value"] [--port=port] [--replicas=replicas] [--dry-run=bool] [--overrides=inline-json] [--command] -- [COMMAND] [args...] [options]
```

`NAME` 和 `--image` 是必需项。分别代表此次部署的名字及所使用的镜像，其余部分之后进行解释。当然，在我们实际使用时，推荐编写配置文件并通过 `kubectl create` 进行部署。

eg:  部署redis 实例



### expose

使用 replication controller, service, deployment 或者 pod 并暴露它作为一个 新的 Kubernetes Service

eg: `kubectl expose deploy/redis --port=6379 --protocol=TCP --target-port=6379 --name=redis-server`



待补充：

- **kubectl describe** - 显示资源的详细信息
- **kubectl logs** - 打印pod中的容器日志
- **kubectl exec** - pod中容器内部执行命令