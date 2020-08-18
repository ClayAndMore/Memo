---
title: "Tornado比较其他py_web.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Tornado"]
categories: ["python web"]
author: "Claymore"

---
## 谈Tornado相比于其他 python web 的差异

我们要从一个简单的http server 说起：

### http server

1. http server 使用http协议，http协议封装在tcp协议中。

2. 用socket 变成实现tcp协议的细节，跟语言无关：

   server端：

   1. 初始化socket 
   2. 绑定套接字到端口(bind)
   3. 监听端口(listen)
   4. 接受连接请求(accept)
   5. 通信(send/recv)
   6. 关闭连接(close)

   client端：

   1. 初始化 socket；
   2. 发出连接请求(connect)；
   3. 通信(send/recv)；
   4. 关闭连接(close)；

3. 客户端用浏览器就可实现

4. 服务端：

   ```python
   # coding: utf-8
   # server.py
   import socket
   HOST, PORT = '', 8888
   # 初始化
   listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   # 绑定
   listen_socket.bind((HOST, PORT))
   # 监听
   listen_socket.listen(1)
   print 'Serving HTTP on port %s ...' % PORT
   while True:
       # 接受请求
       client_connection, client_address = listen_socket.accept()
       # 通信
       request = client_connection.recv(1024)
       print request
       http_response = """
   HTTP/1.1 200 OK
   Hello, World!
   """
       client_connection.sendall(http_response)
       # 关闭连接
       client_connection.close()
   ```

   

### wsgi server

我们先看一张图：

![](http://ovolonhm1.bkt.clouddn.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20171121091755.png)



1. nginx 做为代理服务器：负责静态资源发送（js、css、图片等）、动态请求转发以及结果的回复；
2. uWSGI 做为后端服务器：负责接收 nginx 请求转发并处理后发给 Django 应用以及接收 Django 应用返回信息转发给 nginx；
3. Django 应用收到请求后处理数据并渲染相应的返回页面给 uWSGI 服务器。

各个流程中的含义。

* cgi: 通用网关接口，规定一个程序该如何与web服务器程序之间通信从而可以让这个程序跑在web服务器上。当然，CGI 只是一个很基本的协议，在现代常见的服务器结构中基本已经没有了它的身影，更多的则是它的扩展和更新。
  * 后来有FCGI(FastCGI): 提升了性能，但是这里不用
* wsgi :它是用在 python web 框架编写的应用程序与后端服务器之间的规范
* uWSGI:  是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。用于接收前端服务器转发的动态请求并处理后发给 web 应用程序。
* uwsgi:  是uWSGI服务器实现的独有的协议 ,用于前端服务器与 uwsgi 的通信规范.

这些协议都是扩展于cgi协议之上的。



我们要说的wsgi server就是实现了wsgi协议的服务器，那么就是上方的uWSGI。

它规定一个客户端application:

application 是一个接受接受两个参数`environ, start_response`的标准 wsgi app:

```
environ:          一个包含请求信息及环境信息的字典
start_response:   一个接受两个参数`status, response_headers`的方法
status:           返回状态码，如http 200、404等
response_headers: 返回信息头部列表
```

具体实现：

```python
def application(environ, start_response):    
	status = '200 OK'    
	response_headers = [('Content-Type', 'text/plain')]    
	start_response(status, response_headers)    
	return ['Hello world']
```

这样一个标准的 wsgi app 就写好了，虽然这看上去和我们写的 Django app、 tornado app 大相径庭，但实际上这些 app 都会经过相应的处理来适配 wsgi 标准



server : 这里代码写起来太长，说一下大体流程：

1. 初始化，建立套接字，绑定监听端口；
2. 设置加载的 web app；
3. 开始持续运行 server；
4. 处理访问请求（在这里可以加入你自己的处理过程，比如我加入了打印访问信息，字典化访问头部信息等功能）；
5. 获取请求信息及环境信息（`get_environ(self)`）；
6. 用`environ`运行加载的 web app 得到返回信息；
7. 构造返回信息头部；
8. 返回信息；

一个 wsgi server 的重要之处就在于用`environ`去跑 web app 得到返回结果这一步，这一步和前面的 application 实现相辅相成，然后框架和服务器都根据这套标准，大家就可以愉快的一起工作了。



### Django WSGI server

Django本身很庞大复杂，但是server也是继承于（WSGIServer)



### Tornado WSGI

tornado 直接从底层用 epoll 自己实现了 事件池操作、tcp server、http server，所以它是一个完全不同的异步框架，但 tornado 同样也提供了对 wsgi 对支持，不过这种情况下就没办法用 tornado 异步的特性了。

与其说 tornado 提供了 wsgi 支持，不如说它只是提供了 wsgi 兼容，tornado 提供两种方式：

体现tornado特性的 tornado server：

#### WSGIContainer

tornado server做底层，其他应用如django做app.



兼容wsgi的 wsgi server:

#### WSGIAdapter:

将tornado应用改为符合标准的wsgi app 。



### epoll 特性

Tornado 用的内核i/o处理模型为epoll。

相比select,poll，严格来说epoll 也是轮询，只不过前者是将所有的流来轮询，而epoll是将活跃的流来轮询，如何知道活跃的流？在内核中就是中断机制，如果有多个io事件同时发生,epoll还是要通过轮询来处理的。

相比而言，直接处理活跃的流比轮询所有流找到活跃的流要节省不少时间。



### 单线程异步

Tornado本身是单线程的异步网络程序，它默认启动时，会根据CPU数量运行多个实例；充分利用CPU多核的优势。

网站基本都会有数据库操作，而**Tornado是单线程**的，这意味着如果数据库查询返回过慢，整个服务器响应会被堵塞。 数据库查询，实质上也是远程的网络调用；理想情况下，是将这些操作也封装成为异步的；但Tornado对此并没有提供任何支持。 这是Tornado的设计，而不是缺陷。 一个系统，要满足高流量；是必须解决数据库查询速度问题的！数据库若存在查询性能问题，整个系统无论如何优化，数据库都会是瓶颈，拖慢整个系统！ 
**异步**并不能从本质上提到系统的性能；它仅仅是避免多余的网络响应等待，以及切换线程的CPU耗费。 如果数据库查询响应太慢，需要解决的是数据库的性能问题；而不是调用数据库的前端Web应用。对于实时返回的数据查询，理想情况下需要确保所有数据都在内存中，数据库硬盘IO应该为0；这样的查询才能足够快；而如果数据库查询足够快，那么前端web应用也就无将数据查询封装为异步的必要。 就算是使用协程，异步程序对于同步程序始终还是会提高复杂性；需要衡量的是处理这些额外复杂性是否值得。如果后端有查询实在是太慢，无法绕过，Tornaod的建议是将这些查询在后端封装独立封装成为HTTP接口，然后使用Tornado内置的异步HTTP客户端进行调用。