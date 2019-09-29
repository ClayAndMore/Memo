Tags:[python, py_lib] date: 2017-09-04



logging是python的内置库，用来输出日志和错误信息。

### 简单demo

```python
import logging

logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')
```

运行会输出后三个信息，因为默认级别为warn,只有高于等于这个级别的才会输出。

输出格式：

`warning : root : messages`   日志级别： logger实例名称，日志消息内容

用logging直接输出会生成一个系统的root logger,

**这个root log 最好不要设置，其他logger的输出root logger也会跟着输出。**

级别则为demo中的五个级别。

DEBUG：详细的信息,通常只出现在诊断问题上
INFO：确认一切按预期运行
WARNING：一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”)。这个软件还能按预期工作。
ERROR：更严重的问题,软件没能执行一些功能
CRITICAL：一个严重的错误,这表明程序本身可能无法继续运行



同时输出到屏幕和日志文件：

```python
import logging
logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```



### 几个概念

- Logger 记录器，暴露了应用程序代码能直接使用的接口。
- Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
- Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
- Formatter 格式化器，指明了最终输出中日志记录的布局。



####  Logger记录器

Logger是一个树形层级结构，在使用接口debug，info，warn，error，critical之前必须创建Logger实例，即创建一个记录器.

在调用getLogger时要提供Logger的名称（注：多次使用相同名称 来调用getLogger，返回的是同一个对象的引用。）

`logger = logging.getLogger(logger_name)`



logger记录;

```python
import logging
log = logging.getLogger()
log.debug('debug message')
log.info('info message')
log.warn('warn message')
log.error('error message')
log.critical('critical message')
```





如果没有显式的进行创建，

则默认创建一个root logger，并应用默认的日志级别(WARN)，

处理器Handler(StreamHandler，即将日志信息打印输出在标准输出上)，

和格式化器Formatter(默认的格式即为第一个简单使用程序中输出的格式)。

方法：

* logger.setLevel(logging.ERROR)  # 设置日志级别为ERROR，即只有日志级别大于等于ERROR的日志才会输出
* logger.addHandler(handler_name)  # 为Logger实例增加一个处理器
* logger.removeHandler(handler_name)   # 为Logger实例删除一个处理器



#### Handler处理器

常用的两个StreamHandler,FileHandler

`s_handler = logging.StreamHandler(stream=None)`

`f_handler = logging.FileHandler(filename, mode='a',encoding=None,delay=False)`



```python
import logging
 
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt="[%Y-%m-%d %H:%M:%S]")
 
root = logging.getLogger()
print(1,root.getEffectiveLevel()) #RootLogger,根Logger
 
log1 = logging.getLogger('s')
print(2,log1.getEffectiveLevel())
 
h1 = logging.FileHandler('test.log')
h1.setLevel(logging.WARNING)
log1.addHandler(h1)
print(3,log1.getEffectiveLevel())

log1.warning('log info---')
```

输出：

```
1 20
2 20
3 20
[2017-12-17 19:02:53] 7956 log info---
```

在根root输出log info 的同时，test.log中也会记录一份log info--, 



#### Filter过滤器

完成比级别更复杂的过滤，

`filer = logging.filter(name='')`

andler也可以设置使用logging.Formatter()设置格式和Logging.Filter()设置过滤器：

```python
import logging
 
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt="[%Y-%m-%d %H:%M:%S]")
 
root = logging.getLogger()
print(1,root.getEffectiveLevel()) #RootLogger,根Logger
 
log1 = logging.getLogger('s')#模块化用__module__，函数化用__name__作为Logger名，Logger同名内存中也只有一个
print(2,log1.getEffectiveLevel())
 
h1 = logging.FileHandler('test.log')
h1.setLevel(logging.WARNING)
fmt1 = logging.Formatter('[%(asctime)s] %(thread)s %(threadName)s log1-handler1 %(message)s')
h1.setFormatter(fmt1) #重新个性化定义记录的格式化字符串
log1.addHandler(h1)
filter1 = logging.Filter('s') #过滤器 会记录s, s.s2的信息
log1.addFilter(filter1)
print(3,log1.getEffectiveLevel())
 
log2 = logging.getLogger('s.s2')
print(4,log2.getEffectiveLevel())
 
h2 = logging.FileHandler('test1.log')
h2.setLevel(logging.WARNING)
log1.addHandler(h2)
filter1 = logging.Filter('s.s2') #过滤器不会记录s.s2的消息，只会记录自己的消息
log1.addFilter(filter1)
print(3,log1.getEffectiveLevel())
 
log1.warning('log1 warning===')
log2.warning('log2 warning---')
 
运行结果：
test.log: #handler1记录了到了log1和log2的信息
[2017-12-17 19:43:12,654] 5872 MainThread log1-handler1 log1 warning===
[2017-12-17 19:43:12,654] 5872 MainThread log1-handler1 log2 warning---
 
 
test1.log:    #handler2只记录了它自己的信息
log2 warning---
```





### 基础配置

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S', # 月份%m
                filename='myapp.log',
                filemode='w')
    
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
 
./myapp.log文件中内容为:
Sun, 24 May 2009 21:48:54 demo2.py[line:11] DEBUG This is debug message
Sun, 24 May 2009 21:48:54 demo2.py[line:12] INFO This is info message
Sun, 24 May 2009 21:48:54 demo2.py[line:13] WARNING This is warning message
```



`logging.basicConfig(filename='logger.log', level=logging.INFO)`

日志输出到同级的logger.log文件，并设置INFO级别。

* filename 创建一个FileHandler，使用指定的文件名，而不是使用StreamHandler。

* filemode 如果指明了文件名，指明打开文件的模式（如果没有指明filemode，默认为'a'）。

  * a 为追加
  * w 为重写， 每次写入会把上次写入的清除掉。

* format   handler使用指明的格式化字符串。

  format 可以输出很多有用的信息：

   %(levelno)s: 打印日志级别的数值
   %(levelname)s: 打印日志级别名称
   %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
   %(filename)s: 打印当前执行程序名
   %(funcName)s: 打印日志的当前函数
   %(lineno)d: 打印日志的当前行号
   %(asctime)s: 打印日志的时间
   %(thread)d: 打印线程ID
   %(threadName)s: 打印线程名称
   %(process)d: 打印进程ID
   %(message)s: 打印日志信息

* datefmt   使用指明的日期／时间格式。


* level 指明根logger的级别。
* **stream** ：设置特定的流用于初始化StreamHandler；


#### 配置方式

* 显式创建记录器Logger、处理器Handler和格式化器Formatter，并进行相关设置；
* 通过简单方式进行配置，使用[basicConfig()](http://python.usyiyi.cn/python_278/library/logging.html#logging.basicConfig)函数直接进行配置；
* 通过配置文件进行配置，使用[fileConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.fileConfig)函数读取配置文件；
* 通过配置字典进行配置，使用[dictConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.dictConfig)函数读取配置信息；
* 通过网络进行配置，使用[listen()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.listen)函数进行网络配置。

eg: `logging.config.fileConfig("./logging.conf")`



#### 继承方式

##### logging的继承

main.py:

```python
# main.py  
# coding=utf-8   
import logging  
import util  
  
logging.basicConfig(level=logging.INFO,  
                    filename='./log/log.txt',  
                    filemode='w',  
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  
def main():  
    logging.info('main module start')  
    util.fun()  
    logging.info('main module stop')  
  
if __name__ == '__main__':  
    main()  
```

uitl.py:

```python
# util.py  
__author__ = 'liu.chunming'  
import logging  
  
def fun():  
    logging.info('this is a log in util module')  
```

输出:

```
运行后打开log.txt，结果如下：
2015-05-21 18:10:34,684 - main.py[line:11] - INFO: main module start
2015-05-21 18:10:34,684 - util.py[line:5] - INFO: this is a log in util module
2015-05-21 18:10:34,684 - main.py[line:13] - INFO: main module stop
```

**注意** :子模块会跟着上级的logging走



##### logger的继承

```python
p = logging.getLogger("root")

c1 = logging.getLogger("root.c1")

c2 = logging.getLogger("root.c2")

例子中，p是父logger, c1,c2分别是p的子logger。c1, c2将继承p的设置。
p.setLevel(logging.INFO)
c1.setLevel(logging.WARNING)
c1级别在INFO时不会输出
```







#### 配置输出流

```python
 #!/usr/bin/python
    import sys
    import logging

    class InfoFilter(logging.Filter):
        def filter(self, rec):
            return rec.levelno in (logging.DEBUG, logging.INFO)

    logger = logging.getLogger('__name__')
    logger.setLevel(logging.DEBUG)

    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h1.addFilter(InfoFilter())
    h2 = logging.StreamHandler()
    h2.setLevel(logging.WARNING)

    logger.addHandler(h1)
    logger.addHandler(h2)
```





### 进阶

#### 格式输出：

如果有这样的错误：`[not all arguments converted during string formatting]`

改输出格式为标准如下两种： 

```
logging.info('date=%s', date)
logging.info('date={}'.format(date))
```

logger:

```python

```





#### 异常处理

logging.execption() 会和traceback 那样自动处理异常的详细信息：

```
except:
    logging.exception('Got exception on main handler') # 这个参数一定有一个，哪怕传''
    raise
```

输出：

```
ERROR:root:Got exception on main handler
Traceback (most recent call last):
  File "/tmp/teste.py", line 9, in <module>
    run_my_stuff()
NameError: name 'run_my_stuff' is not defined
```





#### 输出到控制台并输出到文件

```python
# coding=utf-8  
__author__ = 'liu.chunming'  
import logging  
  
# 第一步，创建一个logger  
logger = logging.getLogger()  
logger.setLevel(logging.INFO)    # Log等级总开关  
  
# 第二步，创建一个handler，用于写入日志文件  
logfile = './log/logger.txt'  
fh = logging.FileHandler(logfile, mode='w')  
fh.setLevel(logging.DEBUG)   # 输出到file的log等级的开关  
  
# 第三步，再创建一个handler，用于输出到控制台  
ch = logging.StreamHandler()  
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关  
  
# 第四步，定义handler的输出格式  
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)  
  
# 第五步，将logger添加到handler里面  
logger.addHandler(fh)  
logger.addHandler(ch)  
  
# 日志  
logger.debug('this is a logger debug message')  
logger.info('this is a logger info message')  
logger.warning('this is a logger warning message')  
logger.error('this is a logger error message')  
logger.critical('this is a logger critical message')  
```



### 问题

#### ValueError: incomplete format

format 设置了 `%(message)`, 

默认是`%(message)s`,  s代表可转换的字符串类型。应该用这种。