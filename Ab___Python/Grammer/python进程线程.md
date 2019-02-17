Tags:[python]

## 线程进程

### 多线程

Python的标准库提供了两个模块：`_thread`和`threading`，`_thread`是低级模块，`threading`是高级模块，对`_thread`进行了封装。绝大多数情况下，我们只需要使用`threading`这个高级模块。

启动一个线程就是把一个函数传入并创建`Thread`实例，然后调用`start()`开始执行：

```
import time,threading
def loop():

    print('线程 %s 正在跑'%threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+1
        print('线程 %s >>> %s'%(threading.current_thread().name,n))
        time.sleep(1)
    print('线程 %s 结束'%threading.current_thread().name)
print('线程 %s 正在跑跑'%threading.current_thread().name)

t=threading.Thread(target=loop,name='LoopTread')
t.start()
t.join()

print('thread %s ended'%threading.current_thread().name)
```

![img](http://ojynuthay.bkt.clouddn.com/pythonthread.png)

join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞,这里也就是说一直阻塞主线程，直到threading线程结束，我们该程序才可运行。

#### threading

threading 模块对象：

| threading模块对象 | 解释                                                         |
| ----------------- | ------------------------------------------------------------ |
| Thread            | 创建一个可执行的线程对象                                     |
| Lock              | 锁原语对象                                                   |
| RLock             | 可重入锁对象，使单线程可以获得已经获得了的锁（递归锁定）     |
| Condition         | 条件变量对象能让一个线程停下来，等待其他线程满足了某个条件   |
| Event             | 通用的条件变量。多个线程可以等待某个事件的发生，在事件发生后所有的线程都会被激活 |
| Semaphore         | 为等待锁的线程提供一个类似等待室的结构                       |
| BoundedSemaphore  | 与Semaphore类似，只是他不允许超过初始值                      |
| Timer             | 与Thread类似，只是它等待一段时间后才开始运行                 |
| activeCount()     | 当前活动的线程数量                                           |
| currentThread()   | 返回当前线程对象                                             |
| enumerate()       | 返回当前活动线程的列表                                       |
| settrace(func)    | 为所有线程设置一个跟踪函数                                   |
| setprofile(func)  | 为所有线程设置一个profile函数 threading模块对象              |

Thread参数：

`Thread(group=None, target=None, name=None, args=(), kwargs={})`

> group，预留参数，一直为None
>
> target，线程启动时执行的可调用对象，由run()方法调用
>
> name，线程名
>
> args，target处可调用对象（target）的参数，如果可调用对象没有参数，不用赋值
>
> kwargs，target处可调用对象的关键字参数

Thread方法：

1. start()

   启动线程，这个方法**只能调用一次**，执行run()方法

2. run()

   线程启动时将调用此方法。默认情况下，它将调用target，还可以在Thread的子类中重新定义此方法

3. join(timeout = None)

   > timeout，超时时间(单位 = s) ，默认为无时间限制

   等待线程终止或者出现超时为止，能多次使用该方法。就是说让主线程来等我这个join的线程

4. getName(),name     返回线程名

5. setName(name)      设置线程名

6. isAlive(),is_alive()      线程正在运行返回True，否则返回False

7. isDaemon()               返回线程的daemon状态

8. setDaemon(daemonic),daemon设置线程的daemon状态，一定要在start之前调用

   daemon = True,主线程结束，子线程结束

   daemon = False,主线程结束，子线程不结束，继续执行

   就是说将它设置为守护线程，守护线程自己执行完后，如果没有子线程自己就终结了。有父线程的子线程会在自己执行完后将自己挂起，如果父线程一直在，那么悬挂的子线程就会变的很多。

#### lock

两个线程同时一存一取，就可能导致余额不对，你肯定不希望你的银行存款莫名其妙地变成了负数，所以，我们必须确保一个线程在修改`balance`的时候，别的线程一定不能改。

如果我们要确保`balance`计算正确，就要给`change_it()`上一把锁，当某个线程开始执行`change_it()`时，我们说，该线程因为获得了锁，因此其他线程不能同时执行`change_it()`，只能等待，直到锁被释放后，获得该锁以后才能改。由于锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。创建一个锁就是通过`threading.Lock()`来实现：

```
balance = 0
lock = threading.Lock()

def run_thread(n):

    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
```

#### Event

用于线程间通信，即程序中的其一个线程需要通过判断某个线程的状态来确定自己下一步的操作，就用到了event对象

event对象默认为假（内置标志服为Flase），即遇到event对象在等待就阻塞线程的执行, 那么当程序执行 event.wait 方法时就会阻塞，如果“Flag”值为True，那么event.wait 方法时便不再阻塞。

- 主线程和子线程间通信，代码模拟连接服务器：

```
import threading
import time
event=threading.Event()

def foo():
    print('wait server...')

    event.wait()    #括号里可以带数字执行，数字表示等待的秒数，不带数字表示一直阻塞状态
    print('connect to server')

t=threading.Thread(target=foo,args=())  #子线程执行foo函数

t.start()

time.sleep(3)

print('start server successful')

time.sleep(3)

event.set()     #默认为False，set一次表示True，所以子线程里的foo函数解除阻塞状态继续执行
```

- 子线程和子线程通信

```

import threading

import time

event=threading.Event()

def foo():

    print('wait server...')
    event.wait()   

    print('connect to server')

def start():
    time.sleep(3)
    print('start server successful')
    time.sleep(3)
    event.set()     
t=threading.Thread(target=foo,args=())  #子线程执行foo函数
t.start()
t2=threading.Thread(target=start,args=())  #子线程执行start函数
t2.start()
```

两个线程间只用一个Event，当start()中event.set执行时，就激活了foo()中的event.wait()让foo线程继续执行。

- 多线程阻塞

```
import threading
import time

event=threading.Event()

def foo():
    while not event.is_set():   #返回event的状态值，同isSet

        print("wait server...")
        event.wait(2)   #等待2秒，如果状态为False，打印一次提示继续等待
    print("connect to server")

for i in range(5):  #5个子线程同时等待
    t=threading.Thread(target=foo,args=())
    t.start()
print("start server successful")
time.sleep(10)

event.set()   # 设置标志位为True，event.clear()是回复event的状态值为False
```

起了五个进程，如果没有开启就一直循环打印等待服务器（wait server)，当set的那一刻，这个五个线程就要开始工作了。

几个方法：

Event.set(), 将标识符设为Ture.

Event.clear(), 将标识符设为False.

Event.isSet(),  判断标识位是否为Ture.



#### 队列

我们先假设有很多个线程，n个消费者，一个生产者，生产者和消费者都不断的运行，那么我们的CUP岂不是在他们之间来回换，看看这个消费者要没要产品，看看生产者产没产出产品，这样太不科学了，我们一应该用队列来存储产品，如果有消费者要就去队列去取，如果没有则等待，可以这样讲队列线程在没有产品的时候设置为event.wait,当有数据的时候设置成event.set通知其他消费者。



#### local

先看代码：

```python
from threading import local, enumerate, Thread, currentThread

local_data = local()
local_data.name = 'local_data'

class TestThread(Thread):
        def run(self):
                print currentThread()
                print local_data.__dict__
                local_data.name = self.getName()
                local_data.add_by_sub_thread = self.getName()
                print local_data.__dict__

if __name__ == '__main__':
        print currentThread()
        print local_data.__dict__

        t1 = TestThread()
        t1.start()
        t1.join()

        t2 = TestThread()
        t2.start()
        t2.join()

        print currentThread()
        print local_data.__dict__
```

output:

```python
<_MainThread(MainThread, started)>
{'name': 'local_data'}
<TestThread(Thread-1, started)>
{}
{'add_by_sub_thread': 'Thread-1', 'name': 'Thread-1'}
<TestThread(Thread-2, started)>
{}
{'add_by_sub_thread': 'Thread-2', 'name': 'Thread-2'}
<_MainThread(MainThread, started)>
{'name': 'local_data'}
```

主线程中的local_data并没有被改变，而子线程中的local_data各自都不相同。

local_data具有全局访问权，主线程，子线程都能访问它，但是它的值却是各当前线程有关。

查看了一下local的源代码，发现就神奇在_path()方法中:

```
def _patch(self):
    key = object.__getattribute__(self, '_local__key')
    d = currentThread().__dict__.get(key)
    if d is None:
        d = {}
        currentThread().__dict__[key] = d
        object.__setattr__(self, '__dict__', d)

        # we have a new instance dict, so call out __init__ if we have
        # one
        cls = type(self)
        if cls.__init__ is not object.__init__:
            args, kw = object.__getattribute__(self, '_local__args')
            cls.__init__(self, *args, **kw)
    else:
        object.__setattr__(self, '__dict__', d)
```

每次调用local实例的属性前，local都会调用这个方法，找到它保存值的地方.

d = currentThread().__dict__.get(key)  就是这个地方，确定了local_data值的保存位置。所以子线程访问local_data时，并不是获取主线程的local_data的值，在子线程第一次访问它是，它是一个空白的字典对象，所以local_data.__dict__为 {}，就像我们的输出结果一样。

如果想在当前线程保存一个全局值，并且各自线程互不干扰，使用local类吧。



#### GIL锁

我们要知道，现在的cpu有多核的概念，正常来说，一个线程或进程只能在一个核上，多核或多cpu是可以真正并行多进程或线程的。

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，**即使100个线程跑在100核CPU上，也只能用到1个核**。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以 通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

划重点，无论你有几个cpu，python因为GIL锁的原因只能在一个CPU上工作，多线程也就是快速切换线程.



#### Timer

threading.timer, 等待一段时间再进行，我们可以用来实现定时器。

```python
import threading
def timer_handle():
    print 'hello'
   
timer = threading.Timer(5, timer_handler, [参数一，参数二..]) #时间间隔(s)， 回调函数(执行函数)，回调函数参数

timer.cancle()  #关闭定期器
```

上述只打印一次，我们要一直间隔打印才能形成定时器，一种是while True， 一种是用递归调用：

```python
import threading

def time_handler():
    print 'hello'
    global timer
    timer = threading.Timer(5, time_handler)
    timer.start()
timer_handler
```

程序看起来很简单，通过在回调函数里面，重新创建定时器，来使得定时器能够一直工作。

但是值得注意的是，定时器的句柄需要定义成为一个全局变量，这样做的好处是，创建的定时器进程和实例不会堆积，而是覆盖，避免不必要的内存占用。



一个结构化的定时器类：

```python
from threading import Timer,Thread,Event

class perpetualTimer():
   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print 'aaaa'

t = perpetualTimer(5,printer)
t.start()
```







### 多进程

这得从操作系统说起。

linux操作系统提供 一个`fork()`系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是`fork()`调用一次，**返回两次**，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。

```
import os

os.fork()

print 1
```

这个文件运行会打印两次1

子进程永远返回`0`，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用`getppid()`就可以拿到父进程的ID。

Python的`os`模块封装了常见的系统调用，其中就包括`fork`，可以在Python程序中轻松创建子进程：

```
import os
print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))

else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
```

运行结果如下：

```
Process (876) start...

I (876) just created a child process (877).
I am child process (877) and my parent is 876.
```

由于Windows没有`fork`调用，上面的代码在Windows上无法运行。

难道在Windows上无法用Python编写多进程的程序？

由于Python是跨平台的，自然也应该提供一个跨平台的多进程支持。`multiprocessing`模块就是跨平台版本的多进程模块。

`multiprocessing`模块提供了一个`Process`类来代表一个进程对象，下面的例子演示了启动一个子进程并等待其结束：

```python
from multiprocessing import Process

import os

def run(name):

    print('跑的这个子进程是%s(%s)'%(name,os.getpid()))

if __name__=='__main__':

    print('父进程是%s.'%os.getpid())

    p=Process(target=run,args=('test',))

    print('子进程要启动了')

    p.start()
    p.join()
    print('子进程结束了它的生命')
```

![img](http://ojynuthay.bkt.clouddn.com/Process.png)

start()`方法启动，这样创建进程比`fork()`还要简单。

`join()`方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。

#### Pool

如果要启动大量的子进程，可以用进程池的方式批量创建子进程：

```python
from multiprocessing import Pool
import os,time,random

def task(name):
    print('运行任务%s(%s)'%(name,os.getpid()))
    start=time.time()
    time.sleep(random.random()*3)
    end=time.time()
    print('任务%s运行了%0.2f 秒'%(name,(end-start)))

if __name__=='__main__':
    print('父进程%s'%os.getpid())
    p=Pool(4)
    for i in range(5):
        p.apply_async(task,args=(i,))

    print('等待所有子进程运行完')
    p.close()
    p.join()
    print('所有进程运行完')
```

![img](http://ojynuthay.bkt.clouddn.com/processpool.png)

请注意输出的结果，task `0`，`1`，`2`，`3`是立刻执行的，而task `4`要等待前面某个task完成后才执行，这是因为`Pool`的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是`Pool`有意设计的限制，并不是操作系统的限制。如果改成：

```
p = Pool(5)
```

就可以同时跑5个进程。

由于`Pool`的默认大小是CPU的核数，如果你不幸拥有8核CPU，你要提交至少9个子进程才能看到上面的等待效果。



#### multiprocessing

 a simple demo:

```python
from multiprocessing import Process

def worker(num):
    print "this is a worker id:%s"%num
    return
p = Process(target=worker, args=(1,))
p.start()
```

扩充：

```python
# 为进程起名字，方便管理
Process(name='my_service',target=my_func)
# 得到目前进程名
multiprocessing.current_process().name

# 该进程是否在进行
p.is_alive() 	

```



停止进程：

```python
# 停止进程
p.join() # 等待进程停止
p.terminate() # 强制停止
注意 terminate之后要join，使其可以更新状态。
import multiprocessing
import time

def slow_worker():
    print 'Starting worker'
    time.sleep(0.1)
    print 'Finished worker'

if __name__ == '__main__':
    p = multiprocessing.Process(target=slow_worker)
    print 'BEFORE:', p, p.is_alive()

    p.start()
    print 'DURING:', p, p.is_alive()

    p.terminate()
    print 'TERMINATED:', p, p.is_alive()

    p.join()
    print 'JOINED:', p, p.is_alive()
```



进程退出：

```python
import sys
import time
from multiprocessing import Process

def exit_error():
    sys.exit(1)

def exit_ok():
    return  

def return_value():
    return 1

def raises():
    raise RuntimeError('There was an error!')

def terminated():
    time.sleep(3)

if __name__ == '__main__':
    a = Process(target=exit_error)
    b = Process(target=exit_ok)
    c = Process(target=return_value)
    d = Process(target=raises)

    a.start(); b.start(); c.start(); d.start()

    print '========'
    a.join();b.join();c.join();d.join()
    print a.name, a.exitcode
    print b.name, b.exitcode
    print c.name, c.exitcode
    print d.name, d.exitcode
```



#### 进程间传递消息

传递信号:

Event提供一种简单的方法，可以在进程间传递状态信息。事件可以切换设置和未设置状态。通过使用一个可选的超时值，时间对象的用户可以等待其状态从未设置变为设置。

```python
import multiprocessing
import time

def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print 'wait_for_event: starting'
    e.wait()
    print 'wait_for_event: e.is_set()->', e.is_set()

def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print 'wait_for_event_timeout: starting'
    e.wait(t)
    print 'wait_for_event_timeout: e.is_set()->', e.is_set()

if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block',
                                 target=wait_for_event,
                                 args=(e,))
    w1.start()

    w2 = multiprocessing.Process(name='nonblock',
                                 target=wait_for_event_timeout,
                                 args=(e, 2))
    w2.start()

    print 'main: waiting before calling Event.set()'
    time.sleep(3)
    e.set()
    print 'main: event is set'
```



传递消息：

```python
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    while True:
        value = q.get(True)
        print 'Get %s from queue.' % value

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
```
