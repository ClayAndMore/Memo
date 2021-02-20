---
title: "sync.md"
date: 2020-02-23 18:22:30 +0800
lastmod: 2020-02-23 18:22:30 +0800
draft: false
tags: ["go lib"]
categories: ["go"]
author: "Claymore"

---
### WaitGroup

先看下面一段代码：

``` go
package main

import (
  "fmt"
  "time"
)

func main (){
  for i := 0; i < 100 ; i++{
    go fmt.Println(i)
  }
    time.Sleep(time.Second)
}
```

主线程为了等待goroutine都运行完毕，不得不在程序的末尾使用`time.Sleep()` 来睡眠一段时间，等待其他线程充分运行。

对于简单的代码，100个for循环可以在1秒之内运行完毕，`time.Sleep()` 也可以达到想要的效果。但实际的大多数场景来说，1秒是不够的，并且大部分时候我们都无法预知for循环内代码运行时间的长短。这时候就不能使用`time.Sleep()` 来完成等待操作了。

可以使用管道来完成上述工作：

``` go
func main() {
    c := make(chan bool, 100)
    for i := 0; i < 100; i++ {
        go func(i int) {
            fmt.Println(i)
            c <- true
        }(i)
    }

    for i := 0; i < 100; i++ {
        <-c
    }
}
```

这里肯定能达到我们的目的，管道在这里显得大材小用，假设有一万个for循环，这里建立管道对内存也是不小的开销。

go语言中有一个其他的工具`sync.WaitGroup` 能更加方便的帮助我们达到这个目的。

`WaitGroup` 对象内部有一个计数器，最初从0开始，它有三个方法：`Add(), Done(), Wait()` 用来控制计数器的数量。

**`Add(n)` 把计数器设置为`n` ，`Done()` 每次把计数器`-1` ，`wait()` 会阻塞代码的运行，直到计数器地值减为0。**

所以对上方程序可以使用 WaitGroup来改进：

``` go
func main() {
    wg := sync.WaitGroup{}
    wg.Add(100)
    for i := 0; i < 100; i++ {
        go func(i int) {
            fmt.Println(i)
            wg.Done()
        }(i)
    }
    wg.Wait()
}
```



### 注意

我们不能使用`Add()` 给`wg` 设置一个负值，否则代码将会报错，同样使用`Done()` 也要特别注意不要把计数器设置成负数了。



### WaitGroup对象不是一个引用类型

``` go
func main() {
    wg := sync.WaitGroup{}
    wg.Add(100)
    for i := 0; i < 100; i++ {
        go f(i, &wg)
    }
    wg.Wait()
}

// 一定要通过指针传值，不然进程会进入死锁状态
func f(i int, wg *sync.WaitGroup) { 
    fmt.Println(i)
    wg.Done()
}
```

WaitGroup对象不是一个引用类型，在通过函数传值的时候需要使用地址



### Once



