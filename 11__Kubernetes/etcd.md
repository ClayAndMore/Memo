---
title: "etcd.md"
date: 2020-03-24 09:58:51 +0800
lastmod: 2020-03-24 09:58:51 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
etcd是一个高可用的分布式键值(key-value)数据库。etcd内部采用raft协议作为一致性算法，etcd基于Go语言实现。
 etcd是一个服务发现系统，具备以下的特点：
 简单：安装配置简单，而且提供了HTTP API进行交互，使用也很简单
 安全：支持SSL证书验证
 快速：根据官方提供的benchmark数据，单实例支持每秒2k+读操作
 可靠：采用raft算法，实现分布式系统数据的可用性和一致性