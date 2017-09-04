date: 2017-08-31 



### 内置

#### os

`os.chdir(paht) `方法用于改变当前工作目录到指定的路径。如果允许访问返回 True , 否则返回False。

`os.chmod(path, mode)` 更改文件或目录的权限，无返回值。

`os.access(path, mode)` 用当前的uid/gid尝试访问路径。大部分操作使用有效的 uid/gid, 因此运行环境可以在 suid/sgid 环境尝试。如果允许访问返回 True , 否则返回False。

- **path** -- 要用来检测是否有访问权限的路径。
- **mode** -- mode为F_OK，测试存在的路径，或者它可以是包含R_OK, W_OK和X_OK或者R_OK, W_OK和X_OK其中之一或者更多。
  - **os.F_OK:** 作为access()的mode参数，测试path是否存在。
  - **os.R_OK:** 包含在access()的mode参数中 ， 测试path是否可读。
  - **os.W_OK** 包含在access()的mode参数中 ， 测试path是否可写。
  - **os.X_OK** 包含在access()的mode参数中 ，测试path是否可执行。

#### json

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



#### subprocess

subprocess最早是在2.4版本中引入的。
用来生成子进程，并可以通过管道连接它们的输入/输出/错误，以及获得它们的返回值。

它用来代替多个旧模块和函数:
os.system
os.spawn*
os.popen*
popen2.*
commands.*



#### binascii 

主要用于二进制和ASCII的互转，还有其他进制。



#### shutil

高层次的文件操作，对文件的复制和删除支持较好。



### 非内置

#### docopt

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



#### beanstalkd

beanstalkd是一个快速的、通用目的的work queue。协议简单，是个轻量级的消息中间件。 

beanstalk核心概念：

job:一个需要异步处理的任务，需要放在一个tube中。
tube:一个有名的任务队列，用来存储统一类型的job
producer:job的生产者
consumer:job的消费者

简单来说流程就一句话：
由 producer 产生一个任务 job ，并将 job 推进到一个 tube 中，
然后由 consumer 从 tube 中取出 job 执行（当然了，这一切的操作的前提是beanstalk服务正在运行中）

beanstalkd拥有的一些特性：

* producer产生的任务可以给他分配一个优先级，支持0到2**32的优先级，值越小，优先级越高，默认优先级为1024。优先级高的会被消费者首先执行
* 持久化，可以通过binlog将job及其状态记录到文件里面，在Beanstalkd下次启动时可以通过读取binlog来恢复之前的job及状态。
* 分布式容错，分布式设计和Memcached类似，beanstalkd各个server之间并不知道彼此的存在，都是通过client来实现分布式以及根据tube名称去特定server获取job。
* 超时控制，为了防止某个consumer长时间占用任务但不能处理的情况， Beanstalkd为reserve操作设置了timeout时间，如果该consumer不能在指定时间内完成job，job将被迁移回READY状态，供其他consumer执行。



beanstalkc 是beanstalkd的python 简单客户端。