

##Docker 



### 初识容器和Docker

虚拟化技术，虚拟化可以通过硬件，软件，而Docker是虚拟化操作系统

Docker 基于GO语言实现的开源容器项目，可以简单的将它理解为一个沙盒，每个沙盒里运行着一个应用，每个应用间可以通过网络通信，并且每个沙盒占用的资源十分少。

Docker 构想： 对应用的封装，分发，部署，运行。这个应用可以是一个web应用，一个编译环境，也可以是一套数据库平台服务等。 最终目的： 一次封装，到处运行。

Docker的镜像管理：借鉴于Git的设计理念。

#### 三大核心概念

* 镜像（Image)

  类似于虚拟机镜像，理解为一个只读的模板。eg: 一个镜像有基本的系统，安装了Apache应用程序，可以诚挚为一个Apache镜像。
  docker的images,我们可以理解为积木, 一层一层往上搭, 最后完成一个工程化的大项目. 
  在最初,docker实际上,只有一个静态的image(Ps: read-only). 相当于只能读, 所以, 你所有的改动并不会影响到原来的image上, 只会一层一层的叠加, 比如, 你在Ubuntu的image上面, 再接一层nodeJS的image. 实际上的结果是, 两个image叠加起来.

  通过版本管理系统来获取和更新。

* 容器（Container)

  容器是来运行和隔离应用的。可以看成一个简易版的linux系统。

* 仓库（Repository)

  镜像的仓库，目前最大的仓库：Docker Hub。

  注册服务器是存放仓库的地方，一个仓库有大量的镜像，镜像可以通过不同的Tag来区分。



### 安装

Ubuntu：

系统要求：

* 64位
* 内核版本>=3.10 查看内核版本：`uname -a`
* Ubuntu版本>=12.04 LTS   检查：`more /etc/issue`

具体步骤

1. 安装支持HTTPS的源：

   `apt-get install -y apt-transport-https`

2. 添加源的gpg密钥

   `sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`

3. 获取操作系统的代号（每个版本的系统都会有个代号，和安卓系统类似）

   `lsb_release -c`

4. 添加官方apt软件源：

   ` <<EOF > /etc/apt/sources.list.d/docker.list`:

   ```
   deb https://apt.dockerproject.org/repo ubuntu-xenial main
   EOF
   ```

通过官方脚本安装：

`curl -fsSL https://get.docker.com/ | sh`

或： `wget -qO- https://get.docker.com/ | sh`



#### 配置

默认配置文件：`/etc/default/docker` 

服务管理脚本：`/etc/init.d/docker`

​               日志： `/var/log/upstart/docker.log`



#### 命令

确保服务正常运行：`docker version`

服务停止和重起等，都和服务命令一样： `docker  start | relstart | stop`





### 三大概念的操作

#### 使用Docker镜像

Docker运行前需要本地对应的镜像，如果没有会尝试从默认仓库下载（Docker Hub），
docker 在下载image的时候,会在/var/lib/docker目录下创建相关的image 目录.

* 获取镜像：

  `docker pull NAME[:TAG]`    

  name为仓库名（用来区分镜像），tag是镜像的标签（往往用来表示版本信息）。

  eg:

  `docker pull ubuntu:14.04`

  如果不指定tag，会自动下载最新的。

  如果非官方hub，eg:

  `docker pull hub.c.163.com/public/ubuntu:14.04`

* 使用镜像

  利用镜像创建一个容器：

  `docker run -it ubuntu:14.04 bash` 

  如果使用非官方的hub，否则会下载另一个hub:

  `docker run -it hub.163.com/public/ubuntu:14.04 bash`

  ​

* 查看镜像

  `docker images` 

  会有个镜像ID,镜像的唯一标识，在使用的时候，可以使用该ID的前若干字符可以分串来代替完整的ID.

  相同的镜像本地只会存一份

  用tag命令添加镜像标签，这个为同一个镜像起个不同的别名而已：

  `docker tag ubuntu:lastest mybuntu:lastest`

  查看详细信息：

  `docker inspect`

* 搜寻镜像

  `docker search` 

  可以搜索远端仓库中的镜像

* 删除镜像

  `docker rmi myubuntu:lastest`

  myubuntu可以换成id,如果它的id有多个，这里只是删掉了一个Tag而已。

  当这个tag只剩下一个时，就是删掉这个id咯。

  如果镜像在被容器使用，则不会删除，正确做法是先删除容器，在删除镜像。

待补充： 创建镜像，存出和载入镜像，上传镜像。



#### 容器操作
运行的container则会放在/var/lib/docker/containers中.

* 创建容器

  `docker create` 

  创建的容器处于停止状态，要用`docker start` 

* 启动容器

  `docker run`   

  这个命令会附加很多参数，再详谈。docker run = docker create + docker start

  这个命令的操作进程：

  * 检查本地镜像，如果没有就从官网下载
  * 利用镜像创建一个容器，并启动该容器
  * 为该容器分配文件系统，再容器外面挂一层可读写层。
  * 从主机的网桥接口中配置一个虚拟接口道容器中
  * 从网桥的地址池配置一个ip给容器。
  * 执行容器中用户指定的应用程序。


* 查看本机上存在的所有容器

  `docker ps -a`

* 使用容器输出一段话：

  `docker run unbuntu:14.04 echo 'hello'`

* 使用exit（或ctrl+d)退出容器，当应用停止后，容器也停止

* 如果应用没有正常执行，那么容器也会直接退出

* 终止容器

  docker stop 来终止一个运行中的容器。

如果容器在后台挂起，我们需要进入容器：

* attach 命令 

  这个命令在多窗口同时attach同一个容器时会阻塞。

* exec 命令 

  `docker exec -it `

* nsenter 工具



删除容器

`docker rm`

rm 后可跟容器的名字或者id,用tab键可以补出要删除的东西。
不能删除正在运行的容器。

其他：

导出容器，导入容器

HAProxy 工具。



#### 访问Docker仓库

Docker hub公共市场，https://hub.docker.com  

通过` docker login` 来登陆，注册成功后，docker会将你的认证信息存放在. ~/.docker/config.json当中。
通过` docker logout` 来登出。

* docker search 

  查找官方仓库中的镜像

  可用docker pull 命令将它下载到本地。


### 使用Dockerfile创建镜像
Dockerfile 是一个文本格式的配置文件。
一般来说，这个配置文件包括四个部分：
* 基础镜像信息
* 维护者信息
* 镜像操作指令
* 容器启动时指令

#### 命令说明
以#来注释，配合自己各种指令。

一个demo:
```
# first dockerfile demo
FROM ubuntu:latest
# 设置该dockerfile的作者和联系邮箱
MAINTAINER Jimmy "xxxx@gmail.com"
# 开始配置环境, 下载apt-get,生成index.html的文件
RUN apt-get update && apt-get install -y nginx
RUN echo 'first demo' > /usr/share/nginx/html/index.html
# 暴露server的port
EXPOSE 80
```
* FROM: 指定创建镜像的基础镜像，指定第一层image, 这是必须有的. 并且指定的image是存在在你的computer中. 相当于是 docker run.没有回不去Docker Hub中下载。
* MAINTAINER: 设置作者和联系邮箱.其实就是docker commit 后面的Name参数. 而且加上了联系邮箱. 这是在dockerfile 运行完后,会自动添加到image上的.
* RUN: 在容器中做出相应的修改并提交给镜像，作为一个新的镜像： `修改+docker commite xxx` ,这样原来的镜像就又加了一层并提交作为一个新的镜像。run命令有两种形式：
  * RUN+命令： 这种形式等同于`/bin/sh -c + 命令` -c参数是说标准输入替换为字符串。这时如果命令较长可以用反斜杠来整理格式：
    ```
    RUN apt-get update \
            && apt-get install -y libsnappy-dev ziliblg-dev libbz2-dev \
            && rm -rf /var/cache/apt 
    ```
  * RUN+数组： 这种形式不会启动shell环境，用exec执行，eg:`RUN ["/bin/bash","-c","echo hell"]`
* EXPOSE: 用来给最新的container 设置与外部交流的port,现在我们可以使用-P(注意是大写). 来手动开启所有在dockerfile中,通过EXPOSE暴露的端口.

其他命令：
* CMD : 指定启动容器时的默认命令，写法和RUN一样（也是分shell环境和非shell环境）：
  ```yaml
  # 当调起container时,运行/bin/bash
  docker run  -t -i jimmy/ubuntu:latest /bin/bash
  # 等同于在dockerfile中指定CMD
  CMD ["/bin/bash"]
  // 运行docker run
  docker run -t -i jimmy/ubuntu:latest
  ```
  如果docker run时写运行命令，会覆盖掉CMD.
* ENTRYPOINT: 是说强制执行的环境,有时可以和CMD相互代替，主要功能实际上是,指定了内部运行命令的解析器. 而使用docker   run添加的命令,会被当做参数添加给ENTRYPOINT.
  ```
  # 已经指定了ENTRYPOINT ["/bin/sh"]
  # 运行docker run
  docker run -t -i jimmy/demo /bin/bash/
  # 实际上相当于(不出错才怪嘞...)
  /bin/sh /bin/bash/
  ```
  另外,我们还可以使用CMD配合ENTRYPOINT写成默认参数的效果.
  ```
  # 默认执行 /bin/bash default.sh
  ENTRYPOINT ["/bin/bash"]
  CMD ["default.sh"]
  # 如果你在docker run中指定了参数的话,则CMD会默认被代替 
  docker run jimmy/demo sam.sh
  ```
  不过,CMD和ENTRYPOINT都只能在dockerfile里面出现一次.
* WORKDIR 指定运行目录
  我们在RUN命令的时候想在不同目录下操作：
  ```
  # 在/var/data里面创建data.js
  WORKDIR /var/data
  RUN touch data.js
  # 然后在/etc 下创建data.conf文件
  WORKDIR /etc
  RUN touch data.conf
  ```
  并且当你在使用docker run时也会停留在workdir指定的目录中。
* VOLUME 指定数据卷的位置：
  ```
  # 指定/opt/data为数据卷
  VOLUME ["/opt/data"]
  # 指定多个目录为数据卷/opt/data, /opt/project
  VOLUME ["/opt/data","/opt/project"]
  ```
* COPY和ADD ，为容器添加文件
  限制：你添加的文件或者目录,只能在docker build运行的目录下, 因为,这是docker在调起container的时候,只将该目录放进了daemon。
  ```
  # 现假设,docker build运行的目录为: /data
  // 只能添加指定目录下
  // 将/data/sam.js 添加到image中的/opt/node/sam.js
  // 如果存在该文件,则不会被覆盖
  ADD sam.js /opt/node/
  # 添加文件,还可以使用通配符
  // 将所有的js文件,添加到node目录下
  ADD *.js /opt/node/
  # 如果destination不是绝对路径,则相对于最近的WORKDIR
  // 如果最近的WORKDIR为/var
  // 则下列添加的路径为/var/opt/node
  ADD *.js opt/node/
  # 使用url添加
  // 将指定路由的文件放到根目录当中
  ADD http://example.com/foobar /
  # 自动解压tar.gz文件
  // 将文件解压过后放在指定目录中
  ADD latest.tar.gz /var/www/wordpress/
  # 使用url添加
  // 将指定路由的文件放到根目录当中
  ADD http://example.com/foobar /
  # 自动解压tar.gz文件
  // 将文件解压过后放在指定目录中
  ADD latest.tar.gz /var/www/wordpress/
  ```
  COPY和ADD非常类似. 我们可以做个类比:

  ADD 包含 COPY

  COPY做的事情比不上ADD, 他比ADD少了解压缩和URL下载的功能. 不过,他耗费的性能比较少,他只做纯粹的添加和下载.他的结构和ADD一毛一样. 不过, 有一点,COPY的时候,如果遇到目录不存在的情况下,COPY会自动创建

  `COPY file.js /opt/data/`

* ARG 和ENV 命令相似，ARG只能用在docker build的阶段, 并且不会被保存在image中,这就是和ENV的区别.
  ```
  # 在dockerfile定义了默认变量
  ARG user=jimy
  # 在运行时,进行手动替换
  docker build --build-arg user=sam -t jimmy/demo   
  ```
* ONBUILD ,模板image,因为镜像的可写层数是有限制的，我们需要继承模板来在子dockerfile中使用。

#### 运行
基本格式：
`docker build -t="repository/name:tag"  directory`
该命令会创建镜像，directory 指的是内容的目录，会把该路径内容上传到服务器，在该目录中会自动搜索Dockerfile文件。
一般用.来代替该目录，一般建议放Dockerfile的目录为空目录。
如果指定不是该内容目录下的Dockerfile,用-f参数。
-t用来指定生成的image的name,比如仓库,image的名字以及他的tag,如果你不指定tag, 那么docker会自动添加latest代替。
运行后用docker images就能看到你刚才创建的镜像。

dockerfile cache
如果我们build出问题，我们生成的image会停留在那一步，当我们改掉错误后，docker是不会重来一遍的，它会从你改动行的前一步，以此继续向下构建。这个机理是docker每次运行一条命令的时候都会自动生成一个id值，所以机理就是id命中。

这里要说一下ENV参数：
它的作用是指定环境变量，但是这样我们就不能使用上面的cache了，得重来，因为一旦你改变了ENV就会改变id.
格式就是：
```
# 一个一个的赋值
ENV key value
// demo:
ENV name jimmy
ENV age 18
# 另外,还可以一起赋值
ENV key=value[...]
// demo:
ENV name=jimmy age=18
```
ENV最独特之处在于,他所设置的变量,会在你运行的时候生效.即,如果你修改了PATH,他也会在container中立即生效：
```
# 修改环境变量
ENV PATH=$PATH:/user/bin
// 现在进入到运行的container中
echo $PATH
>> /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/data
```


### Docker 容器数据管理

多个容器间共享数据。Docker有两种方式：

* 数据卷：容器内数据直接映射到本地主机环境
* 数据卷容器： 使用特定容器维护数据卷

#### 数据卷
数据卷是个目录，数据卷将主机操作系统目录直接映射进容器，有个特点：
* 多个容器间可以共享数据卷，传递数据高效方便
* 对数据卷内的数据修改会马上生效，无论是容器还是本地操作
* 数据卷解耦了数据和应用

两种方式： 
1. 容器内创建一个数据卷：
  `docker run -d -p --name web -v /webapp training/webapp python app.py`
  使用training/webapp镜像创建一个web容器，并创建一个数据卷挂载到容器的/webapp目录。
2. 系统内创建一个数据卷

#### 数据卷容器



——————

* BaaS（后端即服务，Backend as a Service），公司为移动应用开发者提供整合云后端的边界服务。

* IaaS（基础设施即服务，Infrastructure as a Service），要搭建上层数据应用，先得通过互联网获得基础性设施服务。

* PaaS（平台即服务，Platform-as-a-Service），搭建平台，集成应用产品，整合起来提供服务。

* SaaS（软件即服务，Software-as-a-Service），通过网络提供程序应用类服务。

不管是BaaS、PaaS、SaaS都要建立在IaaS基础设施服务上。其中PaaS、SaaS是IaaS在应用层的延伸，大量SaaS及应用程序服务集中在平台上，打造而成的PaaS才拥有存在的价值。BaaS是针对特定领域（移动应用）提供边界增值服务的平台类型。与SaaS、PaaS互为补充，完善了整个生态格局。 


### 端口映射与容器互联


## 实战
### 用Docker安装操作系统
