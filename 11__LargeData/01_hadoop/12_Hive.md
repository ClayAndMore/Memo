---
title: "12_Hive.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["hadoop"]
categories: ["大数据"]
author: "Claymore"

---
### hive 简介

非java编程者对hdfs的数据做mapreduce操作。

使用SQL代替java的业务逻辑。

SQL --> java --> MapReduce

或转成HDFS的操作，如 select * from table 是直接对应一条HDFS操作的。

hive是数据仓库， 数据仓库： 是对过去的数据做数据统计， 它用MapReduce的过程很慢。

而 数据库则是用于存储和实时的交互访问。



hive的三个阶段： 解释器，编译器，优化器等

hive 运行时， 元数据存储在关系型数据库里面。

官网： https://hive.apache.org/



### hive架构

编译器将一个Hive SQL转换成操作符

操作符是Hive的最小的处理单元，一个SQL可以转换成好几个操作符。

每个操作符代表HDFS的一个操作或者一道MapReduce作业。



#### 操作符 operator

几种操作符：

Select

TableScan  扫描整个表

Limit 

File Output



#### ANTLR 词法语法分析工具解析hql

```
Parser 将HQL转换成抽象语法树
Semanitic Analyzer 将抽象语法树转换成查询块
Logic Plan Generator 将查询块转换成逻辑查询计划
LogicalIOptimizer 重写逻辑查询计划
Physical Plan Generator 将逻辑机会转成物理计划（M/R jobs）
PhysicalOptimizer 选择最佳的策略
```



### Hive 搭建模式

#### local 模式

此模式连接到一个In-memory（内存） 的数据库Derby, 一般用于简单的测试。



后两种模式， 前提是先装一个mysql server.

#### 单用户模式

通过网络连接到一个数据库中

```
+--------------------+      +----------+
|    Hive CLI        |      |          |
|  +-----------------+      |  MySQL   |
|  |Meta Store Client+----->+  Server  |
|  +-----------------+      |          |
+--------------------+      +----------+
```



#### 远程服务器模式/多用户模式

用于非java客户端访问元数据库，在

```
+--------------------+    +---------------+  +---------+
|    Hive CLI        |    |               |  |         |
|  +-----------------+    |MetaStoreServer|  |MySQL    |
|  |Meta Store Client+--->+   Thrift      +->+Server   |
|  +-----------------+    |               |  |         |
+--------------------+    +---------------+  +---------+
```



后两种模式是常用的。