
---
title: "dlv远程调试.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-03-17 15:10:43 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


## go dlv 远程调试



## dlv

Dlv 是 delve 的简称

Gitlab: https://github.com/go-delve/delve

在 linux 上的安装：

``` bash
go get -u github.com/go-delve/delve/cmd/dlv

# 或使用克隆git的方式
$ git clone https://github.com/go-delve/delve.git $GOPATH/src/github.com/go-delve/delve
$ cd $GOPATH/src/github.com/go-delve/delve
$ make install  
```

make install 也会去联网下一些包，如果访问不了 goland.org, 可以设置代理：

`go env -w GOPROXY=https://goproxy.cn,direct`

``` bash
root@wy:~/go/workspace/src/github.com/go-delve/delve# make install
go: downloading github.com/spf13/cobra v0.0.0-20170417170307-b6cb39589372
...
go install "-ldflags=-X main.Build=f863be0a172a9c62d679143ec53587ef6255737e" github.com/go-delve/delve/cmd/dlv
go: downloading github.com/sirupsen/logrus v0.0.0-20180523074243-ea8897e79973
go: downloading golang.org/x/arch v0.0.0-20190927153633-4e8777c89be4
go: downloading gopkg.in/yaml.v2 v2.2.1
go: downloading github.com/peterh/liner v0.0.0-20170317030525-88609521dc4b
go: downloading github.com/google/go-dap v0.2.0
...
```

安装后的验证：

``` bash
root@wy:~/go/workspace/src/github.com/go-delve/delve# ls $GOPATH/bin
dlv
root@wy:~/go/workspace/src/github.com/go-delve/delve# dlv --help
Delve is a source level debugger for Go programs.
...
Pass flags to the program you are debugging using `--`, for example:

`dlv exec ./hello -- server --config conf/config.toml`

Usage:
  dlv [command]

Available Commands:
  attach      Attach to running process and begin debugging.
  connect     Connect to a headless debug server.
  core        Examine a core dump.
```



### 编译待调试程序

在服务器上编译你的程序, 必须添加 `-gcflags` 参数, 其他随意.

- Go 1.10 及以上

```
go build -gcflags "all=-N -l" github.com/app/demo
```

- Go 1.9 及以下

```
go build -gcflags "-N -l" github.com/app/demo
```



开始编译：

``` bash 
root@wy:~/go/workspace/src/trireme-dsec# go version
go version go1.13.6 linux/amd64

root@wy:~/go/workspace/src/trireme-dsec# go build -gcflags "all=-N -l" -mod=vendor
```



### 启动待调试程序

启动示例：

```
dlv --listen=:2345 --headless=true --api-version=2 --accept-multiclient exec ./demo
```

--acrept-multiclient 是 多客户端调试，一般不加。

如果启动的程序需要参数 需要在后面加 --：

```
dlv --listen=:2345 --headless=true --api-version=2  exec ./demo -- -c=config
```



run.sh:

```bash
dlv --listen=:2345 --headless=true --api-version=2 exec \
./trireme-dsec -- docker daemon --api http://172.19.19.16:12345 --namespace /test1
```

开启：

```
root@wy:~/go/workspace/src/trireme-dsec# ./run.sh
API server listening at: [::]:2345

```



### ide

使用 goland ide，Run` -> `EditConfigurations` -> `+` -> `GoRemote

配置好 ip 和端口。

然后设置断点，点击 run - debug 刚才配置的remote.

还可以 在 **Variables** 面板可以查看变量, 可以点击**+**增加**Watch**



dlv启动停止的时候直接利用Ctrl-C无法停止项目，需要ps查看进程号将进程杀死，同时需要注意的是，debug也是一个进程，所以需要将debug进程也杀死:

```
kill -9 ps -ef | grep "dlv|mytest" -E | awk '{print $2}'
```

mytest是程序名。

在ide点停止调试也可以让远端的dle停止。