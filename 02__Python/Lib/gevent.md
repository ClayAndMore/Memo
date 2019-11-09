进程和协程的不同点：

1. 执行流的调度者不同, 进程是内核调度, 而协程是在用户态调度, 也就是说进程 的上下文是在内核态保存恢复的,而协程是在用户态保存恢复的. 很显然用户态的 代价更低
2. 进程会被抢占,而协程不会,也就是说协程如果不主动让出CPU,那么其他的协程是不 可能得到执行机会,这实际和早期的操作系统类似,比如DOS, 它有一个yield原语, 一个进程调用yield,那么它就会让出CPU, 其他的进程也就有机会执行了, 如果一 个进程进入了死循环,那么整个系统也就挂起了,永远无法运行其他的进程了, 但 对协程而言,这不是问题
3. 对内存的占用不同,实际上协程可以只需要4K的栈就够了, 而进程占用的内存要大 的多.
4. 从操作系统的角度讲, 多协程的程序是单线程,单进程的



## Gevent

 https://blog.csdn.net/freeking101/article/details/53097420 

 https://cloud.tencent.com/developer/article/1175613 

 https://www.xncoding.com/2016/01/02/python/gevent.html 



使用 Python 进行并行编程，不推荐gevent.

1. Monkey-patching。中文「猴子补丁」，常用于对测试环境做一些hack。我个人不太喜欢这种「黑魔法」，因为如果其他人不了解细节，极为容易产生困惑。Gvanrossum说用它就是"patch-and-pray"，太形象了。由于Gevent直接修改标准库里面大部分的阻塞式系统调用，包括socket、ssl、threading和 select等模块，而变为协作式运行。但是我们无法保证你在复杂的生产环境中有哪些地方使用这些标准库会由于打了补丁而出现奇怪的问题，那么你只能祈祷（pray）了。其次，在Python之禅中明确说过：「Explicit is better than implicit.」，猴子补丁明显的背离了这个原则。最后，Gvanrossum说Stackless之父Christian Tismer也赞同他。 我喜欢显式的「yield from」
2. 第三方库支持。得确保项目中用到其他用到的网络库也必须使用纯Python或者明确说明支持Gevent，而且就算有这样的第三方库，我还会担心这个第三方库的代码质量和功能性。
3. Greenlet不支持Jython和IronPython，这样就无法把gevent设计成一个标准库了。

之前是没有选择，很多人选择了Gevent，而现在明确的有了更正统的、正确的选择：asyncio



