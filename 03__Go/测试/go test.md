---
title: "go test.md"
date: 2020-02-10 14:02:16 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: ["go test"]
categories: ["go"]
author: "Claymore"

---
go test 是 go 语言自带的测试工具, 



格式和参数：

`go` `test [-c] [-i] [build flags] [packages] [flags ``for` `test binary]`

``` 
-c : 编译 go test 成为可执行的二进制文件，但是不运行测试。
-i : 安装测试包依赖的 package，但是不运行测试。

关于 build flags，调用 go help build，这些是编译运行过程中需要使用到的参数，一般设置为空
关于 packages，调用 go help packages，这些是关于包的管理，一般设置为空
关于 flags for test binary，调用 go help testflag，这些是 go test 过程中经常使用到的参数：

-test.v : 是否输出全部的单元测试用例（不管成功或者失败），默认没有加上，所以只输出失败的单元测试用例
-test.run pattern : 只跑哪些单元测试用例
-test.bench patten : 只跑那些性能测试用例
-test.benchmem : 是否在性能测试的时候输出内存情况
-test.benchtime t : 性能测试运行的时间，默认是1s
-test.cpuprofile cpu.out : 是否输出cpu性能分析文件
-test.memprofile mem.out : 是否输出内存性能分析文件
-test.blockprofile block.out : 是否输出内部goroutine阻塞的性能分析文件
-test.memprofilerate n : 内存性能分析的时候有一个分配了多少的时候才打点记录的问题。这个参数就是设置打点的内存分配间隔，也就是 profile 中一个 sample 代表的内存大小。默认是设置为 512 * 1024 的。如果你将它设置为 1，则每分配一个内存块就会在 profile 中有个打点，那么生成的 profile 的 sample 就会非常多。如果你设置为 0，那就是不做打点了

你可以通过设置 memprofilerate=1 和 GOGC=off 来关闭内存回收，并且对每个内存块的分配进行观察

-test.blockprofilerate n : 基本同上，控制的是 goroutine 阻塞时候打点的纳秒数。默认不设置就相当于 -test.blockprofilerate=1，每一纳秒都打点记录一下

-test.parallel n : 性能测试的程序并行 cpu 数，默认等于 GOMAXPROCS
-test.timeout t : 如果测试用例运行时间超过 t，则抛出 panic
-test.cpu 1,2,4 : 程序运行在哪些 CPU 上面，使用二进制的 1 所在位代表，和 nginx nginx_worker_cpu_affinity 是一个道理
-test.short : 将那些运行时间较长的测试用例运行时间缩短

```

规则：

**测试代码文件要命名为： xx_test.go**

**测试函数要以 TestXxx 的形式命名**



### 运行

运行整个项目测试文件: go test

单个测试文件： go test xx_test.go

**在运行测试文件时，常常遇到不到源码函数的错误， 因为 即使你的测试文件和源码同一个包，测试文件中可以使用源码里的函数， 但是在go test 运行时，也要加上源码。**

所以我们需要将源码文件与测试文件关联一起运行：

```
go test two_sum_test.go two_sum.go
```

因为 go test 默认将**文件编译成一个临时执行文件，函数只能在这个临时文件中寻找**。

运行详细结果，可以加上`-v`参数：

```
$ go test -v two_sum_test.go two_sum.go
```

 运行结果：

``` 
=== RUN   TestTwoSum
--- PASS: TestTwoSum (0.00s)
        two_sum_test.go:6: [0 1]
PASS
ok      command-line-arguments  0.006s
```



**注意，如果使用vendor，记得加上-mod=vendor ,因为test也是需要编译的**



### -run 测试某个函数

参数`-run`对应一个正则表达式，只有测试函数名被它正确匹配的测试函数才会被`go test`测试命令运行：

```
 go test -v -run="TestTwo"
 
===
=== RUN   TestTwoSum
--- PASS: TestTwoSum (0.00s)
        two_sum_test.go:6: [0 1]
PASS
ok      leetcode        0.006s
```

其他写法：

``` 
测试单个函数：$ go test -v hello_test.go -test.run TestHello
$ go test -v hello_test.go -run TestHello
```





### 其他参数

### test 二进制文件

生成test二进制文件：go test -c， 会在当前目录下生成 **包名.test 二进制**文件

生成指定二进制文件：

`go test -v -o leetcode.test `



#### 用于go build 的参数

`go test` 还可以从主题中分离出来生成独立的测试二进制文件，因为`go test`命令中包含了编译动作，所以它可以接受可用于`go build`命令的所有参数。

| -c   | 生成用于运行测试的可执行文件，但不执行它。这个可执行文件会被命名为“pkg.test”，其中的“pkg”即为被测试代码包的导入路径的最后一个元素的名称。 |
| ---- | ------------------------------------------------------------ |
| -i   | 安装/重新安装运行测试所需的依赖包，但不编译和运行测试代码。  |
| -o   | 指定用于运行测试的可执行文件的名称。追加该标记不会影响测试代码的运行，除非同时追加了标记`-c`或`-i`。 |