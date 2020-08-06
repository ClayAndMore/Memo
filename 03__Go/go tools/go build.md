---
title: "go build.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
## go build



### -ldflags

go build 可以用 `-gcflags` 给*go*编译器传入参数，也就是传给go tool compile的参数，因此可以用go tool compile --help查看所有可用的参数。

eg:

**减小编译后的体积**

`go build -ldflags '-w -s'`

说明：
-w 禁止生成debug信息,注意使用该选项后，无法使用 gdb 进行调试，但是打印，看见文件名、行号等信息依然保留。
-s 禁用符号表
可以使用 `go tool link --help` 查看 ldflags 各参数含义



**禁止gc优化和内联**

`go build -gcflags '-N -l'`

-N 禁止编译优化
-l 禁止内联,禁止内联也可以一定程度上减小可执行程序大小

禁止优化和内联可以让运行时(runtime)中的函数变得更容易调试.



**报错时移除绝对路径信息**

```sh
   CGO_ENABLED=0 go build -v -a -ldflags '-s -w' \
   	-gcflags="all=-trimpath=${PWD}" \
   	-asmflags="all=-trimpath=${PWD}" \
   	-o ./main main.go
```





### 临时目录

设置build 时的临时目录，有时目录会满或者磁盘只读等问题：

export TMPDIR=/othertmp





## go 的交叉编译

golang如何在一个平台编译另外一个平台可以执行的文件。比如在mac上编译Windows和linux可以执行的文件。那么我们的问题就设定成：如何在mac上编译64位linux的可执行文件。