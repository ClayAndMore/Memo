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

可以看出	 **浅复制副本会共享内部引用**

防止浅复制会出现意外的值，我们需要深复制。



### python自省

这个也是python彪悍的特性.

自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.简单一句就是运行时能够获得对象的类型.比如type(),dir(),getattr(),hasattr(),isinstance().

#### getattr()



#### hasattr(object, name)

说明：判断对象object是否包含名为name的特性（hasattr是通过调用getattr(ojbect, name)是否抛出异常来实现的）。





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

