---
title: python整理（三）
date: 2017-04-07 14:58:44
categories: python
header-img: 
tags: python
---



### 浅拷贝和深拷贝

可变类型：list , set , dict

不可变类型：int, str , float , tuple

不可变类型是谈不上拷贝的，只有可变类型能谈得上拷贝。

浅复制方法：[:] , copy.copy() ,  
深复制方法：copy.deepcopy()

```python
import copy
a = [1, 2, 3, 4, ['a', 'b']]  #原始对象
 
b = a  #赋值，传对象的引用
c = copy.copy(a)  #对象拷贝，浅拷贝
d = copy.deepcopy(a)  #对象拷贝，深拷贝
 
a.append(5)  #修改对象a
a[4].append('c')  #修改对象a中的['a', 'b']数组对象
 
print 'a = ', a
print 'b = ', b
print 'c = ', c
print 'd = ', d
 
输出结果：
a =  [1, 2, 3, 4, ['a', 'b', 'c'], 5]
b =  [1, 2, 3, 4, ['a', 'b', 'c'], 5]
c =  [1, 2, 3, 4, ['a', 'b', 'c']]
d =  [1, 2, 3, 4, ['a', 'b']]
```



- **hasattr(object, name)**

说明：判断对象object是否包含名为name的特性（hasattr是通过调用getattr(ojbect, name)是否抛出异常来实现的）。



### python自省

这个也是python彪悍的特性.

自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.简单一句就是运行时能够获得对象的类型.比如type(),dir(),getattr(),hasattr(),isinstance().

#### getattr()





### python2和python3区别

http://python.jobbole.com/80006/

#### 字符

python2 有基于ASCII的str()类型，可以通过单独的unicode()转换成unicode类型，但没有byte类型。

python2中不要以0开头来创建一些数据。尽量把开头的零去掉，在python3中不会这样。



#### xrange

python2会常用xrange()创建一个可迭代对象，通常出现在for循环或列表，集合，字典，推导式中。

这里的xrange和python3中的range一样，惰性求值，意味这可以在其上面无限取值。

python2 中range()也可以用，通常比xrange快一点，不过不建议多次迭代中用range,因为range()每次都会在内存中重新生成一个列表。



#### 触发异常

raise  IOError,'file error'

raise  IOError('file error')

python3支持第二种。

异常处理：

```
try:
	....
except NameError,err:  #python3中得变成except NameError as err:
	print err,'our error message'
```



#### for循环变量与全局命名空间泄漏

python2:

```python
i=1
print 'before: i=',i
print [i for i in range(5)]
print 'after: i=',i
```

```
before: i=1
[0,1,2,3,4]
after: i=4
```

python3 改进了，after:i=1



#### input输入

python3用户输入默认储存为str的对象。

python2 中，会判断你的输入而储存为相应对象，如输入123，则存为int对象。

为了避免非字符输入的危险行为，使用raw_input()代替input.这时，再输入123，则存为str对象。

```
>>>my_input=raw_input('enter a number')
123
>>>type(my_input)
<type 'str'>
```



#### 返回可迭代对象，而不是列表

python2中有些迭代函数返回的是列表，而不是可迭代类型。

python2:

```
print range(3)
print type((range(3)))
out:
[0,1,2]
<type 'list'>
```

python3:

```
print (range(3))
print (type(range3))
range(0,3)
<class 'range'>
```





### python中的异步

#### 理解yield

粗略知道yield可以作为一个函数返回值：

```python
def addlist(alist):
	for i in alist:
		yield i+1
	
alist=[1,2,3,4]
for x in addlist(alist):
	print(x)
```

输出：2，3，4，5

某个函数包含了yield，这意味着这个函数已经是一个Generator，它的执行会和其他普通的函数有很多不同。

```python
def h():
	print('aaa')
	yield 5
h()
```

这个h()并不能输出aaa,因为它有yield表达式，因此，我们通过`__next()__`语句让它执行。

##### `__next__()`

next()语句将恢复Generator执行，并直到下一个yield表达式处.

```python
def h():
	print("aaa")
	yield 5
	print("bbb")
	yield 12
c=h()
c.__next__()
```

输出: aaa 5

再次调用nex()时，会找到下一个yield，输出bbb 12.



##### **yield是表达式**

`m=yield 5`

表达式(yield 5)的返回值将赋值给m，所以，认为 m = 5 是错误的。那么如何获取(yield 5)的返回值呢？需要用到后面要介绍的send(msg)方法。

##### send(msg)

其实next()和send()在一定意义上作用是相似的，区别是send()可以传递yield表达式的值进去，而next()不能传递特定的值，只能传递None进去。因此，我们可以看做

c.next() 和 c.send(None) 作用是一样的。

```python
def h():
    print("aaa")  
    m=yield 5   
    print(m)
    d=yield 12
    print(d)
    print("bbb")
    n=yield 13

c=h()
c.__next__() #c.next() 和 c.send(None) 作用是一样的。
c.__next__() #yield 5被赋予了None
c.send('ccc')#yeild 12表达式被赋予了ccc
```

输出：

```
aaa 
None
ccc
bbb
```

这个示例会执行到 yield 13再次执行会出现异常，因为后面没有yield.

**注意：**第一次调用时，请使用next()语句或是send(None)，不能使用send发送一个非None的值，否则会出错的，因为没有yield语句来接收这个值。

##### send(msg) 与 next()的返回值

end(msg) 和 next()是有返回值的，它们的返回值很特殊，返回的是**下一个**yield表达式的参数。比如yield 5，则返回 5 。这可以看出我们第一个代码示例中为什么输出5了。

但是有send(msg)传入值，则会返回传入的值。

##### 中断Generator

可以通过throw抛出一个GeneratorExit异常来终止Generator。Close()方法作用是一样的，其实内部它是调用了throw(GeneratorExit)的。我们看：

```python
def close(self):
    try:
        self.throw(GeneratorExit)
    except (GeneratorExit, StopIteration):
        pass
    else:
        raise RuntimeError("generator ignored GeneratorExit")
# Other exceptions are not caught
```

因此，当我们调用了close()方法后，再调用next()或是send(msg)的话会抛出一个异常.



### 协程

子程序，或者称为函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。

所以子程序调用是通过栈实现的，一个线程就是执行一个子程序。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

注意，在一个子程序中中断，去执行其他子程序，不是函数调用，有点类似CPU的中断。

#### 那和多线程比，协程有何优势？

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。

Python对协程的支持是通过generator实现的。

#### 生产者消费者模型

传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。

如果改用协程，生产者生产消息后，直接通过`yield`跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：

```python
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[消费者] 消费了 %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[生产者] 生产了 %s...' % n)
        r = c.send(n)
        print('[生产者] 消费者返回状态: %s' % r)
    c.close()

c = consumer()
produce(c)
```

输出：

![](http://ojynuthay.bkt.clouddn.com/custormReturn.png)

思路分析：

- c=consumer() 只是赋值，函数并不会执行
- c.send(None),等同于`c.__next__()`，consumer()执行到n=yield '',则停止，继续produce()的语句
- n=0, while ...输出生产者生产了1
- r=c.send(1) ,将yield表达式赋值为1，此时n是1，if not 内不执行，然后打印消费者。
- 此时customer()中r='200 ok',send()的返回值是下个yield表达式的参数。所以produce()中r=send(n)等于‘200 ok'
- close()关闭协程。

### asynico

`asyncio`是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

用`asyncio`提供的`@asyncio.coroutine`可以把一个generator标记为coroutine类型，然后在coroutine内部用`yield from`调用另一个coroutine实现异步操作。

`asyncio`的编程模型就是一个消息循环。我们从`asyncio`模块中直接获取一个`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

用`asyncio`实现`Hello world`代码如下：

```python
import asyncio

@asyncio.coroutine #把一个generator标记为coroutine类型，然后，我们就把这个coroutine扔到EventLoop中执行。
def hello():
    print('Hello world')
    r=yield from asyncio.sleep(3)
    print('Hello again')

loop=asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
```

两个coroutine:

```python
import threading
import asyncio

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

![](http://ojynuthay.bkt.clouddn.com/asynchronous.png)



`hello()`会首先打印出`Hello world!`，然后，`yield from`语法可以让我们方便地调用另一个`generator`。由于`asyncio.sleep()`也是一个`coroutine`，所以线程不会等待`asyncio.sleep()`，而是直接中断并执行下一个消息循环。当`asyncio.sleep()`返回时，线程就可以从`yield from`拿到返回值（此处是`None`），然后接着执行下一行语句。

把`asyncio.sleep(1)`看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行`EventLoop`中其他可以执行的`coroutine`了，因此可以实现并发执行。



### async/await

用`asyncio`提供的`@asyncio.coroutine`可以把一个generator标记为coroutine类型，然后在coroutine内部用`yield from`调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法`async`和`await`，可以让coroutine的代码更简洁易读。

请注意，`async`和`await`是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

1. 把`@asyncio.coroutine`替换为`async`；
2. 把`yield from`替换为`await`。

让我们对比一下上一节的代码：

```python
@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")
```

用新语法重新编写如下：

```python
async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")
```

 



### python 面试题

#### 参数传递

```python
a = 1
def fun(a):
    a = 2
fun(a)
print(a)  #1

a=[]
def fun(a):
    a.append(1)
fun(a)
print(a) #a[1]
```

传递时是引用传递，如果是不可变对象，如第一个例子，会复制一个引用传入参数，而原来的引用不变。

如果是可变对象，如第二个例子，会直接操作引用的地址。

下面的例子也是一样的：

```python
class Person:
    name="aaa"
 
p1=Person()
p2=Person()
p1.name="bbb"
print p1.name  # bbb
print p2.name  # aaa
print Person.name  # aaa
====================

class Person:
    name=[]
 
p1=Person()
p2=Person()
p1.name.append(1)
print p1.name  # [1]
print p2.name  # [1]
print Person.name  # [1]
```



#### 单例模式

`__new__`版本

```python
class Singleton(object):
    _instance=None #保存实例的引用

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._instance

one=Singleton()
two=Singleton()

print(one is two)
```

在上面的代码中，我们将类的实例和一个类变量 `_instance` 关联起来，如果 `cls._instance` 为 None 则创建实例，否则直接返回 `cls._instance`。

import版本

 mysingle.py

```python
class My_Single(object):
	def foo(self):
		pass
my_single=My_Single()

from mysingle import my_single

my_single.foo()
```

装饰器版本：

```python

def single(cls):
	instances={}
	def getinstance(*args,**kwargs):
		if cls not in instances:
			instances[cls]=cls(*args,**kwargs)
		return instances[cls]
	return getinstance

@single
class MyClass(object):
    a=1

a=MyClass()
b=MyClass()
print(a is b)
```





#### read,readline,readlines

- read 读取整个文件
- readline 读取下一行,使用生成器方法
- readlines 读取整个文件到一个迭代器以供我们遍历

