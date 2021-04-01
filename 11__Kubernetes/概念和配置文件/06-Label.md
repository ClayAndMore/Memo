---

title: "06-Label.md"
date: 2020-04-03 19:50:52 +0800
lastmod: 2020-04-03 19:50:52 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---
## label

Label是Kubernetes系统中的一个核心概念。**Label以key/value键值对的形式附加到任何对象上，如Pod，Service，Node，RC（ReplicationController）/RS（ReplicaSet）等**。Label可以在创建对象时就附加到对象上，也可以在对象创建后通过API进行额外添加或修改。

在为对象定义好Label后，其他对象就可以通过Label来对对象进行引用。Label的最常见的用法便是通过**spec.selector**来引用对象



### 定义和创建

我们通常使用**metadata.labels**字段，来为对象添加Label。Label可以为多个。一个简单的例子如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    release: stable
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
```

上面的描述文件为名为nginx的Pod添加了两个Label，分别为`app: nginx`和`release: stable`。



### 常见的label

一般来说，我们会给一个Pod（或其他对象）定义多个Label，以便于配置，部署等管理工作。例如：部署不同版本的应用到不同的环境中；或者监控和分析应用（日志记录，监控，报警等）。通过多个Label的设置，我们就可以多维度的Pod或其他对象进行精细化管理。一些常用的Label示例如下：

```yaml
relase: stable
release: canary
environment: dev
environemnt: qa
environment: production
tier: frontend
tier: backend
tier: middleware
```



### Label Selector

新建一个RC的例子：

``` yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```

关于Label的用法重点在于这两步：

- 通过**template.metadata.labels**字段为即将新建的Pod附加Label。在上面的例子中，新建了一个名称为nginx的Pod，它拥有一个键值对为`app:nginx`的Label。
- 通过**spec.selector**字段来指定这个RC管理哪些Pod。在上面的例子中，新建的RC会管理所有拥有`app:nginx`Label的Pod。这样的**spec.selector**在Kubernetes中被称作**Label Selector**。



### node label

``` sh
# kubectl get node --show-labels
NAME      STATUS   ROLES    AGE    VERSION   LABELS
node200   Ready    master   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node200,kubernetes.io/os=linux,node-role.kubernetes.io/master=

node201   Ready    <none>   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node201,kubernetes.io/os=linux
```

由此可见，master 会有单独的标签 `node-role.kubernetes.io/master=`

添加标签：

``` sh
# kubectl label nodes node200 myNode=200
node/node200 labeled

# kubectl get node --show-labels
NAME      STATUS   ROLES    AGE    VERSION   LABELS
node200   Ready    master   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node200,kubernetes.io/os=linux,myNode=200,node-role.kubernetes.io/master=
node201   Ready    <none>   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node201,kubernetes.io/os=linux
```

删除标签：

``` sh
# kubectl label nodes node200 myNode-
node/node200 labeled

# kubectl get node --show-labels
NAME      STATUS   ROLES    AGE    VERSION   LABELS
node200   Ready    master   134d   v1.17.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node200,kubernetes.io/os=linux,node-role.kubernetes.io/master=
node201   Ready    <none>   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node201,kubernetes.io/os=linux
```

