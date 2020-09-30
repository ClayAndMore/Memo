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

**`Go` 语言程序编译时会将所有必须的依赖编译到二进制文件中，但也不能完全肯定它使用的是静态链接，**因为 `Go` 的某些包是依赖系统标准库的。

例如使用到 DNS 解析的包，只要代码中导入了这些包，编译的二进制文件就需要调用到某些系统库，为了这个需求，Go 实现了一种机制叫 `cgo`，以允许 Go 调用 C 代码，这样编译好的二进制文件就可以调用系统库。

也就是说，如果 Go 程序使用了 `net` 包，就会生成一个动态的二进制文件，如果想让镜像能够正常工作，必须将需要的库文件复制到镜像中，或者直接使用 `busybox:glibc` 镜像。

当然，**你也可以禁止 `cgo`，这样 Go 就不会使用系统库**，使用内置的实现来替代系统库（例如使用内置的 DNS 解析器），这种情况下生成的二进制文件就是静态的。



### CGO_ENABLED

**可以通过设置环境变量 `CGO_ENABLED=0` 来禁用 cgo**，例如：

```dockerfile
FROM golang
COPY whatsmyip.go .
ENV CGO_ENABLED=0
RUN go build whatsmyip.go

FROM scratch
COPY --from=0 /go/whatsmyip .
CMD ["./whatsmyip"]
```

由于编译生成的是静态二进制文件，因此可以直接跑在 `scratch` 镜像中



### tags

也可以不用完全禁用 `cgo`，可以通过 `-tags` 参数指定需要使用的内建库，例如 `-tags netgo` 就表示使用内建的 net 包，不依赖系统库：

```text
$ go build -tags netgo whatsmyip.go
```

果导入的其他包都没有用到系统库，那么编译得到的就是静态二进制文件。也就是说，只要还有一个包用到了系统库，都会开启 `cgo`，最后得到的就是动态二进制文件。要想一劳永逸，还是设置环境变量 `CGO_ENABLED=0` 吧。



### -ldflags

go build 可以用 `-gcflags` 给*go*编译器传入参数，也就是传给go tool compile的参数，因此可以用go tool compile --help查看所有可用的参数。

eg:

**减小编译后的体积**

`go build -ldflags '-w -s'`

说明：
-w 禁止生成debug信息,注意使用该选项后，无法使用 gdb 进行调试，但是打印，看见文件名、行号等信息依然保留。
-s 禁用符号表
可以使用 `go tool link --help` 查看 ldflags 各参数含义

**使用静态编译**

–ldflags “-extldflags -static” 来让gcc使用静态编译



### -gcflags 

如下命令将 Go 语言的源代码编译成汇编语言，然后通过汇编语言分析程序具体的执行过程：

``` go 
go build -gcflags -S main.go
	rel 22+4 t=8 os.(*file).close+0
"".main STEXT size=137 args=0x0 locals=0x58
	0x0000 00000 (main.go:5)	TEXT	"".main(SB), ABIInternal, $88-0
	0x0000 00000 (main.go:5)	MOVQ	(TLS), CX
	0x0009 00009 (main.go:5)	CMPQ	SP, 16(CX)
	..
```





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