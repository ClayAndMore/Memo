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