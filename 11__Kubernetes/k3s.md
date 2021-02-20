k3s 是 Rancher 推出的轻量级 k8s。k3s 本身包含了 k8s 的源码，所以本质上和 k8s 没有区别。但为了降低资源占用，k3s 和 k8s 还是有一些区别的，主要是：

使用了相比 Docker 更轻量的 containerd 作为容器运行时（Docker 并不是唯一的容器选择）
去掉了 k8s 的 Legacy, alpha, non-default features
用 sqlite3 作为默认的存储，而不是 etcd
其他的一些优化，最终 k3s 只是一个 binary 文件，非常易于部署
所以 k3s 适用于边缘计算，IoT 等资源紧张的场景。同时 k3s 也是非常容易部署的

``` sh
# 启动服务
k3s server --docker  # --docker 是声明指定使用docker，默认使用containerc

k3s kubectl get nodes
NAME   STATUS     ROLES    AGE     VERSION
12     NotReady   <none>   4d22h   v1.19.3+k3s2
ft3    Ready      master   4d2h    v1.19.3+k3s2
ft1    Ready      master   4d22h   v1.19.3+k3s2


# 获取密钥
cat /var/lib/rancher/k3s/server/node-token
K10e4f0ac06fc41b71da65909f3d01548326d93d1f531a4eeda21ced101c3d17b6f::server:57874bb74bd1c201e0111a7e2bac6543


# 加入
k3s agent --server https://10.8.1.4:6443 --token=

```

