---
title: "nats.md"
date: 2021-02-29 17:53:13 +0800
lastmod: 2021-02-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["队列"]
author: "Claymore"

---

## 写在前面

官网：
https://nats.io/
文档：
https://docs.nats.io/
NATS 服务端源码：
https://github.com/nats-io/nats-server
NATS Go客户端源码：
https://github.com/nats-io/nats.go



NATS是一个开源的、轻量级、高性能的，支持发布、订阅机制的分布式消息队列系统， **实际上就是一个分布式的消息队列系统，支持PubSub/ReqRsp 模型**

它的核心基于EventMachine（EventMachine 其实是一个使用 Ruby 实现的事件驱动的并行框架）开发，代码量不多，可以下载下来慢慢研究。其核心原理就是基于消息发布订阅机制。每个台服务器上的每个模块会根据自己的消息类别，向MessageBus发布多个消息主题；而同时也向自己需要交互的模块，按照需要的信息内容的消息主题订阅消息。 NATS原来是使用Ruby编写，可以实现每秒150k消息，后来使用Go语言重写，能够达到每秒8-11百万个消息，整个程序很小只有3M Docker image，它不支持持久化消息，如果你离线，你就不能获得消息。



## 搭建

### 搭建服务

https://nats.io/download/nats-io/nats-server/ 这里下载二进制或者官方镜像，我们使用官方镜像：

``` sh
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name nats-server -ti nats:latest
[1] 2021/03/05 05:49:19.379200 [INF] Starting nats-server version 2.1.9
[1] 2021/03/05 05:49:19.379272 [INF] Git commit [7c76626]
[1] 2021/03/05 05:49:19.379516 [INF] Starting http monitor on 0.0.0.0:8222
[1] 2021/03/05 05:49:19.379768 [INF] Listening for client connections on 0.0.0.0:4222
[1] 2021/03/05 05:49:19.379784 [INF] Server id is NBHVAU3RDSS3MVTRSZWJ2T3M7CQAXEIYYAAVX2OK6ULTKWAVSAKH6IS5
[1] 2021/03/05 05:49:19.379791 [INF] Server is ready
[1] 2021/03/05 05:49:19.380119 [INF] Listening for route connections on 0.0.0.0:6222

```

默认使用三个端口：

- 4222 is for clients. 用于客户端连接
- 8222 is an HTTP management port for information reporting.  浏览器等可以访问的端口
- 6222 is a routing port for clustering.  集群模式下使用的端口

一般只开放 4222 就可以了。

## 



### 搭建nats集群

https://docs.nats.io/nats-server/nats_docker



## 发布订阅

NATS 监听某个主题的订阅者将接收关于该主题发布的消息。

如果订阅者没有积极地收听主题，则不会收到该消息。

订阅者可以使用通配符标记(如*和>)来匹配单个标记或匹配主题的尾部。

![](https://gblobscdn.gitbook.com/assets%2F-LqMYcZML1bsXrN3Ezg0%2F-LqMZac7AGFpQY7ewbGi%2F-LqMZgSl7CBR9-ZIe5Jh%2Fpubsubtut.svg?alt=media)

``` sh
# 克隆样例：
clone https://github.com/nats-io/nats.go.git
cd $GOPATH/src/github.com/nats-io/nats.go/examples
# 运行订阅者样例：
go run nats-sub/main.go mgs.test
# 运行发布者样例：
go run nats-pub/main.go msg.test hello
```

默认使用本地4222端口，实际使用时可指定远端nats server:

``` sh
E:\gitCompany\src\github.com\nats-io\nats.go>go run examples/nats-sub/main.go -s 10.8.2.202:4222 msg.test
Listening on [msg.test]
[#1] Received on [msg.test]: 'hello'
[#2] Received on [msg.test]: 'hello222'
```





## 请求响应模式 Request/Reply

请求-答复（响应）是现代分布式系统中的常见模式。 发送一个请求，应用程序要么等待某个超时的响应，要么异步接收响应。

![](https://gblobscdn.gitbook.com/assets%2F-LqMYcZML1bsXrN3Ezg0%2F-LqMZac7AGFpQY7ewbGi%2F-LqMZgh0PE7kV9Q2l3BV%2Freqrepl.svg?alt=media)

其原理也是使用订阅发布，只是订阅者接收到消息会给发布者一个回复。



先启动响应服务：

``` sh
E:\gitCompany\src\github.com\nats-io\nats.go>go run examples/nats-rply/main.go -s 10.8.2.202:4222 help.please "OK, I CAN HELP"
Listening on [help.please]

```

再启动请求服务：

``` sh
E:\gitCompany\src\github.com\nats-io\nats.go>go run examples/nats-req/main.go -s 10.8.2.202:4222 help.please "who can help me"
Published [help.please] : 'who can help me'
Received  [_INBOX.l40KLcEGN5JXfb8vEcr0bE.OpyR3f7i] : 'OK, I CAN HELP'

```

可以看到请求后会收到答复， 当然响应端也会收到 "who can help me "的消息。



## 队列

nat支持通过队列组实现负载均衡。订阅者注册队列组名。将随机选择组中的单个订阅者来接收消息。

![](https://gblobscdn.gitbook.com/assets%2F-LqMYcZML1bsXrN3Ezg0%2F-LqMZac7AGFpQY7ewbGi%2F-LqMZeqHRi1BPHIRKAMs%2Fqueue.svg?alt=media)

对同一主题，起三个队列订阅者，起两个普通订阅者：

``` sh
go run examples/nats-qsub/main.go -s 10.8.2.202:4222 foo my-queue
 Listening on [foo], queue group [my-queue]
go run examples/nats-qsub/main.go -s 10.8.2.202:4222 foo my-queue
 Listening on [foo], queue group [my-queue]
go run examples/nats-qsub/main.go -s 10.8.2.202:4222 foo my-queue1 # 这里队列名不一样
 Listening on [foo], queue group [my-queue1]

# 两个普通订阅者：
go run examples/nats-sub/main.go -s 10.8.2.202:4222 foo
Listening on [foo]
go run examples/nats-sub/main.go -s 10.8.2.202:4222 foo
Listening on [foo]
```

启动发布者：

``` sh
go run examples/nats-pub/main.go -s 10.8.2.202:4222 foo sss11
Published [foo] : 'sss11'
# 此处为发的多条消息
```

向foo主题发送消息，观察订阅者：

my-queue 两个订阅者各自随机收到消息，my-queue1的订阅者能收到全部消息。

普通订阅者也能收到全部消息。



## NATS Streaming

NATS由于不能保证消息的投递正确性和存在其他的缺点,NATS Streaming就孕育而生.他是一个由NATS提供支持的数据流系统,采用Go语言编写,NATS Streaming与核心NATS平台无缝嵌入，扩展和互操作.除了核心NATS平台的功能外,他还提供了以下功能:
**NATS Streaming特征**
增强消息协议(Enhanced message protocol)
消息/事件持久化(Message/event persistence)
至少一次数据传输(At-least-once-delivery)
Publisher限速(Publisher rate limiting)
Subscriber速率匹配(Rate matching/limiting per subscriber)
按主题重发消息(Historical message replay by subject)
持续订阅(Durable subscriptions)