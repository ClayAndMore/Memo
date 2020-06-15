
---
title: "06-linux启动过程.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
### LInux 系统启动过程分析

基于centos 6

```
按下电源——>
bois 自检
主引导记录 MBR lilo/grub
启动内核
初始化系统
```

#### BOIS 自检

1. 检测系统外围关键设备（如：CPU、内存、显卡、I/O、键盘鼠标等）是否正常。

   例如，最常见的是内存松动的情况，BIOS自检阶段会报错，系统就无法启动起来；

2. 之后执行一段小程序用来枚举本地设备并对其初始化。

   这一步主要是根据我们在BIOS中设置的系统启动顺序来搜索用于启动系统的驱动器，如硬盘、光盘、U盘和网络等。

   我们以硬盘启动为例，BIOS此时去读取硬盘驱动器的第一个扇区(MBR，512字节)，然后执行里面的代码。实际上这里BIOS并不关心启动设备第一个扇区中是什么内容，它只是负责读取该扇区内容（MBR）到内存、并执行。

至此，BIOS的任务就完成了，此后将系统启动的控制权移交到MBR部分的代码。



#### 主引导记录

MBR，主引导记录，它是Master Boot Record的缩写。硬盘的第一个扇区为主引导扇区，这个扇区的内容就是MBR。

它由三个部分组成，主引导程序(Bootloader)、 硬盘分区表DPT（Disk Partition table）和硬盘有效标志（55AA），其结构图如下所示：

```
+-+---+--------------+
  |   |              |
  |   |              |
  |   |              |
  v   |              |
      |              |
 446B |  BootLoader  |
  ^   |              |
  |   |              |
  |   |              |
  |   |              |
  |   |              |
+--------------------+
  |   |              |
  v   |              |
 64B  |Partition table
  ^   |              |
  |   |              |
+-+------------------+
 2B   |  Magic Number|
      |              |
+-----+--------------+
```

通常情况下，诸如lilo、grub这些常见的引导程序都直接安装在MBR中。我们以grub为例来分析这个引导过程。

grub引导也分为两个阶段stage1阶段和stage2阶段:

第一阶段把stage2的程序加载到内存。

第二阶段：当stage2被载入内存执行时，它首先会去解析grub的配置文件/boot/grub/grub.conf，**然后加载内核镜像到内存中**，并将控制权转交给内核。

ps:加载这些配置文件之前需要有文件系统的支持，**可是现在还没有文件系统呢**，GRUB内置文件系统访问支持，虽然是极度精简的，但已经具备根据路径读取相应文件的二进制流。换句话说，GRUB在不依赖Linux内核的情况下具有读取配置文件与内核映像的能力”。GRUB的内置文件系统其实是依靠stage1.5那些文件定义的，而且有不同文件系统的stage1.5。(1.5上方没说，可以理解为12的中间过程)

ps+: grub.conf:

```ini
default=0# 默认启动第一个系统内核，即后面的title部分，1代表第二个，依次类推，
timeout=5# 设置系统留给用户选择系统内核的时间为5s。
splashimage=(hd0,0)/grub/splash.xpm.gz
# 用户选择内核时候的背景图片文件，这里的hd0,0是第一个硬盘的第一个分区，没有/dev/sdaX的概念
hiddenmenu     # 是否显示选单画面
title CentOS 6 (2.6.32-696.el6.x86_64)    # 第一个选单的名字，可以自定义
    root (hd0,0)    # 内核文件放置的分区
    kernel ... ro root= ... rhgb quiet
    # 内核文件；读取内核文件之后要挂载/目录，只读，root后跟真正的/目录挂载的分区，rhgb表示系统启动时默认为图形界面
    # rhgb 表示默认图形显示，把启动过程覆盖掉
    # quit表示系统启动时将模块启动的详细信息屏蔽，只显示模块启动时候成功（ok or failed）
    initrd ...# 内核镜像文件
```





#### 启动内核

 Linux内核需要适应多种不同的硬件架构，但是将所有的硬件驱动编入内核又是不实际的，而且内核也不可能每新出一种硬件结构，就将该硬件的设备驱动写入内核。实际上Linux的内核镜像仅是包含了基本的硬件驱动，在系统安装过程中会检测系统硬件信息， 因此内核还要加载提供这些程序功能的模块，然而这些模块都在根目录的/lib/modules/2.6.32-696.el6.x86_64下（/和/lib/modules/不能挂载不同的分区），这时候内核还没有文件系统的概念，没有文件系统就没办法挂载根目录，想要挂载根目录就需要相应的模块支持，而我们原本的问题就是如何加载模块（先有鸡后有蛋的问题）。

根据安装信息和系统硬件信息将一部分设备驱动写入 initrd 。这样在以后启动系统时，一部分设备驱动就放在initrd中来加载

##### initrd

​       initrd 的英文含义是 bootloader initialized RAM disk，就是由 boot loader 初始化的内存盘。在 linu2.6内核启动前，boot loader 会将存储介质中的 initrd 文件加载到内存，内核启动时会在访问真正的根文件系统前先访问该内存中的 initrd 文件系统(initramfs)。

##### initramfs

initramfs 是在 kernel 2.5中引入的技术，实际上它的含义就是：在内核镜像中附加一个cpio包，这个cpio包中包含了一个小型的文件系统，当内核启动时，内核将这个 cpio包解开，并且将其中包含的文件系统释放到rootfs中，内核中的一部分初始化代码会放到这个文件系统中，作为用户层进程来执行。这样带来的明显的好处是精简了内核的初始化代码，而且使得内核的初始化过程更容易定制。

内核完成硬件检测和加载模块后，内核会呼叫第一个进程，就是/sbin/init，至此内核把控制权交给init进程。



#### 初始化系统-init进程

/sbin/init进程是系统其他所有进程的父进程，

当它接管了系统的控制权先之后，它首先会去读取/etc/inittab文件来执行相应的脚本进行系统初始化，可以看到第一行是这样的：

`id:2:initdefault:　　`

说明:

` id:runlevel:action:process `

| id       | 代表设定的项目，没有具体的实际意义                           |
| -------- | ------------------------------------------------------------ |
| runlevel | 执行级别，0-关机、1-单用户、2-没有NFS的多用户、3-真正的多用户、4-预留、5-Xwindows、6-reboot |
| action   | init的动作行为，initdefault表示要默认启动的runlevel          |
| process  | 执行动作的指令，一般为脚本文件                               |



##### /etc/rc.d/rc.sysinit

sysinit系统初始化脚本:

1. 设置主机名，挂载/etc/fstab中的文件系统，修改/etc/sysctl.conf 的内核参数等各项系统环境。
2. 定义主机名，如果不存在则将主机名定义为localhost；
3. 读取/etc/sysconfig/network文件，设置网络环境；
4. 挂载内存装置/proc和USB装置/sys，如果USB装置存在，则会加载usb模块并挂载usb文件系统；
5. 接下来是SELINUX的一些相关设置；
6. 设定text banner，显示欢迎界面；
7. ...
8. 将开机启动信息存放到/var/log/dmesg



##### /etc/rcN.d

上面完事之后，开始按运行级别来走。每个运行级别在/etc目录下面，都有一个对应的子目录，指定要加载的程序。

> ```
> /etc/rc0.d
> /etc/rc1.d
> /etc/rc2.d
> /etc/rc3.d
> /etc/rc4.d
> /etc/rc5.d
> /etc/rc6.d　　
> ```

上面目录名中的"rc"，表示run command（运行程序），最后的d表示directory（目录）。下面让我们看看 /etc/rc2.d 目录中到底指定了哪些程序。

> ```
> 　　$ ls  /etc/rc2.d
> 　　
> 　　README
> 　　S01motd
> 　　S13rpcbind
> 　　S14nfs-common
> 　　S16binfmt-support
> 　　S16rsyslog
> 　　S16sudo
> 　　S17apache2
> 　　S18acpid
> 　　...　　
> ```

可以看到，除了第一个文件README以外，其他文件名都是"字母S+两位数字+程序名"的形式。K开头表示该运行级别下需要把该服务杀死，S开头表示该运行级别下需要把该服务开启.

后面的两位数字表示处理顺序，数字越小越早处理，所以第一个启动的程序是motd，然后是rpcbing、nfs......数字相同时，则按照程序名的字母顺序启动，所以rsyslog会先于sudo启动。

这个目录里的所有文件（除了README），就是启动时要加载的程序。

##### /etc/init/init.d

七种预设的"运行级别"各自有一个目录，存放需要开机启动的程序。不难想到，如果多个"运行级别"需要启动同一个程序，那么这个程序的启动脚本，就会在每一个目录里都有一个拷贝。这样会造成管理上的困扰：如果要修改启动脚本，岂不是每个目录都要改一遍？

Linux的解决办法，就是七个 /etc/rcN.d 目录里列出的程序，都设为链接文件，指向另外一个目录 /etc/init.d ，真正的启动脚本都统一放在这个目录中。init进程逐一加载开机启动程序，其实就是运行这个目录里的启动脚本

> ```
> 　　$ ls -l /etc/rc2.d
> 　　
> 　　README
> 　　S01motd -> ../init.d/motd
> 　　S13rpcbind -> ../init.d/rpcbind
> 　　S14nfs-common -> ../init.d/nfs-common
> 　　S16binfmt-support -> ../init.d/binfmt-support
> 　　S16rsyslog -> ../init.d/rsyslog
> 　　S16sudo -> ../init.d/sudo
> 　　S17apache2 -> ../init.d/apache2
> 　　S18acpid -> ../init.d/acpid
> 　　...　　
> ```

这样做的另一个好处，就是如果你要手动关闭或重启某个进程，直接到目录 /etc/init.d 中寻找启动脚本即可。比如，我要重启Apache服务器，就运行下面的命令：

` /etc/init.d/apache2 restart`

/etc/init.d 这个目录名最后一个字母d，是directory的意思，表示这是一个目录，用来与程序 /etc/init 区分。



##### rc.local

上面每个rcN.d目录内最后都会有一个S99local文件 ，该文件指向 ../rc.local脚本。

这时候系统已经完成了各种必要系统服务的启动，假如我们想自定义一些指令要在开机的时候启动，我们就可以把他们放到/etc/rc.d/rc.local内，该文件默认为空。



##### 启动终端

接下来会由/sbin/mingetty指令启动终端，由于系统设置启动tty1-tty6 ，所以会启动6个命令行终端。mingetty就是启动终端的命令。

#### Login shell

分登录方式会有读取配置文件的区别：

命令行登录和 ssh：首先读入 /etc/profile，这是对所有用户都有效的配置；然后依次寻找下面三个文件，这是针对当前用户的配置。

> ```sh
> 　　~/.bash_profile #注意这个文件
> 　　~/.bash_login
> 　　~/.profile　　
> ```

需要注意的是，**这三个文件只要有一个存在，就不再读入后面的文件了。比如，要是 ~/.bash_profile 存在，就不会再读入后面两个文件了。**

图形界面登录：只加载 /etc/profile 和 ~/.profile。也就是说，~/.bash_profile 不管有没有，都不会运行。



##### no-login shell

大多情况我们会手动执行一个shell，如`bash`, 然后执行其`~/.bashrc`(我们对于bash的定制，都是写在这个文件里面的)

也许会问，要是不进入 non-login shell，岂不是.bashrc就不会运行了，因此bash 也就不能完成定制了?

请打开文件 ~/.profile，可以看到下面的代码：

 ```sh
 　　if [ -n "$BASH_VERSION" ]; then　　　　
 　　    if [ -f "$HOME/.bashrc" ]; then　　　　　　
 　　        . "$HOME/.bashrc"　　　　
 　　    fi　　
 　　fi　　
 ```

上面说过，只要运行～/.profile文件，～/.bashrc文件就会连带运行。但是上一节的第一种情况提到过，如果存在～/.bash_profile文件，那么有可能不会运行～/.profile文件

解决这个问题很简单，把下面代码写入.bash_profile就行了。

 ```sh
 　　if [ -f ~/.profile ]; then　　　　
 　　    . ~/.profile
 　　fi　　
 ```



其实centos7中默认已经没有profile：

```sh
[root@node201 ~]# cat .bash_profile 
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin
export PATH
```



##### mac

Mac OS X 使用的shell也是Bash。但是，它只加载.bash_profile，然后在.bash_profile里面调用.bashrc。而且，不管是ssh登录，还是在图形界面里启动shell窗口，都是如此。



Bash的设置之所以如此繁琐，是由于历史原因造成的。早期的时候，计算机运行速度很慢，载入配置文件需要很长时间，Bash的作者只好把配置文件分成了几个部分，阶段性载入。系统的通用设置放在 /etc/profile，用户个人的、需要被所有子进程继承的设置放在.profile，不需要被继承的设置放在.bashrc。



#### 引用

https://www.cnblogs.com/bluestorm/p/5981435.html

https://blog.51cto.com/2979193/2095375

https://mp.weixin.qq.com/s/cSpX-BqxsYN9OrpUtZyCBQ