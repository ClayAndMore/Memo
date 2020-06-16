---
title: "goconvey.md"
date: 2020-02-10 14:02:16 +0800
lastmod: 2020-02-10 14:02:16 +0800
draft: false
tags: ["go test", "go lib"]
categories: ["go test"]
author: "Claymore"

---
## goconvey

是一款针对Golang的测试框架，可以管理和运行测试用例，同时提供了丰富的断言函数，并支持很多 Web 界面特性。

GoConvey 网站 : http://smartystreets.github.io/goconvey/

GoConvey 是个相当不错的 Go 测试工具，支持 go test。可直接在终端窗口和浏览器上使用。

特点：

- 直接与 go test 集成
- 巨大的回归测试套件
- 可读性强的色彩控制台输出
- 完全自动化的 Web UI
- 测试代码生成器
- 桌面提醒（可选）
- 自动在终端中运行自动测试脚本



### 安装

在命令行运行下面的命令：

```
go get github.com/smartystreets/goconvey
```

运行时间较长，运行完后你会发现：

1. 在$GOPATH/src目录下新增了github.com子目录，该子目录里包含了GoConvey框架的库代码
2. 在$GOPATH/bin目录下新增了GoConvey框架的可执行程序goconvey， 这里我试点时候并没有，没有下载成功，网络问题。



### 使用

``` go
package goconvey

import "errors"

func Add(a, b int) int {
    return a + b
}

func Subtract(a, b int) int {
    return a - b
}

func Multiply(a, b int) int {
    return a * b
}

func Division(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("被除数不能为 0")
    }
    return a / b, nil
}
```

这 4 个函数分别书写单元测试：

``` go
package goconvey

import (
    "testing"
    . "github.com/smartystreets/goconvey/convey" 
  // 前面加点号"."，以减少冗余的代码 
  // 凡是在测试代码中看到Convey和So两个方法，肯定是convey包的，不要在产品代码中定义相同的函数名
)

func TestAdd(t *testing.T) {
    Convey("将两数相加", t, func() {
        So(Add(1, 2), ShouldEqual, 3)
    })
}

func TestSubtract(t *testing.T) {
    Convey("将两数相减", t, func() {
        So(Subtract(1, 2), ShouldEqual, -1)
    })
}

func TestMultiply(t *testing.T) {
    Convey("将两数相乘", t, func() {
        So(Multiply(3, 2), ShouldEqual, 6)
    })
}

func TestDivision(t *testing.T) {
    Convey("将两数相除", t, func() {

        Convey("除以非 0 数", func() {
            num, err := Division(10, 2)
            So(err, ShouldBeNil)
            So(num, ShouldEqual, 5)
        })

        Convey("除以 0", func() {
            _, err := Division(10, 0)
            So(err, ShouldNotBeNil)
        })
    })
}
```

**每个测试用例需要使用 `Convey` 函数包裹起来。它接受的第一个参数为 string 类型的描述；第二个参数一般为 `*testing.T`，即本例中的变量 t；第三个参数为不接收任何参数也不返回任何值的函数（习惯以闭包的形式书写）。**

`Convey` 语句同样可以无限嵌套，以体现各个测试用例之间的关系，例如 `TestDivision` 函数就采用了嵌套的方式体现它们之间的关系。需要注意的是，**只有最外层的 `Convey` 需要传入变量 t，内层的嵌套均不需要传入。**



#### So 断言

最后，需要使用 `So` 语句来对条件进行判断。在本例中，我们只使用了 3 个不同类型的条件判断：

* `ShouldEqual` 值应该相等
* `ShouldBeNil`和 `ShouldNotBeNil`，分别表示值应该为 nil、和值不应该为 nil。

所有的 断言类型： https://github.com/smartystreets/goconvey/wiki/Assertions



#### Skip

针对想忽略但又不想删掉或注释掉某些断言操作，GoConvey提供了Convey/So的Skip方法：

- SkipConvey函数表明相应的闭包函数将不被执行
- SkipSo函数表明相应的断言将不被执行

当存在SkipConvey或SkipSo时，测试日志中会显式打上"skipped"形式的标记：

- 当测试代码中存在SkipConvey时，相应闭包函数中不管是否为SkipSo，都将被忽略，测试日志中对应的符号仅为一个"⚠"
- 当测试代码Convey语句中存在SkipSo时，测试日志中每个So对应一个"✔"或"✘"，每个SkipSo对应一个"⚠"，按实际顺序排列
- 不管存在SkipConvey还是SkipSo时，测试日志中都有字符串"{n} total assertions (one or more sections skipped)"，其中{n}表示测试中实际已运行的断言语句数



#### web ui

想要使用 GoConvey 的 Web 界面特性，需要在相应目录下执行 `goconvey`（需使用 `go get` 安装到 `$GOPATH/bin` 目录下），然后打开浏览器，访问 [http://localhost:8080](http://localhost:8080/)