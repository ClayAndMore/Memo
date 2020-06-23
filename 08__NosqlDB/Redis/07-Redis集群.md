
---
title: "07-Redis集群.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "07-Redis集群.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
单机/单点的问题：单点故障/瓶颈

一变多的方式：

镜像： 多台数据一致，数据容量不变，强一致性。

分片：横向扩展



集群分类

主从复制 Replication

* 一个Redis服务可以有多个该服务的复制品，这个Redis服务称为Master，其他复制品称为Slaves

* 只要网络连接正常，Master会一直将自己的数据更新同步给Slaves，保持主从同步 
* 只有Master可以执行写命令，Slaves只能执行读命令 

创建：

* 主： redis-server --port 6380 ， 从： redis-server --slaveof ip:port (ip说明是谁的从)
* SLAVEOF host port 命令： 将当前服务器从Master修改为其他服务器的Slave
  * redis> SLAVE 192.168.1.1 6379 将服务器转换为Slave
  * redis> SLAVE NO ONE, 将服务器恢复到Master,不会丢弃已同步数据



这里主从同步实际上是主节点异步告诉从节点，具体同步的怎么样，主节点是不管的。

哨兵机制，监控整个redis集群，只要主挂了，马上选一个从做主。





### 伪分布式

