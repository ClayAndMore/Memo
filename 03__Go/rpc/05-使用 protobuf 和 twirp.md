## Twirp

twirp 是一个基于 Google Protobuf 的 RPC 框架。`twirp`通过在`.proto`文件中定义服务，然后自动生产服务器和客户端的代码。让我们可以将更多的精力放在业务逻辑上。

咦？这不就是 gRPC 吗？不同的是，**gRPC 自己实现了一套 HTTP 服务器和网络传输层，twirp 使用标准库`net/http`**。另外 gRPC 只支持 HTTP/2 协议，twirp 还可以运行在 HTTP 1.1 之上。同时 twirp 还可以使用 JSON 格式交互。

https://github.com/twitchtv/twirp



### 使用

``` sh
#  前提安装：
go get -u -v github.com/golang/protobuf/proto
go get -u -v github.com/golang/protobuf/protoc-gen-go
 
# twirp:
go get -u -v github.com/twitchtv/twirp/protoc-gen-twirp
```



新建 文件夹 helloworld, 新建文件 helloworld.proto:

``` protobuf
syntax = "proto3";

package helloworld;
// 定义 Greeter 服务
service Greeter{
  //发送一个greeter
  rpc SayHello (HelloRequest) returns (HelloReply){}
}

message HelloRequest{
  string name = 1;
}

message HelloReply{
  string message = 1;
}
```

调用 

```
protoc --twirp_out=. --go_out=. helloworld/helloworld.proto
```

生成了 helloworld.pb.go 和 helloworld.proto



### server

server.go:

``` go
package main

import (
	"context"
	"my-protoc/twirp/helloworld"
	"net/http"
)

type Server struct{}

func (s *Server) SayHello(ctx context.Context, request *helloworld.HelloRequest) (*helloworld.HelloReply, error) {
	return &helloworld.HelloReply{Message: request.GetName()}, nil
}

func main() {
	server := &Server{}
	twripHandler := helloworld.NewGreeterServer(server, nil)

	http.ListenAndServe(":8080", twripHandler)
}
```



### client

client.go

``` go
package main

import (
	"context"
	"fmt"
	"my-protoc/twirp/helloworld"
	"net/http"
)

func main() {
	client := helloworld.NewGreeterProtobufClient("http://localhost:8080", &http.Client{})

	response, err := client.SayHello(context.Background(), &helloworld.HelloRequest{Name: "你好,世界！"})
	if err != nil {
		fmt.Println("err: ", err)
	}
	fmt.Println("response: ", response.GetMessage())
}
```



两个终端分别执行 go run server, go run client.go:

```
go run client.go
response:  你好,世界！
```



目录结构：

```
my-protoc
  twrip
    helloworld
       helloworld.pb.go
       helloworld.proto
       hellwoorld.twirp.go
    client.go
    server.go
```

