---
title: "00-Go start.md"
date: 2019-10-10 17:44:20 +0800
lastmod: 2020-02-08 12:28:55 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
Tags:[Go]

## Go

Go 语言又称Golang, 是谷歌开发的一种 **静态类型， 编译型、并发型 具有垃圾回收** 的编程语言。

2009年发布



### 安装

Go 提供了每个平台打好包的一键安装，这些包默认会安装到如下目录：`/usr/local/go`。当然你可以改变它们的安装位置，但是改变之后你必须在你的环境变量中设置如下两个环境变量：

- GOROOT：GOROOT 就是 Go 的安装路径
- GOPATH：GOPATH 是作为编译后二进制的存放目的地和 import 包时的搜索路径



#### mac

mac 下一般使用`brew install go` 来 安装

在安装之前也可以通过 **brew info go** 查看版本信息



#### 前提

在Mac系统中，只要你安装了Xcode，就已经包含了相应的编译工具。

在类Unix系统中，需要安装gcc等工具。例如Ubuntu系统可通过在终端中执行`sudo apt-get install gcc libc6-dev`来安装编译工具。

在Windows系统中，你需要安装MinGW，然后通过MinGW安装gcc，并设置相应的环境变量。



#### 配置

安装，去官网下载对应平台的安装包：https://golang.org/, 打不开可以去：https://golang.google.cn/dl/

Linux 版本选择 goxxxxx.linux-amd64.tar.gz 格式的安装包，这里在 Linux 服务器上直接用 `wget` 命令下载：

```
$ wget https://dl.google.com/go/go1.10.2.linux-amd64.tar.gz
```

当前目录

```sh
root@wy:~/go# ls
go1.13.6.linux-amd64.tar.gz
# 解压到当前目录，解压后会多余出来一个go目录
go go1.13.6.linux-amd64.tar.gz
# ls go
1  api  AUTHORS  bin  CONTRIBUTING.md  CONTRIBUTORS  doc  favicon.ico  lib  LICENSE  misc  PATENTS  pkg  README.md  robots.txt  SECURITY.md  src  test  VERSION

# 我们建立 gopath （工作目录）目录， workspace
root@wy:~/go# ls
go  go1.13.6.linux-amd64.tar.gz workspace
```



#### 设置环境变量

```bash
export GOROOT=/root/go/go
export GOPATH=/root/go/go_workspace
export PATH=$GOROOT/bin:$GOPATH/bin/:$PATH
```

如果不想每次登录系统都设置一次环境变量，将上面 追加到 `$HOME/.bashrc` 文件中, 或者 `.zshrc` 或者自己的 `sh` 的配置文件中。

执行`source ~/.bashrc`,

`go env` ,  就能看到刚才配置的GOPATH路径了。

如果 go >= 1.13， 则可以使用 go env -w  去永久设置环境变量，eg:

`go env -w GO111MODULE=off`



**注意**， GOPATH  不用和安装目录一样。

执行 `go version` 检查 Go 是否成功安装

```
$ go version
go version go1.13.6 linux/amd64
```



创建 `$GOPATH/src` 目录

`$GOPATH/src` 是 Go 源码存放的目录，所以在正式开始编码前要先确保 `$GOPATH/src` 目录存在，执行命令：

```
$ mkdir -p $GOPATH/src
```



ps: 

*  可以配置多个GOPATH,  当我们引包时，会在多个$GOPATH/src里查找
*  GOPATH分割列表分隔符不同，UNIX-like使用冒号， Windows使用分号。
*  使用git等工具时，建议忽略pkg, bin目录，直接在src或具体的子包下创建代码仓库。



#### 多版本管理gvm

https://github.com/moovweb/gvm



### 目录结构

#### **路径**：

GO寻找依赖包时会根据`$GOPATH` 来寻找，，

Go从1.1版本到1.7必须设置这个变量，而且不能和Go的安装目录一样， 从go 1.8开始，GOPATH环境变量现在有一个默认值，如果它没有被设置。 它在Unix上默认为$HOME/go。

`$GOPATH` 的目录约定有三个子目录：

- src存放源代码
- pkg存放编译后的生成文件
- bin存放编译后的可执行文件。 

```
workspace/
	|
	+--- src/                       源码
	|	  |
	|     + --- server/
	|     |       |
	| 	  |       + --- main.go
	|     + --- server/
	|             |
	|             + --- main.go
	| --- bin/                      可执行文件安装路径，不会创建额外子目录。
    |     |
    |     + --- server
    + --- pkg/                      包安装路径，安装操作系统和平台隔离。
          |
          + --- linux_amd64/
          		  |
          		  + --- service.a
```



#### main文件

包名`main`则告诉我们它是一个可独立运行的包，它在编译后会产生可执行文件。

每一个可独立运行的Go程序，**必定包含一个package main**`，在这个`main`包中必定包含一个入口函数`main，而这个函数既没有参数，也没有返回值。

我们以hello world为示例：

vim $GOPATH/src/hello/hello.go:

```go
package main
  
import "fmt"

func main(){
        fmt.Printf("hello, world\n")
}
```

编译：

`cd src/hello,  go build`

当下目录会生成一个可执行文件， 执行会输出hello world.

`go install `  会在GOPATH/bin下生成一个二进制可执行文件。

`go clearn -i` 会移除上面bin中的文件。



#### 包文件

除了`main`包之外，其它的包最后都会生成`*.a`文件（也就是包文件）并放置在`$GOPATH/pkg/$GOOS_$GOARCH`中（以Mac为例就是`$GOPATH/pkg/darwin_amd64`,  centos 是 `/disk/go_workspace/pkg/linux_amd64/`）。

src 目录是开发的主要目录， 源码都在这个目录， 一般一个应用或者一个包这样表示：

`$GOPATH/src/mymath`

新建一个包：

```go
cd $GOPATH/src
mkdir mymath
vi  sqrt.go

//代码如下：
package mymath //一般建议package的名称和目录名保持一致

func Sqrt(x float64) float64 {
	z := 0.0
	for i := 0; i < 1000; i++ {
		z -= (z*z - x) / (2 * x)
	}
	return z
}
```



#### 编译包

两种方式可以进行编译安装：

* 应用包目录： `go install`
* 任意目录： `go install mymath`



之后我们可以在 `cd $GOPATH/pkg/${GOOS}_${GOARCH}`, 看到：mymath. a (这个a文件就是应用包了。)

如果pkg文件夹没有建立，会自动创建

**和编译main文件不一样的是，go build不会建立任何东西.**



#### 调用包

```
cd $GOPATH/src
mkdir mathapp
cd mathapp
vim main.go
```

main.go源码：

```go
package main

import (
	"mymath"
	"fmt"
)

func main() {
	fmt.Printf("Hello, world.  Sqrt(2) = %v\n", mymath.Sqrt(2))
}
```

import里面调用的包是`mymath`,这个就是相对于`$GOPATH/src`的路径，如果是多级目录，就在import里面引入多级目录，如果你有多个GOPATH，也是一样，Go会自动在多个`$GOPATH/src`中寻找。

测试成果：

go build, 生成该目录下一个可执行文件：./mathapp

```
root@10.250.xx.xx mathapp # ./mathapp
Hello, world.  Sqrt(2) = 1.414213562373095
```

进入该目录执行`go install`,那么在$GOPATH/bin/下增加了一个可执行文件mathapp,

此时如果没有bin目录，会在`$GOPATH`中自动创建bin目录，并将刚才的mathapp可执行文件放入其中， 为了方便我们将该bin目录加入我们的环境变量 `$PATH` 变量中。



