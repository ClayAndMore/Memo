## Go(2)_ 语言基础



### 关键字

就25个：

```
break    default      func    interface    select
case     defer        go      map          struct
chan     else         goto    package      switch
const    fallthrough  if      range        type
continue for          import  return       var
```



### 启动

看一个hello world:

```go
package main

import "fmt"

func main() {
	fmt.Printf("Hello, world or 你好，世界 or καλημ ́ρα κóσμ or こんにちはせかい\n")
}
```



* `package <package_name>  `  告诉我们当前文件属于哪个包
* `main`包中必定包含一个入口函数`main`，而这个函数既没有参数，也没有返回值。
* 打印函数`Printf`，这个函数来自于`fmt`包，所以我们在第三行中导入了系统级别的`fmt`包：`import "fmt"`。
* Go是**天生支持UTF-8**的，任何字符都可以直接输出，你甚至可以用UTF-8中的任何字符作为标识符。



### 定义变量

使用`var`关键字是Go最基本的定义变量方式，与C语言不同的是Go把变量类型放在变量名后面：

```
//定义一个名称为“variableName”，类型为"type"的变量
var variableName type
```

定义多个变量

```
//定义三个类型都是“type”的变量
var vname1, vname2, vname3 type
```





#### 初始化

```go
//初始化“variableName”的变量为“value”值，类型是“type”
var variableName type = value
```

同时初始化多个变量

```go
/*
	定义三个类型都是"type"的变量,并且分别初始化为相应的值
	vname1为v1，vname2为v2，vname3为v3
*/
var vname1, vname2, vname3 type= v1, v2, v3
```

简化：

`var vname1, vname2, vname3 = v1, v2, v3`

然后Go会根据其相应值的类型来帮你初始化它们

继续简化：

`vname1, vname2, vname3 := v1, v2, v3`

现在是不是看上去非常简洁了？`:=`这个符号直接取代了`var`和`type`,这种形式叫做简短声明。不过它有一个限制，那就是它只能用在函数内部；在函数外部使用则会无法编译通过，所以一般用`var`方式来定义全局变量。



#### 常量

字符串等类型。

它的语法如下：

```
const constantName = value
//如果需要，也可以明确指定常量的类型：
const Pi float32 = 3.1415926
```

下面是一些常量声明的例子：

```
const Pi = 3.1415926
const i = 10000
const MaxThread = 10
const prefix = "astaxie_"
```

Go 常量和一般程序语言不同的是，可以指定相当多的小数位数(例如200位)， 若指定給float32自动缩短为32bit，指定给float64自动缩短为64bit



#### 分组声明

在Go语言中，同时声明多个常量、变量，或者导入多个包时，可采用分组的方式进行声明。

例如下面的代码：

```go
import "fmt"
import "os"

const i = 100
const pi = 3.1415
const prefix = "Go_"

var i int
var pi float32
var prefix string
```

可以分组写成如下形式：

```go
import(
	"fmt"
	"os"
)

const(
	i = 100
	pi = 3.1415
	prefix = "Go_"
)

var(
	i int
	pi float32
	prefix string
)
```



### 内置类型

#### Boolean

在Go中，布尔值的类型为`bool`，值是`true`或`false`，默认为`false`。

```
//示例代码
var isActive bool  // 全局变量声明
var enabled, disabled = true, false  // 忽略类型的声明
func test() {
	var available bool  // 一般声明
	valid := false      // 简短声明
	available = true    // 赋值操作
}
```



#### 数值类型

整数类型有无符号和带符号两种。Go同时支持`int`和`uint`，这两种类型的长度相同，但具体长度取决于不同编译器的实现。Go里面也有直接定义好位数的类型：`rune`, `int8`, `int16`, `int32`, `int64`和`byte`, `uint8`, `uint16`, `uint32`, `uint64`。其中`rune`是`int32`的别称，`byte`是`uint8`的别称。

> 需要注意的一点是，这些类型的变量之间不允许互相赋值或操作，不然会在编译时引起编译器报错。
>
> 如下的代码会产生错误：invalid operation: a + b (mismatched types int8 and int32)
>
> > var a int8

> > var b int32

> > c:=a + b
>
> 另外，尽管int的长度是32 bit, 但int 与 int32并不可以互用。

浮点数的类型有`float32`和`float64`两种（没有`float`类型），默认是`float64`。

这就是全部吗？No！Go还支持复数。它的默认类型是`complex128`（64位实数+64位虚数）。如果需要小一些的，也有`complex64`(32位实数+32位虚数)。复数的形式为`RE + IMi`，其中`RE`是实数部分，`IM`是虚数部分，而最后的`i`是虚数单位。下面是一个使用复数的例子：

```
var c complex64 = 5+5i
//output: (5+5i)
fmt.Printf("Value is: %v", c)
```



#### 字符串

我们在上一节中讲过，Go中的字符串都是采用`UTF-8`字符集编码。字符串是用一对双引号（`""`）或反引号（``` ```）括起来定义，它的类型是`string`。

```go
//示例代码
var frenchHello string  // 声明变量为字符串的一般方法
var emptyString string = ""  // 声明了一个字符串变量，初始化为空字符串
func test() {
	no, yes, maybe := "no", "yes", "maybe"  // 简短声明，同时声明多个变量
	japaneseHello := "Konichiwa"  // 同上
	frenchHello = "Bonjour"  // 常规赋值
}
```

在Go中字符串是不可变的，例如下面的代码编译时会报错：cannot assign to s[0]

```go
var s string = "hello"
s[0] = 'c'

```

但如果真的想要修改怎么办呢？下面的代码可以实现：

```go
s := "hello"
c := []byte(s)  // 将字符串 s 转换为 []byte 类型
c[0] = 'c'
s2 := string(c)  // 再转换回 string 类型
fmt.Printf("%s\n", s2)
```

Go中可以使用`+`操作符来连接两个字符串：

```go
s := "hello,"
m := " world"
a := s + m
fmt.Printf("%s\n", a)
```

修改字符串也可写为：

```go
s := "hello"
s = "c" + s[1:] // 字符串虽不能更改，但可进行切片操作
fmt.Printf("%s\n", s)
```

如果要声明一个多行的字符串怎么办？可以通过```来声明：

```go
m := `hello
	world`
```

\``` 括起的字符串为Raw字符串，即字符串在代码中的形式就是打印时的形式，它没有字符转义，换行也将原样输出。例如本例中会输出：

```
hello
	world
```



#### 错误类型

Go内置有一个`error`类型，专门用来处理错误信息，Go的`package`里面还专门有一个包`errors`来处理错误：

```go
err := errors.New("emit macho dwarf: elf header corrupted")
if err != nil {
	fmt.Print(err)
}
```





#### iota枚举

Go里面有一个关键字`iota`，这个关键字用来声明`enum`的时候采用，它默认开始值是0，const中每增加一行加1：

```go
package main

import (
	"fmt"
)

const (
	x = iota // x == 0
	y = iota // y == 1
	z = iota // z == 2
	w        // 常量声明省略值时，默认和之前一个值的字面相同。这里隐式地说w = iota，因此w == 3。其实上面y和z可同样不用"= iota"
)

const v = iota // 每遇到一个const关键字，iota就会重置，此时v == 0

const (
	h, i, j = iota, iota, iota //h=0,i=0,j=0 iota在同一行值相同
)

const (
	a       = iota //a=0
	b       = "B"
	c       = iota             //c=2
	d, e, f = iota, iota, iota //d=3,e=3,f=3
	g       = iota             //g = 4
)

func main() {
	fmt.Println(a, b, c, d, e, f, g, h, i, j, x, y, z, w, v)
}
```

> 除非被显式设置为其它值或`iota`，每个`const`分组的第一个常量被默认设置为它的0值，第二及后续的常量被默认设置为它前面那个常量的值，如果前面那个常量的值是`iota`，则它也被设置为`iota`。



#### array



#### slice



#### map



#### 默认零值

```go
int     0
int8    0
int32   0
int64   0
uint    0x0
rune    0 //rune的实际类型是 int32
byte    0x0 // byte的实际类型是 uint8
float32 0 //长度为 4 byte
float64 0 //长度为 8 byte
bool    false
string  ""
```



#### struct



### Go内置的一些规则

Go之所以会那么简洁，是因为它有一些默认的行为：

- 大写字母开头的变量是可导出的，也就是其它包可以读取的，是公有变量；小写字母开头的就是不可导出的，是私有变量。
- 大写字母开头的函数也是一样，相当于`class`中的带`public`关键词的公有函数；小写字母开头的就是有`private`关键词的私有函数。