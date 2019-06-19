tags:[消息队列, nosql, database, Redis]

## Redis

Red is 是一个基于内存的高效的非关系型数据库, C语言实现。
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



### 持久化

因为为内存数据存储，需要将内存的数据持久化

方式：

#### RDB

RDB(Redis DB) 类似与hdfs,fsimage

将内存中的数据库快照保存在名字为dump.rdb的二进制文件中。

方式：

时点操作， 比如8点一次，10点一次，有可能数据丢失掉。

阻塞方式：先停服，客户端执行save

非阻塞方式：redis服务正常接受客户端请求，redis会fork出一个新的子进程来创建RDB文件，子进程处理完后会通知父进程。  父进程用新的dump.rdb文件代替旧的

命令： bgsave

cow,  copy on write 写时拷贝

```
+--------+
|        |
| 40G    |
|        |
| aaa:20 | fork            +-----------+
|        +-----------------+  aaa:10   |
|        |   copy on write |           |
|        |       +---------+-----------+
|        +-------------+
|        |       |     |
+--------+  +--+-v--+--v-+--+-------+
            |  |    |    |  | 物理地址 |
            +--+----+----+--+-------+
```

开始时，aaa为10， 持久化时fork出一个子进程，子进程做持久化的工作，此时又将aaa改为20, aaa不会在用原来的地址，而是新开一块空间存20，之前的值让持久化的进程来用。实质上是指针的操作。



自动执行：

默认配置

save 900 1

save 300 10

save 60 100000

save其实就是bgsave, 三个触发条件，60秒内有10万次增删改查 or 300s内有10次 or 900s内 有一次， 触发一次全部清零。



RDB优点和缺点：

优点：

* 完全备份，不同的数据集备份可以做到多版本恢复
* 紧凑的单一文件，方便网络传输，适合灾难恢复
* 恢复大数据集速度教AOF快

缺点：

* 会丢失最近写入、修改的而未能持久化的数据
* fork过程非常耗时，会造成毫秒级不能响应客户端请求

生产环境：

* 创建一个定时任务cron job,每小时或没天将dump.rdb复制到指定目录
* 确保备份文件名称带有日期时间信息，便于管理和还原对应的时间点快照版本
* 定时任务删除过期的备份
* 如果有备用，跨物理主机，跨机架，异地备份。



#### AOF

AOF(AppendOnlyFile) 相当于 hdfs的edit logs。

* 采用追加的方式保存
* 默认文件 appendonly.aof
* 记录所有的写操作命令，使用这些命令就可以还原数据库

写入机制：

在常见操作系统中，写入文件时，系统调用write函数，为了提高效率，减小和硬盘的交互，系统同城不会直接讲内容写入到硬盘里面，而是先将内容放入一个内存缓冲区(buffer)里面，等到缓冲区被填满，或者用户执行fsync和fdatasync调用才将缓冲区里的真正内容写入到硬盘里，未写入之前，数据可能丢失。

写入策略：

appendfsync选项: always, everysec 或 no

always,每次写操作都要写入硬盘，这样不容易丢失数据。但是影响效率

everysec, 每秒一次写入磁盘，最多丢失一秒的数据量。

no， 不主动调用，最多丢失一个buffer的量，关键看缓冲区设置的大小。

AOF重写机制

当AOF文件特别大的时候，比如十年第一次关机，要恢复数据，需要等很久。

AOF重新机制就是尽量记录少的操作：

| 原有**AOF**文件              | 重写后的**AOF**文件                   |
| ---------------------------- | ------------------------------------- |
| SELECT 0                     | SELECT 0                              |
| SADD fruits “apple”          | SADD fruits “apple” “banana” “cherry” |
| SADD fruits “banana”         | SET msg “hello world again!”          |
| SADD fruits “cherry”         | RPUSH lst 3 5 7                       |
| SET msg “hello world”        |                                       |
| SET msg “hello world again!” |                                       |
| RPUSH lst 1 3 5              |                                       |
| RPUSH lst 7                  |                                       |
| LPOP lst                     |                                       |



上述的重写过程：

* fork 个子进程负责重写AOF文件 

* 子进程会创建一个临时文件写入 AOF信息 

* 父进程会开辟一个内存缓冲区接收新的写命令

* 进程重写完成后，父进程会获得一个信号，将父进程接收到的新的写操作由子进程写
     到临时文件中
     
* 新文件替代旧文件 
  

注:如果写 操作的时候出现故障导致命令写半截，可以使 redis-check-aof 具修复 



重写触发：

手动:客户端向服务端发送BGREWRITEAOF命令 

动:配置文件中的选项， 手动执 BGREWRITEAOF命令 

* auto-aof-rewrite-min-size <size>，触发AOF重写所需的最小体积:只要在AOF文件的体积大于等于size时，才会考虑是否需要进行AOF重写，这个选项用于避免对体积过小的AOF文件进行重写 

* auto-aof-rewrite-percentage <percent>，指定触发重写所需的AOF文件体积百分比: 当AOF文件的体积大于auto-aof-rewrite-min-size指定的体积，并且超过上 次重写之后的 AOF文件体积的percent %时，就会触发AOF重写。(如果服务器刚刚启动不久，还没有进行过 AOF重写，那么使用服务器启动时载入的AOF 件的体积来作为基准值)。将这个值设置为0表示关闭自动AOF重写 



优缺点：

* 写入机制，默认fysnc每秒执 ，性能很好不阻塞服务，最多丢失1秒的数据 

* 重写机制，优化AOF文件 

* 如果误操作 (FLUSHALL等)，只要AOF未被重写，停止服务移除AOF文件尾部的 FLUSHALL命令，重启Redis，可以将数据集恢复到 FLUSHALL 执 之前的状态 

缺点

* 相同数据集，AOF文件体积较RDB大了很多 

* 恢复数据库速度较RDB慢( 文本，命令重演) 

