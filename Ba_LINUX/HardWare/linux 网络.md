Tags:[linux]

## linux 网络

### linux的网卡

网卡的名称是以网卡内核模块对应的设备名称来表示的。

默认网卡名称为eth0， 第二张网卡则为eth1, 以此类推。



网卡需要内核的支持，才能驱动它。

如果不兼容，要么重新编译内核，要么重新编译网卡的内核模块，当然，大家都不愿意这么干。





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



### 网络

- netstat 当前网络状态
- ping 
- ifconfig
- ssh
- ftp
- telnet

#### 查看端口

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