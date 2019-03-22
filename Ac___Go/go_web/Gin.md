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

