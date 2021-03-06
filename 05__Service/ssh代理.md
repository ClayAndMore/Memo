---
title: "ssh代理.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-04-03 19:50:52 +0800
draft: false
tags: ["linux软件"]
categories: ["linux"]
author: "Claymore"

---
### SSH端口转发

SSH 端口转发是 SSH 提供的一种机制，通过 Server 和 Client 之间的加密连接中继其它端口的流量。

SSH 端口转发一般分为两类：

#### 1.本地端口转发

本地端口转发的作用是把 Client 的某个端口的流量通过 SSH 连接转发到 Server

举个例子，远程有个 mongo 服务器需要连接，但是 mongo 不允许远程连接，只能通过和它同一个局域网的跳板机 A （x.x.x.x）连接。这个时候可以通过端口转发的方法直接连接。

命令格式是：

```text
 ssh -L <local port>:<remote host>:<remote port> <SSH hostname>
```

例如本地开启了 8000 端口监听， mongo 服务器地址为 192.168.0.2 端口 27017, 跳板机地址 192.168.0.1：

```text
 ssh -N -L 8000:192.168.0.2:27017  192.168.0.1 
```

开启完端口转发后，连接 mongo 可以直接通过命令 mongo --host localhost --port 8000

参数 -L `listen-port:host:port ` 指派本地的 port 到达端机器地址上的 port



#### 2.远程端口转发

把 Server 的某个端口的流量通过 SSH 连接转发到 Client 

还是上面的例子：本地 client 无法通过 ssh 连接 跳板机, 但是 跳板机 能 ssh 连接本地。这种情况下可以通过远程端口转发

命令格式：

```text
ssh -R <local port>:<remote host>:<remote port> <SSH hostname>
```

上例可以在本地运行

```text
ssh -R 8000:192.168.0.2:27017  192.168.0.1
```



### 防火墙穿透

假设现在有 A、B、C 三台服务器，C 服务器提供 MySQL 服务，并且防火墙限制只信任来自 B 服务器的流量，其他任何主机均拒绝访问任何端口， A -> B -> C。

有时为了测试需要临时从 A 访问，此时如果修改防火墙策略的话会有些麻烦，还需要测试完后恢复。如果用 SSH 本地端口转发的话，一条命令就解决了，当测试完成后断开此连接即可恢复

```
                            +----------+
                            |    C     | 111.4
                            | Mysql    |
                            +----^-----+
                                 |
                                 +
          A                      B
      +---------+           +----------+
port  |         |           |          |
3306  |         | +-------> | firewall |
      +---------+           +----------+
    192.168.111.2            192.168.111.3
```

`root@A ssh -gL 3306:192.168.111.4:3306 192.168.111.3 -p 22`

现在即可通过连接 A 服务器的 3306 端口，访问 C 服务的MySQL 服务了



### 建立 Socks server

非常简单，只需一条命令即可建立SSH隧道。

```
ssh user@host -ND 127.0.0.1:1080
```

其实就是在常规的SSH命令加上`-D`参数，开启动态端口转发，使SSH成为了SOCKS server，在后台提供网络服务，此时 SSH 充当 Socks 代理服务器的角色。

`-N`参数是让ssh不要返回命令行终端，因为我们不需要发送命令，只是做转发。

1080是绑定的本地端口，也就是SOCKS server提供服务的端口，可以换成其他端口号。

127.0.0.1表示只能有你本机访问这个服务，去掉IP只留下端口号的话，就没有这个限制了。



### 内网穿透

通俗的讲，就是能让外网的电脑找到处于内网的电脑

前提：

VPS：用来接收网络请求，转发请求与相应数据（一般VPS，都会赠送一个相对稳定的`IP`）

域名：有没有都可以，没有的话需要使用`IP`进行访问

内网SSH工具：只要内网的设备可以通过`SSH命令`连接到`VPS`即可

v p s 打开 /etc/ssh/sshd_config，将GatewayPorts参数设为yes, 重启sshd

```
# 内网电脑执行：ssh -NTf -R 8080:127.0.0.1:80 root@vps
8080:绑定远程电脑的端口号
127.0.0.1:内网电脑ip
80:内网电脑端口号
```

远端电脑防火墙开放 8080 端口， 访问 v p s:8080 即可访问内网电脑的 80



### scp 走代理

```shell
scp -o "ProxyCommand=nc -X connect -x proxy_ip:proxy_host %h %p"  filename  username@target_ip:/target_path
```



### 一些参数

```
-1：强制使用ssh协议版本1
-2：强制使用ssh协议版本2
-4：强制使用IPv4地址
-6：强制使用IPv6地址
-A：开启认证代理连接转发功能
-a：关闭认证代理连接转发功能
-b：使用本机指定地址作为对应连接的源ip地址
-C：请求压缩所有数据
-c：选择所加密的密码型式 （blowfish|3des 预设是3des）
-e：设定跳脱字符
-F：指定ssh指令的配置文件
-f：后台执行ssh指令
-g：允许远程主机连接主机的转发端口
-i：指定身份文件（预设是在使用者的家目录 中的 .ssh/identity）
-l：指定连接远程服务器登录用户名
-N：不执行远程指令
-n：重定向stdin 到 /dev/null
-o：指定配置选项
-p：指定远程服务器上的端口（默认22）
-P：使用非特定的 port 去对外联机（注意这个选项会关掉 RhostsAuthentication 和 RhostsRSAAuthentication）
-q：静默模式
-T：禁止分配伪终端
-t：强制配置 pseudo-tty
-v：打印更详细信息
-X：开启X11转发功能
-x：关闭X11转发功能
-y：开启信任X11转发功能
-L listen-port:host:port 指派本地的 port 到达端机器地址上的 port
建立本地SSH隧道(本地客户端建立监听端口)
将本地机(客户机)的某个端口转发到远端指定机器的指定端口.
-R listen-port:host:port 指派远程上的 port 到本地地址上的 port
建立远程SSH隧道(隧道服务端建立监听端口)
将远程主机(服务器)的某个端口转发到本地端指定机器的指定端口.
-D port 指定一个本地机器 “动态的’’ 应用程序端口转发.
```

