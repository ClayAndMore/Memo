---
title: python进阶整理
date: 2017-01-30 08:15:53
categories: python
header-img:
tags: python
---

### 上下文管理器
先看两段程序： 
```python
# without context manager
f = open("new.txt", "w")
print(f.closed)               # whether the file is open
f.write("Hello World!")
f.close()
print(f.closed)
```
用上下文管理器：
```python
# with context manager
with open("new.txt", "w") as f:
    print(f.closed)
    f.write("Hello World!")
print(f.closed)
```
两段程序是相同的操作，但是第二段程序没有关闭文件的链接，只是用**缩进**
和`with...as..`上下文管理来规定了对象的使用范围。
对于文件对象f来说，它定义了__enter__()和__exit__()方法(可以通过dir(f)看到)。在f的__exit__()方法中，有self.close()语句。所以在使用上下文管理器时，我们就不用明文关闭f文件了。



### 内存管理
为了探索对象在内存的存储，我们可以求助于Python的内置函数id()。它用于返回对象的身份(identity)。其实，这里所谓的身份，就是该对象的内存地址。
`a=1
print(id(a))`
输出11246696
这就是1的内存地址，a为地址的引用。
python 对于相同整数和短字符串，保留了同一份引用。对于其它，即使内容相同，还是创建新的对象。is()函数可以判断是不是同一个引用。

is比较的是地址`==`比较的是内容

```python
# True
a = 1
b = 1
print(a is b)

# True
a = "good"
b = "good"
print(a is b)

# False
a = "very good morning"
b = "very good morning"
print(a is b)

# False
a = []
b = []
print(a is b)
```
#### 垃圾回收
如果对象的引用计数变为0,就是没有任何引用指向该对象，那么对象就可以被垃圾回收。
但垃圾回收是个费时的操作，python会记录分配对象和取消分配对象的次数，当达到一定阈值时，垃圾回收才会启动。
我们可以通过gc模块的get_threshold()方法来看阈值：
```
import gc
print(gc.get_threshold())
```
返回（700，10，10）,后面的两个10是与分代回收相关的阈值，后面可以看到。700即是垃圾回收启动的阈值。可以通过gc中的set_threshold()方法重新设置。
我们也可以手动启动垃圾回收，即使用gc.collect()。



#### 循环引用

对于循环引用，只有容器对象才会存在该问题，python中的容器对象有list,tuple,dict,class,instances，python的内存管理模块会使用双向链表串联起这些对象，并为它们添加一个新的计数：gc_refs，然后使用以下步骤找出循环引用对象：

1. 设置双向链表中所有对象的gc_refs初始值为其引用计数值
2. 把每个对象中引用的对象的gc_refs值减1
3. 遍历双向链表，移除gc_refs大于1的对象，添加进新的集合中，这些对象的内存不能被释放
4. 遍历集合，在双向链表中找到集合中每个对象引用的对象，并移除，这些对象也不能被释放
5. 双向链表中剩余的对象就是无法访问到的对象，需要被释放



#### 分代回收
存活越久的对象越有价值，我们会减少对它的扫面次数。
Python将所有的对象分为0，1，2三代。所有的新建对象都是0代对象。当某一代对象经历过垃圾回收，依然存活，那么它就被归入下一代对象。垃圾回收启动时，一定会扫描所有的0代对象。如果0代经过一定次数垃圾回收，那么就启动对0代和1代的扫描清理。当1代也经历了一定次数的垃圾回收后，那么会启动对0，1，2，即对所有对象进行扫描。
这两个次数即上面get_threshold()返回的(700, 10, 10)返回的两个10。也就是说，每10次0代垃圾回收，会配合1次1代的垃圾回收；而每10次1代的垃圾回收，才会有1次的2代垃圾回收。



### 多进程和多线程

#### 多进程

这得从操作系统说起。

linux操作系统提供 一个`fork()`系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是`fork()`调用一次，**返回两次**，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。

```python
import os
os.fork()
print 1
```

这个文件运行会打印两次1

子进程永远返回`0`，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用`getppid()`就可以拿到父进程的ID。

Python的`os`模块封装了常见的系统调用，其中就包括`fork`，可以在Python程序中轻松创建子进程：

```python
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

![](http://ojynuthay.bkt.clouddn.com/Process.png)

start()`方法启动，这样创建进程比`fork()`还要简单。

`join()`方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。

##### Pool

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

![](http://ojynuthay.bkt.clouddn.com/processpool.png)

请注意输出的结果，task `0`，`1`，`2`，`3`是立刻执行的，而task `4`要等待前面某个task完成后才执行，这是因为`Pool`的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是`Pool`有意设计的限制，并不是操作系统的限制。如果改成：

```
p = Pool(5)

```

就可以同时跑5个进程。

由于`Pool`的默认大小是CPU的核数，如果你不幸拥有8核CPU，你要提交至少9个子进程才能看到上面的等待效果。



#### 多线程

Python的标准库提供了两个模块：`_thread`和`threading`，`_thread`是低级模块，`threading`是高级模块，对`_thread`进行了封装。绝大多数情况下，我们只需要使用`threading`这个高级模块。

启动一个线程就是把一个函数传入并创建`Thread`实例，然后调用`start()`开始执行：

```python
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

![](http://ojynuthay.bkt.clouddn.com/pythonthread.png)



join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞,这里也就是说一直阻塞主线程，直到threading线程结束，我们该程序才可运行。



#### lock
threading 模块对象：

| threading模块对象    | 解释                                       |
| ---------------- | ---------------------------------------- |
| Thread           | 创建一个可执行的线程对象                             |
| Lock             | 锁原语对象                                    |
| RLock            | 可重入锁对象，使单线程可以获得已经获得了的锁（递归锁定）             |
| Condition        | 条件变量对象能让一个线程停下来，等待其他线程满足了某个条件            |
| Event            | 通用的条件变量。多个线程可以等待某个事件的发生，在事件发生后所有的线程都会被激活 |
| Semaphore        | 为等待锁的线程提供一个类似等待室的结构                      |
| BoundedSemaphore | 与Semaphore类似，只是他不允许超过初始值                 |
| Timer            | 与Thread类似，只是它等待一段时间后才开始运行                |
| activeCount()    | 当前活动的线程数量                                |
| currentThread()  | 返回当前线程对象                                 |
| enumerate()      | 返回当前活动线程的列表                              |
| settrace(func)   | 为所有线程设置一个跟踪函数                            |
| setprofile(func) | 为所有线程设置一个profile函数 threading模块对象         |



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




##### lock

两个线程同时一存一取，就可能导致余额不对，你肯定不希望你的银行存款莫名其妙地变成了负数，所以，我们必须确保一个线程在修改`balance`的时候，别的线程一定不能改。

如果我们要确保`balance`计算正确，就要给`change_it()`上一把锁，当某个线程开始执行`change_it()`时，我们说，该线程因为获得了锁，因此其他线程不能同时执行`change_it()`，只能等待，直到锁被释放后，获得该锁以后才能改。由于锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。创建一个锁就是通过`threading.Lock()`来实现：

```python
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



##### Event

用于线程间通信，即程序中的其一个线程需要通过判断某个线程的状态来确定自己下一步的操作，就用到了event对象

event对象默认为假（Flase），即遇到event对象在等待就阻塞线程的执行。

* 主线程和子线程间通信，代码模拟连接服务器：

```python
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

* 子线程和子线程通信

```python
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

* 多线程阻塞

```python
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



##### 队列

我们先假设有很多个线程，n个消费者，一个生产者，生产者和消费者都不断的运行，那么我们的CUP岂不是在他们之间来回换，看看这个消费者要没要产品，看看生产者产没产出产品，这样太不科学了，我们一应该用队列来存储产品，如果有消费者要就去队列去取，如果没有则等待，可以这样讲队列线程在没有产品的时候设置为event.wait,当有数据的时候设置成event.set通知其他消费者。



#### GIL锁

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。



划重点，无论你有几个cpu，python因为GIL锁的原因只能在一个CPU上工作，多线程也就是快速切换线程.