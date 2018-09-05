Ï=ate: 2017-08-31 



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

#### 系统操作

`os.system(cmd)`   执行shell 命令。

`os.getpid()`  获得当前python进程pid，当我们想要在代码中结束当前服务时，可以杀掉该进程。

`os.fork()`

fork 调用将生成一个子进程，所以这个函数会同时属于两个进程，父进程和子进程。也会返回两个值

在父进程的返回结果是一个整数值，这个值是子进程的进程号，父进程可以使用该进程号来控制子进程的运行。fork 在子进程的返回结果是零。

如果 fork 返回值小于零，一般意味着操作系统资源不足，无法创建进程。 

我们可以通过 fork 调用的返回值来区分当前的进程是父进程还是子进程。

```pytthon
if pid > 0:
    # in parent process
if pid == 0:
    # in child process
if pid < 0:
    # fork error
```

子进程创建后，父进程拥有的很多操作系统资源，子进程也会持有。比如套接字和文件描述符，它们本质上都是对操作系统内核对象的一个引用。如果子进程不需要某些引用，一定要即时关闭它，避免操作系统资源得不到释放导致资源泄露。 





#### 路径操作

`os.getcwd() `  获得父目录路径

`os.makedirs(path,mode)`   递归创建目录 ,  如果其中有一个目录存在则异常，mode 默认 0777

`os.mkdir(path,mode)`  创建目录，如果最后一个文件的父目录不存在则异常 ， mode 默认 0777

`os.chmod(path, mode)` 更改文件或目录的权限，无返回值。

`os.chdir(paht) `方法用于改变当前工作目录到指定的路径。如果允许访问返回 True , 否则返回False。



####　文件操作

`os.mknod(“test.txt”)`  创建空文件 

`os.mkdir('')` 创建新的文件夹

`os.unlink('path/file')`  删除文件，如果是目录则返回一个错误。

`os.remove()` 删除一个文件

`os.rmdir()` 删除一个空目录， 不是空返回异常

`os.walk()` 遍历文件和子文件：

​	`os.walk(top, topdown=True, onerror=None, followlinks=False)` 

返回一个3个元素的元祖，(dirpath, dirnames, filenames), 

```
- dirpath：要列出指定目录的路径
- dirnames：目录下的所有文件夹
- filenames：目录下的所有文件

参数一：top – 根目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。

参数二：topdown –可选，为True或者没有指定, 一个目录的的3-元组将比它的任何子文件夹的3-元组先产生 (目录自上而下)。如果topdown为 False, 一个目录的3-元组将比它的任何子文件夹的3-元组后产生 (目录自下而上)。

参数三：onerror – 可选，是一个函数; 它调用时有一个参数, 一个OSError实例。报告这错误后，继续walk,或者抛出exception终止walk。

参数四：followlinks – 设置为 true，则通过软链接访问目录。
```





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

* os.path.abspath(a)  返回当前目录下文件的绝对路径, 不管a是什么， 返回/../../../a
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

  注： 会将中文编译成unicode，并其他字段也会变成unicode,

  如果想将中文变成ascii 的str， 可使用 `encode('utf-8')`


  一些参数：

  ensure_ascii：默认值True，只做两件事：

  		1. 如果有非ASII的字符， 用utf-8解码。
  		2. 确保dumps后的数据为 str 字符数组。

如果dict内含有non-ASCII的字符，则会解码成utf-8的数据，去掉了u, 双斜杠转义单斜杠

  设置成False后，

  ```python
  >>> a={'a':'aa', 'b':'彻底'}
  >>> import json
  >>> json.dumps(a)
  '{"a": "aa", "b": "\\u5f7b\\u5e95"}'
  >>> '彻底'.decode('utf-8')
  u'\u5f7b\u5e95
  >>> '彻底'
  '\xe5\xbd\xbb\xe5\xba\x95'
  >>> json.dumps(a, ensure_ascii=False)
  '{"a": "aa", "b": "\xe5\xbd\xbb\xe5\xba\x95"}'
  ```

  ​

indent：应该是一个非负的整型，如果是0，或者为空，则一行显示数据，否则会换行且按照indent的数量显示前面的空白，这样打印出来的json数据也叫pretty-printed json

*encoding*：默认是UTF-8，设置json数据的编码方式。

```python

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

  ​	     如果里面用单引号，外面用双引号也会解析失败，规定里面只能用双引号，如果想load里面是单引号的：

  ```
  >>> import ast
  >>> s = "{'username':'dfdsfdsf'}"
  >>> ast.literal_eval(s)
  {'username': 'dfdsfdsf'}
  >>> type(s)
  <dict>
  ```

  ​

* json.dump(f), 

  ```python
  >>> with open('test.conf', 'w') as f:
  ...  json.dump({'b':'bb','c':'cc'},f)
  ```

  生成文件流​

  ​

* json.load(f),

  f为从文件读取出来的文件流，注意该文件内的josn格式 只能用双引号：

  ```
  {
      "a": "aaaa",
      "b": "bbbbbbb"
  }

  ```

  ​

对象的转换：

对python对象的转换： 

```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
print(json.dumps(s))
```

这样会毫不留情的得到一个TypeError.可选参数`default`就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为`Student`专门写一个转换函数，再把函数传进去即可：

```python
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

print(json.dumps(s, default=student2dict))
```



现在我们可以偷个懒，把任意`class`的实例变为`dict`：

```
print(json.dumps(s, default=lambda obj: obj.__dict__))
```



同样的道理，如果我们要把JSON反序列化为一个`Student`对象实例，`loads()`方法首先转换出一个`dict`对象，然后，可选参数object_hook`函数负责把`dict`转换为`Student实例：

```python
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))

<__main__.Student object at 0x10cd3c190>
打印出的是反序列化的Student实例对象。
```






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

默认输出到stderr.





### collections

#### defaultdict

它是dict的内建子类，常用于为字典赋默认值。

参数是int,set,list,dict ,str等，也可以是函数，lamda表达式。

参数默认为None，为None时，和dict函数没有什么不同。

demo:

```python
from collections import defaultdict
s='abcd'
d=defaultdict(int)
for x in s:
	 d[x]=1
print d
```

out: `defaultdict(<type 'int'>, {'a': 1, 'c': 1, 'b': 1, 'd': 1})`

d[x]这样也不会出错，会有默认值0.

默认值没给就是所赋值类型的默认值:

```python
from collections import defaultdict
a = defaultdic(dict)
>>>a['a']
>>>{}
```



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

s=defaultdict(lambad:[0])  # 注意这里我们可以赋值带类型有初始值的值
s['ss']
[0]
```



#### OderedDict

创建有序字典：

```python
import collections

dic = collections.OrderedDict()
dic['k1'] = 'v1'
dic['k2'] = 'v2'
dic['k3'] = 'v3'
print(dic)

#输出：OrderedDict([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
```





#### namedtuple 具名元组

它是一个工厂函数，它可以用来构建一个**带字段名的元祖**和一个右名字的类

```python
from collections import namedtuple
# 接受两个参数，类名，和各个字段的名字，可以是由数个字符串组成的可迭代对象，或者像下面这样由空格组成的可迭代对象
City = namedtuple("City", 'name country population') 
tokyo = City('Tokyo', 'JP', 36993)
tokyo
City(name='Tokyo', country='JP', population=36993)
tokyo.country  #通过名字获得信息
'JP'
tokey[0] # 通过位置获得信息
'Tokyo'
City._fields # 这个属性可以获得所有类属性的元祖
('name', 'country', 'population')
```

**用namedtuple构建等类等实例所消耗等内存和元祖是一样的**



#### deque类

我们可以用append和pop方法来把列表当做栈来用，但是这类操作比较费时，因为会移动所有的元素。

connections.deque类(双向队列)是一个线程安全，可以快速从两端添加或删除的数据类型。

```python
from collections import deque
dq = deque(range(10), maxlen=10) # maxlen可选，指明最大长度，一旦指明不能修改
dq.appendleft(-1) # 头部添加-1, 尾部的9会被删除。
dq.extend([11,22]) # 尾部添加，头部的2个元素会被挤掉
dp.popleft() #头部移除一个
dp.rotate(3) # 旋转操作，尾部3个到头部
```

Appendleft 和 popleft 都是原子操作，也就是说可以在多线程中安全使用。



### pprint

格式化输出字典(或其他可遍历对象)，用于json转dict时做的输出：

```
import pprint
pprint.pprint(dict)
```

输出到标准错误， 并层级间间隔为四：

`pprint.pprint(dict, indent=4, stream=sys.stderr)`

输出为字符串，而不是字典：

```
>>> import pprint
>>> pprint.pformat({'key1':'val1', 'key2':[1,2]})
"{'key1': 'val1', 'key2': [1, 2]}"
```





### subprocess

subprocess最早是在2.4版本中引入的。
用来生成子进程，并可以通过管道连接它们的输入/输出/错误，以及获得它们的返回值。

它用来代替多个旧模块和函数: `os.system os.spawn os.popen popen2  commands`

用法：

* `subprocess.call(args*, stdin=None, stdout=None, stderr=None, shell=False)`

  起子进程调用命令行，父进程等待子进程完成。

  返回值成功时一般为0。

  两种用法，eg：

  `a=subprocess.call(['ls', '-l'])`

  `b=subprocess.call('ls -l', shell=True)`

  此时a,b返回为零.

  **子进程的PID存储在a.pid**

subprocess 的目的就是启动一个新的进程并且与之通信。

* subprocess.Popen()

  subprocess的函数都是封装在Popen类中，调用方式和上方call函数一样

  注意，这时父进程不会等待子进程

  等待：

  ```
  >>> child = subprocess.Popen('ping -c4 blog.linuxeye.com',shell=True)
  >>> child.wait()
  >>> print 'parent process'
  ```

  其他方法：

  child.returncode() #获取进程的返回值。如果进程还没有结束，返回None。

  child.poll() # 检查子进程状态
  child.kill() # 终止子进程
  child.send_signal() # 向子进程发送信号
  child.terminate() # 终止子进程

* 文本流控制

  可以在Popen()建立子进程的时候改变标准输入、标准输出和标准错误，并可以利用`subprocess.PIPE`将多个子进程的输入和输出连接在一起，构成管道(pipe)，如下2个例子：

  复制代码 代码如下:

  **subprocess.PIPE实际上为文本流提供一个缓存区**。

  child1的stdout将文本输出到缓存区，随后child2的stdin从该PIPE中将文本读取走。child2的输出文本也被存放在PIPE中，直到communicate()方法从PIPE中读取出PIPE中的文本。

  ```
  >>> import subprocess
  >>> child1 = subprocess.Popen(["ls","-l"], stdout=subprocess.PIPE)
  >>> print child1.stdout.read(),
  #或者child1.communicate()
  >>> import subprocess
  >>> child1 = subprocess.Popen(["cat","/etc/passwd"], stdout=subprocess.PIPE)
  >>> child2 = subprocess.Popen(["grep","0:0"],stdin=child1.stdout, stdout=subprocess.PIPE)
  >>> out = child2.communicate()
  ```

  注意：communicate()是Popen对象的一个方法，该方法会阻塞父进程，直到子进程完成


  获取错误的输出：

  ```python
  import subprocess
  a=subprocess.Popen('ntpdate pool.ntp.org',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (out,err)=a.communicate()

  print 'err:' + str(err)
  print 'out:' + str(out)
  ```

  ​






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



### shutil

`shutil.rmtree() ` 会移除该文件夹所有内容，不管其中文件是否被占用。

`shutil.move('原文件夹/原文件名','目标文件夹/目标文件名')  `   把一个文件从一个文件夹移动到另一个文件夹，并同时重命名

`shutil.copy('源目录'， '目标目录')`

`shutil.copyfile('源目录', '目标目录')`

copyfile仅仅是把文件拷贝到目的文件。但是copy函数可以把文件的mode也一起拷贝。比如说原来的文件有+x可执行权限，那么目的文件也会有可执行权限。

`shutil.make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0,dry_run=0, owner=None, group=None, logger=None)` 要锁打包



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

>>> import timeit

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



### StringIO 和 cStringIO

StringIO的行为与file对象非常像，但它不是磁盘上文件，而是一个内存里的“文件”，我们可以将操作磁盘文件那样来操作StringIO。

将字符串当成一个文件一样使用，具备和文件一样的 read 和 write 操作。

Python 提供了两个实现，一个是纯 Python 实现 StringIO，一个是底层 C 的实现 cStringIO。 

```python
from StringIO import StringIO  
  
# 生成一个StringIO对象，当前缓冲区内容为ABCDEF    
s = StringIO('ABCDEF')  
# 从开头写入，将会覆盖ABC  
s.write('abc')  
# 每次使用read()读取前，必须seek()  
# 定位到开头  
s.seek(0)  
# 将输出abcDEF  
print s.read()  
# 定位到第三个字符c  
s.seek(2)  
# 从当前位置一直读取到结束，将输出cDEF  
print s.read()  
s.seek(3)  
# 从第三个位置读取两个字符，将输出DE  
print s.read(2)  
s.seek(6)  
# 从指定位置写入  
s.write('GH')  
s.seek(0)  
# 将输出abcDEFGH  
print s.read()  
# 如果读取所有内容，可以直接使用getvalue()  
# 将输出abcDEFGH  
print s.getvalue()  
```



### webbrowser

用python调用浏览器打开一个网址： 

`webbrowser.open(url)`



### 常用内建模块

#### datetime

经常听到的Unix时间戳，UTC时间，格林威治时间等，从表示上来讲他们基本属于同一个东西，因为他们的时间表示都是从1970年.1月.1日开始到现在的秒数。

为什么是这个日期呢，因为这天是unix诞生的时间。

python有两个时间模块，time和datetime.

time时间戳只支持到了2038年，我们还是用封装了time模块的datetime模块。



datetime.date：表示日期的类。

 常用的属性有year, month, day；

datetime.time：表示时间的类。

 常用的属性有hour, minute, second, microsecond；

datetime.datetime：表示日期时间。

datetime.timedelta：表示时间间隔，即两个时间点之间的长度。

datetime.tzinfo：与时区有关的相关信息。



创建一个时间：

`d=datetime.datetime(2017,05,11,20,30,08)`

注意在python2中不要以0开头来创建一些数据。尽量把开头的零去掉，在python3中不会这样。



获取当前时间：

```python
import datetime
d1= datetime.datetime.now()
#转为字符串
d2=d1.strftime('%Y-%m-%d %H:%M:%S')
#字符串转为时间类型
date='2017-05-11 11:11:11'
d3=datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
```

日期符号：

```
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12） 
%M 分钟数（00=59）
%S 秒（00-59
```

日期和时间的比较

```
<= datetime.time #时间
>= datetime.date #日期
```



一个省力的技巧： 

```
str(datetime.date.today())
'2017-09-30'
```



时间戳转时间：

```python
import datetime
a = datetime.datetime.fromtimestamp(int("1172969203.1"))
>>> datetime.datetime(2007, 3, 4, 0, 46, 43, 100000)
a.strftime('%Y-%m-%d %H:%M:%S')
```





#### time

UTC: 协调世界时。世界不同时区的⼀个基准，⽐如中国为 UTC+8。

* epoch: 基准点。1970-01-01 00:00:00 UTC。

    ```python
    >>> from time import *
    >>> t = time()
    >>> t
    1357761634.903692
    >>> gmtime(t)! ! ! # epoch -> UTC 
    time.struct_time(tm_year=2013, tm_mon=1, tm_mday=9, tm_hour=20, tm_min=0, tm_sec=34,
    tm_wday=2, tm_yday=9, tm_isdst=0)
    >>> localtime(t)! ! ! # epoch -> Local (UTC+8)
    time.struct_time(tm_year=2013, tm_mon=1, tm_mday=10, tm_hour=4, tm_min=0, tm_sec=34,
    tm_wday=3, tm_yday=10, tm_isdst=0)
    ```

     time() 返回⾃ epoch 以来的秒数，gmtime()、localtime() 将其转换为 struct_time 结构体, 但是其中差别看注释。

* 将 struct_time 转回 epoch：

    ```python
    >>> from calendar import timegm
    >>> t = time()
    >>> t
    1357762219.162796
    >>> utc = gmtime(t)!! ! # epoch -> UTC
    >>> timegm(utc)! ! ! # UTC -> epoch
    1357762219
    >>> local = localtime(t)! ! # epoch -> local
    >>> mktime(local)! ! ! # local -> epoch
    1357762219
    ```

* time 于datetime 互转

    ```python
    >>> from datetime import datetime
    >>> from time import time
    >>> t = time()
    >>> d = datetime.fromtimestamp(t)! ! # localtime 时间
    >>> d
    datetime.datetime(2013, 1, 10, 4, 20, 27, 301148)
    --- 转回去 time - datetime ---
    >>> d.timetuple()
    time.struct_time(tm_year=2013, tm_mon=1, tm_mday=10, tm_hour=4, tm_min=20, tm_sec=27,
    tm_wday=3, tm_yday=10, tm_isdst=-1)
    ```

* struct_time和字符串格式化互转

    ```python
    >>> t = time()
    >>> s = strftime("%Y-%m-%d %H:%M:%S", localtime(t))
    >>> s
    '2013-01-10 04:27:39'
    >>> strptime(s, "%Y-%m-%d %H:%M:%S")
    time.struct_time(tm_year=2013, tm_mon=1, tm_mday=10, tm_hour=4, tm_min=27, tm_sec=39,
    tm_wday=3, tm_yday=10, tm_isdst=-1)
    ```

* 其他

    clock: 返回当前进程消耗的CPU时间 (秒)。可以用来记录程序运行时间。
    sleep: 暂停进程 (秒，可以是⼩数，以便设置毫秒、微秒级暂停)。

    ```python
    >>> clock()
    0.56022400000000006
    >>> sleep(0.1)
    ```

    timezone: 与 UTC 的时差。
    tzname: 当前时区名称。

    ```python
    >>> timezone/3600
    -8
    >>> tzname
    ('CST', 'CST') # 北京时间，China Standard Time
    ```

    ​





#### collections

namedtuple:

Python有一个类似tuple的容器namedtuples（命名元组），位于collection模块中。namedtuple是继承自tuple的子类，可创建一个和tuple类似的对象，而且对象拥有可访问的属性。

示例1：

```
import collections
 
# 创建namedtuple
Student = collections.namedtuple('Student',['name','age','id'])
 
# 初始化
S = Student('snail','23','14335')
 
# 使用下标访问
print(S[1])    # 23
# 使用名字访问
print(S.name)  # snail
# 使用getattr()访问
print(getattr(S,'id'))  # 14335

```

示例2：

```
import collections
 
# 创建namedtuple
Student = collections.namedtuple('Student',['name','age','id'])
 
# 初始化
S = Student('snail','23','14335')
 
# 获得字段名
print(S._fields)  # ('name', 'age', 'id')
# 更改值
print(S._replace(name = 'test'))  # Student(name='test', age='23', id='14335')
 
# namedtuple转为OrderedDict
print(S._asdict())  # OrderedDict([('name', 'snail'), ('age', '23'), ('id', '14335')])
 
# 使用list构造namedtuple
li = ['panda', '12', '32343' ]
print(Student._make(li))  # Student(name='panda', age='12', id='32343')
 
# 使用dict构造namedtuple
di = { 'name' : "sucker", 'age' : 34 , 'id' : '544554' }
print(Student(**di))  # Student(name='sucker', age=34, id='544554')
```



#### base64

Base64是一种用64（2的6次方）个字符来表示任意二进制数据的方法。 

处理乱码的时候很好用。

将原字节8bit的字符串每6bit对应一个字符：

`['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']`

26 + 26 + 10 +2

因为不一定是6的倍数，再在编码的末尾加上1个或2个`=`号，表示补了多少字节。

```python
>>> import base64
>>> base64.b64encode('binary\x00string')
'YmluYXJ5AHN0cmluZw=='
>>> base64.b64decode('YmluYXJ5AHN0cmluZw==')
'binary\x00string'
```

由于标准的Base64编码后可能出现字符`+`和`/`，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符`+`和`/`分别变成`-`和`_`：

```python
>>> base64.b64encode('i\xb7\x1d\xfb\xef\xff')
'abcd++//'
>>> base64.urlsafe_b64encode('i\xb7\x1d\xfb\xef\xff')
'abcd--__'
>>> base64.urlsafe_b64decode('abcd--__')
'i\xb7\x1d\xfb\xef\xff'
```

由于`=`字符也可能出现在Base64编码中，但`=`用在URL、Cookie里面会造成歧义，所以，很多Base64编码后会把`=`去掉：

```
# 标准Base64:
'abcd' -> 'YWJjZA=='
# 自动去掉=:
'abcd' -> 'YWJjZA'
```

去掉`=`后怎么解码呢？因为Base64是把3个字节变为4个字节，所以，Base64编码的长度永远是4的倍数，因此，需要加上`=`把Base64字符串的长度变为4的倍数，就可以正常解码了。

请写一个能处理去掉`=`的base64解码函数：

```python
>>> base64.b64decode('YWJjZA==')
'abcd'
>>> base64.b64decode('YWJjZA')
Traceback (most recent call last):
  ...
TypeError: Incorrect padding
>>> safe_b64decode('YWJjZA')
'abcd'
```



#### struct

python没有专门处理字节的类型，b'str'这样可以表示字节，也就是b'str'表示了str的二进制。但是一个数字在传输的时候如何变成网络传输的字节流呢？

struct 模块解决了这个字节问题。

- pack() 函数可以把任意数据类型变成bytes.

  ```python
  >>> import struct
  >>> struct.pack('>I', 10240099)
  b'\x00\x9c@c'
  ```

  `pack`的第一个参数是处理指令，`'>I'`的意思是：

  `>`表示字节顺序是big-endian，也就是网络序，`I`表示4字节无符号整数。

  后面的参数个数要和处理指令一致。

- unpack() 可以把bytes变成相应的数据类型。

  ```python
  >>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
  (4042322160, 32896)
  ```

  根据`>IH`的说明，后面的`bytes`依次变为`I`：4字节无符号整数和`H`：2字节无符号整数。

  所以，尽管Python不适合编写底层操作字节流的代码，但在对性能要求不高的地方，利用`struct`就方便多了。

- demo:

  ```python
  value_in_bytes = struct.pack("I", 1024)  # 将一个整数编码成 4 个字节的字符串
  value, = struct.unpack("I", value_in_bytes)  # 将一个 4 字节的字符串解码成一个整数
  # 注意等号前面有个逗号，这个非常重要，它不是笔误。
  # 因为 unpack 返回的是一个列表，它可以将一个很长的字节串解码成一系列的元祖。...
  
  ```

  

#### 

#### itertools

#### contextlib

#### XML

#### HTMLParser

#### urllib

在3.x的版本中，urllib与urllib2已经合并为一个urllib库。

在2.x的版本中，urllib与urllib2并不是可以代替的，只能说2是一个补充。



#### urllib2

urlopen方法是urllib2模块最常用也最简单的方法，它打开URL网址，url参数可以是一个字符串url或者是一个Request对象。

　　对于可选的参数timeout，阻塞操作以秒为单位，如尝试连接（如果没有指定，将使用设置的全局默认timeout值）。实际上这仅适用于HTTP，HTTPS和FTP连接。

　　先看只包含URL的请求例子：

```
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
```

　　urlopen方法也可通过建立了一个Request对象来明确指明想要获取的url。调用urlopen函数对请求的url返回一个response对象。这个response类似于一个file对象，所以用.read()函数可以操作这个response对象

```
import urllib2
req = urllib2.Request('http://python.org/')
response = urllib2.urlopen(req)
the_page = response.read()
```

这里用到了`urllib2.``Request`类，对于上例，我们只通过了URL实例化了Request类的对象，其实Request类还有其他的参数。

post:

`req = urllib2.urlopen(url, dumps(target))`

设置超时时间：

`socket.setdefaulttimeout(5); # 超时 5秒`

