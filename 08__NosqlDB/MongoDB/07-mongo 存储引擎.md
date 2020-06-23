
---
title: "07-mongo 存储引擎.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "07-mongo 存储引擎.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
MongoDB 从 3.0 版本 开始，引入了存储引擎的概念，并开放了 StorageEngine 的API 接口，为了方便KV存储引擎接入作为 MongoDB 的存储引擎，MongoDB 又封装出一个 KVEngine 的API接口，比如官方的 wiredtiger 存储引擎就是实现了 `KVEngine` 的接口，本文介绍的 mongorocks 也是实现了KVEngine的接口



存储引擎是MongoDB的核心组件，负责管理数据如何存储在硬盘和内存上。从MongoDB 3.2 版本开始，MongoDB 支持多数据存储引擎，MongoDB支持的存储引擎有：WiredTiger，MMAPv1和In-Memory。

从mongodb3.2开始默认的存储引擎是WiredTiger，3.3版本之前的默认存储引擎是MMAPv1，mongodb4.x版本不再支持MMAPv1存储引擎。

wiredTiger相对于MMAPV1其有如下优势:

 读写操作性能更好,WiredTiger能更好的发挥多核系统的处理能力；
 MMAPV1引擎使用表级锁,当某个单表上有并发的操作,吞吐将受到限制。WiredTiger使用文档级锁,由此带来并发及吞吐的提高
 相比MMAPV1存储索引时WiredTiger使用前缀压缩,更节省对内存空间的损耗；
 提供压缩算法,可以大大降低对硬盘资源的消耗,节省约60%以上的硬盘资源；



### 配置文件

```yaml
storage:
    journal:
        enabled: true
    dbPath: /data/zhou/mongo1/
    ##是否一个库一个文件夹
    directoryPerDB: true
    ##数据引擎
    engine: wiredTiger
    ##WT引擎配置
    WiredTiger:
        engineConfig:
            ##WT最大使用cache（根据服务器实际情况调节）
            cacheSizeGB: 1
            ##是否将索引也按数据库名单独存储
            directoryForIndexes: true
            journalCompressor:none （默认snappy）
        ##表压缩配置
        collectionConfig:
            blockCompressor: zlib (默认snappy,还可选none、zlib)
        ##索引配置
        indexConfig:
            prefixCompression: true
```

压缩 算法 Tips:
性能: none > snappy >zlib
压缩比:zlib > snappy > none

 