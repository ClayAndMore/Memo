Tags:[python, py_lib]

### linux的信号量

linux中，信号(signal)就是一种向进程传递信息的方式。我们可以将信号想象成大楼的管理员往房间的信箱里塞小纸条。

相对于其他的进程间通信方式(interprocess communication， 比如说pipe, shared memory来说，信号所能传递的信息比较粗糙，只是一个整数。但正是由于传递的信息量少，信号也便于管理和使用。信号因此被经常地用于系统管理相关的任务，比如通知进程终结、中止或者恢复等等。

信号是由内核(kernel)管理的。

信号的产生方式多种多样，它可以是内核自身产生的，比如出现硬件错误(比如出现分母为0的除法运算，或者出现segmentation fault)，内核需要通知某一进程；也可以是其它进程产生的，发送给内核，再由内核传递给目标进程。

内核中针对每一个进程都有一个表存储相关信息(房间的信箱)。当内核需要将信号传递给某个进程时，就在该进程相对应的表中的适当位置写入信号(塞入纸条)，这样，就生成(generate)了信号。当该进程执行系统调用时，在系统调用完成后退出内核时，都会顺便查看信箱里的信息。

如果有信号，进程会执行对应该信号的操作(signal action, 也叫做信号处理signal disposition)，此时叫做执行(deliver)信号。从信号的生成到信号的传递的时间，信号处于等待(pending)状态(纸条还没有被查看)。我们同样可以设计程序，让其生成的进程阻塞(block)某些信号，也就是让这些信号始终处于等待的状态，直到进程取消阻塞(unblock)或者无视信号。

`kill -l` 命令可以看到比较全的信号，数字和信号名字是等量的，比如我们常用的kill -9 = kill -KIGKILL



### 几个常用信号

SIGINT   CTRL+C从shell中发出信号，信号被传递给shell前台运行的进程，默认操作中断 (INTERRUPT) 该进程。

SIGQUIT  CTRL+\从shell中发出信号，信号被传递给shell中前台运行的进程，对应该信号的默认操作是退出 (QUIT) 该进程。

SIGTSTP  CTRL+Z从shell中发出信号，信号被传递给shell中前台运行的进程，对应该信号的默认操作是暂停 (STOP) 该进程。

SIGCONT  用于通知暂停的进程继续。

SIGALRM  起到定时器的作用，通常是程序在一定的时间之后才生成该信号。

 eg:

```sh
[root@localhost]# ping localhost
PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.040 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.029 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.026 ms
^Z
[1]+  Stopped                 ping localhost
[root@localhost]# ps aux | grep ping
root     20487  0.0  0.0 105428  2084 pts/6    T    14:16   0:00 ping localhost
root     20489  0.0  0.0 103384  2076 pts/6    S+   14:16   0:00 grep ping
[root@localhost]# kill -SIGCONT 20487
64 bytes from localhost (127.0.0.1): icmp_seq=4 ttl=64 time=0.038 ms
[root@localhost]# 64 bytes from localhost (127.0.0.1): icmp_seq=5 ttl=64 time=0.019 ms
64 bytes from localhost (127.0.0.1): icmp_seq=6 ttl=64 time=0.025 ms
64 bytes from localhost (127.0.0.1): icmp_seq=7 ttl=64 time=0.025 ms
64 bytes from localhost (127.0.0.1): icmp_seq=8 ttl=64 time=0.025 ms
^C
[root@localhost wangyu]# 64 bytes from localhost (127.0.0.1): icmp_seq=9 ttl=64 time=0.027 ms
64 bytes from localhost (127.0.0.1): icmp_seq=10 ttl=64 time=0.025 ms

```

这个时候进程已经不再前台了 需要杀掉才能不让其输出。



### signal

Python 所用信号名和Linux一致，可以通过：

```python
import signal
dir(signale)
```

来查询。

#### signal.signal

这个包的核心是使用singnal.signal()函数来预设(register)信号处理函数：

`signal.signal(signalnum, handler)`

signalnum为某个信号，handler为该信号的处理函数。

进程可以无视信号，可以采取默认操作，还可以自定义操作。

当handler为signal.SIG_IGN时，信号被无视(ignore)。

当handler为singal.SIG_DFL，进程采取默认操作(default)。

当handler为一个函数名时，进程采取函数中定义的操作。

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



#### 传递参数

触发信号量handle函数的时候顺便传递参数：

```python
from functools import partial
def signal_handler(which, signum, frame):
    print which, 'come here'
signal.signal(signal.SIGINT, partial(signal_handler, 'I'))
```





#### signal.alarm

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

signal.SIGALRM,  是一个特殊信号类型，它可以让程序要求系统经过一段时间对自己发送通知。

os 标准模块中指出，它可用于避免无限制阻塞 I/O 操作或其它系统调用。

像下面例子，原本程序睡眠 10 后才打印出　print 'After :', time.ctime()，但是由于 signal.alarm(2)，所以 2 秒后就执行了打印。

```python
import signal
import time
 
def receive_alarm(signum, stack):
    print 'Alarm :', time.ctime()
 
# Call receive_alarm in 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)
    
print 'Before:', time.ctime()
time.sleep(10)
print 'After :', time.ctime()

out:
Before: Fri May 10 14:31:40 2019
Alarm : Fri May 10 14:31:42 2019
After : Fri May 10 14:31:42 2019

```

**注意， After两秒后也进行了 打印。**

标注：

```
alarm()函数的主要功能是设置信号传送闹钟，即用来设置信号SIGALRM在经过参数seconds秒数后发送给目前的进程。如果未设置信号SIGALARM的处理函数，那么alarm()默认处理终止进程。

如果在seconds秒内再次调用了alarm函数设置了新的闹钟，则后面定时器的设置将覆盖前面的设置，即之前设置的秒数被新的闹钟时间取代；当参数seconds为0时，之前设置的定时器闹钟将被取消。
```

可以用signal.alarm(0)来取消掉前面的闹钟



#### 规定时间内执行函数

是对上方alarm功能的一个实用的例子，如果规定时间内执行某函数没有返回，则做处理：

基础版：

```python
import time
import signal
from functools import partial
class SvectorTimeout(Exception):
    def __init__(self, *arg):
        self.args = arg

def signal_handler(md5, signum, frame):
    print md5
    raise SvectorTimeout("Timed out!")

def long_function_call():
    time.sleep(5)
    print 'long run finish'

signal.signal(signal.SIGALRM, partial(signal_handler, 'ddddd'))
signal.alarm(4)   # Ten seconds
try:
    #signal.alarm(0)  # 取消闹钟
    long_function_call()
except SvectorTimeout, msg:
    print "Timed out!"
```

with版：

```python
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def long_function_call():
    import time
    time.sleep(5)

try:
    with time_limit(4):
        long_function_call()
except TimeoutException as e:
    print("Timed out!")
```





#### 发信号

signal包的核心是设置信号处理函数。除了signal.alarm()向自身发送信号之外，并没有其他发送信号的功能。

但在os包中，有类似于linux的kill命令的函数，分别为

os.kill(pid, sid)

os.killpg(pgid, sid)

```python
import os  
import signal  
#发送信号， 
os.kill(16175,signal.SIGTERM)  
#发送信号  
os.kill(16175,signal.SIGUSR1)
```

