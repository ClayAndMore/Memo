
---
title: "testing 和 测试.md"
date: 2020-02-10 14:02:16 +0800
lastmod: 2020-02-10 14:02:16 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## Testing

Go 语言中的 testing 系统包。

它要求我们：

* 以 `*_test.go` 新建文件
* 在文件中以 `TestXxx` 命名函数， Test 后第一个不能是小写字母
* 然后再通过 `go test [flags] [packages]` 执行函数。

eg: demo_test.go:

``` go
package gotest

import "testing"

func Fib(n int)  int {
	if n < 2 {
		return n
	}
	return Fib(n-1) + Fib(n-2)
}

func TestFib(t *testing.T) {
	var (
		in = 7
		expected = 13
	)
	actual := Fib(in)
	if actual != expected {
		t.Errorf("Fib(%d) = %d; expected %d", in, actual, expected)
	}
}
```

命令行执行go test demo_test.go:

```
~/Documents/go/src/gotest go test demo_test.go 
ok      command-line-arguments  0.006s
```



它也为我们提供了三种类型的函数：

``` go
TestXxxx(t testing.T) // 基本测试用例 
BenchmarkXxxx(b testing.B) // 压力测试的测试用例， 也称之为基准测试
Example_Xxx() // 测试控制台输出的例子， 示例函数，
TestMain(m *testing.M) // 测试 Main 函数
```





### TestXxx Testing.T 

基本函数测试，其基本签名是：

```go
func TestName(t *testing.T){
    // ...
}
```

类型 testing.T 有以下方法：

``` go
// 打印日志。对于测试，会在失败或指定 -test.v 标志时打印。对与基准测试，总是打印，避免因未指定 -test.v 带来的测试不准确
func (c *T) Log(args ...interface{})
func (c *T) Logf(format string, args ...interface{})


// 标记函数失败，继续执行该函数
func (c *T) Fail()
// 标记函数失败，调用 runtime.Goexit 退出该函数。但继续执行其它函数或基准测试。
func (c *T) FailNow()
// 返回函数是否失败
func (c *T) Failed() bool


// 等同于 t.Log + t.Fail
func (c *T) Error(args ...interface{})
// 等同于 t.Logf + t.Fail
func (c *T) Errorf(format string, args ...interface{})


// 等同于 t.Log + t.FailNow
func (c *T) Fatal(args ...interface{})
// 等同于 t.Logf + t.FailNow
func (c *T) Fatalf(format string, args ...interface{})


// 将调用函数标记标记为测试助手函数。
func (c *T) Helper()

// 返回正在运行的测试或基准测试的名称
func (c *T) Name() string

// 用于表示当前测试只会与其他带有 Parallel 方法的测试并行进行测试。
func (t *T) Parallel()

// 执行名字为 name 的子测试 f，并报告 f 在执行过程中是否失败
// Run 会阻塞到 f 的所有并行测试执行完毕。
func (t *T) Run(name string, f func(t *T)) bool


// 相当于 t.Log + t. SkipNow
func (c *T) Skip(args ...interface{})
// 将测试标记为跳过，并调用 runtime.Goexit 退出该测试。继续执行其它测试或基准测试
func (c *T) SkipNow()
// 相当于 t.Logf + t.SkipNow
func (c *T) Skipf(format string, args ...interface{})
// 报告该测试是否是忽略
func (c *T) Skipped() bool
```

上面斐波那契的例子，如果我们需要验证很多结果，我们可以使用Table-Driven 的方式写测试，标准库中有很多测试是使用这种方式写的。

``` go
func TestFib(t *testing.T) {
    var fibTests = []struct {
        in       int // input
        expected int // expected result
    }{
        {1, 1},
        {2, 1},
        {3, 2},
        {4, 3},
        {5, 5},
        {6, 8},
        {7, 13},
    }

    for _, tt := range fibTests {
        actual := Fib(tt.in)
        if actual != tt.expected {
          // Errorf 在失败时步骤终止执行
            t.Errorf("Fib(%d) = %d; expected %d", tt.in, actual, tt.expected)
        }
    }
}
```





### Bechmark testing.B

基准测试, 可以进行性能测试其基本签名是：

```go
func BenchmarkName(b *testing.B){
    // ...
}
```

测试函数的名字必须以 `Benchmark` 开头，可选的后缀名必须不以小写字母开头，一般跟我们测试的函数名。

还是上方的那个样例，我们再添加一个函数：

``` go
func BenchmarkFib10(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Fib(10)
	}
}
```

执行：

```sh
~/Documents/go/src/gotest go test -bench=. gotest  
.
1 total assertion

goos: darwin
goarch: amd64
pkg: gotest
BenchmarkFib10-4         3243240               366 ns/op
PASS
ok      gotest  1.569s

```

运行了 3243240 次，平均运行一次的时间是 366ns。

在性能测试函数多的时候 使用 -bench 指定具体函数，如本例： `go test -bench=Fib10 gotest`

待补充





### Example 测试

示例函数可以帮助我们写一个示例，并与输出相比较， example_test.go:

``` go
package gotest

import "fmt"

func ExampleHello() {
	fmt.Println("hello")
	// Output: hello
}

func ExampleSalutations() {
	fmt.Println("hello, and")
	fmt.Println("goodbye")
	// Output:
	// hello, and
	// goodbye
}

// 无序输出 Unordered output
func ExamplePerm() {
	p := [...]int{4,2,1,3,0}
	for _, value := range p {
		fmt.Println(value)
	}
	// Unordered output: 4
	// 2
	// 1
	// 3
	// 0
}
```

执行 go test example_test.go   :  ` go test example_test.go`

一些规则：

- 函数的签名需要以 `Example` 开头
- 输出的对比有有序（Output）和无序（Unordered output）两种
- **如果函数没有输出注释，将不会被执行**

可见 它是一种基于控制台的测试，感觉用处不大。

官方给我们的命名的规则是：

``` go
// 一个包的 example
func Example() { ... }
// 一个函数 F 的 example
func ExampleF() { ... }
// 一个类型 T 的 example
func ExampleT() { ... }
// 一个类型 T 的方法 M 的 example
func ExampleT_M() { ... }

// 如果以上四种类型需要提供多个示例，可以通过添加后缀的方式
// 后缀必须小写
func Example_suffix() { ... }
func ExampleF_suffix() { ... }
func ExampleT_suffix() { ... }
func ExampleT_M_suffix() { ... }
```



### 子测试

待补充





###  Main 测试

有时候我们也需要从主函数开始进行测试：

```go
func TestMain(m *testing.M)

例：
func TestMain(m *testing.M) {
    // call flag.Parse() here if TestMain uses flags
    os.Exit(m.Run())
}
```