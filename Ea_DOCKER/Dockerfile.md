Tags:[Docker]

## 使用Dockerfile创建镜像

Dockerfile 是一个文本格式的配置文件。
一般来说，这个配置文件包括四个部分：

- 基础镜像信息
- 维护者信息
- 镜像操作指令
- 容器启动时指令

### 命令说明

以#来注释，配合自己各种指令。

一个demo:

```shell
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

#### FROM: 
指定创建镜像的基础镜像，指定第一层image, 这是必须有的. 并且指定的image是存在在你的computer中. 相当于是 docker run.没有回不去Docker Hub中下载。

#### MAINTAINER
设置作者和联系邮箱.其实就是docker commit 后面的Name参数. 而且加上了联系邮箱. 这是在dockerfile 运行完后,会自动添加到image上的.

#### RUN
在容器中做出相应的修改并提交给镜像，作为一个新的镜像： `修改+docker commite xxx` ,这样原来的镜像就又加了一层并提交作为一个新的镜像。run命令有两种形式：

  - RUN+命令： 这种形式等同于`/bin/sh -c + 命令` -c参数是说标准输入替换为字符串。这时如果命令较长可以用反斜杠来整理格式：

    ```
    RUN apt-get update \
            && apt-get install -y libsnappy-dev ziliblg-dev libbz2-dev \
            && rm -rf /var/cache/apt 
    ```

  - RUN+数组： 这种形式不会启动shell环境，用exec执行，eg:`RUN ["/bin/bash","-c","echo hell"]`


#### EXPOSE
用来给最新的container 设置与外部交流的port,现在我们可以使用-P(注意是大写). 来手动开启所有在dockerfile中,通过EXPOSE暴露的端口.

其他命令：
#### CMD
指定启动容器时的默认命令，写法和RUN一样（也是分shell环境和非shell环境）：

  ```yaml
  # 当调起container时,运行/bin/bash
  docker run  -t -i jimmy/ubuntu:latest /bin/bash
  # 等同于在dockerfile中指定CMD
  CMD ["/bin/bash"]
  // 运行docker run
  docker run -t -i jimmy/ubuntu:latest
  ```

  如果docker run时写运行命令，会覆盖掉CMD.

#### ENTRYPOINT
是说强制执行的环境,有时可以和CMD相互代替，主要功能实际上是,指定了内部运行命令的解析器. 而使用docker   run添加的命令,会被当做参数添加给ENTRYPOINT.

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

#### WORKDIR 
指定运行目录
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

#### VOLUME 
指定数据卷的位置：

  ```
  # 指定/opt/data为数据卷
  VOLUME ["/opt/data"]
  # 指定多个目录为数据卷/opt/data, /opt/project
  VOLUME ["/opt/data","/opt/project"]
  ```

#### COPY 和 ADD 
为容器添加文件
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

  COPY做的事情比不上ADD, 他比ADD少了解压缩和URL下载的功能. 不过,他耗费的性能比较少,他只做纯粹的添加和下载.他的结构和ADD一毛一样. 

  不过, 有一点,COPY的时候,如果遇到目录不存在的情况下,COPY会自动创建

  `COPY file.js /opt/data/`

#### ARG 和 ENV 
命令相似，ARG只能用在docker build的阶段, 并且不会被保存在image中,这就是和ENV的区别.

  ```
  # 在dockerfile定义了默认变量
  ARG user=jimy
  # 在运行时,进行手动替换
  docker build --build-arg user=sam -t jimmy/demo   
  ```

#### ONBUILD 
模板image,因为镜像的可写层数是有限制的，我们需要继承模板来在子dockerfile中使用。



### 运行

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

### 