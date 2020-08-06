---
title: "Context.md"
date: 2020-02-10 14:02:16 +0800
lastmod: 2020-03-17 15:10:43 +0800
draft: false
tags: ["go lib"]
categories: ["go"]
author: "Claymore"

---
golang在1.6.2的时候还没有自己的context，在1.7的版本中就把golang.org/x/net/context包被加入到了官方的库中。**golang 的 Context包，是专门用来简化对于处理单个请求的多个goroutine之间与请求域的数据、取消信号、截止时间等相关操作，这些操作可能涉及多个 API 调用。**

比如有一个网络请求Request，每个Request都需要开启一个goroutine做一些事情，这些goroutine又可能会开启其他的goroutine。这样的话， 我们就可以通过Context，来跟踪这些goroutine，并且通过Context来控制他们的目的，这就是Go语言为我们提供的Context，**中文可以称之为“上下文”**

另外一个实际例子是，**在Go服务器程序中，每个请求都会有一个goroutine去处理。然而，处理程序往往还需要创建额外的goroutine去访问后端资源，比如数据库、RPC服务等。**由于这些goroutine都是在处理同一个请求，所以它们往往需要访问一些共享的资源，比如用户身份信息、认证token、请求截止时间等。而且如果请求超时或者被取消后，所有的goroutine都应该马上退出并且释放相关的资源。这种情况也需要用Context来为我们取消掉所有goroutine.



### Context 定义：

context 包的核心是 struct Context，声明如下：

``` go
type Context interface {
    // Deadline returns the time when work done on behalf of this context
    // should be canceled. Deadline returns ok==false when no deadline is set.
    Deadline() (deadline time.Time, ok bool)
    // Done returns a channel that's closed when work done on behalf of this
    // context should be canceled.
    Done() <-chan struct{}
    // Err returns a non-nil error value after Done is closed.
    Err() error
    // Value returns the value associated with this context for key.
    Value(key interface{}) interface{}
}
```

* Deadline方法是获取设置的截止时间的意思，第一个返回式是截止时间，到了这个时间点，Context会自动发起取消请求；第二个返回值ok==false时表示没有设置截止时间，如果需要取消的话，需要调用取消函数进行取消。

* `Done`会返回一个只读的channel，类型为struct{}，当该context被取消的时候，该channel会被关闭，同时对应的使用该context的routine也应该结束并返回。

  我们在goroutine中，如果该方法返回的chan可以读取，则意味着parent context已经发起了取消请求，我们通过Done方法收到这个信号后，就应该做清理操作，然后退出goroutine，释放资源。之后，Err 方法会返回一个错误，告知为什么 Context 被取消。

* Err方法返回取消的错误原因，因为什么Context被取消。
* `Value`方法获取该Context上绑定的值，是一个键值对，所以要通过一个Key才可以获取对应的值可以让routine共享一些数据，当然获得数据是协程安全的。



### emptyCtx

context.go 的168行定义了一个不可取消，没有设置截止时间，没有携带任何值的Context。

```go
type emptyCtx int

func (*emptyCtx) Deadline() (deadline time.Time, ok bool) {
	return
}

func (*emptyCtx) Done() <-chan struct{} {
	return nil
}

func (*emptyCtx) Err() error {
	return nil
}

func (*emptyCtx) Value(key interface{}) interface{} {
	return nil
}
```



### Context 的实现方法

Context 虽然是个接口，但是并不需要使用方实现，**golang内置的context 包，已经帮我们实现了2个方法，一般在代码中，开始上下文的时候都是以这两个作为最顶层的parent context，然后再衍生出子context。**这些 Context 对象形成一棵树：当一个 Context 对象被取消时，继承自它的所有 Context 都会被取消。两个实现如下：

Context.go 文件 的 196行：

``` go
var (
	background = new(emptyCtx)
	todo = new(emptyCtx)
)

func Background() Context {
	return background
}

func TODO() Context {
	return todo
}
```

一个是Background，主要用于main函数、初始化以及测试代码中，作为Context这个树结构的最顶层的Context，也就是根Context，它不能被取消。

一个是TODO，如果我们不知道该使用什么Context的时候，可以使用这个，但是实际应用中，暂时还没有使用过这个TODO。

他们两个本质上都是emptyCtx结构体类型，是一个不可取消，没有设置截止时间，没有携带任何值的Context。





### 所有方法

这是context.go 系统文件里的所有方法

``` go
func Background() Context
func TODO() Context

func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
func WithValue(parent Context, key, val interface{}) Context
```



#### withCancel

context.WithCancel生成了一个withCancel的实例以及一个cancelFuc，这个函数就是用来关闭ctxWithCancel中的 Done channel 函数。

``` go
// WithCancel returns a copy of parent whose Done channel is closed as soon as
// parent.Done is closed or cancel is called.
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
```

WithCancel返回一个继承的Context,这个Context在父Context的Done被关闭时关闭自己的Done通道，或者在自己被Cancel的时候关闭自己的Done。
 WithCancel同时还返回一个取消函数cancel，这个cancel用于取消当前的Context。

Eg:

``` go
package main

import (
	"context"
	"fmt"
	"time"
)

func Handler(){
	ctx, cancel := context.WithCancel(context.Background())
	go work(ctx)

	time.Sleep(5 * time.Second)
	cancel()
}

func work(ctx context.Context){
	for {
		time.Sleep(1 * time.Second)
		select {
		case <-ctx.Done():
			fmt.Println("done") // 这个怎么不会打印？
			return
		default:
			fmt.Println("work")
		}

	}
}

func main() {
	fmt.Println("start ...")
	Handler()
	fmt.Println("finish")
}
```

执行结果：

```
start ...
work
work
work
work
finish
```



#### WithTimeout 和 WithDeadline

根据上方代码，添加一handler:

``` go
func timeoutHandler() {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	//ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(3*time.Second))
	go work(ctx)
	
	time.Sleep(5 * time.Second)
	cancel()
}
```

在main中配置 timeoutHander, 执行，输出:

```
start ...
work
work
done
finish
```

这次的done为啥又输出了。。

**WithTimeout 等价于 WithDeadline(parent, time.Now().Add(timeout)).**

可以在子协程中判断当前context是否设置了时间，是否过期：

``` go
func doTimeOutWork(ctx context.Context) {
	for {
		time.Sleep(1 * time.Second)
		
		if deadline, ok := ctx.Deadline(); ok { //是否设置了deadline
			fmt.Println("deadline set")
			if time.Now().After(deadline) { // 是否过期
				fmt.Println(ctx.Err().Error())
				return
			}

		}

		select {
		case <-ctx.Done():
			fmt.Println("done")
			return
		default:
			fmt.Println("work")
		}
	}
}
```

输出：

```
start ...
deadline set
work
deadline set
work
deadline set
context deadline exceeded
finish
```





#### 使用 context.WithValue 传值

``` go
package main

import (
	"context"
	"fmt"
	"time"
)

func watch(ctx context.Context) {
	for{
		time.Sleep(1 * time.Second)
		select {
		case <-ctx.Done():
			fmt.Println(ctx.Value("key"), "is cancel") // 没有输出
		default:
			fmt.Println(ctx.Value("key"))
		}
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	valueCtx := context.WithValue(ctx, "key", "add value")
	go watch(valueCtx)
	time.Sleep(5 * time.Second)
	cancel()
}
```

输出：

```
add value
add value
add value
add value
```

