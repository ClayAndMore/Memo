---
title: "go build.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
## go build



### -ldflags

go build 可以用 `-gcflags` 给*go*编译器传入参数，也就是传给go tool compile的参数，因此可以用go tool compile --help查看所有可用的参数。