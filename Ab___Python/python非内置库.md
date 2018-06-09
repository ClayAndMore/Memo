## 非内置



### psutil

 psutil是一个跨平台库，能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要应用于系统监控，分析和限制系统资源及进程的管理。



### chardet

只支持python2.7 和 python3+

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



一般使用：

chardet.detect() 参数只接受  type 字节数组，否侧：

`TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>`



这就要根据python版本来区分了， 在python2中str(默认字符类型）为字节数组， 和字符前加b是等效的：

```python
>>> chardet.detect('hello')
{'confidence': 1.0, 'language': '', 'encoding': 'ascii'}
>>> chardet.detect(b'hello')
{'confidence': 1.0, 'language': '', 'encoding': 'ascii'}
>>> chardet.detect('天王盖地虎')
{'confidence': 0.0, 'language': None, 'encoding': None}
>>> chardet.detect('天王盖地虎'.decode('gbk').encode('utf-8'))
{'confidence': 0.9690625, 'language': '', 'encoding': 'utf-8'}
```



而python3中默认字符类型是str(unicode), 需要转换成字节数组：

```python
>>> chardet.detect('hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "F:\Anaconda\lib\site-packages\chardet\__init__.py", line 34, in detect
    '{0}'.format(type(byte_str)))
TypeError: Expected object of type bytes or bytearray, got: <class 'str'>
>>> chardet.detect(b'hello')
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
>>> chardet.detect(b'hello')
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
>>> chardet.detect(b'宝塔镇河妖')
  File "<stdin>", line 1
SyntaxError: bytes can only contain ASCII literal characters.
>>> chardet.detect('宝塔镇河妖'.encode('gbk'))
{'encoding': None, 'confidence': 0.0, 'language': None}
>>> chardet.detect('天王k盖地虎,宝塔镇河妖'.encode('gbk'))
{'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
```

当然字符长度长一些时才能更精准的识别。