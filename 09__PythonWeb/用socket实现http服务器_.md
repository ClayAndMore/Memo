---
title: "用socket实现http服务器_.md"
date: 2017-02-22  17:54:22 +0800
lastmod: 2019-11-18 17:54:22 +0800
draft: false
tags: [""]
categories: ["python web"]
author: "Claymore"

---


### TCP socket

在Python中，我们使用标准库中的**socket包**来进行底层的socket编程。

服务端：

```python
import socket

# 地址
HOST='127.0.0.1'
PORT=8000

reply='Yes'

#socket.socket()创建一个socket对象，并说明socket使用的是IPv4(AF_INET，IP version 4)和TCP协议(SOCK_STREAM)。
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 绑定ip和端口 
s.bind((HOST, PORT))

# 被动监听，连接队列中最大有三个连接数
s.listen(3)

# 接受连接，并建立链接
conn,addr=s.accept()

# 接受消息
request=conn.recv(1024)

print('request is:',request)
print('Connet bu',addr)

#发送消息
conn.sendall(reply)
conn.close()
```

客户端：

```python
# Written by Vamei
# Client side
import socket

# Address,没有两台计算机，用本地ip
HOST = '127.0.0.1'
PORT = 8000

request = 'can you hear me?'

# configure socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# send message
s.sendall(request)
# receive message
reply  = s.recv(1024)
print('reply is: ',reply)
# close connection
s.close()
```

### 基于TCP socket的http服务器

上面的例子中，我们已经可以使用TCP socket来为两台远程计算机建立连接。然而，socket传输自由度太高，从而带来很多安全和兼容的问题。我们往往利用一些应用层的协议(比如HTTP协议)来规定socket **使用规则**，以及所传输信息的**格式**。

**HTTP**协议利用**请求-回应(request-response)**的方式来使用TCP socket。客户端向服务器发一段文本作为request，服务器端在接收到request之后，向客户端发送一段文本作为response。在完成了这样一次request-response交易之后，TCP socket被废弃。下次的request将建立新的socket。request和response本质上说是两个文本，只是HTTP协议对这两个文本都有一定的格式要求。

```python
import socket
# Address
HOST = ''
PORT = 8080

# Prepare HTTP response
text_content = '''HTTP/1.x 200 OK
Content-Type: text/html

<head>
<title>WOW</title>
</head>
<html>
<p>Wow, Python Server</p>
<IMG src="test.jpg"/>
</html>
'''

# Read picture, put into HTTP format
f = open('test.jpg','rb')#encoding='gbk',errors='ignore'
pic_content = '''
HTTP/1.x 200 OK
Content-Type: image/jpg

'''
# s=f.read()
# print(chardet.detect(s))


pic_content = pic_content.encode()+f.read()#.decode('utf-8',errors='ignore')
f.close()

# Configure socket
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# infinite loop, server forever
while True:
    # 3: maximum number of requests waiting
    s.listen(3)
    conn, addr = s.accept()
    request    = conn.recv(1024)
    temp=request.decode().split(' ')[0]
    method = temp
    temp2= request.decode().split(' ')[1]
    src =temp2

    # deal with GET method
    if method == 'GET':
        # ULR
        if src == '/test.jpg':
            content = pic_content
        else: content = text_content.encode()

        print('Connected by', addr)
        print('Request is:', request)
        conn.sendall(content)
    # close connection
    conn.close()
```

#### response

整个response分为**起始行**(start line), **头信息**(head)和**主体**(body)三部分。

* 起始行就是第一行:`HTTP/1.x 200 OK`

HTTP/1.x表示所使用的HTTP版本，200表示状态(status code)，200是HTTP协议规定的，表示服务器正常接收并处理请求，OK是供人来阅读的status code。

* 头信息

`Content-Type: text/html`

用来表示主题信息的类型为html文本。头信息和主体要有一行**空行**.

而pic_content的头信息(Content-Type: image/jpg)说明主体的类型为jpg图片(image/jpg)。



#### request

尽管request也可以像response那样分为三部分，request的格式与response的格式并不相同。request由客户发送给服务器，比如下面是一个request：

```
GET /test.jpg HTTP/1.x
Accept: text/*
```

起始行可以分为三部分:

* 第一部分为请求方法(**request method**)，第二部分是**URL**，第三部分为HTTP版本。request method可以有GET， PUT， POST， DELETE， HEAD。
* 第二部分为URL，它通常指向一个资源(服务器上的资源或者其它地方的资源)。像现在这样，就是指向当前服务器的当前目录的test.jpg。

```
# 使用浏览器访问时的request
GET /test.jpg HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: image/webp,*/*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: http://localhost:8080/
Cookie: pgv_pvid=1319877504
Cache-Control: max-age=0

# 使用curl 访问时的request
GET / HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.58.0
Accept: */*
```





浏览器访问：

![](http://claymore.wang:5000/uploads/big/c5ceecbc59a654ee0ef1df353cfb994e.png)

从终端，我们可以看到，浏览器实际上发出了两个请求。第一个请求为 (关键信息在**起始行**，这一个请求的主体为空)

我们的Python程序根据这个请求，发送给服务器text_content的内容。

浏览器接收到text_content之后，知道需要获得text.jpg文件来补充为图片，立即发出了第二个请求.

我们的Python程序分析过起始行之后，发现/test.jpg符合if条件，所以将pic_content发送给客户。

最后，浏览器根据html语言的语法，将html文本和图画以适当的方式显示出来。