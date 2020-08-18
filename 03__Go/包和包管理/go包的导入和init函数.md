---
title: "go包的导入和init函数"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-16 23:21:51 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---


## 包管理



### 导入包

import 导入，参数是已src为起始的绝对路径。

`import "net/http"   // 实际路径：/usr/local/go/src/net/http`

编译器从标准库里开始搜索，依次搜索GOPATH列表中的各个工作空间。



可以使用别名，以解决同名冲突问题：

```go
import osx "github.com/apple/osx/lib"
import nix "github.com/linux/lib"
```

So, import默认导入的是路径，而非包名，只是习惯将其包名和目录名保持一致。



使用包中的A方式：

```go
import "github.com/tt/test"     // 默认方式: test.A
import X "github.com/tt/test"   // 别名方式: X.A
import . "github.com/tt/test"	// 简便方式: A, 这样可以直接使用包中的函数名，省略包名
import _ "github.com/tt/test"   // 初始化方式： 无法引用， 只是调用test中的初始函数(init)，和python类似
```



ps:

* 导入的包没有使用会报错
* 不能循环导入
* import	声明必须跟在⽂件的	package	声明之后。



### 相对路径 

在非工作空间可用





### 自定义路径

pass



### 包 package

包由一个或多个保存在同一目录下（不含子目录）的源码文件组成。包名与目录名不要求保持一致。

一个包由位于单个目录下的一个或多个.go源代码文件组成, 目录定义包的作用。

```go
package service  //包通常使用单数形式

func Ping(){
    println("ping")
}
```

每个源文件都以一条`package`声明语句开始，这个例子里就是`package service`, 表示该文件属于哪个包，同一目录下的所有源码文件必须使用相同包名称。

有几个包名被保留：

* main, 可执行入口
* all, 标准库及GOPATH中能找到的包
* std, cmd， 标准库及工具链
* Documentation, 存储文档信息，无法导入（和目录名无关）



#### 初始化

包内每个源码文件的函数init:

```go
var x = 100
func init(){
    println("init:", x)
    x++
}
func main(){
    println("main:", x)
}
输出：
init: 100
main: 101
```

包内每个文件的init，**编译器不保证执行次序**

实际上，所有这些初始函数都由编译器的一个包函数来调用，可以保证只执行一次。

**编译器首先确保完成所有全局变量初始化，然后才开始执行初始化函数。**

直到这些全部结束后，运行时才正式进入main.main入口函数。



**如果在多个初始化函数中引用全局变量， 那么最好在变量定义处直接赋值**。

**因无法保证执行次序，所有初始化函数的赋值都有可能"延迟无效"**

具体可看后面的init函数。



#### 权限

* 所有成员在包内均可访问，无论是否在同一源码文件中。

* 但只有名称首字母大写的为可导出成员，在包外可视。

* 该规则适用于全局变量，常量，类型，结构，函数等等。



但是可以通过指针绕过改限制：

```go
//lib/data.go
package lib

type data struct{
    x int
    Y int
}

func NewData() *data{
    return new(data)
}
```

Test.go

```go
package main
import {
    "fmt"
    "test/lib"
    "unsafe"
}

func main(){
    d := lib.NewData()
    d.Y = 200   //直接访问公有字段
    p := (*struct{x int})(unsafe.Pointer(d)) //利用指针转换访问私有字段
    p.x = 100
    
    fmt.Printf("%+v\n", *d)
}
输出：
{x:100, Y:200}
```



#### 内部包 internal

代码重构分离时，内部模块基于大小写的方式权限控制太粗旷，我们的内部包结构增加了新的访问权限控制

**所有在internal 目录下的包（包括自身）仅能被其父目录下的包（含所有层次子目录）访问 **

```
src/
|
+ -- main.go            # main.go 导入 lib/internal 会 error, not allowed
| 						# 内部包 internal、a、b 仅能被lib、 lib/x、lib/x/y 访问
+ -- lib/				# 内部包之间可以互相访问
	  |
	  +-- internal/		# 可导入外部包，比如lib/x/y
	  |     |
	  |     + -- a/
	  |		| 
	  | 	+ -- b/
	  + -- x/
	  	   |
	  	   + -- y/
```

导入内部包必须使用完整路径，如`import "lib/internal/a"` 



#### 依赖管理 vendor

vendor机制， 专门放第三方包，实现将源码和依赖完整打包分发。

```go
src/
|
+ -- server/
		|
		+ -- vendor/
		|		|
		| 		+ -- github.com/
		|				|
		|				+ -- qyuhen/
		| 						|
		|						+ -- test/
		+ -- main.go    # import "github.com/qyuhen/test" // 优先使用vendor/github.com
```

导入vendor中的第三方包，**参数是以`vendor/` 为起点的绝对路径**， 注意， vendor比标准库优先级更高。

多个vendor时，逐级向上找第一个vendor, 如果没有则用GOPATH。

如果使用vendor机制， 需要开启GO15VENDOREXPERIMENT=1的环境开关，go(1.6)默认开启。



### 注意

如果你在main里定义一个全局变量，其他包是访问不到的

全局变量可以放到一个包下面给大家共同访问



## init 函数

**init函数的主要作用：**

- 初始化不能采用初始化表达式初始化的变量。
- 程序运行前的注册。
- 实现sync.Once功能。
- 其他

**init函数的主要特点：**

- init函数先于main函数自动执行，**不能被其他函数调用；**
- init函数没有输入参数、返回值；
- 每个包可以有多个init函数；
- **包的每个源文件也可以有多个init函数**，这点比较特殊；
- 同一个包的init执行顺序，golang没有明确定义，编程时要注意程序不要依赖这个执行顺序。
- 不同包的init函数按照包导入的依赖关系决定执行顺序。



### **golang程序初始化**

golang程序初始化先于main函数执行，由runtime进行初始化，初始化顺序如下：

1. 初始化导入的包（包的初始化顺序并不是按导入顺序（“从上到下”）执行的，runtime需要解析包依赖关系，没有依赖的包最先初始化，与变量初始化依赖关系类似；
2. 初始化包作用域的变量（该作用域的变量的初始化也并非按照“从上到下、从左到右”的顺序，runtime解析变量依赖关系，没有依赖的变量最先初始化。
3. 执行包的init函数；

**变量初始化->init()->main()**：

``` go
var T int64 = a()

func init() {
   fmt.Println("init in main.go ")
}

func a() int64 {
   fmt.Println("calling a()")
   return 2
}
func main() {                  
   fmt.Println("calling main")     
}
```

输出：

```text
calling a()
init in main.go
calling main
```





### 可以多次定义

``` go
package main
import "fmt"
func init() {
   fmt.Println("init 1")
}
func init() {
   fmt.Println("init 2")
}
func main() {
   fmt.Println("main")
}
```

输出：

init 1
init 2
main

**init函数比较特殊，可以在包里被多次定义。**



### 初始化不能使用初始化表达式初始化的变量

``` go
var intArg [20]int
func init() {
  initArg[0] = 10
  for i := 1; i < len(initArg); i++ {
       initArg[i] = initArg[i-1] * 2
   }
}
```



### 导入包时只执行init

`import _ "net/http/pprof"`

**golang对没有使用的导入包会编译报错，但是有时我们只想调用该包的init函数，不使用包导出的变量或者方法，这时就采用上面的导入方案。**

执行上述导入后，init函数会启动一个异步协程采集该进程实例的资源占用情况，并以http服务接口方式提供给用户查询。