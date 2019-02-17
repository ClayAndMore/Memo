Tags: [网络协议, tcp]

## tcp

### 报文格式

![](G:\picture\blog\tcp\tcp_rep_format.png)

标志位：共6个，即URG、ACK、PSH、RST、SYN、FIN等，具体含义如下：

* ACK：确认序号有效, 确认编号,Acknowledgement Number, 是对TCP请求的确认标志,同时提示对端系统已经成功接收所有数据。
* SYN：发起一个新连接, 同步序列编号,Synchronize Sequence Numbers
* FIN：释放一个连接, 结束标志,FINish.
* PSH：接收方应该尽快将这个报文交给应用层。
* RST：重置连接。
* URG：紧急指针（urgent pointer）有效。

Seq序号，占32位，用来标识从TCP源端向目的端发送的字节流，发起方发送数据时对此进行标记

Ack序号，占32位，只有ACK标志位为1时，确认序号字段才有效，Ack=Seq+1

注意：

（A）不要将确认序号Ack与标志位中的ACK搞混了。
（B）确认方Ack发起方Req+1，两端配对。



### 三次握手

![](G:\picture\blog\tcp\tcp_3times_build.png)



#### SYN 攻击

在三次握手过程中，服务器发送SYN-ACK之后，收到客户端的ACK之前的TCP连接称为半连接(half-open connect).此时服务器处于Syn_RECV状态。
当收到ACK后，服务器转入ESTABLISHED状态.Syn攻击就是 攻击客户端 在短时间内伪造大量不存在的IP地址，向服务器不断地发送syn包，服务器回复确认包，并等待客户的确认，由于源地址是不存在的，服务器需要不断的重发直 至超时，这些伪造的SYN包将长时间占用未连接队列，正常的SYN请求被丢弃，目标系统运行缓慢，严重者引起网络堵塞甚至系统瘫痪。
Syn攻击是一个典型的DDOS攻击。检测SYN攻击非常的方便，当你在服务器上看到大量的半连接状态时，特别是源IP地址是随机的，基本上可以断定这是一次SYN攻击.在Linux下可以如下命令检测是否被Syn攻击`netstat -ntp | grep SYN_RECV`
一般较新的TCP/IP协议栈都对这一过程进行修正来防范Syn攻击，修改tcp协议实现。
主要方法有SynAttackProtect保护机制、SYN cookies技术、增加最大半连接和缩短超时时间等.但是不能完全防范syn攻击。



#### TCP queue

 当 client 通过 connect 向 server 发出 SYN 包时:

**client 会维护一个 socket 等待队列，而 server 会维护一个 SYN 队列**

SYN 队列的长度为` max(64, /proc/sys/net/ipv4/tcp_max_syn_backlog) `决定

* 此时进入半链接的状态，如果 socket 等待队列满了，server 则会丢弃，而 client 也会由此返回 connection time out；

* 当 server 收到 client 的 SYN 包后，会返回 SYN, ACK 的包加以确认，client 的 TCP 协议栈会唤醒 socket 等待队列，发出 connect 调用

* 只要是 client 没有收到 SYN+ACK，3s 之后，client 会再次发送，如果依然没有收到，9s 之后会继续发送



client 返回 ACK 的包后，server 会进入一个新的叫 accept 的队列，该队列的长度为 `min(backlog, somaxconn)。`

默认情况下，[somaxconn](https://serverfault.com/questions/518862/will-increasing-net-core-somaxconn-make-a-difference) 的值为 128，表示最多有 129 的 ESTAB 的连接等待 accept()。

而 backlog 的值则由 `int listen(int sockfd, int backlog)` 中的第二个参数指定

当 accept 队列满了之后，即使 client 继续向 server 发送 ACK 的包，也会不被相应.

此时，server 通过 `/proc/sys/net/ipv4/tcp_abort_on_overflow` 来决定如何返回，

0 表示直接丢丢弃该 ACK，1 表示发送 RST 通知 client；相应的，client 则会分别返回 read timeout 或者 connection reset by peer。

但实际可能是服务器会随机的忽略收到的 SYN，建立起来的连接数可以无限的增加，只不过客户端会遇到延时以及超时的情况。





### 四次挥手

![](G:\picture\blog\tcp\tcp_4times_close.png)



不要被图中的 client 和 server 所迷惑，你只要记住：主动关闭的一方发出 FIN 包，被动关闭的一方响应 ACK 包，此时，被动关闭的一方就进入了 CLOSE_WAIT 状态。



#### CLOSE_WAIT 过多

如上图， close_wait状态出现的原因是被动关闭方未关闭socket造成

通常，CLOSE_WAIT 状态在服务器停留时间很短，如果你发现大量的 CLOSE_WAIT 状态，那么就意味着被动关闭的一方没有及时发出 FIN 包，一般有如下几种可能：

* 程序问题：如果代码层面忘记了 close 相应的 socket 连接，那么自然不会发出 FIN 包，从而导致 CLOSE_WAIT 累积；或者代码不严谨，出现死循环之类的问题，导致即便后面写了 close 也永远执行不到。

* 响应太慢或者超时设置过小：如果连接双方不和谐，一方不耐烦直接 timeout，另一方却还在忙于耗时逻辑，就会导致 close 被延后。

  响应太慢是首要问题，不过换个角度看，也可能是 timeout 设置过小。

* BACKLOG 太大：此处的 backlog 不是 syn backlog，而是 accept 的 backlog，如果 backlog 太大的话，设想突然遭遇大访问量的话，即便响应速度不慢，也可能出现来不及消费的情况，导致多余的请求还在队列里就被对方关闭了。

[error: [Errno 32\] Broken pipe] 



按照前面图例所示，当被动关闭的一方处于 CLOSE_WAIT 状态时，主动关闭的一方处于 FIN_WAIT2 状态。 那么为什么我们总听说 CLOSE_WAIT 状态过多的故障，但是却相对少听说 FIN_WAIT2 状态过多的故障呢？

这是因为 Linux 有一个「tcp_fin_timeout」设置，控制了 FIN_WAIT2 的最大生命周期。坏消息是 CLOSE_WAIT 没有类似的设置，如果不重启进程，那么 CLOSE_WAIT 状态很可能会永远持续下去；好消息是如果 socket 开启了 [keepalive](http://www.tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/) 机制，那么可以通过相应的设置来清理无效连接，不过 keepalive 是治标不治本的方法，还是应该找到问题的症结才对。

通过修改一下TCP/IP的参数，来缩短这个时间：修改tcp_keepalive_*系列参数有助于解决这个问题。tcp_keepalive_time ：INTEGER 默认值是7200(2小时)当keepalive打开的情况下，TCP发送keepalive消息的频率。

由于目前网络攻击等因素,造成了利用这个进行的攻击很频繁,曾经也有cu的朋友提到过,说如果2边建立了连接,然后不发送任何数据或者rst/fin消息,那么持续的时间是不是就是2小时,空连接攻击? tcp_keepalive_time就是预防此情形的.我个人在做nat服务的时候的修改值为1800秒)



#### TIME_WAIT 过多

`TIME_WAIT`产生的原因图中已经说明了，是主动关闭的一方所处的状态，然后在保持这个状态2MSL（max segment lifetime）时间之后，彻底关闭回收资源。

最后，Client端等待了2MSL后依然没有收到回复，则证明Server端已正常关闭，那好，我Client端也可以关闭连接了， 为什么TIME_WAIT状态需要经过2MSL(最大报文段生存时间)才能返回到CLOSE状态？

- 为了保证发送的最后一个ACK报文段能够到达B

- 防止“已失效的连接请求报文段”出现在本连接中。在发送完最后一个ACK报文段后，再经过实践2MSL，就可以使本连接持续的时间内所产生的所有报文段，都从网络中消失。这样就可以使下一个新的连接中不会出现这种就得连接请求报文段。

- 可靠的关闭TCP连接。在主动关闭方发送的最后一个 ack(fin) ，有可能丢失，这时被动方会重新发fin, 如果这时主动方处于 CLOSED 状态 ，就会响应 rst 而不是 ack。

  所以主动方要处于 TIME_WAIT 状态，而不能是 CLOSED 。另外这么设计TIME_WAIT 会定时的回收资源，并不会占用很大资源的，除非短时间内接受大量请求或者受到攻击



CLOSE_WAIT的情况需要从程序本身出发，而`TIME_WAIT`更倾向于修改系统参数。

/etc/sysctl.conf和timeout有关的参数：

```shell
#表示开启重用。允许将TIME_WAIT sockets重新用于新的TCP连接，默认为0，表示关闭
1、net.ipv4.tcp_tw_reuse = 1

#表示开启TCP连接中TIME_WAIT sockets的快速回收，默认为0，表示关闭
2、net.ipv4.tcp_tw_recycle = 1

#表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN_WAIT_2状态的时间（可改为30，一般来说FIN_WAIT_2的连接也极少
3、net.ipv4.tcp_fin_timeout = 30

#表示系统同时保持TIME_WAIT的最大数量，如果超过这个数字，TIME_WAIT将立刻被清除并打印警告信息。默认为180000，改为60000。
4、net.ipv4.tcp_max_tw_buckets = 60000

#为了打开对端的连接，内核需要发送一个SYN并附带一个回应前面一个SYN的ACK。也就是所谓三次握手中的第二次握手。这个设置决定了内核放弃连接之前发送SYN+ACK包的数量。
5、net.ipv4.tcp_synack_retries = 2

#对于一个新建连接，内核要发送多少个 SYN 连接请求才决定放弃。不应该大于255，默认值是5，对应于180秒左右时间。
6、net.ipv4.tcp_syn_retries = 2 

# 表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；
7、net.ipv4.tcp_syncookies = 1

# 表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为1024到65000。
8、net.ipv4.ip_local_port_range = 1024 65000

# 表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数。
net.ipv4.tcp_max_syn_backlog = 8192
```



#### FIN_WAIT2 过多

https://huoding.com/2016/09/05/542




### sysctl

sysctl命令用于运行时配置内核参数，这些参数位于/proc/sys目录下。

sysctl配置与显示在/proc/sys目录中的内核参数．可以用sysctl来设置或重新设置联网功能，如IP转发、IP碎片去除以及源路由检查等。

用户只需要编辑/etc/sysctl.conf文件，即可手工或自动执行由sysctl控制的功能。   

sysctl [param]

常用参数的意义：

​    -w   临时改变某个指定参数的值，如

​         sysctl -w net.ipv4.ip_forward=1

​    -a   显示所有的系统参数

​    -p   从指定的文件加载系统参数，如不指定即从/etc/sysctl.conf中加载

eg:

```
如果仅仅是想临时改变某个系统参数的值，可以用两种方法来实现,例如想启用IP路由转发功能：

1) #echo 1 > /proc/sys/net/ipv4/ip_forward

2) #sysctl -w net.ipv4.ip_forward=1
以上两种方法都可能立即开启路由功能，但如果系统重启，或执行了

service network restart
命令，所设置的值即会丢失，如果想永久保留配置，可以修改/etc/sysctl.conf文件
将 net.ipv4.ip_forward=0改为net.ipv4.ip_forward=1
```

修改好后记得用 sysctl -p 重载



### sysctl 和 sysctl.conf的关系

其实每个'.'分割的就代表一个目录，例如，fs.file-max也就代表/proc/sys/fs/file-max。

那么/proc/sys/是用来做什么的呢？

大家都知道/proc是每次系统启动的时候都要重新挂载的，它反映了系统内存里面的一些状态。

通过/proc/可以很好的了解到当前系统的一些信息。

而/proc/sys/则是这些信息的一小部分而已。



### sysctl.conf

内核：/etc/sysctl.conf

```ini
#表示开启重用。允许将TIME_WAIT sockets重新用于新的TCP连接，默认为0，表示关闭
1、net.ipv4.tcp_tw_reuse = 1
 
#表示开启TCP连接中TIME_WAIT sockets的快速回收，默认为0，表示关闭
2、net.ipv4.tcp_tw_recycle = 1
 
#表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN_WAIT_2状态的时间（可改为30，一般来说FIN_WAIT_2的连接也极少）</span>
3、net.ipv4.tcp_fin_timeout = 30
 
#控制 TCP/IP 尝试验证空闲连接是否完好的频率, 7200(2小时)
4、net.ipv4.tcp_keepalive_time = 600 
 
#表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数。
5、net.ipv4.tcp_max_syn_backlog = 8192 
 
#表示系统同时保持TIME_WAIT的最大数量，如果超过这个数字，TIME_WAIT将立刻被清除并打印警告信息。默认为180000，改为60000。
6、net.ipv4.tcp_max_tw_buckets = 60000
 
#记录的那些尚未收到客户端确认信息的连接请求的最大值。对于有128M内存的系统而言，缺省值是1024，小内存的系统则是128。
7、net.ipv4.tcp_max_syn_backlog = 65536
 
#每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
8、net.core.netdev_max_backlog = 32768
 
#web应用中listen函数的backlog默认会给我们内核参数的net.core.somaxconn限制到128，而nginx定义的NGX_LISTEN_BACKLOG默认为511，所以有必要调整这个值。
9、net.core.somaxconn = 32768
 
#定义默认的发送窗口大小;对于更大的 BDP 来说,这个大小也应该更大。
10、net.core.wmem_default = 8388608
 
#该文件指定了接收套接字缓冲区大小的缺省值(以字节为单位)。
11、net.core.rmem_default = 8388608
 
#最大socket读buffer。
12、net.core.rmem_max = 16777216
 
#最大socket写buffer。
13、net.core.wmem_max = 16777216
 
#为了打开对端的连接，内核需要发送一个SYN并附带一个回应前面一个SYN的ACK。也就是所谓三次握手中的第二次握手。这个设置决定了内核放弃连接之前发送SYN+ACK包的数量。
14、net.ipv4.tcp_synack_retries = 2
 
#对于一个新建连接，内核要发送多少个 SYN 连接请求才决定放弃。不应该大于255，默认值是5，对应于180秒左右时间。
15、net.ipv4.tcp_syn_retries = 2 
 
#表示开启TCP连接中TIME-WAITsockets的快速回收，默认为0，表示关闭
16、net.ipv4.tcp_tw_recycle = 1
 
#开启重用。允许将TIME-WAITsockets重新用于新的TCP连接。
17、net.ipv4.tcp_tw_reuse = 1
 
#同样有3个值,意思是:低于第一个值，TCP没有内存压力；在第二个值下，进入内存压力阶段；高于第三个值，TCP拒绝分配socket（内存单位是页）。
18、net.ipv4.tcp_mem = 94500000 915000000 927000000
 
#系统中最多有多少个TCP套接字不被关联到任何一个用户文件句柄上。
19、net.ipv4.tcp_max_orphans = 3276800
 
#每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
20、net.core.netdev_max_backlog = 8096
 
#表示开启SYNCookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭。
21、net.ipv4.tcp_syncookies = 1

```

