Tags:[python]

### 函数

```python
def square_sum(a,b):
    c=a+b
    return c
```

def 关键字通知python我们在定义一个函数，没有return时返回none.
参数传递，可以sum(1,2),或者sum(a=1,b=1).



值转递和引用传递，

**参数是可变类型时为引用传递，不可变类型时为参数传递**



### 函数参数

用*收集位置参数，以元祖的形式返回，如果有使用的位置参数，*会收集剩下的

```python
def print_args(a,b,*args)
    print("have a",a)
    print("have b",b)
    print("the rest:",args)
```

用**可以将参数收集到一个字典中，参数的名字是字典的键，对应参数的值是字典的值。

**在python总圆括号意味着调用函数，在没有圆括号的情况下，会把函数当成普通对象**

`*args`是可变参数，args接收的是一个tuple；

`**kw`是关键字参数，kw接收的是一个dict。

以及调用函数时如何传入可变参数和关键字参数的语法：

可变参数既可以直接传入：`func(1, 2, 3)`，又可以先组装list或tuple，再通过`*args`传入：`func(*(1, 2, 3))`；

关键字参数既可以直接传入：`func(a=1, b=2)`，又可以先组装dict，再通过`**kw`传入：`func(**{'a': 1, 'b': 2})`。



#### 函数的参数为引用时

Python 唯一支持的参数传递模式是共享传参，指函数等各个形参获得实参引用的副本，函数内部的形参是实参的别名。

这样的害处是可能会修改作为参数**传入的可变对象**

```python
def f(a, b):
    a+=b
    return a
x = 1
y = 2
f(x, y)
3
a=[1,2]
b=[3,4]
f(a, b)
[1,2,3,4]
a, b
([1,2,3,4], [3,4]) #注意这里
t = (10, 20)
u = (30, 40)
f(t, u)
(10,20,30,40)
t, u
((10,20), (30, 40))
```

结论，可变对象会被修改



#### 可变类型作为参数默认值

```python
>>> def func(numbers=[], num=1):
...     numbers.append(num)
...     return numbers

>>> func()
[1]
>>> func()
[1, 1]
>>> func()
[1, 1, 1]
```

numbers 第一次生成时在内存中地址不变，后期调用实际在改变的是地址的值。

**在使用默认参数为可变类型时一定要注意。**

这样也可以用做缓存：

```python
def factorial(num, cache={}):
    if num == 0:
        return 1
    if num not in cache:
        print('xxx')
        cache[num] = factorial(num - 1) * num
    return cache[num]


print(factorial(4))
print("-------")
print(factorial(4))

---第一次调用---
xxx
xxx
xxx
xxx
24
---第二次调用---
24
```





### 包裹传递

- 在传递函数的参数时，我们不知道有多少个参数，这时可以传递包裹

```python
def func(*name):
    print type(name)
    print name

func(1,4,6)  # <type 'tuple'> (1, 4, 6)
func(5,6,7,1,2,3)
#<type 'tuple'>
#(5, 6, 7, 1, 2, 3)
```

所有的参数被name收集，根据位置合并成一个元组(tuple)，这就是包裹位置传递。

- 包裹关键字传递：

```python
def func(**dict):
    print type(dict)
    print dict

func(a=1,b=9) # <type 'dict'> {'a': 1, 'b': 9}
func(m=2,n=1,c=11) 
# <type 'dict'>
# {'c': 11, 'm': 2, 'n': 1}
```

与上面一个例子类似，dict是一个字典，收集所有的关键字，传递给函数func。为了提醒Python，参数dict是包裹关键字传递所用的字典，在dict前加 * *

- 定义的时候没有定义包裹也可以在传递的时候用：

```python
def func(a,b,c):
    print a,b,c

args = (1,3,4)
func(*args)
# 相应的：
dict = {'a':1,'b':2,'c':3}
func(**dict)
```




### lambda表达

```python
def func(x,y):
    return x+y
----------------
func = lambda x,y:x+y
```

关键字`lambda`表示匿名函数，冒号前面的`x`表示函数参数。

匿名函数，就是只能有一个表达式，不用写`return`，返回值就是该表达式的结果。

不能使用while和try等语句。



### 内置函数

#### join()

```python
>>> tup = ('a', 'b', 'c', 'd', 'g', 'x', 'r', 'e')
>>> ''.join(tup)
'abcdgxre'
>>> myTuple = ['h','e','l','l','o']
>>> ''.join(myTuple)
'hello'
>>> str='-'
>>> seq=("a", "b", "c")
>>> print str.join(seq)
a-b-c
```



#### map()

它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回。

```python
def f(x):
    return x*x
print map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
输出结果：

[1, 4, 9, 10, 25, 36, 49, 64, 81]
```

仍然可以接受两个list:

```
re = map((lambda x,y: x+y),[1,2,3],[6,7,9])
```

map()将每次从两个表中分别取出一个元素，带入lambda所定义的函数。结果返回到表re中。
map函数第一个参数是一个函数对象。

#### filter()(根据条件判断)

filter函数的第一个参数也是一个函数对象。它也是将作为参数的函数对象作用于多个元素。如果函数对象返回的是True，则该次的元素被储存于返回的表中。 filter通过读入的函数来筛选数据。同样，在Python 3.X中，filter返回的不是表，而是循环对象。

```python
def func(a):
    if a > 100:
        return True
    else:
        return False

print filter(func,[10,56,101,500])
```

#### reduce()(累积传参）

`print reduce((lambda x,y: x+y),[1,2,5,7,9])`
相当于((1+2)+5)+7)+9
reduce()函数在3.0里面不能直接用的，它被定义在了functools包里面，需要引入包。

比方说对一个序列求和，就可以用`reduce`实现：

```python
>>> from functools import reduce
>>> def add(x, y):
...     return x + y
...
>>> reduce(add, [1, 3, 5, 7, 9])
25
```

当然求和运算可以直接用Python内建函数`sum()`，没必要动用`reduce`。

但是如果要把序列`[1, 3, 5, 7, 9]`变换成整数`13579`，`reduce`就可以派上用场：

```python
>>> from functools import reduce
>>> def fn(x, y):
...     return x * 10 + y
...
>>> reduce(fn, [1, 3, 5, 7, 9])
13579
```

这个例子本身没多大用处，但是，如果考虑到字符串`str`也是一个序列，对上面的例子稍加改动，配合`map()`，我们就可以写出把`str`转换为`int`的函数：

```python
>>> from functools import reduce
>>> def fn(x, y):
...     return x * 10 + y
...
>>> def char2num(s):
...     return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
...
>>> reduce(fn, map(char2num, '13579'))
13579
```



#### zip()

zip()函数的功能，就是从多个列表中，依次各取出一个元素。每次取出的(来自不同列表的)元素合成一个元组，合并成的元组放入zip()返回的列表中。zip()函数起到了聚合列表的功能。
分解聚合后的列表：

```python
ta = [1,2,3]
tb = [9,8,7]

# cluster
zipped = zip(ta,tb)
print(zipped) # [(1, 9), (2, 8), (3, 7)]

# decompose
na, nb = zip(*zipped)
print(na, nb) # ((1, 2, 3), (9, 8, 7))
```



#### dir() 

dir()可以用来查询一个类或者对象的所有属性 dir(list)

打印一个对象的所有属性和值：

```python
def prn_obj(obj): 
  print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()]) 
```



#### help()

help() 来查询相应文档  help（list)



#### 运算和逻辑

##### 计算

max, min, 

all, any, 



##### sorted *

`sorted()`函数就可以对list进行排序, **注意原变量不会被改变**

```
>>> sorted([36, 5, -12, 9, -21])
[-21, -12, 5, 9, 36]
```

此外，`sorted()`函数也是一个高阶函数，它还可以接收一个`key`函数来实现自定义的排序，例如按绝对值大小排序：

```
>>> sorted([36, 5, -12, 9, -21], key=abs)
[5, 9, -12, -21, 36]
```

key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序。对比原始的list和经过`key=abs`处理过的list：

```
list = [36, 5, -12, 9, -21]

keys = [36, 5,  12, 9,  21]
```

然后`sorted()`函数按照keys进行排序，并按照对应关系返回list相应的元素：

```
keys排序结果 => [5, 9,  12,  21, 36]
                |  |    |    |   |
最终结果     => [5, 9, -12, -21, 36]
```

我们再看一个字符串排序的例子：

```
>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
['Credit', 'Zoo', 'about', 'bob']
```

默认情况下，对字符串排序，是按照ASCII的大小比较的，由于`'Z' < 'a'`，结果，大写字母`Z`会排在小写字母`a`的前面。

现在，我们提出排序应该忽略大小写，按照字母序排序。要实现这个算法，不必对现有代码大加改动，只要我们能用一个key函数把字符串映射为忽略大小写排序即可。忽略大小写来比较两个字符串，实际上就是先把字符串都变成大写（或者都变成小写），再比较。

这样，我们给`sorted`传入key函数，即可实现忽略大小写的排序：

```
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
['about', 'bob', 'Credit', 'Zoo']
```

**重点**来了：，key可以结合lambda表达式， 根据末尾数字排序：

```python
>>> s=['No.5', 'No.2', 'No.4', 'No.3', 'No.1']
>>> sorted(s, key=lambda x: x[::-1])
['No.1', 'No.2', 'No.3', 'No.4', 'No.5']
```

lambda的返回值即使对其排序的逻辑。



要进行反向排序，不必改动key函数，可以传入第三个参数`reverse=True`：

```
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']
```

从上述例子可以看出，高阶函数的抽象能力是非常强大的，而且，核心代码可以保持得非常简洁。key是一个函数，自己也可以按功能定义。



#### isinstance()

使用内建的`isinstance`函数可以判断一个变量是不是字符串：

```
>>> x = 'abc'
>>> y = 123
>>> isinstance(x, str)
True
>>> isinstance(y, str)
False
```

使用`isinstance()`判断一个对象是否是`Iterable`对象：

```
>>> from collections import Iterable
>>> isinstance([], Iterable)
True
>>> isinstance({}, Iterable)
True
>>> isinstance('abc', Iterable)
True
>>> isinstance((x for x in range(10)), Iterable)
True
>>> isinstance(100, Iterable)
False
# 确认是声明的类
>>> type(type)
<type 'type'>
>>> class A:
...  pass
>>> isinstance(A, type)
True
>>> type(A)
<type 'type'>

# 多选
>>> a='yyy'
>>> isinstance(a,(bytes,unicode))
True
满足其中一个就可。

```

#### type()

一般使用type()函数来看数据的类型：

```python
a=(1,2,3)
b=(x for x in range(3))
print(type(a)) #<class 'tuple'>
print(type(b)) #<class 'generator'>
```



### 函数式编程

函数式编程就是一种抽象程度很高的编程范式，纯粹的函数式编程语言编写的函数没有变量，因此，任意一个函数，只要输入是确定的，输出就是确定的，这种纯函数我们称之为没有副作用。而允许使用变量的程序设计语言，由于函数内部的变量状态不确定，同样的输入，可能得到不同的输出，因此，这种函数是有副作用的。

函数式编程的一个特点就是，允许把函数本身作为参数传入另一个函数，还允许返回一个函数！

Python对函数式编程提供部分支持。由于Python允许使用变量，因此，Python不是纯函数式编程语言。

- 高阶函数

  函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数。

  一个最简单的高阶函数：

  ```
  def add(x, y, f):
      return f(x) + f(y)
  
  
  ```

  当我们调用`add(-5, 6, abs)`时，参数`x`，`y`和`f`分别接收`-5`，`6`和`abs`，根据函数定义，我们可以推导计算过程为：

  ```
  x = -5
  y = 6
  f = abs
  f(x) + f(y) ==> abs(-5) + abs(6) ==> 11
  return 11
  
  ```

编写高阶函数，就是让函数的参数能够接收别的函数