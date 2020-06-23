
---
title: "flask+gunicorn+supervisorn+nginx项目部署.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "flask+gunicorn+supervisorn+nginx项目部署.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Flask"]
categories: ["python web"]
author: "Claymore"

---
Tags:[flask,python] date: 2017-03-19

在腾讯云上申请了一个服务器，这里记录一下初次部署flask项目的经历：

centOS7+python3.5，本地开发可用fabric部署，有时间再补录。

### 虚拟环境

* 安装

  `pip install virtualenv`

* 当前目录创建名为myenv的虚拟环境

  `virtualenv myenv`

* 进入虚拟环境：

  `source myenv/bin/activate`

* 退出

  `deactivate`


### 创建项目

run.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/') 
def index():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run()
```

我们用gunicorn来启动它：


### gunicorn

gunicorn是一个python Wsgi http server，只支持在Unix系统上运行，来源于Ruby的unicorn项目。g.unicorn(读音)

wsgi: web server gateway interface.是python语言定义的web服务器和web应用程序或框架之间的一种简单而通用的接口

，是基于现存的CGI标准设计的。

很多框架自带了WSGI server.比如Flask,Djanggo,等。当然性能都不好，多用于测试。



#### gunicorn的设计 

基于‘pre-fork worker'模型，意味着有一个中心主控master进程，用它来管理一组worker进程。

worker进程可以支持不同的IO方式（sync,gevent,eventlet,tornado等）

#### gunicorn+Nginx

gunicorn可以单独提供服务，但是会占用很多静态资源，它应该更关注业务请求和处理，所以用Nginx作为前端服务器处理一切静态文件请求，把动态请求给gunicorn后端服务器，让 nginx 作均衡负载转发请求给多个 gunicorn 进程从而提升服务器处理效率与处理能力。最后，nginx 还可以配置很多安全相关、认证相关等很多处理，可以让你的网站更专注业务的编写，把一些转发规则等其它业务无关的事情交给 nginx 做。

#### uWSGI

uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。

- WSGI看前面很清楚了，是一种通信协议。
- uwsgi同WSGI一样是一种通信协议。
- 而uWSGI是实现了uwsgi和WSGI两种协议的Web服务器。

uwsgi协议是一个uWSGI服务器自有的协议，它用于定义传输信息的类型（type of information），每一个uwsgi packet前4byte为传输信息类型描述，它与WSGI相比是两样东西。



为什么有了uWSGI为什么还需要nginx？

因为nginx具备优秀的静态内容处理能力，然后将动态内容转发给uWSGI服务器，这样可以达到很好的客户端响应。

#### 安装

` pip install gunicorn`

#### 启动

前面介绍了那么多是为了更好的理解，我们看一下怎么启动，先进入到有run.py即你要运行的那个目录里：

`gunicorn -D -w 3 -b 127.0.0.1:8000 run:app`

- D 表示后台运行 
- w 表示有3 个 工作线程（感觉有些类似 nginx 的 master-worker 模型） 
- b 指定ip 和端口 
- 这里采用本机访问， 主要是为了使用nginx 进行代理， 方便管理 ，可以用0.0.0.0来让其他主机访问，但是记得要看后面的防火墙端口，记得开启这里的8000
- run表存放 写着全局变量 app 的那个工程文件，可以是manage
- 在我们的这个工程中， 即包含 **init**.py 的那个文件 



### supervisor

一个管理进程的工具，有一个进程需要每时每刻不断的跑，但是这个进程又有可能由于各种原因有可能中断。当进程中断的时候，希望能自动重新启动它。此时，我就需要使用到了Supervisor。

安装：

`pip install supervisor`

进到工程目录，在项目目录添加supervisor的配置文件，

`echo_supervisord_conf > supervisord.conf`

会生成一个配置文件

`vi supervisord.conf`

添加信息：

```
[program:myapp]  
directory = /home/flask
command = 虚拟环境目录/gunicorn -w4 -b 0.0.0.0:8000 run:app
```

myapp 自己起的项目名

directory运行项目所在的工程文件

command ,gunicorn 的启动命令

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



同时可以开启supervisor的web管理页面:

```
[inet_http_server]
port = 0.0.0.0:8002
username=user              ; (default is no username (open server))
password=123               ; (default is no password (open server))
```



#### 命令

```
supervisord -c supervisor.conf                             通过配置文件启动supervisor,注意它和其他命令不一样

supervisorctl (-c supervisor.conf) status                    察看supervisor的状态
supervisorctl (-c supervisor.conf) reload                    重新载入 配置文件
supervisorctl (-c supervisor.conf) start [all]|[appname]     启动指定/所有 supervisor管理的程序进程
supervisorctl (-c supervisor.conf) stop [all]|[appname]      关闭指定/所有 supervisor管理的程序进程
supervisorctl shutdown 		关掉其服务进程 
```

括号内的命令可不写

#### 配置开机就启动我们的项目

`vi /etc/rc.d/rc.local`  # 可能也没有rc.d

在最后添加

`supervisord -c /home/flask/supervisord.conf`

注意上述自启动方法在ubuntu16.04后不可用



16.04以后的做法：



#### 出现的问题

* `unix:///tmp/supervisor.sock no such file`

  是清理了tmp文件所致的，我们在执行一遍`supervisord -c supervisor.conf  `就可以了。

  `/tmp/supervisord.log`是我们的supervisor 监控的日志，有问题可以去看下。

* 日志里看到`CRIT Server 'unix_http_server' running without any HTTP authentication check`

  ，也是这个的错误：`Exited too quickly`  

  这个问题删掉配置文件中supervisor.conf中`directory =/root/bisheFlask/webapp`这行。

* 还是有Exited too quickly或其他错的时候，我们可以单独运行配置文件中的command来验证命令是否错误。





### 开启防火墙端口

**CentOS 7.0默认使用的是firewall作为防火墙，使用iptables必须重新设置一下**

`systemctl stop firewalld.service `          #停止firewall

`systemctl disable firewalld.service  `   #禁止firewall开机启动

**设置 iptables service**(两种方法）:

1. `yum -y install iptables-services`

   如果要修改防火墙配置，如增加防火墙端口3306，这里也可以看开放端口状态

   `vi /etc/sysconfig/iptables `

   增加规则

   `-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT`

2. ` /sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT`   写入修改

   `service iptables save` 保存

保存退出后

`systemctl restart iptables.service `#重启防火墙使配置生效

`systemctl enable iptables.service` #设置防火墙开机启动

**最后重启系统使设置生效即可.**



### Nginx

Nginx由内核和模块组成，其中，内核的设计非常微小和简洁，完成的工作也非常简单，仅仅通过查找配置文件将客户端请求映射到一个location block（location是Nginx配置中的一个指令，用于URL匹配），而在这个location中所配置的每个指令将会启动不同的模块去完成相应的工作。

Nginx的模块从结构上分为核心模块、基础模块和第三方模块



#### 进程模型

两种工作方式：

* 单进程工作方式，主进程（master)+工作进程worker（单线程）
* 多进程工作模式，主进程（master)+工作进程worker（多线程，一个主线程）

master进程：

要用来管理worker进程，包含：接收来自外界的信号，向各worker进程发送信号，监控worker进程的运行状态，当worker进程退出后(异常情况下)，会自动重新启动新的worker进程。

master进程充当整个进程组与用户的交互接口，同时对进程进行监护。它不需要处理网络事件，不负责业务的执行，只会通过管理worker进程来实现重启服务、平滑升级、更换日志文件、配置文件实时生效等功能。

work进程：

每个进程之间都是平等的，多个worker进程之间是对等的，他们同等竞争来自客户端的请求，各进程互相之间是独立的。一个请求，只可能在一个worker进程中处理。

worker进程的个数是可以设置的，一般我们会设置与机器cpu核数一致，这里面的原因与nginx的进程模型以及事件处理模型是分不开的。



#### 多进程时间模型：异步非阻塞





#### 配置

安装:

`yum install nginx`

我的版本是：`nginx version: nginx/1.10.3`

安装完的nginx 在 `/usr/local/nginx` 目录下， 我们可以找到`conf`文件夹下的 `nginx.conf` 文件， 将其修改 :

```
server {
    listen 8001;
    server_name _;
    location /{
        proxy_pass http://127.0.0.1:8000;
    }
}
```

我们监听8001端口，将外部通过 8001 端口发送过来的请求， 代理给了 `127.0.0.1:8000` 也就是我们上面gunicorn启动的flask 项目。

配置好启动：

```
[root@server ~]# service nginx start
Starting nginx:                                            [  OK  ]
[root@server ~]# nginx -s reload
```



ps：记得浏览器是有缓存的，有可能还是你原来的那个界面，换端口的时候记得换浏览器看，或者清理缓存，这个问题耽误了我两个下午。555...



### 记得开启安全组

到网站去看自己的安全组规则，可添加规则

