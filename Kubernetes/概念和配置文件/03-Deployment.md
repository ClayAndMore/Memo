---
title: "03-Deployment.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---
## Deployment

Deployment对象，顾名思义，是用于部署应用的对象。它使Kubernetes中最常用的一个对象，它为ReplicaSet和Pod的创建提供了一种声明式的定义方法，从而无需手动创建ReplicaSet和Pod对象（使用Deployment而不直接创建ReplicaSet是因为Deployment对象拥有许多ReplicaSet没有的特性，例如滚动升级和回滚）。

### 创建

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```





### 查看deployment:

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

查看deployment:

``` sh
$kubectl get deployments
NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3         0         0            0           1s

# kubectl get deployments -A
NAMESPACE     NAME                READY   UP-TO-DATE   AVAILABLE   AGE
kube-system   coredns             2/2     2            2           22h
kube-system   nginx-deployment    1/1     1            1           6h33m
kube-system   nginx2-deployment   1/1     1            1           5h24m
```

* `NAME`代表Deployment的名字
* `DESIRED`代表这个Deployment期望的副本数量
* `CURRENT`代表当前已经创建了的副本数量
* `UP-TO-DATE`代表已经更新完成的副本数量
* `AVAILABLE`代表对于当前用户可用的副本数量，
* `AGE`代表当前Deployment已经运行的时长。

``` sh
# kubectl get rs -A
NAMESPACE     NAME                          DESIRED   CURRENT   READY   AGE
kube-system   coredns-6955765f44            2         2         2       22h
kube-system   nginx-deployment-85dfbdd967   1         1         1       6h34m
kube-system   nginx2-deployment-cb5b85b7f   1         1         1       5h25m
```

通过`kubectl get rs`来查看系统中ReplicaSet对象，由此可以看出**Deployment会自动创建一个ReplicaSet对象。**



### 更新

假如我们现在想要让 nginx pod 使用 nginx:1.9.1 的镜像来代替原来的 nginx:1.7.9 的镜像，运行以下命令：

```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```

或者我们可以使用 edit 命令来编辑 Deployment，将image从nginx:1.7.9 改写成 nginx:1.9.1。

```undefined
kubectl edit deployment/nginx-deployment
```

查看更新进度：

```csharp
$ kubectl rollout status deployment/nginx-deployment
Waiting for rollout to finish: 2 out of 3 new replicas have been updated...
deployment "nginx-deployment" successfully rolled out
```

扩容：

```undefined
kubectl scale deployment nginx-deployment --replicas 10
```

如果集群支持 horizontal pod autoscaling 的话，还可以为 Deployment 设置自动扩展：

```swift
kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80
```

Deployment更新时会创建一个新的ReplicaSet，然后将新的ReplicaSet中的Pod慢慢扩容到指定的副本数，将旧的ReplicaSet慢慢缩容到0。因此，更新时总能够确保旧的服务不会停止，这就是滚动更新。



### 回滚

当我们像上文一样更新了Deployment之后，我们发现nginx:1.9.1的镜像不是很稳定，因此想要修改回nginx:1.7.9的版本，此时我们不需要手动更改Deployment文件，而是利用Deployment的回滚功能。

使用rollout history命令查看Deployment的版本（revision）：



```bash
$ kubectl rollout history deployment/nginx-deployment
deployments "nginx-deployment":
REVISION    CHANGE-CAUSE
1           kubectl create -f docs/user-guide/nginx-deployment.yaml --record
2           kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```

> 因为我们创建 Deployment 的时候使用了 —recored 参数可以记录命令，我们可以很方便的查看每次 revison 的变化。

查看单个 revision 的详细信息：

```bash
kubectl rollout history deployment/nginx-deployment --revision=2
```

现在，可以使用`rollout undo`命令回滚到前一个revision：

```ruby
$ kubectl rollout undo deployment/nginx-deployment
deployment "nginx-deployment" rolled back
```

也可以使用`--to-revision`参数指定某个历史版本：

```ruby
$ kubectl rollout undo deployment/nginx-deployment --to-revision=2
deployment "nginx-deployment" rolled back
```



### rollout 命令

`rollout`命令的更多用法：

history （查看历史版本）

```sh
# 查看deployment的历史记录
kubectl rollout history deployment/abc
# 查看daemonset修订版3的详细信息
kubectl rollout history daemonset/abc --revision=3
```

pause 暂停Deployment

```
kubectl rollout pause deployment/nginx
```

resume 恢复暂停的Deployment

```
kubectl rollout resume deployment/nginx
```

status查看资源状态

``` sh
c# kubectl rollout status deployment/nginx-deployment -n kube-system
deployment "nginx-deployment" successfully rolled out
```



