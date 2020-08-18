---
title: "troubleshoot.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-03-17 15:10:43 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
docker 搭建nginx的时候，如果内部使用容器的网关ip，即使不接外网也记得给被代理的端口加防火墙规则。





### dockers exec user process caused "exec format error"

可能是镜像与系统不兼容



### failed: iptables: No chain/target/match by that name

docker 服务启动的时候，docker服务会向iptables注册一个链，以便让docker服务管理的containner所暴露的端口之间进行通信

如果你删除了iptables中的docker链，或者iptables的规则被丢失了（例如重启firewalld）。

解决办法：

1, 重启 docker, ` systemctl restart docker` 

2, 如果还是不行，关闭 firewalld 服务： `systemctl stop firewalld`,  还是不行的话关闭iptables: `systemctl stop iptables`