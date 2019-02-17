
Tags:[flask,python]  date: 2017-02-01

### vagrant 和 docker

Vagrant就是你的开发环境的部署工具；而docker是你的运行环境部署工具。

Vagrant并不提供虚拟化技术，本质上是一个虚拟机外挂，通过虚拟机的管理接口来管理虚拟机，让用户更轻松的进行一些常用配置。说白了vagrant就是一个普普通通的装了一个Linux的VirtualBox虚拟机，配以vagrant 团队为之开发的一系列套件，辅助完成诸如安装初始化、文件同步、ssh、部署环境升级、功能插件安装等等一些列问题的开发环境部署套件

docker是一个容器引擎，每一个实例是一个**相对隔离**的空间，**与宿主机共享操作系统内核**，并且共享宿主机资源。相对于披着虚拟机皮的vagrant，docker更加轻量，消耗更少的资源。



### wsgi和werkzeug

CGI:(Common Gateway Interface) 公用网关接口，是WWW技术中最重要的技术之一，有着不可替代的重要地位.

WSGI是Web Server Gateway Interface的缩写。以层的角度来看，WSGI所在层的位置低于CGI。但与CGI不同的是WSGI具有很强的伸缩性且能运行于多线程或多进程的环境下，这是因为WSGI只是一份标准并没有定义如何去实现。

Werkzeug是Python的[WSGI](http://baike.baidu.com/view/1660037.htm)规范的实用函数库。使用广泛，基于[BSD协议](http://baike.baidu.com/view/1178915.htm).。



### openid和OAuth 

前者是网站对用户进行认证，让网站知道“你是你所声称的URL的属主”
后者其实并不包括认证，只不过“只有认证成功的人才能进行授权”，结果类似于“认证+授权”了。OAuth相当于：A网站给B网站一个令牌，然后告诉B网站说根据这个令牌你可以获取到某用户在A网站上允许你访问的所有信息作者



### PyPI

Python Package Index，所有的pip安装的包都来自PyPI。



### 钩子

个具体化的说法叫回调函数。linux内核中就有很多这样的机制，底层用c语言的函数指针来调用函数，顶层将该指针指向某个函数，以此来达到解耦代码的目的

 

windows中：

钩子实际上是一个处理消息的程序段，通过系统调用，把它挂入系统。每当特定的消息发出，在没有到达目的窗口前，钩子程序就先捕获该消息，亦即钩子函数先得到控制权。这时钩子函数即可以加工处理（改变）该消息，也可以不作处理而继续传递该消息，还可以强制结束消息的传递。



###  一些docker命令

#### 下载镜像

`docker pull test/web_develop:dev`

它会先看主机上是否有，如果没有会从**镜像仓库Dockers Hub**下载这个镜像。

#### 查看镜像列表

`docker images`

#### 启动容器

```
 sudo docker run -i -t ubuntu /bin/bash
```

`-t` 选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上， `-i` 则让容器的标准输入保持打开。

我们告诉 Docker 基于什么镜像来创建容器，实例中使用的是 ubuntu 镜像。

随后， Docker 在文件系统内部用这个镜像创建了一个容器，该容器有着自己的网络、IP地址以及和宿主主机用来通信的桥接网络接口。

最后，在新创建的容器中运行 /bin/bash 命令启动了一个 Bash shell.

这样，容器创建完毕后，我们就可以看到容器中启动了shell .

在看个例子：

`docker run --name web_dev -it -p 9000:9000 dongweiming/web_develop/bin/zsh`

--name 指定了容器的名字为web_dev ,it 应该是上文中的 -i -t ，-p制定端口， /bin/zsh是登陆容器的默认shell。

#### 退出容器

ctrl+d 或 exit

#### 重新进入一个存在的容器

*  查看容器列表

` docker ps -a`

* 进入容器

`docker start xxx`xxx可以为容器名字 或者容器的id\

`docekr attach yyy`yyy为容器名字或者id 要按两下回车进入容器

