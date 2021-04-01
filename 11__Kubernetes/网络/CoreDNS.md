---
title: "CoreDNS.md"
date: 2020-03-24 09:58:51 +0800
lastmod: 2020-03-24 09:58:51 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


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





### 一些问题

#### ContainerCreating, Error from server (BadRequest)

``` sh
# kubectl get pods -A
NAMESPACE     NAME                              READY   STATUS              RESTARTS   AGE
kube-system   coredns-6955765f44-m2fqx          0/1     ContainerCreating   0          7m18s
kube-system   coredns-6955765f44-vd647          0/1     ContainerCreating   0          7m17s
kube-system   etcd-node200                      1/1     Running             0          7m46s
kube-system   kube-apiserver-node200            1/1     Running             1          7m46s
kube-system   kube-controller-manager-node200   1/1     Running             0          7m46s
kube-system   kube-proxy-5rvrq                  1/1     Running             0          7m18s
kube-system   kube-proxy-kmmhs                  1/1     Running             0          3m11s
kube-system   kube-scheduler-node200            1/1     Running             1          8m8s
```

查看日志：

```
kubectl logs coredns-6955765f44-m2fqx -n kube-system
Error from server (BadRequest): container "coredns" in pod "coredns-6955765f44-m2fqx" is waiting to start: ContainerCreating
```

添加网络插件后变为正常状态：

``` sh
kubectl apply -f /home/rambo/flannel1.yml

# kubectl get pods -A
NAMESPACE     NAME                              READY   STATUS    RESTARTS   AGE
kube-system   coredns-6955765f44-m2fqx          1/1     Running   0          15m
kube-system   coredns-6955765f44-vd647          1/1     Running   0          15m
```





## 调试k8s的DNS

起一个可用dns命令的pod:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: dnsutils
  namespace: default
spec:
  containers:
  - name: dnsutils
    image: gcr.io/kubernetes-e2e-test-images/dnsutils:1.3
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
```

或者使用：kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml

状态：

``` sh
kubectl get pods dnsutils
NAME      READY     STATUS    RESTARTS   AGE
dnsutils   1/1       Running   0          <some-time>
```

运行nslookup命令：

``` sh
kubectl exec -ti dnsutils -- nslookup kubernetes.default
Server:    10.0.0.10
Address 1: 10.0.0.10

Name:      kubernetes.default
Address 1: 10.0.0.1
```



### nslookup 运行出错

可能会出现：

```sh
/ # nslookup kubernetes.default
;; connection timed out; no servers could be reached

# 或
kubectl exec -ti dnsutils -- nslookup kubernetes.default
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'kubernetes.default'

# 或
kubectl exec -ti dnsutils -- nslookup kubernetes.default
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'kubernetes.default'
```

看一下 resolv.conf 文件：

```shell
kubectl exec -ti dnsutils -- cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local 
nameserver 10.0.0.10
options ndots:5
```

确认搜索路径和服务名，不同的云服务商可能不一样

确认DNS pod 运行状态是running:

也可能会出现  can't resolve：

``` sh
# nslookup google.com
nslookup: can't resolve '(null)': Name does not resolve

Name:      google.com
Address 1: 172.217.164.110 sfo03s18-in-f14.1e100.net
Address 2: 2607:f8b0:4005:80b::200e sfo03s18-in-x0e.1e100.net

# 指定 dns 
nslookup google.com 8.8.8.8
Server:    8.8.8.8
Address 1: 8.8.8.8 dns.google

Name:      google.com
Address 1: 172.217.164.110 sfo03s18-in-f14.1e100.net
Address 2: 2607:f8b0:4005:80b::200e sfo03s18-in-x0e.1e100.net
```

这是个bug,新版本应该已经修复。



### DNS Pod 运行状态

CoreDNS:

``` sh
kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
NAME                       READY     STATUS    RESTARTS   AGE
...
coredns-7b96bf9f76-5hsxb   1/1       Running   0           1h
coredns-7b96bf9f76-mvmmt   1/1       Running   0           1h
...
```

Kube-dns:

```sh
kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
NAME                    READY     STATUS    RESTARTS   AGE
...
kube-dns-v19-ezo1y      3/3       Running   0           1h
...
```



### DNS log

``` sh
 for p in $(kubectl get pods --namespace=kube-system -l k8s-app=kube-dns -o name); do kubectl logs --namespace=kube-system $p; done
.:53
[INFO] plugin/reload: Running configuration MD5 = 4e235fcc3696966e76816bcd9034ebc7
CoreDNS-1.6.5
linux/amd64, go1.13.4, c2fd1b2
[ERROR] plugin/errors: 2 6936741458835321801.4609081455828696090. HINFO: read udp 10.244.0.3:54867->192.168.59.241:53: i/o timeout
[ERROR] plugin/errors: 2 6936741458835321801.4609081455828696090. HINFO: read udp 10.244.0.3:48954->192.168.59.241:53: i/o timeout
...: read udp 10.244.0.3:36185->192.168.59.241:53: i/o timeout
[ERROR] plugin/errors: 2 6936741458835321801.4609081455828696090. HINFO: read udp 10.244.0.3:38958->192.168.59.241:53: i/o timeout
.:53
[INFO] plugin/reload: Running configuration MD5 = 4e235fcc3696966e76816bcd9034ebc7
CoreDNS-1.6.5
linux/amd64, go1.13.4, c2fd1b2
[ERROR] plugin/errors: 2 6074140797085019225.7868176384750749927. HINFO: read udp 10.244.0.2:34279->192.168.59.241:53: i/o timeout
[ERROR] plugin/errors: 2 6074140797085019225.7868176384750749927. HINFO: read udp 10.244.0.2:57237->192.168.59.241:53: i/o timeout
[ERROR] plugin/errors: 2 6074140797085019225.7868176384750749927. HINFO: ...
[ERROR] plugin/errors: 2 6074140797085019225.7868176384750749927. HINFO: read udp 10.244.0.2:58751->192.168.59.241:53: i/o timeout
```

这里为什么会使用主机的dns设置, 因为coredns默认会读取主机的dns配置：

/etc/systemd/resolved.conf:

```sh
[Resolve]
DNS=192.168.59.241
#Domains=
#LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
#DNSStubListener=yes
```

可以参考：

https://segmentfault.com/a/1190000015639327

https://github.com/easzlab/kubeasz/issues/423 

https://github.com/coredns/coredns/issues/2087

https://segmentfault.com/a/1190000015639327 这里说是可以把dns换成 kube-dns 的 ip

https://kubernetes.io/zh/docs/tasks/administer-cluster/dns-debugging-resolution/ 官方也说明了 ubuntu 16 或 18 可能会有这种dns问题



去掉 loop 后又出现新的问题：

###  dial tcp 10.96.0.1:443: i/o timeout

可能是之前的cni0和现在用的子网范围不一致导致的：

```sh
root@node200:~# ip r
10.244.0.0/24 dev cni0 proto kernel scope link src 10.244.0.1 linkdown

# kubeadm init --pod-network-cidr=10.244.0.0/16
```

删除 cn0,重新reset 即可：

``` sh
ip link delete cni0
```





### DNS service 

```shell
kubectl get svc --namespace=kube-system
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
...
kube-dns     ClusterIP   10.0.0.10      <none>        53/UDP,53/TCP        1h
...
```

endpoints暴露了么？

 `kubectl get endpoints` command：

```shell
kubectl get ep kube-dns --namespace=kube-system
NAME       ENDPOINTS                       AGE
kube-dns   10.180.3.17:53,10.180.3.17:53    1h
```





### 添加log输出

在coredns添加log插件：

``` sh 
kubectl -n kube-system edit configmap coredns

apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        log   # ！
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          upstream
          fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        proxy . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }

```



### 编辑 coredns 的configmap

kubectl edit cm coredns -n kube-system

编辑后保存，删掉原来的coredns pod:

``` sh
kubectl get pods -n kube-system -oname |grep coredns |xargs kubectl delete -n kube-system
```



