
---
title: "01_redis介绍和安装.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "01_redis介绍和安装.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
### 关系型数据库原理

```
                磁盘                        |   内存
  4k                   4k                   |
+---------------+      +-----------------+  | +----------+
|     datapage  |      |    index        |  | |          |
|               |      |                 |  | | B+ tree  |
|               +<-------+               |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
|               |      |                 |  | |          |
+----------------      +-----------------+  | +----------+                          
```

1. 在磁盘中存数据是按datapage页来存的
2. 所有的页需要被索引管理，但是索引记录也需要4k的page来记录
3. 4k的原因 是i/o交互的最大容量
4. 那谁来找管理和找索引页呢，在内存中有B+tree来管理
5. 两次i/o， 查索引页一次，查datapage一次。

缺点： 当并发时，内存频繁和内存交互，响应缓慢。





## Redis

Red is 是一个基于内存的高效的非关系型数据库, C语言实现。

1. 基于开源的BSD协议，当然基于开源的做出的东西也要开源。
2. 使用c语言编写，非常小，7兆左右
3. **基于内存的持久化**
4. 高性能的key-value 的 nosql数据库



### 相关链接

官方 https: //redis. io
官方文档 https ://redis.io/documentation
中文官网 https://www.redis.cn
GitHub: https://github.com/antirez/redis
中文教程 http ://www.runoob.com/redis/dis-tutorial.html



### 安装

CentOS Red Hat

```
首先添加 EPEL 仓库，然后更新 yum 源：
sudo yum install epel release
sudo yum update

然后安装 数据库：
sudo yum -y install redis

安装好后启动服务即可
sudo systemctl start redis

可以使用 redis-cli 进入 命令行模式操作:
$ redis-cli
121.0.0.1:6379> set ’ name ’ ’Germey'
OK
121.0.0.1:6379> get ’ name'
”Germey”
```

配置远程连接

为了可以使 Redis能被远程连接，需要修改配置文件，路径为/etc/redis.conf：

```
首先，注释这一行
bind 127.0 . 0.1
另外，推荐给redis设置密码，取消注释这一行：
requirepass foobared
foobared 即当前密码，可以自行修改
```

然后重启 服务，使用的命令如下：
systemctl restart redis 



编译安装：

https://redis.io/download

```
前提：
# yum -y install gcc tcl

[root@node201 ~]# curl -O -L http://download.redis.io/releases/redis-5.0.5.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1929k  100 1929k    0     0  14664      0  0:02:14  0:02:14 --:--:-- 26331

[root@node201 ~]# mv redis-5.0.5.tar.gz /opt/module
[root@node201 module]# tar xzf redis-5.0.5.tar.gz
hadoop-2.9.2.tar.gz  hadoop-3.1.2  jdk1.8.0_211  redis-5.0.5  redis-5.0.5.tar.gz

[root@node201 redis-5.0.5]# make

# 问题：fatal error: jemalloc/jemalloc.h: No such file or directory
make MALLOC=libc

[root@node201 redis-5.0.5] vi /etc/profile

export REDIS_HOME=/opt/module/redis-5.0.5
export PATH=$PATH:$REDIS_HOME/src

source /etc/profile
```



起服务：

```
redis-server  # 直接运行

utils目录下有个install_server.sh 可以直接安装，不用每次都启动

[root@node201 utils]# ./install_server.sh
Welcome to the redis service installer
This script will help you easily set up a running redis server

Please select the redis port for this instance: [6379]
Selecting default: 6379
Please select the redis config file name [/etc/redis/6379.conf]
Selected default - /etc/redis/6379.conf
Please select the redis log file name [/var/log/redis_6379.log]
Selected default - /var/log/redis_6379.log
Please select the data directory for this instance [/var/lib/redis/6379]
Selected default - /var/lib/redis/6379
Please select the redis executable path [/usr/local/bin/redis-server]
Selected config:
Port           : 6379
Config file    : /etc/redis/6379.conf
Log file       : /var/log/redis_6379.log
Data dir       : /var/lib/redis/6379
Executable     : /usr/local/bin/redis-server
Cli Executable : /usr/local/bin/redis-cli
Is this ok? Then press ENTER to go on or Ctrl-C to abort.
Copied /tmp/6379.conf => /etc/init.d/redis_6379
Installing service...
Successfully added to chkconfig!
Successfully added to runlevels 345!
Starting Redis server...
Installation successful!
```



起客户端：

```
[root@node201 utils]# redis-cli
127.0.0.1:6379> help
redis-cli 5.0.5
To get help about Redis commands type:
      "help @<group>" to get a list of commands in <group>
      "help <command>" for help on <command>
      "help <tab>" to get a list of possible help topics
      "quit" to exit

To set redis-cli preferences:
      ":set hints" enable online hints
      ":set nohints" disable online hints
Set your preferences in ~/.redisclirc
127.0.0.1:6379> help @string

  APPEND key value
  summary: Append a value to a key
  since: 2.0.0
```



### key

redis 的key值是二进制安全的，任何字符都转成二进制来存key