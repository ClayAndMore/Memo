---
title: windows一些快捷键和命令
date: 2016-07-06 09:42:13
categories: windows
tags: [windonws,命令与快捷键]
---

### 查看自己DirectX版本的方法是：

    点“开始”、“运行”，在“运行”里输入“dxdiag”回车，
    弹出DirectX 诊断工具窗口，就在首页中，有很多系统信息，

### 新建文件夹快捷键 

`ctrl+shift+n`

### 启动服务 

运行-》services.msc

<!-- more -->

### 注册表 regedit 

 ### Win10定时关机命令：

`shutdown –s –t 3600`

### 当面目录直接进入cmd

打开文件后，在空白处按住shift+右键->在此处打开命令窗口

### 开机启动

win+r msconfig ->启动 可以关闭开机启动项 （ms 微软）

### 画图

win+r mspaint

### MD5

﻿MD5即Message-Digest Algorithm 5（信息-摘要算法5），用于确保信息传输完整一致。是计算机广泛使用的杂凑算法之一（又译[摘要算法](http://baike.baidu.com/view/10961371.htm)、[哈希算法](http://baike.baidu.com/view/273836.htm)），主流编程语言普遍已有MD5实现。将数据（如汉字）运算为另一固定长度值，是杂凑算法的基础原理，MD5的前身有MD2、[MD3](http://baike.baidu.com/view/2535629.htm)和[MD4](http://baike.baidu.com/view/444142.htm)。让大容量信息在用[数字签名](http://baike.baidu.com/view/7626.htm)软件签署私人[密钥](http://baike.baidu.com/view/934.htm)前被"[压缩](http://baike.baidu.com/subview/786588/12546221.htm)"成一种保密的格式（就是把一个任意长度的字节串变换成一定长的[十六进制](http://baike.baidu.com/view/230306.htm)数字串）。除了MD5以外，其中比较有名的还有[sha-1](http://baike.baidu.com/view/94209.htm)、[RIPEMD](http://baike.baidu.com/view/260854.htm)以及Haval等。

一种图标快捷方式

如果想长期使用，可以创建一个文本文档，将**slidetoshutdown（或者其他cmd口令）**输入进去，并将文本文档的txt后缀改成cmd，关机的时候点击就行了。

### 批量重命名

假如我们要修改D盘A文件夹下的所有文件扩展名，并且全部都改为jpg，那么我们可以使用以下命令：
　　ren D:\A\* *.jpg
　　当然，有时候我们可能只需要修改某一类型（同一扩展名）的文件，比如所有bmp文件全部改为jpg，则使用下列命令：
　　ren D:\A\*.bmp *.jpg
　　最后，在给大家一个小技巧。这需要将下面命令复制到新建文本中并保存文件为“修改扩展名.bat”：
　　cd /d %~dp0
　　ren * *.jpg
　　（其中jpg为我们想要修改的扩展名，可根据需要修改）

### 刷新dns

`ipconfig /flushdns`