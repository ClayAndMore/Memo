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






