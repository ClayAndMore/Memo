# Centos 部署k8s集群

## 准备条件

### 设置主机名
三台虚拟机且均设置hosts文件和主机名
```linux
[root@master01 ~]# vim /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.124.66 master01.com master01
192.168.124.67 node01.com node01
192.168.124.68 node02.com node02

[root@master01 ~]# vim /etc/hostname

master01
...
```

服务的操作命令大都相同
### 关闭iptables
```libux
# 查看防火墙状态
systemctl status iptables

# 关闭防火墙
systemctl stop iptables

# 开启自启
systemctl enable iptables

# 关闭自启
systemctl disable iptables

# 重启
systemctl restart iptables

# 开启
systemctl start iptabels
```

如果该服务没有找到，就先安装下。  
`yum install -y iptables-services`

### 关闭firewalld(防火墙)
```linux
systemctl status firewalld

systemctl enable firewalld

systemctl stop firewalld

systemctl disable firewalld
```

### 关闭selinux
```linux
# 查看状态
getenforce

# 永久关闭
vim /etc/selinux/config

SELINUX=disabled

# 验证
[root@node02 ~]# getenforce
Disabled
```

### 关闭虚拟内存
```linux
swapoff -a

# 永久关闭
vim /etc/fstab
# /dev/mapper/centos-swap swap                    swap    defaults        0 0

# 验证
[root@node02 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:           1.8G        158M        1.3G        8.7M        295M        1.5G
Swap:            0B          0B          0B
```  

### 修改时区
- 安装ntp  
`yum install ntp`  
- 修改`/etc/sysconfig/ntpd`   
`OPTIONS="-g -x"`
- 重启服务  
`systemctl restart ntpd`
- 开机自启  
`systemctl enable ntpd`
- 修改时区  
`ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime`
- 验证时间  

```linux
[root@node01 ~]# date
2019年 05月 23日 星期四 21:38:53 CST
```

### 下载yum仓库

- docker-ce.repo  
```linux
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```  

- kubernetes.repo  
```linux
[root@master01 ~]# cat /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=kubernetes repo
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
gpgcheck=0
enabled=1
repo-gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
  https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
```  

- 仓库检查：`yum repolist`  
- 拷贝至另外两台机器  
`scp kubernetes.repo docker-ce.repo node01:/etc/yum.repos.d/`  
`scp kubernetes.repo docker-ce.repo node02:/etc/yum.repos.d/`

## 安装
### docker
#### 安装
- `yun install docker-ce`  

#### 配置
- 代理(可选：新建该文件，docker启动时会加载该文件)  

```linux
[root@node01 ~]# cat /etc/systemd/system/docker.service.d/docker.conf
[Service]
Environment="HTTPS_PROXY=ip:port"
Environment="HTTP_PROXY=ip:port"
Enviroment="NO_PROXY=localhost,127.0.0.0/8,172.20.0.0/16"
ExecStartPost=/sbin/iptables -P FORWARD ACCEPT

# 代理只是针对内网用户和需要翻墙用户设置。

# 重新加载配置
systemctl daemon-reload

# 重启docker
systemctl restart docker
```  

- 配置源(可换阿里源或者网易源)  

```linux
[root@node01 ~]# cat /etc/docker/daemon.json
{
    "registry-mirrors": ["https://o9wm45c3.mirror.aliyuncs.com"],
}
```  

- 配置`cgroup driver:systemd`  

```linux
[root@node01 ~]# cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://o9wm45c3.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
```

####  验证
- 版本  

```linux
[root@master01 ~]# docker version
Client:
 Version:           18.09.6
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        481bc77156
 Built:             Sat May  4 02:34:58 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.6
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.8
  Git commit:       481bc77
  Built:            Sat May  4 02:02:43 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```
- 信息  

```linux
[root@master01 ~]# docker info
Containers: 1
 Running: 0
 Paused: 0
 Stopped: 1
Images: 1
Server Version: 18.09.6
Storage Driver: devicemapper
 Pool Name: docker-253:0-128594-pool
 Pool Blocksize: 65.54kB
 Base Device Size: 10.74GB
 Backing Filesystem: xfs
 Udev Sync Supported: true
 Data file: /dev/loop0
 Metadata file: /dev/loop1
 Data loop file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata loop file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 19.33MB
 Data Space Total: 107.4GB
 Data Space Available: 46.51GB
 Metadata Space Used: 17.37MB
 Metadata Space Total: 2.147GB
 Metadata Space Available: 2.13GB
 Thin Pool Minimum Free Space: 10.74GB
 Deferred Removal Enabled: true
 Deferred Deletion Enabled: true
 Deferred Deleted Device Count: 0
 Library Version: 1.02.149-RHEL7 (2018-07-20)
Logging Driver: json-file
Cgroup Driver: systemd
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: bb71b10fd8f58240ca47fbb579b9d1028eea7c84
runc version: 2b18fe1d885ee5083ef9f0838fee39b62d653e30
init version: fec3683
Security Options:
 seccomp
  Profile: default
Kernel Version: 3.10.0-957.12.1.el7.x86_64
Operating System: CentOS Linux 7 (Core)
OSType: linux
Architecture: x86_64
CPUs: 4
Total Memory: 3.683GiB
Name: master01
ID: A535:QMTO:P5AT:RL6V:M4PZ:AW7B:URR2:QKZP:PO22:ZLLT:A2JH:FCLE
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
HTTP Proxy: ip:port
HTTPS Proxy: ip:port
Registry: https://index.docker.io/v1/
Labels:
Experimental: false
Insecure Registries:
 127.0.0.0/8
Registry Mirrors:
 https://o9wm45c3.mirror.aliyuncs.com/
Live Restore Enabled: false
Product License: Community Engine

WARNING: the devicemapper storage-driver is deprecated, and will be removed in a future release.
WARNING: devicemapper: usage of loopback devices is strongly discouraged for production use.
         Use `--storage-opt dm.thinpooldev` to specify a custom block storage device.
```
- 运行  

```linux
[root@master01 ~]# docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
#### 自启
- `systemd enable docker`  

### 翻墙
可选，k8s拉取镜像走国外源
#### 纸飞机
- 安装shadowsocks：`pip install shadowsocks`
- 编写配置文件  

```linux

[root@node01 ~]# vim /etc/shadowsock/vpn.json

{
    "server":"77.81.105.186",
    "server_port":6666,
    "password":"jw123456",
    "method":"aes-256-cfb",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "timeout":600
}

```  

- 编写开机自启服务  

```linux
# 编辑文件

[root@node01 ~]# cat /etc/systemd/system/shadowsocks.service
[Unit]
Description=Shadowsocks
[Service]
TimeoutStartSec=0
ExecStart=/usr/bin/sslocal -c /etc/shadowsock/vpn.json
[Install]
WantedBy=multi-user.target

# 启动命令根据自己选择，看你的ss安装位置 后面跟配置文件
```
- 启动并设置为开机自启  
  
```linux

# 查看
[root@node01 ~]# systemctl status shadowsocks
● shadowsocks.service - Shadowsocks
   Loaded: loaded (/etc/systemd/system/shadowsocks.service; enabled; vendor preset: disabled)
   Active: active (running) since 五 2019-05-24 04:40:11 CST; 6h left
 Main PID: 6228 (sslocal)
   CGroup: /system.slice/shadowsocks.service
           └─6228 /usr/bin/python2 /usr/bin/sslocal -c /etc/shadowsock/vpn.json

5月 24 04:40:11 node01 systemd[1]: Started Shadowsocks.
5月 24 04:40:15 node01 sslocal[6228]: INFO: loading config from /etc/shadowsock/vpn.json
5月 24 04:40:16 node01 sslocal[6228]: 2019-05-24 04:40:16 INFO     loading libcrypto from libcrypto.so.10
5月 24 04:40:16 node01 sslocal[6228]: 2019-05-24 04:40:16 INFO     starting local at 127.0.0.1:1080
Hint: Some lines were ellipsized, use -l to show in full.

# 开机启动
[root@node01 ~]# systemctl enable shadowsocks
```

####  privoxy
- 安装privoxy(可选：设置了翻墙就可以根据他来设置全局翻墙走sock5代理)：`yum install -y privoxy`

- 修改配置文件  

```linux

/etc/privoxy/config
        - listen-address 127.0.0.1:8118 # 8118 是默认端口，不用改
        - forward-socks5t / 127.0.0.1:1080 . #转发到本地端口，注意最后有个点
```  

- 设置启动、开机自启：可参考前些个服务来设置

- 设置代理(所有用户)  

```linux
[root@node01 ~]# vim /etc/profile
# add proxy
# export http_proxy=127.0.0.1:8118
# export https_proxy=127.0.0.1:8118

# 取消注释就代表你机子一开机就可以翻墙，但是走国内网就好慢。所以我喜欢设置临时代理，那样每次开机或重启就失效
export http_proxy=127.0.0.1:8118
```  

- 验证  

```linux
[root@node01 ~]# curl www.google.com
^C
[root@node01 ~]# export http_proxy=127.0.0.1:8118
[root@node01 ~]# curl www.google.com
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="ro"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script nonce="amuyDgG6uwcVD392HoN3yQ==">(function()
```

### k8s
#### 安装
- `yum install -y kubectl kubeadm kubelet`  

#### 验证
```linux
[root@master01 ~]# kubectl version -o json
{
  "clientVersion": {
    "major": "1",
    "minor": "14",
    "gitVersion": "v1.14.2",
    "gitCommit": "66049e3b21efe110454d67df4fa62b08ea79a19b",
    "gitTreeState": "clean",
    "buildDate": "2019-05-16T16:23:09Z",
    "goVersion": "go1.12.5",
    "compiler": "gc",
    "platform": "linux/amd64"
  }
}
The connection to the server localhost:8080 was refused - did you specify the right host or port?

[root@master01 ~]# kubeadm version -o short
v1.14.2

[root@master01 ~]# kubelet --version
Kubernetes v1.14.2
```  

#### 自启动
- `systemctl enable kubelet`  

## 部署
### pull
先把镜像拉下来，要翻墙，也可以去网上下载之后，打个tag，保证名字一样。
```linux
[root@master01 ~]# kubeadm config images pull
[config/images] Pulled k8s.gcr.io/kube-apiserver:v1.14.2
[config/images] Pulled k8s.gcr.io/kube-controller-manager:v1.14.2
[config/images] Pulled k8s.gcr.io/kube-scheduler:v1.14.2
[config/images] Pulled k8s.gcr.io/kube-proxy:v1.14.2
[config/images] Pulled k8s.gcr.io/pause:3.1
[config/images] Pulled k8s.gcr.io/etcd:3.3.10
[config/images] Pulled k8s.gcr.io/coredns:1.3.1
[root@master01 ~]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/kube-proxy                v1.14.2             5c24210246bb        7 days ago          82.1MB
k8s.gcr.io/kube-apiserver            v1.14.2             5eeff402b659        7 days ago          210MB
k8s.gcr.io/kube-controller-manager   v1.14.2             8be94bdae139        7 days ago          158MB
k8s.gcr.io/kube-scheduler            v1.14.2             ee18f350636d        7 days ago          81.6MB
k8s.gcr.io/coredns                   1.3.1               eb516548c180        4 months ago        40.3MB
hello-world                          latest              fce289e99eb9        4 months ago        1.84kB
k8s.gcr.io/etcd                      3.3.10              2c4adeb21b4f        5 months ago        258MB
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        17 months ago       742kB
```
### save 
然后把镜像save下来，load到其他两个从节点上去
```linux
# one-one(体积大，操作繁琐)
docker save k8s.gcr.io/kube-proxy > kube-proxy_v1.14.2.tar
docker save k8s.gcr.io/kube-apiserver > kube-apiserver_v1.14.2.tar
docker save k8s.gcr.io/kube-controller-manager > kube-controller-manager_v1.14.2.tar
docker save k8s.gcr.io/kube-scheduler > kube-scheduler_v1.14.2.tar
docker save k8s.gcr.io/coredns > coredns_1.3.1.tar
docker save k8s.gcr.io/etcd > etcd_3.3.10.tar
docker save k8s.gcr.io/pause > pause_3.1.tar

# all-in-one1(体积更小)
docker save k8s.gcr.io/kube-proxy:v1.14.3 k8s.gcr.io/kube-controller-manager:v1.14.3 k8s.gcr.io/kube-apiserver:v1.14.3 k8s.gcr.io/kube-scheduler:v1.14.3 |gzip > k8s1.tar.gz

# all-in-one2(体积更小)
docker save k8s.gcr.io/coredns:1.3.1 k8s.gcr.io/etcd:3.3.10 k8s.gcr.io/pause:3.1 |gzip > k8s2.tar.gz

# save后拷贝到各个从节点
scp -r images/ node01:/root/docker/images/
scp -r images/ node02:/root/docker/images/

```
### load
每个从节点都load镜像
```linux
# one-one
docker load  < kube-proxy_v1.14.2.tar
docker load  < kube-apiserver_v1.14.2.tar
docker load  < kube-controller-manager_v1.14.2.tar
docker load  < kube-scheduler_v1.14.2.tar
docker load  < coredns_1.3.1.tar
docker load  < etcd_3.3.10.tar
docker load  < pause_3.1.tar

# all-1
docker load < k8s1.tar.gz
# all-2
docker load < k8s2.tar.gz
```  

### ls
每台机器查看所有镜像
```linux
[root@master01 images]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/kube-proxy                v1.14.3             004666307c5b        11 days ago         82.1MB
k8s.gcr.io/kube-apiserver            v1.14.3             9946f563237c        11 days ago         210MB
k8s.gcr.io/kube-controller-manager   v1.14.3             ac2ce44462bc        11 days ago         158MB
k8s.gcr.io/kube-scheduler            v1.14.3             953364a3ae7a        11 days ago         81.6MB
k8s.gcr.io/coredns                   1.3.1               eb516548c180        5 months ago        40.3MB
k8s.gcr.io/etcd                      3.3.10              2c4adeb21b4f        6 months ago        258MB
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        18 months ago       742kB
```  

### init
```linux
kubeadm init --kubernetes-version=v1.14.3 --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.19.19.119:6443 --token s1u4f4.mj75xtzp7tkei3ki \
    --discovery-token-ca-cert-hash sha256:85e93562222e113e3dae772f030e5aad09dd129a8bf202877a90e970f9a867a6 
```  

### calico 
初始化之后按照上面提示操作，这个时候集群还没完全准备好，需要安装网络插件。这里安装calico网络插件为例。
```
# 下载版本为v3.7的calico文件
curl https://docs.projectcalico.org/v3.7/manifests/calico.yaml -O

# 设置环境变量
export POD_CIDR="10.244.0.0/16"

# 替换原有yaml文件的部分内容
sed -i -e "s?192.168.0.0/16?$POD_CIDR?g" calico.yaml

# 运行calico相关pod
kubectl apply -f calico.yaml

# 查看主节点是否准备
kubectl get nodes

# 查看主节点各个系统pod的运行状态
kubectl get pods -n kube-system
```  

### join
其他两个节点分别执行此命令加入master01主节点
```linux

kubeadm join 172.19.19.119:6443 --token s1u4f4.mj75xtzp7tkei3ki \
    --discovery-token-ca-cert-hash sha256:85e93562222e113e3dae772f030e5aad09dd129a8bf202877a90e970f9a867a6
```
为了从节点也能运行主节点的kubectl命令，需要把主节点的admin.conf 复制到用户目录下的.kube/config
```linux
scp /etc/kubernetes/admin.conf node01:/root/.kube/config
scp /etc/kubernetes/admin.conf node02:/root/.kube/config
```  

### ready
稍等片刻，查看各个节点的运行状态以及pod运行状态
```linux
[root@master01 ~]# kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
master01   Ready    master   72m   v1.14.3
node01     Ready    <none>   61m   v1.14.3
node02     Ready    <none>   46m   v1.14.3
[root@master01 ~]# kubectl get pods -n kube-system
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-78f8f67c4d-gxw5k   1/1     Running   0          65m
calico-node-r5mzw                          1/1     Running   0          43m
calico-node-tfdqp                          1/1     Running   0          61m
calico-node-v259x                          1/1     Running   0          65m
coredns-fb8b8dccf-mxqn2                    1/1     Running   0          72m
coredns-fb8b8dccf-xklrn                    1/1     Running   0          72m
etcd-master01                              1/1     Running   0          71m
kube-apiserver-master01                    1/1     Running   0          71m
kube-controller-manager-master01           1/1     Running   0          71m
kube-proxy-6ffwz                           1/1     Running   0          46m
kube-proxy-lvvp8                           1/1     Running   0          61m
kube-proxy-nwd7l                           1/1     Running   0          72m
kube-scheduler-master01                    1/1     Running   0          71m
```