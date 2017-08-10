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
一行写不下可以用+\连接

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




### 变量
变量不需要声明，直接 a=10,
type(a)，可以看变量的类型
收回变量直接赋新值就好
在python3中，一个int类型可以存任意大小的整数，甚至超过了64位，但是超出一定范围就直接表示为`inf`（无限大）。
None和False不一样。

### 序列
* tuple，定值表 ，也成为元组，s1=(1,2,true)  其中的值不可变更

  如果要定义一个空的tuple，可以写成`()`：

  ```
  >>> t = ()
  >>> t
  ()

  ```

  但是，要定义一个只有1个元素的tuple，如果你这么定义：

  ```
  >>> t = (1)
  >>> t
  1

  ```

  定义的不是tuple，是`1`这个数！这是因为括号`()`既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义，因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是`1`。

  所以，**只有1个元素的tuple定义时必须加一个逗号`,`，来消除歧义**：

  ```
  >>> t = (1,)
  >>> t
  (1,)

  ```

  Python在显示只有1个元素的tuple时，也会加一个逗号`,`，以免你误解成数学计算意义上的括号。

  最后来看一个“可变的”tuple：

  ```
  >>> t = ('a', 'b', ['A', 'B'])
  >>> t[2][0] = 'X'
  >>> t[2][1] = 'Y'
  >>> t
  ('a', 'b', ['X', 'Y'])

  ```

  这个tuple定义的时候有3个元素，分别是`'a'`，`'b'`和一个list。

  **表面上看，tuple的元素确实变了，但其实变的不是tuple的元素，而是list的元素。tuple一开始指向的list并没有改成别的list，所以，tuple所谓的“不变”是说，tuple的每个元素，指向永远不变。即指向`'a'`，就不能改成指向`'b'`，指向一个list，就不能改成指向其他对象，但指向的这个list本身是可变的！**

#### 切片

* list，表(本质是个类)   s2=[1,2,['g']] ,可变. 函数 **range(n)** ，建立一个从0到n-1的表

* 下表引用 基本样式 下限：上限：步长
  `print s1[0:5:2]` 从下标0到下标4，每隔2取一个元素，输出为0，2，4
  so,上限不包括本身。

* 尾部元素引用 s1[-1] 序列中最后一个元素，s1[-3]序列倒数第三个元素

  切片操作十分有用。我们先创建一个0-99的数列：

  ```
  >>> L = list(range(100))
  >>> L
  [0, 1, 2, 3, ..., 99]

  ```

  可以通过切片轻松取出某一段数列。比如前10个数：

  ```
  >>> L[:10]
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

  ```

  后10个数：

  ```
  >>> L[-10:]
  [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

  ```

  前11-20个数：

  ```
  >>> L[10:20]
  [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

  ```

  前10个数，每两个取一个：

  ```
  >>> L[:10:2]
  [0, 2, 4, 6, 8]

  ```

  所有数，每5个取一个：

  ```
  >>> L[::5]
  [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

  ```

  甚至什么都不写，只写`[:]`就可以原样复制一个list：

  ```
  >>> L[:]
  [0, 1, 2, 3, ..., 99]
  ```

* tuple也是一种list，唯一区别是tuple不可变。因此，**tuple也可以用切片操作**，只是操作的结果仍是tuple

* 字符串`'xxx'`也可以看成是一种list，每个元素就是一个字符。因此，字符串也可以用切片操作，只是操作结果仍是字符串：

  ```
  >>> 'ABCDEFG'[:3]
  'ABC'
  >>> 'ABCDEFG'[::2]
  'ACEG'
  ```

#### 关于序列的内置函数
* 适用于序列：
```
len(s)         返回： 序列中包含元素的个数
min(s)         返回： 序列中最小的元素
max(s)         返回： 序列中最大的元素
all(s)         返回： True, 如果所有元素都为True的话
any(s)         返回： True, 如果任一元素为True的话
```
* 查询功能，适用于表和定值表：
```
sum(s)         返回：序列中所有元素的和
# x为元素值，i为下标(元素在序列中的位置)

s.count(x)     返回： x在s中出现的次数
s.index(x)     返回： x在s中第一次出现的下标
```
* 只适用于表：
```
# l为一个表, l2为另一个表

l.extend(l2)        在表l的末尾添加表l2的所有元素
l.append(x)         在l的末尾附加x元素
l.sort()            对l中的元素排序
l.reverse()         将l中的元素逆序
l.pop()             返回：表l的最后一个元素，并在表l中删除该元素
del l[i]            删除该元素

(以上这些方法都是在原来的表的上进行操作，会对原来的表产生影响，而不是返回一个新表。)
```
* 用于字符串的方法。尽管字符串是定值表的特殊的一种，但字符串(string)类有一些方法是改变字符串的。这些方法的本质不是对原有字符串进行操作，而是删除原有字符串，再建立一个新的字符串，所以并不与定值表的特点相矛盾。
```
#str为一个字符串，sub为str的一个子字符串。s为一个序列，它的元素都是字符串。width为一个整数，用于说明新生成字符串的宽度。

str.count(sub)       返回：sub在str中出现的次数
str.find(sub)        返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1

str.index(sub)       返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误

str.rfind(sub)       返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1

str.rindex(sub)      返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误

str.split(',')		以负号分割字符，返回一个列表，元素为字符串，如果没有整个分割符，那么返回整个字符串的列表。原来字符串不变。	

str.isalnum()        返回：True， 如果所有的字符都是字母或数字
str.isalpha()        返回：True，如果所有的字符都是字母
str.isdigit()        返回：True，如果所有的字符都是数字
str.istitle()        返回：True，如果所有的词的首字母都是大写
str.isspace()        返回：True，如果所有的字符都是空格
str.islower()        返回：True，如果所有的字符都是小写字母
str.isupper()        返回：True，如果所有的字符都是大写字母

str.split([sep, [max]])    返回：从左开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.split(',')的方式使用逗号或者其它分割符。

str.rsplit([sep, [max]])   返回：从右开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.rsplit(',')的方式使用逗号或者其它分割符

str.join(s)                返回：将s中的元素，以str为分割符，合并成为一个字符串。

str.strip([sub])           返回：去掉字符串开头和结尾的空格。也可以提供参数sub，去掉位于字符串开头和结尾的sub  

str.replace(sub, new_sub)  返回：用一个新的字符串new_sub替换str中的sub
str.capitalize()           返回：将str第一个字母大写
str.lower()                返回：将str全部字母改为小写
str.upper()                返回：将str全部字母改为大写
str.swapcase()             返回：将str大写字母改为小写，小写改为大写
str.title()                返回：将str的每个词(以空格分隔)的首字母大写

str.center(width)          返回：长度为width的字符串，将原字符串放入该字符串中心，其它空余位置为空格。

str.ljust(width)           返回：长度为width的字符串，将原字符串左对齐放入该字符串，其它空余位置为空格。

str.rjust(width)           返回：长度为width的字符串，将原字符串右对齐放入该字符串，其它空余位置为空格。
#str为一个字符串，sub为str的一个子字符串。s为一个序列，它的元素都是字符串。width为一个整数，用于说明新生成字符串的宽度。

str.count(sub)       返回：sub在str中出现的次数
str.find(sub)        返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1

str.index(sub)       返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误

str.rfind(sub)       返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1

str.rindex(sub)      返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误


str.isalnum()        返回：True， 如果所有的字符都是字母或数字
str.isalpha()        返回：True，如果所有的字符都是字母
str.isdigit()        返回：True，如果所有的字符都是数字
str.istitle()        返回：True，如果所有的词的首字母都是大写
str.isspace()        返回：True，如果所有的字符都是空格
str.islower()        返回：True，如果所有的字符都是小写字母
str.isupper()        返回：True，如果所有的字符都是大写字母

str.split([sep, [max]])    返回：从左开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.split(',')的方式使用逗号或者其它分割符

str.rsplit([sep, [max]])   返回：从右开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.rsplit(',')的方式使用逗号或者其它分割符

str.join(s)                返回：将s中的元素，以str为分割符，合并成为一个字符串。

str.strip([sub])           返回：去掉字符串开头和结尾的空格。也可以提供参数sub，去掉位于字符串开头和结尾的sub  

str.replace(sub, new_sub)  返回：用一个新的字符串new_sub替换str中的sub
str.capitalize()           返回：将str第一个字母大写
str.lower()                返回：将str全部字母改为小写
str.upper()                返回：将str全部字母改为大写
str.swapcase()             返回：将str大写字母改为小写，小写改为大写
str.title()                返回：将str的每个词(以空格分隔)的首字母大写

str.center(width)          返回：长度为width的字符串，将原字符串放入该字符串中心，其它空余位置为空格。

str.ljust(width)           返回：长度为width的字符串，将原字符串左对齐放入该字符串，其它空余位置为空格。

str.rjust(width)           返回：长度为width的字符串，将原字符串右对齐放入该字符串，其它空余位置为空格。
```



### 不可变对象

str是不变对象，而list是可变对象。

对于可变对象，比如list，对list进行操作，list内部的内容是会变化的，比如：

```
>>> a = ['c', 'b', 'a']
>>> a.sort()
>>> a
['a', 'b', 'c']
```

而对于不可变对象，比如str，对str进行操作呢：

```
>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
```

虽然字符串有个`replace()`方法，也确实变出了`'Abc'`，但变量`a`最后仍是`'abc'`，应该怎么理解呢？

我们先把代码改成下面这样：

```
>>> a = 'abc'
>>> b = a.replace('a', 'A')
>>> b
'Abc'
>>> a
'abc'
```

要始终牢记的是，`a`是变量，而`'abc'`才是字符串对象！有些时候，我们经常说，对象`a`的内容是`'abc'`，但其实是指，`a`本身是一个变量，它指向的对象的内容才是`'abc'`：

![a-to-str](http://www.liaoxuefeng.com/files/attachments/001389580505217f87b492b060b4b0ea60c8e5e70a1b53c000/0)

当我们调用`a.replace('a', 'A')`时，实际上调用方法`replace`是作用在字符串对象`'abc'`上的，而这个方法虽然名字叫`replace`，但却没有改变字符串`'abc'`的内容。相反，`replace`方法创建了一个新字符串`'Abc'`并返回，如果我们用变量`b`指向该新字符串，就容易理解了，变量`a`仍指向原有的字符串`'abc'`，但变量`b`却指向新字符串`'Abc'`了：

![a-b-to-2-strs](http://www.liaoxuefeng.com/files/attachments/001389580620829061e426d429640ddb1d17174a82a7244000/0)

所以，对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。

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



#### for/else 

for else 是 Python 中特有的语法格式，else 中的代码在 for 循环遍历完所有元素之后执行。

```python
flagfound = False
for i in mylist:
    if i == theflag:
        flagfound = True
        break
    process(i)

if not flagfound:
    raise ValueError("List argument missing terminal flag.")
```

pythonic

```python
for i in mylist:
    if i == theflag:
        break
    process(i)
else:
    raise ValueError("List argument missing terminal flag.")
```



### 迭代
`for 元素 in 序列：`
`statement`

Python提供一个`range()`函数，可以生成一个整数序列，再通过`list()`函数可以转换为list。比如`range(5)`生成的序列是从0开始小于5的整数：

```
>>> list(range(5))
[0, 1, 2, 3, 4]
```

#### 迭代list/dict

默认情况下，dict迭代的是key。如果要迭代value，可以用`for value in d.values()`，如果要同时迭代key和value，可以用`for k, v in d.items()`。注意items.

```python
>>> l = {'name': 'aa', 'age': 18,'phone':'1111111111'}
>>> for x,y in l.items():
...  print(x,y)
...
name aa
age 18
phone 1111111111
```



由于字符串也是可迭代对象，因此，也可以作用于`for`循环：

```
>>> for ch in 'ABC':
...     print(ch)
...
A
B
C
```

所以，当我们使用`for`循环时，只要作用于一个可迭代对象，`for`循环就可以正常运行，而我们不太关心该对象究竟是list还是其他数据类型。

如果要对list实现类似Java那样的下标循环怎么办？Python内置的`enumerate`函数可以把一个list变成索引-元素对，这样就可以在`for`循环中同时迭代索引和元素本身：

```python
>>> for i, value in enumerate(['A', 'B', 'C']):
...     print(i, value)
...
0 A
1 B
2 C
```

```python
>>> for i,value in enumerate(a):
...  print(i,value)
...
0 i
1 m
2
3 c
4 o
5 m
6 e
```



上面的`for`循环里，同时引用了两个变量，在Python里是很常见的，比如下面的代码：

```
>>> for x, y in [(1, 1), (2, 4), (3, 9)]:
...     print(x, y)
...
1 1
2 4
3 9
```



### 函数
```
def square_sum(a,b):
    c=a+b
    return c
```
def 关键字通知python我们在定义一个函数，没有return时返回none.
参数传递，可以sum(1,2),或者sum(a=1,b=1).

###函数参数
用*收集位置参数，以元祖的形式返回，如果有使用的位置参数，*会收集剩下的
```
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



### 类
```python
# 定义
class Bird(object):
    have_feather = True
    way_of_reproduction = 'egg'
    # 方法
    def move(self,dx,dy):
    position = [0,0]
    position[0] = position[0]+dx
    position[1] = position[1]+dy
    return position 
    
# 使用
summer = Bird()
print summer.way_of_reproduction

# 继承
class Chicken(Bird);
    way_of_move = 'walk'
```
方法中有个self，方便我们引用自身对象，无论用或不用，第一个参数必须是self.传参可以不传.这个相当与其他语言中的this，代表这个实例，可以在方法中用本类的属性

#### 访问限制

如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线`__`，在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问，所以，我们把Student类改一改：

```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
```

改完后，对于外部代码来说，没什么变动，但是已经无法从外部访问`实例变量.__name`和`实例变量.__score`了，子类也不能访问，只有自己能访问。

`_abc`单下划线是保护变量，子类能访问。外部不能访问。更多看作用域。

#### `__slots__`

只允许对Student实例添加`name`和`age`属性。

为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的`__slots__`变量，来限制该class实例能添加的属性：

```
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

```

然后，我们试试：

```python
>>> s = Student() # 创建新的实例
>>> s.name = 'Michael' # 绑定属性'name'
>>> s.age = 25 # 绑定属性'age'
>>> s.score = 99 # 绑定属性'score'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'score'
```

由于`'score'`没有被放到`__slots__`中，所以不能绑定`score`属性，试图绑定`score`将得到`AttributeError`的错误。

使用`__slots__`要注意，`__slots__`定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：

```
>>> class GraduateStudent(Student):
...     pass
...
>>> g = GraduateStudent()
>>> g.score = 9999

```

除非在子类中也定义`__slots__`，这样，子类实例允许定义的属性就是自身的`__slots__`加上父类的`__slots__`。

#### super()方法

http://python.jobbole.com/87291/



#### `__init__()方法`
python中有一些特殊方法，特殊方法的特点是名字前后有两个下划线
如果在类中定义了init这个方法，python会自动调用这个方法，这个过程也叫初始化

####`__new__()`方法

`__new__` 这个方法负责创建类实例，而 `__init__` 负责初始化类实例 。 `__new__` 函数可以用来自定义对象的创建，它的第一个参数是这个类的引用，然后是一些构造参数；返回值通常是对象实例的引用。

通常用来判断有没有这个类的实例。

#### `__repr__()`方法
这个函数，对应repr(object)这个功能。意思是当需要显示一个对象在屏幕上时，将这个对象的属性或者是方法整理成一个可以打印输出的格式。

这个功能与eval也可以对应。打印出的结果直接放到eval里，通常可以获得原来的对象。
比如：
t1=datetime.datetime.now()
print repr(t1)
结果是
datetime.datetime(2014, 9, 9, 6, 34, 29, 756000)


### dir() 和 help  
dir()可以用来查询一个类或者对象的所有属性 dir(list)

打印一个对象的所有属性和值：

```python
def prn_obj(obj): 
  print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()]) 
```



help() 来查询相应文档  help（list)

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

### 词典（字典dict）
可以理解为一种key-value的list
`dic = {'tom':11,'sam':12,'lily':100}`
与表不同的是，不能通过下下标来引用，要通过键来引用
`print dic['tom']`
循环词典：
```
dic = {'lilei': 90, 'lily': 100, 'sam': 57, 'tom': 90}
for key in dic:
    print dic[key]
```
判断存在：

要避免key不存在的错误，有两种办法，一是通过`in`判断key是否存在：

```
>>> 'Thomas' in d
False

```

二是通过dict提供的get方法，如果key不存在，可以返回None，字符串或者自己指定的value：

```python
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
```

注意：返回`None`的时候Python的交互式命令行不显示结果。

牢记的第一条就是dict的key必须是**不可变对象**。

这是因为dict根据key来计算value的存储位置，如果每次计算相同的key得出的结果不同，那dict内部就完全混乱了。这个通过key计算位置的算法称为哈希算法（Hash）。

要保证hash的正确性，作为key的对象就不能变。在Python中，字符串、整数等都是不可变的，因此，可以放心地作为key。

常用方法：

```
>>>print dic.keys()           # 返回dic所有的键
>>>print dic.values()         # 返回dic所有的值
>>>print dic.items()          # 返回dic所有的元素（键值对）
>>>dic.clear()                # 清空dic，dict变为{}
>>>del dic['tom']             # 删除 dic 的‘tom’元素
del是Python中保留的关键字，用于删除对象。
与表类似，你可以用len()查询词典中的元素总数。
>>>print len(dic)
```

#### 集合set

set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。

set ( 集 合 ) 。 集 合 是 一 个 无 序 不 重 复 元素 的 集 。 基 本 功 能 包 括 关 系 测 试 和 消 除 重 复 元 素 。 集 合 对 象 还 支 持 union( 联
合),intersection(交),difference(差)和 sysmmetric difference(对称差集)等数学运算。
大括号或 set() 函数可以用来创建集合。

python中的set基于哈希表实现，存取时间可看做O(1)，但是没有办法高效的完成顺序相关的操作(比如找前驱后继，最大最小值等等)，所以认为是“无序”的。

 注意:想要创建空集合,你必须使用set() 而不是 {} 。{}用于创建空字典；

要创建一个set，需要提供一个list作为输入集合：

```
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}

```

注意，传入的参数`[1, 2, 3]`是一个list，而显示的`{1, 2, 3}`只是告诉你这个set内部有1，2，3这3个元素，显示的顺序也不表示set是有序的。。

重复元素在set中自动被过滤：

```
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}

```

通过`add(key)`方法可以添加元素到set中，可以重复添加，但不会有效果：

```
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}

```

通过`remove(key)`方法可以删除元素：

```
>>> s.remove(4)
>>> s
{1, 2, 3}

```

set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：

```
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}

```

set和dict的唯一区别仅在于没有存储对应的value，但是，set的原理和dict一样，所以，同样不可以放入可变对象，因为无法判断两个可变对象是否相等，也就无法保证set内部“不会有重复元素”。试试把list放入set，看看是否会报错。

```
a=set()
a.add(1)
a.add([3,4,5])
print(a) #TypeError: unhashable type: 'list'
```



### 文件操作

*   创建文件
        `对象名 = open(文件名，模式)`
        常用的模式：
  * r 打开只读文件，该文件必须存在。
    * r+ 打开可读写的文件，该文件必须存在。
    * w 打开只写文件，若文件存在则文件长度清为0，即该文件内容会消失。若文件不存在则 建立该文件。
    * w+ 打开可读写文件，若文件存在则文件长度清为零，即该文件内容会消失。若文件不存在则建立该文件。
    * a 以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。
    * a+ 以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。

      上述的形态字符串都可以再加一个b字符，如rb、w+b或ab＋等组合，加入b 字符用来告诉函数库打开的文件为二进制文件，而非纯文字文件。windows下文件是二进制，而linux不需要区分二进制和文件。
* 读取 
```
content = f.read(N)          # 读取N bytes的数据
content = f.readline()       # 读取一行
content = f.readlines()      # 读取所有行，储存在列表中，每个元素是一行。
```
* 写入
  `f.write('I like apple!\n')      # 将'I like apple'写入文件并换行`
* 关闭文件
  `f.close()`

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



### 模块

相当与引用其他.py文件，类似于java中的引入包。
`import 文件名`
使用其他文件中的对象：`文件名(模块).对象`
其他引入方式：
```
import a as b             # 引入模块a，并将模块a重命名为b
from a import function1   # 从模块a中引入function1对象。调用a中对象时，我们不用再说明模块，即直接使用function1，而不是a.function1。
from a import *           # 从模块a中引入所有对象。调用a中对象时，我们不用再说明模块，即直接使用对象，而不是a.对象。
```
### 模块包
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



### 包裹传递
* 在传递函数的参数时，我们不知道有多少个参数，这时可以传递包裹
```
def func(*name):
    print type(name)
    print name

func(1,4,6)
func(5,6,7,1,2,3)
```
所有的参数被name收集，根据位置合并成一个元组(tuple)，这就是包裹位置传递。

* 包裹关键字传递：
```
def func(**dict):
    print type(dict)
    print dict

func(a=1,b=9)
func(m=2,n=1,c=11)
```
与上面一个例子类似，dict是一个字典，收集所有的关键字，传递给函数func。为了提醒Python，参数dict是包裹关键字传递所用的字典，在dict前加 * *

* 定义的时候没有定义包裹也可以在传递的时候用：
```
def func(a,b,c):
    print a,b,c

args = (1,3,4)
func(*args)
# 相应的：
dict = {'a':1,'b':2,'c':3}
func(**dict)
```
### 循环设计
* range()
```
S = 'abcdefghijk'
for i in range(0,len(S),2):
    print S[i]
```

* enumerate()
  利用enumerate()函数，可以在每次循环中同时得到下标和元素：
```
S = 'abcdefghijk'
for (index,char) in enumerate(S):
    print index
    print char
```
实际上，enumerate()在每次循环中，返回的是一个包含两个元素的定值表(tuple)，两个元素分别赋予index和char。

* zip()
  如果你多个等长的序列，然后想要每次循环时从各个序列分别取出一个元素，可以利用zip()方便地实现：
```
ta = [1,2,3]
tb = [9,8,7]
tc = ['a','b','c']
for (a,b,c) in zip(ta,tb,tc):
    print(a,b,c)
```
zip()函数的功能，就是从多个列表中，依次各取出一个元素。每次取出的(来自不同列表的)元素合成一个元组，合并成的元组放入zip()返回的列表中。zip()函数起到了聚合列表的功能。
分解聚合后的列表：
```
ta = [1,2,3]
tb = [9,8,7]

# cluster
zipped = zip(ta,tb)
print(zipped)

# decompose
na, nb = zip(*zipped)
print(na, nb)
```
### 循环对象
在python3中有个__next__() 方法，进行到下个结果，最后出现StopIteration错误
假设有个test.txt的文件：、
```
1234
abcd
efg
```
运行python命令：
```
>>>f = open('test.txt')
>>>f.next()
>>>f.next()
..#直到最后出现stoplteration.
```
### 列表生成式

列表生成式即List Comprehensions，是Python内置的非常简单却强大的可以用来创建list的生成式。

举个例子，要生成list `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`可以用`list(range(1, 11))`：

```
>>> list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

```

但如果要生成`[1x1, 2x2, 3x3, ..., 10x10]`怎么做？方法一是循环：

```
>>> L = []
>>> for x in range(1, 11):
...    L.append(x * x)
...
>>> L
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

```

但是循环太繁琐，而列表生成式则可以用一行语句代替循环生成上面的list：

```
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

```

写列表生成式时，把要生成的元素`x * x`放到前面，后面跟`for`循环，就可以把list创建出来，十分有用，多写几次，很快就可以熟悉这种语法。

for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：

```
>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]

```

还可以使用两层循环，可以生成全排列：

```
>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

### 生成器

通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。

所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，称为生成器：generator。

要创建一个generator，有很多种方法。第一种方法很简单，只要把一个列表生成式的`[]`改成`()`，就创建了一个generator：

```
>>> L = [x * x for x in range(10)]
>>> L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> g = (x * x for x in range(10))
>>> g
<generator object <genexpr> at 0x1022ef630>

```

创建`L`和`g`的区别仅在于最外层的`[]`和`()`，`L`是一个list，而`g`是一个generator。

我们可以直接打印出list的每一个元素，但我们怎么打印出generator的每一个元素呢？当然是for循环。

用`for`循环调用generator时，发现拿不到generator的`return`语句的返回值。如果想要拿到返回值，必须捕获`StopIteration`错误，返回值包含在`StopIteration`的`value`中：

```python
ef fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

>>> g = fib(6)
>>> while True:
...     try:
...         x = next(g)
...         print('g:', x)
...     except StopIteration as e:
...         print('Generator return value:', e.value)
...         break
...
g: 1
g: 1
g: 2
g: 3
g: 5
g: 8
Generator return value: done
```

---

上面是定义生生成器的一种方法，还有一种方法：

著名的斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到：

1, 1, 2, 3, 5, 8, 13, 21, 34, ...

斐波拉契数列用列表生成式写不出来，但是，用函数把它打印出来却很容易：

```
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'

```

*注意*，赋值语句：

```
a, b = b, a + b

```

相当于：

```
t = (b, a + b) # t是一个tuple
a = t[0]
b = t[1]

```

但不必显式写出临时变量t就可以赋值。仔细观察，可以看出，`fib`函数实际上是定义了斐波拉契数列的推算规则，可以从第一个元素开始，推算出后续任意的元素，这种逻辑其实非常类似generator。

也就是说，上面的函数和generator仅一步之遥。要把`fib`函数变成generator，只需要把`print(b)`改为`yield b`就可以了。

这就是定义generator的另一种方法。

**如果一个函数定义中包含`yield`关键字，那么这个函数就不再是一个普通函数，而是一个generator。**



generator的主要目的是构建一个用户自定义的循环对象，编写方法和函数相似，只是把return的地方改为yield，每次运行到生成器的时候在yield处暂停，返回yield后面值，当再次调用的时候，从暂停的地方继续运行，每次循环使用一个yield返回的值。
```
def gen():
    a = 100
    yield a
    a = a*8
    yield a
    yield 1000
```
#### 生成器表达式：
```
def gen():
    for i in range(4):
        yield i
```
等价于：
`G=(x for x in range(4))`



### 迭代器

我们已经知道，可以直接作用于`for`循环的数据类型有以下几种：

一类是集合数据类型，如`list`、`tuple`、`dict`、`set`、`str`等；

一类是`generator`，包括生成器和带`yield`的generator function。

这些可以直接作用于`for`循环的对象统称为可迭代对象：`Iterable`。

而生成器不但可以作用于`for`循环，还可以被`next()`函数不断调用并返回下一个值，直到最后抛出`StopIteration`错误表示无法继续返回下一个值了。

可以被`next()`函数调用并不断返回下一个值的对象称为迭代器：`Iterator`。

生成器都是`Iterator`对象，但`list`、`dict`、`str`虽然是`Iterable`，却不是`Iterator`。

把`list`、`dict`、`str`等`Iterable`变成`Iterator`可以使用`iter()`函数：

```
>>> isinstance(iter([]), Iterator)
True
>>> isinstance(iter('abc'), Iterator)
True
```


### 函数
#### lambda表达
```
def func(x,y):
    return x+y
----------------
func = lambda x,y:x+y
```

关键字`lambda`表示匿名函数，冒号前面的`x`表示函数参数。

匿名函数有个限制，就是只能有一个表达式，不用写`return`，返回值就是该表达式的结果。

#### map()函数

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

#### filter()函数(根据条件判断)
filter函数的第一个参数也是一个函数对象。它也是将作为参数的函数对象作用于多个元素。如果函数对象返回的是True，则该次的元素被储存于返回的表中。 filter通过读入的函数来筛选数据。同样，在Python 3.X中，filter返回的不是表，而是循环对象。
```python
def func(a):
    if a > 100:
        return True
    else:
        return False

print filter(func,[10,56,101,500])
```

#### reduce()函数(累积传参）
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

#### sorted

`sorted()`函数就可以对list进行排序：

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

要进行反向排序，不必改动key函数，可以传入第三个参数`reverse=True`：

```
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']

```

从上述例子可以看出，高阶函数的抽象能力是非常强大的，而且，核心代码可以保持得非常简洁。key是一个函数，自己也可以按功能定义。



#### 函数式编程

函数式编程就是一种抽象程度很高的编程范式，纯粹的函数式编程语言编写的函数没有变量，因此，任意一个函数，只要输入是确定的，输出就是确定的，这种纯函数我们称之为没有副作用。而允许使用变量的程序设计语言，由于函数内部的变量状态不确定，同样的输入，可能得到不同的输出，因此，这种函数是有副作用的。

函数式编程的一个特点就是，允许把函数本身作为参数传入另一个函数，还允许返回一个函数！

Python对函数式编程提供部分支持。由于Python允许使用变量，因此，Python不是纯函数式编程语言。

* 高阶函数

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



#### 闭包

```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
```

在这个例子中，我们在函数`lazy_sum`中又定义了函数`sum`，并且，内部函数`sum`可以引用外部函数`lazy_sum`的参数和局部变量，当`lazy_sum`返回函数`sum`时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。

注意到返回的函数在其定义内部引用了局部变量`args`，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。

另一个需要注意的问题是，返回的函数并没有立刻执行，而是**直到调用了f()`**才执行。我们来看一个例子：

```python
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

```

你可能认为调用`f1()`，`f2()`和`f3()`结果应该是`1`，`4`，`9`，但实际结果是：

```
>>> f1()
9
>>> f2()
9
>>> f3()
9

```

全部都是`9`！原因就在于返回的函数引用了变量`i`，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量`i`已经变成了`3`，因此最终结果为`9`。

为什么要闭包？

```python
def funx():
    x=5
    def funy():
        nonlocal x
        x+=1
        return x
    return funy
 
>>> a=funx()
>>> a()
6
>>> a()
7
>>> a()
8
>>> a()
9
>>> x
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    x
NameError: name 'x' is not defined
>>> 
```

我们会发现，funx中的x变量原本仅仅是funx的一个局部变量。但是形成了闭包之后，它的行为就好像是一个全局变量一样。但是最后的错误说明x并不是一个全局变量。其实这就是闭包的一个十分浅显的作用，形成闭包之后，闭包变量能够随着闭包函数的调用而实时更新，就好像是一个全局变量那样。（注意我们上面的a=funx()，a实际上应该是funy，所以a称为闭包）

##### global and nonlocal

global关键字用来在函数或其他局部作用域中使用全局变量。但是如果不修改全局变量也可以不使用global关键字。

正确eg:

```python
In [13]: b
Out[13]: 1

In [14]: def func1():
    ...:     global b 
    ...:     b = 3 
    ...:     

In [15]: func1()

In [16]: b
Out[16]: 3
```

错误eg:

```
In [10]: b=1

In [11]: def func():
    ...:     b = 2
    ...:     

In [12]: func()

In [13]: b
Out[13]: 1
```



nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量。python2 不支持

#### 装饰器

```python
>>> def now():
...     print('2015-3-25')
...
>>> f = now
>>> f()
2015-3-25

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
--------------
@log		#把@log放到now()函数的定义处，相当于执行了语句：now = log(now)
def now():
    print('2015-3-25')
   
>>> now()
call now():
2015-3-25
```

增强`now()`函数的功能，比如，在函数调用前后自动打印日志，但又不希望修改`now()`函数的定义，这种在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）



##### `@property`

Python内置的`@property`装饰器就是负责把一个方法变成属性调用的：

```python
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```

`@property`的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上`@property`就可以了，此时，`@property`本身又创建了另一个装饰器`@score.setter`，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：

```
>>> s = Student()
>>> s.score = 60 # OK，实际转化为s.set_score(60)
>>> s.score # OK，实际转化为s.get_score()
60
>>> s.score = 9999
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!

```

注意到这个神奇的`@property`，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。

还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性：

```
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth

```

上面的`birth`是可读写属性，而`age`就是一个**只读**属性，因为`age`可以根据`birth`和当前时间计算出来。

#### 偏函数

Python的`functools`模块提供了很多有用的功能，其中一个就是偏函数（Partial function）。要注意，这里的偏函数和数学意义上的偏函数不一样。

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
    ...
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

### 相等比较

```
#== 和 is的差别，==比较的是内容，is比较的是引用。
```



### 钩子

钩子来源于英文词Hook，在windows系统中，一切皆消息，比如按了一下键盘，也是一个消息，Hook的意思是勾住，也就是在消息过去之前，可以先把消息勾住，不让其传递，你可以优先处理，也即这项技术就是提供了一个入口，能够针对不同的消息或者API在执行前，先执行你的操作，你的操作也称为「钩子函数」。



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

* 使用内建的`isinstance`函数可以判断一个变量是不是字符串：

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
  ```

* 一般使用type()函数来看数据的类型：

   ```python
   a=(1,2,3)
   b=(x for x in range(3))
   print(type(a)) #<class 'tuple'>
   print(type(b)) #<class 'generator'>
   ```

   ​