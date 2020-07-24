## /proc

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



### satat

``` sh
root@TinaLinux:/proc/3782# cat stat
3782 (bvrobot) S 114 3782 114 64512 4072 1077936384 8727 14959 0 0 37 524 0 1 20 0 11 0 71083 45535232 8490 4294967295 65536 1285064 3201052128 3201049428 3069071928 0 0 4096 67137026 4294967295 0 0 17 2 0 0 0 0 0 1353712 1360302 4616192
```

解释：

| 参数             |     数值     | 解释                                                         |
| ---------------- | :----------: | :----------------------------------------------------------- |
| pid              |     3782     | 进程(包括轻量级进程，即线程)号                               |
| comm             |   bvrobot    | 应用程序或命令的名字                                         |
| task_state       |      S       | 任务的状态: R:runnign, S:sleeping (TASK_INTERRUPTIBLE), T: stopped, Z:zombie, D:dead |
| ppid             |     114      | 父进程ID                                                     |
| pgid             |     3782     | 进程组号                                                     |
| sid              |     114      | 该任务所在的会话组ID                                         |
| tty_nr           | 64512(pts/6) | 该任务的tty终端的设备号                                      |
| tty_pgrp         |     4072     | 终端的进程组号，当前运行在该任务所在终端的前台任务(包括shell 应用程序)的PID。 |
| task->flags      |  1077936384  | 进程标志位，查看该任务的特性                                 |
| min_flt          |     8727     | 该任务不需要从硬盘拷数据而发生的缺页（次缺页）的次数         |
| cmin_flt         |    14959     | 累计的该任务的所有的waited-for进程曾经发生的次缺页的次数目   |
| maj_flt          |      0       | 该任务需要从硬盘拷数据而发生的缺页（主缺页）的次数           |
| cmaj_flt         |      0       | 累计的该任务的所有的waited-for进程曾经发生的主缺页的次数目   |
| utime            |      37      | 该任务在用户态运行的时间，单位为jiffies                      |
| stime            |     524      | 该任务在核心态运行的时间，单位为jiffies                      |
| cutime           |      0       | 累计的该任务的所有的waited-for进程曾经在用户态运行的时间，单位为jiffies |
| cstime           |      1       | 累计的该任务的所有的waited-for进程曾经在核心态运行的时间，单位为jiffies |
| priority         |      20      | 任务的动态优先级                                             |
| nice             |      0       | 任务的静态优先级                                             |
| num_threads      |      11      | 该任务所在的线程组里线程的个数                               |
| it_real_value    |      0       | 由于计时间隔导致的下一个 SIGALRM 发送进程的时延，以 jiffy 为单位. |
| start_time       |    71038     | 该任务启动的时间，单位为jiffies                              |
| vsize            |   45535232   | 该任务的虚拟地址空间大小                                     |
| rss              |     8490     | 该任务当前驻留物理地址空间的大小；。                         |
| rlim             |  4294967295  | 该任务能驻留物理地址空间的最大值                             |
| start_code       |    65536     | 该任务在虚拟地址空间的代码段的起始地址                       |
| end_code         |   1285064    | 该任务在虚拟地址空间的代码段的结束地址                       |
| start_stack      |  3201052128  | 该任务在虚拟地址空间的栈的结束地址                           |
| kstkesp          |  3201049428  | esp(32 位堆栈指针) 的当前值, 与在进程的内核堆栈页得到的一致. |
| kstkeip          |  3069071928  | 指向将要执行的指令的指针, EIP(32 位指令指针)的当前值.        |
| pendingsig       |      0       | 待处理信号的位图，记录发送给进程的普通信号                   |
| block_sig        |      0       | 阻塞信号的位图                                               |
| sigign           |     4096     | 忽略的信号的位图                                             |
| sigcatch         |   67137026   | 被俘获的信号的位图                                           |
| wchan            |  4294967295  | 如果该进程是睡眠状态，该值给出调度的调用点                   |
| nswap            |      0       | 被swapped的页数，当前没用                                    |
| cnswap           |      0       | 所有子进程被swapped的页数的和，当前没用                      |
| exit_signal      |      17      | 该进程结束时，向父进程所发送的信号                           |
| task_cpu(task)   |      2       | 运行在哪个CPU上                                              |
| task_rt_priority |      0       | 实时进程的相对优先级别                                       |
| task_policy      |      0       | 进程的调度策略，0:非实时进程，1:FIFO实时进程；2:RR实时进程   |
| blio_ticks       |      0       | 等待阻塞IO的时间                                             |
| gtime            |   1353712    | guest time of the task in jiffies                            |
| cgtime           |   1360302    | guest time of the task children in jiffies                   |
| start_data       |   4616192    | address above which program data+bss is placed               |
| end_data         |              | address below which program data+bss is placed               |
| start_brk        |              | address above which program heap can be expanded with br     |