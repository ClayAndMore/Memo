
---
title: "fmt.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "fmt.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
### 简单使用



### print

```go
// Print 将参数列表 a 中的各个参数转换为字符串并写入到标准输出中。
// 非字符串参数之间会添加空格，返回写入的字节数。
func Print(a ...interface{}) (n int, err error)

// Println 功能类似 Print，只不过最后会添加一个换行符。
// 所有参数之间会添加空格，返回写入的字节数。
func Println(a ...interface{}) (n int, err error)

// Printf 将参数列表 a 填写到格式字符串 format 的占位符中。
// 填写后的结果写入到标准输出中，返回写入的字节数。
func Printf(format string, a ...interface{}) (n int, err error)
```

eg:

```go
    fmt.Print("a", "b", 1, 2, 3, "c", "d", "\n")
    fmt.Println("a", "b", 1, 2, 3, "c", "d")
    fmt.Printf("ab %d %d %d cd\n", 1, 2, 3)
//out:
ab1 2 3cd
a b 1 2 3 c d
ab 1 2 3 cd
```





#### printf 的格式化

```go
package main

import "fmt"
import "os"

type point struct {
	x, y int
}

func main() {

	// Go提供了几种打印格式，用来格式化一般的Go值，例如
	// 下面的%v打印了一个point结构体的对象的值
	p := point{1, 2}
  //
}
```

结构体和其他：

| 占位符 | 语句                           | 解释                                                         | 输出                 |
| ------ | ------------------------------ | ------------------------------------------------------------ | -------------------- |
| %v     | fmt.Printf("%v\n", p)          | %v打印了一个point结构体的对象的值                            | {1 2}                |
| %+v    | fmt.Printf("%+v\n", p)         | 如果所格式化的值是一个结构体对象，那么`%+v`的格式化输出将包括结构体的成员名称和值 | {x:1 y:2}            |
| %#v    | fmt.Printf("%#v\n", p)         | `%#v`格式化输出将输出一个值的Go语法表示方式。                | main.point{x:1, y:2} |
| %T     | fmt.Printf("%T\n", p)          | 使用`%T`来输出一个值的数据类型                               | main.point           |
| %t     | fmt.Printf("%t\n", true)       | 格式化布尔型变量                                             | true                 |
| %%     | 字面上的百分号，并非值的占位符 | Printf("%%")                                                 | %                    |
| %p     | Printf("%p", &p)               | 十六进制表示，前缀 0x                                        | 0x4f57f0             |

**常用%#v, 比起 %+v 有时更能输出结构体的字段和值**

格式化整型：

| 占位符 | 说明                                       | 举例                 | 输出   |
| ------ | ------------------------------------------ | -------------------- | ------ |
| %b     | 二进制表示                                 | Printf("%b", 5)      | 101    |
| %c     | 相应Unicode码点所表示的字符                | Printf("%c", 0x4E2D) | 中     |
| %d     | 十进制表示                                 | Printf("%d", 0x12)   | 18     |
| %o     | 八进制表示                                 | Printf("%d", 10)     | 12     |
| %q     | 单引号围绕的字符字面值，由Go语法安全地转义 | Printf("%q", 0x4E2D) | '中'   |
| %x     | 十六进制表示，字母形式为小写 a-f           | Printf("%x", 13)     | d      |
| %X     | 十六进制表示，字母形式为大写 A-F           | Printf("%x", 13)     | D      |
| %U     | Unicode格式，相当于 "%04X" 加上前导 "U+"   | Printf("%U", 0x4E2D) | U+4E2D |

**浮点数和复数**：

| 占位符 | 说明                                                  | 举例                   | 输出         |
| ------ | ----------------------------------------------------- | ---------------------- | ------------ |
| %e     | 科学计数法，例如 -1234.456e+78                        | Printf("%e", 10.2)     | 1.020000e+01 |
| %E     | 科学计数法，例如 -1234.456E+78                        | Printf("%e", 10.2)     | 1.020000E+01 |
| %f     | 有小数点而无指数，例如 123.456                        | Printf("%f", 10.2)     | 10.200000    |
| %g     | 根据情况选择 %e 或 %f 以产生更紧凑的（无末尾的0）输出 | Printf("%g", 10.20)    | 10.2         |
| %G     | 根据情况选择 %E 或 %f 以产生更紧凑的（无末尾的0）输出 | Printf("%G", 10.20+2i) | (10.2+2i)    |



控制宽度和精度：

```go
// 当输出数字的时候，经常需要去控制输出的宽度和精度。
// 可以使用一个位于%后面的数字来控制输出的宽度，默认
// 情况下输出是右对齐的，左边加上空格
fmt.Printf("|%6d|%6d|\n", 12, 345)

// 你也可以指定浮点数的输出宽度，同时你还可以指定浮点数的输出精度
fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45)

// To left-justify, use the `-` flag. 左对齐
fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45)

// 你也可以指定输出字符串的宽度来保证它们输出对齐。默认情况下，输出是右对齐的
fmt.Printf("|%6s|%6s|\n", "foo", "b")

// 为了使用左对齐你可以在宽度之前加上`-`号
fmt.Printf("|%-6s|%-6s|\n", "foo", "b")

// 输出
|    12|   345|
|  1.20|  3.45|
|1.20  |3.45  |
|   foo|     b|
|foo   |b     |
```

使用非空格控制宽度：

```go
func main() {
    fmt.Printf("%4d\n", 1)
    fmt.Printf("%4d\n", 10)
    fmt.Printf("%4d\n", 100)
    fmt.Printf("%4d\n", 1000)
    fmt.Printf("%4d\n", 10000)  // 这个会超出宽度
}

/* 输出结果
$ go run main.go
   1
  10
 100
1000
10000
*/

// 默认使用空格填充，也可以指定填充的内容，比如使用0填充，在输出二进制数的时候非常有用：
func main() {
    fmt.Printf("%04b\n", 1)
    fmt.Printf("%04b\n", 2)
    fmt.Printf("%04b\n", 3)
    fmt.Printf("%04b\n", 4)
    fmt.Printf("%04b\n", 666)  // 这个会超出宽度
}

/* 输出结果
$ go run main.go
0001
0010
0011
0100
1010011010
*/
```





#### 其他print函数

```go
// 功能同上面三个函数，只不过将转换结果写入到 w 中。
func Fprint(w io.Writer, a ...interface{}) (n int, err error)
func Fprintln(w io.Writer, a ...interface{}) (n int, err error)
func Fprintf(w io.Writer, format string, a ...interface{}) (n int, err error)

// 功能同上面三个函数，只不过将转换结果以字符串形式返回。
func Sprint(a ...interface{}) string
func Sprintln(a ...interface{}) string
func Sprintf(format string, a ...interface{}) string

// 功能同 Sprintf，只不过结果字符串被包装成了 error 类型。
func Errorf(format string, a ...interface{}) error
```

eg:

```go
if err := percent(30, 70, 90, 160); err != nil {
		fmt.Println(err)
	}
	// 30%
	// 70%
	// 90%
	// 数值 160 超出范围（100）

func percent(i ...int) error {
	for _, n := range i {
		if n > 100 {
			return fmt.Errorf("数值 %d 超出范围（100）", n)
		}
		fmt.Print(n, "%\n")
	}
	return nil
}
```



其他：https://blog.51cto.com/steed/2380418



### scan



待整理： https://www.cnblogs.com/golove/p/3286303.html





### Sprintf

接口类型转成字符串：

``` go
package main

import "fmt"

func main() {

    mapInterface := make(map[interface{}]interface{})   
    mapString := make(map[string]string)

    mapInterface["k1"] = 1
    mapInterface[3] = "hello"
    mapInterface["world"] = 1.05

    for key, value := range mapInterface {
        strKey := fmt.Sprintf("%v", key)
        strValue := fmt.Sprintf("%v", value)
        mapString[strKey] = strValue
    }

    fmt.Printf("%#v", mapString)
```

