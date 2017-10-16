## beanstalkd

### 写在前面

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

- producer产生的任务可以给他分配一个优先级，支持0到2**32的优先级，值越小，优先级越高，默认优先级为1024。优先级高的会被消费者首先执行
- 持久化，可以通过binlog将job及其状态记录到文件里面，在Beanstalkd下次启动时可以通过读取binlog来恢复之前的job及状态。
- 分布式容错，分布式设计和Memcached类似，beanstalkd各个server之间并不知道彼此的存在，都是通过client来实现分布式以及根据tube名称去特定server获取job。
- 超时控制，为了防止某个consumer长时间占用任务但不能处理的情况， Beanstalkd为reserve操作设置了timeout时间，如果该consumer不能在指定时间内完成job，job将被迁移回READY状态，供其他consumer执行。

beanstalkc 是beanstalkd的python 简单客户端。



### 下载

先需要下载客户端：

ubuntu : `apt-get install beanstalkd`

centos:  https://kr.github.io/beanstalkd/download.html



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

* put 为入队操作，这里入队的为工作体，必须为string
* reserve() ,请求当前保留的任务
* delete  ,标记当前任务已经做完



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
每个客户端会管理两个不相干的部分：

use和using ，jobs put的部分。

watch和watching，jobs  reserve的部分。



