Tags:[python,py_lib]

### random

计算机不会产生绝对随机的随机数，计算机只能产生“伪随机数”。

一定的方法，一定的规律 产生的随机数也是固定的，所以我们要喂一个数字来影响随机数的产生，达到一定的随机。还有的是通过移动内存内的位置产生随机， 不太系统不太相同。

* random.seed()   喂随机数  eg:`random.seed(time.time())`

* random.random()用于生成一个0到1的随机符点数: 0 <= n < 1.0

* random.uniform的函数原型为：random.uniform(a, b)，用于生成一个指定范围内的随机符点数，两个参数其中一个是上限，一个是下限。

* random.randint(a, b)，用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n: a <= n <= b

* random.choice从序列中获取一个随机元素。

  ```python
  print random.choice("学习Python")   
  print random.choice(["JGood", "is", "a", "handsome", "boy"])  
  print random.choice(("Tuple", "List", "Dict"))  
  ```

* random.shuffle(x[, random])，用于将一个列表中的元素打乱。如:

  ```python
  p = ["Python", "is", "powerful", "simple", "and so on..."]  
  random.shuffle(p)  
  print p 
  #['powerful', 'simple', 'is', 'Python', 'and so on...'] 
  ```

* random.sample(sequence, k)，从指定序列中随机获取指定长度的片断。sample函数不会修改原有序列。

  ```python
  list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
  slice = random.sample(list, 5)  #从list中随机获取5个元素，作为一个片断返回  
  ```



### shutil



#### copy文件

* `shutil.copymode(src, dst)`

  复制 `src` 的文件**权限位**到 `dst` 。 文件的内容、属主和用户组不会受影响。

* `shutil.copystat(src, dst)`

  复制文件 `src` 的文件**权限位**、**最后访问 access 时间**、**最后修改 modification 时间**和**标识 flags **到 `dst`。文件的内容、属主和用户组不会受影响。 时间和标识等可以理解为元数据。

* `shutil.copyfileobj(fsrc, fdst[, length])`

  对象 `fsrc` 的内容到类文件对象 `fdst`。 可选**整数参数** `length`， 指定缓冲区大小。

  具体而言， `length` 的值为负数，复制操作不会将源数据分块进行复制。

  默认的，为了避免不可控制的内存消耗，数据会被分块存入chunk中。 

  **注意：** 如果 `fsrc` 对象的当前文件位置不为 0 ，则只有从当前文件位置到文件末位的内容会被复制。

  eg:

  ```python
  with open(src, 'rb') as f1,open(os.path.join(dst,'test.pdf'), 'wb') as f2:
  	shutil.copyfileobj(f1, f2)
  ```

* `shutil.copyfile(src, dst)`

  复制文件 `src` 的内容（不包含元素据）到文件 `dst` 中。

   `dst` 必须为一个完整的目标文件, 可以不存在。

   `src` 和 `dst` 不能为同一个文件，否则会报错。 

  如果 `dst` 已经存在，则会被覆盖。

  目标文件位置必须为可写状态，否则会触发  IOError。 

   特别的， 字符设备、块设备和管道不能使用此方法复制。 

* `shutil.copy(src, dst)`

  复制文件 `src` 到 `dst` 文件或文件夹中。 如果 `dst` 是文件夹， 则会在文件夹中创建或覆盖一个文件，且该文件与 `src` 的文件名相同。 文件权限位会被复制(可执行等).

* `shtil.copy2(src, dst)`

  与 `shutil.copy()` 类似，另外会同时复制文件的元数据。 实际上，该方法是 `shutil.copy()` 和 `shutil.copystat()` 组合。该方法相当于 Unix 命令的 ` cp -p `。



```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Function              preserves     supports          accepts     copies other
                      permissions   directory dest.   file obj    metadata  
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
shutil.copy              ✔             ✔                 ☐           ☐
shutil.copy2             ✔             ✔                 ☐           ✔
shutil.copyfile          ☐             ☐                 ☐           ☐
shutil.copyfileobj       ☐             ☐                 ✔           ☐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

* copytree:

  ```python
  import shutil, errno
  
  def copyanything(src, dst):
      try:
          shutil.copytree(src, dst)
      except OSError as exc: # python >2.5
          if exc.errno == errno.ENOTDIR:
              shutil.copy(src, dst)
          else: raise
  ```




#### 移动和删除

`shutil.rmtree() ` 会移除该文件夹所有内容，不管其中文件是否被占用。

`shutil.move('原文件夹/原文件名','目标文件夹/目标文件名')  `   把一个文件从一个文件夹移动到另一个文件夹，并同时重命名

将一个文件或文件夹从 `src` 移动到 `dst` 如果 `dst` 已存在且为文件夹，则 `src` 将会被移动到 `dst`内。 

如果如 `dst` 存在但不是一个文件夹， 取决于 `os.rename()` 的语义，`dst` 可能会被覆盖。 

如果 `dst` 与 `src` 在相同的文件系统下， 则使用 `os.rename()` 。 

否认则，将使用 `shutil.copy2()` 复制 `src`到 `dst` 并删除。



#### 打包

`shutil.make_archive(base_name, format,...)`

创建压缩包并返回文件路径，例如：zip、tar

- - base_name： 压缩包的文件名，也可以是压缩包的路径。只是文件名时，则保存至当前目录，否则保存至指定路径，
    如 data_bak                       =>保存至当前路径
    如：/tmp/data_bak =>保存至/tmp/

  - format：	压缩包种类，“zip”, “tar”, “bztar”，“gztar”

  - root_dir：	要压缩的文件夹路径（默认当前目录）

  - owner：	用户，默认当前用户

  - group：	组，默认当前组

  - logger：	用于记录日志，通常是logging.Logger对象

  - eg:

    ```python
    #将 /data 下的文件打包放置当前程序目录
    import shutil
    ret = shutil.make_archive("data_bak", 'gztar', root_dir='/data')
      
      
    #将 /data下的文件打包放置 /tmp/目录
    import shutil
    ret = shutil.make_archive("/tmp/data_bak", 'gztar', root_dir='/data')
    ```



shutil 对压缩包的处理是调用 ZipFile 和 TarFile 两个模块来进行的，详细：



### zipfile

```python
import zipfile

# 压缩
z = zipfile.ZipFile('laxi.zip', 'w')
z.write('a.log')
z.write('data.data')
z.close()

# 解压
z = zipfile.ZipFile('laxi.zip', 'r')
z.extractall(path='.')
z.close()
```



### tar file

```python
import tarfile

# 压缩
t=tarfile.open('/tmp/egon.tar','w')
t.add('/test1/a.py',arcname='a.bak')
t.add('/test1/b.py',arcname='b.bak')
t.close()


# 解压
t=tarfile.open('/tmp/egon.tar','r')
t.extractall('/egon')
t.close()
```








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