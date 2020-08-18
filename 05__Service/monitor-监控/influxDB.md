---
title: "influxDB.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: ["监控服务"]
author: "Claymore"

---


InfluxDB官方文档：https://docs.influxdata.com/influxdb/。

中文文档： https://jasper-zhang1.gitbooks.io/influxdb/content/Introduction/getting_start.html

docker images: https://hub.docker.com/_/influxdb

InfluxDB 是一个时间序列数据库，用于处理海量写入与负载查询。InfluxDB旨在用作涉及大量时间戳数据的任何用例（包括DevOps监控，应用程序指标，物联网传感器数据和实时分析）的后端存储。

特点：

- 为时间序列数据专门编写的自定义高性能数据存储。 TSM引擎具有高性能的写入和数据压缩

- Golang编写，没有其它的依赖

- 提供简单、高性能的写入、查询 http api

- 支持类sql查询语句

- tags可以索引序列化，提供快速有效的查询

- 同一时间点多次写入同样的数据被认为是重复写入

- 极少出现删除数据的情况，删除数据基本都是清理过期数据

- 极少更新已有数据且不会出现有争议的更新，时间序列数据总是新数据

- 绝大多数写入是针对最新时间戳的数据，并且数据按时间升序添加

- 数据的规模会非常大，必须能够处理大量的读写操作

- 能够写入和查询数据会比强一致性更重要

- 很多time series非常短暂的存在，所以time series 数量比较大

- 没有哪个point是过于重要的

### 安装和配置

```
docker run -d -p 8086:8086 -v "/root/influxdb:/var/lib/influxdb" --name=influxdb influxdb
```

8086是influxdb的HTTP API端口

启动InfluxDB容器后，通过http接口访问进行测试。

`curl -G http://localhost:8086/query --data-urlencode "q=show databases"`
若influxdb运行正常，则会返回如下结果：

```
# 链接查询参数为show databases 数据库会返回所有的数据库名，新安装的influxdb默认只有一个"_internal"
# 数据库。

{"results":[{"statement_id":0,"series":[{"name":"databases","columns":["name"],"values":[["_internal"],["telegraf"]]}]}]}
```

8083是influxdb的web管理工具端口（目前1.1版本后已经取消这个功能）:

`docker run -d -p 8083:8083 -p8086:8086 --name influxsrv influxdb`

用户名root，密码root    

配置文件一般在/etc/influxdb/influxdb.conf



### 命令行操作

#### 数据库与表的操作

可以直接在web管理页面做操作，当然也可以命令行。

```sh
#创建数据库
create database "db_name"
#显示所有的数据库
show databases
#删除数据库
drop database "db_name"
#使用数据库
use db_name
#显示该数据库中所有的表
show measurements
#创建表，直接在插入数据的时候指定表名
insert test,host=127.0.0.1,monitor_name=test count=1
#删除表
drop measurement "measurement_name"
```

#### 用户管理

```sh
#显示用户  
show users
#创建用户
create user "username" with password 'password'
#创建管理员权限用户create user "username" with password 'password' with all privileges
#删除用户
drop user "username"
```

#### 增

向数据库中插入数据。

- 通过命令行
  
  ```
  use testDb
  insert test,host=127.0.0.1,monitor_name=test count=1
  ```

- 通过http接口
  
  ```
  curl -i -XPOST 'http://127.0.0.1:8086/write?db=testDb' --data-binary 'test,host=127.0.0.1,monitor_name=test count=1'
  ```

读者看到这里可能会观察到插入的数据的格式貌似比较奇怪，这是因为influxDB存储数据采用的是Line Protocol格式。那么何谓Line Protoco格式？

#### 查

查询数据库中的数据。

- 通过命令行
  
  ```
  select * from test order by time desc
  ```

- 通过http接口
  
  ```
  curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=testDb" --data-urlencode "q=select * from test order by time desc"
  ```

influxDB是支持类sql语句的

#### 数据保存策略（Retention Policies）

influxDB是没有提供直接删除数据记录的方法，但是提供数据保存策略，主要用于指定数据保留时间，超过指定时间，就删除这部分数据。

- 查看当前数据库Retention Policies
  
  ```
  show retention policies on "db_name"
  ```

- 创建新的Retention Policies
  
  ```
  create retention policy "rp_name" on "db_name" duration 3w replication 1 default
  ```
  
  - rp_name：策略名；
  - db_name：具体的数据库名；
  - 3w：保存3周，3周之前的数据将被删除，influxdb具有各种事件参数，比如：h（小时），d（天），w（星期）；
  - replication 1：副本个数，一般为1就可以了；
  - default：设置为默认策略

- 修改Retention Policies
  
  ```
  alter retention policy "rp_name" on "db_name" duration 30d default
  ```

- 删除Retention Policies
  
  ```
  drop retention policy "rp_name"
  ```
### 数据格式

#### Measurement

描述了相关数据的存储结构，类似于 mysql 的 table，但是不需要创建，写入数据的时候自动创建。

#### point

Point相当于传统数据库里的一行数据，如下表所示：

| Point属性 | 传统数据库中的概念                 |
| ------- | ------------------------- |
| time    | 每个数据记录时间，是数据库中的主索引(会自动生成) |
| fields  | 各种记录值（没有索引的属性）            |
| tags    | 各种有索引的属性                  |

#### Line Protocol

Line Protocol格式：写入数据库的Point的固定格式。想对此格式有详细的了解参见[官方文档](https://docs.influxdata.com/influxdb/v0.10/write_protocols/line/)

我们可以粗略的将要存入的一条数据看作**一个虚拟的 key 和其对应的 value(field value)**。格式如下：

```
cpu_usage,host=server01,region=us-west value=0.64 1434055562000000000
```

 虚拟的 key 包括以下几个部分： 

* measurement: 测量指标名（表名），例如 cpu_usage 表示 cpu 的使用率。

* tag sets: tags 在 InfluxDB 中会按照字典序排序，不管是 tagk 还是 tagv，只要不一致就分别属于两个 key，例如 host=server01,region=us-west 和 host=server02,region=us-west 就是两个不同的 tag set。它可以被索引。tag 的类型只能是字符串。
- retention policy: 存储策略，用于设置数据保留的时间，每个数据库刚开始会自动创建一个默认的存储策略 autogen，数据保留时间为永久，之后用户可以自己设置，例如保留最近2小时的数据。插入和查询数据时如果不指定存储策略，则使用默认存储策略，且默认存储策略可以修改。InfluxDB 会定期清除过期的数据。

- tag--标签，在InfluxDB中，tag是一个非常重要的部分，表名+tag一起作为数据库的索引，是“key-value”的形式。

- field name: 例如上面数据中的 value 就是 fieldName，InfluxDB 中支持一条数据中插入多个 fieldName，这其实是一个语法上的优化，在实际的底层存储中，是当作多条数据来存储。

- timestamp: 每一条数据都需要指定一个时间戳，在 TSM 存储引擎中会特殊对待，以为了优化后续的查询操作。

深层次：https://blog.csdn.net/gongpulin/article/details/81023085