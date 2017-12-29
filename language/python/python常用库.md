date: 2017-08-31 



## 内置

### sys

* sys.argv  「argv」是「argument variable」参数变量的简写形式，一般在命令行调用的时候由系统传递给程序。

  这个变量其实是一个List列表，argv[0] 一般是被调用的脚本文件名或全路径，和操作系统有关，argv[1]和以后就是传入的数据了。

  test.py:

  ```
  import sys
  print sys.argv
  ```

  运行：python test.py -aaa bbb ccc

  输出：['test.py', '-aaa', 'bbb', 'ccc']

* sys.exc_info() 捕获异常信息，包括已异常类的名字和具体信息：

  ```python
  import sys
  try:
      raise ValueError
  except:
      print(sys.exc_info())
  (<class 'ValueError'>, ValueError(), <traceback object at 0x0000000002CF1108>)
  ```

* sys.path.insert(0,path)   path是系统路径的一个列表，这条语句是将path路径插入到path的第一个位置，这样在import时候更容易被搜索到，提高效率。




### os

`os.system(cmd)`   执行shell 命令。

`os.getpid()`  获得当前python进程pid，当我们想要在代码中结束当前服务时，可以杀掉该进程。

#### 路径操作

`os.getcwd() `  获得父目录路径

`os.makedirs(path,mode)`   递归创建目录 ,  如果其中有一个目录存在则异常，mode 默认 0777

`os.mkdir(path,mode)`  创建目录，如果最后一个文件的父目录不存在则异常 ， mode 默认 0777

`os.chmod(path, mode)` 更改文件或目录的权限，无返回值。

`os.chdir(paht) `方法用于改变当前工作目录到指定的路径。如果允许访问返回 True , 否则返回False。



####　文件操作

`os.mknod(“test.txt”)`  创建空文件 

`os.unlink('path/file')`  删除文件，如果是目录则返回一个错误。



#### 判断目标

`os.path.exists(“goal”)  `判断目标是否存在 
`os.path.isdir(“goal”)`  判断目标是否目录 
`os.path.isfile(“goal”) `  判断目标是否文件





 `os.access(path, mode)` 用当前的uid/gid尝试访问路径。大部分操作使用有效的 uid/gid, 因此运行环境可以在 suid/sgid 环境尝试。如果允许访问返回 True , 否则返回False。

- **path** -- 要用来检测是否有访问权限的路径。
- **mode** -- mode为F_OK，测试存在的路径，或者它可以是包含R_OK, W_OK和X_OK或者R_OK, W_OK和X_OK其中之一或者更多。
  - **os.F_OK:** 作为access()的mode参数，测试path是否存在。
  - **os.R_OK:** 包含在access()的mode参数中 ， 测试path是否可读。
  - **os.W_OK** 包含在access()的mode参数中 ， 测试path是否可写。
  - **os.X_OK** 包含在access()的mode参数中 ，测试path是否可执行。



#### `os.path`

* os.path.abspath  返回当前目录下文件的绝对路径。
* os.path.basename() 
* os.path.dirname(`__file__`)    如果以全路径进行输出父目录路径，如果相对路径运行则输出空
* os.path.realpath  返回真实地址，如软连接的真实地址。



#### `os.environ `

获取环境变量的值，environ是一个字符串所对应环境的映像对象。如environ['HOME']就代表了当前这个用户的主目录。

linux：

os.environ['USER']:当前使用用户。

os.environ['LC_COLLATE']:路径扩展的结果排序时的字母顺序。

os.environ['SHELL']:使用shell的类型。

os.environ['LAN']:使用的语言。

os.environ['SSH_AUTH_SOCK']:ssh的执行路径。



`os.walk`遍历目录

`os.tmpnam` 创建一个临时文件夹并返回路径：`/tmp/文件夹`



### json

* json.dumps 用于将 Python 对象编码成 JSON 字符串。

  ```python
  In [1]: import json

  In [2]: data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

  In [3]: json = json.dumps(data)

  In [4]: print json
  [{"a": 1, "c": 3, "b": 2, "e": 5, "d": 4}]
  ```

* json.loads 解码 JSON 数据。该函数返回 Python 字段的数据类型。

  ```python
  import json
  jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
  text = json.loads(jsonData)
  print text
  {u'a': 1, u'c': 3, u'b': 2, u'e': 5, u'd': 4}
  ```

  注意： json的str转会python变成了unicode而不是str

  ​



python向json类型转换：

| Python           | JSON   |
| ---------------- | ------ |
| dict             | object |
| list, tuple      | array  |
| str, unicode     | string |
| int, long, float | number |
| True             | true   |
| False            | false  |
| None             | null   |

json向python类型转换：

| JSON          | Python    |
| ------------- | --------- |
| object        | dict      |
| array         | list      |
| string        | unicode   |
| number (int)  | int, long |
| number (real) | float     |
| true          | True      |
| false         | False     |
| null          | None      |

注意： json的str转会python变成了unicode而不是str



### traceback

输出异常位置和信息，如普通我们获取异常：

```
try:
	1/0
except Exception,e:
	print e
```

out:

root@Claymore:~# python test.py 
integer division or modulo by zero

用该模块

```python
import traceback
try:
    1/0 
except Exception,e:
    traceback.print_exc()
```

out:

root@Claymore:~# python test.py 
Traceback (most recent call last):
  File "test.py", line 89, in <module>
1/0

ZeroDivisionError: integer division or modulo by zero

会告诉异常位置和具体异常类信息。

traceback.print_exc()跟traceback.format_exc()有什么区别呢？

format_exc()返回字符串，print_exc()则直接给打印出来。

即traceback.print_exc()与print traceback.format_exc()效果是一样的。

print_exc()还可以接受file参数直接写入到一个文件。比如

traceback.print_exc(file=open('tb.txt','w+'))

写入到tb.txt文件去。



### collections

#### defaultdict

它是dict的内建子类，常用于为字典赋默认值。

参数是int,set,list,dict ,str等，也可以是函数，lamda表达式。默认为None，

为None时，和dict函数没有什么不同。

demo:

```python
from collections import defaultdict
s='abcd'
d=defaultdict(int):
for x in s:
	 d[x]+=1
print d
```

out: `defaultdict(<type 'int'>, {'a': 1, 'c': 1, 'b': 1, 'd': 1})`

d[x]这样不会出错，会有默认值0.

赋复杂的值：

```
>>> from collections import defaultdict
>>> d = defaultdict(list)
>>> for i in [1,2,3]:
...     d['eric'].append(i)
...
>>> d
defaultdict(<class 'list'>, {'eric': [1, 2, 3]})

>>> d['amy'] = {}
>>> d['amy']['a'] = 1
>>> d
defaultdict(<class 'list'>, {'eric': [1, 2, 3], 'amy': {'a': 1}}
```

赋值函数：

```
>>> from collections import defaultdict
>>> def zero():
...     return 0
...
>>> d = defaultdict(zero)
>>> d['eric']
0
>>> d
defaultdict(<function zero at 0x100662e18>, {'eric': 0})
```

吧上面变成lamba表达式：

```python
d=defaultdict(lambad:0)
d['amy']
0
```





### subprocess

subprocess最早是在2.4版本中引入的。
用来生成子进程，并可以通过管道连接它们的输入/输出/错误，以及获得它们的返回值。

它用来代替多个旧模块和函数:
os.system
os.spawn*
os.popen*
popen2.*
commands.*



subprocess 的目的就是启动一个新的进程并且与之通信。







### Queue

py2: `import Queue`  ,  py3: `import queue`

线程安全，可上锁，后续添加。





### singnal

Python 所用信号名和Linux一致，可通过`man 7 signal`查询。

这个包的核心是使用singnal.signal()函数来预设(register)信号处理函数：

`singnal.signal(signalnum, handler)`

signalnum为某个信号，handler为该信号的处理函数。我们在信号基础里提到，进程可以无视信号，可以采取默认操作，还可以自定义操作。当handler为signal.SIG_IGN时，信号被无视(ignore)。当handler为singal.SIG_DFL，进程采取默认操作(default)。当handler为一个函数名时，进程采取函数中定义的操作。

```python
import signal
# Define signal handler function
def myHandler(signum, frame):
    print('I received: ', signum)

# register signal.SIGTSTP's handler 
signal.signal(signal.SIGTSTP, myHandler)
signal.pause()
print('End of Signal Demo')
```

我们用signal.signal()函数来预设信号处理函数，当该进程接受到信号SIGTSTP时，会执行myHandler函数。

运行该程序，当程序运行到signal.pause()的时候，进程暂停并等待信号。此时，通过按下CTRL+Z向该进程发送SIGTSTP信号。

发信号：

一个有用的函数是signal.alarm()，它被用于在一定时间之后，向进程自身发送`SIGALRM`信号:

```python
import signal
# Define signal handler function
def myHandler(signum, frame):
    print("Now, it's the time")
    exit()

# register signal.SIGALRM's handler 
signal.signal(signal.SIGALRM, myHandler)
signal.alarm(5)
while True:
    print('not yet')
```

我们这里用了一个无限循环以便让进程持续运行。在signal.alarm()执行5秒之后，进程将向自己发出SIGALRM信号，随后，信号处理函数myHandler开始执行。

signal包的核心是设置信号处理函数。除了signal.alarm()向自身发送信号之外，并没有其他发送信号的功能。但在os包中，有类似于linux的kill命令的函数，分别为

os.kill(pid, sid)

os.killpg(pgid, sid)

分别向进程和进程组(见[Linux进程关系](http://www.cnblogs.com/vamei/archive/2012/10/07/2713023.html))发送信号。sid为信号所对应的整数或者singal.SIG*。



### socketserver

py2:Socketserver,  py3: socketserver





### argparse

是python的一个命令行解析包

http://www.jianshu.com/p/fef2d215b91d

1. 默认配置，也就是最单纯的写法：test.py

  ```python
  import argparse
  parse = argparse.ArgumentParser()
  parse.parse_args()
  ```

  这样只有自带的h参数生效： python test.py -h

2. 带固定参数

   ```python
   parser = argparse.ArgumentParser()
   parser.add_argument("echo")
   args = parser.parse_args()
   print args.echo
   ```

   不带参数`python test.py `会有错误提示，正确使用为：

   `python test.py hahaha`   输出 hahaha

3. 带可选参数

   ```python
   import argparse parser = argparse.ArgumentParser() 
   parser.add_argument("-v", "--verbosity", help="increase output verbosity") 
   args = parser.parse_args() 
   if args.verbosity: 
   	print "verbosity turned on"
   ```

    通过“-”，“--”来声明可选参数，调用形式：`python test.py --v 1`  1是v代表的参数，

   参数通过解析后存在parser.parse_args()中，如果没有给定则会报错。

   如果用那种不用给参数的，像-h,我们需要指定`action="store_true"`  eg:

   `parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")`这时 parse_args()存的是True或False ，通过解析则为True

4. 传递不同类型的的参数类型

   ```python
   import argparse parser = argparse.ArgumentParser() 
   parser.add_argument('x', type=int, help="the base") 
   args = parser.parse_args() 
   answer = args.x ** 2
   print answer
   ```

   传参时只能传int，eg:`python test.py 2`

   如果需要参数默认值： `parser.add_argument('x', type=int, help="the base",default=1) `

5. 为参数设立可选值

   ```
   parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                       help="increase output verbosity")
   ```

   这里可以和3中的对比，如果在0，1，2范围外的参数值将报错

6. 提供帮说明

   为整个文档提供帮助说明：

   ``argparse.ArgumentParser(description="calculate X to the power of Y"``

   这时在用帮助参数时会打印上述描述信息。


### shlex

用来解析一些类似shell的语句，或者是解析带引号的语句，将单词分离出来，特点是带引号的也能分离。

```python
import  shlex
a='This string has embedded "double quotes" and /"dj"'
p=shlex.split(a)
['This', 'string', 'has', 'embedded', 'double quotes', 'and', '/dj']
```

可以看到，如果字符旁有符号，也可以一起解析出来。那么这样用于解析shell语句相当方便：

```python
shlex.split("python -u a.py -a A    -b   B     -o test")
['python', '-u', 'a.py', '-a', 'A', '-b', 'B', '-o', 'test']
```



### timeit

检测一段代码的运行时间

```

>>> importtimeit

>>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)

0.8187260627746582

>>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)

0.7288308143615723

>>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)

0.5858950614929199
```



在linux系统中使用time.time()获得的精度更高，

在window系统中使用time.clock()获得的精度更高。

timeit.default_tmer() 基于平台选择精度高的记录时间方法。





### ConfigParser

读取配置文件的包



### binascii 

主要用于二进制和ASCII的互转，还有其他进制。



### shutil

高层次的文件操作，对文件的复制和删除支持较好。



## 非内置

### docopt

官方库：https://github.com/docopt/docopt

参数解析的库，将py文件的`__doc__`解析出来：

```python
"""val Fate.
 
Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version
 
Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
 
"""
from docopt import docopt
 
if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print arguments
```



这里只有vesion参数被指定。



### beanstalkd

beanstalkd是一个快速的、通用目的的work queue。协议简单，是个轻量级的消息中间件。 

beanstalk核心概念：

job:一个需要异步处理的任务，需要放在一个tube中。
tube:一个有名的任务队列，用来存储统一类型的job
producer:job的生产者
consumer:job的消费者

简单来说流程就一句话：
由 producer 产生一个任务 job ，并将 job 推进到一个 tube 中，
然后由 consumer 从 tube 中取出 job 执行（当然了，这一切的操作的前提是beanstalk服务正在运行中）

![](http://ojynuthay.bkt.clouddn.com/beanstalkd%E7%8A%B6%E6%80%81%E5%9B%BE.png)



beanstalkd拥有的一些特性：

* producer产生的任务可以给他分配一个优先级，支持0到2**32的优先级，值越小，优先级越高，默认优先级为1024。优先级高的会被消费者首先执行
* 持久化，可以通过binlog将job及其状态记录到文件里面，在Beanstalkd下次启动时可以通过读取binlog来恢复之前的job及状态。
* 分布式容错，分布式设计和Memcached类似，beanstalkd各个server之间并不知道彼此的存在，都是通过client来实现分布式以及根据tube名称去特定server获取job。
* 超时控制，为了防止某个consumer长时间占用任务但不能处理的情况， Beanstalkd为reserve操作设置了timeout时间，如果该consumer不能在指定时间内完成job，job将被迁移回READY状态，供其他consumer执行。


beanstalkc 是beanstalkd的python 简单客户端。



### psutil

 psutil是一个跨平台库，能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要应用于系统监控，分析和限制系统资源及进程的管理。



### chardet

有时我们不知道某字符串是什么编码，我们可以用这个模块检测，带有概率的检测：

```python
import chardet  
import urllib  
  
#可根据需要，选择不同的数据  
TestData = urllib.urlopen('http://www.baidu.com/').read()  
print chardet.detect(TestData)  
  
运行结果：  
{'confidence': 0.99, 'encoding': 'GB2312'}  
```

运行结果表示有99%的概率认为这段代码是GB2312编码方式。

```python 
import urllib  
from chardet.universaldetector import UniversalDetector  
usock = urllib.urlopen('http://www.baidu.com/')  
#创建一个检测对象  
detector = UniversalDetector()  
for line in usock.readlines():  
    #分块进行测试，直到达到阈值  
    detector.feed(line)  
    if detector.done: break  
#关闭检测对象  
detector.close()  
usock.close()  
#输出检测结果  
print detector.result  
  
运行结果：  
{'confidence': 0.99, 'encoding': 'GB2312'}  
```

应用背景，如果要对一个大文件进行编码识别，使用这种高级的方法，可以只读一部，去判别编码方式从而提高检测速度。