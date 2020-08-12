## Protobuf

### 序列化和Protobuf

序列化(serialization、marshalling)的过程是指将数据结构或者对象的状态转换成可以存储(比如文件、内存)或者传输的格式(比如网络)。

反向操作就是反序列化(deserialization、unmarshalling)的过程。

我们熟知的序列化编码方式有：XML, JSON, YAML等等。



Protobuf是Protocol Buffers的简称，Protobuf可以用于结构化数据串行化，或者说序列化。它的设计非常适用于在网络通讯中的数据载体，很适合做数据存储或 RPC 数据交换格式，它序列化出来的数据量少再加上以 K-V 的方式来存储数据，对消息的版本兼容性非常强，可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式



和 Json相比：

跟Json相比protobuf性能更高，更加规范

- 编解码速度快，数据体积小
- 使用统一的规范，不用再担心大小写不同导致解析失败等蛋疼的问题了

但也失去了一些便利性

- 改动协议字段，需要重新生成文件。
- 数据没有可读性



### 来源

2001年初，Protobuf首先在Google内部创建， 我们把它称之为 `proto1`，一直以来在Google的内部使用，其中也不断的演化，根据使用者的需求也添加很多新的功能，一些内部库依赖它。几乎每个Google的开发者都会使用到它。

Google开始开源它的内部项目时，因为依赖的关系，所以他们决定首先把Protobuf开源出去。 proto1在演化的过程中有些混乱，所以Protobuf的开发者重写了Protobuf的实现，保留了proto1的大部分设计，以及proto1的很多的想法。但是开源的proto2不依赖任何的Google的库，代码也相当的清晰。2008年7月7日，Protobuf开始公布出来。

Protobuf公布出来也得到了大家的广泛的关注， 逐步地也得到了大家的认可，很多项目也采用Protobuf进行消息的通讯，还有基于Protobuf的微服务框架GRPC。在使用的过程中，大家也提出了很多的意见和建议，Protobuf也在演化，于2016年推出了Proto3。 Proto3简化了proto2的开发，提高了开发的效能，但是也带来了版本不兼容的问题。

https://github.com/protocolbuffers/protobuf



### 数据格式







## 代码生成

要生成Java，Python，C ++，Go..代码，你需要使用`.proto`文件中定义的消息类型，你需要在`.proto`上运行protocol buffer编译器`protoc`



### 安装

首先，你要安装`protoc`编译器，通过这个https://github.com/protocolbuffers/protobuf/releases地址下载，选择适合自己操作系统的版本。下载后要把二进制`protoc`放在自己的`$PATH/bin`目录中，确保可以在终端执行。

或者直接用go get:

```
go get -u github.com/golang/protobuf/proto
```

因为ProtoBuf本身不支持GO语言，所以我们还得安装一个生成Golang代码的插件。安装方式也非常简单，通过如下代码即可：

```
go get -u github.com/golang/protobuf/protoc-gen-go
```



### 编译结果

<ul>
<li>C++: 每个<code>.proto</code>文件生成一个<code>.h</code>文件和一个<code>.cc</code>文件，每个消息类型对应一个类</li>
<li>Java: 生成一个<code>.java</code>文件，同样每个消息对应一个类，同时还有一个特殊的<code>Builder</code>类用于创建消息接口</li>
<li>Python: 姿势不太一样，每个<code>.proto</code>文件中的消息类型生成一个含有静态描述符的模块，该模块与一个元类<em>metaclass</em>在运行时创建需要的Python数据访问类</li>
<li>Go: 生成一个<code>.pb.go</code>文件，每个消息类型对应一个结构体</li>



### 使用

```
protoc --proto_path=IMPORT_PATH --cpp_out=DST_DIR --java_out=DST_DIR --python_out=DST_DIR --go_out=DST_DIR --ruby_out=DST_DIR --objc_out=DST_DIR --csharp_out=DST_DIR path/to/file.proto
```

--proto_path, `-I` 是它的简短形式， 指定protoc的搜索import的proto的文件夹，如果忽略将在当前工作目录进行查找，可以通过传递多次`--proto-path`参数来指定多个import目录

--go_out 指定生成的代码文件路径

eg: ` protoc -I=$SRC_DIR --go_out=$DST_DIR $SRC_DIR/addressbook.proto`

--go_out 后面可以跟其他参数,

- plugins 指定插件
- M 指定.proto 文件编译后对应的 golang 包名
- import_prefix 为所有 import 路径添加前缀
- import_path 指定未声明 package 或 go_package 的文件的包名，最右面的斜线前的字符会被忽略



eg: 

```
protoc -I ./protos ./protos/helloworld.proto --go_out=plugins=grpc:helloworld
```





###  编译路径

helloworld.proto:

``` protobuf
syntax = "proto3";
 
option go_package = "github.com/grpc/example/helloworld";
 
package helloworld;
 
service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

编译 .proto 文件：

``` sh
$ protoc helloworld.proto --go_out=output
$ tree .
.
├── helloworld.proto
└── output
    └── github.com
        └── grpc
            └── example
                └── helloworld
                    └── helloworld.pb.go
5 directories, 2 files
```

注意：

**-go_out 和 go_package 组合起来会影响生成的go代码位置。**



### gogo 版本

除了上方的 go get github.com/golang/protobuf/proto 官方版本，还可以安装 gogo 版本，其中有 `protoc-gen-gogo` 和 `protoc-gen-gofast` 两个插件可用，后者生成的代码更加复杂，但是性能也更高 (快5~7倍)。

```
----- 安装两个插件
$ go get github.com/gogo/protobuf/protoc-gen-gogo
$ go get github.com/gogo/protobuf/protoc-gen-gofast
----- 安装库文件(可选)
$ go get github.com/gogo/protobuf/gogoproto
```

最后是使用上述的插件生成编译后的 go 文件。

```
$ protoc --go_out=. *.proto
$ protoc --gogo_out=. *.proto
$ protoc --gofast_out=. *.proto
```