### 前期准备

关闭 Swap

查看：

```
free -h 
blkid
lsblk
```

关闭：

```
swapoff /dev/mapper/centos-swap
swapoff -a
vi /etc/fstab # 删掉有swap的那一行
```

处理后 reboot 或  mount -a



通过 `sudo cat /sys/class/dmi/id/product_uuid` 可查看机器的 `product_uuid` 请确保要搭建集群的所有节点的 `product_uuid` 均不相同。同时所有节点的 Mac 地址也不能相同，通过 `ip a` 或者 `ifconfig -a` 可进行查看。



端口情况：

 K8S 是 C/S 架构，在启动后，会固定监听一些端口用于提供服务。可以通过：

 `sudo netstat -ntlp |grep -E '6443|23[79,80]|1025[0,1,2]'` 

查看这些端口是否被占用，如果被占用，请手动释放。

在 CentOS 系统中需要通过 `sudo yum install net-tools` 安装，而在 Debian/Ubuntu 系统中，则需要通过 `sudo apt install net-tools` 进行安装。



### 安装docker

安装或并启动， 推荐docker 版本大于17.03



### 安装 kubectl kubelet kubeam

配置国内源：

安装kubernetes的时候，需要安装kubelet, kubeadm等包，但k8s官网给的yum源是`packages.cloud.google.com`，国内访问不了，此时我们可以使用阿里云的yum仓库镜像。

阿里云上没有附Help说明连接，简单摸索了下，如下设置可用（centos）。注意不要开启check。

```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

* 安装 

  `yum install -y kubectl kubelet kubeadm`

* 开机启动

  `systemctl enable kubelet`

* 启动

  `systemctl start kubelet`



不过阿里云跟kubernetes同步不太及时，例如现在是1.8.1了，但是阿里云还是1.7.5。

如果你用的是ubuntu，也可以试试ustc的[mirror](https://link.jianshu.com/?t=http%3A%2F%2Fmirrors.ustc.edu.cn%2Fkubernetes%2F)，更新比较及时。

```
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial main
EOF
```



第二种安装方式是去github:

<https://github.com/kubernetes/kubernetes>

找：[CHANGELOG-1.14.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.14.md)

下载Server Binaries， eg:

```
wget -q https://dl.k8s.io/v1.11.3/kubernetes-server-linux-amd64.tar.gz

[root@master tmp]# tar -zxf kubernetes-server-linux-amd64.tar.gz
[root@master tmp]# ls kubernetes
addons  kubernetes-src.tar.gz  LICENSES  server
[root@master tmp]# ls kubernetes/server/bin/ | grep -E 'kubeadm|kubelet|kubectl'
kubeadm
kubectl
kubelet

[root@master tmp]# mv kubernetes/server/bin/kube{adm,ctl,let} /usr/bin/
[root@master tmp]# ls /usr/bin/kube*
/usr/bin/kubeadm  /usr/bin/kubectl  /usr/bin/kubelet

[root@master tmp]# kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"11", GitVersion:"v1.11.3", GitCommit:"a4529464e4629c21224b3d52edfe0ea91b072862", GitTreeState:"clean", BuildDate:"2018-09-09T17:59:42Z", GoVersion:"go1.10.3", Compiler:"gc", Platform:"linux/amd64"}
[root@master tmp]# kubectl version --client
Client Version: version.Info{Major:"1", Minor:"11", GitVersion:"v1.11.3", GitCommit:"a4529464e4629c21224b3d52edfe0ea91b072862", GitTreeState:"clean", BuildDate:"2018-09-09T18:02:47Z", GoVersion:"go1.10.3", Compiler:"gc", Platform:"linux/amd64"}
[root@master tmp]# kubelet --version
Kubernetes v1.11.3
```



### 配置systemd服务

为了在生产环境中保障各组件的稳定运行，同时也为了便于管理，我们增加对 `kubelet` 的 `systemd` 的配置，由 `systemd` 对服务进行管理。

### 配置 kubelet

```
[root@master tmp]# cat <<EOF > /etc/systemd/system/kubelet.service
[Unit]
Description=kubelet: The Kubernetes Agent
Documentation=http://kubernetes.io/docs/

[Service]
ExecStart=/usr/bin/kubelet
Restart=always
StartLimitInterval=0
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
[root@master tmp]# mkdir -p /etc/systemd/system/kubelet.service.d
[root@master tmp]# cat <<EOF > /etc/systemd/system/kubelet.service.d/kubeadm.conf
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
EnvironmentFile=-/etc/default/kubelet
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
EOF
[root@master tmp]# systemctl enable kubelet
Created symlink from /etc/systemd/system/multi-user.target.wants/kubelet.service to /etc/systemd/system/kubelet.service.
```

在这里我们添加了 `kubelet` 的 systemd 配置，然后添加了它的 `Drop-in` 文件，我们增加的这个 `kubeadm.conf` 文件，会被 systemd 自动解析，用于复写 `kubelet` 的基础 systemd 配置，可以看到我们增加了一系列的配置参数。在第 17 章中，我们会对 `kubelet` 做详细剖析，到时再进行解释。



### 安装 crictl 

 ln -s /root/k8s/crictl /usr/bin/crictl

<https://github.com/kubernetes-sigs/cri-tools/releases>

### 安装 socat
socat 是一款很强大的命令行工具，可以建立两个双向字节流并在其中传输数据。这么说你也许不太理解，简单点说，它其中的一个功能是可以实现端口转发。

无论在 K8S 中，还是在 Docker 中，如果我们需要在外部访问服务，端口转发是个必不可少的部分。

yum install -y socat ，

sudo apt-get install -y socat





### 拉取镜像

```
root@VM-0-6-ubuntu:~/k8s# kubeadm config images pull
failed to pull image "k8s.gcr.io/kube-apiserver:v1.14.0": output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
root@VM-0-6-ubuntu:~/k8s# kubeadm config images list --kubernetes-version v1.14.0
k8s.gcr.io/kube-apiserver:v1.14.0
k8s.gcr.io/kube-controller-manager:v1.14.0
k8s.gcr.io/kube-scheduler:v1.14.0
k8s.gcr.io/kube-proxy:v1.14.0
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.3.10
k8s.gcr.io/coredns:1.3.1
root@VM-0-6-ubuntu:~/k8s# docker pull mirrorgooglecontainers/kube-apiserver:v1.14.0
Error response from daemon: manifest for mirrorgooglecontainers/kube-apiserver:v1.14.0 not found
root@VM-0-6-ubuntu:~/k8s# docker pull registry.aliyuncs.com/google_containers/kube-apiserver:v1.14.0
v1.14.0: Pulling from google_containers/kube-apiserver
346aee5ea5bc: Pull complete
a1448280d5df: Pull complete
Digest: sha256:ebfb9018e345697e85d7adc4664c9340570bca33fff126e158264a791c6a5708
Status: Downloaded newer image for registry.aliyuncs.com/google_containers/kube-apiserver:v1.14.0
root@VM-0-6-ubuntu:~/k8s# ^C
```



更换名称：

```
root@VM-0-6-ubuntu:~/k8s# docker images
REPOSITORY                                                        TAG                 IMAGE ID            CREATED             SIZE
registry.aliyuncs.com/google_containers/kube-proxy                v1.14.0             5cd54e388aba        19 hours ago        82.1MB
registry.aliyuncs.com/google_containers/kube-controller-manager   v1.14.0             b95b1efa0436        19 hours ago        158MB
registry.aliyuncs.com/google_containers/kube-scheduler            v1.14.0             00638a24688b        19 hours ago        81.6MB
registry.aliyuncs.com/google_containers/kube-apiserver            v1.14.0             ecf910f40d6e        19 hours ago        210MB
busybox                                                           latest              d8233ab899d4        5 weeks ago         1.2MB
registry.aliyuncs.com/google_containers/coredns                   1.3.1               eb516548c180        2 months ago        40.3MB
registry.aliyuncs.com/google_containers/etcd                      3.3.10              2c4adeb21b4f        3 months ago        258MB
kindest/node                                                      v1.12.2             58eadc0ca522        4 months ago        1.5GB
registry.aliyuncs.com/google_containers/pause                     3.1                 da86e6ba6ca1        15 months ago       742kB


root@VM-0-6-ubuntu:~/k8s# docker tag registry.aliyuncs.com/google_containers/kube-proxy:v1.14.0 k8s.gcr.io/kube-proxy:v1.14.0
root@VM-0-6-ubuntu:~/k8s# docker images
REPOSITORY                                                        TAG                 IMAGE ID            CREATED             SIZE
registry.aliyuncs.com/google_containers/kube-proxy                v1.14.0             5cd54e388aba        19 hours ago        82.1MB
k8s.gcr.io/kube-proxy                                             v1.14.0             5cd54e388aba        19 hours ago        82.1MB
registry.aliyuncs.com/google_containers/kube-controller-manager   v1.14.0             b95b1efa0436        19 hours ago        158MB
registry.aliyuncs.com/google_containers/kube-scheduler            v1.14.0             00638a24688b        19 hours ago        81.6MB
registry.aliyuncs.com/google_containers/kube-apiserver            v1.14.0             ecf910f40d6e        19 hours ago        210MB
busybox                                                           latest              d8233ab899d4        5 weeks ago         1.2MB
registry.aliyuncs.com/google_containers/coredns                   1.3.1               eb516548c180        2 months ago        40.3MB
registry.aliyuncs.com/google_containers/etcd                      3.3.10              2c4adeb21b4f        3 months ago        258MB
kindest/node                                                      v1.12.2             58eadc0ca522        4 months ago        1.5GB
registry.aliyuncs.com/google_containers/pause  
```

删除无用的镜像
`docker images | grep mirrorgooglecontainers | awk '{print "docker rmi "  $1":"$2}' | sh -x`

or:

`docker images | grep google_containers | awk '{print "docker rmi "  $1":"$2}' | sh -x`






### 配置kubectl

```
[root@master ~]# kubectl --kubeconfig /etc/kubernetes/admin.conf get nodes                                                
NAME      STATUS     ROLES     AGE       VERSION
master    NotReady   master    13h       v1.11.3
[root@master ~]#
[root@master ~]# KUBECONFIG=/etc/kubernetes/admin.conf kubectl get nodes                                                  
NAME      STATUS     ROLES     AGE       VERSION
master    NotReady   master    13h       v1.11.3
```

推荐方式更改默认配置文件：

```
[root@master ~]# mkdir -p $HOME/.kube
[root@master ~]# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@master ~]# sudo chown $(id -u):$(id -g) $HOME/.kube/config
[root@master ~]# kubectl get nodes                                                  
NAME      STATUS     ROLES     AGE       VERSION
master    NotReady   master    13h       v1.11.3
```





### kubeadm

初始化： kubeadm init

重置： kubeadm reset 

记得： sysctl net.bridge.bridge-nf-call-iptables=1 

用上finnal: kubeadm init --pod-network-cidr=10.244.0.0/16



#### finnal

https://github.com/coreos/flannel

使用前记得 **再配置一遍  kubectl**

1.14.0, 用的

 `kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`

没有问题

有问题时报：

```
NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
```





其他问题：Error from server (Forbidden)

https://github.com/coreos/flannel/issues/1103

解决方式

```

sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
```





再次查看 Node状态：

`kubectl get nodes`

如果没有ready,看输出：

`kubectl get nodes -o yaml`



pod状态

`kubectl get pods --all-namespaces`



### join

kubeadm join 192.168.18.196:6443 --token 5z73l2.injxi65alp66le4g  --discovery-token-ca-cert-hash sha256:dd907e2f6d5dd6272d4e6394cdd2ac12f89ec6b2e7c139f868775649bc4de997



### kubectl

官方提供了 CLI 工具 `kubectl` 用于完成大多数集群管理相关的功能。当然凡是你可以通过 `kubectl`完成的与集群交互的功能，都可以直接通过 API 完成。

一般的用法 `kubectl [flags] [options]` 



#### get

kubectl get node ， 获得集群信息、

如果我们想要看到更详细的信息呢？可以通过传递 `-o` 参数以得到不同格式的输出。：

```
➜  ~ kubectl get nodes -o wide 
NAME       STATUS    ROLES     AGE       VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE            KERNEL-VERSION   CONTAINER-RUNTIME
minikube   Ready     master    2d        v1.11.3   10.0.2.15     <none>        Buildroot 2018.05   4.15.0           docker://17.12.1-ce
```



当然也可以传递 `-o yaml` 或者 `-o json` 得到更加详尽的信息。



#### run

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



### 安装docker-compose

https://docs.docker.com/compose/install/



`pip install docker-compose` 

验证：

`docker-compose version`



遇到`'module' object has no attribute 'SSL_ST_INIT'`

```
rm -rf /usr/lib/python2.7/dist-packages/OpenSSL
rm -rf /usr/lib/python2.7/dist-packages/pyOpenSSL-0.15.1.egg-info
sudo pip install pyopenssl

```



#### 重填token

```

[root@localhost ~]# kubeadm token list
TOKEN                     TTL         EXPIRES                     USAGES                   DESCRIPTION                                                EXTRA GROUPS
0kqaiy.z6hq7mmjf4cny7mf   <invalid>   2019-03-29T14:40:17+08:00   authentication,signing   The default bootstrap token generated by 'kubeadm init'.   system:bootstrappers:kubeadm:default-node-token
jerycu.41sw7emsvgjgmtau   <invalid>   2019-03-30T17:06:48+08:00   authentication,signing   <none>                                                     system:bootstrappers:kubeadm:default-node-token

```





重新生成新的token:

`kubeadm token create`

获得sha256 hash 值：

```
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```

eg: 
```
kubeadm join 202.182.112.120:6443 --token t14kzc.vjurhx5k98dpzqdc --discovery-token-ca-cert-hash sha256:d64f7ce1af9f9c0c73d2d737fd0095456ad98a2816cb5527d55f984c8aa8a762
```



### 问题

#### not ready

First, describe nodes and see if it reports anything:

```
$ kubectl describe nodes
```

Look for conditions, capacity and allocatable:

```
Conditions:
  Type              Status
  ----              ------
  OutOfDisk         False
  MemoryPressure    False
  DiskPressure      False
  Ready             True
Capacity:
 cpu:       2
 memory:    2052588Ki
 pods:      110
Allocatable:
 cpu:       2
 memory:    1950188Ki
 pods:      110
```

If everything is alright here, SSH into the node and observe `kubelet` logs to see if it reports anything. Like certificate erros, authentication errors etc.

If `kubelet` is running as a systemd service, you can use

```
$ journalctl -u kubelet
```



#### host could not be reached

把自己的host改成ip

/ect/hostname 和/ect/hosts



#### CA 认证

先尝试 kubeadm reset



####  x509 cert issues after kubeadm init

```
export KUBECONFIG=/etc/kubernetes/kubelet.conf
kubectl get nodes
```



#### It seems like the kubelet isn't running or healthy

systemctl enable docker

systemctl start docker



systemctl start kubectl

systemctl enable kubectl



reboot .   我就是这样解决的，怀疑是某些配置配置后没有重启生效。



#### The connection to the server localhost:8080 was refused

运行kubectl 相关命令时会提示refused， 我们需要像上面配置kubectl那样去配置，

但是说没有/etc/kubernetes/admin， 它 是 kubeadm init生成的。

也有说如果说是子节点需要拿父节点的配置：

<https://github.com/kubernetes/kubernetes/issues/50295>