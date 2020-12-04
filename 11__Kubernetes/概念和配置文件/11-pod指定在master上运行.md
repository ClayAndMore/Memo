---
title: "pod指定在master上运行.md"
date: 2020-04-07 08:49:48 +0800
lastmod: 2020-04-07 08:49:48 +0800
draft: false
tags: [""]
categories: ["k8s"]
author: "Claymore"

---


在某些场景，例如资源有限或特殊的拓扑结构下，需要将某些服务可以或者指定到k8s的master节点进行运行。



### 配置文件

这时候就需要通过修改pod的配置，使其可以在任意节点上运行（包括master和node）：

```yaml
tolerations:
    - key: node-role.kubernetes.io/master
      effect: NoSchedule
```


如果需要指定必须在master上执行，需要再配置nodeSelector：

```
nodeSelector:
    node-role.kubernetes.io/master: ""
```



Demo:

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: kube-system

spec:
  selector:
    matchLabels:
      name: nginx1
  replicas: 1 
  template:
    metadata:
      labels:
        name: nginx1
    spec:
      containers:
      - name: nginx1
        image: nginx:alpine
        ports:
        - containerPort: 80
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      nodeSelector:
        node-role.kubernetes.io/master: ""
```



### 命令

如果希望将k8s-master也当作Node使用，可以执行如下命令：

```
kubectl taint node k8s-master node-role.kubernetes.io/master-
```

其中k8s-master是主机节点hostname如果要恢复Master Only状态，执行如下命令：


```
kubectl taint node k8s-master node-role.kubernetes.io/master=""
```