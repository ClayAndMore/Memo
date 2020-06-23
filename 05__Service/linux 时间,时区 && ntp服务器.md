
---
title: "linux 时间,时区 && ntp服务器.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "linux 时间,时区 && ntp服务器.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux, linux_software]

## 时间

linux的时间标准

**GMT时区：**

​      因为全球每个地方都有自己的习惯（根据早期太阳调整的时间，比如都是早上六点起床），

将全球以纬度为零的地点在英国格林尼治的为标准时间（24时区中的零区，以左为东时区，右为西时区），

即标准时间GMT(Greenwich Mean Time), 北京时间为东八区（GMT+8), 会比GMT快8个小时。

**UTC 时区：**

​	 地球周转轨道是椭圆，自传速度好像逐年变慢，所以GMT时间不是很准确。

最准确是原子震荡周期所计算的物理时钟 即UTC.

bois 就是用这种计算时间的芯片。

这种芯片之间会有差异，温度，制作误差等等，所以我们还是需要时间统一。



###  CST

四个不同时区的缩写：

1. Central Standard Time (USA) UT-6:00   美国标准时间
2. Central Standard Time (Australia) UT+9:30  澳大利亚标准时间
3. China Standard Time UT+8:00     中国标准时间
4. Cuba Standard Time UT-4:00     古巴标准时间



作者：维仔_411d
链接：https://www.jianshu.com/p/735e8444cdda
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



### linux 时钟管理

软件时钟： linux操作系统个根据1970/01/01/开始计算的总秒数。（命令： `date +%s`)

硬件时钟： bios中的时钟芯片记录的时间。

用于硬件时钟和标准的UTC时钟多多少少存在差异, 我们一定会需要同步时间。



### 时间修改

软件时钟： 

```shell
date MMDDhhmmYYYY
# eg: 修改为 2018年3月3 16：22 
date 030316222018

# 时间设定成2009年5月10号的命令：
date -s 05/10/2009`

# 系统时间设定成下午14点30分59秒：
date -s 14:30:50

# 日期加时间
date -s “2016-05-18 12:00:00”
```

硬件时钟：

```shell
# 查看当前硬件时钟
hwclock

# 硬件时钟 同步系统时间
 hwclock --hctosys
 
 # 或者
 hwclock：硬件时钟
-w：同步系统时间到硬件时间
-s：同步硬件时间到系统时间
```

每次linux重启，系统时间会从BIOS中重新读出来，所以BIOS才是重要的时间依据。



### 时区修改

```
 ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```





## NTP 服务器

计算机内部所记录时钟是于BIOS(CMOS)内的， 如果它的电池没电了或被清除了等会导致时间不准。

NTP(Network Time Protoco) 网络时间协议就是通过网络来对准时间的。





### NTP 通信协议

Network Time Protocol

国内授时中心服务器（210.72.145.44） 去国际服务器同步时间，国内各大高校再去国内同步。



使用UDP 以123 为连接端口

#### 客户端 ntpdate

去一个服务器同步本地时间：

```
/usr/sbin/ntpdate pool.ntp.org
26 Mar 14:26:09 ntpdate[20304]: step time server 5.79.108.34 offset -103.320653 sec
```

offset 显示了微调了多少，这里我们就减了103秒。

只是查看：

```
[root@bogon]# /usr/sbin/ntpdate -q pool.ntp.org
server 193.228.143.14, stratum 2, offset -0.026901, delay 0.30731
server 120.25.115.20, stratum 2, offset 0.014994, delay 0.06955
server 94.237.64.20, stratum 2, offset 0.032471, delay 0.41748
server 203.135.184.123, stratum 1, offset 0.029970, delay 0.39737
26 Mar 14:50:09 ntpdate[3195]: adjust time server 203.135.184.123 offset 0.029970 sec
```



#### 服务端 ntpd

服务端和客户端不能同时开启，用ntpd也能同步时间，不过是平滑处理，有间隔的一点点更改时间，而ntpdate是一下子更新成远端的时间。

安装： https://gist.github.com/AntonioPaternina/23e6fe53142e4489e6cb7924fb1457fc