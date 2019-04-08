

官方提供了 CLI 工具 `kubectl` 用于完成大多数集群管理相关的功能。当然凡是你可以通过 `kubectl`完成的与集群交互的功能，都可以直接通过 API 完成。

一般的用法 `kubectl [flags] [options]` 



在我们的用户家目录，可以看到一个名为 `.kube/config` 的配置文件，主要包含

- K8S 集群的 API 地址
- 用于认证的证书地址



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



### run

```
Usage:
  kubectl run NAME --image=image [--env="key=value"] [--port=port] [--replicas=replicas] [--dry-run=bool] [--overrides=inline-json] [--command] -- [COMMAND] [args...] [options]
```

`NAME` 和 `--image` 是必需项。分别代表此次部署的名字及所使用的镜像，其余部分之后进行解释。当然，在我们实际使用时，推荐编写配置文件并通过 `kubectl create` 进行部署。

eg:  部署redis 实例

在 Redis 的[官方镜像列表](https://link.juejin.im/?target=https%3A%2F%2Fhub.docker.com%2F_%2Fredis%2F)可以看到有很多的 tag 可供选择，其中使用 [Alpine Linux](https://link.juejin.im/?target=https%3A%2F%2Falpinelinux.org) 作为基础的镜像体积最小，下载较为方便。我们选择 `redis:alpine` 这个镜像进行部署。

```
[root@localhost k8s]# kubectl run redis --image='redis:alpine'
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/redis created
[root@localhost k8s]# kubectl run redis --image='redis:alpine' --generator=run-pod/v1
pod/redis created
[root@localhost k8s]# kubectl get all
NAME                        READY   STATUS    RESTARTS   AGE
pod/redis                   0/1     Pending   0          8s
pod/redis-c55dbd898-dc2xm   0/1     Pending   0          2m6s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   92m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis   0/1     1            0           2m6s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/redis-c55dbd898   1         1         0       2m6s
[root@localhost k8s]#
```

刚才执行 `run` 操作后创建的 `deployment.apps/redis`，还有 `replicaset.apps/redis-7c7545cbcb`, `service/kubernetes` 以及 `pod/redis-7c7545cbcb-f984p`。

使用 `kubectl get all` 输出内容的格式 `/` 前代表类型，`/` 后是名称。

`Deployment` 是一种高级别的抽象，允许我们进行扩容，滚动更新及降级等操作。

还有一个作用是将`Pod` 托管给下面将要介绍的 `ReplicaSet`。



我们上面已经提到 `Deployment` 主要是声明一种预期的状态，并且会将 `Pod` 托管给 `ReplicaSet`，而 `ReplicaSet` 则会去检查当前的 `Pod` 数量及状态是否符合预期，并尽量满足这一预期。

`ReplicaSet` 可以由我们自行创建，但一般情况下不推荐这样去做，因为如果这样做了，那其实就相当于跳过了 `Deployment` 的部分，`Deployment` 所带来的功能或者特性我们便都使用不到了。

除了 `ReplicaSet` 外，我们还有一个选择名为 `ReplicationController`，这两者的主要区别更多的在选择器上，我们后面再做讨论。现在推荐的做法是 `ReplicaSet` 所以不做太多解释。

`ReplicaSet` 可简写为 `rs`，通过以下命令查看：

```
[root@localhost k8s]# kubectl get rs -o wide
NAME              DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES         SELECTOR
redis-c55dbd898   1         1         0       8m17s   redis        redis:alpine   pod-template-hash=c55dbd898,run=redis
```

在输出结果中，我们注意到这里除了我们前面看到的 `run=redis` 标签外，还多了一个 `pod-template-hash=3731017676` 标签，这个标签是由 `Deployment controller` 自动添加的，目的是为了防止出现重复，所以将 `pod-template` 进行 hash 用作唯一性标识。



service

`Service` 简单点说就是为了能有个稳定的入口访问我们的应用服务或者是一组 `Pod`。通过 `Service`可以很方便的实现服务发现和负载均衡

```
[root@localhost k8s]# kubectl get service -o wide
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE    SELECTOR
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   145m   <none>
```

通过使用 `kubectl` 查看，能看到主要会显示 `Service` 的名称，类型，IP，端口及创建时间和选择器等。我们来具体拆解下。

#### 类型

`Service` 目前有 4 种类型：

- `ClusterIP`： 是 K8S 当前默认的 `Service` 类型。将 service 暴露于一个仅集群内可访问的虚拟 IP 上。
- `NodePort`： 是通过在集群内所有 `Node` 上都绑定固定端口的方式将服务暴露出来，这样便可以通过 `<NodeIP>:<NodePort>` 访问服务了。
- `LoadBalancer`： 是通过 `Cloud Provider` 创建一个外部的负载均衡器，将服务暴露出来，并且会自动创建外部负载均衡器路由请求所需的 `Nodeport` 或 `ClusterIP` 。
- `ExternalName`： 是通过将服务由 DNS CNAME 的方式转发到指定的域名上将服务暴露出来，这需要 `kube-dns` 1.7 或更高版本支持。



#### expose

已经部署了一个 Redis ,当还无法访问到该服务，接下来我们将刚才部署的 Redis 服务暴露出来。

```
[root@localhost k8s]# kubectl expose deploy/redis --port=6379 --protocol=TCP --target-port=6379 --name=redis-server
service/redis-server exposed

[root@localhost k8s]# kubectl get  svc -o wide
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE    SELECTOR
kubernetes     ClusterIP   10.96.0.1       <none>        443/TCP    148m   <none>
redis-server   ClusterIP   10.108.147.36   <none>        6379/TCP   69s    run=redis
```

现在我们的 redis 是使用的默认类型 `ClusterIP`，所以并不能直接通过外部进行访问，我们使用 `port-forward` 的方式让它可在集群外部访问。

```
➜  ~ kubectl port-forward svc/redis-server 6379:6379
Forwarding from 127.0.0.1:6379 -> 6379
Forwarding from [::1]:6379 -> 6379
Handling connection for 6379
```

在另一个本地终端内可通过 redis-cli 工具进行连接：

```
➜  ~ redis-cli -h 127.0.0.1 -p 6379
127.0.0.1:6379> ping
PONG
```

