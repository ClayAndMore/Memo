---
title: "os.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-01-16 18:29:52 +0800
draft: false
tags: ["go lib"]
categories: ["go"]
author: "Claymore"

---


os	包以跨平台的⽅式，提供了⼀些与操作系统交互的函数和变量。程序的命令⾏参数可从os包的Args变量获取；os包 外部使⽤os.Args访问该变量。

os.Args变量是⼀个字符串（string）的切⽚（slice）

os.Args的第⼀个元素：os.Args[0]，是命令本身的名字

``` go
package main

import (
    "fmt"
    "os"
)

func main() {
    var s, sep string
    for i :=1; i < len(os.Args); i++ {
        s += sep + os.Args[i]
        sep = " "
    }

    fmt.Println(s)
}

// 输出

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go de 111
de 111

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go de 111 你好
de 111 你好
```



#### 获取系统变量

导入”os”包通过os包中的Getenv方法来获取

`func Getenv（key string） string {}`


示例代码：

```go
package main

import "fmt"
import "os"

func main(){
    var JAVAHOME string
    JAVAHOME = os.Getenv("JAVA_HOME")
    fmt.Println(JAVAHOME)
}
```