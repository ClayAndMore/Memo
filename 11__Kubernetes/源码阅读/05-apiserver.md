### go-restful框架

[go-restful](https://github.com/emicklei/go-restful)是一个用go语言开发的快速构建restful风格的web框架。k8s最核心的组件kube-apiserver使用到了该框架，该框架的代码比较精简，这里做个简单的功能介绍，然后分析相关源码。

go-restful基于golang官方的net/http实现

go-restful定义了三个重要的数据结构：

- Router：表示一条路由，包含url、回调处理函数
- Webservice：表示一个服务
- Container：表示一个服务器

go-restful并不是一个热度很高的golang web框架，但是k8s中用到了它，本篇文章通过源码分析对go-restful的内部实现做了简单的分析。从分析的过程来看，确实是一个精悍小巧的框架。内部更深入的功能我们没有继续研究了，只要达到能看懂k8s kube-apiserver组件源码的目的就行。

内部核心实现只要是：

- 通过http包默认的路由对象DefaultServeMux添加处理函数dispatch
- 路由分发功能全部转给dispatch
- dispatch内部调用RouteSelector的默认实现类CurlyRouter的SelectRoute方法选择合适的Route
- 调用Route中注册的handler方法，处理请求

https://cloud.tencent.com/developer/article/1717413



### api

以下为常用资源的URL路径，将/apis/GROUP/VERSION/替换为/api/v1/,则表示基础API组：

```javascript
/apis/GROUP/VERSION/RESOURCETYPE
/apis/GROUP/VERSION/RESOURCETYPE/NAME
/apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE
/apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME
/apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE
/apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE
```

![image-20210325110740980](https://gitee.com/ClayAndMore/image/raw/master/k8s-apiserver-api.png)



1. API group, 在逻辑上相关的一组 Kind 集合。如 Job 和 ScheduledJob 都在 batch API group 里。
2. Version, 标示 API group 的版本更新， API group 会有多个版本 (version)。v1alpha1: 初次引入 ==> v1beta1: 升级改进 ==> v1: 开发完成毕业。 group + domain + version 在url 上经常体现为`$group_$domain/version` 比如 `batch.tutorial.kubebuilder.io/v1`
3. Kind, 表示实体的类型。直接对应一个Golang的类型，会持久化存储在etcd 中
4. Resource, 通常是小写的复数词，Kind 的小写形式（例如，pods），用于标识一组 HTTP 端点（路径），来对外暴露 CURD 操作。每个 Kind 和 Resource 都存在于一个APIGroupVersion 下，分别通过 GroupVersionKind 和 GroupVersionResource 标识。关联GVK 到GVR （资源存储与http path）的映射过程称作 REST mapping。

通常情况下，Kind 和 resources 之间有一个一对一的映射。 例如，pods 资源对应于 Pod 种类。但是有时，同一类型可能由多个资源返回。例如，Scale Kind 是由所有 scale 子资源返回的，如 deployments/scale 或 replicasets/scale。这就是允许 Kubernetes HorizontalPodAutoscaler(HPA) 与不同资源交互的原因。然而，使用 CRD，每个 Kind 都将对应一个 resources。

可以通过 api-resources 来看所有的group.



### 工作原理

#### 分层

kube-apiserver 提供了 Kubernetes 的 REST API，实现了认证、授权、准入控制等安全校验功能，同时也负责集群状态的存储操作（通过 etcd）。

![image-20210324190414162](https://gitee.com/ClayAndMore/image/raw/master/image-20210324190414162.png)

#### 存储层

位于 `k8s.io/apiserver/pkg/storage` 下

```
// k8s.io/apiserver/pkg/storage/interface.go
type Interface interface {
    Versioner() Versioner
    Create(ctx context.Context, key string, obj, out runtime.Object, ttl uint64) error
    Delete(ctx context.Context, key string, out runtime.Object, preconditions *Preconditions) error
    Watch(ctx context.Context, key string, resourceVersion string, p SelectionPredicate) (watch.Interface, error)
    Get(ctx context.Context, key string, resourceVersion string, objPtr runtime.Object, ignoreNotFound bool) error
    List(ctx context.Context, key string, resourceVersion string, p SelectionPredicate, listObj runtime.Object) error
    ...
}
```

封装了对etcd 的操作，还提供了一个cache 以减少对etcd 的访问压力。在Storage这一层，并不能感知到k8s资源对象之类的内容，纯粹的存储逻辑。

#### registry 层

实现各种资源对象的存储逻辑

1. `kubernetes/pkg/registry`负责k8s内置的资源对象存储逻辑实现
2. `k8s.io/apiextensions-apiserver/pkg/registry`负责crd和cr资源对象存储逻辑实现



参考： https://qiankunli.github.io/2019/01/05/kubernetes_source_apiserver.html