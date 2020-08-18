---
title: "02-Protobuf 数据格式和语法.md"
date: 2020-08-15 19:03:39 +0800
lastmod: 2020-08-15 12:28:55 +0800
draft: true
tags: ["go roc"]
categories: ["go"]
author: "Claymore"

---

## 数据格式

ProtoBuf的数据结构都是通过`.proto`文件进行定义的，然后再通过ProtoBuf工具生成相应平台语言的类库，这样就可以被我们使用了。

eg: example.proto

``` protobuf
syntax = "proto3";
message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}
```

* 第一行指定protobuf的版本，这里是以`proto3`格式定义。可以指定为`proto2`。如果没有指定，默认以`proto2`格式定义。
* 第二行定义了一个message类型，声明为 SearchRequest
* 定义字段`query`, 首先是它的类型`string`，其次是字段的名称，然后是等号`=`, 之后是字段的编号，然后是分号。

其他：

* 使用// 和 /* ... */ 来注释
* 命名规范： Message采用驼峰式命名方式，字段命名采用小写字母加下划线隔离方式。



### 字段类型

所有的字段需要前置声明数据类型，上面的示例指定了两个数值类型和一个字符串类型。看下基本类型和编程语言的对应关系：

| \.proto Type | Notes                                                        | Python Type\[2\] | Go Type  |
| ------------ | ------------------------------------------------------------ | ---------------- | -------- |
| double       |                                                              | float            | float64  |
| float        |                                                              | float            | float32  |
| int32        | 使用可变长度编码。编码负数的效率低 \- 如果您的字段可能有负值，请改用sint32。 | int              | int32    |
| int64        | 使用可变长度编码。编码负数的效率低 \- 如果您的字段可能有负值，请改用sint64。 | int/long\[3\]    | int64    |
| uint32       | 使用可变长度编码                                             | int/long         | uint32   |
| uint64       | 使用可变长度编码\.                                           | int/long         | uint64   |
| sint32       | 使用可变长度编码。签名的int值。这些比常规int32更有效地编码负数。 | int              | int32    |
| sint64       | 使用可变长度编码。签名的int值。这些比常规int64更有效地编码负数。 | int/long         | int64    |
| fixed32      | 总是四个字节。如果值通常大于228，则比uint32更有效。          | int/long         | uint32   |
| fixed64      | 总是八个字节。如果值通常大于256，则比uint64更有效            | int/long\[3\]    | uint64   |
| sfixed32     | 总是四个字节                                                 | int              | int32    |
| sfixed64     | 总是八个字节                                                 | int/long         | int64    |
| bool         |                                                              | bool             | bool     |
| string       | 字符串必须始终包含UTF\-8编码或7位ASCII文本，且不能超过232。  | str/unicode      | string   |
| bytes        | 可以包含不超过232的任意字节序列。                            | str              | \[\]byte |



### 默认值

- 对于字符串，默认值为空字符串。
- 对于字节，默认值为空字节。
- 对于bools，默认值为false。
- 对于数字类型，默认值为零。
- 对于枚举，默认值是第一个定义的枚举值，该值必须为0。
- 对于消息字段，未设置该字段。它的确切值取决于语言。



### 字段编号

在message定义中每个字段都有一个唯一的编号，这些编号被用来在二进制消息体中识别你定义的这些字段，一旦你的message类型被用到后就不应该在修改这些编号了。注意在将message编码成二进制消息体时字段编号1-15将会占用1个字节，16-2047将占用两个字节。所以在一些频繁使用用的message中，你应该总是先使用前面1-15字段编号。

你可以指定的最小编号是1，最大是2E29 - 1（536,870,911）。其中19000到19999是给protocol buffers实现保留的字段标号，定义message时不能使用。同样的你也不能重复使用任何当前message定义里已经使用过和预留的字段编号。

保留字段：

当你删掉或者注释掉message中的一个字段时，未来其他开发者在更新message定义时就可以重用之前的字段编号。如果他们意外载入了老版本的`.proto`文件将会导致严重的问题，比如数据损坏、隐私泄露等。一种避免问题发生的方式是指定保留的字段编号和字段名称。如果未来有人用了这些字段标识那么在编译时protocol buffer的编译器会报错。

```go
message Foo {
  reserved 2, 15, 9 to 11;
  reserved "foo", "bar";
}
```

只要在更新后的消息类型中不再重用字段编号，就可以删除该字段。你也可以重命名字段，比如说添加`OBSOLETE_`前缀或者将字段编号设置为`reserved`，这些未来其他用户就不会意外地重用该字段编号了。

**Reserved可以用来指明此message不使用某些字段，也就是忽略这些字段。**

可以通过字段编号范围或者字段名称指定保留的字段,如上面的9 to 11.



### 使用其他Message类型 和 repeated

可以使用其他message类型作为字段的类型，假设你想在每个`SearchResponse`消息中携带类型为`Result`的消息，

你可以在同一个`.proto`文件中定义一个`Result`消息类型，然后在`SearchResponse`中指定一个`Result`类型的字段。

```go
message SearchResponse {
  repeated Result results = 1;
}

message Result {
  string url = 1;
  string title = 2;
  repeated string snippets = 3;
}
```

**repeated：标识字段可以重复任意次，这样就声明了它的类型数组**



### 嵌套Message

消息类型可以被定义和使用在其他消息类型中，下面的例子里`Result`消息被定义在`SearchResponse`消息中

```go
message SearchResponse {
  message Result {
    string url = 1;
    string title = 2;
    repeated string snippets = 3;
  }
  repeated Result results = 1;
}
```

如果你想在外部使用定义在父消息中的子消息，使用`Parent.Type`引用他们

```go
message SomeOtherMessage {
  SearchResponse.Result result = 1;
}
```

你可以嵌套任意多层消息

```go
message Outer {                  // Level 0
  message MiddleAA {  // Level 1
    message Inner {   // Level 2
      int64 ival = 1;
      bool  booly = 2;
    }
  }
  message MiddleBB {  // Level 1
    message Inner {   // Level 2
      int32 ival = 1;
      bool  booly = 2;
    }
  }
}
```





### package 

你可以在`.proto`文件中添加一个可选的`package`符来防止消息类型之前的名称冲突。

```protobuf
package foo.bar;
message Open { ... }
```

在定义message的字段时像如下这样使用package名称

```protobuf
message Foo {
  ...
  foo.bar.Open open = 1;
  ...
}
```

package符对生成代码的影响视编程语言而定



在没有为特定语言定义`option xxx_package`的时候，它还可以用来生成特定语言的包名，比如Java package, go package。

Go 中：默认使用package名作为包名，除非指定了 option go_package选项



### 导入其他 proto 文件

可以使用import 语句导入使用其他描述文件中声明的类型：

```
import "others.proto"
```



protocol buffer编译器会在` -I / --proto_path` 参数指定的目录中查找导入的文件，如果没有指定该参数，默认在当前目录中查找。



### 枚举类型

在定义消息类型时，您可能希望其中一个字段只有一个预定义的值列表中的值。例如，假设您要为每个`SearchRequest`添加`corpus`字段，其中`corpus`可以是UNIVERSAL，WEB，IMAGES，LOCAL，NEWS，PRODUCTS或VIDEO。您可以非常简单地通过向消息定义添加枚举，并为每个可能的枚举值值添加常量来实现。

在下面的例子中，我们添加了一个名为`Corpus`的枚举类型，和一个`Corpus`类型的字段：

```protobuf
message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
  enum Corpus {
    UNIVERSAL = 0;
    WEB = 1;
    IMAGES = 2;
    LOCAL = 3;
    NEWS = 4;
    PRODUCTS = 5;
    VIDEO = 6;
  }
  Corpus corpus = 4;
}
```

如你所见，`Corpus`枚举的第一个常量映射到了0：所有枚举定义都需要包含一个常量映射到0并且作为定义的首行，这是因为：

- 必须有0值，这样我们就可以将0作为枚举的默认值。
- proto2语法中首行的枚举值总是默认值，为了兼容0值必须作为定义的首行。



### map类型

proto3支持map类型

``` protobuf
// 格式
<key_type, value_type> map_field = N;

message Project {...}
map<string, Project> projects = 1;
```

* 键、值类型可以是内置的标量类型，也可以是自定义message类型
* 字段不支持repeated属性
* 不要依赖map类型的字段顺序



### 选项 Options

在定义.proto文件时可以标注一系列的options。Options并不改变整个文件声明的含义，但却可以影响特定环境下处理方式。

option的定义格式是`"option" optionName "=" constant ";"`

可以使用 go_package 指定后的包名

```go
package person;
option go_package = ".;person"; 
//,; 代表当前路径，实际上我是在包person下执行的protoc --go_out=. person.proto，
// 希望生成同级下的person.pb.go
```





### 定义服务 Service 

如果想消息类型与RPC（远程过程调用）系统一起使用，你可以在`.proto`文件中定义一个RPC服务接口，然后protocol buffer编译器将会根据你选择的编程语言生成服务接口代码，加入你要定义一个服务，它的一个方法接受`SearchRequest`消息返回`SearchResponse`消息，你可以在`.proto`文件中像如下示例这样定义它：

```protobuf
service SearchService {
  rpc Search (SearchRequest) returns (SearchResponse);
}
```

与protocol buffer 一起使用的最简单的RPC系统是`gRPC`：一种由Google开发的语言和平台中立的开源RPC系统。 `gRPC`特别适用于protocol buffer，并允许您使用特殊的protocol buffer编译器插件直接从`.proto`文件生成相关的RPC代码。

**生成的接口代码作为客户端与服务端的约定，服务端必须实现定义的所有接口方法，客户端直接调用同名方法向服务端发起请求。比较蛋疼的是即便业务上不需要参数也必须指定一个请求消息，一般会定义一个空message。** 如：

``` protobuf
service ReaderService {
    rpc read(Request) returns Response {}
}

service WriterService {
    rpc read(HelloWorld) returns Response {}
}
```

