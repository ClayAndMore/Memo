---
title: linux进阶
date: 2017-02-22 10:12:45
categories: linux
header-img:
tags: linux
---



### virtual box虚拟机连接网络的方式

1、NAT 网络地址转换模式(NAT,Network Address Translation) 
2、Bridged Adapter 桥接模式 
3、Internal 内部网络模式 
4、Host-only Adapter 主机模式 

#### 第一种 NAT模式 

解释： 
NAT模式是最简单的实现虚拟机上网的方式，你可以这样理解：Vhost访问网络的所有数据都是由主机提供的，vhost并不真实存在于网络中，主机与网络中的任何机器都不能查看和访问到Vhost的存在。 
虚拟机与主机关系： 
只能单向访问，虚拟机可以通过网络访问到主机，主机无法通过网络访问到虚拟机。 
虚拟机与网络中其他主机的关系： 
只能单向访问，虚拟机可以访问到网络中其他主机，其他主机不能通过网络访问到虚拟机。
虚拟机与虚拟机之间的关系： 
相互不能访问，虚拟机与虚拟机各自完全独立，相互间无法通过网络访问彼此。 
IP:10.0.2.15 
网关：10.0.2.2 
DNS：10.0.2.3 
一台虚拟机的多个网卡可以被设定使用 NAT， 第一个网卡连接了到专用网 10.0.2.0，第二个网卡连接到专用网络 10.0.3.0，等等。默认得到的客户端ip（IP Address）是10.0.2.15，网关（Gateway）是10.0.2.2，域名服务器（DNS）是10.0.2.3，可以手动参考这个进行修改。 
NAT方案优缺点： 
笔记本已插网线时： 虚拟机可以访问主机，虚拟机可以访问互联网，在做了端口映射后（最后有说明），主机可以访问虚拟机上的服务（如数据库）。 
笔记本没插网线时： 主机的“本地连接”有红叉的，虚拟机可以访问主机，虚拟机不可以访问互联网，在做了端口映射后，主机可以访问虚拟机上的服务（如数据库）。 

#### 第二种 Bridged Adapter模式 

解释： 
网桥模式是我最喜欢的用的一种模式，同时，模拟度也是相当完美。你可以这样理解，它是通过主机网卡，架设了一条桥，直接连入到网络中了。因此，它使得虚拟机能被分配到一个网络中独立的IP，所有网络功能完全和在网络中的真实机器一样。 
虚拟机与主机关系： 
可以相互访问，因为虚拟机在真实网络段中有独立IP，主机与虚拟机处于同一网络段中，彼此可以通过各自IP相互访问。 
虚拟机于网络中其他主机关系： 
可以相互访问，同样因为虚拟机在真实网络段中有独立IP，虚拟机与所有网络其他主机处于同一网络段中，彼此可以通过各自IP相互访问。 
虚拟机于虚拟机关系： 
可以相互访问，原因同上。 
IP：一般是DHCP分配的，与主机的“本地连接”的IP 是同一网段的。虚拟机就能与主机互相通信。 
笔记本已插网线时：（若网络中有DHCP服务器）主机与虚拟机会通过DHCP分别得到一个IP，这两个IP在同一网段。 主机与虚拟机可以ping通，虚拟机可以上互联网。 
笔记本没插网线时：主机与虚拟机不能通信。主机的“本地连接”有红叉，就不能手工指定IP。虚拟机也不能通过DHCP得到IP地址，手工指定IP后，也无法与主机通信，因为主机无IP。 
这时主机的VirtualBox Host-Only Network 网卡是有ip的，192.168.56.1。虚拟机就算手工指定了IP 192.168.56.*，也ping不能主机。 

#### 第三种 Internal模式 

解释： 
内网模式，顾名思义就是内部网络模式，虚拟机与外网完全断开，只实现虚拟机于虚拟机之间的内部网络模式。 
虚拟机与主机关系： 
不能相互访问，彼此不属于同一个网络，无法相互访问。 
虚拟机与网络中其他主机关系： 
不能相互访问，理由同上。 
虚拟机与虚拟机关系： 
可以相互访问，前提是在设置网络时，两台虚拟机设置同一网络名称。如上配置图中，名称为intnet。 
IP: VirtualBox的DHCP服务器会为它分配IP ，一般得到的是192.168.56.101，因为是从101起分的，也可手工指定192.168.56.*。 
笔记本已插网线时：虚拟机可以与主机的VirtualBox Host-Only Network 网卡通信 
这种方案不受主机本地连接（网卡）是否有红叉的影响。 

#### 第四种 Host-only Adapter模式 

解释： 
主机模式，这是一种比较复杂的模式，需要有比较扎实的网络基础知识才能玩转。可以说前面几种模式所实现的功能，在这种模式下，通过虚拟机及网卡的设置都可以被实现。 
我们可以理解为Vbox在主机中模拟出一张专供虚拟机使用的网卡，所有虚拟机都是连接到该网卡上的，我们可以通过设置这张网卡来实现上网及其他很多功能，比如（网卡共享、网卡桥接等）。 
虚拟机与主机关系 
默认不能相互访问，双方不属于同一IP段，host-only网卡默认IP段为192.168.56.X 子网掩码为255.255.255.0，后面的虚拟机被分配到的也都是这个网段。通过网卡共享、网卡桥接等，可以实现虚拟机于主机相互访问。 
虚拟机与网络主机关系 
默认不能相互访问，原因同上，通过设置，可以实现相互访问。 
虚拟机与虚拟机关系 
默认可以相互访问，都是同处于一个网段。 
虚拟机访问主机 用的是主机的VirtualBox Host-Only Network网卡的IP：192.168.56.1 ，不管主机“本地连接”有无红叉，永远通。 
主机访问虚拟机，用是的虚拟机的网卡3的IP： 192.168.56.101 ，不管主机“本地连接”有无红叉，永远通。 
虚拟机访问互联网，用的是自己的网卡2， 这时主机要能通过“本地连接”有线上网，（无线网卡不行） 

通过对以上几种网络模式的了解，我们就可以灵活运用，模拟组建出我们所想要的任何一种网络环境了。 
比如我想模拟出来一个一台主机，监控一个局域网上网情况的网络环境。 
首先我开启了两台虚拟机vhost1与vhost2，当然如果硬件允许，我同样可以再增加vhost3、vhost4… 
所有的vhost我都设置成internat内网模式，网络名称为intnal，网关为192.168.56.100，意思就是通过 192.168.56.100网卡上网。其中有一台vhost1我设置为双网卡，一张为内网模式（192.168.56.100），一张为网桥模式（192.168.1.101）。两张网卡设置双网卡共享上网 
虚拟机之间为局域网，其中有一台虚拟机vhost1通过与外网相连，所有局域网中的虚拟机又通过vhost1来实现上外网。这样vhost1就可以监控整个虚拟机局域网上网情况了。 

NAT 设置端口映射 
[http://huzhangsheng.blog.163.com/blog/static/34787784200802801435931/](https://www.douban.com/link2/?url=http%3A%2F%2Fhuzhangsheng.blog.163.com%2Fblog%2Fstatic%2F34787784200802801435931%2F) 
你可以设置一个虚拟机的服务（比如 WEB 服务），通过使用命令行工具 VboxManage 代理。你需要知道虚拟机的服务使用哪个端口，然后决定在主机上使用哪个端口（通常但不总是想要使虚拟机和主机使用同一个端口）。在主机上提供一个服务需要使用一个端口，你能使用在主机上没有准备用来提供服务的任何端口。一个怎样设置新的 NAT 例子，在虚拟机上连接到一个 ssh 服务器，需要下面的三个命令： 
VBoxManage setextradata 'Linux Guest' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/guestssh/Protocol' TCP 
VBoxManage setextradata 'Linux Guest' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/guestssh/GuestPort' 22 
VBoxManage setextradata 'Linux Guest' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/guestssh/HostPort' 2222 
说明：VboxManage 是一个命令行程序，请查询你的 VirtualBox 安装目录，'Linux Guest' 是虚拟主机名。guestssh 是一个自定义的名称，你可以任意设置，通过上面的三个命令，把虚拟机的 22 端口 转发到主机的 2222 端口。 
又比如，我在虚拟机 debian 上安装了 apache2 服务器，使用 80 端口，映射到主机的 80 端口。使用下面的命令。 
'C:\Program Files\innotek VirtualBox\VBoxManage.exe' setextradata 'debian' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/huzhangsheng/Protocol' TCP 
'C:\Program Files\innotek VirtualBox\VBoxManage.exe' setextradata 'debian' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/huzhangsheng/GuestPort' 80 
'C:\Program Files\innotek VirtualBox\VBoxManage.exe' setextradata 'debian' 'VBoxInternal/Devices/pcnet/0/LUN#0/Config/huzhangsheng/HostPort' 80 
注意：要使设置生效，请关掉 VirtualBox 再运行虚拟机，我把 VirtualBox 安装在 winxp 上，在虚拟机中安装 debian 4.02r ，虚拟机名是 debian ，并安装了 apache2 php5 mysql-server ，在主机上用IE浏览 http://localhost，成功转发到虚拟机 debian 的 apache2 web 服务器上 

上文出处：[http://www.cnblogs.com/coltiam/archive/2010/03/26/1696939.html](http://www.cnblogs.com/coltiam/archive/2010/03/26/1696939.html) 

个人感觉通过使用端口映射的方式很不爽，还不如直接桥接来的快，现在多数情况下连接到网络是没问题的，端口映射还需要在宿主跟虚拟机都额外开某个服务，感觉不爽。 

“网络”配置页面有4个方案： 

1：NAT 网络地址转换（Network Address Translation） 

2：Birdged Network 桥接 

3：Internal Network 内部网络（可以是虚拟机与虚拟机之间） 

4：Host-Only 只与主机通信（大概吧） 

安装完VirtualBox2.2后，主机多了一个“VirtualBox Host-Only Network ”本地网卡。 

--------------------------------------------------------------------

### xshell连接ubuntu虚拟机

* 在vm中网络连接设置成上面所说的第二种模式bridge
* 确保虚拟机上有网络，查看ip 命令：`ifconfig`注意是if不是ip,

![](http://ojynuthay.bkt.clouddn.com/ifconfig.png)

* 安装openssh-server

xshell连接不了ubuntu，原因没有安装openssh-server，解决方法： 

$:sudo apt-get install openssh-server 

查看server是否启动： 

$:ps -ef |grep ssh 

如果看到/usr/sbin/sshd -D，说明服务已经启动，否则服务尚未启动，那么需要启动server： 

$：/etc/init.d/ssh start 

####  传送文件

* 先下载rz和sz的工具包

`sudo apt install lrzsz`

* 从windows上传文件到linux

`rz`  回车后会提示上传的文件。

上传的文件会在当前linux的目录

* 从linux上传文件到windows

`sz`，后面跟要下载的文件名； 前提是要进入相关目录

回车后会提示保存的位置



### 磁盘管理

#### 查看磁盘容量-df

`$ df -h`

加上参数-h是以更易读的方式展示，以兆或者g来显示。

#### 查看目录容量 du

`$ du -h`

`$ du -h -d 0` 只看一级目录的信息

`$ du -h -d 1`只看二级目录的信息

#### 分区

`sudo fdisk l` 可看磁盘情况

`sudo fdisk sdb`对sdb进行分区，接下来会提示你按下m获得详细帮助

#### 格式化（创建文件系统）

在linux中把格式化叫创建文件系统

`sudo mkfs -t ext3 /dev/sdb1`

t指格式化的类型type为ext3,后面为指定分区

#### 挂载

没挂载的会显示黄色，代表块文件，需要挂载将其编成目录

`mount -t ext3 /dev/sdb1 /mnt/sdb`

将sdb1 挂载成mnt的sdb,

`mount sdb`常看sdb的挂载信息

#### 卸载 

`unmount mnt/sdb`

### 解压文件

#### 压缩格式

一些压缩格式：`*.zip`,`*.rar`,`*.7z`后缀的压缩文件（windows和linux)

Linux 上面常见常用的除了以上这三种外，

还有`*.gz`,`*.xz`,`*.bz2`,`*.tar`,`*.tar.gz`,`*.tar.xz`,`*tar.bz2`

tar是打包文件，就是将很多文件合成一个文件，并没有压缩

#### gzip

压缩gzip ,没有tar

`gzip hello.c` 压缩hello.c成hello.c.gz，hello.c会消失。

解压

`gzip -d hello.c.gz`   将hello.c.gz解压成hello.c，hello.c.gz会消失

参数：

-o:不提示的情况下覆盖文件；
-d:-d /home/sunny 指明将文件解压缩到/home/sunny目录下

#### tar 

tar是打包格式，一般tar后面会有tar.xz等。

压缩：`tar -czvf [desfile][sourcefile]`  

desfile 要带上压缩后缀，sourcefile 要全路径

解压：`tar -xzvf [sourcefile]`

命令详解：(这五个必须要用到其中一个，只能一个)

```
    -c: 建立压缩档案
　　-x：解压
　　-t：查看内容
　　-r：向压缩归档文件末尾追加文件
　　-u：更新原压缩包中的文件
```

后面可跟：

```
	-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
	-z: 用gzip来压缩/解压缩文件
	-v: 详细报告tar处理的文件信息。
	-z 支持gzip解压文件
	-j 支持bzip2解压文件
```





### 安装软件的方式

#### （1）下载源文件编译，安装：

思路：

1. 先到网站下载源代码，方式包括http,ftp,svn,git..
2. 解开压缩包
3. `./configure`意味着在当前目录下进行配置文件进行配置
4. `make`编译  ，编译源代码成二进制文件
5. `make install`

另：卸载`make uninstall`



#### （2）软件包（安装包）

将可执行文件打包，压缩，常见的格式：rpm(红帽系统下),deb

命名格式： 软件包名_版本号-修订版本__体系架构

#### （2）软件包的管理工具

dpkg(deb包常用的管理工具)

dpkg-deb

dpkg -i package 安装包

dpkg -r package 移除包

dpkg -P package 移除包和配置文件

dpkg -L package  列出安装包清单

dpkg --contents 包的具体文件

**dpkg的缺陷**

* 不能主动从镜像站点获取软件包
* 安装软件包的时候不能自动安装相关依赖包

#### (3)apt(常用在线只能管理工具集)

* apt-get 用于管理软件包，包括安装、卸载、升级

apt-get install package （搜索本地一个数据库，详情看软件源）

apt-get update   从软件镜像服务器上下载/更新用于本地软件源的软件包列表

apt-get upgrade 自动升级软件包到最新版本

apt-get check 检查当前apt管理里面的依赖包情况

apt-get -f install 修复依赖包关系

apt-get remove 卸载（但是卸载不干净，不包括软件包的配置文件）

apt-get remove --purge package (完全卸载)

apt-get --reinstall install package  重新安装



* apt-cache :用于查询软件包信息：

apt-cache show package 显示软件包信息

apt-cache policy package 显示软件包安装状态

apt-cache depends package 显示软件包依赖关系

apt-cache search package 在source某个名称的软件



#### 软件源

我们要定期从服务器下载一个软件包列表，使用

`sudo apt-get update`命令来保持本地的软件包列表是最新的。



一些问题：

apt source 镜像站点地址存在哪儿

/etc/apt/sources.list

apt的本地索引存在哪儿

/var/lib/apt/lists/*

apt的下载deb包存在哪里

/var/cache/apt/archives



### 卸载软件

查看所有安装的软件：`dpkg -l`

用上面的完全卸载，如果不想保留配置文件的话



### 比较合并

比较

`diff -y [file1][flie2]` 同行输出两个文件的不同

`diff -u [file1][flie2]`以补丁格式输出两个文件的不同

`diff -Nu [file1][file2]>[patchfile]`将不同输出到补丁文件

`patch -p[n]<[patchfile]` 打补丁文件，n一般为0，目录级联



### 环境变量

`$PATH`可看当前的环境变量

`export PATH = $PATH:/home/study`添加/home/study环境变量

`export hello=/home/study`

`cd hello`



所有用户的环境变量：/etc/profile文件
root用户的环境变量：~/.bashrc文件
非root用户的环境变量：/home/非root用户名/.bashrc文件



### 进程

#### 进程的分类

第一个角度来看，我们可以分为用户进程与系统进程

- 用户进程：通过执行用户程序、应用程序或称之为内核之外的系统程序而产生的进程，此类进程可以在用户的控制下运行或关闭。
- 系统进程：通过执行系统内核程序而产生的进程，比如可以执行内存资源分配和进程切换等相对底层的工作；而且，该进程的运行不受用户的干预，即使是root用户也不能干预系统进程的运行。

第二角度来看，我们可以将进程分为交互进程、批处理进程、守护进程

- 交互进程：由一个 shell 终端启动的进程，在执行过程中，需要与用户进行交互操作，可以运行于前台，也可以运行在后台。
- 批处理进程：该进程是一个进程集合，负责按顺序启动其他的进程。
- 守护进程：守护进程是一直运行的一种进程，经常在 Linux 系统启动时启动，在系统关闭时终止。它们独立于控制终端并且周期性的执行某种任务或等待处理某些发生的事件。例如httpd进程，一直处于运行状态，等待用户的访问。还有经常用的 cron（在 centOS 系列为 crond） 进程，这个进程为 crontab 的守护进程，可以周期性的执行用户设定的某些任务。



#### fork和exec()

**fork()** 是一个系统调用（system call），它的主要作用就是为当前的进程创建一个新的进程，这个新的进程就是它的子进程，这个子进程除了父进程的返回值和 PID 以外其他的都一模一样，如进程的执行代码段，内存信息，文件描述，寄存器状态等等

**exec()** 也是系统调用，作用是切换子进程中的执行程序也就是替换其从父进程复制过来的代码段与数据段

#### 僵尸进程和孤儿进程

子进程就是父进程通过系统调用 `fork()` 而产生的复制品，`fork()` 就是把父进程的 PCB 等进程的数据结构信息直接复制过来，只是修改了 PID，所以一模一样，指挥在执行 `exec()` 之后才会不同，

子进程代码执行部分其实已经结束执行了，系统的资源也基本归还给系统了，但是其进程的进程控制块（PCB）仍驻留在内存中，而它的 PCB 还在，代表这个进程还存在（因为 PCB 就是进程存在的唯一标志，里面有 PID 等消息），并没有消亡，这样的进程称之为僵尸进程（Zombie）。

**僵尸进程已经放弃了几乎所有的内存空间，没有任何执行代码，也不能被调度，在进程列表中保留一个位置，记载该进程的退出状态等信息供其父进程收集，从而释放它。但是 Linux 系统中能使用的 PID 是有限的，如果系统中存在有大量的僵尸进程，系统将会因为没有可用的 PID 从而导致不能产生新的进程。**

#### init 进程

进程 0 是系统引导时创建的一个特殊进程，也称之为内核初始化，其最后一个动作就是调用 `fork()` 创建出一个子进程运行 `/sbin/init` 可执行文件,而该进程就是 PID=1 的进程1，也就是 init 进程，而进程 0 就转为交换进程（也被称为空闲进程），而进程 1 （init 进程）是第一个普通用户态的进程,再由它不断调用 fork() 来创建系统里其他的进程，所以它是所有进程的父进程或者祖先进程。同时它是一个守护程序，直到计算机关机才会停止。

`init 0~7`:

0 - halt (Do NOT set initdefault to this)   //停机(不要把initdefault设置为零为0，因为这样会使[Linux](http://lib.csdn.net/base/linux)无法启动)
 1 - Single user mode                    //单用户模式，就像WinXP下的安全模式
 2 - Multiuser, without NFS (The same as 3, if you do not have networking)     //多用户，但没有NFS
 3 - Full multiuser mode                 //完全多用户模式，即命令行界面。图形界面完全关闭。如果窗口中有文件未保存，将丢失。用init 5 可以回到图形界面，但原来的进程已死。
 4 - unused          //一般不用，但在一些特殊情况下可以用他来做一些事情
 5 - X11                //选择此项，系统在登录时将进入图形化登录界面
 6 - reboot (Do NOT set initdefault to this)    //重新启动(不要把initdefault设置为6，因为这样会使Linux不断重新启动)



alt+ctrl+f1~f7可以切换多个命令界面。



#### 进程组和Session

每一个进程都会是一个进程组的成员，而且这个进程组是唯一存在的，他们是依靠 PGID（process group ID）来区别的，而每当一个进程被创建的时候，它便会成为其父进程所在组中的一员。

session:

Linux中的session跟web的session有点类似，也是在一个用户登录到主机，那么就建立了一个session，但是它的维系是基于连接的，那么该对于这个会话存在两种的维持方法

    1. 本地连接：就是说用户是在主机本机上进行的登录，直接通过键盘和屏幕和主机进行交互。
    2. 远程连接：用户通过互联网进行连接，比如基于ssh，连接都是经过加密的。


![](http://ojynuthay.bkt.clouddn.com/session.png)

session是一个或多个进程组的集合。

Session 主要是针对一个 tty 建立，Session 中的每个进程都称为一个工作(job)。每个会话可以连接一个终端(control terminal)。当控制终端有输入输出时，都传递给该会话的前台进程组。Session 意义在于将多个jobs囊括在一个终端，并取其中的一个 job 作为前台，来直接接收该终端的输入输出以及终端信号。 其他jobs在后台运行。

> **前台**（foreground）就是在终端中运行，与你能有交互的
>
> **后台**（background）就是在终端中运行，但是你并不能与其任何的交互，也不会显示其执行的过程

* &符号可以让我们的命令在后台中运行
* `ctrl+z`使我们的当前工作停止并丢到后台中去
* `jobs` 查看后台被停止的工作
* `fg [%jobnumber]`将后台工作拿到前台
* `bg [%jobnumber]`后台停止的工作再运作

#### kill

结束进程

```
#kill的使用格式如下
kill -signal %jobnumber

#signal从1-64个信号值可以选择，可以这样查看
kill －l
```

其中常用的有这些信号值

| 信号值  | 作用                  |
| ---- | ------------------- |
| -1   | 重新读取参数运行，类似与restart |
| -2   | 如同 ctrl+c 的操作退出     |
| -9   | 强制终止该任务             |
| -15  | 正常的方式终止该任务          |

若是在使用kill＋信号值然后直接加数字的话，这个数字代表的是 pid，你将会对 pid 对应的进程做操作

若是在使用kill+信号值然后％jobnumber，这时所操作的对象才是 job，这个数字就是就当前 bash 中后台的运行的 job 的 ID



#### 查看进程

top 动态实时查看进程的状态。

ps 静态查看当前的进程信息，打印当前进程快照

###### top

![](http://ojynuthay.bkt.clouddn.com/top.png)

我们看到 top 显示的第一排，

| 内容                           | 解释                    |
| ---------------------------- | --------------------- |
| top                          | 表示当前程序的名称             |
| 11:05:18                     | 表示当前的系统的时间            |
| up 8 days,17:12              | 表示该机器已经启动了多长时间        |
| 1 user                       | 表示当前系统中只有一个用户         |
| load average: 0.29,0.20,0.25 | 分别对应1、5、15分钟内cpu的平均负载 |

load average 也就是对当前 CPU 工作量的度量，具体来说也就是指运行队列的平均长度，也就是等待CPU的平均进程数相关的一个计算值。

假设我们的系统是单CPU单内核的，把它比喻成是一条单向的桥，把CPU任务比作汽车。

- load = 0 的时候意味着这个桥上并没有车，cpu 没有任何任务；
- load < 1 的时候意味着桥上的车并不多，一切都还是很流畅的，cpu 的任务并不多，资源还很充足；
- load = 1 的时候就意味着桥已经被车给沾满了，没有一点空隙，cpu 的已经在全力工作了，所有的资源都被用完了，当然还好，这还在能力范围之内，只是有点慢而已；
- load > 1 的时候就意味着不仅仅是桥上已经被车占满了，就连桥外都被占满了，cpu 已经在全力的工作了，系统资源的用完了，但是还是有大量的进程在请求，在等待。若是这个值大于２，大于３，超过 CPU 工作能力的 2，３。而若是这个值 > 5 说明系统已经在超负荷运作了。

这是单个 CPU 单核的情况，而实际生活中我们需要将得到的这个值除以我们的核数来看。我们可以通过一下的命令来查看 CPU 的个数与核心数

```
#查看物理CPU的个数
#cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l

#每个cpu的核心数
cat /proc/cpuinfo |grep "physical id"|grep "0"|wc -l
```

来看 top 的第二行数据，基本上第二行是进程的一个情况统计

| 内容              | 解释         |
| --------------- | ---------- |
| Tasks: 26 total | 进程总数       |
| 1 running       | 1个正在运行的进程数 |
| 25 sleeping     | 25个睡眠的进程数  |
| 0 stopped       | 没有停止的进程数   |
| 0 zombie        | 没有僵尸进程数    |

来看 top 的第三行数据，这一行基本上是 CPU 的一个使用情况的统计了

| 内容             | 解释                                       |
| -------------- | ---------------------------------------- |
| Cpu(s): 1.0%us | 用户空间占用CPU百分比                             |
| 1.0% sy        | 内核空间占用CPU百分比                             |
| 0.0%ni         | 用户进程空间内改变过优先级的进程占用CPU百分比                 |
| 97.9%id        | 空闲CPU百分比                                 |
| 0.0%wa         | 等待输入输出的CPU时间百分比                          |
| 0.1%hi         | 硬中断(Hardware IRQ)占用CPU的百分比               |
| 0.0%si         | 软中断(Software IRQ)占用CPU的百分比               |
| 0.0%st         | (Steal time) 是当 hypervisor 服务另一个虚拟处理器的时候，虚拟 CPU 等待实际 CPU 的时间的百分比 |

CPU 利用率，是对一个时间段内 CPU 使用状况的统计，通过这个指标可以看出在某一个时间段内 CPU 被占用的情况，Load Average 是 CPU 的 Load，它所包含的信息不是 CPU 的使用率状况，而是在一段时间内 CPU 正在处理以及等待 CPU 处理的进程数情况统计信息，这两个指标并不一样。

来看 top 的第四行数据，这一行基本上是内存的一个使用情况的统计了

| 内容             | 解释         |
| -------------- | ---------- |
| 8176740 total  | 物理内存总量     |
| 8032104 used   | 使用的物理内存总量  |
| 144636 free    | 空闲内存总量     |
| 313088 buffers | 用作内核缓存的内存量 |

> **注意**
>
> 系统的中可用的物理内存最大值并不是 free 这个单一的值，而是 free + buffers + swap 中的 cached 的和

来看 top 的第五行数据，这一行基本上是交换区的一个使用情况的统计了

| 内容     | 解释                                       |
| ------ | ---------------------------------------- |
| total  | 交换区总量                                    |
| used   | 使用的交换区总量                                 |
| free   | 空闲交换区总量                                  |
| cached | 缓冲的交换区总量,内存中的内容被换出到交换区，而后又被换入到内存，但使用过的交换区尚未被覆盖 |

在下面就是进程的一个情况了

| 列名      | 解释                                   |
| ------- | ------------------------------------ |
| PID     | 进程id                                 |
| USER    | 该进程的所属用户                             |
| PR      | 该进程执行的优先级priority 值                  |
| NI      | 该进程的 nice 值                          |
| VIRT    | 该进程任务所使用的虚拟内存的总数                     |
| RES     | 该进程所使用的物理内存数，也称之为驻留内存数               |
| SHR     | 该进程共享内存的大小                           |
| S       | 该进程进程的状态: S=sleep R=running Z=zombie |
| %CPU    | 该进程CPU的利用率                           |
| %MEM    | 该进程内存的利用率                            |
| TIME+   | 该进程活跃的总时间                            |
| COMMAND | 该进程运行的名字                             |

> **注意**
>
> **NICE 值**叫做静态优先级，是用户空间的一个优先级值，其取值范围是-20至19。这个值越小，表示进程”优先级”越高，而值越大“优先级”越低。nice值中的 -20 到 19，中 -20 优先级最高， 0 是默认的值，而 19 优先级最低
>
> **PR 值**表示 Priority 值叫动态优先级，是进程在内核中实际的优先级值，进程优先级的取值范围是通过一个宏定义的，这个宏的名称是MAX_PRIO，它的值为140。Linux实际上实现了140个优先级范围，取值范围是从0-139，这个值越小，优先级越高。而这其中的 0 - 99 是实时的值，而 100 - 139 是给用户的。
>
> 其中 PR 中的 100 to 139 值部分有这么一个对应 PR = 20 + (-20 to +19)，这里的 -20 to +19 便是nice值，所以说两个虽然都是优先级，而且有千丝万缕的关系，但是他们的值，他们的作用范围并不相同
>
> **VIRT **任务所使用的虚拟内存的总数，其中包含所有的代码，数据，共享库和被换出 swap空间的页面等所占据空间的总数

在上文我们曾经说过 top 是一个前台程序，所以是一个可以交互的

| 常用交互命令 | 解释                                       |
| ------ | ---------------------------------------- |
| q      | 退出程序                                     |
| I      | 切换显示平均负载和启动时间的信息                         |
| P      | 根据CPU使用百分比大小进行排序                         |
| M      | 根据驻留内存大小进行排序                             |
| i      | 忽略闲置和僵死的进程，这是一个开关式命令                     |
| k      | 终止一个进程，系统提示输入 PID 及发送的信号值。一般终止进程用15信号，不能正常结束则使用9信号。安全模式下该命令被屏蔽。 |

###### ps

* `ps aux`罗列出所有的进程信息
* `ps aux | grep zsh`查找某个进程
* `ps －afxo user,ppid,pid,pgid,command`自定义显示参数
* `pstree`可以很直接的看到相同的进程数量，最主要的还是我们可以看到所有进程的之间的相关性。

### 网络

* netstat 当前网络状态
* ping 
* ifconfig
* ssh
* ftp
* telnet


#### 查看端口

查看80端口的占用情况：

lsof -i:80  

或者：

netstat -apn | grep 80

上面的命令执行之后可以显示进程号，找到进程号以后，再使用以下命令查看详细信息：

ps -aux | grep <进程号>


### 遇到的问题

* tab自动补全失灵

编辑etc/bash bashrc文件（管理员权限），找到以下几行：

```
# enable bash completion in interactive shells
# if{-f etc/bash_conmpletion} $$ ! shopt -oq posix:then
# ./etc/bash_completion
# fi
```

取消注释即可

**bashrc文件讲讲rc的含义**：run command ,一般rc后缀文件就是启动脚本文件