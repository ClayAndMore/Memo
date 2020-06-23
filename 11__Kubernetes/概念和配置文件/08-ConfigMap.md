---

title: "08-ConfigMap.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---



### ConfigMap

许多应用程序会从配置文件、命令行参数或环境变量中读取配置信息。这些**配置信息需要与docker image解耦**，你总不能每修改一个配置就重做一个image吧？ConfigMap API给我们提供了向容器中注入配置信息的机制，ConfigMap可以被用来保存单个属性，也可以用来保存整个配置文件或者JSON二进制大对象。

### 创建 ConfigMap

#### 从 key-value 字符串创建

可以使用 `kubectl create configmap` 从文件、目录或者 key-value 字符串。

```sh
$ kubectl create configmap special-config --from-literal=special.how=very
configmap "special-config" created
$ kubectl get configmap special-config -o go-template='{{.data}}'
map[special.how:very]
```

创建了一个名为special-config，拥有一条key为`special.how`，value为`very`的键值对数据。

#### 从 env 文件创建

``` sh
$ echo -e "a=b\nc=d" | tee config.env
a=b
c=d
$ kubectl create configmap special-config --from-env-file=config.env
configmap "special-config" created
$ kubectl get configmap special-config -o go-template='{{.data}}'
map[a:b c:d]
```

从一个env文件读取键值对，然后存入一个名为special-config的ConfigMap中。

#### 从目录创建

``` sh
$ mkdir config
$ echo a>config/a
$ echo b>config/b
$ kubectl create configmap special-config --from-file=config/
configmap "special-config" created
$ kubectl get configmap special-config -o go-template='{{.data}}'
map[a:a
 b:b
]
```

读取config目录下的所有文件，以**文件名为key，文件内容为value**，存入名为special-config的ConfigMap中。



#### 根据 yaml 文件创建

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
data:
  special.how: very
  special.type: charm
```

创建：

```ruby
$ kubectl create  -f  config.yaml
configmap "special-config" created
```



### 查看

```bash
 kubectl get configmaps game-config -o yaml
 #如果找不到 记得指定命名空间试下:
 kubectl get configmap/trireme-config -n kube-system -o yaml
```



### ConfigMap 的使用

Pod可以通过三种方式来使用ConfigMap，分别为：

- 将ConfigMap中的数据设置为环境变量
- 将ConfigMap中的数据设置为命令行参数
- 使用Volume将ConfigMap作为文件或目录挂载

> **注意！！**
>
> - ConfigMap必须在Pod使用它之前创建
> - Pod只能使用同一个命名空间的ConfigMap



#### 用作环境变量

首先创建两个ConfigMap，分别名为`special-config`和`env-config`：

```csharp
$ kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
$ kubectl create configmap env-config --from-literal=log_level=INFO
```

然后以环境变量方式引用：

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "env" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
      envFrom:    
        - configMapRef:
            name: env-config
  restartPolicy: Never
```

当pod 运行结束后，输出如下：

```
SPECIAL_LEVEL_KEY=very
SPECIAL_TYPE_KEY=charm
log_level=INFO
```



#### 用作命令行参数

将ConfigMap用作命令行参数时，需要先把ConfigMap的数据保存在环境变量中，然后**通过$(VAR_NAME)的方式引用环境变量**。

上方的command改为：

`command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]` 

输出：`very charm`



#### 使用 volume 将 ConfigMap 作为文件或目录挂载

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: vol-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "cat /etc/config/special.how" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
  restartPolicy: Never
```

将创建的ConfigMap直接挂载至Pod的/etc/config目录下，其中**每一个key-value键值对都会生成一个文件，key为文件名，value为内容**。

输出： `very`



``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh","-c","cat /etc/config/keys/special.level" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
        items:
        - key: special.how
          path: keys/special.level
  restartPolicy: Never
```

将创建的ConfigMap中special.how这个key挂载到/etc/config目录下的一个相对路径/keys/special.level。如果存在同名文件，直接覆盖。其他的key不挂载。

输出：`very`

``` sh
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: nginx
      command: ["/bin/sh","-c","sleep 36000"]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/nginx/special.how
        subPath: special.how
  volumes:
    - name: config-volume
      configMap:
        name: special-config
        items:
        - key: special.how
          path: special.how
  restartPolicy: Never
```

在一般情况下 configmap 挂载文件时，会先覆盖掉挂载目录，然后再将 congfigmap 中的内容作为文件挂载进行。如果想不对原来的文件夹下的文件造成覆盖，只是将 configmap 中的每个 key，按照文件的方式挂载到目录下，可以使用 subpath 参数。

``` sh
root@dapi-test-pod:/# ls /etc/nginx/
conf.d    fastcgi_params    koi-utf  koi-win  mime.types  modules  nginx.conf  scgi_params    special.how  uwsgi_params  win-utf
root@dapi-test-pod:/# cat /etc/nginx/special.how
very
```

