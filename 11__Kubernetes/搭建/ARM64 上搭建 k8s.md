## ARM 环境搭建 k8s

### 环境

``` 
Linux node100 4.4.131-20190726.kylin.server-generic #kylin SMP Tue Jul 30 16:44:09 CST 2019 aarch64 aarch64 aarch64 GNU/Linux
```



### 下载

kubectl kubeadm kubelet



### 镜像

列出当前所需镜像列表：

```sh
# kubeadm config images list
k8s.gcr.io/kube-apiserver:v1.19.4
k8s.gcr.io/kube-controller-manager:v1.19.4
k8s.gcr.io/kube-scheduler:v1.19.4
k8s.gcr.io/kube-proxy:v1.19.4
k8s.gcr.io/pause:3.2
k8s.gcr.io/etcd:3.4.13-0
k8s.gcr.io/coredns:1.7.0
```

我们不知道现在arm的国内可用镜像的版本，我们可以去docker hub https://hub.docker.com/, 搜索，比如搜索 kube-apiserver ，然后勾选左侧的arm64 ，会列出当前下载比较多的镜像，

比如有个kubesphere的组织，他们的kube-apiserver arm镜像更新到了 v1.19.0

这时我们可以下载镜像了：

``` sh
kubeadm -v=5 config   --kubernetes-version=1.19.0  --image-repository=kubesphere images pull
[config/images] Pulled kubesphere/kube-apiserver:v1.19.0
[config/images] Pulled kubesphere/kube-controller-manager:v1.19.0
[config/images] Pulled kubesphere/kube-scheduler:v1.19.0
[config/images] Pulled kubesphere/kube-proxy:v1.19.0
[config/images] Pulled kubesphere/pause:3.2
exit status 1
output: Error response from daemon: manifest for kubesphere/etcd:3.4.13-0 not found: manifest unknown: manifest unknown

```

当遇到这个etcd镜像时卡掉了，去docker-hub 上找 arm版的etcd:3.4.13的镜像，用docker pull 拉取下拉然后改tag为：kubesphere/etcd:3.4.13-0。

改掉后再用kubeadm images pull 还是会到etcd这里卡主，我们可以不用这个命令拉取了，看下还有哪个镜像没有拉取：

``` sh
# kubeadm -v=5 config   --kubernetes-version=1.19.0  --image-repository=kubesphere images list
kubesphere/kube-apiserver:v1.19.0
kubesphere/kube-controller-manager:v1.19.0
kubesphere/kube-scheduler:v1.19.0
kubesphere/kube-proxy:v1.19.0
kubesphere/pause:3.2
kubesphere/etcd:3.4.13-0
kubesphere/coredns:1.7.0
```

可知剩下一个coredns，也是去单独拉取，改tag.



### 启动

使用 如下命令启动：

```
kubeadm init --v=1 --kubernetes-version=1.19.0  --image-repository=kubesphere
```

启动最后启动失败，观察 kubelet:

``` sh
        This error is likely caused by:
                - The kubelet is not running
                - The kubelet is unhealthy due to a misconfiguration of the node in some way (required cgroups disabled)

        If you are on a systemd-powered system, you can try to troubleshoot the error with the following commands:
                - 'systemctl status kubelet'
                - 'journalctl -xeu kubelet'

```

观察 docker 容器：

``` sh
# docker ps -a
CONTAINER ID    COMMAND                  CREATED              STATUS                         NAMES
6d1b515e7dc9    "kube-apiserver --ad…"   30 seconds ago       Exited (1) 7 seconds ago       k8s_kube-apiserver_
f9b3e4cf13d0    "etcd --advertise-cl…"   About a minute ago   Exited (1) About a minute ago  k8s_etcd_etcd-node1
09a8eb87e51b    "kube-controller-man…"   About a minute ago   Up About a minute              k8s_kube-controller
cc6c6f7382c1    "kube-scheduler --au…"   About a minute ago   Up About a minute              k8s_kube-scheduler_
9d878522749b    "/pause"                 About a minute ago   Up About a minute              k8s_POD_kube-schedu
c6124f96a0dc    "/pause"                 About a minute ago   Up About a minute              k8s_POD_kube-contro
545e353085e1    "/pause"                 About a minute ago   Up About a minute              k8s_POD_kube-apise
efad269143d5    "/pause"                 About a minute ago   Up About a minute              k8s_POD_etcd-node10
# docker logs f9b3e4cf13d0
etcd on unsupported platform without ETCD_UNSUPPORTED_ARCH=arm64 set
```

确认 etcd 镜像可用：

``` sh
# docker run --rm -it kubesphere/etcd:3.4.13-0 ls
bin   dev  home  media  opt   root  sbin  sys  usr
boot  etc  lib   mnt    proc  run   srv   tmp  var
# docker run --rm -it kubesphere/etcd:3.4.13-0
etcd on unsupported platform without ETCD_UNSUPPORTED_ARCH=arm64 set
# docker run --rm -it -e "ETCD_UNSUPPORTED_ARCH=arm64" kubesphere/etcd:3.4.13-0
running etcd on unsupported architecture "arm64" since ETCD_UNSUPPORTED_ARCH is set
[WARNING] Deprecated '--logger=capnslog' flag is set; use '--logger=zap' flag instead
2020-11-27 07:03:01.765713 I | etcdmain: etcd Version: 3.4.13
2020-11-27 07:03:01.765774 I | etcdmain: Git SHA: ae9734ed2
2020-11-27 07:03:01.765786 I | etcdmain: Go Version: go1.12.17
2020-11-27 07:03:01.765802 I | etcdmain: Go OS/Arch: linux/arm64
...
```

**如此看来需要设置 etcd 的环境变量才可以在arm64下使用**



### 分步启动

根据https://github.com/kubernetes/kubeadm/issues/1380，我们设置etcd的分步启动：

``` sh
# kubeadm reset
#kubeadm init phase certs all
#kubeadm init phase kubeconfig all
#kubeadm init phase control-plane all --pod-network-cidr 10.244.0.0/16
#sed -i 's/initialDelaySeconds: [0-9][0-9]/initialDelaySeconds: 240/g' /etc/kubernetes/manifests/kube-apiserver.yaml
#sed -i 's/failureThreshold: [0-9]/failureThreshold: 18/g'             /etc/kubernetes/manifests/kube-apiserver.yaml
#sed -i 's/timeoutSeconds: [0-9][0-9]/timeoutSeconds: 20/g'            /etc/kubernetes/manifests/kube-apiserver.yaml

kubeadm init phase etcd -v=5 local
cp etcd.yaml /etc/kubernetes/manifests/etcd.yaml
sudo kubeadm init --v=1 --skip-phases=etcd --ignore-preflight-errors=all --kubernetes-version=1.19.0 --image-repository=kubesphere
```

这里的 kubernetes init etcd 会在 /etc/kubernetes/manifest/下生成一个etcd.yaml，因为它只能使用默认的版本，我们需要在这里做一些修改，改镜像名和添加环境变量，放到当下目录，然后替换以后生成的：

``` yaml
    image: kubesphere/etcd:3.4.13-0
    imagePullPolicy: IfNotPresent
    env:
    - name: ETCD_UNSUPPORTED_ARCH
      value: "arm64"
```



终于成功启动：

``` sh
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```



### 网络插件

这时我们使用 kubectl get nodes 观察 node应该还是 NotReady的状态，应该是还没有下载完网络插件。

还是去docer hub 找一个支持arm的比较新的flannal插件，docker pull 下来，然后去flannel ：

https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml， 这里的yaml内容拷贝下来，把镜像名字换掉，使用 apply -f 启动。 



