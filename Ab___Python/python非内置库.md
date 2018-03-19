## 非内置



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

