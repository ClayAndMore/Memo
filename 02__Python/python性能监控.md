Tags: [python, 监控]

## 性能监控

随着功能的增多， 代码越来越多， 我们需要找出代码慢的坑位。



### 时间装饰器

最原始的方式了， 用自带的time模块来输出所耗时；

由于公司所用代码在一个while True循环里， 不太好记录，所以我给它发入一个字典里， 每个被装饰的函数是key, value是其所消耗的时间数组， 当其消耗时间大于最大时才加入该数组，这样也是有缺陷的，不是实时的，可以修改。

```python
import collections
# 时间统计
from functools import wraps

class Timer:
    def __init__(self):
        self.time_start_lock = False # 
        self.all_time_dict = collections.defaultdict(lambda: [0]) # 默认值为一

	# 记录时间块， 不方便装饰器的需要手动，
    def print_time(self, delt, modle_name): 
        '''
        	delt, 时间段
        	modle_name 函数名
        '''
        if self.time_start_lock:
            if delt > max(self.all_time_dict[modle_name]):
                self.all_time_dict[modle_name].append(delt)
            print>> sys.stdout, modle_name, ' with %s seconds'%str(delt)

    def fn_timer(self, function):    # 装饰器
        @wraps(function)
        def function_timer(*args, **kwargs):
            if not self.time_start_lock:
                return function(*args, **kwargs)
            t0 = time()
            result = function(*args, **kwargs)
            t1 = time()
            delta_time = t1-t0
            if delta_time > max(self.all_time_dict[function.func_name]):
                self.all_time_dict[function.func_name].append(delta_time)
            return result
        return function_timer
    
  
timer = Timer() #全局唯一
```








### Profile / cProfile + pastas

usga:

```
import cProfile
cProfile.run('foo()')

python -m cProfile myscript.py
```

需要pastats格式化输出日志文件，具体使用的过程中感觉使用还输出都不友好。



### line_profiler

`https://github.com/rkern/line_profiler`

特点是代码行具体输出所用时间，输出很友好，它也是通过装饰器的，会在整个python变量中生成一个全局装饰器变量。也是由于这点，尝试后放弃。





### gprof2dot

centos isntall :

```
yum install 'graphviz*'
yum install python_graphviz

```



生成一张图片， 显示了调用关系，具体我用的时候，，输出信息太少

`./bin/python2.7 ./bin/gprof2dot.py -f pstats output.log | dot -Tpng -o output.png`





### vprof

`https://github.com/nvdv/vprof`

这是我最喜欢的一个库了，输出很美好， 支持web直接浏览。

分四个维度:

* CPU flame graph
* profiler
* memory graph
*  code heatmap



`./bin/vprof -c cpmh mongo2csv.py -H 0.0.0.0 -p 8000`

起一个监控服务器

./vprof -r -H 0.0.0.0



支持脚本调用和程序内嵌。

因为每增加一个维度都要再跑一遍这个函数或脚本，四个维度跑四遍。。

 所以对于循环的程序不太适合。



### pprofile

`https://github.com/vpelletier/pprofile`

pprofile 是 line_profile的相似品， 我使用它的原因是无需像line_profile 生成内部装饰器，并且可以方便的生成日志信息：
如：`pprofile --format callgrind --out cachegrind.out.threads demo/threads.py`

输出的cachegrind.out.threads 可以作为Kcachegrind和qcachegrind 的输入。



最终方案选择了pprofile,  命令行执行一直循环的程序，内部有信号量来break掉。

拿到日志到qcachegrind上来分析。

### Kcachegrind

运行在linux的gui 分析输出日志软件

Incl表示inclusive，包含其调用的函数的消耗cost。

Self表示exclusive，具有排他性，只表示自身的消耗cost。



[Kcachegrind 介绍](http://pytlab.org/2016/12/20/Python%E4%BC%98%E5%8C%96%E7%AC%AC%E4%B8%80%E6%AD%A5-%E6%80%A7%E8%83%BD%E5%88%86%E6%9E%90%E5%AE%9E%E8%B7%B5/)



### qcachegrind 

是Kcachegrind 的window 版， 很好用 ， 将源代码指定在某一路径，就可以看每行的运行时间。





## 系统监控

### glances

https://github.com/nicolargo/glances

https://www.tecmint.com/glances-monitor-remote-linux-in-web-server-mode/