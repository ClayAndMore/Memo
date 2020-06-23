
---
title: "Beego.md"
date: 2019-10-10 17:44:20 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "Beego.md"
date: 2019-10-10 17:44:20 +0800
lastmod: 2019-10-10 17:44:20 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


中文文档：https://beego.me/docs/intro/







### bee 工具

https://beego.me/docs/install/bee.md

**bee new 项目名**， 创建一个web项目

```
root@10.250.123.xx beego # go get github.com/beego/bee
root@10.250.123.xx beego # bee new first_beego
______
| ___ \
| |_/ /  ___   ___
| ___ \ / _ \ / _ \
| |_/ /|  __/|  __/
\____/  \___| \___| v1.10.0
2019/10/09 17:33:28 INFO     ▶ 0001 Creating application...
        create   /disk/go_workspace/src/beego/first_beego/
....
        create   /disk/go_workspace/src/beego/first_beego/main.go
2019/10/09 17:33:28 SUCCESS  ▶ 0002 New application successfully created!
```

目录结构：

```
first_beego
├── conf
│   └── app.conf
├── controllers
│   └── default.go
├── main.go
├── models
├── routers
│   └── router.go
├── static
│   ├── css
│   ├── img
│   └── js
├── tests
│   └── default_test.go
└── views
    └── index.tpl

8 directories, 4 files

```



**bee api 项目名**， 创建一个api项目

```

root@10.250.123.10 beego # bee api api_beego
______
| ___ \
| |_/ /  ___   ___
| ___ \ / _ \ / _ \
| |_/ /|  __/|  __/
\____/  \___| \___| v1.10.0
2019/10/09 17:44:37 INFO     ▶ 0001 Creating API...
        create   /disk/go_workspace/src/beego/api_beego
...
        create   /disk/go_workspace/src/beego/api_beego/main.go
2019/10/09 17:44:37 SUCCESS  ▶ 0002 New API successfully created!
```

目录结构：

```
api_beego/
├── conf
│   └── app.conf
├── controllers
│   ├── object.go
│   └── user.go
├── main.go
├── models
│   ├── object.go
│   └── user.go
├── routers
│   └── router.go
└── tests
    └── default_test.go

5 directories, 8 files
```

