---
title: "02-ReplicaSet.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---
## ReplicaSet

说到ReplicaSet对象，得先说说ReplicationController（简称为RC）。

在旧版本的Kubernetes中，只有ReplicationController对象。它的主要作用是**确保Pod以你指定的副本数运行**，即如果有容器异常退出，会自动创建新的 Pod 来替代；而异常多出来的容器也会自动回收。

在新版本的 Kubernetes 中建议使用 ReplicaSet（简称为RS ）来取代 ReplicationController。ReplicaSet 跟 ReplicationController 没有本质的不同，只是名字不一样，并且 ReplicaSet 支持集合式的 selector（ReplicationController 仅支持等式）

虽然也 ReplicaSet 可以独立使用，但建议使用 Deployment 来自动管理 ReplicaSet，这样就无需担心跟其他机制的不兼容问题（比如 ReplicaSet 不支持 rolling-update 但 Deployment 支持），并且Deployment还支持版本记录、回滚、暂停升级等高级特性。

Kubernetes官方强烈建议避免直接使用ReplicaSet，而应该通过Deployment来创建RS和Pod。



### RS 的创建

``` YAML
apiVersion: v1
kind: ReplicaSet
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    app: nginx
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```

* **spec.selector字段指定为你需要管理的Pod的label（label的意义体现在此处）。这儿将spec.selector设置为app: nginx，意味着所有包含label：app: nginx的Pod都将被这个RC管理**
* spec.replicas字段代表了受此RC管理的Pod，需要运行的副本数。
* template模块用于定义Pod，包括Pod的名字，Pod拥有的label以及Pod中运行的应用。



### RS 的删除

使用`kubectl delete`命令会删除此RS以及它管理的Pod。在Kubernetes删除RS前，会将RS的replica调整为0，等待所有的Pod被删除后，在执行RS对象的删除。如果希望仅仅删除RS对象（保留Pod），请使用`kubectl delete`命令时添加`--cascade=false`选项。



### Horizontal Pod Autoscaler（HPA）

RS可以通过HPA来根据一些运行时指标实现自动伸缩，下面是一个简单的例子：



```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-scaler
spec:
  scaleTargetRef:
    kind: ReplicaSet
    name: nginx
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```



### 其他值

#### minReadySeconds 

这个值意味着从容器启动到应用正常提供服务所需要的时间 s（秒），这个值默认是 `0`

新创建的Pod状态为Ready持续的时间至少为`.spec.minReadySeconds`才认为Pod Available(Ready)。

- Kubernetes在等待设置的时间后才进行升级
- 如果没有设置该值，Kubernetes会假设该容器启动起来后就提供服务了
- 如果没有设置该值，在某些极端情况下可能会造成服务服务不正常正常运行

eg:

``` yaml
apiVersion: apps/v1beta1
kind: DaemonSet
metadata:
  name: relationship-c-ds
  labels:
    name: relationship-c-agent-ds
    app: relationship-c-app-ds
  namespace: topsec
spec:
  minReadySeconds: 5
  selector:
    matchLabels:
      app: relationship-c-app
  template:
```

