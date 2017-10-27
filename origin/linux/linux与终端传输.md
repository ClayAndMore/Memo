---
title: linux与终端传输
date: 2017-06-22 10:12:45
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



### ftp


