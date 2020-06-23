
---
title: "12-type.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-06-16 23:21:51 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "12-type.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-03-17 15:10:43 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
## type 

### 类型定义

⼀个类型声明语句创建了⼀个新的类型名称，和现有类型具有相同的底层结构。新命名的类型提供了⼀个⽅法，⽤来分 隔不同概念的类型，这样即使它们底层类型相同也是不兼容的。

```
type	类型名字	底层类型
```

在任何程序中都会存在⼀些变量有着**相同的内部结构，但是却表示完全不同的概念。**

例如，⼀个int类型的变量可以⽤来 表示⼀个循环的迭代索引、或者⼀个时间戳、或者⼀个⽂件描述符、或者⼀个⽉份；⼀个float64类型的变量可以⽤来表 示每秒移动⼏⽶的速度、或者是不同温度单位下的温度；⼀个字符串可以⽤来表示⼀个密码或者⼀个颜⾊的名称。

类型声明语句⼀般出现在包⼀级，因此如果新创建的类型名字的⾸字符⼤写，则在包外部也可以使⽤.

为了说明类型声明，我们将不同温度单位分别定义为不同的类型：

``` go
//	Package	tempconv	performs	Celsius	and	Fahrenheit	temperature	computations. 
package	tempconv
import	"fmt"
type Celsius float64	//	摄⽒温度 
type Fahrenheit	float64	//	华⽒温度
const (				
    AbsoluteZeroC	Celsius	=	-273.15	//	绝对零度				
    FreezingC	    Celsius	=	0	    //	结冰点温度				
    BoilingC	    Celsius	=	100		//	沸⽔温度 
)

func CToF(c	Celsius) Fahrenheit	{ return Fahrenheit( c*9/5 + 32 )}
func FToC(f	Fahrenheit)	Celsius	{ return Celsius((f	- 32) *	5 /	9)}
```

我们在这个包声明了两种类型：Celsius和Fahrenheit分别对应不同的温度单位。**它们虽然有着相同的底层类型float64， 但是它们是不同的数据类型，**因此它们不可以被相互⽐较或混在⼀个表达式运算。刻意区分类型，可以避免⼀些像⽆意 中使⽤不同单位的温度混合计算导致的错误；因此需要⼀个类似Celsius(t)或Fahrenheit(t)形式的显式转型操作才能将 float64转为对应的类型。Celsius(t)和Fahrenheit(t)是类型转换操作，它们并不是函数调⽤。类型转换不会改变值本身， 但是会使它们的语义发⽣变化。另⼀⽅⾯，CToF和FToC两个函数则是对不同温度单位下的温度进⾏换算，它们会返回 不同的值。



### 类型转换

**对于每⼀个类型T，都有⼀个对应的类型转换操作T(x)，⽤于将x转为T类型（译注：如果T是指针类型，可能会需要⽤⼩ 括弧包装T，⽐如	(*int)(0)	）**。只有当两个类型的底层基础类型相同时，才允许这种转型操作，或者是两者都是指向相 同底层结构的指针类型，这些转换只改变类型⽽不会影响值本身。如果x是可以赋值给T类型的值，那么x必然也可以被 转为T类型，但是⼀般没有这个必要.

⽐较运算符	==	和	<	也可以⽤来⽐较⼀个命名类型的变量和另⼀个有相同类型的变量，或有着相同底层类型的未命名类 型的值之间做⽐较。但是如果两个**值**有着不同的类型，则不能直接进⾏⽐较：

``` go
var	c Celsius var f	Fahrenheit fmt.Println(c==0) //	"true" 
fmt.Println(f	>=	0)					 // "true" 
fmt.Println(c	==	f)					 //compile	error:	type	mismatch 
fmt.Println(c	==	Celsius(f))	//	"true"!
```

注意最后那个语句。尽管看起来像函数调⽤，**但是Celsius(f)是类型转换操作，它并不会改变值，仅仅是改变值的类型⽽ 已**。测试为真的原因是因为c和g都是零值。

⼀个命名的类型可以提供书写⽅便，特别是可以避免⼀遍⼜⼀遍地书写复杂类型（译注：例如⽤匿名的结构体定义变 量）。虽然对于像float64这种简单的底层类型没有简洁很多，但是如果是复杂的类型将会简洁很多，特别是我们即将讨 论的结构体类型。
命名类型还可以为该类型的值定义新的⾏为。这些⾏为表示为⼀组关联到该类型的函数集合，我们称为类型的⽅法集。 我们将在第六章中讨论⽅法的细节，这⾥只说些简单⽤法。
下⾯的声明语句，Celsius类型的参数c出现在了函数名的前⾯，表示声明的是Celsius类型的⼀个名叫String的⽅法，该 ⽅法返回该类型对象c带着°C温度单位的字符串：

`func (c Celsius)	String() string	 {	return	fmt.Sprintf("%g°C",	c)	}`

许多类型都会定义⼀个String⽅法，因为当使⽤fmt包的打印⽅法时，将会优先使⽤该类型对应的String⽅法返回的结果 打印



### 类型别名

**类型定义和类型别名，不要弄混了**。

类型别名与类型定义不同之处在于：

* 类型别名需要在别名和原类型之间加上赋值符号(=)；
* 类型别名定义的类型与原类型等价，而使用类型定义出来的类型是一种新的类型。

```go
type I int    // 类型定义
type D = int  // 类型别名
```

类型别名这个功能非常有用，鉴于go中有些类型写起来非常繁琐，比如json相关的操作中，经常用到map[string]interface {}这种类型，写起来是不是很繁琐，没关系，给它起个简单的别名：

` type strMap2Any = map[string]interface {}`



#### 设计初衷

类型别名的设计初衷是为了解决代码重构时，类型在包(package)之间转移时产生的问题

> 项目中有一个叫`p1`的包，其中包含一个结构体`T1`。随着项目的进展`T1`变得越来越庞大。我们希望通过代码重构将`T1`抽取并放入到独立的包`p2`，同时不希望影响现有的其他代码。这种情况下以往的go语言的功能不能很好的满足此类需求。类型别名的引入可以为此类需求提供良好的支持。

首先我们可以将T1相关的代码抽取到包p2中：

```go
package p2
type T1 struct {
...
}
func (*T1) SomeFunc() {
...
}
```

之后在p1中放入T1的别名：

```go
package p1
import "p2"

type T1 = p2.T1
```

通过这种操作我们可以在不影响现有其他代码的前提下将类型抽取到新的包当中。现有代码依旧可以通过导入p1来使用T1。而不需要立马切换到p2，可以进行逐步的迁移。此类重构发生不仅仅存在于上述场景还可能存在于以下场景：

- 优化命名：如早期Go版本中的io.ByteBuffer修改为bytes.Buffer。
- 减小依赖大小：如io.EOF曾经放在os.EOF，为了使用EOF必需导入整个os包。
- 解决循环依赖问题



type alias这个特性的主要目的是用于已经定义的类型，在package之间的移动时的兼容。比如我们有一个导出的类型flysnow.org/lib/T1，现在要迁移到另外一个package中, 比如flysnow.org/lib2/T1中。没有type alias的时候我们这么做，就会导致其他第三方引用旧的package路径的代码，都要统一修改，不然无法使用。

有了type alias就不一样了，类型T1的实现我们可以迁移到lib2下，同时我们在原来的lib下定义一个lib2下T1的别名，这样第三方的引用就可以不用修改，也可以正常使用，只需要兼容一段时间，再彻底的去掉旧的package里的类型兼容，这样就可以渐进式的重构我们的代码，而不是一刀切。

```rust
//package:flysnow.org/lib
type T1=lib2.T1。
```