
---
title: "从CGI 到 SWGI.md"
date: 2019-11-18 17:54:22 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "从CGI 到 SWGI.md"
date: 2019-11-18 17:54:22 +0800
lastmod: 2019-11-18 17:54:22 +0800
draft: false
tags: [""]
categories: ["python web"]
author: "Claymore"

---
tags:[web]

### web（http） 服务器

如果说Google Chrome、Mozilla Firefox、Microsoft IE 和 Opera 浏览器是最流行的一些 Web 客户端，

那么哪些是最常用的 Web 服务器呢？

这些包括 Apache、ligHTTPD、Microsoft IIS、LiteSpeed Technologies 等。。



### CGI

通用网关接口（Common Gateway Interface CGI）

Web 最初目的是在全球范围内对文档进行在线存储和归档（大多用于教学和科研）。这
些文件通常用静态文本表示，一般是 HTML。

这些静态 HTML 文档位于 Web 服务器上，在需要的时候会被发送到客户端。

随着因特网和 Web 服务的发展，除了浏览之外，还需要处理用户的输入。

Web 服务器不能处理表单中传递过来的用户相关的数据。

**这不是 Web 服务器的职责**，Web 服务器将这些请求发送给外部应用，将这些外部应用动态生成的
HTML 页面发送回客户端。

![](cgi)

为什么需要 CGI。

因为服务器无法创建动态内容，它们不知道用户特定的应用信息和数据，如验证信息、银行账户、在线支付等。

Web服务器必须与外部的进程通信才能处理这些自定义工作。

由于 CGI 有明显的局限性，以及限制 Web 服务器同时处理客户端的数量，因此 CGI 被
抛弃了。



### WSGI

Web 服务器网关接口（Web Server Gateway Interface, WSGI）



#### 代替CGI

CGI 进程（类似 Python 解释器）针对每个请求进行创建，用完就抛弃。
如果应用程序接收数千个请求，创建大量的语言解释器进程很快就会导致服务器停机。
有两种方法可以解决这个问题，一是服务器集成，二是外部进程。



服务器集成，也称为服务器 API。

广泛的服务器解决方案是 Apache HTTP Web 服务器，使用术语模块来描述服务器上插入的编
译后的组件，这些组件可以扩展服务器的功能和用途.

换句话说，不是将服务器切分成多个语言解释器来分别处理请求，而是生成函数调用，运行应用程序代码，在运行过程中进行响应。

服务器根据对应的 API 通过一组预先创建的进程或线程来处理工作。

大部分可以根据所支持应用的需求进行相应的调整。例如，服务器一般还会提供压缩数据、安全、代理、虚拟主机等功能。

缺点：

* 有 bug 的代码会影响到服务器实现执行效率。
* 不同语言的实现无法完全兼容，需要 API 开发者使用与Web 服务器实现相同的编程语言
* 应用程序需要整合到商业解决方案中（如果没有使用开源服务器 API）。
* 应用程序必须是线程安全的，等等。



外部进程， 这是让 CGI 应用在服务器外部运行。

当有请求进入时，服务器将这个请求传递到外部进程中。

这种方式的可扩展性比纯 CGI 要好，因为外部进程存在的时间很长，而不是处理完单个请求后就终止。使用外部进程最广为人知的解决方案是**FastCGI**。

FastCGI 有 Python 实现，除此之外还有 Apache 的其他 Python 模块（如 PyApache、
mod_snkae、mod_python 等），其中有些已经不再维护了。所有这些模块加上纯 CGI 解决方
案，组成了各种 Web 服务器 API 网关解决方案，以调用 Python Web 应用程序。

总之，这些模块为开发者提供了新的负担，不仅要开发应用本身，还要决定与 Web 服务器的集成

在编写应用时，就需要完全知道最后会使用哪个机制，并以相应的方式执行

对于 Web 框架开发者，问题就更加突出了，如果不想强迫他们开发多版本的应用，就必须为所有服务器解决方案提供接口，以此来让更多的用户采用你的框架。

这个困境看起来绝不是 Python 的风格，就导致了 Web 服务器网类接口（Web Server Gateway Interface，WSGI）标准的建立。



#### WSGI简介

WSGI 不是服务器，也不是用于与程序交互的 API，更不是真实的代码，而只是定义的一个接口。WSGI 规范作为 PEP 333 于 2003 年创建，用于处理日益增多的不同 Web 框架、Web 服务器，及其他调用方式（如纯 CGI、服务器 API、外部进程）。

其目标是在 Web 服务器和 Web 框架层之间提供一个通用的 API 标准，减少之间的互操作性并形成统一的调用方式。

WSGI 刚出现就得到了广泛应用。基本上所有基于 Python 的Web 服务器都兼容 WSGI



#### WSGI 应用

根据 WSGI 定义，其应用是可调用的对象，其参数固定为以下两个：

* 一个是含有服务器环境变量的字典
* 另一个是可调用对象，该对象使用 HTTP 状态码和会返回给客户端的 HTTP
  头来初始化响应。这个可调用对象必须返回一个可迭代对象用于组成响应负载。

eg:

```python
def simple_wsgi_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return ['Hello world!']
```

environ 变量包含一些熟悉的环境变量，如 HTTP_HOST、HTTP_USER_AGENT、ERVER_PROTOCOL 等。

start_response()这个可调用对象必须在应用执行，生成最终会发送回客户端的响应。
在这个第 1 版的 WSGI 标准中，start_response()还应该返回一个 write()函数，以便支持遗
留服务器，此时生成的是数据流。建议使用 WSGI 时只返回可迭代对象，让 Web 服务器负责
管理数据并返回给客户端（而不是让应用程序处理这些不精通的事情）。由于这些原因，大多
数应用并不使用或保存 start_response()的返回值，只是简单将其抛弃。

* 设置状态码和头信息

  响应必须含有 HTTP 返回码（200、300 等），以及 HTTP 响应头

  前面的例子中，可以看到其中设置了 200 状态码，以及 Content-Type 头。

  这些信息都传递给 start_response()，来正式启动响应。

* 返回内容
  返回的内容必须是可迭代的，如列表、生成器等,
  它们生成实际的响应负载。在这个例子中，只返回含有单个字符串的列表，但其实可以返回
  更多数据。除了返回列表之外，还可以返回其他可迭代对象，如生成器或其他可调用实例。

* 错误响应

  关于 start_response()最后一件事是其第三个参数，这是个可选参数，这个参数含有异
  常信息，通常大家知道其缩写 exc_info。

  如果应用将 HTTP 头设置为“200 OK”（但还没有发送），并且在执行过程中遇到问题，则可以将 HTTP 头改成其他内容，如“403Forbidden”或“500 Internal Server Error”。
  为了做到这一点，可以假设应用使用一对正常的参数开始执行。

  当发生错误时，会再次调用 start_response()，但会将新的状态码与 HTTP 头和 exc_info 一起传入，替换原有的内容。

  如果第二次调用时 start_response()没有提供 exc_info，则会发生错误。而且必须在发送
  HTTP 头之前第二次调用 start_response()。



#### WSGI 服务器

在服务器端，必须调用应用（前面已经介绍了），传入环境变量和 start_response()这个可
调用对象，接着等待应用执行完毕。在执行完成后，必须获得返回的可迭代对象，将这些数
据返回给客户端。在下面这段代码中，给出了一个具有简单功能的例子，这个例子演示了
WSGI 服务器看起来会是什么样子的。

```python
import StringIO
import sys
def run_wsgi_app(app, environ):
    body = StringIO.StringIO()
    def start_response(status, headers):
    	body.write('Status: %s\r\n' % status)
    	for header in headers:
    		body.write('%s: %s\r\n' % header)
    	return body.write
    iterable = app(environ, start_response)  #注意这里
    try:
    if not body.getvalue():
    	raise RuntimeError("start_response() not called by app!")
    	body.write('\r\n%s\r\n' % '\r\n'.join(line for line in iterable))
    finally:
    	if hasattr(iterable, 'close') and callable(iterable.close):
    		iterable.close()
sys.stdout.write(body.getvalue())
sys.stdout.flush()
```

底层的服务器/网关会获得开发者提供的应用程序，将其与 envrion 字典放在一起，envrion 字典含有 os.environ()中的内容，以及 WSGI 相关的 wsig.*环境变量。

使用这些内容来调用 run_wsgi_app()，该函数将响应传送给客户端。

事实上，应用开发者不会在意这些细节。如创建一个提供 WSGI 规范的服务器，并为应用程序提供一致的执行框架。

从前面的例子中可以看到，WSGI 在应用端和服务器端有明显的界线。

任何应用都可以传递到上面描述的服务器（或任何其他 WSGI 服务器）中。

同样，
在任何应用中，无须关心哪种服务器会调用这个应用。只须在意当前的环境，以及将数据返
回给客户端之前需要执行的 start_response()可调用对象。



#### 内置库wsgiref参考实现

```python
#!/usr/bin/env python
from wsgiref.simple_server import make_server, demo_app
httpd = make_server('', 8000, demo_app)
print "Started app serving on port 8000..."
httpd.serve_forever()
```

wsgiref.simple 提供了简单参考的服务器和实例应用。

*  这个 demo_app()与 simple_wsgi_app()几乎相同，只是其还会显示环境变量。
* make_server()，通过这个函数可以部署一个用于简单访问的参考服务器。

这只是兼容 WSGI 服务器的参考模型。它不具有完整功能或也不打算在生产环境中使用，
但服务器创建者可以以此为蓝本，创建自己的兼容 WSGI 的服务器。应用开发者可以将
demo_app()当作参考，来实现兼容 WSGI 的应用。



#### 中间件及封装 WSGI 应用

在某些情况下，除了运行应用本身之外，还想在应用执行之前（处理请求）或之后（发
送响应）添加一些处理程序。

**这就是熟知的中间件，它用于在 Web 服务器和 Web 应用之间添加额外的功能。**

中间件要么对来自用户的数据进行预处理，然后发送给应用；要么在应用
将响应负载返回给用户之前，对结果数据进行一些最终的调整。

这种方式类似洋葱结构，应用程序在内部，而额外的处理层在周围。

预处理可以包括动作，如拦截、修改、添加、移除请求参数，修改环境变量（包括用户提交的表单（CGI）变量），使用 URL 路径分派应用的功能，转发或重定向请求，通过入站客户端 IP 地址对网络流量进行负载平衡，委托其功能（如使用 User-Agent 头向移动用户发送简化过的 UI/应用），以及其他功能。
而后期处理主要包括调整应用程序的输出。

eg: 对应用程序返回的每一条结果都会加一个时间戳：

```python
class Ts_ci_wrapp(object):
	def __init__(self, app):
		self.orig_app = app
	def __call__(self, *stuff):
		return ('[%s] %s' % (ctime(), x) for x in self.orig_app(*stuff))
httpd = make_server('', 8000, Ts_ci_wrapp(simple_wsgi_app))
print "Started app serving on port 8000..."
httpd.serve_forever()
```

WSGI 的主旨是在 Web 应用和 Web 服务器之间做了明显的分割。

这样有利于分块开发，让团队更方便地划分任务，让 Web应用能以一致且灵活的方式在任何兼容 WSGI 的后端中运行。