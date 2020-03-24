Tags:[k8s]

 `Service` 的 4 种基础类型，在前面的介绍中，我们一般都在使用 `ClusterIP`或 `NodePort` 等方式将服务暴露在集群内或者集群外。

介绍另一种处理服务访问的方式 `Ingress`。



`Ingress` 是一组允许外部请求进入集群的路由规则的集合。它可以给 `Service` 提供集群外部访问的 URL，负载均衡，SSL 终止等。

直白点说，`Ingress` 就类似起到了智能路由的角色，外部流量到达 `Ingress` ，再由它按已经制定好的规则分发到不同的后端服务中去。

看起来它很像我们使用的负载均衡器之类的。那你可能会问，`Ingress` 与 `LoadBalancer` 类型的 `Service` 的区别是什么呢？

- `Ingress` 不是一种 `Service` 类型

  `Ingress` 是 K8S 中的一种资源类型，我们可以直接通过 `kubectl get ingress` 的方式获取我们已有的 `Ingress` 资源。

- `Ingress` 可以有多种控制器（实现）

  通过之前的介绍，我们知道 K8S 中有很多的 `Controller` (控制器)，而这些 `Controller` 已经打包进了 `kube-controller-manager` 中，通过 `--controllers` 参数控制启用哪些。

  但是 `Ingress` 的 `Controller` 并没有包含在其中，而且有多种选择。