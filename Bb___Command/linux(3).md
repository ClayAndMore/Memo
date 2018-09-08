---
title: linux 进阶（二）
date: 2017-03-09 15:31:23
categories:
header-img:
tags:
---



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

  ​

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



### 管道

管道是一种通信机制，常用于进程间的通信（也可以用socket网络通信），它表现出的形式就是将前面的每一个进程的输出直接作为下一个进程的输入。

#### `|`

`ls -al /etc | less`

将ls命令的输出做下一个命令less的输入，然后可以一行一行的看。

#### cut

打印每一行的某一字段 。打印/etc/passwd文件以：为分隔符的第一个字段和第六个字段：

`cut /etc/passwd -d ':' -f 1,6`

打印每一行的前N个字符：

```
# 前五个（包含第五个）
$ cut /etc/passwd -c -5
# 前五个之后的（包含第五个）
$ cut /etc/passwd -c 5-
# 第五个
$ cut /etc/passwd -c 5
# 2到5之间的（包含第五个）
$ cut /etc/passwd -c 2-5
```

#### grep

在文本中或stdin（输入）中查找匹配字符串

一般形式：

`grep [命令选项]... 用于匹配的表达式 [文件]...`

可结合正则表达式表现强大的功力：

查看环境变量中以"yanlou"结尾的字符串

`$ export | grep ".*yanlou$"`

当前目录下以py结尾文件内容中包含：AutoField的文件。

`grep -nr 'AutoField' *.py`



#### wc

用于输出文件中，行，单词，字节数。

输出文件夹下 的行数： `ls | wc -l`

输出`/etc/passwd`文件的统计信息：

`wc /etc/passwd`

#### sort

将输入按照一定方式排序，然后再输出,它支持的排序有按字典排序,数字排序，按月份排序，随机排序，反转排序，指定特定字段进行排序等等。 

#### uniq

`uniq`命令可以用于过滤或者输出重复行。



### 数据流重定向

经常用到的两个重定向操作：

`>` 输出到文件，如果存在，则清空，不存在则创建

`>>`追加到文件，如果存在，则追加，不存在则创建

`<` 的作用，就是将原本应该由键盘输入的数据经由文件读入。

linux默认提供了三个特殊设备，用于终端的显示和输出，分别为`stdin`（标准输入,对应于你在终端的输入），`stdout`（标准输出，对应于终端的输出），`stderr`（标准错误输出，对应于终端的输出）。

| 文件描述符 | 设备文件          | 说明   |
| ----- | ------------- | ---- |
| `0`   | `/dev/stdin`  | 标准输入 |
| `1`   | `/dev/stdout` | 标准输出 |
| `2`   | `/dev/stderr` | 标准错误 |

文件描述符：文件描述符在形式上是一个非负整数。实际上，它是一个索引值，指向内核为每一个进程所维护的该进程打开文件的记录表。当程序打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。在程序设计中，一些涉及底层的程序编写往往会围绕着文件描述符展开。但是文件描述符这一概念往往只适用于 UNIX、Linux 这样的操作系统。



##### tee

将屏幕输出同时保存到文件：`sh test.sh | tee file.txt`





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



### find 查找文件

` find  [指定查找目录][查找规则]  [查找完后执行的action]`

eg:

`find /etc /tmp /root -name passwd`

注意的是目录之间要用空格分开

查找规则：

   （1）根据文件名查找

           -name     //根据文件名查找（精确查找）
    
           -iname       //根据文件名查找，但是不区分大小写 
    
    附文件通配：
    
    *表示  通配任意的字符
    
    `find /etc -name pass*`
    
    ？表示  通配任意的单个字符
    
    `find /etc -name passw?`
    
    [ ] 表示 通配括号里面的任意一个字符
    
    `find /tmp -name "[ab].sh"`



#### 删除符合条件的文件

eg： 删除当下目录的所有pyc文件

```
find . -name \*.pyc -delete
```



#### 查找文件中的字符串

我们用grep命令来查找：
`grep -rn "x" *  `

-rn表示递归查找，x表示要查找的字符，*表示当前目录下的所有文件



### Suprise Get

#### state

查看文件状态，eg: `state filename`



#### date

时间设定成2009年5月10号的命令：

`date -s 05/10/2009`

系统时间设定成下午14点30分59秒：

`date -s 14:30:50`





##### w

用于显示已经登陆系统的用户列表，并显示用户正在执行的指令。执行这个命令可得知目前登入系统的用户有那些人，以及他们正在执行的程序。单独执行w命令会显示所有的用户，您也可指定用户名称，仅显示某位用户的相关信息。

```
[root@bogon ~]# w
 17:30:33 up 9 days,  1:43,  4 users,  load average: 4.09, 3.19, 2.92
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/1    192.168.19.39    09:34    7:40m  0.41s  0.24s python kk_count.py
root     pts/2    192.168.19.39    09:38    7:34m  0.01s  0.00s tail -f server_sample.log
root     pts/3    192.168.19.39    09:57   17:05   0.04s  0.04s -bash
root     pts/4    192.168.19.20    17:30    1.00s  0.00s  0.00s w
```

User：登录用户名 
TTY：登录后系统分配的终端号 
From：远程主机名，即从哪登录的 
login@：何时登录 
IDLE：用户空闲时间。这是个计时器，一旦用户执行任何操作，改计时器就会被重置。 
JCPU：和终端连接的所有进程占用时间。包括当前正在运行的后台作业占用时间 
PCPU：当前进程所占用时间 
WHAT：当前正在运行进程的命令行



还可以向某人发消息：

```
[root@bogon ~]# write root pts/1 

hhh
```



##### bg

命令行运行时使用CTRL + Z ，强制当前进程转为后台， 使之挂起（暂停）.

命令job：看当前有哪个进程挂起。

bg %N 使第N个任务在后台运行(%前有空格)

fg %N 使第N个任务在前台运行