Tags:[Go]

## Go

Go 语言又称Golang, 是谷歌开发的一种 **静态类型， 编译型、并发型 具有垃圾回收** 的编程语言。

2009年发布



### 安装



#### 前提

在Mac系统中，只要你安装了Xcode，就已经包含了相应的编译工具。

在类Unix系统中，需要安装gcc等工具。例如Ubuntu系统可通过在终端中执行`sudo apt-get install gcc libc6-dev`来安装编译工具。

在Windows系统中，你需要安装MinGW，然后通过MinGW安装gcc，并设置相应的环境变量。



#### 配置

* 安装，去官网下载对应平台的安装包：https://golang.org/

* 创建目录： `tar -C /usr/local -xzf go1.9.2.linux-amd64.tar.gz`  , 个人喜好不放在/usr/local下

* 环境变量： `vi ~/.bashrc` 

  添加`export PATH=$PATH:/usr/local/go/bin`

  执行`source ~/.bashrc` 使环境变量生效

* 查看： `go version`



个人喜好建立一个新文件夹go_workspace 作为GOPATH:

vim ~/.bashrc:

`export GOPATH=/root/go_workspace`

执行`source ~/.bashrc`,

`go env` ,  就能看到刚才配置的GOPATH路径了。

为了方便，我们加入到 `.bashrc` 或者 `.zshrc` 或者自己的 `sh` 的配置文件中。



ps: 

*  可以配置多个GOPATH,  当我们引包时，会在多个$GOPATH/src里查找
*  GOPATH分割列表分隔符不同，UNIX-like使用冒号， Windows使用分号。
*  使用git等工具时，建议忽略pkg, bin目录，直接在src或具体的子包下创建代码仓库。



#### GOROOT

待补充，

会影响GOROOTDIR, GOROOTDIR则会影响go tool的使用。

个人一般是设置GOROOT 到安装目录`export GOROOT=/root/go`



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

每一个可独立运行的Go程序，必定包含一个`package main`，在这个`main`包中必定包含一个入口函数`main`，而这个函数既没有参数，也没有返回值。

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

`cd src/hell,  go build`

当下目录会生成一个可执行文件， 执行会输出hello world.

`go install `  会在GOPATH/bin下生成一个二进制可执行文件。

`go clearn -i` 会移除上面bin中的文件。



#### 包文件

除了`main`包之外，其它的包最后都会生成`*.a`文件（也就是包文件）并放置在`$GOPATH/pkg/$GOOS_$GOARCH`中（以Mac为例就是`$GOPATH/pkg/darwin_amd64`）。

src 目录是开发的主要目录， 源码都在这个目录， 一般一个应用或者一个包这样表示：

`$GOPATH/src/mymath`

新建一个包：

```
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

和编译main文件不一样的是，go build不会建立任何东西.



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

进入该目录执行`go install`,那么在$GOPATH/bin/下增加了一个可执行文件mathapp,

此时如果没有bin目录，会在`$GOPATH`中自动创建bin目录，并将刚才的mathapp可执行文件放入其中， 为了方便我们将该bin目录加入我们的环境变量 `$PATH` 变量中。



