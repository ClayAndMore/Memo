在 K8S 中有一套默认[集群内 DNS 服务，我们通常把它叫做 `kube-dns`，它基于 SkyDNS，为我们在服务注册发现方面提供了很大的便利。

比如，在我们的示例项目 [SayThx]中，各组件便是依赖 DNS 进行彼此间的调用。

CoreDNS是 CNCF 旗下又一孵化项目，在 K8S 1.9 版本中加入并进入 Alpha 阶段。

我们当前是以 K8S 1.11 的版本进行介绍，它并不是默认的 DNS 服务，但是它作为 K8S 的 DNS 插件的功能已经 GA 。

CoreDNS 在 K8S 1.13 版本中才正式成为默认的 DNS 服务。



首先，我们需要明确 CoreDNS 是一个独立项目，它不仅可支持在 K8S 中使用，你也可以在你任何需要 DNS 服务的时候使用它。

CoreDNS 使用 Go 语言实现，部署非常方便。

它的扩展性很强，很多功能特性都是通过插件完成的，它不仅有大量的[内置插件](https://link.juejin.im/?target=https%3A%2F%2Fcoredns.io%2Fplugins%2F)，同时也有很丰富的[第三方插件](https://link.juejin.im/?target=https%3A%2F%2Fcoredns.io%2Fexplugins%2F)。甚至你自己[写一个插件](https://link.juejin.im/?target=https%3A%2F%2Fcoredns.io%2F2016%2F12%2F19%2Fwriting-plugins-for-coredns%2F)也非常的容易。



### 安装

github: https://github.com/coredns/coredns

使用 `kubeadm` 创建集群时候 `kubeadm init` 可以传递 `--feature-gates` 参数，用于启用一些额外的特性。

比如在之前版本中，我们可以通过 `kubeadm init --feature-gates CoreDNS=true` 在创建集群时候启用 CoreDNS。

而在 1.11 版本中，使用 `kubeadm` 创建集群时 `CoreDNS` 已经被默认启用，这也从侧面证明了 CoreDNS 在 K8S 中达到了生产可用的状态。

集群创建完成后，可用过以下方式进行查看：

```
[root@192.168.18.196 saythx_k8s]#kubectl -n kube-system get all  -l k8s-app=kube-dns -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP            NODE             NOMINATED NODE   READINESS GATES
pod/coredns-fb8b8dccf-dbrcl   1/1     Running   0          3h28m   10.244.0.47   192.168.18.196   <none>           <none>
pod/coredns-fb8b8dccf-q62p9   1/1     Running   0          3h28m   10.244.0.46   192.168.18.196   <none>           <none>

NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE     SELECTOR
service/kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   3h28m   k8s-app=kube-dns

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                     SELECTOR
deployment.apps/coredns   2/2     2            2           3h28m   coredns      k8s.gcr.io/coredns:1.3.1   k8s-app=kube-dns

NAME                                DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES                     SELECTOR
replicaset.apps/coredns-fb8b8dccf   2         2         2       3h28m   coredns      k8s.gcr.io/coredns:1.3.1   k8s-app=kube-dns,pod-template-hash=fb8b8dccf
```

这里主要是为了兼容 K8S 原有的 `kube-dns` 所以标签和 `Service` 的名字都还使用了 `kube-dns`，但实际在运行的则是 CoreDNS。



### 配置和监控

CoreDNS 使用 `ConfigMap` 的方式进行配置，但是如果更改了配置，`Pod` 重启后才会生效。

我们通过以下命令可查看其配置：

```
root@192.168.18.196 saythx_k8s]#kubectl -n kube-system get configmap coredns -o yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           upstream
           fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2019-04-22T09:10:36Z"
  name: coredns
  namespace: kube-system
  resourceVersion: "207"
  selfLink: /api/v1/namespaces/kube-system/configmaps/coredns
  uid: 7d8d714c-64de-11e9-8400-801844f349cc
```

