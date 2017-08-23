---
title: python进阶整理
date: 2017-01-30 08:15:53
categories: python
header-img:
tags: python
---

### 特殊方法
python是多范式语言，既可以面向对象，也可以函数式，依赖于python的对象中的特殊方法。
格式：`_特殊方法名_()`
运算符（如+）、内置函数（如len()）、表元素（如list[3]），有特殊方法的函数可以被认为对象等。

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

### 对象的属性
Python一切皆对象(object)，每个对象都可能有多个属性(attribute)。Python的属性有一套统一的管理方案。
#### 属性的`_dict_`系统
对象的属性储存在对象的`__dict__`属性中。`__dict__`为一个词典，键为属性名，对应的值为属性本身。
```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age

summer = chicken(2)

print(bird.__dict__)
print(chicken.__dict__)
print(summer.__dict__)
```
输出结果：
```
{'__dict__': <attribute '__dict__' of 'bird' objects>, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'bird' objects>, 'feather': True, '__doc__': None}


{'fly': False, '__module__': '__main__', '__doc__': None, '__init__': <function __init__ at 0x2b91db476d70>}


{'age': 2}
```
可以看到，Python中的属性是分层定义的，比如这里分为object/bird/chicken/summer这四层。当我们需要调用某个属性的时候，Python会一层层向上遍历，直到找到那个属性。(某个属性可能出现再不同的层被重复定义，Python向上的过程中，会选取先遇到的那一个，也就是比较低层的属性定义)。
#### 特性
同一个对象的不同属性之间可能存在依赖关系。当某个属性被修改时，我们希望依赖于该属性的其他属性也同时变化。这时，我们不能通过`__dict__`的方式来静态的储存属性。Python提供了多种即时生成属性的方法。其中一种称为特性(property)。特性是特殊的属性。比如我们为chicken类增加一个特性adult。当对象的age超过1时，adult为True；否则为False：
```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age
    def getAdult(self):
        if self.age > 1.0: return True
        else: return False
    adult = property(getAdult)   # property is built-in

summer = chicken(2)

print(summer.adult)
summer.age = 0.5
print(summer.adult)
```
特性使用内置函数property()来创建。property()最多可以加载四个参数。前三个参数为函数，分别用于处理查询特性、修改特性、删除特性。最后一个参数为特性的文档，可以为一个字符串，起说明作用。
进一步说明：
```
class num(object):
    def __init__(self, value):
        self.value = value
    def getNeg(self):
        return -self.value
    def setNeg(self, value):
        self.value = -value
    def delNeg(self):
        print("value also deleted")
        del self.value
    neg = property(getNeg, setNeg, delNeg, "I'm negative")

x = num(1.1)
print(x.neg)
x.neg = -22
print(x.value)
print(num.neg.__doc__)
del x.neg
```
上面的num为一个数字，而neg为一个特性，用来表示数字的负数。当一个数字确定的时候，它的负数总是确定的；而当我们修改一个数的负数时，它本身的值也应该变化。这两点由getNeg和setNeg来实现。而delNeg表示的是，如果删除特性neg，那么应该执行的操作是删除属性value。property()的最后一个参数("I'm negative")为特性negative的说明文档。

#### 使用特殊方法_getattr_
我们可以用__getattr__(self, name)来查询即时生成的属性。当我们查询一个属性时，如果通过__dict__方法无法找到该属性，那么Python会调用对象的__getattr__方法，来即时生成该属性。比如:
```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age
    def __getattr__(self, name):
        if name == 'adult':
            if self.age > 1.0: return True
            else: return False
        else: raise AttributeError(name)

summer = chicken(2)

print(summer.adult)
summer.age = 0.5
print(summer.adult)

print(summer.male)
```
每个特性需要有自己的处理函数，而__getattr__可以将所有的即时生成属性放在同一个函数中处理。__getattr__可以根据函数名区别处理不同的属性。比如上面我们查询属性名male的时候，raise AttributeError。

(Python中还有一个__getattribute__特殊方法，用于查询任意属性。__getattr__只能用来查询不在__dict__系统中的属性)
__setattr__(self, name, value)和__delattr__(self, name)可用于修改和删除属性。它们的应用面更广，可用于任意属性。

#### 静态方法@staticmethod和@classmethod

类中有三个方法，实例方法，静态方法，和类方法。

```python
 
class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)
 
    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)
 
    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x
 
a=A()
```

第一个实例方法，self需要为self传递一个实例，调用时是a.foo(x)。不能A.foo(x)。这里self指的是a.

第二个类方法，cls指的是一个类，不是非得要实例，A.class_foo(x)或a.class_foo(x)。这里的cls指得是A

第三个是静态方法，不需要对谁绑定，a.static_foo(x),A.static_foo(x)都可以。



#### 鸭子类型

当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”

我们并不关心对象是什么类型，到底是不是鸭子，只关心行为。

如果有个飞机类，行为函数fly()。飞。 鸟类，也有个fly().

```python
class Airplane(object):
    def fly(self):
        print('i can fly,i am a airplane')

class Bird(object):
    def fly(self):
        print('i can fly,i am a bird')

def who(object):
    object.fly()

a=Airplane()
b=Bird()
who(a) #i can fly,i am a airplane
who(b) #i can fly,i am a bird
```



### 闭包
Python以函数对象为基础，为闭包这一语法结构提供支持的 (我们在特殊方法与多范式中，已经多次看到Python使用对象来实现一些特殊的语法)。Python一切皆对象，函数这一语法结构也是一个对象。在函数对象中，我们像使用一个普通对象一样使用函数对象，比如更改函数对象的名字，或者将函数对象作为参数进行传递。
一个函数和它的环境变量合在一起，就构成了一个**闭包**(closure)。
在Python中，所谓的闭包是一个包含有环境变量取值的函数对象。环境变量取值被保存在函数对象的__closure__属性中。比如下面的代码：
```python
def line_conf():
    b = 15
    def line(x):
        return 2*x+b
    return line       # return a function object

b = 5
my_line = line_conf()
print(my_line.__closure__)
print(my_line.__closure__[0].cell_contents)
```
按理说用函数的时候会调用环境中存在的值b=5,但是实际上用的定义时的b=15。
简单来说：**闭包是函数被调用时，用的是定义时的值，不是当前存在的值**。
看一个实际例子：
```python
def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))
```
环境line和环境a,b构成闭包，通过参数a,b最终确定了形式 a*x+b,只要换a,b的值，就可以获得不同的直线表达函数，由此，闭包具有提高代码可复用性的作用。
如果没有闭包，我们需要每次创建直线函数的时候同时说明a,b,x。这样，我们就需要更多的参数传递，也减少了代码的可移植性。

#### 闭包与并行计算
闭包有效的减少了函数所需定义的参数数目。这对于并行运算来说有重要的意义。在并行运算的环境下，我们可以让每台电脑负责一个函数，然后将一台电脑的输出和下一台电脑的输入串联起来。最终，我们像流水线一样工作，从串联的电脑集群一端输入数据，从另一端输出数据。这样的情境最适合只有一个参数输入的函数。闭包就可以实现这一目的。

并行运算正成为一个热点。这也是函数式编程又热起来的一个重要原因。函数式编程早在1950年代就已经存在，但应用并不广泛。然而，我们上面描述的流水线式的工作并行集群过程，正适合函数式编程。由于函数式编程这一天然优势，越来越多的语言也开始加入对函数式编程范式的支持。
<hr>

一个有意义的闭包，根据总数求平均值：

```python
def avg():
	all = []
	def get_avg(x):
		 all.append(x)
		 total = sum(all)
		 return total/len(all)
	return get_avg
  
a = avg()
a(10)
a(11)
```



#### 闭包中的陷阱和nonlocal





### 装饰器
装饰器可以对一个函数、方法或者类进行加工。
先看这样的代码：
```python
# get square sum
def square_sum(a, b):
    print("intput:", a, b)
    return a**2 + b**2

# get square diff
def square_diff(a, b):
    print("input", a, b)
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))
```
两个计算函数，分别有输出。我们用装饰器把输出函数提出去：
```python
def decorator(F):
    def new_F(a, b):
        print("input", a, b)
        return F(a, b)
    return new_F

# get square sum
@decorator
def square_sum(a, b):
    return a**2 + b**2

# get square diff
@decorator
def square_diff(a, b):
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))
```
定义好装饰器后，我们就可以通过@语法使用了。在函数square_sum和square_diff定义之前调用@decorator，我们实际上将square_sum或square_diff传递给decorator，并将decorator返回的新的可调用对象赋给原来的函数名(square_sum或square_diff)。 所以，当我们调用square_sum(3, 4)的时候，就相当于：
```
square_sum = decorator(square_sum)
square_sum(3, 4)
```
我们知道，Python中的变量名和对象是分离的。变量名可以指向任意一个对象。从本质上，装饰器起到的就是这样一个重新指向变量名的作用(name binding)，让同一个变量名指向一个新返回的可调用对象，从而达到修改可调用对象的目的。

与加工函数类似，我们可以使用装饰器加工类的方法。

如果我们有其他的类似函数，我们可以继续调用decorator来修饰函数，而不用重复修改函数或者增加新的封装。这样，我们就提高了程序的可重复利用性，并增加了程序的可读性。

#### 含参的装饰器
```python
# a new wrapper layer
def pre_str(pre=''):
    # old decorator
    def decorator(F):
        def new_F(a, b):
            print(pre + "input", a, b)
            return F(a, b)
        return new_F
    return decorator

# get square sum
@pre_str('^_^')
def square_sum(a, b):
    return a**2 + b**2

# get square diff
@pre_str('T_T')
def square_diff(a, b):
    return a**2 - b**2

print(square_sum(3, 4))
print(square_diff(3, 4))
```
上面的pre_str是允许参数的装饰器。它实际上是对原有装饰器的一个函数封装，并返回一个装饰器。我们可以将它理解为一个含有环境参量的闭包。当我们使用@pre_str('^_^')调用的时候，Python能够发现这一层的封装，并把参数传递到装饰器的环境中。该调用相当于:
`square_sum = pre_str('^_^') (square_sum)`

#### 装饰类
```python
def decorator(aClass):
    class newClass:
        def __init__(self, age):
            self.total_display   = 0
            self.wrapped         = aClass(age)
        def display(self):
            self.total_display += 1
            print("total display", self.total_display)
            self.wrapped.display()
    return newClass

@decorator
class Bird:
    def __init__(self, age):
        self.age = age
    def display(self):
        print("My age is",self.age)

eagleLord = Bird(5)
for i in range(3):
    eagleLord.display()
```
在decorator中，我们返回了一个新类newClass。在新类中，我们记录了原来类生成的对象（self.wrapped），并附加了新的属性total_display，用于记录调用display的次数。我们也同时更改了display方法。

通过修改，我们的Bird类可以显示调用display的次数了。

<hr>

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

linux操作系统提供 一个`fork()`系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是`fork()`调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。

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

#### lock

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

#### GIL锁

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

