---
title: "03-使用Protobuf序列化.md"
date: 2020-08-14 19:03:39 +0800
lastmod: 2020-08-14 12:28:55 +0800
draft: true
tags: ["go roc"]
categories: ["go"]
author: "Claymore"

---

## 使用 protobuf 序列化

新建项目my-protoc，初始化go mod: go mod init my-protoc.

建立文件夹 person, 在其中建立文件person.proto:

``` protobuf
syntax = "proto3";

package person;
option go_package = ".;person"; // 注意这里

message Person {
  string name = 1;
  int32 id = 2;  // Unique ID number for this person.
  string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    string number = 1;
    PhoneType type = 2;
  }

  repeated PhoneNumber phones = 4;
}

// Our address book file is just one of these.
message AddressBook {
  repeated Person people = 1;
}
```

这里包含的一些比较复杂的类型，如枚举 PhoneType, 嵌套message, 类型数组等。

生成person.pb.go:

``` sh
# go mod 下载 官方 protobuf包：
go get -v github.com/golang/protobuf/proto

cd person
protoc --go_out=. person.proto
```



main.go

``` go
package main

import (
	"fmt"
	"log"

	"github.com/golang/protobuf/proto"

	pb "my-protoc/person"
)

func main() {
	p := &pb.Person{
		Id:    1234,
		Name:  "claymore",
		Email: "https@claymore.com",
		Phones: []*pb.Person_PhoneNumber{
			{Number: "12345678", Type: pb.Person_HOME},
			{Number: "10101010", Type: pb.Person_WORK},
		},
	}

	// 编码
	out, err := proto.Marshal(p)
	if err != nil {
		log.Fatal("failed to marshal: ", err)
	}
	fmt.Println(out)


	// 解码
	p2 := &pb.Person{}
	if err := proto.Unmarshal(out, p2); err != nil {
		log.Fatal("failed to unmarshal: ", err)
	}

	fmt.Println(p2)
	fmt.Println(out)
	fmt.Println(string(out))
}
```

输出：

```
out=====: [10 8 99 108 97 121 109 111 114 101 16 210 9 26 18 104 116 116 112 115 64 99 108 97 121 109 111 114 101 46 99 111 109 34 12 10 8 49 50 51 52 53 54 55 56 16 1 34 12 10 8 49 48
49 48 49 48 49 48 16 2]
p2======: name:"claymore"  id:1234  email:"https@claymore.com"  phones:{number:"12345678"  type:HOME}  phones:{number:"10101010"  type:WORK}
out=====: [10 8 99 108 97 121 109 111 114 101 16 210 9 26 18 104 116 116 112 115 64 99 108 97 121 109 111 114 101 46 99 111 109 34 12 10 8 49 50 51 52 53 54 55 56 16 1 34 12 10 8 49 48
49 48 49 48 49 48 16 2]

claymore�     https@claymore.com"

12345678╔"

10101010╗


```



当前目录结构：

```
my-protoc
 person
    -- person.pb.go
    -- person.proto
 main.go
 go.mod
```

