
---
title: "docker 安全.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
### gosu

gosu是个工具，用来提升指定账号的权限，作用与sudo命令类似，而docker中使用gosu的起源来自安全问题；

docker容器中运行的进程，如果以root身份运行的会有安全隐患，该进程拥有容器内的全部权限，更可怕的是如果有数据卷映射到宿主机，那么通过该容器就能操作宿主机的文件夹了，一旦该容器的进程有漏洞被外部利用后果是很严重的。
https://github.com/tianon/gosu 