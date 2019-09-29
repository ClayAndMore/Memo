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





这两天申请了一个云服务器，用的centOS,自带python2.7.5没有pip,

为了做东西，更新了2.7到最新版本。装了python3.5,以及两个版本的pip,很繁琐，下面总结下：

