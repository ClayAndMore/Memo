---
title: python基础整理
date: 2017-01-30 08:08:55
categories: python
header-img:
tags:  python
---

python的哲学：

`用一种方法，最好是只有一种方法来做一件事。`

linux 命令行将以\$开始，比如\$ls,$python
python命令行将以>>>开始 如：>>>print 'Hello World!'
注释会以#开始
文件后缀.py
一行写不下可以用\连接,或者用括号：

```python
a= 'sdfaf' \
     'test'
if （xxxx is None and
 xxx is None and
 XXX)
```

一行太短用分号断开写多条语句。



头部 `#!/usr/bin/python`或者`#!/usr/bin/env python`

用 `python xxoo.py` 来运行，那么写不写都没关系，如果要用 `./xxoo.py` 那么就必须加这行，这行被称为 shebang, 用来为脚本语言指定解释器.



### 解释器

当我们编写Python代码时，我们得到的是一个包含Python代码的以.py为扩展名的文本文件。要运行代码，就需要Python解释器去执行.py文件。

由于整个Python语言从规范到解释器都是开源的，所以理论上，只要水平够高，任何人都可以编写Python解释器来执行Python代码（当然难度很大）。事实上，确实存在多种Python解释器。

* CPython

当我们从Python官方网站下载并安装好Python 3.5后，我们就直接获得了一个官方版本的解释器：CPython。这个解释器是用C语言开发的，所以叫CPython。在命令行下运行python就是启动CPython解释器。

CPython是使用最广的Python解释器。教程的所有代码也都在CPython下执行。

* IPython

IPython是基于CPython之上的一个交互式解释器，也就是说，IPython只是在交互方式上有所增强，但是执行Python代码的功能和CPython是完全一样的。好比很多国产浏览器虽然外观不同，但内核其实都是调用了IE。

CPython用>>>作为提示符，而IPython用In [序号]:作为提示符。

* PyPy

PyPy是另一个Python解释器，它的目标是执行速度。PyPy采用JIT技术，对Python代码进行动态编译（注意不是解释），所以可以显著提高Python代码的执行速度。

绝大部分Python代码都可以在PyPy下运行，但是PyPy和CPython有一些是不同的，这就导致相同的Python代码在两种解释器下执行可能会有不同的结果。如果你的代码要放到PyPy下执行，就需要了解PyPy和CPython的不同点。

* Jython

Jython是运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行。

* IronPython

IronPython和Jython类似，只不过IronPython是运行在微软.Net平台上的Python解释器，可以直接把Python代码编译成.Net的字节码。



### 输出和输入

输出`print()`

输入`input('请输入您要输入的内容')`

一个有问题的条件判断。很多同学会用`input()`读取用户的输入，这样可以自己输入，程序运行得更有意思：

```
birth = input('birth: ')
if birth < 2000:
    print('00前')
else:
    print('00后')

```

输入`1982`，结果报错：

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unorderable types: str() > int()

```

这是因为`input()`返回的数据类型是`str`，`str`不能直接和整数比较，必须先把`str`转换成整数。Python提供了`int()`函数来完成这件事情：

```
s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')
```



### 格式化

最后一个常见的问题是如何输出格式化的字符串。我们经常会输出类似`'亲爱的xxx你好！你xx月的话费是xx，余额是xx'`之类的字符串，而xxx的内容都是根据变量变化的，所以，需要一种简便的格式化字符串的方式。

在Python中，采用的格式化方式和C语言是一致的，用`%`实现，举例如下：

```
>>> 'Hello, %s' % 'world'
'Hello, world'
>>> 'Hi, %s, you have $%d.' % ('Michael', 1000000)
'Hi, Michael, you have $1000000.'

```

你可能猜到了，`%`运算符就是用来格式化字符串的。在字符串内部，`%s`表示用字符串替换，`%d`表示用整数替换，有几个`%?`占位符，后面就跟几个变量或者值，顺序要对应好。如果只有一个`%?`，括号可以省略。

常见的占位符有：

| %d   | 整数     |
| ---- | ------ |
| %f   | 浮点数    |
| %s   | 字符串    |
| %x   | 十六进制整数 |

其中，格式化整数和浮点数还可以指定是否补0和整数与小数的位数：

```
>>> '%2d-%02d' % (3, 1)
' 3-01'
>>> '%.2f' % 3.1415926  #会四舍五入
'3.14'
```

如果你不太确定应该用什么，`%s`永远起作用，它会把任何数据类型转换为字符串：

```
>>> 'Age: %s. Gender: %s' % (25, True)
'Age: 25. Gender: True'

```

有些时候，字符串里面的`%`是一个普通字符怎么办？这个时候就需要转义，用`%%`来表示一个`%`：

```
>>> 'growth rate: %d %%' % 7
'growth rate: 7 %'

```

输出时注意前面不要有逗号：

```python
a='abc'
print('hello,%s!'%a) #%a前不要有逗号
```

#### format

```python
    def __repr__(self):
        return "<用户名 '{}'，邮箱 '{}'".format(self.username,self.email)
```





### 条件判断

```
//一般写法
。if(i>0){
    x=1;
    y=1;
}
# python 写法
if i>0
    x=1;
    y=1;
```
通过缩来实现不同层次
一个if结构：
```
if i>0
    i=1
elif i<0 # 可以写多个elif
    i=2
els:
    i=0
```
elif可理解为else if。

`if`语句执行有个特点，它是从上往下判断，如果在某个判断上是`True`，把该判断对应的语句执行后，就忽略掉剩下的`elif`和`else`，所以下面程序输出20:

```python
age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')
```

#### 真值判断

if 后判断真值，

| 类型   | False          | True                      |
| ---- | -------------- | ------------------------- |
| 布尔   | Flase(与0等价)    | True(与1等价)                |
| 字符串  | “” （空字符串）      | 非空字符串” “(空格)，”a"          |
| 数值   | 0，0.0          | 1，0.1 ，-2等                |
| 容器   | [],(),{},set() | 至少有一个容器对象，[0],(None),[""] |
| None | None           | 非None对象                   |



#### 相等比较
== 和 is的差别，==比较的是内容，is比较的是引用。

注意None时尽量用is None, 而不是==， 首先速度is会快50%，

然后有个demo:

```python
class Foo:
    def __eq__(self,other):
        return True
foo=Foo()

print(foo==None)
# True

print(foo is None)
# False
```



#### 三目运算符

```python
if gender=='male':
	text='男'
else:
	text='女'
```

pythonic:

```python
text='男' if gender=='male' else '女'
```





### 运算符是特殊方法
使用dir(list)的时候，能看到一个属性，是add()。从形式上看是特殊方法（下划线，下划线）。它特殊在哪呢？
这个方法定义了"+"运算符对于list对象的意义，两个list的对象相加时，会进行的操作。
`>>>print [1,2,3] + [5,6,9]`
运算符，比如+, -, >, <, 以及下标引用[start:end]等等，从根本上都是定义在类内部的方法。
尝试一下：
`>>>print [1,2,3] - [3,4]`
会有错误信息，说明该运算符“-”没有定义。现在我们继承list类，添加对"-"的定义：
```
class superList(list):
    def __sub__(self, b):
        a = self[:]     # 这里，self是supeList的对象。由于superList继承于list，它可以利用和list[:]相同的引用方法来表示整个对象。
        b = b[:]        
        while len(b) > 0:
            element_b = b.pop()
            if element_b in a:
                a.remove(element_b)
        return a

print superList([1,2,3]) - superList([3,4])
```
内置函数len()用来返回list所包含的元素的总数。内置函数__sub__() 定义了“-”的操作：从第一个表中去掉第二个表中出现的元素。如果__sub__() 已经在父类中定义，你又在子类中定义了，那么子类的对象会参考子类的定义，而不会载入父类的定义。任何其他的属性也是这样。





### 文件操作

*   创建文件
        `对象名 = open(文件名，模式)`
        常用的模式：
  * r 打开只读文件，该文件必须存在。
    * r+ 打开可读写的文件，该文件必须存在。
    * w 打开只写文件，若文件存在则文件长度清为0，即该文件内容会消失。若文件不存在则 建立该文件。
    * w+ 打开可读写文件，若文件存在则文件长度清为零，即该文件内容会消失。若文件不存在则建立该文件。
    * a 以附加**写**的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。
    * a+ 以附加**读写**方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。

      上述的形态字符串都可以再加一个b字符，如rb、w+b或ab＋等组合，加入b 字符用来告诉函数库打开的文件为二进制文件，而非纯文字文件。windows下文件是二进制，而linux不需要区分二进制和文件。
* 读取 
```
content = f.read(N)          # 读取N bytes的数据
content = f.readline()       # 读取一行
content = f.readlines()      # 读取所有行，储存在列表中，每个元素是一行。
```
* 写入
  `f.write('I like apple!\n')      # 将'I like apple'写入文件并换行`

  `f.writeline(['a\n', 'b\n', 'c\n'])`   注意一定要加换行，不然只写了一行  

* 关闭文件
  `f.close()`

* 输出重定向

  ```python
  import os
  import sys
  
  temp=sys.stdout # 记录当前输出指向，默认是consle
  
  with open("outputlog.txt","a+") as f:
      sys.stdout=f   # 输出指向txt文件
      print("filepath:",__file__,
      "\nfilename:",os.path.basename(__file__))
      print("some other information")
      print("some other")
      print("information")
      sys.stdout=temp # 输出重定向回consle
      print(f.readlines()) # 将记录在文件中的结果输出到屏幕
  ```

  ​

### 作用域

在一个模块中，我们可能会定义很多函数和变量，但有的函数和变量我们希望给别人使用，有的函数和变量我们希望仅仅在模块内部使用。在Python中，是通过`_`前缀来实现的。

正常的函数和变量名是公开的（public），可以被直接引用，比如：`abc`，`x123`，`PI`等；

类似`__xxx__`这样的变量是特殊变量，可以被直接引用，但是有特殊用途，比如上面的`__author__`，`__name__`就是特殊变量，`hello`模块定义的文档注释也可以用特殊变量`__doc__`访问，我们自己的变量一般不要用这种变量名；

类似`_xxx`和`__xxx`这样的函数或变量就是非公开的（private），不应该被直接引用，比如`_abc`，`__abc`等；

之所以我们说，private函数和变量“不应该”被直接引用，而不是“不能”被直接引用，是因为Python并没有一种方法可以完全限制访问private函数或变量，但是，从编程习惯上不应该引用private函数或变量。

private函数或变量不应该被别人引用，那它们有什么用呢？请看例子：

```python
def _private_1(name):
    return 'Hello, %s' % name

def _private_2(name):
    return 'Hi, %s' % name

def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)
```

我们在模块里公开`greeting()`函数，而把内部逻辑用private函数隐藏起来了，这样，调用`greeting()`函数不用关心内部的private函数细节，这也是一种非常有用的代码封装和抽象的方法，即：

外部不需要引用的函数全部定义成private，只有外部需要引用的函数才定义为public。



### 模块和模块包

#### 模块

相当与引用其他.py文件，类似于java中的引入包。
`import 文件名`
使用其他文件中的对象：`文件名(模块).对象`
其他引入方式：

```
import a as b             # 引入模块a，并将模块a重命名为b
from a import function1   # 从模块a中引入function1对象。调用a中对象时，我们不用再说明模块，即直接使用function1，而不是a.function1。
from a import *           # 从模块a中引入所有对象。调用a中对象时，我们不用再说明模块，即直接使用对象，而不是a.对象。

```

#### 模块包

可以将功能相似的模块放在同一个文件夹（比如说this_dir）中，构成一个模块包。通过

`import this_dir.module`
引入this_dir文件夹中的module模块。

该文件夹中必须包含一个 `__init__.py` 的文件，提醒Python，该文件夹为一个模块包。__init__.py 可以是一个空文件。

#### 导入上级模块

```python
import sys
sys.path.append("..")
# 现在直接可以导入上级的包了
```

#### 查看导入包的路径

eg： 查看pymongo包的路径

```python
>>>import pymongo
>>>pymongo.__file__
```

#### 导入其他目录的包

```python
import sys
sys.path.insert(0, '/path/to/application/app/folder')

import file
```



### 错误和异常

```
try:
    ...
except exception1:
    ...
except exception2 as e:
    ...
except:
    ...
else:
    如果没有异常则执行
finally:
    ...
```
* try - 有异常 - except 1 或者 2，都没有，到except - finally

* try - 无异常 - else - finally

* 打印异常 print(exception1),print(e)

* 看异常的类型：

  ```
  import sys
  try:
      raise
  except:
      t,v,tb = sys.exc_info()
      print(t,v)
  ```

  ​

#### 抛异常
`raise StopIteration`
StopIteration是一个类。抛出异常时，会自动有一个中间环节，就是生成StopIteration的一个对象。Python实际上抛出的，是这个对象。当然，也可以自行生成对象:
`raise StopIteration()`

自定义异常



### 注意

* 不要用windows自带的笔记本写py,它会自动加utf-8 bom。导致莫名的错误。
* `not`运算是非运算，它是一个单目运算符，把`True`变成`False`，`False`变成`True`：

```
>>> not True
False
>>> not False
True
>>> not 1 > 2
True
```

* 空值是Python里一个特殊的值，用`None`表示。`None`不能理解为`0`，因为`0`是有意义的，而`None`是一个特殊的空值。

* 在Python中，等号`=`是赋值语句，可以把任意数据类型赋值给变量，同一个变量可以反复赋值，而且可以是不同类型的变量，例如：

  ```
  a = 123 # a是整数
  print(a)
  a = 'ABC' # a变为字符串
  print(a)

  ```

  这种变量本身类型不固定的语言称之为动态语言，与之对应的是静态语言。静态语言在定义变量时必须指定变量类型，

* 解释一下整数的除法为什么也是精确的。在Python中，有两种除法，一种除法是`/`：

  ```
  >>> 10 / 3
  3.3333333333333335
  ```

  `/`除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数：

  ```
  >>> 9 / 3
  3.0
  ```

  还有一种除法是`//`，称为地板除，两个整数的除法仍然是整数：

  ```
  >>> 10 // 3
  3

  ```

  你没有看错，整数的地板除`//`永远是整数，即使除不尽。要做精确的除法，使用`/`就可以。

  因为`//`除法只取结果的整数部分，所以Python还提供一个余数运算，可以得到两个整数相除的余数：

  ```
  >>> 10 % 3
  1

  ```

  无论整数做`//`除法还是取余数，结果永远是整数，所以，整数运算结果永远是精确的。

  ```python
  print('3 / 2 =', 3 / 2)       #1.5
  print('3 // 2 =', 3 // 2) 	  #1
  print('3 / 2.0 =', 3 / 2.0)   #1.5
  print('3 // 2.0 =', 3 // 2.0) # 1.0
  ```

  ​

* 错误：`IndentationError: expected an indented block`

   没有缩进块，或者缩进错误。

* `pass`还可以用在其他语句里，比如：

  ```
  if age >= 18:
      pass

  ```

  缺少了`pass`，代码运行就会有语法错误。
