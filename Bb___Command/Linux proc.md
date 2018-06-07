Linux 下的/proc文件系统是由内核提供的，它不是一个真正的文件系统，只是一些系统运行时的信息，

只在内存中，不占用外存空间。

以文件系统的形式，为访问内核数据提供接口。

```
# ls /proc
1      2      262    32212  733        execdomains  locks         stat
10     221    27     32370  8          fb           mdstat        swaps
113    224    2799   330    8820       filesystems  meminfo       sys
12     226    27990  37     9          fs           misc          ...
```

会看到有很多数字的文件夹，这个数字代表pid, 里面内容：

```
/proc/N
/proc/N/cmdline        进程启动时的命令
/proc/N/cwd            链接到当前进程的工作目录
/proc/N/environ        进程环境变量列表
/proc/N/exe            链接到进程的执行命令文件
/proc/N/fd             进程相关的所有文件描述符
/proc/N/maps           与进程相关的内存映射信息
/proc/N/mem            代指进程持有的内存，不可读
/proc/N/root           链接到进程的根目录
/proc/N/stat           进程的状态
/proc/N/statm          进程使用的内存状态
/proc/N/status         进程状态信息，比stat更具可读性
/proc/self/            链接到当前正在运行的进程
```

