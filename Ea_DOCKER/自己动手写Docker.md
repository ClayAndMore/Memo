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



### Linux Cgroups

上面说的是隔离，但是怎么限制每个每个隔离的空间大小，保证他们之间不会互相争抢呢。

Linu x Cgroups(Control Groups)  ， 可以方便的限制某个进程的资源占用，并且可以实时的监控进程和统计信息。

#### Cgroups 中的三个组件：

* cgroup 

  是进程分组管理的一种机制，一个cgroup包含一组**进程**，并且可以在其增加linux subsystem 的各种参数配置。

* subsystem 

  是对一组进程资源控制的模块，一般包含：

  * 对设置（如硬盘）的输入输出访问控制
  * cpu的调度策略，占用，尺寸
  * 进程挂起，恢复，网络流量， 优先级，监控

* hierarchy

  把一组cgroup变成一个树状的结构，可以让其拥有继承功能。

三个组件的关系：

 一个hierarchy 可以有很多subsystem, 一个subsystem只能附加到一个hierarchy上。

一个进程可以作为多个cgroup的成员，但是这些cgroup必须在不同的hierarchy上。

一个进程fork出子进程时，子进程是和父进程在同一个cgroup中的，也可以移动到其他cgroups。

 

####  kernel 接口

Kernel 怎样才能配置Cgroups?

1. 创建一个hierarchy(cgroup树)， 如下：

   ```
   mkdir cgroup-test # 创建一个hierarchy挂载点
   mount -t cgroup -o none,name=cgroup-test cgroup-test ./cgroup-test # 挂载一个hierarchy
   ls ./cgroup-test/
   cgroup.clone_children  cgroup.procs          notify_on_release  tasks
   cgroup.event_control   cgroup.sane_behavior  release_agent

   ```

   各个文件含义待补充

2. 创建子文件

   ```
   mkdir cgroup-1
   tree
   [root@q cgroup-test]# tree
   .
   |-- cgroup-1
   |   |-- cgroup.clone_children
   |   |-- cgroup.event_control
   |   |-- cgroup.procs
   |   |-- notify_on_release
   |   `-- tasks
   |-- cgroup.clone_children
   |-- cgroup.event_control
   |-- cgroup.procs
   |-- cgroup.sane_behavior
   |-- notify_on_release
   |-- release_agent
   `-- tasks
   ```

   在一个cgroup的目录下创建文件夹时， Kernel会把文件夹标记为这个cgroup的子crgroup, 并继承父的属性。

3. 添加和移动进程

4. 通过subsystem 限制cgroup中进程的资源。


####  Docker 如何使用Cgroups

```
cd /sys/fs/cgroup/memory/docker/<id> 
cat memory.limit_in_bytes  # 看cgroup的内存限制
cat memory.usage_in_bytes  # 查看cgroup中进程所使用的内存大小
```

可以看到， Docker通过为每个容器创建cgroup配置资源限制和资源控制。



#### Go实现对cgroup限制容器的资源





### Union File System

联合文件系统

 为linux 等系统设计的，把其他文件系统联合到一个联合挂载点的文件服务系统，简单说就是把不同物理位置的目录合并mount到同一个目录中。

AUFS完全重写了早期的UnionFS 1.x，其主要目的是为了可靠性和性能，并且引入了一些新的功能，比如可写分支的负载均衡。AUFS在使用上全兼容UnionFS，而且比之前的UnionFS在稳定性和性能上都要好很多

例子：

```
# 目录结构
$ tree
.
├── fruits
│   ├── apple
│   └── tomato
└── vegetables
    ├── carrots
    └── tomato

# 创建一个mount目录
$ mkdir mnt
 
# 把水果目录和蔬菜目录union mount到 ./mnt目录中
$ sudo mount -t aufs -o dirs=./fruits:./vegetables none ./mnt
 
#  查看./mnt目录
$ tree ./mnt
./mnt
├── apple
├── carrots
└── tomato
```

* 如果尝试修改mnt/apple的内容(`echo mmm > apple`)，  mnt目录和fruits目录的apple都会被修改。 因为上方的mount命令默认最左侧出现的第一个目录是可读可写的，后面出现的目录都是可读的。
* 如果尝试修改mun目录中的carrots, 会发现vegetables的carrots并没有变化，但fruit目录中多了修改修改后的carrots。
* 指定权限：`mount -t aufs -o dirs=./fruits=rw:./vegetables=rw none ./mnt`
  * rw表示可写可读read-write。
  * ro表示read-only，如果你不指权限，那么除了第一个外ro是默认值，对于ro分支，其永远不会收到写操作，也不会收到查找whiteout的操作。
  * rr表示real-read-only，与read-only不同的是，rr标记的是天生就是只读的分支，这样，AUFS可以提高性能，比如不再设置inotify来检查文件变动通知。

这时我们尝试改两个目录都有的文件 tomato:

```bash
$ echo "mnt_tomato" > ./mnt/tomato
 
$ cat ./fruits/tomato
mnt_tomato
 
$ cat ./vegetables/tomato
I am a vegetable
```

可见，如果有重复的文件名，在mount命令行上，越往前的就优先级越高。



#### 删除文件

权限中，我们看到了一个术语：whiteout，下面我来解释一下这个术语。

一般来说ro的分支都会有wh的属性，比如 “[dir]=ro+wh”。所谓whiteout的意思，如果在union中删除的某个文件，实际上是位于一个readonly的分支（目录）上，那么，在mount的union这个目录中你将看不到这个文件，但是read-only这个层上我们无法做任何的修改，所以，我们就需要对这个readonly目录里的文件作whiteout。AUFS的whiteout的实现是通过在上层的可写的目录下建立对应的whiteout隐藏文件来实现的。

看个例子：

假设我们有三个目录和文件如下所示（test是个空目录）：

```bash
# tree
.
├── fruits
│   ├── apple
│   └── tomato
├── test
└── vegetables
    ├── carrots
    └── tomato
```

我们如下mount：

```bash
# mkdir mnt
 
# mount -t aufs -o dirs=./test=rw:./fruits=ro:./vegetables=ro none ./mnt
 
# # ls ./mnt/
apple  carrots  tomato
```

现在我们在权限为rw的test目录下建个whiteout的隐藏文件.wh.apple，你就会发现./mnt/apple这个文件就消失了:

```bash
# touch ./test/.wh.apple
 
# ls ./mnt
carrots  tomato
```

上面这个操作和 rm ./mnt/apple是一样的。



#### 作用

这样的unionFS有什么用?

 历史上有一linux发行版，不需要硬盘去安装，直接把CD/DVD上的image运行在一个可写的存储设备上（比如一个U盘上），其实，也就是把CD/DVD这个文件系统和USB这个可写的系统给联合mount起来，这样你对CD/DVD上的image做的任何改动都会在被应用在U盘上，于是乎，你可以对CD/DVD上的内容进行任意的修改，因为改动都在U盘上，所以你改不坏原来的东西。

进阶：

把源代码作为一个只读的文件，和另一个你的working directory给union在一起，然后你就可以做各种修改而不用害怕会把源代码改坏了

Docker:

Docker用UnionFS搭建的分层镜像。

关于docker的分层镜像，除了aufs，docker还支持btrfs, devicemapper和vfs，你可以使用 -s 或 –storage-driver= 选项来指定相关的镜像存储。在Ubuntu 14.04下，docker默认Ubuntu的 aufs（在CentOS7下，用的是devicemapper)



#### 分支

从/sys/fs/aufs/si_[id]目录下查看aufs的mount的情况，下面是个示例：

```bash
#ls /sys/fs/aufs/si_b71b209f85ff8e75/
br0      br2      br4      br6      brid1    brid3    brid5    xi_path
br1      br3      br5      brid0    brid2    brid4    brid6 
 
# cat /sys/fs/aufs/si_b71b209f85ff8e75/*
/var/lib/docker/aufs/diff/87315f1367e5703f599168d1e17528a0500bd2e2df7d2fe2aaf9595f3697dbd7=rw
/var/lib/docker/aufs/diff/87315f1367e5703f599168d1e17528a0500bd2e2df7d2fe2aaf9595f3697dbd7-init=ro+wh
/var/lib/docker/aufs/diff/d0955f21bf24f5bfffd32d2d0bb669d0564701c271bc3dfc64cfc5adfdec2d07=ro+wh
/var/lib/docker/aufs/diff/9fec74352904baf5ab5237caa39a84b0af5c593dc7cc08839e2ba65193024507=ro+wh
/var/lib/docker/aufs/diff/a1a958a248181c9aa6413848cd67646e5afb9797f1a3da5995c7a636f050f537=ro+wh
/var/lib/docker/aufs/diff/f3c84ac3a0533f691c9fea4cc2ceaaf43baec22bf8d6a479e069f6d814be9b86=ro+wh
/var/lib/docker/aufs/diff/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158=ro+wh
64
65
66
67
68
69
70
/run/shm/aufs.xino
```

你会看到只有最顶上的层（branch）是rw权限，其它的都是ro+wh权限只读的。



#### Docker如何使用AUFS的

每个Docker image 由一系列read-only layer 组成.

 看某镜像用到了那些image layer：`docker history changed-ubuntu`

`/var/lib/docker/aufs/` 目录下有三个目录：

##### layer目录

可以看到所有image layer 的文件， id对应一个文件。

文件内容是该镜像ID的祖先镜像列表。



##### diff目录

该目录下是各个镜像ID的同名目录，里面是该镜像包含的真实文件和目录。

` cat /var/lib/docker/aufs/diff/eef7e551d5f8eaf2a7f1c54effef0f28a97978be3e79a2a7/tmp/newfile`

out: hello world!.

该镜像是基于上个镜像创建的，只多了上方文件，上方镜像只有12B， 这里我们会清楚一些aufs的工作方式。



##### mnt目录

运行中的容器映射在 /var/lib/docker/aufs/mnt/下，这就是AUFS给容器和它下层layer的一个mount point。如果容器没有运行了，依然还有这个目录，但却是个空目录，因为AUFS只在容器运行时才映射。除此之外，还有一个-init的目录，



##### container layer 和 AUFS

启动一个容器的时候，Docker会为其创建一个read-only 的 init layer，存储容器环境相关内容。

也会有一个read-write的layer来执行所有的写操作。

所以在容器启动的时候，上方三个目录都会多出两个layer。

额外，container的metadata和配置文件放在`/var/lib/docker/aufs/diff/` 