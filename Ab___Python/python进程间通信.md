### 写在前面

`os.fork()`，它将产生一个子进程。fork调用同时在父进程和主进程同时返回，在父进程中返回子进程的pid，在子进程中返回0。





进程间通信：

### 临时文件

使用文件进行通信是最简单的一种通信方式，子进程将结果输出到临时文件，父进程从文件中读出来。文件名使用子进程的进程id来命名。进程随时都可以通过`os.getpid()`来获取自己的进程id。

```python
# coding: utf-8

import os
import sys
import math

# 计算
def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            with open("%d" % os.getpid(), "w") as f:
                f.write(str(s))
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        os.waitpid(pid, 0)  # 等待子进程结束
        with open("%d" % pid, "r") as f:
            sums.append(float(f.read()))
        os.remove("%d" % pid)  # 删除通信的文件
    return math.sqrt(sum(sums) * 8)


print pi(10000000) #输出 3.14159262176
```



### 管道pipe

管道是Unix进程间通信最常用的方法之一，它通过在父子进程之间开通读写通道来进行双工交流。我们通过os.read()和os.write()来对文件描述符进行读写操作，使用os.close()关闭描述符。

单进程管道：

![](http://claymore.wang:5000/uploads/big/dd59087318a666a2a4b4122110938b0f.png)

父子进程分离后的管道：

![](http://claymore.wang:5000/uploads/big/a40bd6ea92c84c095e1d4db62974a5d1.png)

代码：

```python
# coding: utf-8

import os
import sys
import math


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = {}
    unit = n / 10
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        r, w = os.pipe()
        pid = os.fork()
        if pid > 0:
            childs[pid] = r  # 将子进程的pid和读描述符存起来
            os.close(w)  # 父进程关闭写描述符，只读
        else:
            os.close(r)  # 子进程关闭读描述符，只写
            s = slice(mink, maxk)  # 子进程开始计算
            os.write(w, str(s))
            os.close(w)  # 写完了，关闭写描述符
            sys.exit(0)  # 子进程结束
    sums = []
    for pid, r in childs.items():
        sums.append(float(os.read(r, 1024)))
        os.close(r)  # 读完了，关闭读描述符
        os.waitpid(pid, 0)  # 等待子进程结束
    return math.sqrt(sum(sums) * 8)


print pi(10000000)

```



### 套接字

#### 以太网套接字

```python
# coding: utf-8

import os
import sys
import math
import socket


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = []
    unit = n / 10
    servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 注意这里的AF_INET表示普通套接字
    servsock.bind(("localhost", 0))  # 0表示随机端口
    server_address = servsock.getsockname()  # 拿到随机出来的地址，给后面的子进程使用
    servsock.listen(10)  # 监听子进程连接请求
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            servsock.close()  # 子进程要关闭servsock引用
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)  # 连接父进程套接字
            s = slice(mink, maxk)  # 子进程开始计算
            sock.sendall(str(s))
            sock.close()  # 关闭连接
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in childs:
        conn, _ = servsock.accept()  # 接收子进程连接
        sums.append(float(conn.recv(1024)))
        conn.close()  # 关闭连接
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    servsock.close()  # 关闭套接字
    return math.sqrt(sum(sums) * 8)


print pi(10000000)
```



#### Unix域套接字

当同一个机器的多个进程使用普通套接字进行通信时，需要经过网络协议栈，这非常浪费，因为同一个机器根本没有必要走网络。所以Unix提供了一个套接字的特殊版本，它使用和套接字一摸一样的api，但是地址不再是网络端口，而是文件。相当于我们通过某个特殊文件来进行套接字通信。

![](http://claymore.wang:5000/uploads/big/a6f6fce6a9595dcd17deba7381c742e3.png)

```python
# coding: utf-8

import os
import sys
import math
import socket


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    server_address = "/tmp/pi_sock"  # 套接字对应的文件名
    childs = []
    unit = n / 10
    servsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  # 注意AF_UNIX表示「域套接字」
    servsock.bind(server_address)
    servsock.listen(10)  # 监听子进程连接请求
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            servsock.close()  # 子进程要关闭servsock引用
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(server_address)  # 连接父进程套接字
            s = slice(mink, maxk)  # 子进程开始计算
            sock.sendall(str(s))
            sock.close()  # 关闭连接
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in childs:
        conn, _ = servsock.accept()  # 接收子进程连接
        sums.append(float(conn.recv(1024)))
        conn.close()  # 关闭连接
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    servsock.close()  # 关闭套接字
    os.unlink(server_address)  # 移除套接字文件
    return math.sqrt(sum(sums) * 8)

print pi(10000000)
```



#### 无名套接字socketpair

我们知道跨网络通信免不了要通过套接字进行通信，但是本例的多进程是在同一个机器上，用不着跨网络，使用普通套接字进行通信有点浪费。

为了解决这个问题，Unix系统提供了无名套接字socketpair，不需要端口也可以创建套接字，父子进程通过socketpair来进行全双工通信。

socketpair返回两个套接字对象，一个用于读一个用于写，它有点类似于pipe，只不过pipe返回的是两个文件描述符，都是整数。所以写起代码形式上跟pipe几乎没有什么区别。

我们使用sock.send()和sock.recv()来对套接字进行读写，通过sock.close()来关闭套接字对象。

```python
# coding: utf-8

import os
import sys
import math
import socket


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = {}
    unit = n / 10
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        rsock, wsock = socket.socketpair()
        pid = os.fork()
        if pid > 0:
            childs[pid] = rsock
            wsock.close()
        else:
            rsock.close()
            s = slice(mink, maxk)  # 子进程开始计算
            wsock.send(str(s))
            wsock.close()
            sys.exit(0)  # 子进程结束
    sums = []
    for pid, rsock in childs.items():
        sums.append(float(rsock.recv(1024)))
        rsock.close()
        os.waitpid(pid, 0)  # 等待子进程结束
    return math.sqrt(sum(sums) * 8)


print pi(10000000)
```



### 有名管道fifo

相对于管道只能用于父子进程之间通信，Unix还提供了有名管道可以让任意进程进行通信。有名管道又称fifo，它会将自己注册到文件系统里一个文件，参数通信的进程通过读写这个文件进行通信。 fifo要求读写双方必须同时打开才可以继续进行读写操作，否则打开操作会堵塞直到对方也打开。

```python
# coding: utf-8

import os
import sys
import math


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = []
    unit = n / 10
    fifo_path = "/tmp/fifo_pi"
    os.mkfifo(fifo_path)  # 创建named pipe
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            with open(fifo_path, "w") as ff:
                ff.write(str(s) + "\n")
            sys.exit(0)  # 子进程结束
    sums = []
    while True:
        with open(fifo_path, "r") as ff:
            # 子进程关闭写端，读进程会收到eof
            # 所以必须循环打开，多次读取
            # 读够数量了就可以结束循环了
            sums.extend([float(x) for x in ff.read(1024).strip().split("\n")])
            if len(sums) == len(childs):
                break
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    os.unlink(fifo_path)  # 移除named pipe
    return math.sqrt(sum(sums) * 8)


print pi(10000000)
```



### OS 消息队列

操作系统也提供了跨进程的消息队列对象可以让我们直接使用，只不过python没有默认提供包装好的api来直接使用。我们必须使用第三方扩展来完成OS消息队列通信。第三方扩展是通过使用Python包装的C实现来完成的。

![](http://claymore.wang:5000/uploads/big/c916894dc8d6ea964bfff964ef12214f.png)

OS消息队列有两种形式，**一种是posix消息队列，另一种是systemv消息队列**，有些操作系统两者都支持，有些只支持其中的一个，比如macos仅支持systemv消息队列，我本地的python的docker镜像是debian linux，它仅支持posix消息队列。



#### posix

**posix消息队列** 我们先使用posix消息队列来完成圆周率的计算，posix消息队列需要提供一个唯一的名称，它必须是`/`开头。close()方法仅仅是减少内核消息队列对象的引用，而不是彻底关闭它。unlink()方法才能彻底销毁它。O_CREAT选项表示如果不存在就创建。向队列里塞消息使用send方法，收取消息使用receive方法，receive方法返回一个tuple，tuple的第一个值是消息的内容，第二个值是消息的优先级。之所以有优先级，是因为posix消息队列支持消息的排序，在send方法的第二个参数可以提供优先级整数值，默认为0，越大优先级越高。

```python
# coding: utf-8

import os
import sys
import math
from posix_ipc import MessageQueue as Queue


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    q = Queue("/pi", flags=os.O_CREAT)
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            q.send(str(s))
            q.close()
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        sums.append(float(q.receive()[0]))
        os.waitpid(pid, 0)  # 等待子进程结束
    q.close()
    q.unlink()  # 彻底销毁队列
    return math.sqrt(sum(sums) * 8)


print pi(10000000)
```



#### systemv

**systemv消息队列** systemv消息队列和posix消息队列用起来有所不同。systemv的消息队列是以整数key作为名称，如果不指定，它就创建一个唯一的未占用的整数key。它还提供消息类型的整数参数，但是不支持消息优先级。

```python
# coding: utf-8

import os
import sys
import math
import sysv_ipc
from sysv_ipc import MessageQueue as Queue


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    q = Queue(key=None, flags=sysv_ipc.IPC_CREX)
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            q.send(str(s))
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        sums.append(float(q.receive()[0]))
        os.waitpid(pid, 0)  # 等待子进程结束
    q.remove()  # 销毁消息队列
    return math.sqrt(sum(sums) * 8)


print pi(10000000)
```





### 共享内存

共享内存也是非常常见的多进程通信方式，**操作系统负责将同一份物理地址的内存映射到多个进程的不同的虚拟地址空间中。**

进而每个进程都可以操作这份内存。

**考虑到物理内存的唯一性，它属于临界区资源，需要在进程访问时搞好并发控制，比如使用信号量。**

我们通过一个信号量来控制所有子进程的顺序读写共享内存。

我们分配一个8字节double类型的共享内存用来存储极限的和，每次从共享内存中读出来时，要使用struct进行反序列化(unpack)，将新的值写进去之前也要使用struct进行序列化(pack)。

每次读写操作都需要将读写指针移动到内存开头位置(lseek)。

![](http://claymore.wang:5000/uploads/big/47dbd85d4026961d849d5d1d4b0d5fc3.png)



```python
# coding: utf-8

import os
import sys
import math
import struct
import posix_ipc
from posix_ipc import Semaphore
from posix_ipc import SharedMemory as Memory


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    sem_lock = Semaphore("/pi_sem_lock", flags=posix_ipc.O_CREX, initial_value=1)  # 使用一个信号量控制多个进程互斥访问共享内存
    memory = Memory("/pi_rw", size=8, flags=posix_ipc.O_CREX)
    os.lseek(memory.fd, 0, os.SEEK_SET)  # 初始化和为0.0的double值
    os.write(memory.fd, struct.pack('d', 0.0))
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            sem_lock.acquire()
            try:
                os.lseek(memory.fd, 0, os.SEEK_SET)
                bs = os.read(memory.fd, 8)  # 从共享内存读出来当前值
                cur_val, = struct.unpack('d', bs)  # 反序列化，逗号不能少
                cur_val += s  # 加上当前进程的计算结果
                bs = struct.pack('d', cur_val) # 序列化
                os.lseek(memory.fd, 0, os.SEEK_SET)
                os.write(memory.fd, bs)  # 写进共享内存
                memory.close_fd()
            finally:
                sem_lock.release()
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        os.waitpid(pid, 0)  # 等待子进程结束
    os.lseek(memory.fd, 0, os.SEEK_SET)
    bs = os.read(memory.fd, 8)  # 读出最终这结果
    sums, = struct.unpack('d', bs)  # 反序列化
    memory.close_fd()  # 关闭共享内存
    memory.unlink()  # 销毁共享内存
    sem_lock.unlink()  #  销毁信号量
    return math.sqrt(sums * 8)


print pi(10000000)
```



摘自： https://juejin.im/post/5b0abab451882538c220440b