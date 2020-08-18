---
title: "tornado.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Tornado"]
categories: ["python web"]
author: "Claymore"

---


### 基本结构

基本框架

```python
import tornado.ioloop
import tornado.web  # 这两个类是基础

class MainHandler(tornado.web.RequestHandler):
    def get(self):    # GET 方式Handler
        self.write("Hello")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),   # 路由映射和函数
    ])

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()  #一直循环

if __name__ == "__main__":
    main()

```





### 路由解析

由上方` tornado.web.Application( )`  中所填充

* 固定字符串

  [("/", MainHandler),

   ("/entry", EntryHandler)]

* 参数字符串路径

  ```python
  class ParmHandler(tornado.web.RequestHandler):
      def get(self, parm): # 获得传递参数
          self.write('haha, ' + parm)
  
  def make_app():
      return tornado.web.Application([
          (r"/", MainHandler),
          (r"/haha/([^/]+)", ParmHandler), # 正则匹配任意，一定要有正则，否侧匹配不到
      ])
  ```

  以括号为传递参数， 我这里定义为 parm。

  可以有多个参数。



https://blog.csdn.net/u013038616/article/details/72821600



### RequestHandler

RequestHandler是配置和响应URL的请求核心。

#### Entry Point 接入点函数

继承RequestHandler的子类，重写了父类的一些方法被称为接入点函数(Entry Point)

主要为四种：

* initialize  一些初始化工作，如数据库，log等，调用时可以传递参数。
* prepare  每次请求前的的工作
* get，head, post, delete, patch, put, options(*args, **kwargs)
* on_finish  每次请求后的工作，用于清理等



```python
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

class AHandler(RequestHandler):
    def initialize(self, db):
        self.db = db
        self.set_header('cache-control', 'no-cache')
        print 'initalize'

    def prepare(self):
        print 'prepare'

    def get(self):  # head, post,delete, patch, put, options
        self.write('get it')

    def on_finish(self):
        print 'on_finish'


if __name__ == "__main__":
    app = Application([
        (r"/", AHandler,dict(db='sqlite')),
        ])
    app.listen(8888)
    IOLoop.current().start()

```



#### 输入捕获

RequestHandler中用于捕获客户端传递来的内容，如post数据，URL 查询字符串。

##### 获得URL查询参数和POST提交参数集合

* RequestHandler.get_argument(name), get_arguments(name)

  获取URL查询字符串参数和POST提交参数的参数集合。

  get_argument 获得单个值

  get_arguments 针对参数存在多少个值的 情况使用的，返回多个值的列表。

  ```python
  class LoginHandler(tornado.web.RequestHandler):
      def post(self):
          username = self.get_argument("username", '')
          password = self.get_argument("password", '')
  ```

* get_query_argument(name), get_query_arguments(name)

  和上面类似，不过只是从URL查询参数中获得参数值。

* get_body_argument(name), get_body_arguments(name)

  只是从Post提交参数中获得参数值。



##### 获得cookie

RequestHandler.get_cookie(name, default=None), 没有则返回None



获得HTTP请求的一切信息：

```python
import tornado.web
class DetailHandler(tornado.web.RequestHandler):
    def get():
        ip = self.request.remote_ip
        host = self.reuqet.host 
```

常用对象属性：

| 属性名    | 说明                                                         |
| --------- | ------------------------------------------------------------ |
| method    | HTTP请求方法                                                 |
| uri       |                                                              |
| path      | 请求路径，不包括查询字符串                                   |
| query     | uri中的查询字符串                                            |
| version   | 客户端请求时使用的HTTP协议版本                               |
| header    | 以字典方式表达的HTTP Header                                  |
| body      | 字符串表达HTTP请求体                                         |
| remote_ip | 客户端ip                                                     |
| protocol  | 请求协议，HTTP or HTTPS                                      |
| host      | 请求消息中的主机名                                           |
| arguments | 客户端提交的所以参数                                         |
| cookies   | 客户端提交的Cookie字典                                       |
| files     | 以字典方式表达的客户端上传的文件， 每个文件名对应一个HTTPFIle |





#### 输出响应函数

为客户端生成处理结果的工具函数：

##### 设置状态和跳转：

* RequestHandler.set_status(status_code, reason=None)

  设置返回的HTTP状态码。描述性语句 可以赋值给reason参数。

* RequestHander.render(template, **kwargs)

  用给定的参数渲染模板， 可以在本函数中传入模板文件和模板参数。

  `self.render("template.html", title="Tornado Templates", items=["python", "java"])`

* RequestHandler.redirect(url, permanent=False, status=None)

  页面重定向

  `self.redirect(u"/login")`



##### 设置header和cookie

* RequestHandler.set_header(name, value)

  字典形式设置Respones中的HTTP头参数

  同一个键只会设置用设置的最后一个，eg:

  ```python
  self.set_header("LANGUAGE", "France")
  self.set_header("LANGUAGE", "Chinese")
  ```

  那么header： LANGUAGE: Chinese

* RequestHander.add_header(name, value)

  不会覆盖之前设置的Header值：

  ```python
  self.set_header("LANGUAGE", "France")
  self.set_header("LANGUAGE", "Chinese")
  ```

  header: LANGUAGE: France

  ​	       LANGUAGE: Chinese

* RequestHandler.set_cookie(name, value)

  按键/值对设置Response中的Cookie值。



##### 写入body值

* RequestHandler.write(chunk)

  将给定的块作为HTTP Body 发送给客户端。

  在一般情况下，输出给字符串给客户端。

  如果给定的是个字典，则会将这个块以JSON格式 发送给客户端，

  **同时将HTTP Header 中的Content_Type设置成application/json.**

* RquestHandler.finish(chunk=None)

  通知Tornado:Response的生成工作已经完成， chunk是要给客户端传递的HTTPbody.

  调用后，Tornado 将向客户端发送HTTP Response.

  适用于异步请求处理，同步和协程则无需调用finish函数。 



##### 清空

* RequestHandler.clear()

  清空所有本次请求之前写入的Header值和Body内容。

  ```python
  self.set_header("NUMBER", 8)
  self.clear()
  self.set_header("LANGUAGE", "France")
  ```

  最后的Header中将不包含参数NUMBER

* ReqeuestHandler.clear_all_cookies(path='/', domain=None)

  清除本次中的所以Cookie.





### 异步化及协程化

Tornado 有两种方式可以改变同步的处理

#### 异步化

@tornado.web.asynchrounous

```python
import tornado.web
import tornado.httpclient

class MainHandler(tornado.web.ReuqestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://www.baidu.com", callback = self.on_response)
        
    def on_response(self, response):
        if response.error: rase tornado.web.HTTPEError(500)
        self.write(response.body)
        self.finish()    # 调用Finish 完成请求
```



这种方式会繁琐一些，通过回调函数实现的异步。





#### 协程化

@tornado.gen.coroutime

```python
import tornado.web
import tornado.httpclientclass
class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("htttp://www.baidu.com")
        self.write(response.body)
```

通过yield 方式方式实现的异常对象处理结果