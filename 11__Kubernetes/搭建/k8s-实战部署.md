---
title: "k8s-实战部署.md"
date: 2020-03-24 09:58:51 +0800
lastmod: 2020-03-24 09:58:51 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---


### 问题

看日志：

journalctl -xeu kubelet

kubectl -n work logs pod/saythx-frontend-5bd59fb6c4-vkkgt

进入 容器：kubectl exec -n work -it saythx-backend-74db8bbc87-zcqhz bash

删除pods:

kubectl -n work delete  pod/saythx-work-5c7975c9d7-lbxhc



### 删除节点

``` sh
kubectl get nodes
kubectl drain <node-name>
# 忽略 ds 和 删除本地的数据
kubectl drain <node-name> --ignore-daemonsets --delete-local-data
kubectl delete node <node-name>
# 如果删除的节点可达的话，将它 reset
kubeadm reset
```



### 删除pod,强制删除

```sh
# 强制删除 pod
kubectl delete pod/$p -n topsec --grace-period=0 --force
# 批量强制删除某命名空间下 Terminating 的 pod
for p in $(kubectl get pods -n topsec| grep Terminating | awk '{print $1}'); do kubectl delete pod/$p -n topsec --grace-period=0 --force;done
```





### 删除 ns 问题：is forbidden: unable to create new content in namespace topsec because it is being terminated

```sh
# 查看命名空间
# kubectl  get ns 
NAME                STATUS        AGE
default             Active        15h
kube-public         Active        15h
kube-system         Active        15h
topsec   Terminating   28m
```

ns 一直处于 terminating状态，不能删除。

删除

``` sh
NAMESPACE=topsec
kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
```





### 私有仓库 secret

``` sh
kubectl create secret docker-registry registry-key \
  --namespace=topsec \
  --docker-server=10.61.72.70:5001 \
  --docker-username=xxx \
  --docker-password=xxx
  # --docker-email=*****
```

**一定要指定命名空间，切不同命名空间不能够夸命名空间自动拉取镜像**

pod yaml 中配置拉取的secret:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-reg
spec:
  containers:
  - name: private-reg-container
    image: 10.61.72.70:5001/nginx:1.19
  imagePullSecrets:
  - name: registry-key
```



### 更改最大pod数

如果起200个pod, 个别pod会出现 Pod Node didn't have enough resource: pods, requested: 1, used: 110, capacity: 110, 这是告诉我们默认支持110个pod。

如果想支持更多，

我们可以更改 kubelet的配置， 末尾加上数量,  注意不能超过你定义的子网范围，比如你init初始的时候  /24 的子网范围，理论上每个pod一个ip，则最多一个pod可以配置 255 。

``` sh
# cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
# Note: This dropin only works with kubeadm and kubelet v1.11+
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
# This is a file that "kubeadm init" and "kubeadm join" generates at runtime, populating the KUBELET_KUBEADM_ARGS variable dynamically
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
# This is a file that the user can use for overrides of the kubelet args as a last resort. Preferably, the user should use
# the .NodeRegistration.KubeletExtraArgs object in the configuration files instead. KUBELET_EXTRA_ARGS should be sourced from this file.
EnvironmentFile=-/etc/default/kubelet
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS --max-pods=240
```

重启：

```sh
systemctl restart kubelet
systemctl status kubelet
```



验证：

``` sh
# kubectl describe node node70 | grep -i capacity -A 13
Capacity:
  cpu:                64
  ephemeral-storage:  452471344Ki
  hugepages-512Mi:    0
  memory:             533129536Ki
  pods:               240
Allocatable:
  cpu:                64
  ephemeral-storage:  416997589940
  hugepages-512Mi:    0
  memory:             533027136Ki
  pods:               240
System Info:
  Machine ID:                 ea5edc9a40514c3da2a1a86de5a2be81

```




