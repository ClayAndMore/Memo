
---
title: "Dockerfile-多阶段构建.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-04-07 08:49:48 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Docker在17.05之后就能支持多阶构建了，为了使镜像更加小巧，我们采用多阶构建的方式来打包镜像。在多阶构建出现之前我们通常使用一个Dockerfile或多个Dockerfile来构建镜像。

## 多阶段构建

多阶段构建镜像能够缩减镜像的大小，是因为发布程序在编译期相关的依赖包以及临时文件并不是最终发布镜像所需要的。通过划分不同的阶段，构建不同的镜像，最终镜像则取决于我们真正需要发布的实体是什么。

``` dockerfile
FROM golang:1.11-alpine3.7 AS builder

WORKDIR /app
COPY main.go .
RUN go build -o server .

FROM alpine:3.7

WORKDIR /app
COPY --from=builder /app .

CMD ["./server"]
```

如上的`Dockerfile`就是多阶段构建，在`builder`阶段使用的基础镜像是`golang:1.11-alpine3.7`，显然是因为编译期的需要，对于发布真正的`server`程序是完全没必要的。通过多阶段构建镜像的方式就可以仅仅打包需要的实体构成镜像。

除了多阶段构建以外，如果你还想忽略镜像中一些冗余文件，还可以通过`.dockerignore`的方式在文件中定义出来。功能和`.gitignore`类似。



## 如何构建最小化docker镜像

### 减少layer的层数

有两种方式可以减少layer的层数：

* 组合命令： 在定义`Dockerfile`的时候，每一条指令都会对应一个新的镜像层。为了减少镜像的层数，在实际构建镜像时，通过使用`&&`连接命令的执行过程，将多个命令定义到一个构建指令中执行。如：

  ```sh
  FROM debian:stable
  
  WORKDIR /var/www
  
  RUN apt-get update && \
      apt-get -y --no-install-recommends install curl \
          ca-certificates && \
      apt-get purge -y curl \
          ca-certificates && \
      apt-get autoremove -y && \
      apt-get clean
  ```

* 压缩镜像层

  在`Docker`镜像的构建过程中，还可以通过`--squash`的方式，开启镜像层的压缩功能，将多个变化的镜像层，压缩成一个新的镜像层：

  `docker build --squash -t <image> .`



### 减缩镜像的layer大小

#### 选择基础镜像

缩减Layer的大小需要从头开始，即选择什么样的基础镜像作为初始镜像。一般情况下，大家都会从以下三个基础镜像开始。

- **镜像 scratch**(空镜像), 大小 0B
- **镜像 busybox**(空镜像 + busybox), 大小 1.4MB
- **镜像 alpine** (空镜像 + busybox + apk), 大小 3.98MB

**镜像 busybox** 通过`busybox`程序提供一些基础的Linux系统操作命令，**镜像 alpine**则是在次基础上提供了`apk`包管理命令，方便安装各类工具及依赖包。广泛使用的镜像基本都是**镜像 alpine**。**镜像 busybox**更适合一些快速的实验场景。而**镜像 scratch**空镜像，因为不提供任何辅助工具，对于不依赖任何第三方库的程序是合适的。因为**镜像 scratch**空镜像本身不提供任何`container OS`,所以程序是运行在`Docker Host`即宿主机上的，只是利用了`Docker`技术提供的隔离技术而已。



#### 多阶段构建

如上

参考：gitdig.com/build-a-small-image/