Tags:[web]

最常用的 Web 服务器呢？

这些包括 Apache、ligHTTPD、Microsoft IIS、LiteSpeed Technologies LiteSpeed 和 ACME
Laboratories thttpd。

因为这些服务器都远远超过了应用程序的需求，所以这里仅仅使用 Python建立简单但有用的 Web 服务器

### 建立一个web服务器

要用到的所有基础代码都在 Python 标准库中。读者只须进行基本的定制。

要建立一个Web 服务器，必须建立一个基本的服务器和一个“处理程序”

#### HTTPServer

基础的 Web 服务器是一个模板。其角色是在客户端和服务器端完成必要的 HTTP 交互。
在 BaseHTTPServer 模块中可以找到一个名叫 HTTPServer 的服务器基本类



#### 处理程序

处理程序是一些处理主要“Web 服务”的简单软件。它用于处理客户端的请求，并返回适当的文件，包括静态文件或动态文件。处理程序的复杂性决定了 Web 服务器的复杂程度。
Python 标准库提供了 3 种不同的处理程序。



* BaseHTTPResquestHandler

  最基本、最普通的是名为 BaseHTTPResquestHandler 的处理程序，它可以在BaseHTTPServer 模块中找到，其中含有一个的基本 Web 服务器。除了获得客户端的请求
  外，没有实现其他处理工作，因此必须自己完成其他处理任务，这样就导致了 myhttpd.py
  服务器的出现。

* SimpleHTTPRequestHandler
  SimpleHTTPServer 模块中的 SimpleHTTPRequestHandler，建立BaseHTTPResquestHandler
  的基础上，以非常直接的形式实现了标准的 GET 和 HEAD 请求。
  这虽然还不算完美，但它已经可以完成一些简单的功能。
* CGIHTTPRequestHandler
  CGIHTTPServer 模块中的 CGIHTTPRequestHandler 处理程序，这个处理
  程序可以获取 SimpleHTTPRequestHandler，并添加了对 POST 请求的支持。其可以调用
  CGI 脚本完成请求处理过程，也可以将生成的 HTML 脚本返回给客户端。

为了简化用户体验、提高一致性和降低代码维护开销，这些模块（实际上是其中的类）
组合到单个名为 server.py 的模块中，作为 Python 3 中 http 包中的一部分。

| 模块              | 描述                                                         |
| ----------------- | ------------------------------------------------------------ |
| BaseHTTPServer①   | 提供基本的 Web 服务器和处理程序类，分别是 HTTPServer 和 BaseHTTPRequestHandler |
| SimpleHTTPServer① | 含有 SimpleHTTPRequestHandler 类，用于处理 GET 和 HEAD 请求  |
| CGIHTTPServer①    | 含有 CGIHTTPRequestHandler 类，用于处理 POST 请求并执行 CGI  |
| http.server②      | 前面的三个 Python 2 模块和类整合到一个 Python 3 包中         |

① Python 3.0 中移除。
② Python 3.0 中新增。



 #### 一个简单的web服务器

```python
#coding:utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            f = open(self.path[1:],'r')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'File not found: %s ' % self.path)

def main():
    try:
        server = HTTPServer(('',80), MyHandler)
        print 'Welcome to the machine..'
        print 'Press ^C once or twice to quit.'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

```

out:

```
Welcome to the machine..
Press ^C once or twice to quit.
localhost.localdomain - - [28/Feb/2019 15:23:45] code 404, message File not found: /index.html 
localhost.localdomain - - [28/Feb/2019 15:23:45] "GET /index.html HTTP/1.1" 404 -
localhost.localdomain - - [28/Feb/2019 15:24:33] "GET /log HTTP/1.1" 200 -
^C^C received, shutting down serve
```

