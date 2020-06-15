
---
title: "haproxy.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux, linux_software]

## Haproxy

HAProxy 是一款提供高可用性、负载均衡以及基于TCP（第四层）和HTTP（第七层）应用的代理软件。



**四层：**

- 通过分析IP层及TCP/UDP层的流量实现的基于“IP+端口”的负载均衡。

**七层：**

- 可以根据报内容，再配合负载均衡算法来选择后端服务器，不但可以根据“ip+端口”方式进行负载分流，还可以根据网站的URL，访问域名，浏览器类别，语言等决定负载均衡的策略。
- 七层负载均衡模式下，**负载均衡与客户端及后端的服务器会分别建立一次TCP连接，**而在四层负载均衡模式下，仅建立一次TCP连接；七层负载均衡对负载均衡设备的要求更高，处理能力也低于四层负载均衡。



### nginx， LVS

相较与 Nginx，HAProxy 更专注与反向代理，因此它可以支持更多的选项，更精细的控制，更多的健康状态检测机制和负载均衡算法。

相比较而言，LVS性能最好，但是搭建相对复杂；Nginx的upstream模块支持群集功能，但是对群集节点健康检查功能不强，性能没有Haproxy好。



### 工作原理

![](G:\picture\blog\haproxy\haproxy_原理.png)

client 和Haproxy 建立连接，Haproxy 再和对应的后端server 建立连接，然后作为中间人，转发请求。

 在Haproxy 配置中，对一个代理，会划分为2层，frontend（前端） 和backend（后端）

![](G:\picture\blog\haproxy\haproxy_原理2.png)

frontend:监听端口、协议代理定义，HTTP认证，后端选择等；
backend:监控server，负载均衡，队列。
可以看出，在frontend 中定义了要绑定的地址和端口，以及证书等，在backend，罗列了后端的IP和端口。不过要把2者合在一起写，也是可以的，使用listen 即可，如下：

```
listen http-in
    bind *:80
    server server1 127.0.0.1:8000 maxconn 32
```

https://fangpeishi.com/haproxy_best_practice_notes.html



### 配置文件

配置文件：/etc/haproxy/haproxy.cfg

```cfg
    配置段：
      global：全局配置段
        进程管理及安全配置相关的参数
        性能调整相关参数
        Debug参数
      proxies：代理配置段
        defaults：为frontend, listen, backend提供默认配置；
        fronted：前端，相当于nginx, server {}
        backend：后端，相当于nginx, upstream {}
        listen：同时拥前端和后端
```



#### global

**全局配置段**

进程管理

```shell
– chroot <dir>：修改haproxy的工作目录至指定的目录并在放弃权限之前执行chroot()操作，可以提升haproxy的安全级别，不过需要注意的是要确保指定的目录为空目录且任何用户均不能有写权限；
– daemon：让haproxy以守护进程的方式工作于后台，其等同于“-D”选项的功能，当然，也可以在命令行中以“-db”选项将其禁用；
– gid <number>;：以指定的GID运行haproxy，建议使用专用于运行haproxy的GID，以免因权限问题带来风险；
– group <group name>：同gid，不过指定的组名；
– log <address> <facility> [max level [min level]]：定义全局的syslog服务器，最多可以定义两个；
– log-send-hostname [<string>]：在syslog信息的首部添加当前主机名，可以为“string”指定的名称，也可以缺省使用当前主机名；
– nbproc <number>：指定启动的haproxy进程的个数，只能用于守护进程模式的haproxy；默认只启动一个进程，鉴于调试困难等多方面的原因，一般只在单进程仅能打开少数文件描述符的场景中才使用多进程模式；
– pidfile：
– uid：以指定的UID身份运行haproxy进程；
– ulimit-n：设定每进程所能够打开的最大文件描述符数目，默认情况下其会自动进行计算，因此不推荐修改此选项；Linux默认单进程打开文件数为1024个
– user：同uid，但使用的是用户名；
– stats：# 用户访问统计数据的接口
– node：定义当前节点的名称，用于HA场景中多haproxy进程共享同一个IP地址时；
– description：当前实例的描述信息； 
```



性能调整相关

```
– maxconn <number>：设定每个haproxy进程所接受的最大并发连接数，其等同于命令行选项“-n”；“ulimit -n”自动计算的结果正是参照此参数设定的；
– maxpipes <number>：haproxy使用pipe完成基于内核的tcp报文重组，此选项则用于设定每进程所允许使用的最大pipe个数；每个pipe会打开两个文件描述符，因此，“ulimit -n”自动计算时会根据需要调大此值；默认为maxconn/4，其通常会显得过大；
– noepoll：在Linux系统上禁用epoll机制；
– nokqueue：在BSE系统上禁用kqueue机制；
– nopoll：禁用poll机制；
– nosepoll：在Linux禁用启发式epoll机制；
– nosplice：禁止在Linux套接字上使用内核tcp重组，这会导致更多的recv/send系统调用；不过，在Linux 2.6.25-28系列的内核上，tcp重组功能有bug存在；
– spread-checks <0..50, in percent>：在haproxy后端有着众多服务器的场景中，在精确的时间间隔后统一对众服务器进行健康状况检查可能会带来意外问题；此选项用于将其检查的时间间隔长度上增加或减小一定的随机时长；
– tune.bufsize <number>：设定buffer的大小，同样的内存条件小，较小的值可以让haproxy有能力接受更多的并发连接，较大的值可以让某些应用程序使用较大的cookie信息；默认为16384，其可以在编译时修改，不过强烈建议使用默认值；
– tune.chksize <number>：设定检查缓冲区的大小，单位为字节；更大的值有助于在较大的页面中完成基于字符串或模式的文本查找，但也会占用更多的系统资源；不建议修改；
– tune.maxaccept <number>：设定haproxy进程内核调度运行时一次性可以接受的连接的个数，较大的值可以带来较大的吞吐率，默认在单进程模式下为100，多进程模式下为8，设定为-1可以禁止此限制；一般不建议修改；
– tune.maxpollevents <number>：设定一次系统调用可以处理的事件最大数，默认值取决于OS；其值小于200时可节约带宽，但会略微增大网络延迟，而大于200时会降低延迟，但会稍稍增加网络带宽的占用量；
– tune.maxrewrite <number>：设定为首部重写或追加而预留的缓冲空间，建议使用1024左右的大小；在需要使用更大的空间时，haproxy会自动增加其值；
– tune.rcvbuf.client <number>：
– tune.rcvbuf.server <number>：设定内核套接字中服务端或客户端接收缓冲的大小，单位为字节；强烈推荐使用默认值；
– tune.sndbuf.client：
– tune.sndbuf.server：
```







#### default

配置默认参数，一般会被应用组件继承，如果在应用组件中没有特别声明，将安装默认配置参数设置。

```
defaults
	log		global		//定义日志为global配置中的日志定义
	mode 	http		//模式为http
	option	httplog		//采用http日志格式记录日志
	retries	3			//检查节点服务器失败次数，连续达到三次失败，则认为节点不可用
	redispatch			//当服务器负载很高时，自动结束当前队列处理比较久的连接
	maxconn	2000		//最大连接数
	contimeout	5000	//连接超时时间
	clitimeout	5000	//客户端超时时间
	srvtimeout	5000	//服务器超时时间
```



#### proxies

代理配置段

- defaults段为frontend, listen, backend提供默认配置；
- frontend段用于定义一系列监听的套接字，这些套接字可接受客户端请求并与之建立连接。
- backend段用于定义一系列“后端”服务器，代理将会将对应客户端的请求转发至这些服务器。
- listen段通过关联“frontend”和“backend”定义了一个完整的代理，通常只对TCP流量有用



bind：定义一个或几个监听的套接字，绑定ip及端口
`   bind [<address>]:<port_range> [, …][param*]`

```
listen http_proxy
            bind :80,:443
            bind 10.0.0.1:10080,10.0.0.1:10443
            bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy
```



### timeout

```

timeout http request ：在客户端建立连接但不请求数据时，关闭客户端连接
timeout queue ：等待最大时长
timeout connect： 定义haproxy将客户端请求转发至后端服务器所等待的超时时长
timeout client：客户端非活动状态的超时时长
timeout server：客户端与服务器端建立连接后，等待服务器端的超时时长，
timeout http-keep-alive ：定义保持连接的超时时长
timeout check：健康状态监测时的超时时间，过短会误判，过长资源消耗

```





#### balance

- 用法
  - `balance <algorithm> [arguments]`
  - `balance url_param <param> [check_post [<max_wait>]]`
- 功能
  - 定义负载算法，可用于defaults,listen,backend段



#### mode

- 用法
  - `mode {tcp|http|health}`
- 功能
  - 设定实例的运行模式或协议。当实现内容交换时，前端和后端必须工作于同一种模式(一般说来都是HTTP模式)，否则将无法启动实例

tcp：实例运行于纯TCP模式，在客户端和服务器端之间将建立一个全双工的连接，且不会对7层报文做任何类型的检查；此为默认模式，通常用于SSL、SSH、SMTP等应用；
 http：实例运行于HTTP模式，客户端请求在转发至后端服务器之前将被深度分析，所有不与RFC格式兼容的请求都会被拒绝；
 health：实例工作于health模式，其对入站请求仅响应“OK”信息并关闭连接，且不会记录任何日志信息；此模式将用于响应外部组件的健康状态检查请求；目前业讲，此模式已经废弃，因为tcp或http模式中的monitor关键字可完成类似功能



比较全的： https://www.jianshu.com/p/5b9339b8fc97

https://blog.csdn.net/zzhongcy/article/details/46443765



### 负载均衡常用算法

LVS、Haproxy、Nginx最用的调度算法有三种：

1. RR(Round Robin)。RR算法是最简单最常用的一种算法，即轮询调度。
2. LC(Least Connections)。LC算法即最小连接数算法，根据后端的节点连接数大小动态分配前端请求。
3. SH(Source Hashing)。SH即基于来源访问调度算法，此算法用于一些有session回话记录在服务器端的前景，可以基于来源的IP，Cookie等做群集调度。