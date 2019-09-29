Tags:[linux] date: 2017-02-15

### linux启动流程

通电一个默认的物理地址->bios->找到磁盘第一个扇区->引导程序->内核->挂载文件系统->系统服务->应用程序


### SSH

SSH 为 [Secure Shell](http://baike.baidu.com/view/2118359.htm) 的缩写，SSH 为建立在应用层基础上的安全协议。SSH 是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题。SSH最初是UNIX系统上的一个程序，后来又迅速扩展到其他操作平台。SSH在正确使用时可弥补网络中的漏洞。SSH客户端适用于多种平台。几乎所有UNIX平台以及其他平台，都可运行SSH。



### 版本分类

linux 发行版来分类：

RedHat 系列 

centos 社区旗舰版

RHEL (Redhat Enterprise linux)  商业版，大型企业核心服务器首选

* 常见的安装包格式 rpm包,安装rpm包的命令是“rpm -参数” 
* 包管理工具  yum 

Debian系列（ubuntu基于此系列）['dɛbɪrn]

Ubuntu 基于 Debian 的 unstable 或者 testing 分支，同时对来自 Debian 的部分软件包进行了一定的修改，以使其更加适合桌面使用。 同时，优化了安装过程，使 Ubuntu 安装起来更加容易。

* 常见的安装包格式 deb包,安装deb包的命令是“dpkg -参数”
* 包管理工具 apt-get



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

参数后面的文字信息是发送给其他在使用这台机器的用户

如果只是想发送给其他用户消息可以用k参数：

`shutdown -k now '现在谁在用这台机器请联系XX'`

第一个命令中的参数now意味着时间0，

重启：

reboot , init 6

正确的重启方式是：`sync`  -> `reboot`



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



#### sleep

`sleep [--help] [--version] number[smhd]`

- --help : 显示辅助讯息
- --version : 显示版本编号
- number : 时间长度，后面可接 s、m、h 或 d
- 其中 s 为秒，m 为 分钟，h 为小时，d 为日数

eg: 休眠5分钟：

`sleep 5m`





#### 小技巧

* 敲命令时，`ctrl+r`  键入原来打过的命令关键字，自动找出，可以用来找那种很长的命令，但是忘记的。
* `ctrl+u`  : 清空当前已经打下的命令
* 有时候进入了一个很深的目录，但不小心会到了根目录或者其他目录，用`ctrl+-`即可回到原来的目录
* 如果一行太长，可以用`\+enter`来敲打下一行



### Watchdog 看门狗

Linux 自带了一个 watchdog 的实现，用于监视系统的运行，包括一个内核 watchdog module 和一个用户空间的 watchdog 程序。内核 watchdog 模块通过 /dev/watchdog 这个字符设备与用户空间通信。用户空间程序一旦打开 /dev/watchdog 设备（俗称“开门放狗”），就会导致在内核中启动一个1分钟的定时器（系统默认时间），此后，用户空间程序需要保证在1分钟之内向这个设备写入数据（俗称“定期喂狗”），每次写操作会导致重新设定定时器。如果用户空间程序在1分钟之内没有写操作，定时器到期会导致一次系统 reboot 操作（“狗咬人了”呵呵）。通过这种机制，我们可以保证系统核心进程大部分时间都处于运行状态，即使特定情形下进程崩溃，因无法正常定时“喂狗”，Linux系统在看门狗作用下重新启动（reboot），核心进程又运行起来了。多用于嵌入式系统。



### 计划任务crontab

我们会有写定期定时的任务。

该命令从输入设备读取指令，并将其放在crontab中，供之后读取和执行。

通常，crontab储存的指令被守护进程激活，crond为其守护进程，常常在后台执行，每一分钟会检查一次是否有预定的作业要执行。

* 启动日志rsyslog

  启动日志来看我们的任务是否真的被执行

  `sudo service rsyslog start`

* 启动crontab

  `sudo cron -f &`

* 添加一个计划任务

  `crontab -e`

  第一次启动会让你选择一个编辑器，我们选择vim

* 后续会进入到一个编辑界面，这边是添加计划的地方，与一般的配置文档相同，以#开头的是注释

  ![](http://ojynuthay.bkt.clouddn.com/crontab11.png)

  最后一句便是我们添加的任务了，这个任务每分钟会在home/claymore/创建一个年月日时分秒为名字的空白文件

  前面五颗星：minute hour day month week (美好日月星辰)

* 查看添加了那些任务

  `crontab -l`

  虽然我们添加了任务，但是cron的守护进程没有启动不会检测到有任务，我们可以通过下面两种方式来确定我们的cron是否在后台启动：

  `pa aux | grep cron`

  `pgrep cron`

* 看执行任务命令在日志的信息

  `sudo tail -f /var/log/syslog`

* 删除任务

  `crontab -r`

  

#### 深入

每次用`crontab -e`都会添加计划任务，都会在/var/spool/cron/crontabs中添加一个该用户自己的任务文档。这样是为了隔离

所以，系统级别的任务需要sudo权限编辑/etc/crontab文件就可以。

cron 服务监测时间最小单位是分钟，所以 cron 会每分钟去读取一次 /etc/crontab 与 /var/spool/cron/crontabs 里面的內容。

在 /etc 目录下，cron 相关的目录有下面几个：

![](http://ojynuthay.bkt.clouddn.com/cron.png)

每个目录的作用：

1. /etc/cron.daily，目录下的脚本会每天执行一次，在每天的6点25分时运行；
2. /etc/cron.hourly，目录下的脚本会每个小时执行一次，在每小时的17分钟时运行；
3. /etc/cron.mouthly，目录下的脚本会每月执行一次，在每月1号的6点52分时运行；
4. /etc/cron.weekly，目录下的脚本会每周执行一次，在每周第七天的6点47分时运行；

系统默认执行时间可以根据需求进行修改。



### 一句话执行命令

比如可能进行以下部分操作：

```
sudo apt-get update
sudo apt-get install some-tool
some-tool
```

这几个命令之间有等待。我们可以一次性输入完：

`sudo apt-get update;sudo apt-get install some-tool;some-tool`

然后就可以让它一次性运行了

但是前面的命令没成功怎么办？用which来查找是否安装了某个命令

`which cowsay>/dev/null && cowsay -f head-in ohch~`

没有安装cowsay，什么也不会发生，如果安装了cowsay则会发生。

 &&表示前面的命令执行状态（不是输出结果）为0，则执行后面的

||表示前面的命令执行状态不为0，则执行后面的




### 日志系统

在 Linux 中大部分的发行版都内置使用 syslog 系统日志，那么通过前期的课程我们了解到常见的日志一般存放在 `/var/log`中：

`$ ll /var/log`





### 神器 lsof

list openfiles,  列出打开文件，因为unix中一切都是文件，所以将它称之为神器。

lsof有着实在是令人惊讶的选项数量。你可以使用它来获得你系统上设备的信息，你能通过它了解到指定的用户在指定的地点正在碰什么东西，或者甚至是一个进程正在使用什么文件或网络连接。

lsof -p 813   进程为813的进程打开的文件

lsof abc.txt         显示开启文件abc.txt的进程
lsof -c abc         显示abc进程现在打开的文件

lsof +d /usr/local/     显示目录下被进程开启的文件
lsof +D /usr/local/    同上，但是会搜索目录下的目录，时间较长


### date

时间设定成2009年5月10号的命令：

`date -s 05/10/2009`

系统时间设定成下午14点30分59秒：

`date -s 14:30:50`



### 比较合并

比较

`diff -y [file1][flie2]` 同行输出两个文件的不同

`diff -u [file1][flie2]`以补丁格式输出两个文件的不同

`diff -Nu [file1][file2]>[patchfile]`将不同输出到补丁文件

`patch -p[n]<[patchfile]` 打补丁文件，n一般为0，目录级联
