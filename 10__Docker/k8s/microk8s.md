

### 安装

```
root@wy-server:~#  snap install microk8s --classic --channel=1.12/stable
error: cannot install "microk8s": Post https://api.snapcraft.io/v2/snaps/refresh: dial tcp: lookup
       api.snapcraft.io: Temporary failure in name resolution
```

为 snap 配置代理

```sh
# vim /etc/profile
export SYSTEMD_EDITOR="/usr/bin/vim"

# source /etc/profile

# systemctl edit snapd
[Service]
Environment="http_proxy=http://192.168.59.241:8888"
Environment="https_proxy=http://192.168.59.241:8888"

# systemctl daemon-reload
# systemctl restart snapd
```

再次安装：

```sh
# snap install microk8s --classic --channel=1.12/stable
microk8s (1.12/stable) v1.12.9 from Canonical✓ installed
```

注意，安装最新版本的命令是 ：`snap install microk8s --classic `, 当时最新版本是1.13， 1.13没有 microk8s.docker 命令。

因为microk8s会自带一个docker, 如果你的系统里已经安装了docker的话， 它还是用自带的那个docker,也就是microk8s.docker。因此，在解决上面提到的镜像问题的时候， 一定要使用microk8s.docker命令来操作， 使用系统原有的docker是不起作用的。

todo: 如何让 新版 microk8s 使用原有docker



### 基本命令

``` SH
# 1. 启动
microk8s.start 
# 2. 关闭
microk8s.stop 
# 3. 状态
microk8s.status

# 4. kubectl 操作
# --- 查看 cluster
microk8s.kubectl cluster-info
Kubernetes master is running at http://127.0.0.1:8080

# --- 查看 nodes
microk8s.kubectl get nodes
NAME   STATUS   ROLES    AGE   VERSION
wy     Ready    <none>   22m   v1.12.9

# --- 查看 pods
microk8s.kubectl get pods
No resources found.

#  docker 操作
microk8s.docker ps
microk8s.docker images
```

状态：

```  sh
# microk8s.status
microk8s is running
addons:
gpu: disabled
storage: disabled
registry: disabled
ingress: disabled
dns: disabled
metrics-server: disabled
istio: disabled
dashboard: disabled
```



设置别名：

``` SH
# snap alias microk8s.kubectl kubectl
Added:
  - microk8s.kubectl as kubectl
```


kube 命令自动补全:

```SH
# echo "source <(kubectl completion bash)" >> ~/.bashrc
# source ~/.bashrc
```



### 开启服务和拉取镜像

``` sh
# 开启dns: 
# microk8s.enable dns
Enabling DNS
Applying manifest
service/kube-dns created
serviceaccount/kube-dns created
configmap/kube-dns created
deployment.extensions/kube-dns created
Restarting kubelet

# 查看 pod， 需要指定命名空间：
root@wy:~/images# kubectl get pods
No resources found.
root@wy:~/images# kubectl get pods -n kube-system
NAME                        READY   STATUS              RESTARTS   AGE
kube-dns-67b548dcff-lj94b   0/3     ContainerCreating   0          22s

# 查看详细信息：
root@wy:~/images# kubectl describe po kube-dns-67b548dcff-lj94b
Error from server (NotFound): pods "kube-dns-67b548dcff-lj94b" not found
root@wy:~/images# kubectl describe po kube-dns-67b548dcff-lj94b -n kube-system
...
 error: code = Unknown desc = failed pulling image "k8s.gcr.io/pause:3.1": Error response from daemon: Get https://k8s.gcr.io/v2/:
```

由于 gfw 的原因，我们需要使用tag改标签的方式来曲线救国：

```sh
# microk8s.docker pull mirrorgooglecontainers/pause-amd64:3.1
Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled while waiting for connecti                                             on (Client.Timeout exceeded while awaiting headers)
```

应该是公司内网机器需要配置连外网的代理。



#### 配置代理

是配置 microk8s.docker 的代理，而不是 docker的：

```SH
# vim /var/snap/microk8s/current/args/docker-daemon.json
"registry-mirrors": ["https://o9wm45c3.mirror.aliyuncs.com"]  # 国内镜像源

# vim /var/snap/microk8s/current/args/dockerd-env, 
HTTP_PROXY=http://192.168.59.241:8888/
HTTPS_PROXY=http://192.168.59.241:8888/

# vim /var/snap/microk8s/current/args/containerd-env，  有可能用的containerd
HTTP_PROXY=http://192.168.59.241:8888/
HTTPS_PROXY=http://192.168.59.241:8888/
```

我配置的都是配置公司内网的代理，如果不在公司内网，可以直接配置能够连国外的地址，就不用改tag了。

这个文件夹下都是一些环境变量。



尝试：

``` sh
root@wy:~/images# microk8s.docker pull mirrorgooglecontainers/pause-amd64:3.1
3.1: Pulling from mirrorgooglecontainers/pause-amd64
67ddbfb20a22: Pull complete
Digest: sha256:59eec8837a4d942cc19a52b8c09ea75121acc38114a2c68b98983ce9356b8610
Status: Downloaded newer image for mirrorgooglecontainers/pause-amd64:3.1
```

可以了，接下来改tag:

``` sh
root@wy:~/images# microk8s.docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
mirrorgooglecontainers/pause-amd64   3.1                 da86e6ba6ca1        2 years ago         742kB

root@wy:~/images# microk8s.docker tag mirrorgooglecontainers/pause-amd64:3.1 k8s.gcr.io/pause:3.1
root@wy:~/images# microk8s.docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        2 years ago         742kB
mirrorgooglecontainers/pause-amd64   3.1                 da86e6ba6ca1        2 years ago         742kB
```







### 卸载

```
microk8s.reset
snap remove microk8s
```
