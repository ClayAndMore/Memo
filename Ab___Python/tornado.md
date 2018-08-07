### 1

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





#### 输出响应函数



