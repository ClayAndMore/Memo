Tags:[linux, linux_software, python, 消息队列]

## beanstalkd

### 写在前面

beanstalkd是一个快速的、通用目的的work queue。协议简单，是个轻量级的消息中间件。 断电可存储。

beanstalk核心概念：

job:一个需要异步处理的任务，需要放在一个tube中。
tube:一个有名的任务队列，用来存储统一类型的job
producer:job的生产者
consumer:job的消费者

简单来说流程就一句话：
由 producer 产生一个任务 job ，并将 job 推进到一个 tube 中，
然后由 consumer 从 tube 中取出 job 执行（当然了，这一切的操作的前提是beanstalk服务正在运行中）

![](http://claymore.wang:5000/uploads/big/eeac43ca75d26d92fc281fdfa9af9a18.png)



beanstalkd拥有的一些特性：

- producer产生的任务可以给他分配一个优先级，支持0到2**32的优先级，值越小，优先级越高，默认优先级为1024。优先级高的会被消费者首先执行
- 持久化，可以通过binlog将job及其状态记录到文件里面，在Beanstalkd下次启动时可以通过读取binlog来恢复之前的job及状态。
- 分布式容错，分布式设计和Memcached类似，beanstalkd各个server之间并不知道彼此的存在，都是通过client来实现分布式以及根据tube名称去特定server获取job。
- 超时控制，为了防止某个consumer长时间占用任务但不能处理的情况， Beanstalkd为reserve操作设置了timeout时间，如果该consumer不能在指定时间内完成job，job将被迁移回READY状态，供其他consumer执行。

Beanstalkd 不足:

**Beanstalkd 没有提供主备同步 + 故障切换机制, 在应用中有成为单点的风险。**实际应用中，可以用数据库为任务 (job) 提供持久化存储。



### 下载

先需要下载客户端：

ubuntu : `apt-get install beanstalkd`

centos:  https://kr.github.io/beanstalkd/download.html

源码安装：

```
tar -zxvf /usr/bin/beanstalkd/beanstalkd-1.9.tar.gz
cd beanstalkd
make install PERFIX=/usr/bin/beanstalkd
```



### beanstalkc

beanstalkc 是一个简单的python beanstalkd客户端,文档：https://beanstalkc.readthedocs.io/en/latest/tutorial.html

现在只支持python2.

github:https://github.com/earl/beanstalkc

pip: `pip install beanstalkc`

beanstalkc 还需要依赖于pyyaml

pip: `pip install pyyaml`

做一段代码测试：

```
>>> import beanstalkc
>>> beanstalk=beanstalkc.Connection(host='localhost', port=14711)
>>> beanstalk.put('hey!')
1
>>> job=beanstalk.reserve()
>>> job.body
'hey!'
>>> job.delete()
```

如果不指定host和端口，默认是localhost和11300

还有个可选参数`connect_timeout`  默认为1

* put 为入队操作，这里入队的为工作体，**必须为string**， 没有严格限制，也可以放个二进制数据：

  ```
  >>> _ = beanstalk.put('\x00\x01\xfe\xff')
  >>> job = beanstalk.reserve() ; print(repr(job.body)) ; job.delete()
  '\x00\x01\xfe\xff'
  ```

  是的我们可以将图片转换成sring data放入。

  延迟放入：

  正如下方状态图所示的那样。

* reserve() ,请求当前队列保留的任务, 如果没有那么将一直等着，这时候进程就等着了。

  reserve(10) , 等待超时时间为十秒，如果十秒内仍然没有人向队列投送，那么将返回None

  > `reserve` blocks until a job is ready, possibly forever. If that is not desired, we can invoke `reserve` with a timeout (in seconds) how long we want to wait to receive a job. If such a `reserve` times out, it will return `None`:

  ```
  >>> beanstalk.reserve(timeout=0) is None
  True
  ```
  如果用timeout=0那么将立即返回，注：

  **b.reserver() 会一直等，b.reserve(0) 会马上返回**

* delete  ,标记当前任务已经做完

* touch  , 重新记录当前超时时间， 




#### 状态机

```
   put with delay               release with delay
  ----------------> [DELAYED] <------------.
                        |                   |
                        | (time passes)     |
                        |                   |
   put                  v     reserve       |       delete
  -----------------> [READY] ---------> [RESERVED] --------> *poof*
                       ^  ^                |  |
                       |   \  release      |  |
                       |    `-------------'   |
                       |                      |
                       | kick                 |
                       |                      |
                       |       bury           |
                    [BURIED] <---------------'
                       |
                       |  delete
                        `--------> *poof*
```

图中所示方法都为python可用。





#### tubes

队列在这里被称为管道tubes

```
一般会有个默认管道,下面命令会查所有管道：
>>> beanstalk.tubes()
['default']

看目前客户端在用哪个管道：
>>> beanstalk.using()
'default'

使用一个管道：
>>> beanstalk.use('foo')
>>> beanstalk.tubes()
['default', 'foo']

当你再次使用default时，会去掉foo管道：
>>> beanstalk.use('default')
'default'
>>> beanstalk.using()
'default'
>>> beanstalk.tubes()
['default']

客户端会watching有jobs reserve 的管道，目前watching的管道：
>>> beanstalk.watching()
['default']

watching另外一个管道：
>>> beanstalk.watch('bar')
2
>>> beanstalk.watching()
['default', 'bar']

停止watch一个管道：
>>> beanstalk.ignore('bar')
2
>>> beanstalk.watching()
['default']

use和watch都会增加管道。
```
每个客户端会管理两个不相干的部分，一头放入队列job，一头获取队列job:

use和using ，jobs put的部分, 只能use一个tubes.

watch和watching，jobs  reserve的部分，能同时watch好多tubes.



#### Statistics

```python
>>> beanstalk.put('ho?')
3
>>> job = beanstalk.reserve()
>>> from pprint import pprint

# 查看job状态
>>> pprint(job.stats())                         # doctest: +ELLIPSIS
{'age': 0,
 ...
 'id': 3,
 ...
 'state': 'reserved',
 ...
 'tube': 'default'}

# 查看某队列状态
>>> pprint(beanstalk.stats_tube('default'))     # doctest: +ELLIPSIS
{...
 'current-jobs-ready': 0,
 'current-jobs-reserved': 0,
 'current-jobs-urgent': 0,
 ...
 'name': 'default',
 ...}

# 查看客户端状态
>>> pprint(beanstalk.stats())                   # doctest: +ELLIPSIS
{...
 'current-connections': 1,
 'current-jobs-buried': 0,
 'current-jobs-delayed': 0,
 'current-jobs-ready': 0,
 'current-jobs-reserved': 0,
 'current-jobs-urgent': 0,
 ...}
```





### 遇到的问题

#### 不是线程安全的

https://github.com/earl/beanstalkc/issues/30，

尽量一个客户端不要做参数在进程间传递，会引发一些异常。

一些源码分析：https://segmentfault.com/a/1190000016067218#articleHeader1