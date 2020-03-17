docker 搭建nginx的时候，如果内部使用容器的网关ip，即使不接外网也记得给被代理的端口加防火墙规则。





### dockers exec user process caused "exec format error"

可能是镜像与系统不兼容



### 更改 cgroup drive

默认 的 是 cgroupfs， 而k8中 是 systemd, 所以在安装k8s过程中会出现：

```
failed to create kubelet: misconfiguration: kubelet cgroup driver: "cgroupfs" is different from docker cgroup driver: "systemd"
```

有两种方式解决问题，一种是修改docker,，另一种是修改kubelet；
1、修改docker的Cgroup Driver
修改/etc/docker/daemon.json文件,( 在 centos 7 中 可能没有该文件，需要自己建立)

``` json
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

重启docker

```
systemctl daemon-reload
systemctl restart docker
```

使用 docker info 查看修改后的信息

2、修改kubelet的Cgroup Driver
修改/etc/systemd/system/kubelet.service.d/10-kubeadm.conf文件，增加--cgroup-driver=cgroupfs

```
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --cgroup-driver=cgroupfs"
```

重启kubelet

systemctl daemon-reload
systemctl restart kubelet

参考：https://www.cnblogs.com/hongdada/p/9771857.html