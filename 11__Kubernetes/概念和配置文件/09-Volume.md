---

title: "09-volume挂载.md"
date: 2020-03-26 18:40:49 +0800
lastmod: 2020-03-26 18:40:49 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---
## Volume

volume是Pod中能够被多个容器共享的磁盘目录，可以称之为挂载卷。

我们知道，默认情况下Docker容器中的数据都是非持久化的，在容器消亡后数据也会消失。因此Docker提供了Volume机制以便实现数据的持久化。Kubernetes中Volume的概念与Docker中的Volume类似，但不完全相同。具体区别如下：

- Kubernetes中的Volume与Pod的生命周期相同，但与容器的生命周期不相关。当容器终止或重启时，Volume中的数据也不会丢失。
- 当Pod被删除时，Volume才会被清理。并且数据是否丢失取决于Volume的具体类型，比如emptyDir类型的Volume数据会丢失，而PV类型的数据则不会丢失。



### 类型

Kubernetes提供了非常丰富的Volume类型，下面是一些常用的Volume类型：

- emptyDir
- hostPath



### emptyDir

一个emptyDir volume是在Pod分配到Node时创建的。顾名思义，它的初始内容为空，在同一个Pod中的所有容器均可以读写这个emptyDir volume。当 Pod 从 Node 上被删除（Pod 被删除，或者 Pod 发生迁移），emptyDir 也会被删除，并且数据永久丢失。
 一个简单的例子：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

emptyDir类型的volume适合于以下场景：

- 临时空间。例如某些程序运行时所需的临时目录，无需永久保存。

- 一个容器需要从另一容器中获取数据的目录（多容器共享目录）, eg:

  volume.yaml:

  ``` yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: test-pd
  spec:
    containers:
    - image: wangyanglinux/myapp:v2
      name: test-container
      volumeMounts:
      - mountPath: /cache
        name: cache-volume
    - name: liveness-exec-container
      image: busybox
      imagePullPolicy: IfNotPresent
      command: ["/bin/sh","-c","sleep 6000s"]
      volumeMounts:
      - mountPath: /cache
        name: cache-volume
    volumes:
      - name: cache-volume
        emptyDir: {}
  ```

  kubectl describe pod test-pd:

  ``` yaml
  Containers:
    test-container:
      Container ID:   docker://236b2b8c29ed6d42b74aaef24bc1d43d21863598c7c5a5cd19b9fc953993c7c0
  	...
      Mounts:
        /cache from cache-volume (rw)
        /var/run/secrets/kubernetes.io/serviceaccount from default-token-6wcrh (ro)
    liveness-exec-container:
      Container ID:  docker://304943afd2171d58d2b36d93f3833405f7e2651ffb67ad807adaf80c8a6fd330
      ...
      Mounts:
        /cache from cache-volume (rw)
        /var/run/secrets/kubernetes.io/serviceaccount from default-token-6wcrh (ro)
  ```

  可以看到/cache这个目录





### hostPath

hostPath类型的volume允许用户挂在Node上的文件系统到Pod中，**如果 Pod 需要使用 Node 上的文件，可以使用 hostPath。**

``` yaml
      containers:
        -  name: trireme-enforcer
           image: trireme-k8s:latest
           command: ["tail", "-f","/dev/null"]
           env:
             - name: TOPSEC_TRIREME_KUBENODENAME
               valueFrom:
                 fieldRef:
                   fieldPath: spec.host
           securityContext:
             privileged: true
           volumeMounts:
             - mountPath: /var/run
               name: dockersock
               readOnly: false
             - mountPath: /test-vo
               name: test-volume
      volumes:
        - name: dockersock
          hostPath:
            path: /var/run
        - name: test-volume
          hostPath:
            path: /data
            type: Directory
```

主机目录 /data,  容器目录 /test-vo

/test-vo 在容器里会自动创建，/data 需要我们手动创建(根据type指定的方式而不同)，**是在pod运行的node里创建。**， /data里的内容会覆盖到容器 /test-vo 里的内容

不管在 容器中还是主机中操作挂载目录，相关的内容都会同步。

当我们删除该 pod 时， data里的内容 还是会存在。

type类型：

| 值                  | 行为                                                         |
| :------------------ | :----------------------------------------------------------- |
|                     | 空字符串（默认）用于向后兼容，在挂载 hostPath 卷之前不会执行任何检查 |
| `DirectoryOrCreate` | 将根据需要在那里创建一个空目录，权限设置为 0755，与 Kubelet 具有相同的组和权限 |
| `Directory`         | 给定的路径下必须存在目录                                     |
| `FileOrCreate`      | 会根据需要创建一个空文件，权限设置为 0644，与 Kubelet 具有相同的组和权限 |
| `File`              | 给定的路径下必须存在文件                                     |
| `Socket`            | 给定的路径下必须存在 UNIX 套接字                             |
| `CharDevice`        | 给定的路径下必须存在字符设备                                 |
| `BlockDevice`       | 给定的路径下必须存在块设备                                   |



### subPath  挂载单个文件

在`Pod`中通过`volume`挂载数据的时候，如果挂载目录下原来有文件，挂载后将被覆盖掉。

有的时候，我们希望将文件挂载到某个目录，但希望只是挂载该文件，不要影响挂载目录下的其他文件。

这时可以使用subPath



### PV

涉及到 kind: PersistentVolume，StorageClass, PersistentVolumeClaim

参考：

https://www.jianshu.com/p/99e610067bc8

https://draveness.me/kubernetes-volume

