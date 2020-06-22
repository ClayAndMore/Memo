---
title: "iptables.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
- `iptables`：用来管理 Linux 防火墙的命令程序，位于`/sbin/iptables`目录下，属于`用户空间`的防火墙管理体系。
- `netfilter：Linux` 内核中实现包过滤防火墙的内部结构，一般`不以程序`或`文件`的形式存在，属于`内核空间`的防火墙管理体系。



## Iptables

四表五链：iptables包含4个表，5个链。

**表是按照对数据包的操作区分的，链是按照不同的Hook点来区分的，**表和链实际上是netfilter的两个维度



![](https://images2015.cnblogs.com/blog/1124877/201703/1124877-20170313192222073-1011363533.png)

不同的表包含的链不同。



### 四表（Tables）

**表的处理优先级：raw>mangle>nat>filter**， 如图中从左到右。

* raw:有限级最高，决定数据包是否被状态跟踪机制处理， 设置raw时一般是为了不再让iptables做数据包的链接跟踪处理，提高性能
* mangle:用于对特定数据包的修改， 修改数据包的服务类型、TTL（存活时间）、并且可以配置路由
* nat: 用于网络地址转换（IP、端口），端口映射，地址映射等
* filter：一般的过滤功能（没有指定表的时候就是filter表）



### 五链（Chains）

- **PREROUTING（进路由）:数据包进入路由表之前。**

  当一个数据包进入网卡时，数据包首先进入PREROUTING链，在PREROUTING链中我们有机会修改数据包的DestIP(目的IP)，然后内核的"路由模块"根据"数据包目的IP"以及"内核中的路由表"判断是否需要转送出去(注意，这个时候数据包的DestIP有可能已经被我们修改过了)

- **INPUT（进本机）:通过路由表后目的地为本机，**

  数据包的目的IP是本机的网口IP)，数据包到达INPUT链。数据包到达INPUT链后，任何进程都会-收到它

- **OUTPUT（出本机）:由本机产生，向外转发**

  本机上运行的程序也可以发送数据包，这些数据包经过OUTPUT链，然后到达POSTROTING链输出(注意，这个时候数据包的SrcIP有可能已经被我们修改过了)

- **FORWARD:通过路由表后，目的地不为本机.**

  如果数据包是要转发出去的(即目的IP地址不再当前子网中)，且内核允许转发，数据包就会向右移动，经过FORWARD链，然后到达POSTROUTING链输出(选择对应子网的网口发送出去)

- **POSTROUTIONG(出路由):发送到网卡接口之前。**

![](https://www.linuxidc.com/upload/2012_08/120807094039061.gif)



**到本机某进程的报文：PREROUTING --> INPUT**

**由本机转发的报文：PREROUTING --> FORWARD --> POSTROUTING**

**由本机的某进程发出报文（通常为响应报文）：OUTPUT --> POSTROUTING**



### Targets

防火墙的规则指定所检查包的特征，和目标。如果包不匹配，将送往该链中下一条规则检查；

如果匹配,那么下一条规则由目标值确定。 **该目标值可以是用户定义的链名,或是某个专用值,如ACCEPT[通过], DROP[删除], QUEUE[排队], 或者 RETURN[返回]。** 

* ACCEPT 表示让这个包通过。
* DROP表示将这个包丢弃。
* QUEUE表示把这个包传递到用户空间。
* RETURN表示停止这条链的匹配，到前一个链的规则重新开始。如果到达了一个内建的链(的末端)，或者遇到内建链的规则是RETURN，包的命运将由链准则指定的目标决定。





### 处理动作

处理动作在iptables中被称为target（这样说并不准确，我们暂且这样称呼），动作也可以分为基本动作和扩展动作。

此处列出一些常用的动作，之后的文章会对它们进行详细的示例与总结：

* **ACCEPT**：允许数据包通过。
* **DROP**：直接丢弃数据包，不给任何回应信息，这时候客户端会感觉自己的请求泥牛入海了，过了超时时间才会有反应。
* **REJECT**：拒绝数据包通过，必要时会给数据发送端一个响应的信息，客户端刚请求就会收到拒绝的信息。
* **SNAT**：源地址转换，解决内网用户用同一个公网地址上网的问题。
* **MASQUERADE**：是SNAT的一种特殊形式，适用于动态的、临时会变的ip上。
* **DNAT**：目标地址转换。
* **REDIRECT**：在本机做端口映射。
* **RETURN：** 停止执行当前链中的后续规则，并返回到调用链(The Calling Chain)中
* **QUEUE：** 将数据包移交到用户空间
* **LOG**：在/var/log/messages文件中记录日志信息，然后将数据包传递给下一条规则，也就是说除了记录以外不对数据包做任何其他操作，仍然让下一条规则去匹配。



#### SNAT和MASQUERADE的区别

https://blog.csdn.net/wuruixn/article/details/8103374





## 命令

如一条简单的开启端口命令：

``` sh
iptables -I INPUT -p tcp --dport 8000 -j ACCEPT #开启8000端口
```

说明：

``` sh
# 命令顺序：
`iptables -t 表名 <-A/I/D/R> 规则链名 [规则号] <-i/o 网卡名> -p 协议名 <-s 源IP/源子网> --sport 源端口 <-d 目标IP/目标子网> --dport 目标端口 -j 动作`

# 表名：raw，mangle，net, filter
# 链名：INPUT OUTPUT PORWARD PREROUTING OSTOUTING

# 选项：
-t<表>：指定要操纵的表, 默认操作 fiLter 表。
-A：向规则链中添加条目， 会出现在表中的末尾.
-D：从规则链中删除条目,  
-i：向规则链中插入条目, 插入在表的开头，这样优先匹配。
-R：替换规则链中的条目；
-L：显示规则链中已有的条目；
-F：清除规则链中已有的条目；

-N：创建新的用户自定义规则链；

-s：把指定的一个／一组地址作为源地址，按此规则进行过滤
-d: 把指定的一个／一组地址作为目的地址，按此规则进行过滤
--sport num：匹配源端口号
--dport num：匹配目的端口号


-j<目标>：指定要跳转的目标；，如 eth0, eth1.
-i<网络接口>：指定数据包进入本机的网络接口；
# -i 只对 INPUT，FORWARD，PREROUTING 这三个链起作用。如果没有指定此选项， 说明可以来自任何一个网络接口
-o<网络接口>：指定数据包要离开本机所使用的网络接口。
# -o OUTPUT，FORWARD，POSTROUTING 三个链起作用。

# -j 动作, 可以是内置的目标，比如 ACCEPT，也可以是用户自定义的链。
参照上方的“处理动作”
```



### eg

指定端口：

``` sh
iptables -A INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT               #允许本地回环接口(即运行本机访问本机)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT    #允许已建立的或相关连的通行
iptables -A OUTPUT -j ACCEPT         #允许所有本机向外的访问
iptables -A INPUT -p tcp --dport 22 -j ACCEPT    #允许访问22端口
iptables -A INPUT -p tcp --dport 80 -j ACCEPT    #允许访问80端口
iptables -A INPUT -p tcp --dport 21 -j ACCEPT    #允许ftp服务的21端口
iptables -A INPUT -p tcp --dport 20 -j ACCEPT    #允许FTP服务的20端口
iptables -A INPUT -j reject       #禁止其他未允许的规则访问
iptables -A FORWARD -j REJECT     #禁止其他未允许的规则访问
```

屏蔽ip:

``` sh
iptables -I INPUT -s 123.45.6.7 -j DROP       #屏蔽单个IP的命令
iptables -I INPUT -s 123.0.0.0/8 -j DROP      #封整个段即从123.0.0.1到123.255.255.254的命令
iptables -I INPUT -s 124.45.0.0/16 -j DROP    #封IP段即从123.45.0.1到123.45.255.254的命令
iptables -I INPUT -s 123.45.6.0/24 -j DROP    #封IP段即从123.45.6.1到123.45.6.254的命令是
```

网络转发：

公网`210.14.67.7`让内网`192.168.188.0/24`上网

```shell
iptables -t nat -A POSTROUTING -s 192.168.188.0/24 -j SNAT --to-source 210.14.67.127
```

端口映射：

本机的 2222 端口映射到内网 虚拟机的22 端口

```shell
iptables -t nat -A PREROUTING -d 210.14.67.127 -p tcp --dport 2222  -j DNAT --to-dest 192.168.188.115:22
```



### 地址转换

目的地址转换，首先需要在开启中开启转发功能（源地址转换也需要开启）：

`echo 1 > /proc/sys/net/ipv4/ip_forward`

```sh
# 把从 eth0 进来要访问 TCP/80 的数据包的目的地址转换到 192.168.1.18
iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 80 -j DNAT --to 192.168.1.18

# 把从 123.57.172.149 进来要访问 TCP/80 的数据包的目的地址转换到 192.168.1.118:8000
iptables -t nat -A PREROUTING -p tcp -d 123.57.172.149 --dport 80 -j DNAT --to 192.168.1.118:8000
```

源地址转换：

```sh
# 最典型的应用是让内网机器可以访问外网：
# 将内网 192.168.0.0/24 的源地址修改为 1.1.1.1 (可以访问互联网的机器的 IP)
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j SNAT --to 1.1.1.1

# 将内网机器的源地址修改为一个 IP 地址池
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j SNAT --to 1.1.1.1-1.1.1.10
```



### 设置链的默认规则

 -P --policy  设置指定链的默认策略 

```sh
iptables -P INPUT DROP     # 配置默认丢弃访问的数据表
iptables -P FORWARD DROP   # 配置默认禁止转发
iptables -P OUTPUT ACCEPT  # 配置默认允许向外的请求
```



### 删除

将所有iptables以序号标记显示，执行：

```undefined
iptables -L --line-numbers
```

比如要删除INPUT里序号为8的规则，执行：

```undefined
iptables -D INPUT 8
```





### iptables 清空

```sh
iptables -F  # 清空表中所有的规则
iptables -X  # 删除表中用户自定义的链
```



### iptables 规则备份和还原

``` sh
service iptables save       # 默认会把规则保存到/etc/sysconfig/iptables
iptables-save>iptbs.rule    # 把iptables规则备份到iptbs.txt文件中
iptables-restore<iptbs.rule # 恢复刚才备份的规则
```





## 服务

`/etc/sysconfig/iptables`

```sh
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
