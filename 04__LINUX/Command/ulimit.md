
---
title: "ulimit.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
ulimit 用于限制 shell 启动进程所占用的资源，支持以下各种类型的限制：

* 所创建的内核文件的大小
* 进程数据块的大小
* Shell 进程创建文件的大小
* 内存锁住的大小
* 常驻内存集的大小
* 打开文件描述符的数量
* 分配堆栈的最大大小
* CPU 时间
* 单个用户的最大线程数
* Shell 进程所能使用的最大虚拟内存。
* 同时，它支持硬资源和软资源的限制。



### 使用ulimit

ulimit 命令的格式为：`ulimit [options] [limit]`

| 选项 [options] | 含义                                                     | 例子                                                         |
| :------------- | :------------------------------------------------------- | :----------------------------------------------------------- |
| -H             | 设置硬资源限制，一旦设置不能增加。                       | ulimit – Hs 64；限制硬资源，线程栈大小为 64K。               |
| -S             | 设置软资源限制，设置后可以增加，但是不能超过硬资源设置。 | ulimit – Sn 32；限制软资源，32 个文件描述符。                |
| -a             | 显示当前所有的 limit 信息。                              | ulimit – a；显示当前所有的 limit 信息。                      |
| -c             | 最大的 core 文件的大小， 以 blocks 为单位。              | ulimit – c unlimited； 对生成的 core 文件的大小不进行限制。  |
| -d             | 进程最大的数据段的大小，以 Kbytes 为单位。               | ulimit -d unlimited；对进程的数据段大小不进行限制。          |
| -f             | 进程可以创建文件的最大值，以 blocks 为单位。             | ulimit – f 2048；限制进程可以创建的最大文件大小为 2048 blocks。 |
| -l             | 最大可加锁内存大小，以 Kbytes 为单位。                   | ulimit – l 32；限制最大可加锁内存大小为 32 Kbytes。          |
| -m             | 最大内存大小，以 Kbytes 为单位。                         | ulimit – m unlimited；对最大内存不进行限制。                 |
| -n             | 可以打开最大文件描述符的数量。                           | ulimit – n 128；限制最大可以使用 128 个文件描述符。          |
| -p             | 管道缓冲区的大小，以 Kbytes 为单位。                     | ulimit – p 512；限制管道缓冲区的大小为 512 Kbytes。          |
| -s             | 线程栈大小，以 Kbytes 为单位。                           | ulimit – s 512；限制线程栈的大小为 512 Kbytes。              |
| -t             | 最大的 CPU 占用时间，以秒为单位。                        | ulimit – t unlimited；对最大的 CPU 占用时间不进行限制。      |
| -u             | 用户最大可用的进程数。                                   | ulimit – u 64；限制用户最多可以使用 64 个进程。              |
| -v             | 进程最大可用的虚拟内存，以 Kbytes 为单位。               | ulimit – v 200000；限制最大可用的虚拟内存为 200000 Kbytes。  |



### 使用方式

#### 用户启动脚本

如果用户使用的是 bash，就可以在用户的目录下的 .bashrc 文件中，加入 ulimit – u 64，来限制用户最多可以使用 64 个进程。此外，可以在与 .bashrc 功能相当的启动脚本中加入 ulimt。	



#### 应用程序启动脚本

如果用户要对某个应用程序 myapp 进行限制，可以写一个简单的脚本 startmyapp。

```
ulimit – s 512 
myapp
```

以后只要通过脚本 startmyapp 来启动应用程序，就可以限制应用程序 myapp 的线程栈大小为 512K。



### 作用范围

**ulimit 限制的是当前 shell 进程以及其派生的子进程**。

举例来说，如果用户同时运行了两个 shell 终端进程，只在其中一个环境中执行了 ulimit – s 100，则该 shell 进程里创建文件的大小收到相应的限制，而同时另一个 shell 终端包括其上运行的子程序都不会受其影响



#### `/etc/security/limits`

是否有针对某个具体用户的资源加以限制的方法呢？答案是有的，方法是通过修改系统的 /etc/security/limits 配置文件。该文件不仅能限制指定用户的资源使用，还能限制指定组的资源使用。该文件的每一行都是对限定的一个描述，格式如下:

``<``domain``> <``type``> <``item``> <``value``>``

* domain 表示用户或者组的名字，还可以使用 * 作为通配符。

* Type 可以有两个值，soft 和 hard。I
* tem 则表示需要限定的资源，可以有很多候选值，如 stack，cpu，nofile 等等，分别表示最大的堆栈大小，占用的 cpu 时间，以及打开的文件数。通过添加对应的一行描述，则可以产生相应的限制。

例如：

`* hard noflle 100`

该行配置语句限定了任意用户所能创建的最大文件数是 100。

现在已经可以对进程和用户分别做资源限制了，看似已经足够了，其实不然。很多应用需要对整个系统的资源使用做一个总的限制，这时候我们需要修改 /proc 下的配置文件。/proc 目录下包含了很多系统当前状态的参数，例如 /proc/sys/kernel/pid_max，/proc/sys/net/ipv4/ip_local_port_range 等等，从文件的名字大致可以猜出所限制的资源种类



#### 永久设置 `ulimit -n 65535`

/etc/security/limits.conf:

```
*    soft    nofile 8192
*    hard    nofile 8192
```







参考： https://www.ibm.com/developerworks/cn/linux/l-cn-ulimit/



