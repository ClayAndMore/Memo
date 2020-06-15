
---
title: "04-锁和version.md"
date: 2019-10-29 16:53:35 +0800
lastmod: 2019-10-29 16:53:35 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
版本控制，并发情况下，对有限资源的锁，防止多进程/线程同时操作产生脏数据。

### 悲观锁

假定并发下一定会发生冲突，当有线程操作数据库的时候，先给数据库加锁，防止其他人使用。

修改完毕再解锁，优点是很安全，适用于并发量很小的情况下。如果并发量大，频繁的加锁和解锁会有性能问题。



### 乐观锁

假定并发不上发生冲突，一般在提交操作的时候检查数据是否违法。

如果多个线程操作，会有一个线程成功，其他线程是失败的。

缺点是查询操作比较多，因为这些失败的线程会再次查询该资源的状态，并且会有数据不实时的状态。



### es

elasticsearch 中使用的是 乐观锁。

通过内部版本控制 和 外部版本控制：

#### 内部版本控制

`_version` 自增长， 修改数据后， `_versoin` 会自动加 1

```sh
#curl -XGET 'localhost:9200/library/books/1?pretty'
{
  "_index" : "library",
  "_type" : "books",
  "_id" : "1",
  "_version" : 1,
...
    "price" : "49.99"
  }
}

#curl -XPOST 'localhost:9200/library/books/1/_update?pretty ' -H 'Content-Type: application/json' -d '
{
  "doc": {
     "price" : 10
  }
}'
{
  "_index" : "library",
  "_type" : "books",
  "_id" : "1",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```

发现_version 发生 改变，

我们试着通过version 获取：

```sh
#curl -XGET 'localhost:9200/library/books/1?version=3&pretty'
{
  "error" : {
    "root_cause" : [
      {
        "type" : "version_conflict_engine_exception",
        "reason" : "[books][1]: version conflict, current version [2] is different than the one provided [3]",
        "index_uuid" : "3e_Oo9ddRm6JAxpCx4eatg",
        "shard" : "3",
        "index" : "library"
      }
    ],
    "type" : "version_conflict_engine_exception",
    "reason" : "[books][1]: version conflict, current version [2] is different than the one provided [3]",
    "index_uuid" : "3e_Oo9ddRm6JAxpCx4eatg",
    "shard" : "3",
    "index" : "library"
  },
  "status" : 409
}
```

可见提示 version_confict



#### 外部版本控制

为了保持`_version` 与外部版本控制的数值一致，使用version_type = external 检查数据当前的 version 值 是否小于请求中的 version 值。

```sh
#curl -XPUT 'localhost:9200/library/books/2?version=5&version_type=external'  -H 'Content-Type: application/json' -d '
> {
>   "doc": {
>      "price" : 15
>   }
> }'
{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1}
#curl -XGET 'localhost:9200/library/books/2?pretty'
{
  "_index" : "library",
  "_type" : "books",
  "_id" : "2",
  "_version" : 5,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "doc" : {
      "price" : 15
    }
  }
}
```

通过version_type可以改变`_version`, 但是指定 的version 版本 一定要比 现在的大，小于等于都不行。

