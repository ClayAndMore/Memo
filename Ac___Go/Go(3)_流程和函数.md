## 流程和函数

### 流程控制

#### if

Go里面`if`条件判断语句中不需要括号，如下代码所示

```go
if x > 10 {
	fmt.Println("x is greater than 10")
} else {
	fmt.Println("x is less than 10")
}
```

Go的`if`还有一个强大的地方就是条件判断语句里面允许声明一个变量，这个变量的作用域只能在该条件逻辑块内，其他地方就不起作用了，如下所示

```go
// 计算获取值x,然后根据x返回的大小，判断是否大于10。
if x := computedValue(); x > 10 {
	fmt.Println("x is greater than 10")
} else {
	fmt.Println("x is less than 10")
}

//这个地方如果这样调用就编译出错了，因为x是条件里面的变量
fmt.Println(x)
```

多个条件的时候如下所示：

```go
if integer == 3 {
	fmt.Println("The integer is equal to 3")
} else if integer < 3 {
	fmt.Println("The integer is less than 3")
} else {
	fmt.Println("The integer is greater than 3")
}
```



#### goto





#### for

格式：

```go
for expression1; expression2; expression3 {
	//...
}
```

```go
package main

import "fmt"

func main(){
	sum := 0;
	for index:=0; index < 10 ; index++ {
		sum += index
	}
	fmt.Println("sum is equal to ", sum)
}
// 输出：sum is equal to 45
```

有些时候需要进行多个赋值操作，由于Go里面没有`,`操作符，那么可以使用平行赋值`i, j = i+1, j-1`

有些时候如果我们忽略`expression1`和`expression3`：

```go
sum := 1
for ; sum < 1000;  {
	sum += sum
}
```

其中`;`也可以省略，那么就变成如下的代码了，是不是似曾相识？对，这就是`while`的功能。

```go
sum := 1
for sum < 1000 {
	sum += sum
}
```







### 函数

**Go是编译型语言，所以函数编写的顺序是无关紧要的；**

* 当函数执行到代码块最后一行（`}` 之前）或者 `return` 语句的时候会退出，其中 `return` 语句可以带有零个或多个参数

* 除了main()、init()函数外，其它所有类型的函数都可以有参数与返回值。函数参数、返回值以及它们的类型被统称为函数签名。

* 大括号有要求：

  这样是不正确的 Go 代码：

  ```
  func g()
  {
  }
  ```

  它必须是这样的：

  ```
  func g() {
  }
  ```

* 函数调用基本格式：`pack1.Function(arg1, arg2, …, argn)`

