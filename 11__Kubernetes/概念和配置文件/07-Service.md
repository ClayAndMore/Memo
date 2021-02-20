---

title: "07-k8s中Service端口映射.md"
date: 2020-10-28 18:45:29 +0800
lastmod: 2020-10-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---



## pod中的端口映射

pod 的yaml 文件中也可以映射端口，分为 containerPort 和 hostPort

``` yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-run
  name: nginx-name
spec:
  containers:
  - image: nginx:alpine
    name: nginx-test
    ports:
    - containerPort: 80
      hostPort: 8111
```

* contanierPort pod中的容器需要暴露的端口，这里是nginx默认使用80，我们需要将它暴露出来，如果是其他服务或者你指定了其他端口，这里要变化。**这样可以通过 POD IP 来访问服务。**

* hostPort **这样可以通过 Pod 所在 Node 的 IP:hostPort 来访问服务**， 使用了 hostPort 的容器只能调度到端口不冲突的 Node 上。

测试：

``` sh
node200# kubectl get pods -A -o wide
NAMESPACE     NAME        READY   STATUS    RESTARTS   AGE     IP            NODE
default       nginx-name   1/1     Running   0          2m36s   10.244.1.27   node201

# 目前我的位置在node200，pod运行在node201上，可以通过 podip：containerport 来访问
# curl 10.244.1.27:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
#  通过hostPort 来访问：
# curl node200:8111
curl: (7) Failed to connect to node200 port 8111: Connection refused
# curl node201:8111
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```

浏览器可以通过访问201的地址8111端口访问，但是在我node201上 lsof -i:8111并没有看到端口的使用情况，比较疑惑。



## Service

Kubernetes 在设计之初就充分考虑了针对容器的服务发现与负载均衡机制，提供了 Service 资源，并通过 kube-proxy 配合 cloud provider 来适应不同的应用场景,直接用 Service 提供 cluster 内部的负载均衡.

Service 有四种类型：

- ClusterIP：默认类型，自动分配一个仅 cluster 内部可以访问的虚拟 IP
- NodePort：在 ClusterIP 基础上为 Service 在每台机器上绑定一个端口，这样就可以通过 `<NodeIP>:NodePort` 来访问该服务。如果 kube-proxy 设置了 `--nodeport-addresses=10.240.0.0/16`（v1.10 支持），那么仅该 NodePort 仅对设置在范围内的 IP 有效。
- LoadBalancer：在 NodePort 的基础上，借助 cloud provider 创建一个外部的负载均衡器，并将请求转发到 `<NodeIP>:NodePort`
- ExternalName：将服务通过 DNS CNAME 记录方式转发到指定的域名（通过 `spec.externlName` 设定）。需要 kube-dns 版本在 1.7 以上。

比如下面定义了一个名为 nginx 的服务，将服务的 80 端口转发到 default namespace 中**带有标签 `run=nginx` 的 Pod** 的 80 端口:

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
  namespace: default
spec:
  ports:
  - port: 8222
    protocol: TCP
    targetPort: 80
  selector:
    run: nginx-run
  sessionAffinity: None
  type: ClusterIP
```

接下来看下 port 和 targetPort

### Port

port是暴露在cluster ip上的端口，:port提供了集群内部客户端访问service的入口，即`clusterIP:port`

``` sh
# kubectl get svc -o wide
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    23h   <none>
nginx-svc    ClusterIP   10.101.14.144   <none>        8222/TCP   14s   run=nginx-run

# l# curl 10.101.14.144:8222
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```



### TargetPort

TargetPort很好理解，targetPort是pod上暴露的端口，从port和nodePort上到来的数据最终经过kube-proxy流入到后端pod的targetPort上进入容器。



### NodePort

nodePort是kubernetes提供给集群外部客户访问service入口的一种方式，所以，`<nodeIP>:nodePort` 是提供给集群外部客户访问service的入口。

**端口范围在 30000-32767**

重新改一下yaml:

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
  namespace: default
spec:
  ports:
  - port: 8222
    protocol: TCP
    targetPort: 80
    nodePort: 30333
  selector:
    run: nginx-run
  sessionAffinity: None
  type: NodePort
```

应用看下服务

``` sh
# kubectl get svc -o wide
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          23h   <none>
nginx-svc    NodePort    10.104.51.182   <none>        8222:30333/TCP   9s    run=nginx-run
```

这里实际是把30333映射到了CLUSTER-IP上。

页面访问 node201:8111 和 node201:30333 均可以访问到，

但是访问 node200:8111 访问不到, node200:30333可以，**这里能说明使用serivce的好处了，而不是只接在定义pod中暴露。**



## 端口转发

端口转发是 kubectl 的一个子命令，通过 `kubectl port-forward` 可以将本地端口转发到指定的 Pod。

### Pod 端口转发

可以将本地端口转发到指定 Pod 的端口。

```sh
# Listen on ports 5000 and 6000 locally, forwarding data to/from ports 5000 and 6000 in the pod
kubectl port-forward mypod 5000 6000

# Listen on port 8888 locally, forwarding to 5000 in the pod
kubectl port-forward mypod 8888:5000

# Listen on a random port locally, forwarding to 5000 in the pod
kubectl port-forward mypod :5000

# Listen on a random port locally, forwarding to 5000 in the pod
kubectl port-forward mypod 0:5000
```

### 服务端口转发

也可以将本地端口转发到服务、复制控制器或者部署的端口。

```sh
# Forward to deployment
kubectl port-forward deployment/redis-master 6379:6379

# Forward to replicaSet
kubectl port-forward rs/redis-master 6379:6379

# Forward to service
kubectl port-forward svc/redis-master 6379:6379
```



## 使用dns使服务互访

如果想在其他pod中 访问上方的nginx， 我们可以使用dns保证访问地址的唯一性，这样方便于写配置文件：

```sh
# 查看该pod的dns：
root@node200:# kubectl exec -it pod/nginx-name cat /etc/resolv.conf
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5

# 在其他pod中访问：
# kubectl exec -it relationship-s-dp-68d794c79b-mhlrw  -n topsec -- wget nginx-svc.default.svc.cluster.local:8222
Connecting to nginx-svc.default.svc.cluster.local.:8222 (10.104.51.182:8222)
index.html           100% |********************************|   612  0:00:00 ETA
```

可以看到访问使用的是clusteip, **具体的使用格式为 `{server name}.{命名空间}.svc.cluster.local:{暴露的cluster port}`**

svc.cluster.local 有的时候会被改变，他跟cluster-name 相关，我们看kube-system的pod中的/etc/resolv.conf的时候可以观察到，默认的是这样的：

``` 
# kubectl config get-clusters
NAME
kubernetes
```



或者 

比如，一个default空间的pod里要访问kube-system空间里的tomcat-dm服务，用如下方式：

```
curl http://tomcat-dm.kube-system:8087
```





## service 之间互相访问

集群中的service访问另一个service时，不同的namespace，一定要加上这个名字空间才能互访。





## 其他

### 调试service 

https://kubernetes.io/zh/docs/tasks/debug-application-cluster/debug-service/