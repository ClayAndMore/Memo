tags: [python] date: 2017-01-30




### 内存管理
为了探索对象在内存的存储，我们可以求助于Python的内置函数id()。它用于返回对象的身份(identity)。其实，这里所谓的身份，就是该对象的内存地址。
`a=1
print(id(a))`
输出11246696
这就是1的内存地址，a为地址的引用。
**python 对于相同整数和短字符串，保留了同一份引用。对于其它，即使内容相同，还是创建新的对象。**



#### is 和 ==

is()函数可以判断是不是同一个引用。

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

#### 

is 运算符比 == 速度快， 因为它不能重载， 不用找特殊方法，而是直接比较两个整数id.

而 == 是语法糖， 等同于`a.__eq__(b)`.  




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



#### 分代回收

存活越久的对象越有价值，我们会减少对它的扫面次数。
Python将所有的对象分为0，1，2三代。所有的新建对象都是0代对象。当某一代对象经历过垃圾回收，依然存活，那么它就被归入下一代对象。垃圾回收启动时，一定会扫描所有的0代对象。如果0代经过一定次数垃圾回收，那么就启动对0代和1代的扫描清理。当1代也经历了一定次数的垃圾回收后，那么会启动对0，1，2，即对所有对象进行扫描。
这两个次数即上面get_threshold()返回的(700, 10, 10)返回的两个10。也就是说，每10次0代垃圾回收，会配合1次1代的垃圾回收；而每10次1代的垃圾回收，才会有1次的2代垃圾回收。



#### 引用计数

在cpython 中， 垃圾回收的主要算法是引用计数，每个对象会统计有多少个引用指向自己。



#### 循环引用

对于循环引用，只有容器对象才会存在该问题，python中的容器对象有list,tuple,dict,class,instances，python的内存管理模块会使用双向链表串联起这些对象，并为它们添加一个新的计数：gc_refs，然后使用以下步骤找出循环引用对象：

1. 设置双向链表中所有对象的gc_refs初始值为其引用计数值
2. 把每个对象中引用的对象的gc_refs值减1
3. 遍历双向链表，移除gc_refs大于1的对象，添加进新的集合中，这些对象的内存不能被释放
4. 遍历集合，在双向链表中找到集合中每个对象引用的对象，并移除，这些对象也不能被释放
5. 双向链表中剩余的对象就是无法访问到的对象，需要被释放

一组相互引用的对象若没有被其它对象直接引用，并且不可访问，则会永久存活下来。一个应用程序如果持续地产生这种不可访问的对象群组，就会发生内存泄漏。

```python
# -*- coding:utf-8 -*-
import weakref
import gc
from pprint import pprint


class Graph(object):
    def __init__(self, name):
        self.name = name
        self.other = None

    def set_next(self, other):
        print "%s.set_next(%r)" % (self.name, other)
        self.other = other

    def all_nodes(self):
        yield self
        n = self.other
        while n and n.name !=self.name:
            yield n
            n = n.other
        if n is self:
            yield n
        return

    def __str__(self):
        return "->".join(n.name for n in self.all_nodes())

    def __repr__(self):
        return "<%s at 0x%x name=%s>" % (self.__class__.__name__, id(self), self.name)

    def __del__(self):
        print "(Deleting %s)" % self.name

def collect_and_show_garbage():
 	'''
 	第一次打印：
 	Collecting...
    unreachable objects: 0
    garbage:[]
    第二次打印：
    After 2 references removed
    one->two->three->one
    Collecting...
    unreachable objects: 0
    garbage:[]
    下面注释为第三次打印：
 	'''   

    
    print "Collecting..."
    n = gc.collect() # gc.collect() 收集垃圾
    print "unreachable objects:", n
    '''
    Collecting...
    gc: uncollectable <Graph 0x1097891d0>
    gc: uncollectable <Graph 0x109789210>
    gc: uncollectable <Graph 0x109789250>
    gc: uncollectable <dict 0x10977e7f8>
    gc: uncollectable <dict 0x109780c58>
    gc: uncollectable <dict 0x1097805c8>
    '''
    print "garbage:", 
    pprint(gc.garbage) # gc.garbage 获取垃圾列表
    '''
    [<Graph at 0x1097891d0 name=one>,
     <Graph at 0x109789210 name=two>,
     <Graph at 0x109789250 name=three>,
     {'name': 'one', 'other': <Graph at 0x109789210 name=two>},
     {'name': 'two', 'other': <Graph at 0x109789250 name=three>},
 {   'name': 'three', 'other': <Graph at 0x1097891d0 name=one>}]
    '''


def demo(graph_factory):
    print "Set up graph:"
    one = graph_factory("one") 
    two = graph_factory("two")
    three = graph_factory("three")
    one.set_next(two)   # one.set_next(<Graph at 0x109789210 name=two>)
    two.set_next(three) # two.set_next(<Graph at 0x109789250 name=three>)
    three.set_next(one) # three.set_next(<Graph at 0x1097891d0 name=one>)

    print
    print "Graph:"
    print str(one)  # one->two->three->one
    collect_and_show_garbage()

    print
    three = None
    two = None
    print "After 2 references removed"
    print str(one)
    collect_and_show_garbage()

    print
    print "removeing last reference"
    one = None
    collect_and_show_garbage()


gc.set_debug(gc.DEBUG_LEAK) #gc.set_debug(gc.DBEUG_LEAK) 打印无法看到的对象信息
print "Setting up the cycle"
print 
demo(Graph)
print
print "breaking the cycle and cleaning up garbage"
print
gc.garbage[0].set_next(None)
while gc.garbage:
    del gc.garbage[0]
print collect_and_show_garbage()
'''
Collecting...
unreachable objects: 0
garbage:[]
None
[Finished in 0.4s]c: uncollectable <Graph 025C9E50>
gc: uncollectable <Graph 025C9E70>
gc: uncollectable <Graph 025C9E90>
gc: uncollectable <dict 025D3030>
gc: uncollectable <dict 025D30C0>
gc: uncollectable <dict 025C1F60>
'''
```

从结果中我们可以看出，即使我们删除了Graph实例的本地引用，它依然存在垃圾列表中，不能回收。

接下来创建使弱引用的WeakGraph类：

```python
class WeakGraph(Graph):
    def set_next(self, other):
        if other is not None:
            if self in other.all_nodes():
                other = weakref.proxy(other)
        super(WeakGraph, self).set_next(other)
        return
demo(WeakGraph)
```

如果想同时创建多个对象的弱引用咋办？这时可以使用`WeakKeyDictionary`和`WeakValueDictionary`来实现。

`WeakValueDictionary`类，顾名思义，本质上还是个字典类型，只是它的值类型是弱引用。当这些值引用的对象不再被其他非弱引用对象引用时，那么这些引用的对象就可以通过垃圾回收器进行回收。
下面的例子说明了常规字典与`WeakValueDictionary`的区别。

```python
# -*- coding:utf-8 -*-
import weakref
import gc
from pprint import pprint

gc.set_debug(gc.DEBUG_LEAK)


class Man(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Man name=%s>' % self.name

    def __del__(self):
        print "deleting %s" % self


def demo(cache_factory):
    all_refs = {}
    print "cache type:", cache_factory
    cache = cache_factory()
    for name in ["Jim", 'Tom', 'Green']:
        man = Man(name)
        cache[name] = man
        all_refs[name] = man
        del man
    print "all_refs=",
    pprint(all_refs)
    print
    print "before, cache contains:", cache.keys()
    for name, value in cache.items():
        print "%s = %s" % (name, value)
    print "\ncleanup"
    del all_refs
    gc.collect()

    print
    print "after, cache contains:", cache.keys()
    for name, value in cache.items():
        print "%s = %s" % (name, value)
    print "demo returning"
    return

demo(dict)
print

demo(weakref.WeakValueDictionary)
```






#### 弱引用和weakref
弱引用，与强引用相对，是指不能确保其引用的对象不会被垃圾回收器回收的引用。
一个对象若只被弱引用所引用，则可能在任何时刻被回收。
弱引用的主要作用就是减少循环引用，减少内存中不必要的对象存在的数量。

在对象群组内部使用弱引用（即不会在引用计数中被计数的引用）有时能避免出现引用环，因此弱引用可用于解决循环引用的问题。

使用weakref模块，你可以创建到对象的弱引用，Python在对象的引用计数为0或只存在对象的弱引用时将回收这个对象。
你可以通过调用weakref模块的`ref(obj[,callback])`来创建一个弱引用，obj是你想弱引用的对象，callback是一个可选的函数，当因没有引用导致Python要销毁这个对象时调用。回调函数callback要求单个参数（弱引用的对象）。

```python
>>>>　import　sys
>>>　import　weakref
>>>　class　Man:
　　def　__init__(self,name):
　　　　print　self.name = name
　　　　
>>>　o　=　Man('Jim')
>>>　sys.getrefcount(o)   
2
>>>　r　=　weakref.ref(o)　#　创建一个弱引用
>>>　sys.getrefcount(o)　#　引用计数并没有改变
2
>>>　r
<weakref　at　00D3B3F0;　to　'instance'　at　00D37A30>　#　弱引用所指向的对象信息
>>>　o2　=　r()　#　获取弱引用所指向的对象
>>>　o　is　o2
True
>>>　sys.getrefcount(o)
3
>>>　o　=　None
>>>　o2　=　None
>>>　r　#　当对象引用计数为零时，弱引用失效。
<weakref　at　00D3B3F0;　dead>de>

```

sys包中的`getrefcount()`来查看某个对象的引用计数。需要注意的是，当使用某个引用作为参数，传递给`getrefcount()`时，参数实际上创建了一个临时的引用。因此，getrefcount()所得到的结果，会比期望的多1。



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
c = copy.copy(a)  #对象拷贝，浅拷贝， [:]效果一样
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

Class 文档里有说明

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



