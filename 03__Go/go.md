
---
title: "go.md"
date: 2020-01-10 19:03:39 +0800
lastmod: 2020-02-08 12:28:55 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
代理：https://goproxy.io/



教程：https://books.studygolang.com/gopl-zh/ch0/ch0-01.html



获取变量类型： 

`fmt.Println(reflect.TypeOf(var)) `



### 关于 ide 无法识别 go 包的问题

**代码应该放在`GOPATH`的 src 目录**

我在非 GOPATH 目录中的某项目 用 ide 打开，出现无法识别包的现象，想用项目vendor目录里面的，而不是现下。

go编译时，优先从项目源码树根目录下的vendor目录查找代码（可以理解为切换了一次`GOPATH`），如果`vendor`中有，则不再去GOPATH中找。

先关掉 go mod: **直接使用go env -w GO111MODULE=off**， 然后在设置里添加项目的GOPATH, 所以把项目目录的路径填入，注意此时应该**在该目录建立src, 把项目放到src中**， 重新起动 goland, 或者用如下方式：

go ide : goland

在intellij idea下打开go项目，经常出现cannot resolve file等问题。

解决办法：在~/.bash_profile配置GOPATH，配置为当前project目录，然后重新启动Intellij Idea。

若仍然显示红色（无法索引），那么点File下invalid cache/restart即可
