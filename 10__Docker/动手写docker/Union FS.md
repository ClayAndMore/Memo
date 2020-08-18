---
title: "Union FS.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["动手写Docker"]
categories: ["Docker"]
author: "Claymore"

---


## Union File System

联合文件系统

 为linux 等系统设计的，把其他文件系统联合到一个联合挂载点的文件服务系统，简单说就是把不同物理位置的目录合并mount到同一个目录中。形成一个新的虚拟系统。

当你在往新的虚拟系统写操作的时候， 会写到一个新文件，而不改变原来的文件，这是因为用到了Cow(coye on wirte) **写时复制**

写时复制也叫隐式共享， 思想是如果一个资源是重复的，没有任何修改，这个资源可以被新旧实例共享。

当对资源修改的时候， 才会创建一个新资源。

这种资源共享的方式，可以显著的减少未修改资源复制带来的消耗， 但是会在资源修改时增加小部分开销。



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

- 如果尝试修改mnt/apple的内容(`echo mmm > apple`)，  mnt目录和fruits目录的apple都会被修改。 因为上方的mount命令默认最左侧出现的第一个目录是可读可写的，后面出现的目录都是可读的。
- 如果尝试修改mun目录中的carrots, 会发现vegetables的carrots并没有变化，但fruit目录中多了修改修改后的carrots。
- 指定权限：`mount -t aufs -o dirs=./fruits=rw:./vegetables=rw none ./mnt`
  - rw表示可写可读read-write。
  - ro表示read-only，如果你不指权限，那么除了第一个外ro是默认值，对于ro分支，其永远不会收到写操作，也不会收到查找whiteout的操作。
  - rr表示real-read-only，与read-only不同的是，rr标记的是天生就是只读的分支，这样，AUFS可以提高性能，比如不再设置inotify来检查文件变动通知。

这时我们尝试改两个目录都有的文件 tomato:

```bash
$ echo "mnt_tomato" > ./mnt/tomato
 
$ cat ./fruits/tomato
mnt_tomato
 
$ cat ./vegetables/tomato
I am a vegetable
```

可见，如果有重复的文件名，在mount命令行上，越往前的就优先级越高。



### 删除文件

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



### 作用

这样的unionFS有什么用?

 历史上有一linux发行版，不需要硬盘去安装，直接把CD/DVD上的image运行在一个可写的存储设备上（比如一个U盘上），其实，也就是把CD/DVD这个文件系统和USB这个可写的系统给联合mount起来，这样你对CD/DVD上的image做的任何改动都会在被应用在U盘上，于是乎，你可以对CD/DVD上的内容进行任意的修改，因为改动都在U盘上，所以你改不坏原来的东西。

进阶：

把源代码作为一个只读的文件，和另一个你的working directory给union在一起，然后你就可以做各种修改而不用害怕会把源代码改坏了

Docker:

Docker用UnionFS搭建的分层镜像。

关于docker的分层镜像，除了aufs，docker还支持btrfs, devicemapper和vfs，你可以使用 -s 或 –storage-driver= 选项来指定相关的镜像存储。在Ubuntu 14.04下，docker默认Ubuntu的 aufs（在CentOS7下，用的是devicemapper)



### 分支

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



### Docker如何使用AUFS的

每个Docker image 由一系列read-only layer 组成.

 看某镜像用到了那些image layer：`docker history changed-ubuntu`

`/var/lib/docker/aufs/` 目录下有三个目录：

#### layer目录

可以看到所有image layer 的文件， id对应一个文件。

文件内容是该镜像ID的祖先镜像列表。

```
cat /var/lib/docker/aufs/layers/aaaa
a1
b1
c1
```



#### diff目录

该目录下是各个镜像ID的同名目录，里面是该镜像包含的真实文件和目录。

` cat /var/lib/docker/aufs/diff/eef7e551d5f8eaf2a7f1c54effef0f28a97978be3e79a2a7/tmp/newfile`

out: hello world!.

该镜像是基于上个镜像创建的，只多了上方文件，上方镜像只有12B， 这里我们会清楚一些aufs的工作方式。



#### mnt目录

运行中的容器映射在 /var/lib/docker/aufs/mnt/下，这就是AUFS给容器和它下层layer的一个mount point。如果容器没有运行了，依然还有这个目录，但却是个空目录，因为AUFS只在容器运行时才映射。除此之外，还有一个-init的目录，



#### container layer 和 AUFS

启动一个容器的时候，Docker会为其创建一个read-only 的 init layer，存储容器环境相关内容。

也会有一个read-write的layer来执行所有的写操作。

所以在容器启动的时候，上方三个目录都会多出两个layer。

额外，container的metadata和配置文件放在`/var/lib/docker/aufs/diff/` 



### 自己动手写AUFS

新建一个目录aufs, 在改目录下建立如下结构：

```shell
~/make_docker/aufs# tree
.
├── container-layer
│   └── container-layer.txt    
├── image-layer1
│   └── image-layer1.txt
├── image-layer2
│   └── image-layer2.txt
├── image-layer3
│   └── image-layer3.txt
├── image-layer4
│   └── image-layer4.txt
└── mnt

echo "I am container layer" > container-layer/container-layer.txt
echo "I am image layer 1" > image-layer1/image-layer1.txt
echo "I am image layer 2" > image-layer2/image-layer2.txt
echo "I am image layer 3" > image-layer3/image-layer3.txt
echo "I am image layer 4" > image-layer4/image-layer4.txt
```

挂载aufs系统：

`mount -t aufs -o dirs=./container-layer:./image-layer4:./image-layer3:./image-layer2:./image-layer1 none ./mnt`

默认的行为是，dirs 指定的左边起第一个目录是 read-write 权限， 后续的都是 read-only 权限。

```shell
root@ubuntu:~/make_docker/aufs# tree mnt
mnt
├── container-layer.txt
├── image-layer1.txt
├── image-layer2.txt
├── image-layer3.txt
└── image-layer4.txt
```

我们试着执行如下，看看aufs系统是如何对待文件变动的：

```shell
root@ubuntu:~/make_docker/aufs# echo "a new line " >> mnt/image-layer4.txt
root@ubuntu:~/make_docker/aufs# cat mnt/image-layer4.txt
I am image layer 4
a new line

root@ubuntu:~/make_docker/aufs# ls container-layer/
container-layer.txt  image-layer4.txt
root@ubuntu:~/make_docker/aufs# cat container-layer/image-layer4.txt
I am image layer 4
a new line
root@ubuntu:~/make_docker/aufs#
```

当我们向image-layer4.txt执行写操作的时候，系统会在mnt找到image-layer4.txt 拷贝到 read-write层的container-layer 目录，对其进行写操作。

