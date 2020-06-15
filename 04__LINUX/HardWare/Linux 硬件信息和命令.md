
---
title: "Linux 硬件信息和命令.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux]

## Linux 硬件信息和命令

### 磁盘

#### 查看磁盘容量-df

`$ df -h`

加上参数-h是以更易读的方式展示，以兆或者g来显示。

#### 查看目录容量 du

`$ du -h`

`$ du -h --max-depth 0` 只看一级目录的信息

`$ du -h --max-depth 1`只看二级目录的信息

`du -h --max-depth=0 ./log`  看某个文件夹的大小



#### 分区

`sudo fdisk l` 可看磁盘情况

`sudo fdisk sdb`对sdb进行分区，接下来会提示你按下m获得详细帮助



#### fdisk

fdisk -l

可以查看硬盘和分区的详细信息



#### 格式化（创建文件系统）

在linux中把格式化叫创建文件系统

`sudo mkfs -t ext3 /dev/sdb1`

t指格式化的类型type为ext3,后面为指定分区

#### 挂载

没挂载的会显示黄色，代表块文件，需要挂载将其编成目录

`mount -t ext3 /dev/sdb1 /mnt/sdb`

将sdb1 挂载成mnt的sdb,

`mount sdb`常看sdb的挂载信息

#### 卸载

`unmount mnt/sdb`



#### RAID

容错廉价磁盘队列，将多个较小磁盘来扩展服务器的容量，不只是为了存储数据，还为了保护数据。

根据实现方式，RAID有几个等级：

* RAID-0（等量模式）：性能最佳

  就是说数据存储的时候分成几个和磁盘数量相等的份数，比如有个100M的文件，用5块磁盘来存储数据，那么每块盘将分得20M，存文件时将会循环遍历每块盘，如果小的盘慢了就存大的。

  显然，这种方式，一旦有一块磁盘坏掉了，其他磁盘的数据也恢复不出来原本的文件。

* RAID-1 (映像模式)：完整备份。

   两份同样的磁盘，数据在存储的时候会一块盘会完全备份，比如上面的100M的文件，100M存一份磁盘，再用相同的另一份磁盘来存备份这100M,总共用了200M的容量。

  显然这种方式虽然保证了数据的恢复性，但是牺牲掉太多空间了。

* RAID 0+1 , RAID 1+0

  上面两种方式的结合，比如现在有现在有四份盘：ABCD

  0+1: A+B，C+D组成RAID 0,  然后将两份RAID0 组成RAID1

  1+0:  A+B,  C+D组成RAID 1,  然后将两份RAID0 组成RAID0

* RAID 5: 性能和备份的均衡考虑

  至少三块盘能实现，两块盘组成RAID-0的模式，不过在存储数据的时候会存同位检查码，如果有一块坏掉了可以用这个检查码来恢复数据，另一块做空着，当有磁盘坏掉了自动替换坏的磁盘，数据也会因为检查码来恢复到这个磁盘上。

  但是只能支持一块坏掉的盘，如果支持坏掉两块盘就是另一种模式RAID 6.

  如果盘坏掉，还得手动安装，停掉服务等，有一种自动回复的方式就是用Spare Disk,它在磁盘阵列中，但是平时 不会用，只有某块磁盘坏掉的时候，它会自动替换磁盘。

#### 软硬件RAID

上面说了一堆，这种磁盘管理方式是好，但是明显是硬件上的区分，是的，但是这种盘太贵了。。

所以说通过软件来实现这种逻辑。

我们的Centos提供的这种软件为mdadm.

它以分区和磁盘为单位，也就是说我们不需要多块硬盘，只要有两个分区以上就可以实现软件磁盘阵列了。

在系统中/dev/sd[a-p]标识的为硬件磁盘阵列

/dev/md[数字]  为软件磁盘阵列



#### 修改machine-id

``` sh
# 原来的machine-id
cat /etc/maichine-id
# 删掉
rm /etc/machine-id

# 重新生成：
systemd-machine-id-setup

# 确认是否改变：
cat /etc/machine-id
```






### 内存

​      查看内存：`free `   

      [root@bogon img]# free -g
    
                 total       used       free     shared    buffers     cached
    
    Mem:            31         19         11          1          0         10
    
    -/+ buffers/cache:          9         22
    
    Swap:            0          0          0


解释下内存的组成：

![](http://ojynuthay.bkt.clouddn.com/linux%E5%86%85%E5%AD%98.png)





​     shared: 多个进程共享的内存总额

​     `- buffers/cache` : 程序实际吃掉的内存, 第二行used

​    `+ buffers/cache` :  可挪用的内存, 第二行free, 这里值得留意，它是能够回收的，**它是机器真正可用内存**

​     图中：

```
cached + buffers + free = + buffers/cache  
1482   + 36      + 826   =  2344
```



​     内存有物理内存和虚拟内存之说，物理内存是什么自然无需解释，虚拟内存实际是物理内存的抽象，多数情况下，出于方便性的考虑，程序访问的都是虚拟内存地址，然后操作系统会把它翻译成物理内存地址。
很多人会把虚拟内存和Swap混为一谈.



#### Swap

实际上Swap只是虚拟内存引申出的一种技术而已：操作系统一旦物理内存不足，为了腾出内存空间存放新内容，就会把当前物理内存中的内容放到交换分区里，稍后用到的时候再取回来，需要注意的是，Swap的使用可能会带来性能问题，偶尔为之无需紧张，糟糕的是物理内存和交换分区频繁的发生数据交换，这被称之为Swap颠簸，一旦发生这种情况，先要明确是什么原因造成的，如果是内存不足就好办了，加内存就可以解决，不过有的时候即使内存充足也可能会出现这种问题，



#### buffer和cache

对于操作系统来说：

```
buffer（缓冲）是为了提高内存和硬盘（或其他I/O设备）之间的数据交换的速度而设计的。 cache（缓存）是为了提高cpu和内存之间的数据交换速度而设计的，也就是平常见到的一级缓存、二级缓存
```

对于linux系统来说：free命令会显示buffers和cached

buffers与cached都是内存操作，用来保存系统曾经打开过的文件以及文件属性信息，这样当操作系统需要读取某些文件时，会首先在buffers 与cached内存区查找。

　　buffers是用来缓冲块设备做的，它只记录文件系统的元数据（metadata）以及 tracking in-flight pages，而cached是用来给文件做缓冲。

更通俗一点说：buffers主要用来存放目录里面有什么内容，文件的属性以及权限等等。而cached直接用来记忆我们打开过的文件和程序。Linux都会尽可能的把文件缓存到内存里，这样下次访问的时候，就可以直接从内存中取结果，所以cached一栏的数值非常的大，不过不用担心，这部分内存是可回收的，操作系统会按照LRU算法淘汰冷数据。

所以一般cache会比较大。


一些参数：

-b 　以Byte为单位显示内存使用情况。

-k 　以KB为单位显示内存使用情况。

-m 　以MB为单位显示内存使用情况。

-g   以GB为单位显示内存使用情况。

-o 　不显示缓冲区调节列。

-s<间隔秒数> 　持续观察内存使用状况。

-t 　显示内存总和列。

-V 　显示版本信息



#### /proc/meminfo

查看内存详细使用：

```
cat /proc/meminfo
MemTotal:        4020868 kB
MemFree:          230884 kB
Buffers:            7600 kB
Cached:           454772 kB
SwapCached:          836 kB
```



#### 硬件信息

```
dmidecode -t memory
SMBIOS 2.7 present.
Handle 0x0008, DMI type 16, 23 bytes
Physical Memory Array
    Location: System Board Or Motherboard
....
    Maximum Capacity: 32 GB
....
Handle 0x000A, DMI type 17, 34 bytes
....
Memory Device
    Array Handle: 0x0008
    Error Information Handle: Not Provided
    Total Width: 64 bits
    Data Width: 64 bits
    Size: 4096 MB
.....
我的主板有4个槽位，只用了一个槽位，上面插了一条4096MB的内存。
```





### CPU

#### lscpu

lscpu命令，查看的是cpu的统计信息.

```
blue@blue-pc:~$ lscpu
Architecture:          i686          #cpu架构
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian   #小尾序
CPU(s):                4            #总共有4核
On-line CPU(s) list:   0-3
Thread(s) per core:    1              #每个cpu核，只能支持一个线程，即不支持超线程
Core(s) per socket:    4               #每个cpu，有4个核
Socket(s):             1              #总共有1一个cpu
Vendor ID:             GenuineIntel    #cpu产商 intel
CPU family:            6
Model:                 42
Stepping:              7
CPU MHz:               1600.000
BogoMIPS:              5986.12
Virtualization:        VT-x             #支持cpu虚拟化技术
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              6144K
```

#### /proc/cpuinfo

查看/proc/cpuinfo,可以知道每个cpu信息，如每个CPU的型号，主频等。

```
cat /proc/cpuinfo
processor    : 0
vendor_id    : GenuineIntel
cpu family    : 6
model        : 42
model name    : Intel(R) Core(TM) i5-2320 CPU @ 3.00GHz
.....
上面输出的是个cpu部分信息，还有3个cpu信息省略了。
```

更多看进程信息的top命令。

### 网卡

网卡配置文件：`/etc/sysconfig/network-scripts`



#### ifconfig

查看所有网卡： ifconfig -a .

查看某个网卡： ifconfig eth1



#### ip link show



#### 查看某网卡的口是否有线连接：

1. `ethtool eth1`

   最后一行： Link detected: yes为正常no为失败

2. 或 `mii-tool` 用的少，有的驱动不支持。

3. ```
   /mnt/wifi$ cat /proc/net/dev

   Inter-|  Receive                                                | Transmit

   face |bytes  packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carriercompressed

   lo:      0      0    0  0    0    0        0        0        0      0    0    0  0    0      0        0

   eth0:    3439    15  0  0    0    0        0        0        0      0    0    0  0    0      0          0

   在开发板上/proc/net目录下，还有很多关于网络的信息的文件，我试了不少，觉得这个还算准确，但并非100%哦，如果启动开发板后，eth0中bytes、packets 不为0，那它一定插了网线，但此种方法只适合开机启动时判断，之后的话，就很麻烦了。
   ```

   

确定某网卡的具体物理口， 用：

`ethtool -p eth2`  时，对应网卡会闪烁， 注意此时是未插网线。



关闭 / 开启 / 重启 某块网卡：

`ifdown eth0 && ifup eth0       # 一定要连在一起使用！！切记啊  `

重启所有网卡服务：

`/etc/init.d/network restart`





#### 创建虚拟网卡

```
cd /etc/sysconfig/network-scripts
mv
```





### BOIS

`dmiencode`



