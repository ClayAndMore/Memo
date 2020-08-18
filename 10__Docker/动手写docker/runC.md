---
title: "runC.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["动手写Docker"]
categories: ["Docker"]
author: "Claymore"

---


### 由来

过去几年内，linux 增加了 Cgroups,Namespace, Seccomp 等一些功能， Docker 严重依赖这些特性。

实际上容器技术是一系列晦涩难懂的 系统特性集合， 因此， Docker 公司将这些底层的技术合并在一起，开源出一个项目runC.

实际上， runC 是由 Docker 公司 libcontainer 项目发展而来的， 托管于OCI组织。



#### OCI 组织

Linux 基金会在2015年6月份成立了 OCI (open Container Initiative), ps: Initiative(倡议),  

**旨在围绕容器格式定义和运行时配置定制一个开放的工业化标准。**

`github: https://github.com/opencontainers/`



runC 是一个轻量级的容器运行引擎，包括所有Docker 使用和容器相关的系统调用代码。

可以这样立即，runC 的目标就是构造到处可以运行的标准容器。

单的说，OCI有两个规范:

* 一个是容器运行时规范`runtime-spec`
* 一个是镜像格式规范`image-spec`。

一个镜像，简单来说就是一个打包好的符合OCI规范的`filesystem bundule`。

而bundile的话，包含一个配置文件`config.json`和一个rootfs目录。



### OCI 标准包（bundle）

一个标准的容器运行时需要文件系统， 也就是镜像。

OCI 是怎样定义一个基本的容器运行包的呢？

这个容器标准包的定义仅仅考虑如何把容器和它的配置数据存储到磁盘上以便运行时读取。

一般包含两个模块：

* config.json 包括容器的配置数据，这个文件必须在容器的root文件系统内。

* 一个文件夹，代表容器的root文件系统。

  这个文件夹的名字理论上是可以随意的，但是按照一般命名规则，叫 rootfs 比较合适。

  当然这个文件夹内必须包含上面提到的config.json.



#### config.json

```json
ociVersion  // OCI 容器版本号
"root":{    // 配置容器的root文件系统
    "path": "rootfs",  // 指定root文件系统路径，可以是/开头的绝对路径，也可以是相对路径
    “readonly”: true // 如为true, root文件系统在容器内就是只读的，默认是false.
},
“mounts”:[  // 配置额外的挂载点
    {
        "destination": "/tmp",  //挂载点在容器内的目标位置，必须是绝对路径 。
        "type": "tmpfs", // 需要挂载的文件系统类型
        "source":  "tmpfs", // 设备名或文件名
        "options": [ "nosuid", "strictatime", "mode=755", "size=65536k"] //额外信息
    }，
    {
    	"destination":"/data",
    	"type": "bind",
    	"source": "/volumes/testing",
    	"options":["rbind","rw"]
    ｝
],
```

process 配置容器进程信息：

```json
"process": {
    "terminal": true, //是否需要连接一个终端到此进程，默认false
    "consoleSize": {  // 在terminal 连接时，指定控制台大小，包含下面两个属性。
        "height": 25,
        "width": 80
    },
    "user": {   //指定容器内运行进程的用户信息
        "uid": 1,
        "gid": 1,
        "additionalGids": [5, 6] //附加的 groups ID
    },
    "env": [  // 需要传递给进程的环境变量，变量格式必须是KEY=value的格式。
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "TERM=xterm"
    ],
    "cwd": "/root",  //可执行文件的工作目录，必须是绝对路径。
    "args": [   // 转递给可执行文件的参数
        "sh"
    ],
    "apparmorProfile": "acme_secure_profile",
    "selinuxLabel": "system_u:system_r:svirt_lxc_net_t:s0:c124,c675",
    "noNewPrivileges": true,
    "capabilities": {
        "bounding": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
       "permitted": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
       "inheritable": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
        "effective": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL"
        ],
        "ambient": [
            "CAP_NET_BIND_SERVICE"
        ]
    },
    "rlimits": [     // 限制容器内执行的进程资源使用量。
        {
            "type": "RLIMIT_NOFILE",
            "hard": 1024,
            "soft": 1024
        }
    ]
}
```

 钩子 hook：

配置文件提供了钩子的特性，它可以让开发者扩展容器运行的动作， 在容器运行前后执行一些命令。

```json
"hooks": {
        "prestart": [ //容器创建后，用户没有开始前触发执行。
            		 // 在linux 上 它是在Namespace 创建成功后触发的，它能提供一个配置容器初始化环境的机会。
            {
                "path": "/usr/bin/fix-mounts",
                "args": ["fix-mounts", "arg1", "arg2"],
                "env":  [ "key1=value1"]
            },
            {
                "path": "/usr/bin/setup-network"
            }
        ],
        "poststart": [  // 在用户进程启动后执行，可以用来告诉用户进程以及启动。
            {
                "path": "/usr/bin/notify-start",
                "timeout": 5
            }
        ],
        "poststop": [  // 容器停止后执行，可以用来清理容器运行中的垃圾。
            {
                "path": "/usr/sbin/cleanup.sh",
                "args": ["cleanup.sh", "-f"]
            }
        ]
    }
```

path 是需要执行脚本的路径。 args 和 env 都是可选参数， timeout 是执行脚本的超时时间。



### Docker containerd

Containerd 可以作为 daemon 程序运行在Linux 和 Windows 上， 管理机器上所有容器的生命周期。

2016年3月，docker1.1的Docker 里就包含containerd, 2016年12月， Docker 宣布将containerd 从Docker 中分离，  和原来包含在Docker里的Containerd相比， 独立的containerd 具有更多功能，可以涵盖整个容器运行时管理的所有需求。



Containerd 并不是直接面向最终用户的，是集成到更上层的系统里， 比如 Swarm, kubernetes, Mesos等容器编排系统。对于容器编排系统来说，运行时只需要使用containerd + runC， 更加轻量。

它以daemon的形式运行在系统上，通过unix domain socket 暴露底层的gPRC API, 上层系统可以通过这些API管理机器上的所有容器。

每个Containerd 只负责一台机器， pull 镜像，对容器的操作（启动，停止等），网络，存储都是由containerd完成的。 容器具体运行由runc 负责。

 Containerd 项目架构图：

![](http://claymore.wang:5000/uploads/big/fc21fa931e83e04601eb6afa0092126a.png)



### runC

[RunC](https://github.com/opencontainers/runc) 是一个轻量级的工具，它是用来运行容器的，只用来做这一件事，并且这一件事要做好。我们可以认为它就是个命令行小工具，可以不用通过 docker 引擎，直接运行容器。事实上，runC 是标准化的产物，它根据 OCI 标准来创建和运行容器。
runC 由golang语言实现，基于libcontainer库。从docker1.11以后，docker架构图：

![](http://claymore.wang:5000/uploads/big/207b39b121d6ead032e84f38d70f82f8.png)



Containerd-shim:

Containerd-shim是一个真实运行的容器的真实垫片载体，每启动一个容器都会起一个新的docker-shim的一个进程， 
他直接通过指定的三个参数：容器id，boundle目录（containerd的对应某个容器生成的目录，一般位于：/var/run/docker/libcontainerd/containerID）， 
运行是二进制（默认为runc）来调用runc的api创建一个容器（比如创建容器：最后拼装的命令如下：runc create 。。。。。）





### Kubernetes CRI 容器引擎

#### CRI

Container Runtime Interface, 容器运行时接口， 是一组接口规范， 



### todo

https://segmentfault.com/a/1190000017543294#articleHeader2

https://segmentfault.com/a/1190000016366810

https://www.jianshu.com/p/62ede45cfb2e