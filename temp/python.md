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



#### help()

查看模块具体用法：eg :

`help(shutil)` 

`help(shutil.copy)`





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