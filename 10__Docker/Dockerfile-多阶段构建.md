Docker在17.05之后就能支持多阶构建了，为了使镜像更加小巧，我们采用多阶构建的方式来打包镜像。在多阶构建出现之前我们通常使用一个Dockerfile或多个Dockerfile来构建镜像。



### 单文件构建

单文件就是将所有的构建过程（包括项目的依赖、编译、测试、打包过程）全部包含在一个Dockerfile中之下：

例如，编写 `app.go` 文件，该程序输出 `Hello World!`

```go
package main  

import "fmt"  

func main(){  
    fmt.Printf("Hello World!");
}
```

编写 Dockerfile.one 文件:

```dockerfile
FROM golang:1.9-alpine
RUN apk --no-cache add git ca-certificates
WORKDIR /go/src/github.com/go/helloworld/

COPY app.go .

RUN go get -d -v github.com/go-sql-driver/mysql \
  && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app . \
  && cp /go/src/github.com/go/helloworld/app /root

WORKDIR /root/
CMD ["./app"]
```




