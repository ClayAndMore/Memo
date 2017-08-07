---
title: linux基本操作
date: 2017-02-15 09:54:15
categories: linux
header-img:
tags: linux
---

### linux启动流程

通电一个默认的物理地址->bios->找到磁盘第一个扇区->引导程序->内核->挂载文件系统->系统服务->应用程序



### linux桌面环境

本身是没有桌面环境的，桌面只是运行在系统之上的一款软件，这套软件以前是XFree86，现在则是 xorg（X.Org），而这套软件又是通过 X 窗口系统（X Window System，也常被称为X11或X）实现的，X 本身只是工具包及架构协议，而 xorg 便是 X 架构规范的一个实现体，也就是说它是实现了 X 协议规范的一个提供图形用户界面服务的服务器，就像实现了 http 协议提供 web 服务的 Apache。如果只有服务器也是不能实现一个完整的桌面环境的，当然还需要一个客户端，我们称为 X Client，像如下几个大家熟知也最流行的实现了客户端功能的桌面环境**KDE**，**GNOME**，**XFCE**，**LXDE**

### shell

Shell 是指“提供给使用者使用界面”的软件（命令解析器），类似于 DOS 下的 command（命令行）和后来的 cmd.exe。普通意义上的 Shell 就是可以接受用户输入命令的程序。它之所以被称作 Shell 是因为它隐藏了操作系统底层的细节。同样的 Unix/Linux 下的图形用户界面 GNOME 和 KDE，有时也被叫做“虚拟 shell”或“图形 shell”。

在 UNIX/Linux 中比较流行的常见的 Shell 有 bash，zsh，ksh，csh 等等，Ubuntu 终端默认使用的是 bash，



### 文件系统

文件系统是一种存储和组织计算机文件和资料的方法，linux中一切皆文件，无扩展名。

文件格式，正如window系统的FAT32,NTFS格式。

linux有EXT3（主文件系统）和SWAP（交换文件系统）

文件系统数据结构:引导块，超级块（定义数据单元大小）,

data(文件数据)，inode (索引)



ext3基于日志记录的文件系统，所有操作会记录日志，所以重新开机会发现关机前的东西还在。同mac

swap概念同window的虚拟内存，在物理内存不够用时可用虚拟内存。



### SSH

SSH 为 [Secure Shell](http://baike.baidu.com/view/2118359.htm) 的缩写，由 IETF 的网络小组（Network Working Group）所制定；SSH 为建立在应用层基础上的安全协议。SSH 是目前较可靠，专为[远程登录](http://baike.baidu.com/view/59099.htm)会话和其他网络服务提供安全性的协议。利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题。SSH最初是UNIX系统上的一个程序，后来又迅速扩展到其他操作平台。SSH在正确使用时可弥补网络中的漏洞。SSH客户端适用于多种平台。几乎所有UNIX平台—包括[HP-UX](http://baike.baidu.com/view/58963.htm)、[Linux](http://baike.baidu.com/view/1634.htm)、[AIX](http://baike.baidu.com/view/349664.htm)、[Solaris](http://baike.baidu.com/subview/329359/5113665.htm)、[Digital](http://baike.baidu.com/view/428214.htm) [UNIX](http://baike.baidu.com/view/8095.htm)、[Irix](http://baike.baidu.com/view/3373083.htm)，以及其他平台，都可运行SSH。

### yum和apt-get用法及区别

RedHat 系列 

1 常见的安装包格式 rpm包,安装rpm包的命令是“rpm -参数” 

2 包管理工具  yum 

3 支持tar包 

 

Debian系列

1 常见的安装包格式 deb包,安装deb包的命令是“dpkg -参数”

2 包管理工具 apt-get

3 支持tar包

 

wget:
一个下载工具，和操作系统无关。

基本的语法是：`wget [参数列表] URL。`

1 支持断点下传功能
2 同时支持FTP和HTTP下载方式
3 支持代理服务器
4 设置方便简单
5 程序小，完全免费



tar 只是一种压缩文件格式，所以，它只是把文件压缩打包而已。

rpm 相当于[windows](http://www.2cto.com/special/xtxz/)中的安装文件，它会自动处理软件包之间的依赖关系。

 

优缺点来说，rpm一般都是预先编译好的文件，它可能已经绑定到某种CPU或者发行版上面了。

tar一般包括编译脚本，你可以在你的环境下编译，所以具有通用性。

 

如果你的包不想开放源代码，你可以制作成rpm，如果开源，用tar更方便了。

 

tar一般都是[源码](http://www.2cto.com/ym)打包的软件，需要自己解包，然后进行安装三部曲，./configure, make, make install.　来安装软件。

 

rpm是redhat公司的一种软件包管理机制，直接通过rpm命令进行安装删除等操作，最大的优点是自己内部自动处理了各种软件包可能的依赖关系。

| 説明            | [Redhat](http://d.hatena.ne.jp/keyword/Redhat)系 | [Debian](http://d.hatena.ne.jp/keyword/Debian)系 |
| ------------- | ---------------------------------------- | ---------------------------------------- |
| 更新缓存          | yum makecache                            | [apt](http://d.hatena.ne.jp/keyword/apt)-get update |
| 更新包           | [yum](http://d.hatena.ne.jp/keyword/yum) update | [apt](http://d.hatena.ne.jp/keyword/apt)-get upgrade |
| 检索包           | [yum](http://d.hatena.ne.jp/keyword/yum) search | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) search |
| 检索包内文件        | [yum](http://d.hatena.ne.jp/keyword/yum) provides | [apt](http://d.hatena.ne.jp/keyword/apt)-file search |
| 安装指定的包        | [yum](http://d.hatena.ne.jp/keyword/yum) install | [apt](http://d.hatena.ne.jp/keyword/apt)-get install |
| 删除指定的包        | [yum](http://d.hatena.ne.jp/keyword/yum) remove | [apt](http://d.hatena.ne.jp/keyword/apt)-get remove |
| 显示指定包的信息      | [yum](http://d.hatena.ne.jp/keyword/yum) info | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 显示包所在组的一览     | [yum](http://d.hatena.ne.jp/keyword/yum) grouplist | -                                        |
| 显示指定包所在组的信息   | [yum](http://d.hatena.ne.jp/keyword/yum) groupinfo | -                                        |
| 安装指定的包组       | [yum](http://d.hatena.ne.jp/keyword/yum) groupinstall | -                                        |
| 删除指定的包组       | [yum](http://d.hatena.ne.jp/keyword/yum) groupremove | -                                        |
| 参考库的设定文件      | /etc/[yum](http://d.hatena.ne.jp/keyword/yum).repos.d/* | /etc/[apt](http://d.hatena.ne.jp/keyword/apt)/sources.list |
| 安装完的包的列表      | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qa | dpkg-query -l                            |
| 显示安装完的指定包的信息  | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qi | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 安装完的指定包内的文件列表 | [rpm](http://d.hatena.ne.jp/keyword/rpm) -ql | dpkg-query -L                            |
| 安装完的包的信赖包的列表  | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[qR](http://d.hatena.ne.jp/keyword/qR) | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) depends |
| 安装完的文件信赖的包    | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[q](http://d.hatena.ne.jp/keyword/qR)f | dpkg -S                                  |



### 关机

先将内存中的数据同步到银盘：`sync`

关机和重启：h =halt 

```
Shutdown –h now 立马关机
Shutdown –h 20:25 系统会在今天20:25关机
Shutdown –h +10 十分钟后关机
Shutdown –r now 系统立马重启
Shutdown –r +10 系统十分钟后重启
```



### 用户切换

#### 用户符号

`$`表示没有root权限的用户

`#`表示有root权限的用户

`~`表示在home目录下

#### su,su-与sudo

`su `可以切换到用户user，执行时需要输入目标用户的密码，

`sudo `可以以特权级别运行cmd命令，需要当前用户属于sudo组，且需要输入当前用户密码。

`su - `命令也是切换用户，同时环境变量也会跟着改变成目标用户的环境变量。只打su - 会切换到root用户

#### 当前用户更改root密码

`sudo passwd root`

### 用户和用户组

我们一般登录系统时都是以普通账户的身份登录的，要创建用户需要 root 权限，这里就要用到 `sudo` 这个命令了。不过使用这个命令有两个大前提，一是你要知道当前登录用户的密码，二是当前用户必须在 `sudo` 用户组。

添加一个叫test的用户：

`sudo adduser test`

接下来会让你输入原本的用户密码，和新用户的密码和确认密码，还有一些设置，可按回车设置默认。

`useradd -g name tim`讲用户tim添加到name组,一般添加到root用户组。

删除用户(删除所有目录）：

`sudo deluser claymore --remove-home`



#### 用户组(groups命令)

用户组说明这里的用户有同样的权限。

创建用户组：

`groupadd name`  name 为组名

`groupadd -g 200 name`  创建组号为200的name组

删除组：

`groupdel name` 删除name组，不能删除不为空的组

每一个用户都有一个用户组，查看用户的组：

`groups claymore `

out:`claymore:claymore`

前面的为用户名，后面的为用户组，一般创建一个用户会默认创建一个同名的用户组。

/etc/group 的内容包括用户组（Group）、用户组口令、GID 及该用户组所包含的用户（User），每个用户组一条记录。格式如下：

> group_name:password:GID:user_list

你看到上面的 password 字段为一个 'x' 并不是说密码就是它，只是表示密码不可见而已。



### 目录结构

以往的 Windows 一直是以存储介质为主的，主要以盘符（C 盘，D 盘...）及分区的来实现文件管理，然后之下才是目录，目录就显得不是那么重要，除系统文件之外的用户文件放在任何地方任何目录也是没有多大关系。所以通常 Windows 在使用一段时间后，磁盘上面的文件目录会显得杂乱无章（少数善于整理的用户除外吧）。然而 UNIX/Linux 恰好相反，UNIX 是以目录为主的，Linux 也继承了这一优良特性。 Linux 是以树形目录结构的形式来构建整个系统的，可以理解为一个用户可操作系统的骨架。虽然本质上无论是目录结构还是操作系统内核都是存储在磁盘上的，但从逻辑上来说 Linux 的磁盘是“挂在”（挂载在）目录上的，每一个目录不仅能使用本地磁盘分区的文件系统，也可以使用网络上的文件系统。举例来说，可以利用网络文件系统（Network File System，NFS）服务器载入某特定目录等。

![](http://ojynuthay.bkt.clouddn.com/linux%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84.png)

/bin: 存放系统可执行文件

/sbin: super bin 存放管理员可用的执行文件

/etc: 系统配置文件

/lib: 共享的类库

/dev: 外设，设备

/tmp: 临时文件

/boot:  启动文件

/root: root用户目录

/home :  相当与win的users ，比如你的用户a,会有home/a

/mnt: 设备挂载

/opt: 优化目录，临时装一下的东西

/usr: 用户程序目录，

--/bin

--/sbin 

/var: 系统变量

/proc: 虚拟文件系统，vfs

/lost and found 找回文件



### 目录颜色

![](http://ojynuthay.bkt.clouddn.com/linuxColor.png)



### 目录和文件操作

#### 新建目录（mkdir）

`mkdir mydir`  创建一个名为mydir的空目录

`mkdir -p father/son/grandson`  -p创建一个多级目录

#### 新建文件（touch)

`touch test`创建一个空白文件test

#### 复制(cp)

复制文件：

`cp test father/son/grandson`

复制目录：

`cp -r father dirFolder` 要带参数-r才能将father及整个子目录复制到dirFolder

#### 删除（rm)

`rm test` 可删除文件，若有保护的文件 可加参数-f强制删除

删除目录一定要加上-r

`rm -r father`

#### 移动/重命名（mv)

`mv 源目录文件 目的目录`

`mv 旧的文件名 新的文件名`

#### 查看文件

* 使用cat,tac和nl查看文件

cat为正序显示，tac倒序显示

nl 添加行号并打印

* more 和 less命令分页查看，他俩功能基本一致 ，用man命令看细节

`more test`

* 用head和tail命令查看文件，一个只看头10行（默认）,一个只看尾10行
* 使用file查看文件类型




### 软链接和硬链接

软连接，也叫符号链接（Symbolic Link），可以理解为window上的快捷方式

`sudo ln -s 源文件 目标文件`

**ln -s a b **中的 a 就是源文件，b是链接文件名,其作用是当进入b目录，实际上是链接进入了a目录。 这时的b 是不存在的。

删除软链接：

`rm -rf  b`  注意不是`rm -rf  b/`



硬连接，源文件名和链接文件名都指向相同的物理地址，目录不能够有硬连接，文件在磁盘中只有一个复制，可以节省硬盘空间，由于删除文件要在同一个索引节点属于唯一的连接时才能成功，因此可以防止不必要的误删。

**ln  a b **是建立硬链接

正常删除

​	


### 文件权限

#### 查看文件权限

`ls -l`使用较长文件格式列出文件

会看到一些排列

解释：![](http://ojynuthay.bkt.clouddn.com/%E6%96%87%E4%BB%B6%E6%9D%83%E9%99%90.png)

![](http://ojynuthay.bkt.clouddn.com/%E6%96%87%E4%BB%B6%E6%9D%83%E9%99%902.png)

* linux的文件类型：

`·`一般文件

d 目录文件

l 链接文件（link)，如windows下的快捷方式

b 块设备（block），以块为单位存储的文件

c 字符设备 ，charactor,串口通信时用

s 网络通信设备，socket

p 管道，把一个文件的出口写入一个文件的入口

* 权限设定

r  read 设置为1

w write 设置为2

x 设置为4  ，x 对于文件夹来说是可进入，对于文件来说是可执行。

这样可以简化文件的写法，如7（1+2+4）代表就有rwx的权限



#### 修改文件权限

`chmod [who][+-=][mode] 文件名`

eg:  `chmod u+x myflie`

who 为参数，可选：

u (用户user) 文件或目录的所有者

g (组 group)  同组用户具有的权限

o (其他用户 other) 

a （所有用户，系统默认值）



操作参数：

`+` 添加某个权限

`-`减少某个权限 

`=` 赋予给定权限，并取消其他权限如果有的话。



mode 参数：

​	r 可读。

　　w 可写。

　　x 可执行。

　　X 只有目标文件对某些用户是可执行的或该目标文件是目录时才追加x 属性。

　　s 在文件执行时把进程的属主或组ID置为该文件的文件属主。方式“u＋s”设置文件的用户ID位，“g＋s”设置组ID位。

　　t 保存程序的文本到交换设备上。

　　u 与文件属主拥有一样的权限。

　　g 与和文件属主同组的用户拥有一样的权限。

　　o 与其他用户拥有一样的权限。



文件名：以空格分开的要改变权限的文件列表，支持通配符。



数字修改： `chmod  664 myfile`    数字对应的权限范围是： u,g,o



### 一些技巧

#### Tap补全命令

可补全命令或者文件路径，如果你忘了一些命令时，也可按下tap来看剩下可填的命令

#### history

看曾输入的历史命令



#### 通配符*

可以匹配你想要的可变名称，比如看所有的.txt文件

`ls *.txt`

shell常用通配符

| 字符                      | 含义                              |
| ----------------------- | ------------------------------- |
| `*`                     | 匹配 0 或多个字符                      |
| `?`                     | 匹配任意一个字符                        |
| `[list]`                | 匹配 list 中的任意单一字符                |
| `[!list]`               | 匹配 除list 中的任意单一字符以外的字符          |
| `[c1-c2]`               | 匹配 c1-c2 中的任意单一字符 如：[0-9] [a-z] |
| `{string1,string2,...}` | 匹配 sring1 或 string2 (或更多)其一字符串  |
| `{c1..c2}`              | 匹配 c1-c2 中全部字符 如{1..10}         |

#### man命令

是Manual page的缩写，可以获得某个命令的说明和使用方式的详细介绍

`man <command_name>`

看man命令本身的介绍

`man man`

man 手册的内容很多，涉及了 Linux 使用过程中的方方面面，为了便于查找，是做了分册（分区段）处理的，在Research UNIX、BSD、OS X 和 Linux 中，手册通常被分为8个区段，安排如下：

| 区段   | 说明                     |
| ---- | ---------------------- |
| 1    | 一般命令                   |
| 2    | 系统调用                   |
| 3    | 库函数，涵盖了C标准函数库          |
| 4    | 特殊文件（通常是/dev中的设备）和驱动程序 |
| 5    | 文件格式和约定                |
| 6    | 游戏和屏保                  |
| 7    | 杂项                     |
| 8    | 系统管理命令和守护进程            |

要查看相应区段的内容，就在 man 后面加上相应区段的数字即可，如：

`man 1 ls`

会显示第一区段中的`ls`命令man页面。

使用后，说明会按照下面几个方面来说明：

* NAME（名称）
* SYNOPSIS（摘要）
* DESCRIPTION（说明）
* EXAMPLES（示例）
* SEE ALSO（参见）

通常 man 手册中的内容很多，你可能不太容易找到你想要的结果，不过幸运的是你可以在 man 中使用搜索，`/<你要搜索的关键字>`，查找到后你可以使用`n`键切换到下一个关键字所在处，`shift+n`为上一个关键字所在处。使用`Space`(空格键)翻页，`Enter`(回车键)向下滚动一行，或者使用`j`,`k`（vim编辑器的移动键）进行向前向后滚动一行。按下`h`键为显示使用帮助(因为man使用less作为阅读器，实为`less`工具的帮助)，按下`q`退出。

想要获得更详细的帮助，你还可以使用`info`命令，不过通常使用`man`就足够了。如果你知道某个命令的作用，只是想快速查看一些它的某个具体参数的作用，那么你可以使用`--help`参数，大部分命令都会带有这个参数，如：

`ls --help`

#### who 命令

`who am i`

out:`claymore tty2 2017-02-16 10:29`

可以查看你的用户名和终端，tty2表示2终端，可以开七个终端。`ctrl+alt+F1-F7`f7是图形终端，其他都是命令终端，打开多个图形终端被称为伪终端。

`who` 命令其它常用参数

| 参数   | 说明                  |
| ---- | ------------------- |
| `-a` | 打印能打印的全部            |
| `-d` | 打印死掉的进程             |
| `-m` | 同`am i`,`mom likes` |
| `-q` | 打印当前登录用户数及用户名       |
| `-u` | 打印当前登录用户登录信息        |
| `-r` | 打印运行等级              |

#### whereis

`whereis name`可看name文件所在的位置

#### ~目录

cd ~ 进入家目录，这个目录在/home/username里,可用`pwd`，来看当前目录

#### top 

可看系统的任务和进程。PR ，RI进程优先级(数字越小优先级越高)，最后优先级看PR+RI的值，也是越小越高。

#### free

当前内存的使用情况

#### buffer和cache

对于操作系统来说：

```
buffer（缓冲）是为了提高内存和硬盘（或其他I/O设备）之间的数据交换的速度而设计的。 cache（缓存）是为了提高cpu和内存之间的数据交换速度而设计的，也就是平常见到的一级缓存、二级缓存
```

对于linux系统来说：free命令会显示buffers和cached

buffers与cached都是内存操作，用来保存系统曾经打开过的文件以及文件属性信息，这样当操作系统需要读取某些文件时，会首先在buffers 与cached内存区查找。

　　buffers是用来缓冲块设备做的，它只记录文件系统的元数据（metadata）以及 tracking in-flight pages，而cached是用来给文件做缓冲。更通俗一点说：buffers主要用来存放目录里面有什么内容，文件的属性以及权限等等。而cached直接用来记忆我们打开过的文件和程序。

所以一般cache会比较大。

#### source和.

先介绍下sh命令：

```
。当然，linux中sh是链接到bash上的，所以sh与bash在功能上是没有区别的。
还有就是在执行脚本的时候是用sh + 脚本名的方式来执行，
大部分的时候，简单脚本只要权限设置正确，可以直接执行，不需要sh命令的
```

source命令：
source命令也称为“[点命令](http://www.51testing.com/?uid-225738-action-viewspace-itemid-206878)”，也就是一个点符号（.）,是bash的内部命令。
功能：使[Shell](http://www.51testing.com/?uid-225738-action-viewspace-itemid-206878)读入指定的Shell程序文件并依次执行文件中的所有语句
source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。
用法：
`source filename 或 . filename`
source命令(从 C Shell 而来)是bash shell的内置命令;点命令(.)，就是个点符号(从Bourne Shell而来)是source的另一名称。

source filename 与 sh filename 及./filename执行脚本的区别在那里呢？
1.当shell脚本具有可执行权限时，用sh filename与./filename执行脚本是没有区别得。./filename是因为当前目录没有在PATH中，所有"."是用来表示当前目录的。
2.sh filename 重新建立一个子shell，在子shell中执行脚本里面的语句，该子shell继承父shell的环境变量，但子shell新建的、改变的变量不会被带回父shell，除非使用export。
3.source filename：这个命令其实只是简单地读取脚本里面的语句依次在当前shell里面执行，没有建立新的子shell。那么脚本里面所有新建、改变变量的语句都会保存在当前shell里面。

bash和sh

sh跟bash的区别，实际上就是bash有没有开启posix模式的区别

可以预想的是，如果第一行写成 #!/bin/bash --posix，那么脚本执行效果跟#!/bin/sh是一样的（遵循posix的特定规范，有可能就包括这样的规范：“当某行代码出错时，不继续往下解释”）



#### 小技巧

* 敲命令时，`ctrl+r`  键入原来打过的命令关键字，自动找出，可以用来找那种很长的命令，但是忘记的。
* `ctrl+u`  : 清空当前已经打下的命令
* 有时候进入了一个很深的目录，但不小心会到了根目录或者其他目录，用`ctrl+-`即可回到原来的目录
