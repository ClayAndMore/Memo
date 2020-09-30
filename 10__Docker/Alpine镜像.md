---
title: "一些命令.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-22 18:42:33 +0800
draft: false
tags: [""]
categories: ["Docker"]
author: "Claymore"
---

## scratch

`ello world`，C 语言版本的程序大小为 `16 kB`，Go 语言版本的程序大小为 `2 MB`，那么我们到底能不能将镜像缩减到这么小？能否构建一个只包含我需要的程序，没有任何多余文件的镜像？

答案是肯定的，你只需要将多阶段构建的第二阶段的基础镜像改为 `scratch` 就好了。`scratch` 是一个虚拟镜像，不能被 pull，也不能运行，因为它表示空、nothing！这就意味着新镜像的构建是从零开始，不存在其他的镜像层。例如：

``` dockerfile
FROM golang
COPY hello.go .
RUN go build hello.go
FROM scratch
COPY --from=0 /go/hello .
CMD ["./hello"]
```



使用scratch的缺点，缺少 shell, 缺少调试工具，缺少libc



## 缺少libc

```text
standard_init_linux.go:211: exec user process caused "no such file or directory"
```

一般在容器中运行go或c编译后的文件时，会有如上报错， 从报错信息可以看出缺少文件，但没有告诉我们到底缺少哪些文件，**其实这些文件就是程序运行所必需的动态库**（dynamic library）。

所谓动态库、静态库，指的是程序编译的**链接阶段**，链接成可执行文件的方式。**静态库**指的是在链接阶段将汇编生成的目标文件.o 与引用到的库一起链接打包到可执行文件中，因此对应的链接方式称为**静态链接**（static linking）。而动态库在程序编译时并不会被连接到目标代码中，而是在程序运行是才被载入，因此对应的链接方式称为**动态链接**（dynamic linking）。

默认情况下，C 程序使用的是动态链接，Go 程序也是。上面的 `hello world` 程序使用了标准库文件 `libc.so.6`，所以只有镜像中包含该文件，程序才能正常运行。使用 `scratch` 作为基础镜像肯定是不行的，使用 `busybox` 和 `alpine` 也不行，因为 `busybox` 不包含标准库，而 alpine 使用的标准库是 `musl libc`，与大家常用的标准库 `glibc` 不兼容。



### 解决方式：

1使用静态库

我们可以让编译器使用静态库编译程序，办法有很多，如果使用 gcc 作为编译器，只需加上一个参数 `-static`：

```text
$ gcc -o hello hello.c -static
```

go,可以使用 ENV CGO_ENABLED=0

2拷贝库文件到镜像

使用ldd工具找出程序运行需要哪些库文件：

``` 
ldd hello
    linux-vdso.so.1 (0x00007ffdf8acb000)
    libc.so.6 => /usr/lib/libc.so.6 (0x00007ff897ef6000)
    /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007ff8980f7000)
```

你可以选择将 `ldd` 列出的所有库文件拷贝到镜像中，但这会很难维护，特别是当程序有大量依赖库时。对于 `hello world` 程序来说，拷贝库文件完全没有问题，但对于更复杂的程序会有很多依赖。

3使用busybox.glibc作为基础镜像

有一个镜像可以完美解决所有的这些问题，那就是 `busybox:glibc`。它只有 `5 MB` 大小，并且包含了 `glibc` 和各种调试工具。如果你想选择一个合适的镜像来运行使用动态链接的程序，`busybox:glibc` 是最好的选择。

注意：如果你的程序使用到了除标准库之外的库，仍然需要将这些库文件拷贝到镜像中。




## Alpine

`Alpine` 是众多 Linux 发行版中的一员，和 `CentOS`、`Ubuntu`、`Archlinux` 之类一样，只是一个发行版的名字，号称小巧安全，有自己的包管理工具 `apk`。

与 CentOS 和 Ubuntu 不同，Alpine 并没有像 `Red Hat` 或 `Canonical` 之类的大公司为其提供维护支持，软件包的数量也比这些发行版少很多（如果只看开箱即用的默认软件仓库，Alpine 只有 `10000` 个软件包，而 Ubuntu、Debian 和 Fedora 的软件包数量均大于 `50000`。）

容器崛起之前，`Alpine` 还是个无名之辈，可能是因为大家并不是很关心操作系统本身的大小，毕竟大家只关心业务数据和文档，程序、库文件和系统本身的大小通常可以忽略不计。

容器技术席卷整个软件产业之后，大家都注意到了一个问题，那就是容器的镜像太大了，浪费磁盘空间，拉取镜像的时间也很长。于是，人们开始寻求适用于容器的更小的镜像。对于那些耳熟能详的发行版（例如 Ubuntu、Debian、Fedora）来说，只能通过删除某些工具（例如 `ifconfig` 和 `netstat`）将镜像体积控制在 `100M` 以下。而对于 Alpine 而言，什么都不用删除，镜像大小也就只有 `5M` 而已。

Alpine 镜像的另一个优势是包管理工具的执行速度非常快，安装软件体验非常顺滑。诚然，在传统的虚拟机上不需要太关心软件包的安装速度，同一个包只需要装一次即可，无需不停重复安装。容器就不一样了，你可能会定期构建新镜像，也可能会在运行的容器中临时安装某些调试工具，如果软件包的安装速度很慢，会很快消磨掉我们的耐心。



既然 Alpine 这么棒，为什么不用它作为所有镜像的基础镜像呢？为了趟平所有的坑，需要分两种情况来考虑：

1. 使用 Alpine 作为第二构建阶段（`run` 阶段）的基础镜像
2. 使用 ALpine 作为所有构建阶段（`run` 阶段和 `build` 阶段）的基础镜像

### 

### RUN 阶段使用 Alpine

