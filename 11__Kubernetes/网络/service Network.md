

我觉得Service IP只能算一种假IP，除了在iptables中有相应的规则链，并没有任何网络链路的底层实现。所以我觉得它更像是一种集群内的“域名”，通过kube-proxy设置的iptables规则进行“DNS”解析，最终访问到对应的Pod。具体可以看看上一篇中关于kube-proxy的内容。

###  外部访问Service

另外这个虚拟的Service IP(Cluster IP)只能在集群内部才能访问到，如果要从外部访问，可以用一下几种方式：

- Porxy API

这种是直接使用apiserver，通过Proxy API将访问请求转发到对应服务的ClusterIP上。比如访问grafana服务：http://localhost:8080/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy/

![k8s-sevice-clusterip](https://gitee.com/ClayAndMore/image/raw/master/k8s-sevice-clusterip.png)

- NodePort

NodePort是把服务的端口映射到集群每一个Node上的某一个端口上，这样访问集群中任意一个Node的请求都可以被转发到对应的服务的ClusterIP上。

![k8s-sevice-Nodeip](https://gitee.com/ClayAndMore/image/raw/master/k8s-sevice-Nodeip.png)

- LoadBalancer

LoadBalancer是使用云服务提供商的负载均衡器，将来自外网的访问请求转发到ClusterIP上。



![k8s-sevice-loadbanance](https://gitee.com/ClayAndMore/image/raw/master/k8s-sevice-loadbanance.png)

以上三中方式都是Service的type所支持的类型。但各有各的问题，ClusterIP通常只适合debug时访问，因为apiserver的权限过大。而NodePort是直接将集群的Node暴露在外，而且每一个服务就要占用一个端口，非常不便于管理。LoadBalancer一般都是服务提供商付费使用。

- Ingress

Ingress感觉就是一个nginx反代，依据不同的server_name将请求转发给不同的Service。只需要暴露一个入口，就可以访问到集群内很多的服务。Ingress并不是Service的一种，而是对集群内Service入口的统一管理。

![k8s-sevice-ingress](https://gitee.com/ClayAndMore/image/raw/master/k8s-sevice-ingress.png)