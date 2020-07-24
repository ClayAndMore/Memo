---
title: "supervisor.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "supervisor.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## Supervisor

一个管理进程的工具，有一个进程需要每时每刻不断的跑，但是这个进程又有可能由于各种原因有可能中断。当进程中断的时候，希望能自动重新启动它。此时，我就需要使用到了Supervisor。

supervisor管理进程，**是通过fork/exec的方式将这些被管理的进程当作supervisor的子进程来启动**，所以我们只需要将要管理进程的可执行文件的路径添加到supervisor的配置文件中就好了。此时被管理进程被视为supervisor的子进程，若该子进程异常中断，则父进程可以准确的获取子进程异常中断的信息，通过在配置文件中设置autostart=ture，可以实现对异常中断的子进程的自动重启。



### 安装

``` sh
apt-get install supervisor 
pip install supervisor 
```

进到工程目录，在项目目录添加supervisor的配置文件，安装完supervisor后，输入以`echo_supervisord_conf`命令可得到配置文件：

`echo_supervisord_conf > supervisord.conf`



### 配置文件

默认的配置文件： `cat /etc/supervisord/supervisord.conf`

``` sh
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket
;username=chris              ; should be same as http_username if set
;password=123                ; should be same as http_password if set

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
;chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))

[inet_http_server]         ; inet (TCP) server disabled by default
port=127.0.0.1:9002        ; (ip_address:port specifier, *:port for all iface)
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))
```

* 分号表示注释

* [unix_http_server]：这部分设置HTTP服务器监听的UNIX domain socket
- file: 指向UNIX domain socket，即file=/var/run/supervisor.sock
  - chmod：启动时改变supervisor.sock的权限
  
* [supervisord]：与supervisord有关的全局配置需要在这部分设置

  - logfile: 指向记录supervisord进程的log文件
  - pidfile：pidfile保存子进程的路径
  - childlogdir：子进程log目录设为AUTO的log目录

* [supervisorctl]：

  - serverurl：进入supervisord的URL， 对于UNIX domain sockets, 应设为 unix:///absolute/path/to/file.sock
  - username: 如果设置了需要登录才能进

* [include]：如果配置文件包含该部分，则该部分必须包含一个files键：

  - files：包含一个或多个文件，这里包含了/etc/supervisor/conf.d/目录下所有的.conf文件，可以在该目录下增加我们自己的配置文件，在该配置文件中增加[program:x]部分，用来运行我们自己的程序，如下：

* [program:x]：配置文件必须包括至少一个program，x是program名称，必须写上，不能为空
  - command：包含一个命令，当这个program启动时执行
  - directory：执行子进程时supervisord暂时切换到该目录
  - user：账户名
  - startsecs：进程从STARING状态转换到RUNNING状态program所需要保持运行的时间（单位：秒）
  - redirect_stderr：如果是true，则进程的stderr输出被发送回其stdout文件描述符上的supervisord
  - stdout_logfile：**将进程stdout输出到指定文件**, 可以做日志。
  - stdout_logfile_maxbytes：stdout_logfile指定日志文件最大字节数，默认为50MB，可以加KB、MB或GB等单位
  - stdout_logfile_backups：要保存的stdout_logfile备份的数量
* [inet_http_server], 同时可以开启supervisor的web管理页面



eg：

```
[program:myapp]  
directory = /home/flask
command = 虚拟环境目录/gunicorn -w4 -b 0.0.0.0:8000 run:app
```

关于虚拟环境目录，因为我是用python2下载的supervisor,但是我运行的项目在python3，所以这里运行要加上自己环境的虚拟目录。

如我的两个项目：

```
[program:myapp]
directory =/home/myflaskproject/flaskproject
command =/home/myflaskproject/flaskVenv/bin/gunicorn -w4 -b 127.0.0.1:8001 run:app

[program:kesheApp]
directory =/root/bisheFlask/webapp
command =/root/bisheFlask/bisheFlaskVEnv/bin/gunicorn -w4 -b127.0.0.1:8002 __init__:app
```





### 命令

```sh
supervisord -c supervisor.conf                             # 通过配置文件启动supervisor,注意它和其他命令不一样

supervisorctl (-c supervisor.conf) status                  #  察看supervisor的状态
supervisorctl (-c supervisor.conf) reload                  #  重新载入 配置文件
supervisorctl (-c supervisor.conf) start [all]|[appname]   #  启动指定/所有 supervisor管理的程序进程
supervisorctl (-c supervisor.conf) stop [all]|[appname]    #  关闭指定/所有 supervisor管理的程序进程
supervisorctl shutdown 		# 关掉其服务进程 
```

括号内的命令可不写



### 使用系统的环境变量





### 出现的问题

* `unix:///tmp/supervisor.sock no such file`

  是清理了tmp文件所致的，我们在执行一遍`supervisord -c supervisor.conf  `就可以了。

  `/tmp/supervisord.log`是我们的supervisor 监控的日志，有问题可以去看下。

* 日志里看到`CRIT Server 'unix_http_server' running without any HTTP authentication check`

  ，也是这个的错误：`Exited too quickly`  

  这个问题删掉配置文件中supervisor.conf中`directory =/root/bisheFlask/webapp`这行。

* 还是有Exited too quickly或其他错的时候，我们可以单独运行配置文件中的command来验证命令是否错误。

