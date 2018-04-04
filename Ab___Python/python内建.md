### 内建模块

​    在Python中，有一个内建模块，该模块中有一些常用函数;而该模块在Python启动后、且没有执行程序员所写的任何代码前，Python会首先加载 该内建函数到内存。

另外，该内建模块中的功能可以直接使用，不用在其前添加内建模块前缀，其原因是对函数、变量、类等标识符的查找是按LE(N)GB法 则，其中B即代表内建模块。比如：内建模块中有一个abs()函数，其功能是计算一个数的绝对值，如abs(-20)将返回20。

#### `__builtin__`

`__builtin__`、`__builtins__`和builtins之间的关系。

在Python2.X版本中，内建模块被命名为`__builtin__`，而到了Python3.X版本中，却更名为builtins。

##### 向内建函数中添加函数

想要向内建模块中添加一些功能，以便在任何函数中都能直接使用而不 用再进行import，这时，就要导入内建模块(注意： 用内建模块中的功能时不需要导入，但是要为内建模块添加内容时就得导入)，在内建模块的命名空间(即`__dict__`字典属性)中添加该功能。在导入时，如果是Python2.X 版本，就要导入`__builtin__`模块;如果是Python3.X版本，就要导入builtins模块。如我们要写一个能打印hello的函数：

```python
import __builtin__

def print_hello():
	print "hello, world"

__builtin__.__dict__['hello'] = print_hello

print_hello() # 将打印"hello, world"
hello() # 将打印"hello, world"
```

这时，整个程序中都可以使用print_hello()和hello()了



#### `__builtins__`

`__builtins__`，它却同时存在于Python2.X和Python3.X中, 简单的说它时对 **内建模块的引用**，是为了统一python2和python3中的内建模块。

区别： 

* 没有导入就可以引用： `__builtins__`  而 内建模块需要 引入
* 在主模块`__main__`中是和内建模块相等。
* 在非`__main__`模块中是`__builtin__.__dict__`



### 内置字段

#### ` __doc__`

提供py文件，模块，类，函数，的说明。

eg:  doc_test.py:

```python
"""Module docstring."""

class A():
  """Class docstring"""
  pass

def f(x):
    """Function docstring."""
    return 2 * x

if __name__ == '__main__':
   print __doc__
```

输出： 

```
文件本身
"""Module docstring."""

模块
import doc_test
print doc_test.__doc__
"""Module docstring."""

类
print A.__doc__
  """Class docstring"""

函数
print f.__doc__
 """Function docstring."""
```

细节：

* 三引号和单引号都会输出


* 只会输出相关内容的第一行，比如在文件中部的注释都不会输出。




#### `__file__`



#### `__dict__`






#### `__future__`



#### `__all__`

一、

 在模块(*.py)中使用意为导出__all__列表里的类、函数、变量等成员，
 否则将导出modualA中所有不以下划线开头（私有）的成员，
在模块中使用__all__属性可避免在相互引用时的命名冲突 
modualA.py

 ```
 all=["fun1","class1"]
 ```
 使用：
 `from modualA import *`
 导入模块modualA里的所有成员（如果定义了__all__那么就导出列表中的所有，否则默认导出不以下划线开头
 的所有成员）

二、

 在包(假设pkgA，pkgA是一个文件夹)的`__init__.py`中意为导出包里的模块
 例：pkgA/__init__.py

 ```
 all=["modualA","modualB"]
 from modualA import class1,class2
 from modualB import fun1,class3
 ....
 ```

 使用：
 `from pkgA import *`
以上语句即执行了pkgA下的__init__.py，导入两个模块，和这两模块下的函数和类



### 内置函数

#### vars

  vars()函数以字典形式返回每个成员的当前值,如果vars函数没有带参数,那么它会返回包含当前局部命名空间中所有成员的当前值的一个字典.

```
>>> a = 'hhh'
>>> def f():
...  print 'sss'
... 
>>> pprint.pprint(vars())
{'__builtins__': <module '__builtin__' (built-in)>,
 '__doc__': None,
 '__name__': '__main__',
 '__package__': None,
 'a': 'hhh',
 'f': <function f at 0x7f1b1de54410>,
 'pprint': <module 'pprint' from '/usr/lib64/python2.6/pprint.pyc'>}
```





#### locals() 获得函数参数k-v

```
>>> def func(a,b,c):
...  print locals().items()
... 
>>> func(1,2,3)
[('a', 1), ('c', 3), ('b', 2)]
```



#### globals()

python的全局名字空间存储在一个叫globals()的dict对象中



#### eval()





#### getattr()



#### dir()

dir()函数以列表形式返回一个特定的模块,类,对象或它类型的所有成员(以及继承成员)

```python
>>> class A:
...  def a(self):
...   pass
...  def b(self):
...   pass
... 
>>> dir(A)
['__doc__', '__module__', 'a', 'b']
>>> class B(A):
...  def c(self):
...   pass
...  def d(self):
...   pass
... 
>>> dir(B)
['__doc__', '__module__', 'a', 'b', 'c', 'd']
```





#### help()

查看模块具体用法：eg :

`help(shutil)` 

`help(shutil.copy)`





### python 自带命令解析

#### -c

```
def hello():
    return 'Hi :)'
```

命令行输出：`python -c 'import foo; print foo.hello()'`

类似于:

`echo print\(\"hi:\)\"\) | python`

`echo 'print("hi:)")' | python`

`python < test.py` 或 `python > test.py`

#### -m



### 路径问题

python 获取变量路径问题



### 其他

#### 获取某函数的print到变量

```python
from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
```

Usage:

```
with Capturing() as output:
    do_something(my_object)
```



这时do_something函数中的print不会真正的输出，它的输出都会存放在output中，

获得输出我们只需要其output变量就好。