Tags:[python] date: 2017-02-22 


### 搞清字符编码问题：

因为计算机只能处理数字，如果要处理文本，就必须先把文本转换为数字才能处理。最早的计算机在设计时采用8个比特（bit）作为一个字节（byte），所以，一个字节能表示的最大的整数就是255（二进制11111111=十进制255），如果要表示更大的整数，就必须用更多的字节。比如两个字节可以表示的最大整数是`65535`，4个字节可以表示的最大整数是`4294967295`。

由于计算机是美国人发明的，因此，最早只有127个字母被编码到计算机里，也就是大小写英文字母、数字和一些符号，这个编码表被称为`ASCII`编码，比如大写字母`A`的编码是`65`，小写字母`z`的编码是`122`。

但是要处理中文显然一个字节是不够的，至少需要两个字节，而且还不能和ASCII编码冲突，所以，中国制定了`GB2312`编码，用来把中文编进去。

你可以想得到的是，全世界有上百种语言，日本把日文编到`Shift_JIS`里，韩国把韩文编到`Euc-kr`里，各国有各国的标准，就会不可避免地出现冲突，结果就是，在多语言混合的文本中，显示出来会有乱码。

因此，Unicode应运而生。Unicode把所有语言都统一到一套编码里，这样就不会再有乱码问题了。

Unicode标准也在不断发展，但最常用的是用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节）。现代操作系统和大多数编程语言都直接支持Unicode。

现在，捋一捋ASCII编码和Unicode编码的区别：ASCII编码是1个字节，而Unicode编码通常是2个字节。

字母`A`用ASCII编码是十进制的`65`，二进制的`01000001`；

字符`0`用ASCII编码是十进制的`48`，二进制的`00110000`，注意字符`'0'`和整数`0`是不同的；

汉字`中`已经超出了ASCII编码的范围，用Unicode编码是十进制的`20013`，二进制的`01001110 00101101`。

你可以猜测，如果把ASCII编码的`A`用Unicode编码，只需要在前面补0就可以，因此，`A`的Unicode编码是`00000000 01000001`。

新的问题又出现了：如果统一成Unicode编码，乱码问题从此消失了。但是，如果你写的文本基本上全部是英文的话，用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。

所以，本着节约的精神，又出现了把Unicode编码转化为“可变长编码”的`UTF-8`编码。UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。如果你要传输的文本包含大量英文字符，用UTF-8编码就能节省空间。

UTF-8编码有一个额外的好处，就是ASCII编码实际上可以被看成是UTF-8编码的一部分，所以，大量只支持ASCII编码的历史遗留软件可以在UTF-8编码下继续工作

在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。

用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件：

![](http://claymore.wang:5000/uploads/big/ddd6dcd00e70088c7c2e37258a6128e2.png)



浏览网页的时候，服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器：

![](http://claymore.wang:5000/uploads/big/5b06c373a8c0aefaffad254317fcc01b.png)



### 了解编程环境编码

```python
print sys.getdefaultencoding()    #系统默认编码
print sys.getfilesystemencoding() #文件系统编码
print locale.getdefaultlocale()   #系统当前编码
print sys.stdin.encoding          #终端输入编码
print sys.stdout.encoding         #终端输出编码
```

设置系统编码：

```python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

源代码编码：

源代码编码指的是python程序本身的编码，默认为ascii。

在程序开头可指定编码格式。



### python2和python3的编码区别

#### python2

在python2中主要有str和unicode两种字符串类型，

`str`类似于C中的字符数组或者Java中的byte数组，事实上你可以将它理解为一个存储二进制内容的容器，`str`不存储编码信息，如果对`str`类型的字符串迭代的话，则会按照其在内存中的字节序依次迭代，意味着如果这个字符串存储的是多字节字符（Unicode/GBK等），则会截断这个字符：

```python
>>> str1 = "这是一个str"
>>> for ch in str1:
...  print ch,
... 
栿  䠘 ¯ ⠸  ⠸ ª s t r
```

而对于`unicode`类型，Python在内存中存储和使用的时候是按照UTF-8格式，在代码中的表示为字符串前加`u`，如：

```python
>>> str2 = "这是一个str"
>>> str2 = u"这是一个str"
>>> for ch in str2:
...  print ch,
... 
这 是 一 个 s t r
```



**str 和 unicode的转换：**

str 通过 decode 解码 为 unicode.

unicode 通过 encode 编码为 str. 

str 是一种被编码的方式，更难读。

```
>>> '天王盖地虎'.decode('utf-8')
u'\u5929\u738b\u76d6\u5730\u864e'
>>> u'天王盖地虎'.encode('utf-8')
'\xe5\xa4\xa9\xe7\x8e\x8b\xe7\x9b\x96\xe5\x9c\xb0\xe8\x99\x8e'
```

上述是我在linux命令终端里尝试的， 因为终端输入编码为utf-8, 所以用它decode('utf-8')不会有异常，同理在windows cmd默认输入中文为gbk， 我们用utf8 decode 就会有异常：

```python
>>> a.decode("utf-8")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "F:\Anaconda\envs\python27\lib\encodings\utf_8.py", line 16, in decode
    return codecs.utf_8_decode(input, errors, True)
UnicodeDecodeError: 'utf8' codec can't decode byte 0xcc in position 0: invalid continuation byte
>>> a.decode("gbk")   # 用gbk则不会。
u'\u5929\u738b\u76d6\u5730\u864e'
```







**b前缀：python2.x里, b前缀没什么具体意义， 只是为了兼容python3.x的这种写法**



**如果字符串是ascii码的话**，str和unicode是可以直接进行连接和比较，

不管是str还是unicode都可以直接写入文件，而不需要加上它是不是str的类型写入方式，

以Unicode表示的字符串用`u'...'`表示

如果unicode +str 的话 会自动转化成unicode.



#### python3

也分两种：

* str 字符串：是以Unicode编码的，字符串是字符串str对象。 相当于python2的unicode/
* bytes是字节流bytes对象, 是一个byte数组，相当于python2中的str。

**u'a'和‘a'**是等价的都是str字符串

由于Python的字符串类型是`str`，在内存中以Unicode表示，一个字符对应若干个字节。如果要在网络上传输，或者保存到磁盘上，就需要把`str`变为以字节为单位的`bytes`。

**bytes和str是两个独立的类型**。**python3中如果是写或者读bytes类型就必需带上’b’**.直接用b'字符串'表示bytes对象

所以在python3里u前缀也是兼容写法。

**str和byte的转换**

和python 相反。

字符串可以通过encode转化为bytes，bytes可以通过decode转化为字符串，

encode（‘编码方式’）时指定按那个编码转化为bytes。

反之，decode（‘编码方式’）指定按那种方式读取字节码（0和1构成的数字流）。

没有制定编码方式默认为`utf-8`



### 编辑页面的编码

编辑界面编码默认是ascii码，也就是写的程序语句默认是ascii编码，但一旦涉及到ascii码不能表示的，就隐形转换为系统默认编码表示，程序语句中的字符串默认是unicode码，也就是内存中的编码。

在py文件头声明文件的编码方式：

```
#-*-coding: utf-8-*-
```

指定编码方式是告诉系统按照什么编码来读这个py文件的。

**py文件的编码方式是ascii码，字符串默认编码是unicode码，指定编码方式是指定字符串的编码方式。**



### 读入文件编码

代码文件（py文件）本身也是一个文本，它也需要在硬盘或者其他载体上保存，默认编码是系统编码。这样的话，一旦py文件copy到不同平台，问题就会发生，出现乱码。

当从网络或者硬盘读入文件的时候，实质上读到的是字节流：

硬盘读入文件的默认编码方式是系统编码方式，当出现超过gbk范围的字节出现，报错！

网络读入文件时，因为读入的是字节，不会报错，但一旦要print时就会报错！

所以，如果不能按照读入文本的编码方式转化为unicode，就会出现问题。

处理方式：

因为read（）没有编码方式参数，只能读入bytes然后在解码为unicode码或者其他编码。

判断读入内容的编码方式可以用chardet的detect方法，接受一段bytes参数，返回一个结果的字典，里面包含编码方式和信度区间。

```python
import chardet
f=open('aaaa.txt','rb')
s=f.read()
chartest=chardet.detect(s)

print(chartest)
```

前提得下载chardet包。



### 一些问题

那如果它是字符串，我要转化为unicode码咋整？用encode指定unicode方式？

答：如果需要将内存用的unicode码直接保存，就指定编码方式是'unicode-escape'！

```python
>>> '中'.encode('unicode')

Traceback (most recent call last):  File "", line 1, inLookupError: unknown encoding: unicode

>>> '中'.encode('unicode-escape')

b'\u4e2d'
```



当声明字符串的时候末尾为\

```python
a = 'sdfsdf\',  # 这样会提示你没有引号， 
# 如果声明成一个windows路径
# 处理方式：
b = r"\\STORAGE-1\Testing\Test Data\ClearCore\Exports\5" "\\" 
# 等同于\\STORAGE-1\Testing\Test Data\ClearCore\Exports\5\
```

