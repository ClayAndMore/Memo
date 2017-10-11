`__future__`



`__all__`

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