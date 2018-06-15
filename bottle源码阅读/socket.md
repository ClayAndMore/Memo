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

* `accept()`会等待并返回一个客户端的连接
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





