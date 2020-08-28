---
title: "lsof"
date: 2020-07-20 17:53:13 +0800
lastmod: 2020-07-20 17:53:13 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---



这个工具称之为lsof真实名副其实，因为它是指“列出打开文件（lists openfiles）”。而有一点要切记，在Unix中一切（包括网络套接口）都是文件。

有趣的是，lsof也是有着最多开关的Linux/Unix命令之一。它有那么多的开关，它有许多选项支持使用-和+前缀。



### 使用  -i 查看网络连接信息

`lsof -i[46] [protocol][@hostname|hostaddr][:service|port]`

使用：

``` sh
$ lsof -i # 显示所有连接
COMMAND     PID            USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
systemd-r   925 systemd-resolve   12u  IPv4   20186      0t0  UDP localhost:domain
systemd-r   925 systemd-resolve   13u  IPv4   20187      0t0  TCP localhost:domain (LISTEN)
sshd       1613            root    3u  IPv4   24728      0t0  TCP *:ssh (LISTEN)

lsof -i 4   # 显示 ipv4 连接
lsof -i TCP #  显示tcp连接
lsof -i 4TCP  # 显示ipv4 & tcp 连接，注意，这里一定是连着一起的

# hostname
lsof -i4TCP@localhost
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
superviso  3072 root    4u  IPv4   33279      0t0  TCP localhost.localdomain:9002 (LISTEN)
sshd      19984 root   10u  IPv4 5883020      0t0  TCP localhost.localdomain:6010 (LISTEN)

# hostaddr
lsof -i4TCP@192.168.33.206
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
sshd    19984 root    3u  IPv4 5878679      0t0  TCP wy:ssh->192.168.33.206:59373 (ESTABLISHED)

# 然后就是最常用的 -i
lsof -i:22

# 端口范围显示的连接
lsof  -i @fw.google.com:2150=2180
```



### 使用 -u 查看用户打开的文件

``` sh
# lsof -u root | head
COMMAND     PID USER   FD      TYPE             DEVICE SIZE/OFF       NODE NAME
systemd       1 root  cwd       DIR                8,2     4096          2 /
systemd       1 root  rtd       DIR                8,2     4096          2 /
systemd       1 root  txt       REG                8,2  1440088     655582 /lib/systemd/systemd

# 可以消灭指定用户运行的所有文件
kill  -9  `lsof -t -u test`
```





### 使用 -p  查看指定进程id打开的文件

``` sh
# lsof -p 23425
COMMAND     PID USER   FD      TYPE  DEVICE SIZE/OFF    NODE NAME
apiserver 23425 root  cwd       DIR     8,2     4096 2098302 /root/go/workspace/src/apiserver
apiserver 23425 root  rtd       DIR     8,2     4096       2 /
apiserver 23425 root  txt       REG     8,2 40681528 3679546 /root/go/workspace/src/apiserver/apiserver
apiserver 23425 root  mem       REG     8,2    55768  660475 /lib/x86_64-linux-gnu/libnss_files-2.28.so
```



### 指定文件和目录

``` sh
# 使用 +d 显示目录下被进程开启的文件
# lsof +d log/
COMMAND     PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
apiserver 23425 root    8w   REG    8,2  5407256 2372576 log/debug.log
apiserver 23425 root   10w   REG    8,2    74727 2372573 log/err.log

# losf +D  log/ 和上方一样，但是会遍历目录下的目录
```

lsof abc.txt         显示开启文件abc.txt的进程
lsof -c abc         显示abc进程现在打开的文件



