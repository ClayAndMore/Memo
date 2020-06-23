
---
title: "Gin.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "Gin.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
https://github.com/gin-gonic/gin

中文文档：https://gin-gonic.com/zh-cn/docs/



### hello,world

hello.go:

```go
package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
    r.Run(":8080") // listen and serve on 0.0.0.0:8080
}
```

go run hello.go:

```
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /ping                     --> main.main.func1 (3 handlers)
[GIN-debug] Listening and serving HTTP on :8080
[GIN] 2019/03/22 - 18:13:22 | 404 |       1.393µs |  222.128.62.114 | GET      /
[GIN] 2019/03/22 - 18:13:23 | 404 |       2.339µs |  222.128.62.124 | GET      /favicon.ico
[GIN] 2019/03/22 - 18:13:33 | 200 |      90.329µs |  222.128.62.124 | GET      /ping

```

`response: {"message":"Hello World"}`



### 路由





#### 请求方式

```go
router.GET("/someGet", getting)
router.POST("/somePost", posting)
router.PUT("/somePut", putting)
router.DELETE("/someDelete", deleting)
router.PATCH("/somePatch", patching)
router.HEAD("/someHead", head)
router.OPTIONS("/someOptions", options)
```



#### 获取路由参数





#### 获取url查询参数





#### 路由组

```go
	router := gin.Default()

	// Simple group: v1
	v1 := router.Group("/v1")
	{
		v1.POST("/login", loginEndpoint)
		v1.POST("/submit", submitEndpoint)
		v1.POST("/read", readEndpoint)
	}

	// Simple group: v2
	v2 := router.Group("/v2")
	{
		v2.POST("/login", loginEndpoint)
		v2.POST("/submit", submitEndpoint)
		v2.POST("/read", readEndpoint)
	}
```

这样则需访问/v1/login, /v2.logi



#### 使用中间件

