

##Docker 



### 初识容器和Docker

虚拟化技术，虚拟化可以通过硬件，软件，而Docker是虚拟化操作系统

Docker 基于GO语言实现的开源容器项目，可以简单的将它理解为一个沙盒，每个沙盒里运行着一个应用，每个应用间可以通过网络通信，并且每个沙盒占用的资源十分少。

Docker 构想： 对应用的封装，分发，部署，运行。这个应用可以是一个web应用，一个编译环境，也可以是一套数据库平台服务等。 最终目的： 一次封装，到处运行。

Docker的镜像管理：借鉴于Git的设计理念。

#### 三大核心概念

* 镜像（Image)

  类似于虚拟机镜像，理解为一个只读的模板。eg: 一个镜像有基本的系统，安装了Apache应用程序，可以诚挚为一个Apache镜像。

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

  这个命令在多窗口时会阻塞。

* exec 命令 

  `docker exec -it `

* nsenter 工具



删除容器

`docker rm`

不能删除正在运行的容器。

其他：

导出容器，导入容器

HAProxy 工具。



#### 访问Docker仓库

Docker hub公共市场，https://hub.docker.com  

通过` docker login` 来登陆，注册成功后，本地用户的.dockercfg 讲保存用户的认证信息。

* docker search 

  查找官方仓库中的镜像

  可用docker pull 命令将它下载到本地。



### Docker 容器数据管理

多个容器间共享数据。Docker有两种方式：

* 数据卷：容器内数据直接映射到本地主机环境
* 数据卷容器： 使用特定容器维护数据卷





* BaaS（后端即服务，Backend as a Service），公司为移动应用开发者提供整合云后端的边界服务。

* IaaS（基础设施即服务，Infrastructure as a Service），要搭建上层数据应用，先得通过互联网获得基础性设施服务。

* PaaS（平台即服务，Platform-as-a-Service），搭建平台，集成应用产品，整合起来提供服务。

* SaaS（软件即服务，Software-as-a-Service），通过网络提供程序应用类服务。

不管是BaaS、PaaS、SaaS都要建立在IaaS基础设施服务上。其中PaaS、SaaS是IaaS在应用层的延伸，大量SaaS及应用程序服务集中在平台上，打造而成的PaaS才拥有存在的价值。BaaS是针对特定领域（移动应用）提供边界增值服务的平台类型。与SaaS、PaaS互为补充，完善了整个生态格局。  