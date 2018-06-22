### 写在前面

socket 译为套接字。

站在更贴近系统的层级去看，两个机器间的通信方式，无非是要通过运输层的TCP/UDP，网络层IP，因此socket本质是编程接口(API)，对TCP/UDP/IP的封装，TCP/UDP/IP也要提供可供程序员做网络开发所用的接口，这就是Socket编程接口。 socket接口是实际上是**操作系统**提供的**系统调用**。



实际的linux操作系统中，就是socket文件，我们再创建它之后，就会得到一个操作系统返回的对于该文件的描述符，然后应用程序可以通过使用套接字描述符访问套接字，向其写入输入，读出数据。 



socket的使用并不局限于Python语言，你可以用C或者JAVA来写出同样的socket服务器，而所有语言使用socket的方式都类似(Apache就是使用C实现的服务器)。而你不能跨语言的使用框架。

框架的好处在于帮你处理了一些细节，从而实现快速开发，但同时受到Python本身性能的限制。我们已经看到，许多成功的网站都是利用动态语言(比如Python, Ruby或者PHP，比如twitter和facebook)快速开发，在网站成功之后，将代码转换成诸如C和JAVA这样一些效率比较高的语言，从而让服务器能更有效率的面对每天亿万次的请求。在这样一些时间，底层的重要性，就远远超过了框架。





### TCP socket 实现

#### 客户端

```python
# 导入socket库:
import socket
# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('www.sina.com.cn', 80)) 
```

* 创建`Socket`时，`AF_INET`指定使用IPv4协议，如果要用更先进的IPv6，就指定为`AF_INET6` 
* `SOCK_STREAM`指定使用面向流的TCP协议 
* connect参数注意是一个地址+端口的元组

```python
# 发送数据:
s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection:close\r\n\r\n')
# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)
# 关闭连接:
s.close()
```

* 向新浪服务器发送请求，要求返回首页的内容 
* 调用`recv(max)`方法，一次最多接收指定的字节数 
* data 包括HTTP头和网页本身 



#### 服务器

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('127.0.0.1', 9999))
s.listen(5)  # 开始监听端口，传入的参数指定等待连接的最大数量
print 'Waiting for connection...'

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
```

* `accept()`会等待并返回一个客户端的连接,返回（ip, port）
* 每个连接都必须创建新线程（或进程）来处理，否则，单线程在处理连接的过程中，无法接受其他客户端的连接：

新起一个客户端：

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print s.recv(1024)
for data in ['Michael', 'Tracy', 'Sarah']:
    # 发送数据:
    s.send(data)
    print s.recv(1024)
s.send('exit')
s.close()
```

执行：

![](http://ovolonhm1.bkt.clouddn.com/socket.png)





### UDP socket 实现

#### 客户端

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in ['Michael', 'Tracy', 'Sarah']:
    # 发送数据:
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print s.recv(1024)
s.close()
```

* `SOCK_DGRAM`指定了这个Socket的类型是UDP 
* 不需要调用`connect()`，直接通过`sendto()`给服务器发数据：

#### 服务端

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('127.0.0.1', 9999))

while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print 'Received from %s:%s.' % addr
    s.sendto('Hello, %s!' % data, addr)
```

* 需要调用`listen()`方法，而是直接接收来自任何客户端的数据 
* 接调用`sendto()`就可以把数据用UDP发给客户端。 

注意这里省掉了多线程，因为这个例子很简单。 



### socket对象 其他API

#### accpet()

调用前必须绑定端口并监听。

返回值是新的socket对象(这个对象不能收发数据)和绑定连接的地址：

`(new_socket, (ip, port))`



#### setblocking()

设置是否阻塞， setblocking(0)为非阻塞， setblocking(1)为阻塞， 默认为阻塞。

```
>>> import socket
>>> a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> a.bind(('127.0.0.1', 8080))
>>> a.listen(5)
>>> c,s = a.accept()
```

这里accept会一直等待消息的传入， 会阻塞本进程。

```
>>> a.setblocking(0)
>>> c,s = a.accept()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.6/socket.py", line 197, in accept
    sock, addr = self._sock.accept()
socket.error: [Errno 11] Resource temporarily unavailable
```

设置为非阻塞模式， 会立马获得结果，如果读入缓冲区为空则异常。

这个函数和select结合会有很好的效果。



#### fileno()

返回socket的文件描述符。只在unix系统下可用。

```
>>> import socket
>>> s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> s.fileno()
4
```

这里可以用于select.select() ，Python文档如是说。



#### makefile([mode[, bufsize]])

返回一个和socket相关的文件对象，这个文件对象在调用close()时不会被显示的关闭， 但会移走对这个文件对象的引用，如果没有被其他地方引用这个，以便更好的关闭socket.

文件对象File Objects 是 open(), os.popen()等打开的对象。



可选参数 mode , bufsize， 也是内置open()方法的参数， 

mode打开模式， wb, rb 等。

bufsize设置缓冲区：

* -1 **全缓冲：**同系统及磁盘块大小有关，n个字节后执行一次写入操作，缓冲大小为系统默认 
* 1**行缓冲：**遇到换行符执行一次写操作
* `>1`  字节数为buffering的全缓冲 
* 0 **无缓冲：**立刻执行写操作

没有指定则用系统默认。



#### shutdown(how)

当你使用完工 socket对象时，你应调用close()方法显式的关闭socket以尽快释放资源（尽管socket被垃圾回收器回收时将自动被关闭）。

你也可以使用shutdown(how)方法来关闭连接一边或两边。

参数0阻止socket接收数据， socket.SHUT_RD 

1阻止发送，              socket.SHUT_WR

2阻止接收和发送。  socket.SHUT_RDWR 

然后再用socket释放。



shutdown 和 socket 的区别，

对于系统来说，socket是一种资源， 所以有句柄handle来管理， 

close方法会让handle对该socket的引用减一， 如果引用为0，则该socket被释放。

如果减后引用不为零，说明还有其他进程在引用。

shutdown 方法会 对这个根的读写开关， 如果一个进程中关掉相关，其他进程也不能使用相关功能， 但是shutdown方法不会释放掉socket。