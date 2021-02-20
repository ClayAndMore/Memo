---
title: "01-Pod.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---


### 理解pod

Pod是kubernetes中你可以创建和部署的最小也是最简的单位。Pod代表着集群中运行的进程。

Pod中封装着应用的容器（有的情况下是好几个容器），存储、独立的网络IP，管理容器如何运行的策略选项。

根据Docker的结构，Pod中的容器共享namespace和volume，不支持共享PID的namespace。

Pod代表着部署的一个单位：kubernetes中应用的一个实例，可能由一个或者多个容器组合在一起共享资源。

在Kubernetes集群中Pod有如下两种使用方式：

- **一个Pod中运行一个容器**。“每个Pod中一个容器”的模式是最常见的用法；在这种使用方式中，你可以把Pod想象成是单个容器的封装，kuberentes管理的是Pod而不是直接管理容器。
- **在一个Pod中同时运行多个容器**。一个Pod中也可以同时封装几个需要紧密耦合互相协作的容器，它们之间共享资源。这些在同一个Pod中的容器可以互相协作成为一个service单位——一个容器共享文件，另一个“sidecar”容器来更新这些文件。Pod将这些容器的存储资源作为一个实体来管理。



**每个Pod都是应用的一个实例。如果你想平行扩展应用的话（运行多个实例），你应该运行多个Pod，每个Pod都是一个应用实例。在Kubernetes中，这通常被称为replication。**



### pod 中如何管理多个容器

Pod中可以同时运行多个进程（作为容器运行）协同工作。同一个Pod中的容器会自动的分配到同一个 node 上。同一个Pod中的容器共享资源、网络环境和依赖，它们总是被同时调度。

注意在一个Pod中同时运行多个容器是一种比较高级的用法。只有当你的容器需要紧密配合协作的时候才考虑用这种模式。例如，你有一个容器作为web服务器运行，需要用到共享的volume，有另一个“sidecar”容器来从远端获取资源更新这些文件：

```
   file pull
    +
    |
+----------------------------------+
|   |                              |
| +-v------+       +------------+  |
| | sidecar|       | web server |  |
| +-+------+       +-----+------+  |
|   |                    ^         |
|   |                    |         |
|   |    +-------------+ |         |
|   +--> | volume      +-+         |
|        +-------------+           |
|                                  |
+----------------------------------+
          pod
```



### 共享资源

处于一个Pod中的多个容器共享以下资源：

- PID命名空间：Pod中不同的应用程序可以看到其他应用程序的进程ID。
- network命名空间：Pod中多个容器处于同一个网络命名空间，因此能够访问的IP和端口范围都是相同的。也可以通过localhost相互访问。
- IPC命名空间：Pod中的多个容器共享Inner-process Communication命名空间，因此可以通过SystemV IPC或POSIX进行进程间通信。
-  UTS命名空间：Pod中的多个容器共享同一个主机名。
-  Volumes：Pod中各个容器可以共享在Pod中定义分存储卷（Volume）

网络：

每个Pod都会被分配一个唯一的IP地址。Pod中的所有容器共享网络空间，包括IP地址和端口。Pod内部的容器可以使用`localhost`互相通信。Pod中的容器与外界通信时，必须分配共享网络资源（例如使用宿主机的端口映射）。

存储：

可以为一个Pod指定多个共享的Volume。Pod中的所有容器都可以访问共享的volume。Volume也可以用来持久化Pod中的存储资源，以防容器重启后文件丢失。





### 使用pod

你很少会直接在kubernetes中创建单个Pod。因为Pod的生命周期是短暂的，用后即焚的实体。当Pod被创建后（不论是由你直接创建还是被其他Controller），都会被Kubernetes调度到集群的Node上。直到Pod的进程终止、被删掉、因为缺少资源而被驱逐、或者Node故障之前这个Pod都会一直保持在那个Node上。

> 注意：重启Pod中的容器跟重启Pod不是一回事。Pod只提供容器的运行环境并保持容器的运行状态，重启容器不会造成Pod重启。

Pod不会自愈。如果Pod运行的Node故障，或者是调度器本身故障，这个Pod就会被删除。同样的，如果Pod所在Node缺少资源或者Pod处于维护状态，Pod也会被驱逐。Kubernetes使用更高级的称为Controller的抽象层，来管理Pod实例。虽然可以直接使用Pod，但是在Kubernetes中通常是使用Controller来管理Pod的。



### 创建

``` yaml
apiVersion: v1
kind: Pod
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

labels：是一个个的key/value对，定义这样的label到Pod后，其他控制器对象可以通过这样的label来定位到此Pod，从而对Pod进行管理。（参见Deployment等控制器对象）

spec： 其它描述信息，包含Pod中运行的容器，容器中运行的应用等等。不同类型的对象拥有不同的spec定义。

定义Pod时，可以指定restartPolicy字段，表明此Pod中的容器在何种条件下会重启。restartPolicy拥有三个候选值：

- Always：只要退出就重启
- OnFailure：失败退出时（exit code不为0）才重启
- Never：永远不重启



#### 有关 pause 容器

Kubernetes在每个Pod启动时，会自动创建一个镜像为gcr.io/google_containers/pause:version的容器，所有处于该Pod中的容器在启动时都会添加诸如`--net=container:pause --ipc=contianer:pause --pid=container:pause`的启动参数，因此pause容器成为Pod内共享命名空间的基础。所有容器共享pause容器的IP地址，也被称为Pod IP。

如果我们希望从外部访问这nginx应用，那么我们还需要创建Service对象来暴露IP和port。详见kubernetes Service



### 生命周期

Pod的生命周期是Replication Controller进行管理的。一个Pod的生命周期过程包括：

- 通过yaml或json对Pod进行描述
- apiserver（运行在Master主机）收到创建Pod的请求后，将此Pod对象的定义存储在etcd中
- scheduler（运行在Master主机）将此Pod分配到Node上运行
- Pod内所有容器运行结束后此Pod也结束

在整个过程中，Pod通常处于以下的五种阶段之一：

- Pending：Pod定义正确，提交到Master，但其所包含的容器镜像还未完全创建。通常，Master对Pod进行调度需要一些时间，Node进行容器镜像的下载也需要一些时间，启动容器也需要一定时间。（写数据到etcd，调度，pull镜像，启动容器）。
- Running：Pod已经被分配到某个Node上，并且所有的容器都被创建完毕，至少有一个容器正在运行中，或者有容器正在启动或重启中。
- Succeeded：Pod中所有的容器都成功运行结束，并且不会被重启。这是Pod的一种最终状态。
- Failed：Pod中所有的容器都运行结束了，其中至少有一个容器是非正常结束的（exit code不是0）。这也是Pod的一种最终状态。
- Unknown：无法获得Pod的状态，通常是由于无法和Pod所在的Node进行通信。



### controller

> Pod本身不具备容错性，这意味着如果Pod运行的Node宕机了，那么该Pod无法恢复。因此推荐使用Deployment等控制器来创建Pod并管理。

一般来说，Pod不会自动消失，只能手动销毁或者被预先定义好的controller销毁。但有一种特殊情况，当Pod处于Succeeded或Failed阶段，并且超过一定时间后（由master决定），会触发超时过期从而被销毁。

总体上来说，Kubernetes中拥有三种类型的controller：

- Job。通常用于管理一定会结束的Pod。如果希望Pod被Job controller管理，那么restartPolicy必须指定为OnFailure或Never。
- ReplicationController，ReplicaSet和Deployment。用于管理永远处于运行状态的Pod。如果希望Pod被此类controller管理，那么restartPolicy必须指定为Always。
- DaemonSet。它能够保证你的Pod在每一台Node都运行一个副本。



### 一 pod 多容器

``` yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-c-run
  name: nginx-containers
spec:
  containers:
  - image: nginx:alpine
    name: nginx1
    command: ["sleep"]
    args: ["100000"]
  - image: nginx:alpine
    name: nginx2
    command: ["sleep"]
    args: ["100000"]
```

