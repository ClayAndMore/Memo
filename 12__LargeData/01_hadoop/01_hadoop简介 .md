---
title: "01_hadoop简介 .md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["hadoop"]
categories: ["大数据"]
author: "Claymore"

---


官网：<https://hadoop.apache.org/old/>



### 生态组成

可看到hadoop 的四个组成：

The project includes these modules:

- **Hadoop Common**: The common utilities that support the other Hadoop modules. 为其他Hadoop模块提供基础设施
- **Hadoop Distributed File System (HDFS™)**: A distributed file system that provides high-throughput access to application data. 一个高可靠、高吞吐量的分布式文件系统
- **Hadoop YARN**: A framework for job scheduling and cluster resource management. 任务调度与资源管理
- **Hadoop MapReduce**: A YARN-based system for parallel processing of large data sets. 一个分布式的离线并行计算框架

其他和hadoop有关的Apache 项目：

* HBase， 来自谷歌论文，大表，这个表是二维的，行无限，列无限。
* Hive, 把一堆mr转成sql语言，不用写api, 使用其组建数据仓库
* Spark， 计算处理，可以使用java和scala。
* Zookeeper, 分布式协调系统。开源，可以直接进入项目。



### 起源

谷歌三大论文

```
google       hadoop
GFS          HDFS
Mapreduce    Mapeduce
BigTable     Hbase
```

https://www.jianshu.com/p/7df00b383fa1



### 需求

环境，内存： 128M,  有一个1T文件 ，都是一行一行的字符串，每行都是100Byte

1，有两个重复行，请找出这两个重复行。

当前内存内否方向全量数据



hadoop主要思想： 化整为零（大文件切成小文件），并行计算(离线计算， 实时计算)



### 版本

1.x, 2.x, 3.x 三代。

Hadoop 3.0  GA版于2017年12月份正式发布

- Alpha: 内部测试版
- Beta: 对外测试版
- GA: general availability 官方正式发布版
- Release



数据平台： <https://www.zhihu.com/question/27798279>

相关竞赛：<https://www.zhihu.com/question/36374964>

