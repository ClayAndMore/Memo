---

title: "k8s部署问题.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: ["k8s部署"]
categories: ["k8s"]
author: "Claymore"

---




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



#### Error from server (Forbidden)

Error from server (Forbidden): roles.rbac.authorization.k8s.io is forbidden: User "system:node:192.168.18.196" cannot list resource "roles" in API group "rbac.authorization.k8s.io" at the cluster scope

这个问题是衔接上个问题的，

`export KUBECONFIG=/etc/kubernetes/admin.conf `

具体：<https://blog.51cto.com/foxhound/2057395?from=singlemessage>



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

```sh
scp -r /etc/kubernetes/admin.conf ${node1}:/etc/kubernetes/admin.conf
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bashrc
source ~/.bashrc
```





#### kubeadm reset 卡住

基本卡住在[reset] unmounting mounted directories in "/var/lib/kubelet"

Ctrl + c, 

systemctl restart docker.service

再试



#### [ERROR FileContent--proc-sys-net-bridge-bridge-nf-call-iptables]

在 kubeadm join 或者 kubeadm init 的时候：

``` 
[preflight] Running pre-flight checks
error execution phase preflight: [preflight] Some fatal errors occurred:
	[ERROR FileContent--proc-sys-net-bridge-bridge-nf-call-iptables]: /proc/sys/net/bridge/bridge-nf-call-iptables contents are not set to 1
	[ERROR FileContent--proc-sys-net-ipv4-ip_forward]: /proc/sys/net/ipv4/ip_forward contents are not set to 1
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...
```

解决： echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables

或者：sysctl net.bridge.bridge-nf-call-iptables=1 



#### [ERROR FileContent--proc-sys-net-ipv4-ip_forward]

echo 1 > /proc/sys/net/ipv4/ip_forward



#### Kubernetes ingress “an error on the server (”“) has prevented the request from succeeding”

Kubectl命令有时候 会报这个问题，可以加 -v=5 看详细输出，大概是向 master 的 6443端口被拒绝导致的。





### 网络插件-flannel

#### open /run/flannel/subnet.env: no such file or directory

```sh
# kubectl describe pods/coredns-6955765f44-mvdfd -n kube-system
...
network for pod "coredns-6955765f44-mvdfd": networkPlugin cni failed to set up pod "coredns-6955765f44-mvdfd_kube-system" network: open /run/flannel/subnet.env: no such file or directory
```



先看看有没有 /run/flannel/subnet.env， 没有则创建 ：

```
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
```





#### "cni0" already has an IP address different from 10.16.2.1/24

node 节点pod无法启动/节点删除网络重置

```
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
systemctl start docker
```



