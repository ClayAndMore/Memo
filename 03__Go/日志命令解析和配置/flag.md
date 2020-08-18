---
title: "flag.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: ["go lib", "go 日志命令解析和配置"]
categories: ["go"]
author: "Claymore"

---
在 go 标准库中提供了一个包：flag，方便进行命令行解析



### 常用方法


1.flag.Usage
输出使用方法，如linux下ls -h的帮助输出

2.flag.Type(参数名, 默认值, 使用提示)
Type为类型 支持整数（int、int64、uint、uint64）、浮点数（float64）、字符串（string）和时长（time.Duration）
调用相应的flag.Sring flag.Int flag.Uint方法，方法返回相应类型的指针

3.flag.TypeVar(指针, 参数名, 默认值, 使用提示)
与flag.Type方法基本相同，不同的是多一个指针参数，将使用传入的指针，不会再创建指针返回

4.flag.Args
返回解析完命令行参数后的其他参数，如./sh -name cqh  a1 a2，将返回a1 a2

5.flag.Parse
执行解析




```go
package main

import (
    "fmt"
    "flag"
)

func main() {
    name := flag.String("name", "user", "姓名")
    age  := flag.Int("age", 18, "年龄")
    var email string
    flag.StringVar(&email, "email", "test@test.com", "邮箱")

    flag.Parse()
    fmt.Println("name is ", *name)
    fmt.Println("age is ", *age)
    fmt.Println("email is ", email)
}
```

输出：

```sh
~/Documents/go/src/flag ./flag  # 默认输出默认值
name is  user
age is  18
~/Documents/go/src/flag ./flag -h  # 默认支持-h
package main
Usage of ./flag:
  -age int
    	年龄 (default 18)
  -email string
    	邮箱 (default "test@test.com")
  -name string
    	姓名 (default "user")
~/Documents/go/src/flag ./flag -age 33
name is  user
age is  33
~/Documents/go/src/flag ./flag --age 33 # 可见 - 和 --都是等效的
          
~/Documents/go/src/flag ./flag --age 33 -name tfboys -email "ggg@email.com"
name is  tfboys
age is  33
email is  ggg@email.com

# 返回其他参数
~/Documents/go/src/flag ./flag --age 33 -name tfboys -email "ggg@email.com" test1 test2 
name is  tfboys
age is  33
email is  ggg@email.com
args: [test1 test2]
```





### flag解析姿势

在所有的 flag 定义完成之后，可以通过调用 `flag.Parse()` 进行解析。

命令行 flag 的语法有如下三种形式：

```cpp
-flag // 只支持bool类型
-flag=x
-flag x // 只支持非bool类型
```

以上语法对于一个或两个‘－’号，效果是一样的。

bool 类型可以和其他类型一样处理，其次 bool 类型支持 `-flag` 这种形式，因为Parse()中，对 bool 类型进行了特殊处理。默认的，提供了 `-flag`，则对应的值为 true ，否则为 `flag.Bool/BoolVar` 中指定的默认值；如果希望显示设置为 false 则使用 `-flag=false`。

对于第三种情况，只能用于非 bool 类型的 flag。 原因是：如果支持，那么对于这样的命令 cmd -x *，如果有一个文件名字是：0或false等，则命令的原意会改变。

int 类型可以是十进制、十六进制、八进制甚至是负数；bool 类型可以是1, 0, t, f, true, false, TRUE, FALSE, True, False。Duration 可以接受任何 time.ParseDuration 能解析的类型。

- 注：如果bool类型的参数在命令行中用了`-flag false`这种形式时，其后的参数都会被当做非flag（non-flag）参数，non-flag 参数后面解释



### 长短选项

我们知道如果指定参数v，它会支持-v和--v，但是如果想支持-v和--version怎么办？

一个 `Flag` 应该有长短两种形式，但 flag 包并不支持这种风格

```go
flag.BoolVar(&v, "v", false, "print the version")
flag.BoolVar(&v, "version", false, "print the version")
```

定义了两个 `Flag`，同时绑定到了一个变量上。这种效果只能用 `flag.BoolVar` 方式定义新的 `Flag`，`flag.Bool` 没办法做到将同一个变量同时绑定两个 `Flag`。





### 自定义flag

只要实现flag.Value接口即可:

```go
type Value interface {
  String() string
  Set(string) error
}

//自定义解析参数，实现Set和String方法
type Hello string
 
func (p *Hello) Set(s string) error {
    v := fmt.Sprintf("Hello %v", s)
    *p = Hello(v)
    return nil
}
 
func (p *Hello) String() string {
    return fmt.Sprintf("%f", *p)
}

var hello Hello
		flag.Var(&hello, "hello", "hello参数")

 fmt.Println("hello:", hello)
```

