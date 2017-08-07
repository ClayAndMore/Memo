---
title: CentOS7-python2和3及pip等安装问题
date: 2017-03-18 14:54:28
categories:
header-img: python
tags: python
---

这两天申请了一个云服务器，用的centOS,自带python2.7.5没有pip,

为了做东西，更新了2.7到最新版本。装了python3.5,以及两个版本的pip,很繁琐，下面总结下：

### python 系统自带2.7升级到最新2.7.x

下载python2.7.x:

到官网 

`wget + 包的地址`

解压包 ；tar

进入解压目录

安装：`./config`

`make`

`make install`

看python版本信息`python -V`,此时还是旧版本

先把原来的python文件更名

`mv /usr/bin/python /usr/bin/python2.7.5`

建立软链接,使系统默认是python最新版：

` ln -s /usr/local/bin/python2.7 /usr/bin/python`

重新检测python版本

解决yum的python版本，它是根据系统自带旧版的python：

`vi /usr/bin/yum`

将头部的

`#!/usr/bin/python`改为`#! /usr/bin/python2.7.5`也就是刚才你改的那个旧版的文件名。



到`vi /usr/libexec/urlgrabber-ext-down`
把头部的python改成和/usr/bin/yum中一样的

如果是centos6就没有这一步.yum出现File` "/usr/libexec/urlgrabber-ext-down", line 22, in <module>`的错误就是这里的问题



### python2.7安装pip

到官网去下载，

https://pip.pypa.io/en/stable/installing/

它会提供一个get-pip文件：

`wget https://bootstrap.pypa.io/get-pip.py`

运行`python get-pip.py`

它会下载pip和setuptools。pip依赖setuptools.

这期间可能因为网络问题崩掉，换时间多试几次吧。



### python2和python3共存

#### ubuntu

一般linux系统中自带python2，ubuntu下可用apt安装python3:

`sudo apt-get install python3`

##### 同一文件

用py2运行：

`python2 hello.py`

用py3运行：

`python3 hello.py`

如果每次运行都要加入参数-2/-3比较麻烦的，更简单的方法是我们在编写代码时就在代码头部加入说明，表明这个文件应该是由python2解释运行，还是由python3解释运行。说明的方法是在代码文件的最开始加入一行

```
#! python2
# -*- coding: utf-8 -*-12
```

或者

```
#! python3
# -*- coding: utf-8 -*-12
```

分别表示该文件使用Python2或者Python3解释运行。这样，运行时就可以简化为

```
py hello.py
```



##### 分别安装pip

`sudo apt-get install python2-pip`

`sudo apt-get install python3-pip`



##### 分别使用pip

同理根据需求选择性的使用

```
python2 -m pip install xxxx1
```

`sudo pip2 install packagename`

或者

```
python3 -m pip install xxxx
```

`sudo pip3 install packagename`



#### centos

下载python3:

`wget +官网地址`:`wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3rc1.tar.xz`

解压：

`tar xf Python-3.5.3.tar.xz`

进入目录：

`cd Python-3.5.3.tar.xz`

配置，编译，安装：

`./configure`

`make`

`make install`

ok~

### pip共存

![](http://ojynuthay.bkt.clouddn.com/pip2andpip3.png)

