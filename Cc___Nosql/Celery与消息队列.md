---
title: Celery与消息队列
date: 2017-02-08 21:11:37
categories:
header-img:
tags: RabbitMQ
---



### Celery

#### 何为Celery

对于网站应用的缓慢操作时，我们拯救用户体验，尤其是在做一些复杂的数据库处理和图片应用时，可以用一个叫celery的任务队列工具，将这些操作移动到flask流程之外。

Celery是用python编写的任务队列工具，用python的多任务库来**并行**的执行任务。

这里我们可以把任务理解成我们定义的函数。

#### 特点

消息队列可以理解成数据结构中的队列，在生产者和消费者模型中可以理解成仓库，

当生产者生产出产品时会通知消费者去队列里拿最新的消息，而不是让消费者不停的与消息队列联系。类似ajax和webSocket的区别，ajax会反复的与服务器通信，而后者依赖于监听，基于持续的数据流。

也可用nosql键值数据库来代替消息队列，处理较大的负载，还能将消息持久化。



### RabbitMQ

### 下载与安装

#### windows 

需要下载两个运行文件

* rabbitMQ [http://www.rabbitmq.com/download.html](http://www.rabbitmq.com/download.html)
* erlang：http://www.erlang.org/download.html

abbitMQ安装，查看安装文档：[http://www.rabbitmq.com/install-windows.html](http://www.rabbitmq.com/install-windows.html)

安装ERLANG，下载完成ERLANG后，直接打开文件下一步就可以安装完成了，安装完成ERLANG后再回过来安装RABBITMQ

在安装的文件夹里就能找到启动



启动的时候有可能碰到这个问题。

error:node with name "rabbit" already running on "xxx"



停一下重启。

安装界面管理插件：

在D:\software\RabbitMQ Server\rabbitmq_server-3.6.6\sbin进入cmd.输入：

`rabbitmq-plugins enable rabbitmq_management`

可以通过访问http://localhost:15672进行测试，默认的登陆账号为：guest，密码为：guest。