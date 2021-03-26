## kubernets 网络模式

Kubernetes与Docker网络有些不同。Kubernetes网络需要解决下面的4个问题：

集群内：

- 容器与容器之间的通信
- Pod和Pod之间的通信
- Pod和服务之间的通信

集群外：

- 外部应用与服务之间的通信



### 同一pod容器的通信

Kubernetes 创建 Pod 时，首先会创建一个 pause 容器，为 Pod 指派一个唯一的IP地址。然后，以pause的网络命名空间为基础，创建同一个Pod内的其它容器：

``` sh
root@node201:~# docker ps | grep nginx
2a341e1a3227        ea1819c829a5                                            "/docker-entrypoint.…"   4 days ago          Up 4 days                               k8s_nginx2-server_nginx-test-2-xxx-25f1aff3f999_0
b2d21efed21d        k8s.gcr.io/pause:3.1                                    "/pause"                 4 days ago          Up 4 days                               k8s_POD_nginx-test-2-7695864f48-xxxx-25f1aff3f999_0

root@node201:~# docker inspect 2a341e1a3227 | grep NetworkMode
            "NetworkMode": "container:b2d21efed21d92dd7b1c40849e8eb38e67bc14f35a0f1e02f4a98c10b911a105",
```

在这个nginx pod 中， nginx容器通过`"NetworkMode": "container:d2db..."`与pause容器共享了网络，更具体的说，是共享一个Network Namespace中的一个IP。

所以同一个Pod内的所有容器就会共享同一个网络命名空间，在同一个Pod之间的容器可以直接使用localhost进行通信。



#### docker0

然而pause的ip又是从哪里分配到的？如果还是用一个以docker0为网关的内网ip就会出现问题了。

docker默认的网络是为同一台宿主机的docker容器通信设计的，Kubernetes的Pod需要跨主机与其他Pod通信，所以需要设计一套让不同Node的Pod实现透明通信（without NAT）的机制。

docker0的默认ip是172.17.0.1，docker启动的容器也默认被分配在172.17.0.1/16的网段里。跨主机的Pod通信要保证Pod的ip不能相同，所以还需要设计一套为Pod统一分配IP的机制。

这时就需要网络插件来提供跨主机的通讯，官方的一些插件：https://kubernetes.io/docs/concepts/cluster-administration/networking/#how-to-achieve-this



### flannel

flannel 是 kubernetes 默认提供网络插件, Flannel 是由 CoreOS 团队开发社交的网络工具， **规定宿主机下各个Pod属于同一个子网，不同宿主机下的Pod属于不同的子网。**

flannel的主要作用：

* **flannel会在每一个宿主机上运行名为flanneld代理，其负责为宿主机预先分配一个子网，并为Pod分配IP地址。**
* **Flannel使用Kubernetes或etcd来存储网络配置、分配的子网和主机公共IP等信息。**
* **数据包则通过VXLAN、UDP或host-gw这些类型的后端机制进行转发**。

主要流程：

1. 首先在启动Kubernetes Controller Manager时，需要指定集群的pod ip范围：`--cluster-cidr=172.16.0.0/16`，Controller Manager会把为每个Node分配的IP范围保存到etcd中。
2. 新建Pod时，flannel会从etcd中取出属于该Node的ip，分配给Pod，再在etcd中记录下这个Pod的IP（这里涉及flannel分配ip的方式，后面重点说）。这样etcd中就会存有一张Node IP与Pod IP对应的“路由表”。
3. 当Pod需要跨Node通信时，数据包经过Node中的路由会到flannel中，flannel通过etcd查询到目的Pod IP的Node IP，使用flannel的Backends对数据包进行分装，发送给目的Node处理。目的Node拿到数据包后解开封装，拿到原始数据包，再通过Node的路由送到相应的Pod。
4. flannel的Backends有多种实现方式：VXLAN、UDP、gce.....具体参考[官方文档](https://github.com/coreos/flannel/blob/master/Documentation/backends.md)。官方推荐的是VXLAN，之前介绍docker swarm时就提到过，swarm的overlay网络也是通过VXLAN实现的。关于vxlan的具体实现原理可以参考[《vxlan 协议原理简介》](http://cizixs.com/2017/09/25/vxlan-protocol-introduction)。



**flanneld:**

每个节点上有一个fanneld进程， flanneld 可以直接通过 Etcd 管理 初始化时指定的 pod 大网的网段 `--pod-network-cidr=10.244.0.0/16`：

![flanneld](https://gitee.com/ClayAndMore/image/raw/master/flanneld.png)

``` sh
root@node200:~# ps aux |grep flannel
root     10535  0.1  0.3 694604 29284 ?        Ssl  3月12  10:59 /opt/bin/flanneld --ip-masq --kube-subnet-mgr
root     24150  0.0  0.0  16176  1052 pts/1    S+   01:40   0:00 grep --color=auto flannel
```





### 不同 pod 中容器之间的通信

flannel为Pod分配ip有不同的实现方式，Kubernetes推荐的是基于CNI，另一种是直接与docker结合。

#### 基于CNI

Container Network Interface (CNI) 最早是由CoreOS发起的容器网络规范，是Kubernetes网络插件的基础。其基本思想为：Container Runtime在创建容器时，先创建好network namespace，然后调用CNI插件为这个netns配置网络，其后再启动容器内的进程。现已加入CNCF，成为CNCF主推的网络模型。

![k8s-cni](https://gitee.com/ClayAndMore/image/raw/master/k8s-cni.png)



这个协议连接了两个组件：容器管理系统和网络插件。它们之间通过 JSON 格式的文件进行通信，实现容器的网络功能。具体的事情都是插件来实现的，包括：创建容器网络空间（network namespace）、把网络接口（interface）放到对应的网络空间、给网络接口分配 IP 等等。



使用CNI后，容器的IP分配就变成了如下步骤：

1. kubelet 先创建pause容器生成network namespace
2. 调用网络CNI driver， 根据配置调用具体的cni 插件
3. cni 插件给 pause 容器配置网络， pod 中其他的容器都使用 pause 容器的网络



##### cni0

这时候Pod就直接以`cni0`作为了自己的网关，而不是docker默认的docker0。所以使用`docker inspect`查看某个pause容器时，是看不到它的网络信息的。

![k8s-flannel-cni](C:\Users\wy\Pictures\blog\k8s-flannel-cni.png)

flannel 本身会创建一个类似下面这样配置的 CNI bridge 设备。

```json
{
    "name" : "cni0",
    "type" : "bridge",
    "mtu" : 8973,
    "ipMasq" : true,
    "isGateway" : true,
    "ipam" : {
        "type" : "host-local",
        "subnet" : "10.244.0.1/24",
         "routes" : [ { "dst" : "10.244.0.0/16" } ]
    }
}
```



#### 基于CNM

说一下docker的网络实现， docker主要用到了linux的`Bridge`、`Network Namespace`、`VETH`。

Network Namespace做了容器和宿主机的网络隔离，Bridge分别在容器和宿主机建立一个网关，然后再用VETH将容器和宿主机两个网络空间连接起来。

基于上面的网络实现，docker的容器网络管理项目libnetwork提出了CNM（container network model)模型， 该模型对容器网络进行了抽象：

![docker-cnm](https://gitee.com/ClayAndMore/image/raw/master/docker-cnm.jpg)

* Sandbox：每个沙盒包含一个容器网络栈(network stack)的配置，配置包括：容器的网口、路由表和DNS设置等
* Endpoint：通过Endpoint，沙盒可以被加入到一个Network里。
* Network：一组能相互直接通信的Endpoints。

Sandbox对应于Network Namespace， Endpoint对应于VETH， Network对应于Bridge。



##### 使用

这种方式需要把`/run/flannel/subnet.env`中的内容写到docker的环境变量配置文件`/run/flannel/docker`中，然后在docker engine启动时带上相应参数`EnvironmentFile=-/run/flannel/docker`。这样docker0的ip地址就会是flannel为该Node分配的地址了。

![flannal-docker-cnm](https://gitee.com/ClayAndMore/image/raw/master/flannal-docker-cnm.png)

这样子Pod IP是docker engine分配的，Pod也是以docker0为网关，通过veth连接network namespace，符合CNM中的定义。

这张图如果是cni模式，把docker0换成cni0，flannel0换成flannel.1



#### CNI 和 CNM的比较

相比起来，明显是Kubernetes推荐的CNI模式要好一些。

- CNI中，docker0的ip与Pod无关，Pod总是生成的时候才去动态的申请自己的IP，而CNM模式下，Pod的网段在docker engine启动时就已经决定。
- CNI只是一个网络接口规范，各种功能都由插件实现，flannel只是插件的一种，而且docker也只是容器载体的一种选择，Kubernetes还可以使用其他的，比如rtk...官方博客也对此做过说明：[Why Kubernetes doesn’t use libnetwork](https://kubernetes.io/blog/2016/01/why-kubernetes-doesnt-use-libnetwork/)



|                  | CNM                | CNI                |
| ---------------- | ------------------ | ------------------ |
| 标准规范         | Libnetwork         | cni                |
| 最小规范         | 容器               | pod                |
| 对守护进程的依赖 | 依赖dockerd        | 不依赖任何守护进程 |
| 跨主通信         | 要依赖外部KV数据库 | 用本身的KV的数据库 |
| 灵活程度         | 被docker绑架       | 插件可随意替换     |



### 有关 vxland

简单来说就是通过建立 VXLAN 隧道，通过 UDP 把 IP 封装一层直接送到对应的节点，实现了一个大的 VLAN。没有使用 IPoIP 或者 GRE 主要是因为一些云厂商比如 AWS 的安全策略只能支持 TCP/UDP/ICMP。

http://dockone.io/article/2216 Flannel中vxlan backend的原理和实现

https://cizixs.com/2017/09/25/vxlan-protocol-introduction/ vxlan 网络协议简介



### 更多参考文章

https://xuxinkun.github.io/2019/06/05/flannel-vxlan/

https://jiayi.space/post/kubernetescong-ru-men-dao-fang-qi-3-wang-luo-yuan-li

https://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/

https://zhuanlan.zhihu.com/p/110648535

https://www.infoq.cn/article/9vfPPfZPrXLM4ssLlxSR