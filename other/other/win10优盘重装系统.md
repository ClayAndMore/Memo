---
title: win10优盘重装系统
date: 2017-01-29 08:20:00
categories: windows
header-img:
tags: windows
---

### 写在前面

window系统有自带的恢复功能，但是系统文件遭到损坏会提示无法重置。这样：

![](http://ojynuthay.bkt.clouddn.com/%E9%87%8D%E7%BD%AE%E6%97%B6%E9%97%AE%E9%A2%98.jpg)

这样我们就需要用优盘做启动盘重装系统了。

### 准备工作

* 一个大于4g的空优盘

* 如果预装系统不是win10，必须采用GPT分区加uefi引导：进入磁盘管理（左下角右键）

  ![](http://ojynuthay.bkt.clouddn.com/gpt%E5%88%86%E5%8C%BA.jpg)

  ![](http://ojynuthay.bkt.clouddn.com/gpt%E5%88%86%E5%8C%BA.jpg)



* 到官网下载iso:https://www.microsoft.com/zh-cn/software-download/windows10下载工具，之后工具可选：![](http://ojynuthay.bkt.clouddn.com/%E5%AE%89%E8%A3%85%E4%BB%8B%E8%B4%A8.png)

一般我都是选第二个，下载一个iso系统镜像。



### 开始装机

* 将下好的iso整个解压到你的空优盘
* 将重做的电脑关机，插入优盘
* 开机快速按f12，每个厂商进入开机启动选项的设置不一样，要去查和自己相关的。
* 选优盘启动，删除原来的系统盘，或者所有磁盘（不要担心它的各种分区，直接删）：![](http://ojynuthay.bkt.clouddn.com/%E7%A3%81%E7%9B%98%E5%88%A0%E9%99%A4.jpg)
* 这里我选择安在驱动器1,空间足够，等待各项设置，完成安装。
* 安装后再次进入磁盘管理：![](http://ojynuthay.bkt.clouddn.com/%E5%AE%89%E8%A3%85%E5%AE%8C%E6%88%90.jpg)

这时，你的系统盘在c盘，在上图c盘右键，可以分区。、

到此结束。