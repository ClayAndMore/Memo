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



### nodeName

nodeName是节点选择约束的最简单形式，但是由于其限制，通常很少使用它。nodeName是PodSpec的领域。

pod.spec.nodeName将Pod直接调度到指定的Node节点上，会【跳过Scheduler的调度策略】，该匹配规则是【强制】匹配。可以越过Taints污点进行调度。

nodeName用于选择节点的一些限制是：

- 如果指定的节点不存在，则容器将不会运行，并且在某些情况下可能会自动删除。
- 如果指定的节点没有足够的资源来容纳该Pod，则该Pod将会失败，并且其原因将被指出，例如OutOfmemory或OutOfcpu。
- 云环境中的节点名称并非总是可预测或稳定的。



### nodeSelector

nodeSelector是节点选择约束的最简单推荐形式。nodeSelector是PodSpec的领域。它指定键值对的映射。

Pod.spec.nodeSelector是通过Kubernetes的label-selector机制选择节点，由调度器调度策略匹配label，而后调度Pod到目标节点，该匹配规则属于【强制】约束。由于是调度器调度，因此不能越过Taints污点进行调度。

运行kubectl get nodes以获取群集节点的名称。然后可以对指定节点添加标签。比如：k8s-node01的磁盘为SSD，那么添加disk-type=ssd；k8s-node02的CPU核数高，那么添加cpu-type=hight；如果为Web机器，那么添加service-type=web。怎么添加标签可以根据实际规划情况而定。

```sh
 1 ### 给k8s-node01 添加指定标签
 2 [root@k8s-master ~]# kubectl label nodes k8s-node01 disk-type=ssd
 3 node/k8s-node01 labeled
 4 #### 删除标签命令 kubectl label nodes k8s-node01 disk-type-
 5 [root@k8s-master ~]# 
 6 [root@k8s-master ~]# kubectl get node --show-labels
 7 NAME         STATUS   ROLES    AGE   VERSION   LABELS
 8 k8s-master   Ready    master   42d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux,node-role.kubernetes.io/master=
 9 k8s-node01   Ready    <none>   42d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,disk-type=ssd,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node01,kubernetes.io/os=linux
10 k8s-node02   Ready    <none>   42d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernete
```

yaml：

``` yaml
# cat scheduler_nodeSelector.yaml 
 5 apiVersion: apps/v1
 6 kind: Deployment
 7 metadata:
 8   name: scheduler-nodeselector-deploy
 9   labels:
10     app: nodeselector-deploy
11 spec:
12   replicas: 5
13   selector:
14     matchLabels:
15       app: myapp
16   template:
17     metadata:
18       labels:
19         app: myapp
20     spec:
21       containers:
22       - name: myapp-pod
23         image: registry.cn-beijing.aliyuncs.com/google_registry/myapp:v1
24         imagePullPolicy: IfNotPresent
25         ports:
26           - containerPort: 80
27       # 指定节点标签选择，且标签存在
28       nodeSelector:
29         disk-type: ssd
```

