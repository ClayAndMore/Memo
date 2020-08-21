---
title: "11-Goroutines和Channels.md"
date: 2020-02-08 12:27:11 +0800
lastmod: 2020-03-17 15:10:43 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
## Goroutines

在Go语⾔中，每⼀个并发的执⾏单元叫作⼀个goroutine。

设想这⾥的⼀个程序有两个函数，⼀个函数做计算，另⼀个 输出结果，假设两个函数没有相互之间的调⽤关系。⼀个线性的程序会先调⽤其中的⼀个函数，然后再调⽤另⼀个。如 果程序中包含多个goroutine，对两个函数的调⽤则可能发⽣在同⼀时刻。
可以简单地把goroutine类⽐作⼀个线程，goroutine和线程的本质区别后面会讲。

当⼀个程序启动时，其主函数即在⼀个单独的goroutine中运⾏，我们叫它main goroutine。新的goroutine会⽤go语句来 创建。在语法上，go语句是⼀个普通的函数或⽅法调⽤前加上关键字go。go语句会使其语句中的函数在⼀个新创建的 goroutine中运⾏。⽽go语句本身会迅速地完成。

``` go
f()	 //	call f();	wait for it	to	return 
go f()	 //	create a new goroutine	that calls	f(); don't	wait
```

注意 go f()， 并不会等待 f() 返回。



下⾯的例⼦，main	goroutine将计算菲波那契数列的第45个元素值。由于计算函数使⽤低效的递归，所以会运⾏相当⻓ 时间，在此期间我们想让⽤户看到⼀个可⻅的标识来表明程序依然在正常运⾏，所以来做⼀个动画的⼩图标：

``` go
package main

import (
    "time"
    "fmt"
)

func main() {
    go spinner(100 * time.Millisecond)
    const n = 45
    fibN := fib(n)  //  slow
    fmt.Printf("\rFibonacci(%d) = %d\n", n, fibN)
}

func spinner(delay  time.Duration) {
    for {
        for _,  r := range  `-\|/` {
            fmt.Printf("\r%c",  r)
            time.Sleep(delay)
        }
    }
}

func fib(x int) int {
    if  x < 2 {
        return  x
    }
    return  fib(x-1) + fib(x-2)
}
```

fib(45)的调⽤成功地返回，**然后主函数返回。主函数返回时，所有的goroutine都会被直接打断，程序退出。**除了从主函数退出或者直接终⽌程序之 外，没有其它的编程⽅法能够让⼀个goroutine来打断另⼀个的执⾏，但是之后可以看到⼀种⽅式来实现这个⽬的，通过 goroutine之间的通信来让⼀个goroutine请求其它的goroutine，并让被请求的goroutine⾃⾏结束执⾏。

spinning和菲波那契的计算。分别在独⽴的函数中，但两个函数会 同时执⾏。



### 并发的 Clock 服务

这个例子是 顺序执行的时钟服务， 每隔一秒将当前时间写到客户端

``` go
package	main
import	(
    "io"
    "log"				
    "net"
    "time" 
)

func main()	{
    listener, err := net.Listen("tcp",	"localhost:8000")
    if	err	!=	nil	{
        log.Fatal(err)
    }
	for	{ 
        conn, err := listener.Accept()
        if err != nil {	
            log.Print(err)	//	e.g.,	connection	aborted	
            continue
        }
        handleConn(conn)	// handle one connection at	a time
    } 
}
func handleConn(c net.Conn)	{
    defer c.Close()	
    for	{
        _, err := io.WriteString(c, time.Now().Format("15:04:05\n"))
        if err != nil {
            return	// e.g.,	client	disconnected
        }
        time.Sleep(1 * time.Second) 
    } 
}
```

Listen函数创建了⼀个net.Listener的对象，这个对象会监听⼀个⽹络端⼝上到来的连接，在这个例⼦⾥我们⽤的是TCP 的localhost:8000端⼝。listener对象的Accept⽅法会直接阻塞，直到⼀个新的连接被创建，然后会返回⼀个net.Conn对 象来表示这个连接

为了连接例⼦⾥的服务器，我们需要⼀个客户端程序，⽐如netcat这个⼯具（nc命令），这个⼯具可以⽤来执⾏⽹络连 接操作。

```
$ go build	gopl.io/ch8/clock1 
$ ./clock1	& 
$ nc localhost 8000 
13:58:54 
13:58:55 
13:58:56 
13:58:57 ^C
```

因为我们这⾥的服务器程序同⼀时间只 能处理⼀个客户端连接。我们这⾥对服务端程序做⼀点⼩改动，使其⽀持并发：在handleConn函数调⽤的地⽅增加go 关键字，让每⼀次handleConn的调⽤都进⼊⼀个独⽴的goroutine。

``` go
for	{
    conn, err := listener.Accept()
    if err != nil {
        log.Print(err)	//	e.g.,	connection	aborted	
        continue
    }
        go	handleConn(conn)	//	handle	connections	concurrently 
}
```



## Channels

如果说goroutine是Go语⾔程序的并发体的话，那么channels则是它们之间的通信机制。⼀个channel是⼀个通信机制， 它可以让⼀个goroutine通过它给另⼀个 goroutine 发送值信息。每个channel都有⼀个特殊的类型，也就是channels可发 送数据的类型。⼀个可以发送int类型数据的channel⼀般写为chan int。

使用内置 make 函数， 可以创建一个 channel:

`ch	:= make(chan int) // ch	has	type 'chan	int'`

和map类似，channel也对应⼀个make创建的底层数据结构的引⽤。
当我们复制⼀个channel或⽤于函数参数传递时， 我们只是拷⻉了⼀个channel引⽤，因此调⽤者和被调⽤者将引⽤同⼀个channel对象。

`var ch1 chan int // 信道只是 被声明，但没有被初始化，值为nil`

**和其它的引⽤类型⼀样， channel的零值也是nil。**
两个相同类型的channel可以使⽤==运算符⽐较。如果两个channel引⽤的是相同的对象，那么⽐较的结果为真。⼀个 channel也可以和nil进⾏⽐较。



### 发送和接收

⼀个channel有发送和接受两个主要操作，都是通信⾏为。

⼀个发送语句将⼀个值从⼀个goroutine通过channel发送到另 ⼀个执⾏接收操作的goroutine。发送和接收两个操作都使⽤	<-	运算符。

在发送语句中，	<-	运算符分割channel和要发 送的值。

在接收语句中，	<-	运算符写在channel对象之前。

⼀个不使⽤接收结果的接收操作也是合法的。

```
ch <- x	   //  发送语句
x =	<-ch   //  接收语句
<-ch	   // 接收语句，不使用接收结果
```





### 缓存

以最简单⽅式调⽤make函数创建的是⼀个⽆缓存的channel，但是我们也可以指定第⼆个整型参数，对应channel的容 量。如果channel的容量⼤于零，那么该channel就是带缓存的channel。

``` go
ch = make(chan int)		  // unbuffered	channel 
ch = make(chan int,	0)	  // unbuffered	channel 
ch = make(chan int,	3)	  // buffered channel with capacity	3
```

**⼀个基于⽆缓存Channels的发送操作将导致发送者goroutine阻塞**，直到另⼀个goroutine在相同的Channels上执⾏接收 操作，当发送的值通过Channels成功传输之后，两个goroutine可以继续执⾏后⾯的语句。反之，如果接收操作先发 ⽣，**那么接收者goroutine也将阻塞**，直到有另⼀个goroutine在相同的Channels上执⾏发送操作。

基于⽆缓存Channels的发送和接收操作将导致两个goroutine做⼀次同步操作。因为这个原因，⽆缓存Channels有时候 也被称为同步Channels

带缓存的Channel内部持有⼀个元素队列。队列的最⼤容量是在调⽤make函数创建channel时通过第⼆个参数指定的。 

向缓存Channel的发送操作就是向内部缓存队列的尾部插⼊元素，接收操作则是从队列的头部删除元素。**如果内部缓存 队列是满的，那么发送操作将阻塞直到因另⼀个goroutine执⾏接收操作⽽释放了新的队列空间。相反，如果channel是 空的，接收操作将阻塞直到有另⼀个goroutine执⾏发送操作⽽向队列插⼊元素。**

在某些特殊情况下，程序可能需要知道channel内部缓存的容量，可以⽤内置的cap函数获取：

``` go
ch = make(chan string,3 )
ch	<-	"A" 
ch	<-	"B"
fmt.Println(cap(ch)) // "3",  容量
// 内置len 函数会返回 channel 内部缓存袋装中的有效元素的个数。
fmt.Println(len(ch)) //	"2"
```

Go语⾔新⼿有时候会将⼀个带缓存的channel当作同⼀个goroutine中的队列使⽤，虽然语法看似简单，但实际上这是⼀ 个错误。Channel和goroutine的调度器机制是紧密相连的，如果没有其他goroutine从channel接收，发送者——或许是 整个程序——将会⾯临永远阻塞的⻛险。

**如果你只是需要⼀个简单的队列，使⽤slice就可以了。**

下⾯的例⼦展示了⼀个使⽤了带缓存channel的应⽤。它并发地向三个镜像站点发出请求，三个镜像站点分散在不同的 地理位置。它们分别将收到的响应发送到带缓存channel，最后接收者只接收第⼀个收到的响应，也就是最快的那个响 应。因此mirroredQuery函数可能在另外两个响应慢的镜像站点响应之前就返回了结果。（顺便说⼀下，多个goroutines 并发地向同⼀个channel发送数据，或从同⼀个channel接收数据都是常⻅的⽤法。）

``` go
func mirroredQuery() string	{
    responses := make(chan string,	3)
    go func() {	responses <- request("asia.gopl.io") }()
    go func() {	responses <- request("europe.gopl.io") }()
    go func() {	responses <- request("americas.gopl.io") }()				return	<-responses	//	return	the	quickest	response }
func request(hostname string) (response	string)	{ /* ... */	}
```

如果我们使⽤了⽆缓存的channel，那么两个慢的goroutines将会因为没有⼈接收⽽被永远卡住。这种情况，**称为 goroutines泄漏**，这将是⼀个BUG。和垃圾变量不同，泄漏的goroutines并不会被⾃动回收，因此确保每个不再需要的 goroutine能正常退出是重要的。





### 串联的Channels(Pipline)

Channels也可以⽤于将多个goroutine连接在⼀起，⼀个Channel的输出作为下⼀个Channel的输⼊。这种串联的 Channels就是所谓的管道（pipeline）。下⾯的程序⽤两个channels将三个goroutine串联起来:

```
----------                   ----------                 ----------
| Counter| --- naturals -->  | Squarer| --- squares --> | Printer|
----------                   ----------                 ----------
```

第⼀个goroutine是⼀个计数器，⽤于⽣成0、1、2、……形式的整数序列，然后通过channel将该整数序列发送给第⼆ 个goroutine；

第⼆个goroutine是⼀个求平⽅的程序，对收到的每个整数求平⽅，然后将平⽅后的结果通过第⼆个 channel发送给第三个goroutine；

第三个goroutine是⼀个打印程序，打印收到的每个整数。为了保持例⼦清晰，我们有 意选择了⾮常简单的函数.

``` go
func main() {
    naturals := make(chan int)
    squares := make(chan int)
    // Counter
    go func() {
        for x :=0; x++ {
            naturals <- x
        }
    }()
    // Squarer
    go func() {
        for {
            x := <-naturals
            squares <- x * x
        }
    }()
    // Printer (in main goroutine)
    for {
        fmt.Println(<-squares)
    }
}
```



### 关闭

像这样的串联Channels的管道（Pipelines）可以⽤ 在需要⻓时间运⾏的服务中，每个⻓时间运⾏的goroutine可能会包含⼀个死循环，在不同goroutine的死循环内部使⽤ 串联的Channels来通信。但是，如果我们希望通过Channels只发送有限的数列该如何处理呢？

Channel还⽀持close操作，⽤于关闭channel，随后对基于该channel的任何发送操作都将导致panic异常。对⼀个已经 被close过的channel进⾏接收操作依然可以接受到之前已经成功发送的数据；如果channel中已经没有数据的话将产⽣ ⼀个零值的数据。
使⽤内置的close函数就可以关闭⼀个channel：

`close(ch)`

因为关闭操作只⽤于断⾔不再向channel发送新的数据，**所以只有在发送者所在的goroutine才会调⽤close函数，因此对 ⼀个只接收的channel调⽤close将是⼀个编译错误。**

当⼀个channel被关闭后，再向该channel发送数据将导致panic异常。

当⼀个被关闭的channel中已经发送的数据都被成 功接收后，后续的接收操作将不再阻塞，它们会⽴即返回⼀个零值。关闭上⾯例⼦中的naturals变量对应的channel并不 能终⽌循环，它依然会收到⼀个永⽆休⽌的零值序列，然后将它们发送给打印者goroutine。
没有办法直接测试⼀个channel是否被关闭，但是接收操作有⼀个变体形式：它多接收⼀个结果，多接收的第⼆个结果 是⼀个布尔值ok，ture表示成功从channels接收到值，false表示channels已经被关闭并且⾥⾯没有值可接收。使⽤这个 特性，我们可以修改squarer函数中的循环代码，当naturals对应的channel被关闭并没有值可接收时跳出循环，并且也 关闭squares对应的channel.

``` go
// Squarer
go func() {
    for {
        x, ok := <-naturals
        if !ok {
            break // naturals channel 被关闭
        }
        squares <- x * x
    }
    close(squares)
}
```

上⾯的语法是笨拙的，⽽且这种处理模式很常⻅，因此Go语⾔的range循环可直接在channels上⾯迭代。

使⽤ range循环是上⾯处理模式的简洁语法，它依次从channel接收数据，当channel被关闭并且没有值可接收时跳出循环:

``` go
//	Squarer
go func() {	
    for	x := range naturals	{													squares	<- x * x
    }
    close(squares)				
}()
//	Printer	(in	main goroutine)
for	x := range squares {
    fmt.Println(x)				
} 
```

其实你并不需要关闭每⼀个channel。只有当需要告诉接收者goroutine，所有的数据已经全部发送时才需要关闭 channel。不管⼀个channel是否被关闭，当它没有被引⽤时将会被Go语⾔的垃圾⾃动回收器回收。（**不要将关闭⼀个 打开⽂件的操作和关闭⼀个channel操作混淆。对于文件，在不使用的时候都要主动关闭。**）



### 单方向 channel

有的channel 本意只是用于发送（如squares）或接收，我们可以设置一个单方向的channel 用来防止误操作 ，比如发送到 squares.

为了表明这种意图并防⽌被滥⽤，Go语⾔的类型系统提供了单⽅向的channel类型，分别⽤于只发送或只接收的 channel。

**类型 `chan<- int` 表示⼀个只发送int的channel，只能发送不能接收。**

**相反，类型 ` <-chan int`表示⼀个只接收int 的channel，只能接收不能发送。**

（箭头	<-	和关键字chan的相对位置表明了channel的⽅向。）

改进版本：

``` go
func counter(out chan<- int) {
    for	x := 0;	x <	100; x++ {
        out	<-	x
    }
    close(out) 
}
func squarer(out chan<-	int, in	<-chan	int) {
    for	v := range in {
        out	<- v * v
    }				
    close(out) 
}
func printer(in	<-chan  int) {
    for	v:=	range in {
        fmt.Println(v)
    } 
}
func main()	{ 
    naturals := make(chan int)
    squares	:=	make(chan int)
    go counter(naturals)
    go squarer(squares,	naturals)
    printer(squares) 
}
```

调⽤counter（naturals）时，naturals的类型将隐式地从chan int转换成chan<- int。调⽤printer(squares)也会导致相似 的隐式转换，这⼀次是转换为	<-chan int	类型只接收型的channel。任何双向channel向单向channel变量的赋值操作都 将导致该隐式转换.

没有从单向channel 转换成双向channel 的语法



### 死锁

fatal error: all goroutines are asleep - deadlock!  这是使用channale容易遇到的问题。

看一段代码：

``` go
func testDeadLock(c chan int){
	for{
		fmt.Println(<-c)
	}
}

func main() {
	c :=make(chan int)
	c<-'A'
	go testDeadLock(c)  // 这句和上面 c<-'A' 对换也可解决这个问题
	time.Sleep(time.Millisecond)
}
```

我们开辟了一个无缓冲隧道 c, 当我们向 c 中写时，**会阻塞当前协程**，main函数本身是一个协程的执行，所以这里main被阻塞.

正确的写法时开另一个协程对其执行写操作：

``` go
func test(c chan int){
	c<-'A'
}

func testDeadLock(c chan int){
	for{
		fmt.Println(<-c)
	}
}

func main() {
	//chanDemo()
	c :=make(chan int)
	go test(c)
	go testDeadLock(c)
	time.Sleep(time.Millisecond)

}
```





## select

**elect就是用来监听和channel有关的IO操作，当 IO 操作发生时，触发相应的动作。**

select语句用来选择哪个case中的发送或接收操作可以被立即执行。它类似于switch语句，但是它的case涉及到channel有关的I/O操作。



### 基本用法

``` go
//select基本用法
select {
// 如果chan1成功读到数据，则进行该case处理语句
case <- chan1:
// 如果成功向chan2写入数据，则进行该case处理语句
case chan2 <- 1:
// 如果上面都没有成功，则进入default处理流程
default:
```

1. 每个case都必须是一个通信。
2. 在一个用于接收语句的case子句中，可以把接收语句的结果赋值给1个或2个变量，这里的赋值可以使用 简短变量声明的方式（:=），这里的接收表达式必须是一个接收操作（可以用圆括号括起来）。
3. 所有channel表达式都会被求值、所有被发送的表达式都会被求值。求值顺序：自上而下、从左到右.
    结果是选择一个发送或接收的channel，无论选择哪一个case进行操作，表达式都会被执行。
4. 如果有一个或多个IO操作可以完成，**则Go运行时系统会随机的选择一个执行**，如果有default分支，则执行default分支语句。
5. 没有case可以执行, 有default 执行default, 如果连default都没有，则select语句会一直阻塞，直到至少有一个IO操作可以进行.



### Default  和 阻塞

**如果有一个或多个IO操作可以完成，则Go运行时系统会随机的选择一个执行，否则的话，如果有default分支，则执行default分支语句，如果连default都没有，则select语句会一直阻塞，直到至少有一个IO操作可以进行**

``` go
start := time.Now()
c   := make(chan interface{})
ch1 := make(chan int)
ch2 := make(chan int)

go func() {
  time.Sleep(4*time.Second)
  close(c)
}()

go func() {
  time.Sleep(3*time.Second)
  ch1 <- 3
}()

go func() {
  time.Sleep(3*time.Second)
  ch2 <- 5
}()

fmt.Println("Blocking on read...")
select {
  case <- c:
  	fmt.Printf("Unblocked %v later.\n", time.Since(start))
  case <- ch1:
  	fmt.Printf("ch1 case...")
  case <- ch2:
  	fmt.Printf("ch1 case...")
  // 此时，会走 default, 其他的在睡眠中。
  default:
  	fmt.Printf("default go...")
}

output: ====
Blocking on read...
Unblocked 4.000612584s later.
Process finished with exit code 0
```

修改代码，将default注释:

```cpp
//default:
 //       fmt.Printf("default go...")
```

这时，select语句会阻塞，直到监测到一个可以执行的IO操作为止。这里，先会执行完睡眠3s的gorountine,此时两个channel都满足条件，这时系统会随机选择一个case继续操作。

```bash
Blocking on read...
ch2 case...
Process finished with exit code 0
```

接着，继续修改代码，将ch1的gorountine休眠时间改为5s,

此时会先执行到上面的gorountine，select执行的就是c的case。





### 表达式被求值

**所有channel表达式都会被求值、所有被发送的表达式都会被求值。求值顺序：自上而下、从左到右.**

``` go
var ch1 chan int // 信道只是 被声明，但没有被初始化，值为nil
var ch2 chan int
var chs = []chan int{ch1, ch2}
var numbers = []int{1, 2, 3, 4, 5}

func main () {
    select {
    case getChan(0) <- getNumber(2):
        fmt.Println("1th case is selected.")
    case getChan(1) <- getNumber(3):
        fmt.Println("2th case is selected.")
    default:
        fmt.Println("default!.")
    }
}

func getNumber(i int) int {
    fmt.Printf("numbers[%d]\n", i)
    return numbers[i]
}

func getChan(i int) chan int {
    fmt.Printf("chs[%d]\n", i)
    return chs[i]
}
```

此时，select语句走的是default操作(两个通道值为nil，没有走)。但是这时每个case的表达式都会被执行。以case1为例：

```bash
case getChan(0) <- getNumber(2):
```

系统会从左到右先执行getChan函数打印chs[0]，然后执行getNumber函数打印numbers[2]。同样，从上到下分别执行所有case的语句。所以，程序执行的结果为：

```css
chs[0]
numbers[2]
chs[1]
numbers[3]
default!.

Process finished with exit code 0
```



### break

**break关键字结束select**

```go
ch1 := make(chan int, 1)
ch2 := make(chan int, 1)

ch1 <- 3
ch2 <- 5

select {
  case <- ch1:
  fmt.Println("ch1 selected.")
  break

  fmt.Println("ch1 selected after break")
  case <- ch2:

  fmt.Println("ch2 selected.")
  fmt.Println("ch2 selected without break")
}
```

很明显，ch1和ch2两个通道都可以读取到值，所以系统会随机选择一个case执行。我们发现选择执行ch1的case时，由于有break关键字只执行了一句：

```bash
ch1 selected.

Process finished with exit code 0
```

但是，当系统选择ch2的case时，打印结果为：

```bash
ch2 selected.
ch2 selected without break

Process finished with exit code 0
```

如此就显而易见，break关键字在select中的作用,  **都可以执行时，走有break的case**

.
