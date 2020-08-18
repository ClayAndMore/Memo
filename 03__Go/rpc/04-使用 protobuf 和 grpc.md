---
title: "04-使用Protobuf 和 grpc.md"
date: 2020-08-14 19:03:39 +0800
lastmod: 2020-08-14 12:28:55 +0800
draft: true
tags: ["go roc"]
categories: ["go"]
author: "Claymore"

---

## 使用 protobuf 和 grpc

新建项目my-protoc，初始化go mod: go mod init my-protoc.

下载库：

```
go get -u -v github.com/golang/protobuf/proto
go get -u -v github.com/golang/protobuf/protoc-gen-go
go get -u -v google.golang.org/grpc
```

最终目录结构：

```
my-protoc
  server.go
  client.go
  helloworld
  -- helloworld.pb.go
  -- helloworld.proto
```





新建文件夹 helloworld, 新建文件 helloworld.proto:

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

生成pb.go

```sh
protoc --go_out=plugins=grpc:. helloworld/helloworld.proto
# 在目录my-protoc下
# 在helloworld.proto里没有指定go_package
# 指定了 go_out 插件 grpc, 冒号后跟的是当前路径
```



### 服务端

server.go

``` go
package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	pb "my-protoc/helloworld"
)

const port = ":50051"

//server 用于实现从proto 服务定义生成的 helloworld.GreeterServer接口.
type server struct {}

// SayHello 实现 helloworld.GreeterServer接口.
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "hello " + in.Name}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	//创建gRPC 服务器，将我们实现的Greeter服务绑定到一个端口
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to server: %v", err)
	}
}
```



### 客户端

``` go
package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	pb "my-protoc/helloworld"
)

const (
	address     = "localhost:50051"
	defaultName = "你好 ！"
)

func main() {
	//创建一个gRPC频道，指定连接的主机名和服务器端口
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewGreeterClient(conn)

	name := defaultName

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	r, err := c.SayHello(ctx, &pb.HelloRequest{Name: name})

	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	log.Printf("Greeting %s", r.Message)
}
```



### 运行

```sh
# 一个终端运行：
go run server.go

# 领一个终端运行
go run client.go
2020/08/12 18:01:06 Greeting hello 你好 ！

```





构建带鉴权和认证的 gPRC:https://blog.didiyun.com/index.php/2018/12/12/grpc-golang-1/