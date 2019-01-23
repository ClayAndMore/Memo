### tcp







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
 
#<span style="font-family:SimHei;color:#333333;LINE-HEIGHT: 22px;">控制 TCP/IP 尝试验证空闲连接是否完好的频率</span>
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

