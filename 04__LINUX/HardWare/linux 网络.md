Tags:[linux]

## linux 网络

### linux的网卡

网卡的名称是以网卡内核模块对应的设备名称来表示的。

默认网卡名称为eth0， 第二张网卡则为eth1, 以此类推。



网卡需要内核的支持，才能驱动它。

如果不兼容，要么重新编译内核，要么重新编译网卡的内核模块，当然，大家都不愿意这么干。



### hosts

osts文件是Linux系统中一个负责IP地址与域名快速解析的文件，以ASCII格式保存在“/etc”目录下，文件名为“hosts”（不同的linux版本，这个配置文件也可能不同。比如Debian的对应文件是/etc/hostname

一般情况下hosts文件的每行为一个主机，每行由三部份组成，每个部份由空格隔开。其中#号开头的行做说明，不被系统解释。

hosts文件的格式如下：

```
`IP地址 主机名/域名   `
```

微解释一下主机名(hostname)和域名(Domain）的区别：主机名通常在局域网内使用，通过hosts文件，主机名就被解析到对应ip；域名通常在internet上使用，但如果本机不想使用internet上的域名解析，这时就可以更改hosts文件，加入自己的域名解析。

一个IP地址可以指向多个主机名和域名，比如配置`localhost localdomain wangdachui`这三个主机名都是可以解析到本地主机的.



### iptables

`/etc/sysconfig/iptables`

```
# 查看防火墙状态
service iptables status
 
# 停止防火墙
service iptables stop
 
# 启动防火墙
service iptables start
 
# 重启防火墙
service iptables restart
 
# 永久关闭防火墙
chkconfig iptables off
 
# 永久关闭后重启
chkconfig iptables on
```



```
保存规则：shell>iptables-save > /etc/iptables-script

恢复规则：shell>iptables-restore > /etc/iptables-script

保存和恢复的位置只要是两者一致就可以了，如果iptables-script没有则需要创建。
```
`/etc/security/limits.conf`

/etc/security/limits.conf 是 Linux 资源使用配置文件，用来限制用户对系统资源的使用

语法：<domain>  <type>  <item>  <value>

```
[root@localhost ~]# cat /etc/security/limits.conf
* soft nproc 65535      # 警告设定所有用户最大打开进程数为65535
* hard nproc 65535      # 严格设定所有用户最大打开进程数为65535
* soft nofile 65535     # 警告设定所有用户最大打开文件数为65535
* hard nofile 65535     # 严格设定所有用户最大打开文件数为65535
```



```
<domain> 表示要限制的用户，可以是：

         ① 用户名
         ② 组名（组名前面加'@'以区别用户名）
         ③ *（表示所有用户）

<type> 有两个值：

         ① soft 表示警告的设定，可以超过这个设定值，但是超过会有警告信息
         ② hard 表示严格的设定，必定不能超过这个设定的值

<item> 表示可选的资源，如下：

         ① core：限制内核文件的大小
         ② data：最大数据大小
         ③ fsize：最大文件大小
         ④ memlock：最大锁定内存地址空间
         ⑤ nofile：打开文件的最大数目
         ⑥ rss：最大持久设置大小
         ⑦ stack：最大栈大小
         ⑧ cpu：以分钟为单位的最多CPU时间
         ⑨ nproc：进程的最大数目
         ⑩ as：地址空间限制

<value> 表示要限制的值
```



### 查看端口

查看80端口的占用情况：

lsof -i:80  

或者：

netstat -apn | grep 80

上面的命令执行之后可以显示进程号，找到进程号以后，再使用以下命令查看详细信息：

ps -aux | grep <进程号>

### 



### netstat

Netstat用于显示与IP、TCP、UDP和ICMP协议相关的统计数据，一般用于检验本机各端口的网络连接情况.

几个比较重要的参数：

```shell
-a (all)显示所有选项，默认不显示LISTEN相关
-t (tcp)仅显示tcp相关选项
-u (udp)仅显示udp相关选项
-n 拒绝显示别名，能显示数字的全部转化成数字。
-l 仅列出有在 Listen (监听) 的服務状态

-p 显示建立相关链接的程序名
-o 计时
-r 显示路由信息，路由表
-e 显示扩展信息，例如uid等
-s 按各个协议进行统计
-c 每隔一个固定时间，执行该netstat命令。

提示：LISTEN和LISTENING的状态只有用-a或者-l才能看到
```



#### 解释

```shell
root@1# netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 VM-0-6-ubuntu:ssh       222.128.62.122:31001    ESTABLISHED
tcp        0      0 VM-0-6-ubuntu:34546     169.254.0.55:5574       ESTABLISHED
tcp        0      0 VM-0-6-ubuntu:ssh       222.128.62.125:34010    TIME_WAIT  
tcp        0      0 VM-0-6-ubuntu:ssh       211.151.59.19:32842     ESTABLISHED
Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ]         DGRAM                    3483840  /run/user/500/systemd/notify
unix  3      [ ]         STREAM     CONNECTED     21412    /usr/local/yd.socket.client
unix  3      [ ]         DGRAM                    13479    /run/systemd/notify
unix  2      [ ]         DGRAM                    13487    /run/systemd/journal/s
..
```

从整体上看，netstat的输出结果可以分为两个部分：

一个是Active Internet connections，称为有源TCP连接。

- Proto显示socket使用的协议(tcp,udp,raw)。

- "Recv-Q"和"Send-Q"指的是接收队列和发送队列(这些数字一般都应该是0,如果不是则表示软件包正在队列中堆积,这种情况是非常少见的), 单位是字节, 堆积状态是不正常的。

  - Recv-Q :  是表示程序总共还有多少字节的数据没有从内核空间的套接字缓存拷贝到用户空间。

    可能是遭受了拒绝服务 denial-of-service 攻击。

  - Send-Q: 

    可能是有应用向外发送数据包过快，或者是对方接收数据包不够快,

    注意有的程序send成功，但是阻塞在send-Q, send只是表示写入send buffer成功

- Local Address显示在本地哪个地址和端口上监听,Foreign Address显示接收外部哪些地址哪个端口的请求

- State显示socket的状态(通常只有tcp有状态信息)

- PID/Program name显示socket进程id和进程名， p参数

另一个是Active UNIX domain sockets，称为有源Unix域套接口， **和网络套接字一样，但是只能用于本机通信，性能可以提高一倍**。

- Proto显示连接使用的协议
- RefCnt表示连接到本套接口上的进程号,
- Types显示套接口的类型,
- tate显示套接口当前的状态,Path表示连接到套接口的其它进程使用的路径名。





加上-n, 可以比较出加n和不加n的差别， 加n时local Adrress的显示会变成ip:

```shell
ot@VM-0-6-ubuntu:/home/ubuntu# netstat -n
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 172.21.0.6:22           211.151.59.19:32867     ESTABLISHED
tcp        0      0 172.21.0.6:22           222.128.62.122:31001    ESTABLISHED
tcp        0      0 172.21.0.6:34546        169.254.0.55:5574       ESTABLISHED
Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ]         DGRAM                    3483840  /run/user/500/systemd/notify
unix  3      [ ]         STREAM     CONNECTED     21412    /usr/local/yd.socket.client
unix  3      [ ]         DGRAM                    13479    /run/systemd/notify
unix  2      [ ]         DGRAM                    13487    /run/systemd/journal/syslog
...
```



#### 计时器

用-o参数可以计时：

`Proto Recv-Q Send-Q Local Address    Foreign Address   State  PID/Program name  Timer`

会多一行Timer

```
    Timer
keepalive (576.47/0/0)  
timewait (53.30/0/0)
<第一列>      <第二列>
```

第一列，一般有一下几种状态；

* keepalive - 表示是keepalive的时间计时

* on - 表示是重发（retransmission）的时间计时

* off - 表示没有时间计时

* timewait - 表示等待（timewait）时间计时

第二列，

`(576.47/0/0) -> (a/b/c)`

* a -  计时时间值
  * 当第一列为keepalive的时候，a代表keepalive计时时间；
  * 当第一列为on的时候，a代表重发（retransmission）的时间计时；
  * 当第一列为timewait的时候，a代表等待（timewait）的时间计时）

* b - 已经产生的重发（retransmission）次数

* c - keepalive已经发送的探测（probe）包的次数





#### 几个有用的命令组合

* 找出运行在指定端口的进程
  `netstat -anp | grep ':3306'`

* tcp 各种状态表：

  ```
  [root@localhost log]# netstat -nat |awk '{print $6}'|sort|uniq -c
      302 CLOSE_WAIT
        1 established)
      646 ESTABLISHED
        1 FIN_WAIT2
        1 Foreign
       48 LISTEN
        1 SYN_SENT
      317 TIME_WAIT
  ```

* 如果你想看看 http,smtp 或 ntp 服务是否在运行，使用 grep。

  ```shell
  $ sudo netstat -aple | grep ntp
  udp        0      0 enlightened.local:ntp   *:*                                 root       17430       1789/ntpd       
  udp        0      0 localhost:ntp           *:*                                 root       17429       1789/ntpd       
  udp        0      0 *:ntp                   *:*                                 root       17422       1789/ntpd       
  udp6       0      0 fe80::216:36ff:fef8:ntp [::]:*                              root       17432       1789/ntpd       
  udp6       0      0 ip6-localhost:ntp       [::]:*                              root       17431       1789/ntpd       
  udp6       0      0 [::]:ntp                [::]:*                              root       17423       1789/ntpd       
  unix  2      [ ]         DGRAM                    17418    1789/ntpd
  ```

* 各协议网络包的统计：

  ```shell
  $ netstat -s
  Ip:
      32797 total packets received
      0 forwarded
      0 incoming packets discarded
      32795 incoming packets delivered
      29115 requests sent out
      60 outgoing packets dropped
  Icmp:
      125 ICMP messages received
      0 input ICMP message failed.
      ICMP input histogram:
          destination unreachable: 125
      125 ICMP messages sent
      0 ICMP messages failed
      ICMP output histogram:
  ```

  如果想只打印出 TCP 或 UDP 协议的统计数据，只要加上对应的选项（-t 和 -u）

* 核心路由信息：

  ```shell
  [root@localhost ~]# netstat -r
  Kernel IP routing table
  Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
  default         localhost       0.0.0.0         UG        0 0          0 em1
  1.1.1.0         *               255.255.255.0   U         0 0          0 console
  link-local      *               255.255.0.0     U         0 0          0 em1
  link-local      *               255.255.0.0     U         0 0          0 console
  172.17.0.0      *               255.255.0.0     U         0 0          0 docker0
  192.168.18.0    *               255.255.255.0   U         0 0          0 em1
  192.168.122.0   *               255.255.255.0   U         0 0          0 virbr0
  [root@localhost ~]# netstat -rn
  Kernel IP routing table
  Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
  0.0.0.0         192.168.18.2    0.0.0.0         UG        0 0          0 em1
  1.1.1.0         0.0.0.0         255.255.255.0   U         0 0          0 console
  169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 em1
  169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 console
  172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
  192.168.18.0    0.0.0.0         255.255.255.0   U         0 0          0 em1
  192.168.122.0   0.0.0.0         255.255.255.0   U         0 0          0 virbr0
  
  ```




#### state

state列共有12中可能的状态，前面11种是按照TCP连接建立的三次握手和TCP连接断开的四次挥手过程来描述的

* LISTEN:首先服务端需要打开一个socket进行监听，状态为LISTEN 侦听来自远方TCP端口的连接请求 
*  SYN_SENT:客户端通过应用程序调用connect进行active open.于是客户端tcp发送一个SYN以请求建立一个连接.之后状态置为SYN_SENT. 在发送连接请求后等待匹配的连接请求 
* SYN_RECV:服务端应发出ACK确认客户端的 SYN,同时自己向客户端发送一个SYN. 之后状态置为SYN_RECV. 在收到和发送一个连接请求后等待对连接请求的确认 
* ESTABLISHED: 代表一个打开的连接，双方可以进行或已经在数据交互了。代表一个打开的连接，数据可以传送给用户

* FIN_WAIT1: 主动关闭 (active close) 端应用程序调用close，于是其TCP发出FIN请求主动关闭连接，之后进入FIN_WAIT1状态. 等待远程TCP的连接中断请求，或先前的连接中断请求的确认 
* CLOSE_WAIT:被动关闭( passive close )端TCP接到FIN后，就发出ACK以回应FIN请求(它的接收也作为文件结束符传递给上层应用程序),并进入CLOSE_WAIT 等待从本地用户发来的连接中断请求 

* FIN_WAIT2:主动关闭端接到ACK后，就进入了 FIN-WAIT-2  从远程TCP等待连接中断请求 

* LAST_ACK:被动关闭端一段时间后，接收到文件结束符的应用程 序将调用CLOSE关闭连接。这导致它的TCP也发送一个 FIN,等待对方的ACK.就进入了LAST-ACK 等待原来发向远程TCP的连接中断请求的确认 

* TIME_WAIT:在主动关闭端接收到FIN后，TCP 就发送ACK包，并进入TIME-WAIT状态。等待足够的时间以确保远程TCP接收到连接中断请求的确认 

* CLOSING: 比较少见 等待远程TCP对连接中断的确认 

* CLOSED: 被动关闭端在接受到ACK包后，就进入了closed的状态。连接结束.没有任何连接状态 

* UNKNOWN: 未知的Socket状态



### nc/netcat

netcat是网络工具中的瑞士军刀，它能通过TCP和UDP在网络中读写数据。通过与其他工具结合和重定向，你可以在脚本中以多种方式使用它。使用netcat命令所能完成的事情令人惊讶。

netcat所做的就是在两台电脑之间建立链接并返回两个数据流，在这之后所能做的事就看你的想像力了。你能建立一个服务器，传输文件，与朋友聊天，传输流媒体或者用它作为其它协议的独立客户端。

具体参数：

- -g<网关>：设置路由器跃程通信网关，最多设置8个;
- -G<指向器数目>：设置来源路由指向器，其数值为4的倍数;
- -h：在线帮助;
- -i<延迟秒数>：设置时间间隔，以便传送信息及扫描通信端口;
- -l：使用监听模式，监控传入的资料;
- -n：直接使用ip地址，而不通过域名服务器;
- -o<输出文件>：指定文件名称，把往来传输的数据以16进制字码倾倒成该文件保存;
- -p<通信端口>：设置本地主机使用的通信端口;
- -r：指定源端口和目的端口都进行随机的选择;
- -s<来源位址>：设置本地主机送出数据包的IP地址;
- -u：使用UDP传输协议;
- -v：显示指令执行过程; 即详细输出 , 输出Banner
- -w<超时秒数>：设置等待连线的时间;
- -z：使用0输入/输出模式，只在扫描通信端口时使用。连接成功后立即关闭连接， 不进行数据交换 



#### 端口扫描

`nc -z -v -n 172.31.100.7 21-25`

默认是TCP，-u参数调整为udp. 

Banner是一个你连接的服务发送给你的文本信息。在试图鉴别漏洞或者服务器的类型以及版本的时候，Banner信息是非常有用的。并非所有的服务都会发送Banner，但大多数服务都会发送Banner。 



#### Chat Server

假如你想和你的朋友聊聊，有很多的软件和信息服务可以供你使用。但是，如果你没有这么奢侈的配置，比如你在计算机实验室，所有的对外的连接都是被限制的，你怎样和整天坐在隔壁房间的朋友沟通那？不要郁闷了，netcat提供了这样一种方法，你只需要创建一个Chat服务器，一个预先确定好的端口，这样子他就可以联系到你了。

Server

```
$nc -l 1567
```

netcat 命令在1567端口启动了一个tcp 服务器，所有的标准输出和输入会输出到该端口。输出和输入都在此shell中展示。

Client

```
$nc 172.31.100.7 1567
```

不管你在机器B上键入什么都会出现在机器A上。



#### 文件传输

大部分时间中，我们都在试图通过网络或者其他工具传输文件。有很多种方法，比如FTP,SCP,SMB等等，但是当你只是需要临时或者一次传输文件，真的值得浪费时间来安装配置一个软件到你的机器上嘛。假设，你想要传一个文件file.txt 从A 到B。A或者B都可以作为服务器或者客户端，以下，让A作为服务器，B为客户端。

Server

```
$nc -l 1567 < file.txt
```

Client

```
$nc -n 172.31.100.7 1567 > file.txt
```

这里我们创建了一个服务器在A上并且重定向netcat的输入为文件file.txt，那么当任何成功连接到该端口，netcat会发送file的文件内容。

在客户端我们重定向输出到file.txt，当B连接到A，A发送文件内容，B保存文件内容到file.txt.

没有必要创建文件源作为Server，我们也可以相反的方法使用。像下面的我们发送文件从B到A，但是服务器创建在A上，这次我们仅需要重定向netcat的输出并且重定向B的输入文件。

B作为Server

Server

```
$nc -l 1567 > file.txt
```

Client

```
nc 172.31.100.23 1567 < file.txt
```



#### 目录传输

发送一个文件很简单，但是如果我们想要发送多个文件，或者整个目录，一样很简单，只需要使用压缩工具tar，压缩后发送压缩包。

如果你想要通过网络传输一个目录从A到B。

Server

```
$tar -cvf – dir_name | nc -l 1567
```

Client

```
$nc -n 172.31.100.7 1567 | tar -xvf -
```

这里在A服务器上，我们创建一个tar归档包并且通过-在控制台重定向它，然后使用管道，重定向给netcat，netcat可以通过网络发送它。

在客户端我们下载该压缩包通过netcat 管道然后打开文件。

如果想要节省带宽传输压缩包，我们可以使用bzip2或者其他工具压缩。

Server

```
$tar -cvf – dir_name| bzip2 -z | nc -l 1567
```

通过bzip2压缩

Client

```
$nc -n 172.31.100.7 1567 | bzip2 -d |tar -xvf -
```

使用bzip2解压



### ip

作为网络配置工具的一份子，iproute2是linux下管理控制TCP/IP网络和流量控制的新一代工具包，旨在替代老派的工具链net-tools，即大家比较熟悉的ifconfig，arp，route，netstat等命令。

net-tools通过procfs(/proc)和ioctl系统调用去访问和改变内核网络配置，而iproute2则通过netlink套接字接口与内核通讯。iproute2的核心命令是ip。
抛开性能而言，net-tools的用法给人的感觉是比较乱，而iproute2的用户接口相对net-tools来说相对来说，更加直观。比如，各种网络资源（如link、IP地址、路由和隧道等）均使用合适的对象抽象去定义，使得用户可使用一致的语法去管理不同的对象。

老派net-tools已经停止维护， 所以iproute2是未来。

#### 命令格式

`ip`常用命令格式如下：

```
ip [ OPTIONS ] OBJECT { COMMAND | help }

对象OBJECT={ link | addr | addrlabel | route | rule | neigh | ntable | tunnel | maddr | mroute | mrule | monitor | xfrm | token }

选项OPTIONS={ -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] | -h[uman-readable] | -iec | -f[amily] { inet | inet6 | ipx | dnet | link } | -o[neline] | -t[imestamp] | -b[atch] [filename] | -rc[vbuf] [size] }
```

常用对象的取值含义如下：

- `link`：网络设备
- `address`：设备上的协议（IP或IPv6）地址
- `addrlabel`：协议地址选择的标签配置
- `route`：路由表条目
- `rule`：路由策略数据库中的规则

常用选项的取值含义如下：

- `-V，-Version`：显示指令版本信息
- `-s，-stats，statistics`：输出详细信息
- `-h，-human，-human-readable`：输出人类可读的统计信息和后缀
- `-o，-oneline`：将每条记录输出到一行，用‘\’字符替换换行符



#### 网卡信息

`ip add show`,  显示网卡配置信息

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:1e:4f:c8:43:fc brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.24/24 brd 192.168.0.255 scope global eth0
       valid_lft forever preferred_lft forever
```

输出内容详解：
首先这个系统有两个接口：`lo`和`eth0`，`lo`是环回接口，而我们重点关注的则是`eth0`这个普通网络接口；下面在看看每个子项的含义：

- `<BROADCAST,MULTICAST,UP,LOWER_UP>`：`BROADCAST`表示该接口支持广播；`MULTICAST`表示该接口支持多播；`UP`表示该网络接口已启用；`LOWER_UP`表示网络电缆已插入，设备已连接至网络
- `mtu 1500`：最大传输单位（数据包大小）为1,500字节
- `qdisc pfifo_fast`：用于数据包排队
- `state UP`：网络接口已启用
- `qlen 1000`：传输队列长度
- `link/ether 00:1e:4f:c8:43:fc`：接口的MAC（硬件）地址
- `brd ff:ff:ff:ff:ff:ff`：广播地址
- `inet 192.168.0.24/24`：IPv4地址
- `brd 192.168.0.255`：广播地址
- `scope global`：全局有效
- `dynamic enp0s25`：地址是动态分配的
- `valid_lft forever`：IPv4地址的有效使用期限
- `preferred_lft forever`：IPv4地址的首选生存期
- `inet6 fe80::2c8e:1de0:a862:14fd/64`：IPv6地址
- `scope link`：仅在此设备上有效
- `valid_lft forever`：IPv6地址的有效使用期限
- `preferred_lft forever`：IPv6地址的首选生存期



#### ip 管理

- 命令：

  ```
  ip addr add 192.168.0.123/24 dev eth0
  ```

  说明：设置IP

- 命令：`ip add del 192.168.0.123/24 dev eth0`
  说明：删除配置的IP



#### 启用/禁用网卡

- 命令：`ip link set eth0 up`
  说明：启用被禁用的网卡
- 命令：`ip link set eth0 down`
  说明：禁用网卡



#### 路由配置

- 命令：`ip route show`
  说明：查看路由信息
  输出：

  ```
  default via 172.17.175.253 dev eth0 
  169.254.0.0/16 dev eth0 scope link metric 1002 
  172.17.160.0/20 dev eth0 proto kernel scope link src 172.17.169.20 
  ```

  输出内容详解：

  - 输出内容第一条是默认的路由，我们可以根据我们的需要改动它
  - `metric 1002`：跳跃计数，确定网关的优先级，默认20，数值越小优先级越高
  - `proto kernel`：该路由的协议，主要有`redirect`，`kernel`，`boot`，`static`，`ra`等，其中`kernel`指的是直接由核心判断自动设定

- 命令：`ip route get 119.75.216.20`


  说明：通过IP地址查询路由包从哪条路由来

- 命令：`ip route add default via 192.168.0.150/24`
  说明：所有的网络数据包都通过192.168.0.150来转发，而不是以前的默认路由

- 命令：`ip route add 172.16.32.32 via 192.168.0.150/24 dev enp0s3`
  说明：修改特定网卡的默认路由

- 命令：`ip route del 172.17.160.0/20`
  说明：删除路由

- 命令：`ip route flush cache`
  说明：刷新路由表



#### 网络统计数据

这个显示网络统计数据则是`ip`命令非常重要的一个功能，很多时候，我们都依靠该功能来进行排除网络故障。

- 命令：

  ```
  ip -s link
  ```

  说明：显示所有网络接口的统计数据

  输出：

  ```
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT qlen 1
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      RX: bytes  packets  errors  dropped overrun mcast   
      361849729592 174114258 0       0       0       0       
      TX: bytes  packets  errors  dropped carrier collsns 
      361849729592 174114258 0       0       0       0       
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
      link/ether 00:16:3e:08:08:55 brd ff:ff:ff:ff:ff:ff
      RX: bytes  packets  errors  dropped overrun mcast   
      32345193376 115901261 0       0       0       0       
      TX: bytes  packets  errors  dropped carrier collsns 
      139742200499 114451909 0       0       0       0 
  ```

  输出重点内容详解：

  - `RX`：表示接收
  - `TX`：表示发送
  - `bytes`：接收/发送的字节数
  - `packets`：接收/发送的包数
  - `errors`：接收/发送的带有错误的包总数
  - `dropped`：由于处理资源不足导致接收/发送的丢弃的包数
  - `overrun`：因接收溢出（环形缓冲区）导致丢失的包；通常如果接口溢出，则表示内核中存在严重问题，或者说服务器上该网络设备的处理设备太慢
  - `mcast`：接收到的多播包数
  - `carrier`：因数据链路错误导致发送失败的包数
  - `collsns`：因在网络上发送冲突而导致的失败数

- 命令：

  ```
  ip -s -s link ls eth0
  ```

  说明：获取一个特定网络接口的信息；在网络接口名字后面添加选项

  ```
  ls
  ```

  即可。使用多个选项

  ```
  -s
  ```

  会输出指定接口详细的信息；特别是在排除网络连接故障时，这会非常有用。

  输出：



  ```
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
      link/ether 00:16:3e:08:08:55 brd ff:ff:ff:ff:ff:ff
      RX: bytes  packets  errors  dropped overrun mcast   
      32469801665 116402997 0       0       0       0       
      RX errors: length   crc     frame   fifo    missed
                 0        0       0       0       0       
      TX: bytes  packets  errors  dropped carrier collsns 
      140235841575 115066014 0       0       0       0       
      TX errors: aborted  fifo   window heartbeat transns
                 0        0       0       0       2 
  ```





### 修改hostname

#### centos 6

```shell
[root@centos6 ~]$ hostname                                              # 查看当前的hostnmae
centos6.magedu.com
[root@centos6 ~]$ vim /etc/sysconfig/network                            # 编辑network文件修改hostname行（重启生效）
[root@centos6 ~]$ cat /etc/sysconfig/network                            # 检查修改
NETWORKING=yes
HOSTNAME=centos66.magedu.com
[root@centos6 ~]$ hostname centos66.magedu.com                          # 设置当前的hostname(立即生效）
[root@centos6 ~]$ vim /etc/hosts                                        # 编辑hosts文件，给127.0.0.1添加hostname
[root@centos6 ~]$ cat /etc/hosts                                        # 检查
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4 centos66.magedu.com
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
```



#### centos 7

```shell
[root@centos7 ~]$ hostnamectl set-hostname centos77.magedu.com             # 使用这个命令会立即生效且重启也生效
[root@centos7 ~]$ hostname                                                 # 查看下
centos77.magedu.com
[root@centos7 ~]$ vim /etc/hosts                                           # 编辑下hosts文件， 给127.0.0.1添加hostname
[root@centos7 ~]$ cat /etc/hosts                                           # 检查
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 centos77.magedu.com
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
```



改完host,可以执行bash更新 前缀。



### arp

apr -a

