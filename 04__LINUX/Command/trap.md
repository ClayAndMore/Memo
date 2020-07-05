---
title: "linux trap 信号的接收和忽略"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---
### 场景

在一次docker 容器环境退出操作时，因为entrypoint的执行脚本的最后命令是一条 类似于sleep的持续执行命令，容器退出前想要执行一些环境清理工作，而不是直接docker stop container就把entrypoint的命令直接干掉。

但是docker 容器退出时又没有类似的hook命令，只有信号机制可以通信到容器内部：

* docker stop id  

  先向容器中PID为1的进程发送系统信号SIGTERM，等待容器中的应用程序终止执行，如果等待时间达到设定的超时时间，或者默认的10秒，会继续发送SIGKILL的系统信号强行kill掉进程。 可以指定超时时间 stop -t=20

* docker kill  id

  有任何的超时时间设置，它会直接发送SIGKILL信号，以及用户通过signal参数指定的其他信号。

  `docker kill –signal=SIGINT container_name`

  这样看，最优雅的方式当然是docker stop



### trap

linux 自带命令，可以设置信号的接收和忽略。



#### 常见信号

说明如下：

```
Signal     Value     Comment
─────────────────────────────
SIGHUP        1      终止进程，特别是终端退出时，此终端内的进程都将被终止
SIGINT        2      中断进程，几乎等同于sigterm，会尽可能的释放执行clean-up，释放资源，保存状态等(CTRL+C)
SIGQUIT       3      从键盘发出杀死(终止)进程的信号
 
SIGKILL       9      强制杀死进程，该信号不可被捕捉和忽略，进程收到该信号后不会执行任何clean-up行为，所以资源不会释放，状态不会保存
SIGTERM      15      杀死(终止)进程，几乎等同于sigint信号，会尽可能的释放执行clean-up，释放资源，保存状态等
 
SIGSTOP      19      该信号是不可被捕捉和忽略的进程停止信息，收到信号后会进入stopped状态
SIGTSTP      20      该信号是可被忽略的进程停止信号(CTRL+Z)
```

一般使用的方式：

```
kill -1 PID
kill -HUP PID
kill -SIGHUP PID
```



对于trap来说，KILL和STOP这两个信号无法被捕捉。在设置信号陷阱时，只会考虑HUP、INT、QUIT、TERM这4个会终止、中断进程的信号。



#### 语法格式

trap的语法格式为：

```
1.   trap [-lp]
2.   trap cmd-body signal_list
3.   trap '' signal_list
4.   trap    signal_list
5.   trap -  signale_list
 
语法说明：
语法1：-l选项用于列出当前系统支持的信号列表，和"kill -l"一样的作用。
       -p选项用于列出当前shell环境下已经布置好的陷阱。
语法2：当捕捉到给定的信号列表中的某个信号时，就执行此处给定cmd-body中的命令。
语法3：命令参数为空字符串，这时shell进程和shell进程内的子进程都会忽略信号列表中的信号。
语法4：省略命令参数，重置陷阱为启动shell时的陷阱。不建议此语法，当给定多个信号时结果会出人意料。
语法5：等价于语法4。
trap不接任何参数和选项时，默认为"-p"
```



#### eg

```sh
mytrp(){
    echo "Quit"
    exit 1
}
trap 'mytrp' SIGTERM

for i in {1..254};do
ping -w 1 -c 1 172.16.254.$i
done
```

通过kill pid来发送sigterm.

对于守护态的进程，或者是一直在shell中执行的子程序，我们可以改成一次运行后，一直loop来等待信号，这对容器的启动脚本非常好用

```sh
#!/usr/bin/env bash
mytrp(){
    echo "Quit"
    /ng8w/bin/xxxd.py -d stop   
    exit 1
}
trap 'mytrp' SIGTERM

main(){
    #/xxx/bin/xxxd.py start
    service xxx start
    
    echo "xxx started!"
    
    # 每5s检测信号
    while true
    do
        sleep 5
    done
}
```



一个用于docker 启动测试的脚本：test.sh

```sh
#!/usr/bin/env bash

mytrp(){
    echo "Quit" > /home/test/log
    exit 1
}

my_handler(){
   echo "1111"> $l/home/test/log1
}
trap 'mytrp' SIGTERM
trap 'my_handler'  SIGUSR1

while true
do
    sleep 3
done
```

启动容器：`docker run -it -v `pwd`:/home/test centos:6.7 /home/test/test.sh`

发SIGUSR1信号：

docker kill --signal=SIGUSR1 fa6169397636

发送SIGTERM：

docker stop -t=20 fa6169397636



### 注意

**(1).陷阱的守护对象是shell进程本身，不会守护shell环境内的子进程。但如果是信号忽略型陷阱，则会守护整个shell进程组使其忽略给定信号。**

**(2).如果shell中针对某信号设置了陷阱，则该shell进程接收到该信号时，会等待其内正在运行的命令结束才开始处理陷阱。**

**(3).CTRL+C和SIGINT不是等价的。当某一时刻按下CTRL+C，它是在向整个当前运行的进程组发送SIGINT信号。对shell脚本来说，SIGINT不仅发送给shell脚本进程，还发送给脚本中当前正在运行的进程。**



参考：https://www.linuxidc.com/Linux/2017-08/146607.htm