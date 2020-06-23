
---
title: "packet.md"
date: 2020-05-22 18:23:54 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "packet.md"
date: 2020-05-22 18:23:54 +0800
lastmod: 2020-05-22 18:23:54 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---




### 修改：

新建go文件：trireme-dsec\commons\processors\packat.go

``` go
package processors

import (
	"fmt"
	provider "git.cloud.top/DSec/trireme-lib/controller/pkg/aclprovider"
	"git.cloud.top/DSec/trireme-lib/controller/pkg/connection"
	"git.cloud.top/DSec/trireme-lib/controller/pkg/fqconfig"
	"git.cloud.top/DSec/trireme-lib/controller/pkg/packet"
	"git.cloud.top/DSec/trireme-lib/controller/pkg/pucontext"
	"git.cloud.top/DSec/trireme-lib/controller/pkg/tokens"
)

type MyPacket struct {
	des string
}

// 实现 PacketProcessor 接口

func (myp MyPacket) Initialize(fq *fqconfig.FilterQueue, p []provider.IptablesProvider) {
	fmt.Println("========= Initialize")
}

func (myp MyPacket) Stop() error {
	fmt.Println("========= Stop")
	return nil
}

func (myp MyPacket) PreProcessTCPAppPacket(p *packet.Packet, context *pucontext.PUContext, conn *connection.TCPConnection) bool {
	fmt.Println("========= PreProcessTCPAppPacket")
	return true
}

func (myp MyPacket) PostProcessTCPAppPacket(p *packet.Packet, action interface{}, context *pucontext.PUContext, conn *connection.TCPConnection) bool {
	fmt.Println("========= PostProcessTCPAppPacket")
	return true
}

func (myp MyPacket) PreProcessTCPNetPacket(p *packet.Packet, context *pucontext.PUContext, conn *connection.TCPConnection) bool {
	fmt.Println("========= PreProcessTCPNetPacket")
	return true
}

func (myp MyPacket) PostProcessTCPNetPacket(p *packet.Packet, action interface{}, claims *tokens.ConnectionClaims, context *pucontext.PUContext, conn *connection.TCPConnection) bool {
	fmt.Println("========= PostProcessTCPNetPacket")
	return true
}

func (myp MyPacket) PreProcessUDPAppPacket(p *packet.Packet, context *pucontext.PUContext, conn *connection.UDPConnection, packetType uint8) bool {
	fmt.Println("========= PreProcessUDPAppPacket")
	return true
}

func (myp MyPacket) PostProcessUDPAppPacket(p *packet.Packet, action interface{}, context *pucontext.PUContext, conn *connection.UDPConnection) bool {
	fmt.Println("========= PostProcessUDPAppPacket")
	return true
}

func (myp MyPacket) PreProcessUDPNetPacket(p *packet.Packet, context *pucontext.PUContext, conn *connection.UDPConnection) bool {
	fmt.Println("========= PreProcessUDPNetPacket")
	return true
}

func (myp MyPacket) PostProcessUDPNetPacket(p *packet.Packet, action interface{}, claims *tokens.ConnectionClaims, context *pucontext.PUContext, conn *connection.UDPConnection) bool {
	fmt.Println("========= PostProcessUDPNetPacket")
	return true
}
```

这里我们是仿照实现 git.cloud.top\!d!sec\trireme-lib@v0.1.6\controller\pkg\packetprocessor\packetprocessor.go 的 PacketProcessor 接口，

修改 git.cloud.top\DSec\trireme-lib\controller\controller.go 源码：

``` go
func New(serverID string, mode constants.ModeType, service packetprocessor.PacketProcessor, opts ...Option) TriremeController {

	c := &config{
		serverID:               serverID,
		collector:              collector.NewDefaultCollector(),
		service:			    service,   // 这里，新增一个我们自己的service, 防止其使用默认的。
		mode:                   mode,
		fq:                     fqconfig.NewFilterQueueWithDefaults(),
		mutualAuth:             true,
		validity:               constants.DatapathTokenValidity,
		pr
```





更改实例化控制器的代码：

``` go
// 实例化一个控制器
func (cfg *DockerConfiguration) NewController(collectorInstance collector.EventCollector) controller.TriremeController {
	triremeNodeName := utils.GenerateNodeName(cfg.NodeName)
	controllerOptions := cfg.setControllerOptions(collectorInstance)
	service := processors.MyPacket{} // 这里是我们的测试结构体
	ctrl := controller.New(triremeNodeName, constants.RemoteContainer, service, controllerOptions...)
	if ctrl == nil {
		zap.L().Fatal("Unable to initialize Topsec-dsec")
	}
	return ctrl
}
```



### 运行。

我们找一个没有容器的机器，启动trime, 然后在启动两个容器，观察日志：

```sh
{"level":"info","ts":1590138592.525933,"caller":"entrypoint/dockerconfig.go:144","msg":"Initializing Topsec-dsec with PKI Auth"}
{"level":"info","ts":1590138592.6248085,"caller":"tokenaccessor/tokenaccessor.go:34","msg":"Enabling Trireme Datapath v2.0"}
{"level":"info","ts":1590138592.6879175,"caller":"envoyauthorizer/envoyauthorizerenforcer.go:59","msg":"Creating Envoy Authorizer Enforcer"}
========= Initialize  # 这里有我们自定义的输出
{"level":"info","ts":1590138593.2972436,"caller":"docker/monitor.go:750","msg":"Trying to initialize docker monitor"}
{"level":"info","ts":1590138593.320323,"caller":"docker/monitor.go:779","msg":"Started Docker Monitor"}
{"level":"info","ts":1590138593.321042,"caller":"entrypoint/cmd.go:141","msg":"Everything started. Waiting for Stop signal"}
{"level":"info","ts":1590138593.321246,"caller":"policyresolver/policy.go:157","msg":"开始监听策略事件"}
{"level":"info","ts":1590138593.322113,"caller":"nfqdatapath/nfq_linux.go:79","msg":"处理在NF队列中从网络到达的数据包 --> 入站"}

```

建立nc的监听：

``` sh
root@node200:~# docker exec -it nginx1 sh
/ # ip r
default via 182.18.0.1 dev eth0
182.18.0.0/24 dev eth0 scope link  src 182.18.0.2
/ # nc -l 9999

```

另外一个终端：

``` sh
root@node200:~# docker exec -it nginx2 sh
/ # ip r
default via 182.18.0.1 dev eth0
182.18.0.0/24 dev eth0 scope link  src 182.18.0.3
/ # nc 182.18.0.2 9999

```

此时观察日志，会有一些输出，但是没有我们自定义的输出。