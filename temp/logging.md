date: 2017-09-04



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

`logger = logging.getLogger(logger_name)`

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



#### Filter过滤器

完成比级别更复杂的过滤，

`filer = logging.filter(name='')`





### 基础配置

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
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
<<<<<<< HEAD

* level  知名根logger的级别。

=======
* level 指明根logger的级别。
>>>>>>> 4311e721b1e7241c2a2dcac45a7f4a834d173cab
* stream   使用指明的流来初始化StreamHandler。该参数与'filename'不兼容，如果两个都有，'stream'被忽略。

  指定输出到sys.stderr,sys.stdout或者文件，默认输出到sys.stderr。



#### 配置方式

* 显式创建记录器Logger、处理器Handler和格式化器Formatter，并进行相关设置；
* 通过简单方式进行配置，使用[basicConfig()](http://python.usyiyi.cn/python_278/library/logging.html#logging.basicConfig)函数直接进行配置；
* 通过配置文件进行配置，使用[fileConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.fileConfig)函数读取配置文件；
* 通过配置字典进行配置，使用[dictConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.dictConfig)函数读取配置信息；
* 通过网络进行配置，使用[listen()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.listen)函数进行网络配置。

eg: `logging.config.fileConfig("./logging.conf")`





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

