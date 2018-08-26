### bisect

Bisect 是利用二分法来实现有序数组的查询和插入的。

`Bisect(haystack, needle)`

在haystack(这是一个有序数列)里搜索needle的位置

该位置满足把needle插入这个位置后，haystack还能保持升序(如果原来是降序，可以先resersed()一下。

```python
>>> import bisect
>>> a=[2,4,6,8]
>>> bisect.bisect(a, 5) #5会在a[2]的位置
2
>>> bisect.bisect(a, 4) #4也在a[2]的位置
2
>>>>>> bisect.insort(a, 5) # 直接插入并排序
>>> a
[2, 4, 5, 6, 8]
```

一个实用的demo：

```python
# 根据成绩来判断成绩评级
def grade(score, breakpoints=[60,70,80,90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]
[grade(score) for in [33,99,77,70,89,90,100]]
['F', 'A', 'C', 'C', 'B', 'A', 'A']
```



### inspect

#### signatrue

提取函数签名

```python
def clip(text, max_len=80):
    ...
     
from inspect import signature
sig = signature(clip)
str(sige)
'(text, max_len=80)'
for name, param in sig.parameters.items():
    print name, param.kind, param.default
 
text POSITIONAL_OR_KEYWORD <class 'inspect._empty'
max_len POSITIONAL_OR_KEYWORD 80
```





### csv



### ast





### functools

python2.5 引进

#### 偏函数partial

和数学中的偏函数不一样，说白了它可以帮你用一个已知函数固定其中参数的值生成一个参数少传一些的函数：

用法： new_func = partial(func, 固定参数)

```python
# coding:utf-8
from functools import partial
def func(a, b, c):
    print a, '@', b, '@', c

par_func = partial(func, 1)
print '指定一个参数'
par_func(2,3)
#par_func(0,2,3)

print '指定两个参数'
par_func = partial(func, 1, 2)
par_func(3)

print '指定三个参数'
par_func = partial(func, 1,2,3)
par_func()

### 默认参数

def default(a, b='bb',c='cc'):
    print a, b,c

par_default = partial(default, 1)
print '默认参数'
par_default(3)

## 可变参数和关键字参数
def alterable(*args, **kwargs):
    print args
    print kwargs

print '可变参数和关键字参数'
par_alterable = partial(alterable, 1,2, a='aa')
par_alterable(3,4,5,b='bb',c='cc')
```

输出：

```
指定一个参数
1 @ 2 @ 3
指定两个参数
1 @ 2 @ 3
指定三个参数
1 @ 2 @ 3
默认参数
1 3 cc
可变参数和关键字参数
(1, 2, 3, 4, 5)
{'a': 'aa', 'c': 'cc', 'b': 'bb'}
```

在介绍函数参数的时候，我们讲到，通过设定参数的默认值，可以降低函数调用的难度。而偏函数也可以做到这一点。举例如下：

`int()`函数可以把字符串转换为整数，当仅传入字符串时，`int()`函数默认按十进制转换：

```
>>> int('12345')
12345



```

但`int()`函数还提供额外的`base`参数，默认值为`10`。如果传入`base`参数，就可以做N进制的转换：

```
>>> int('12345', base=8)
5349
>>> int('12345', 16)
74565



```

假设要转换大量的二进制字符串，每次都传入`int(x, base=2)`非常麻烦，于是，我们想到，可以定义一个`int2()`的函数，默认把`base=2`传进去：

```
def int2(x, base=2):
    return int(x, base)



```

这样，我们转换二进制就非常方便了：

```
>>> int2('1000000')
64
>>> int2('1010101')
85



```

`functools.partial`就是帮助我们创建一个偏函数的，不需要我们自己定义`int2()`，可以直接使用下面的代码创建一个新的函数`int2`：

```
>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85



```

所以，简单总结`functools.partial`的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。

注意到上面的新的`int2`函数，仅仅是把`base`参数重新设定默认值为`2`，但也可以在函数调用时传入其他值：

```
>>> int2('1000000', base=10)
1000000


```



#### wraps

让被装饰的函数不改变func.name 和doc

```python
from functools import wraps
def my_decorator(f):
    #@wraps(f)
    def wrapper(*args, **kwds):
        print 'Calling decorated function'
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print 'Called example function'

example()
#Calling decorated function
#Called example function
print example.__name__
#'example', 去掉@wraps, 则是wrapper
print example.__doc__
#'Docstring', 去掉@wraps, 为None,也就是wrapper的doc
```

这样的目的是使其看起来更像被包裹（wrapped）的函数； 





### hashlib

使用python求字符串或文件的MD5 

字符串md5:

```python
>>> import hashlib
>>> hashlib.md5("filename.exe").hexdigest()
'2a53375ff139d9837e93a38a279d63e5'
```



求文件md5

```python
>>> import hashlib
>>> hashlib.md5(open('filename.exe','rb').read()).hexdigest()
'd41d8cd98f00b204e9800998ecf8427e'

def _get_md5(filepath):
    md5 = ''
    with open(filepath) as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        return md5

```





较大文件处理：

```python
import hashlib
import os

def get_md5_02(file_path):
  f = open(file_path,'rb')  
  md5_obj = hashlib.md5()
  while True:
    d = f.read(8096)
    if not d:
      break
    md5_obj.update(d)
  hash_code = md5_obj.hexdigest()
  f.close()
  md5 = str(hash_code).lower()
  return md5

if __name__ == "__main__":
  file_path = r'D:\test\test.jar'
  md5_02 = get_md5_02(file_path)
  print(md5_02)
```





### asyncore

异步socket 包装，我们操作网络的时候可以直接使用socket等底层的库，但是asyncore使得我们可以更加方便的操作网络，避免直接使用socket，select，poll等工具时需要面对的复杂。 

这个库只要了解两点： 

* loop函数

  oop()函数负责检测一个dict，dict中保存dispatcher的实例，这个字典被称为channel。每次创建一个dispatcher对象，都会把自己加入到一个默认的dict里面去（当然也可以自己指定channel）。当对象被加入到channel中的时候，socket的行为都已经被定义好，程序只需要调用loop()，一切功能就实现了。 

* dispatcher 基类

  每一个从dispatcher继承的类的对象，都可以看作我们需要处理的一个socket，可以是TCP连接或者UDP，甚至是其它不常用的。使用容易，我们需要定义一个类，它继承dispatcher，然后我们重写（覆盖）一些方法就可以了。 



在python的标准文档中，有一个asyncore的例子

```python
import asyncore， socket
class http_client(asyncore.dispatcher):
  def __init__(self， host， path):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET， socket.SOCK_STREAM)
    self.connect( (host， 80) )
    self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path
  def handle_connect(self):
    pass
  def handle_close(self):
    self.close()
  def handle_read(self):
    print self.recv(8192)
  def writable(self):
    return (len(self.buffer) > 0)
  def handle_write(self):
    sent = self.send(self.buffer)
    self.buffer = self.buffer[sent:]
c = http_client('www.python.org'， '/')
asyncore.loop()
```

运行这个函数，发现python.org的首页被下载下来了，也就是说我们实现了一个http层的协议。但是我们用的仅仅是socket级别的API…那么来看看这几行代码的奥妙吧。

writable和readable在检测到一个socket可以写入或者检测到数据到达的时候，被调用，并返回一个bool来决定是否handle_read或者handle_write

打开asyncore.py可以看到，dispatcher类中定义的方法writable和readable的定义相当的简单：

```
def readable(self):
  return True
def writable(self):
  return True
```

就是说，一旦检测到可读或可写，就直接调用handle_read/handle_write，但是在上面的例子中，我们却看到了一个重载（看上去像C++的虚函数，不是吗。）

```
def writable(self):
  return (len(self.buffer) > 0)
```

很明显，当我们有数据需要发送的时候，我们才给writable的调用者返回一个True，这样就不需要在handle_write中再做判断了，逻辑很明确，代码很清晰，美中不足的是理解需要一点时间，但是不算困难吧。

其余的代码看起来就很清晰了，有一种兵来将挡的感觉。当一个http服务器发送处理完成你的请求，close socket的时候，我们的handle_close()也相应完成自己的使命。close()将对象自身从channel中删除，并且负责销毁socket对象。

```
def close(self):
  self.del_channel()
  self.socket.close()
```

loop()函数检测到一个空的channel，将退出循环，程序完成任务，exit。



封装了select的一些异步函数。