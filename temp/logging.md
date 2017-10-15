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

级别则为demo中的五个级别。



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



`logging.basicConfig(filename='logger.log', level=logging.INFO)`

日志输出到同级的logger.log文件，并设置INFO级别。

* filename 创建一个FileHandler，使用指定的文件名，而不是使用StreamHandler。
* filemode 如果指明了文件名，指明打开文件的模式（如果没有指明filemode，默认为'a'）。
* format   handler使用指明的格式化字符串。
* datefmt   使用指明的日期／时间格式。
* level  知名根logger的级别。
* stream   使用指明的流来初始化StreamHandler。该参数与'filename'不兼容，如果两个都有，'stream'被忽略。



#### 配置方式

* 显式创建记录器Logger、处理器Handler和格式化器Formatter，并进行相关设置；
* 通过简单方式进行配置，使用[basicConfig()](http://python.usyiyi.cn/python_278/library/logging.html#logging.basicConfig)函数直接进行配置；
* 通过配置文件进行配置，使用[fileConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.fileConfig)函数读取配置文件；
* 通过配置字典进行配置，使用[dictConfig()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.dictConfig)函数读取配置信息；
* 通过网络进行配置，使用[listen()](http://python.usyiyi.cn/python_278/library/logging.config.html#logging.config.listen)函数进行网络配置。

eg: `logging.config.fileConfig("./logging.conf")`