---
title: "celery.md"
date: 2019-11-09 17:48:25 +0800
lastmod: 2019-11-09 17:48:25 +0800
draft: false
tags: [""]
categories: ["队列"]
author: "Claymore"

---
### 异步任务

异步任务是web开发中一个很常见的方法。对于一些耗时耗资源的操作，往往从主应用中隔离，通过异步的方式执行。如，做一个注册的功能，在用户使用邮箱注册成功之后，需要给该邮箱发送一封激活邮件。如果直接放在应用中，则调用发邮件的过程会遇到网络IO的阻塞，比好优雅的方式则是使用异步任务，应用在业务逻辑中触发一个异步任务。

实现异步任务的工具有很多，其原理都是使用一个任务队列，比如使用redis生产消费模型或者发布订阅模式实现一个简单的消息队列。

除了redis，还可以使用另外一个神器---Celery。

Celery是一个异步任务的调度工具。它是Python写的库，但是它实现的通讯协议也可以使用ruby，php，javascript等调用。

异步任务除了消息队列的后台执行的方式，还是一种则是跟进时间的计划任务。

 它是一个分布式队列的管理工具，我们可以用 Celery 提供的接口快速实现并管理一个分布式的任务队列。 



### broker /worker/ backend

 broker是一个消息传输的中间件, 中文意思为中间人，在这里就是指任务队列本身.

woker:  就是 Celery 中的工作者，类似与生产/消费模型中的消费者，其从队列中取出任务并执行 .

每当应用程序调用celery的异步任务的时候，会向broker传递消息，而后celery的worker将会取到消息，进行对于的程序执行。

Celery 扮演生产者和消费者的角色，brokers 就是生产者和消费者存放/拿取产品的地方(队列) .

backend:

通常程序发送的消息，发完就完了，可能都不知道对方时候接受了。为此，celery实现了一个backend，用于存储这些消息以及celery执行的一些消息和结果。

对于 brokers，官方推荐是rabbitmq和redis，至于backend，就是数据库啦。为了简单起见，可以都用redis。





 https://zhuanlan.zhihu.com/p/22304455?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io 