---
title: "select.md"
date: 2019-11-18 17:54:22 +0800
lastmod: 2019-11-18 17:54:22 +0800
draft: false
tags: [""]
categories: ["python web"]
author: "Claymore"

---


所有的socket方法都会阻塞， 例如， 当程序从一个socket里读或写它的时候程序本身阻塞，一种可行解决方案是让客户端分离线程，但交换两个线程的信息是开销高的操作。

为解决这个问题，有一些所谓的异步方法。

主要思想是授权操作系统维护socket的状态， socket有读写时，让操作系统通知程序



不同的操作系统有一些接口：

* Linux:  poll, epoll
* BSD : kqueue, kevent 
* 跨平台： select

BSD是Unix的衍生系统， 要求要保证其数据的掉电安全性,所以用同步写的方式,速度更慢 



`readable, writable, exceptional = select.select(rlist, wlist, xlist, [timeout])`



 这是Unix select（）系统调用的直接接口。



* 前三个参数是“可等待对象”的序列 , 可以是socket 或 文件。

  我们调用select.select来要求操作系统检查给定的套接字是否准备好写入，读取，或者是否分别有一些异常。

  这就是为什么它传递了三个套接字列表来指定哪个套接字预期是

  可读的(rlist)，可写的(wlist),  哪些应该检查错误(xlist).

* timeout

  如果不传递timeout参数将会阻塞程序， 直到有一个文件描述符就绪。

  timeout要求传递浮点数， 单位为秒。

  为0时，不会阻塞，一直轮询。

* 返回值

  返回传入对象的list，如 ：

  `[socket1_back,], [], [] = select.select([socket1], [],  [])`




create a server using `select` , example:

```python
import select, socket, sys, Queue
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0) #非阻塞，注意这里
server.bind(('localhost', 50000))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
```



