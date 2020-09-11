---
title: "Docker run.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---



### -e / --env





### --net/--network

使用主机的网络：  docker run --net=host images 

`--network` and `--net` options in the Docker are the same and work similarly. But `--net` is shorter in use. 

docker 有五种网络通信模式：

- bridge: 默认的网络驱动模式。如果不指定驱动程序，bridge 便会作为默认的网络驱动模式。当应用程序运行在需要通信的独立容器 (standalone containers) 中时，通常会选择 bridge 模式。
- host：**移除容器和 Docker 宿主机之间的网络隔离，并直接使用主机的网络。**host 模式仅适用于 Docker 17.06+。
- overlay：overlay 网络将多个 Docker 守护进程连接在一起，并使集群服务能够相互通信。您还可以使用 overlay 网络来实现 swarm 集群和独立容器之间的通信，或者不同 Docker 守护进程上的两个独立容器之间的通信。该策略实现了在这些容器之间进行操作系统级别路由的需求。
- macvlan：Macvlan 网络允许为容器分配 MAC 地址，使其显示为网络上的物理设备。 Docker 守护进程通过其 MAC 地址将流量路由到容器。对于希望直连到物理网络的传统应用程序而言，使用 macvlan 模式一般是最佳选择，而不应该通过 Docker 宿主机的网络进行路由。
- none：对于此容器，禁用所有联网。通常与自定义网络驱动程序一起使用。none 模式不适用于集群服务。



### --link

```
--link name:alias
```

**这里 name 是我们要连接的container的名字， alias 是一link的别名.** 

link可以让其他非host网络模式启动的容器连接到其他容器，这样可以避免暴露端口。

eg:

```sh
# 创建一个db
docker run -d --name mydb postgres
# web应用
docker run -d -P --name web --link mydb:db webapp python app.py
```

docker ps:

```
CONTAINER ID  IMAGE              PORTS                    NAMES
349169744e49  postgres:latest    5432/tcp                 mydb
aed84ee21bde  webapp:latest      0.0.0.0:49154->5000/tcp  mydb/web,web
```

**注意 web container 在name列里还显示了另外一个名字mydb/web。 这个名字告诉我们 web container 被连接到了 db container， 并且建立了一种父子关系。** mydb是父



Docker通过这种方式把父container里的信息暴露给子container:

- 环境变量
- 更新 /etc/host 文件

进入到子容器：

``` sh
root@aed84ee21bde:/opt/webapp# env
HOSTNAME=aed84ee21bde
. . .
DB_NAME=/web/db
DB_PORT=tcp://172.17.0.5:5432
DB_PORT_5000_TCP=tcp://172.17.0.5:5432
DB_PORT_5000_TCP_PROTO=tcp
DB_PORT_5000_TCP_PORT=5432
DB_PORT_5000_TCP_ADDR=172.17.0.5
```

这些变量实际上都是mydb里的，不过这里加了个别名DB（自动变大写）, 如在mydb的变量NAME，在web容器里就变成了DB_NAME。 注意，如果此时再bash一个终端，这些变量消失，它只存在容器运行命令的那个进程中。

除了环境变量之外Docker会把父container的IP添加到子container的/etc/hosts里。我们 看下一下 web container里的hosts文件：

```
root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
. . .
172.17.0.5  db
```

试着ping一下：

```
root@aed84ee21bde:/opt/webapp# ping db
PING db (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
```

