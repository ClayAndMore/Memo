
---
title: "安装runc.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "安装runc.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Docker]

### 依赖项

* Go  > version 1.6 

* libseccomp库

  ```bash
  yum install libseccomp-devel for CentOS
  apt-get install libseccomp-dev for Ubuntu
  # 尝试在ubuntu 14.04上安装， 因为libseccomp-dev < 2.2.0 后面make runc时失败
  # 换到了ubuntu 16
  ```

* `apt-get install pkg-config -y`




### 下载编译

```
# 在GOPATH/src目录创建'github.com/opencontainers'目录
> cd github.com/opencontainers
> git clone https://github.com/opencontainers/runc
> cd runc

> make
> sudo make install
```

或者使用`go get`安装

```
# 在GOPATH/src目录创建github.com目录
> go get github.com/opencontainers/runc
> cd $GOPATH/src/github.com/opencontainers/runc
> make
> sudo make install
```

以上步骤完成后，`runC`将安装在`/usr/local/sbin/runc`目录， 即使是你自定义的过gopath也会出现在上述目录。



unc支持可选的构建标记，用于编译各种功能的支持。要将构建标记添加到make选项，必须设置BUILDTAGS变量。

```
make BUILDTAGS='seccomp apparmor'
```

| Build Tag | Feature                            | Dependency |
| --------- | ---------------------------------- | ---------- |
| seccomp   | Syscall filtering                  | libseccomp |
| selinux   | selinux process and mount labeling | <none>     |
| apparmor  | apparmor profile support           | <none>     |
| ambient   | ambient capability support         | kernel 4.3 |

我一般都是直接make



### 创建一个OCI Bundle

`OCI Bundle`是指满足OCI标准的一系列文件，这些文件包含了运行容器所需要的所有数据，它们存放在一个共同的目录，该目录包含以下两项：

1. config.json：包含容器运行的配置数据
2. container 的 root filesystem

如果主机上安装了docker，那么可以使用`docker export`命令将已有镜像导出为`OCI Bundle`的格式



```
# create the top most bundle directory
> mkdir /mycontainer
> cd /mycontainer

# create the rootfs directory
> mkdir rootfs

# 获取busybox 镜像
> docker pull busybox
> docker run -d busybox top

# export busybox via Docker into the rootfs directory
> docker export -o busybox.tar $(docker busybox containID)  
> tar -C rootfs -xvf busybox.tar
> ls rootfs 
bin  dev  etc  home  proc  root  sys  tmp  usr  var
```

有了root filesystem，还需要config.json，`runc spec`可以生成一个基础模板，之后我们可以在模板基础上进行修改。

```
> runc spec
> ls
config.json rootfs
```

生成的config.json模板比较长，这里我将它**process**中的**arg** 和 **terminal**进行修改 

```shell
terminal : false,  #不进入终端

args: "sleep", "10"  # 运行容器命令，睡10s
```



### 运行容器

```shell
root@:~/mycontainer# runc create mycontainerid
root@:~/mycontainer# runc list
ID              PID         STATUS      BUNDLE              CREATED         OWNER
mycontainerid   562         created     /root/mycontainer   2019-03-12T..   root
root@:~/mycontainer# runc start mycontainerid
root@:~/mycontainer# runc list
ID              PID         STATUS      BUNDLE              CREATED         OWNER
mycontainerid   562         running     /root/mycontainer   2019-03-12T..   root
root@VM-0-6-ubuntu:~/mycontainer# runc list
ID              PID         STATUS      BUNDLE              CREATED         OWNER
mycontainerid   0           stopped     /root/mycontainer   2019-03-12T..   root

```



### runc 命令

开始一个新实例：

`runc run [ -b bundle ] <container-id>`

id 是本机唯一， 是你自己的命名， 指定-b 可以指定bundle 文件夹， 默认是目前文件夹。

eg: 建立运行并进入一个 容器：

```
terminal : true,  

args: "sh" 
```



help:

```bash
USAGE:
   runc [global options] command [command options] [arguments...]

VERSION:
   1.0.0-rc6+dev
commit: 2b18fe1d885ee5083ef9f0838fee39b62d653e30
spec: 1.0.1-dev

COMMANDS:
     checkpoint  checkpoint a running container
     create      create a container
     delete      delete any resources held by the container often used with detached container
     events      display container events such as OOM notifications, cpu, memory, and IO usage statistics
     exec        execute new process inside the container
     init        initialize the namespaces and launch the process (do not call it outside of runc)
     kill        kill sends the specified signal (default: SIGTERM) to the container's init process
     list        lists containers started by runc with the given root
     pause       pause suspends all processes inside the container
     ps          ps displays the processes running inside a container
     restore     restore a container from a previous checkpoint
     resume      resumes all processes that have been previously paused
     run         create and run a container
     spec        create a new specification file
     start       executes the user defined process in a created container
     state       output the state of a container
     update      update container resource constraints
     help, h     Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug             enable debug output for logging
   --log value         set the log file path where internal debug information is written (default: "/dev/null")
   --log-format value  set the format used by logs ('text' (default), or 'json') (default: "text")
   --root value        root directory for storage of container state (this should be located in tmpfs) (default: "/run/runc")
   --criu value        path to the criu binary used for checkpoint and restore (default: "criu")
   --systemd-cgroup    enable systemd cgroup support, expects cgroupsPath to be of form "slice:prefix:name" for e.g. "system.slice:runc:434234"
   --rootless value    ignore cgroup permission errors ('true', 'false', or 'auto') (default: "auto")
   --help, -h          show help
   --version, -v       print the versio
```



