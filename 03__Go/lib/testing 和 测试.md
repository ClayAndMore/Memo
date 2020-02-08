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



它也为我们提供了三种类型的函数：测试函数 T、基准测试函数 B、实例函数 Example。



### Test esting.T 

函数测试，其基本签名是：

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



### Bechmark testing.B

基准测试,其基本签名是：

```go
func BenchmarkName(b *testing.B){
    // ...
}
```

测试函数的名字必须以 `Benchmark` 开头，可选的后缀名必须不以小写字母开头，一般跟我们测试的函数名。