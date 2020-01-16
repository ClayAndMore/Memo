Tags: [python, pip] date: 2017-03-18




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


### python2 和 py3 的兼容

#### 判别语句

可以通过`sys.version_info`来判别：

```python
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

# 或改成：
import sys
py_version = sys.version_info # #sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)
if py_version > (3.0) :
    import pathlib
else:
    import pahtlib2
```



eg, 看下bottle里面的判别：

```python
py   = sys.version_info 
py3k = py >= (3, 0, 0)
py25 = py <  (2, 6, 0)
py31 = (3, 1, 0) <= py < (3, 2, 0)
```





#### `__future__` 类的使用

整除问题：python 2中的除法是默认取整的，比如2/3=0。而Python 3中就会得到0.666667。这种情况下，可以使用内置的`__future__`来解决问题，这下即使在Python 2下也可以默认得到浮点结果了。

```python
from __future__ import division
```

输出、打印问题。print函数在Python 2和3下也有所不同，比如括号的问题。这个也可以用内置的`__future__`来解决问题，这样在python 2下运行print( )也不会多出额外的一对括号了。

```python
from __future__ import print_function
```

文件读取中也有一些麻烦，比如Python 3中的打开文件时可以指定文件编码:
```python
with open('unicode.txt', encoding='utf-8') as f:
    for line in f:
        print(repr(line))
```


如果在Python 2下运行这个代码，就会报错提示没有“encoding”这个参数，因为Python 2内置的open（）所使用的参数和Python 3不同。这种情况下可以使用io中的open函数，这样就同时兼容2和3了

```python
from io import open
with open('unicode.txt', encoding:'utf-8') as f:
    for line in f:
        print(repr(line))
```

>>>>>>> 562b086e39c3b03b8a434f52206323b8769c921d
