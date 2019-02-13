## 自己动手写Docker



我们经常听到docker是一个使用了Linux Namespace 和 Cgroups 的虚拟化工具。

LXC（Linux containers）

### Linux Namespace

* 一个Kernel 的功能
* 将资源隔离， 资源包括进程树， 网络接口，挂载点等。
* linux 一共 有六种不同类型的Namespace.


每种Namespace 都有自己的系统调用参数：

| Namespace 类型    | 系统调用参数          |
| ----------------- | --------------------- |
| UTS Namespace     | ClONE_NEWUTS          |
| IPC Namespace     | ClONE_NEWIPC          |
| PID Namespace     | ClONE_NEWClONE_NEWPID |
| User Namespace    | ClONE_NEWUSER         |
| Mount Namespace   | ClONE_NEWNS           |
| Network Namespace | ClONE_NEWNET          |



#### UTS Namespace

**UTS stands for UNIX Timesharing System**

主要隔离： nodename 和 domainname 两个系统标识。 Hostname和NIS域名(domain name)

在UTS Namespace 里， 每个Nampspace 允许有自己的hostname,



```go
package main

import (
	"os/exec"
    "syscall"
    "os"
    "log"
)

func main(){
    cmd := exec.Command("sh")
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS,
    }
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    
    if err := cmd.Run(); err != nil{
        log.Fatal(err)
    }
}
```

go run main.go , 可以进入到一个sh运行环境，用`pstree -pl`可以看一下进程，



####  IPC Namespace

InterProcess Communication (ipc)

用来隔离system V IPC 和 POSIX message queues.

在linux下的多个进程间的通信机制叫做IPC(Inter-Process Communication)，它是多个进程之间相互沟通的一种方法。在linux下有多种进程间通信的方法：半双工管道、命名管道、消息队列、信号、信号量、共享内存、内存映射文件，套接字等等。使用这些机制可以为linux下的网络服务器开发提供灵活而又坚固的框架。

上个代码中添加:

```python
cmd.SysProcAttr = $syscall.SysProcAttr{
    Cloneflages:syscall.CLONE_NEWUTS | syscall.CLONE_NEWIPC,
}
```

我们仅仅添加syscall.CLONE_NEWIPC。

验证：打开两个shell窗口一个运行：

`ipcs -q`  

一个在执行上方go文件前后都运行一遍。



#### PID Namespace

这个命名空间是用来隔离进程id的,每个被虚拟的空间，都有自己pid为1的init进程，这个init进程在父空间（也就是真实机器）中有对应的id.

上面代码基础上添加一个`| syscall.CLONE_NEWPID`

开两个shell窗口，一个运行pstree -pl 

一个运行go文件，echo $$, 会发现输出一。

这里还不能用ps和top命令看，因为他们用/proc，具体内容在下。



#### Mount Namespace

mount namespace 是linux 第一个实现的Namespace, 因此当时为它命名为NEWNS(new Namespace),当时人们也没有想到有这么多Namespace 会加入到linux大家庭。

类似，添加一行：`| syscall.ClONE_NEWNS`

运行看下/proc文件的内容，proc是一个文件系统，提供额外的机制，通过内核和内核模块来将信息发送给进程。

此时的/proc 还是主机的，我们将/proc mount到我们自己的mount namespace下来：

`mount -t proc proc /proc`

再看一下proc会发现少了很多文件。并且当且的sh的进程是1，说明已经隔离。docker volume也是利用了这个特性。





#### User Namespace

可以做到UID级别的隔离，也就是说，可以以UID为n的用户虚拟化出来一个Namespace,在这个Namespace里面，用户是有root权限的，但在真实的物理机上，他还是以为那个以UID为n的用户。

内核`linux kernel` 3.8 开始，非root进程也可以创建user namespace, 并且此用户在namespaces里可以被映射成root, 且在Namespace 里有root权限。

接着添加：

``` 
| syscall.CLONE_NEWUSER
}
cmd.SysProcAttr.Credential = &syscall.Credential{
    Uid: uint32(1),
    Gid: unit32(1),
}
```

验证：

命令：`id`

显示我们uid, gid,groups 都是0，root

运行刚才的go, 会发现id都变了。

这里可能有`/usr/bin/sh: invalid argument`的问题，`https://github.com/xianlubird/mydocker/issues/3`



#### Network Namespace



用来隔离网络设备，ip地址和等网络的namespace,让每个容器拥有自己独立的（虚拟的）网络设备，容器内的应用可以绑定到自己的端口，且不同容器的应用可以使用相同端口。

照例添加：`| syscall.CLONE_NEWNET`

运行ifconfig, 比较运行go文件的差异，会发现运行go后的ifconfig命令什么也没有。



