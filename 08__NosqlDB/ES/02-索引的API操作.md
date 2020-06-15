
---
title: "02-索引的API操作.md"
date: 2019-10-25 17:50:12 +0800
lastmod: 2019-11-01 18:04:05 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## 索引

### 初始化

简单的创建索引：

`curl -XPUT 'localhost:9200/library`

创建索引前可以对索引做初始化操作， 比如指定 shards 和 replicas 的数量。

shards 分片数，  replicas 副本，过后补充。

```sh
#curl -XPUT 'localhost:9200/library' -H 'Content-Type: application/json' -d '{
"settings":{
 "index":{
  "number_of_shards":5,
  "number_of_replicas":1
}}}
'
{"acknowledged":true,"shards_acknowledged":true,"index":"library"}
```

library 是我们创建的索引名称。



### 获取

查询我们刚刚创建的索引：

```sh
#curl -XGET 'localhost:9200/library'
{"library":{"aliases":{},"mappings":{},"settings":{"index":{"creation_date":"1571985711395","number_of_shards":"5","number_of_replicas":"1","uuid":"3e_Oo9ddRm6JAxpCx4eatg","version":{"created":"6080499"},"provided_name":"library"}}}}
#curl -XGET 'localhost:9200/library/_settings'
{"library":{"settings":{"index":{"creation_date":"1571985711395","number_of_shards":"5","number_of_replicas":"1","uuid":"3e_Oo9ddRm6JAxpCx4eatg","version":{"created":"6080499"},"provided_name":"library"}}}}

#curl -XGET 'localhost:9200/library/_settings?pretty'
{
  "library" : {
    "settings" : {
      "index" : {
        "creation_date" : "1571985711395",
        "number_of_shards" : "5",
        "number_of_replicas" : "1",
        "uuid" : "3e_Oo9ddRm6JAxpCx4eatg",
        "version" : {
          "created" : "6080499"
        },
        "provided_name" : "library"
      }
    }
  }
}

```

查询的时候最好加上？pretty ， 格式化输出。

另外：

```
curl -XGET 'localhost:9200/index1, index2/_settings'  # 获取 index1, index2 两个索引的索引信息
curl -XGET 'localhost:9200/_all/_settings'  # 获取所有的索引信息
```



#### 显示所有索引

`curl 'localhost:9200/_cat/indices?v'`

_cat 提供了一系列集群状态的接口，v 表示显示表头输出。



### 删除

` curl -X DELETE "localhost:9200/customer?pretty" `



##  文档

### 添加

```sh
#curl -XPUT 'localhost:9200/library/books/1?pretty' -H 'Content-Type: application/json'  -d '
{
  "title": "Elasticsearch: The Definitive Guide007",
  "name" : {
    "first" : "Zachary",
    "last" : "Tong"
  },
  "publish_date":"2015-02-06",
  "price":"49.99"
}'
# out:
{
  "_index" : "library",
  "_type" : "books",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}
```

library(索引)/books(type)/1(文档ID) ，文档ID我们可以不设置，



### 获取

通过ID获得文档信息
GET /library/books/1
GET /library/books/2
GET /library/books/AU_A8D0DU9duEv19TRl8

通过`_source`获取指定的字段

```
GET /library/books/1?source=title
GET /library/books/1?source=title,price
GET /library/books/1?_source
```



### 更新

我们更新同一个ID下的文档，可以通过覆盖的方式更新

```
PUT /library/books/1
{
  "title": "Elasticsearch: The Definitive Guide",
  "name" : {
    "first" : "Zachary",
    "last" : "Tong"
  },
  "publish_date":"2015-02-06",
  "price":"59.99"
}
```

或者通过` _update ` API的方式单独更新你想要更新的:

```
POST /library/books/1/_update
{
  "doc": {
     "price" : 10
  }
}
GET /library/books/1
```



### 删除

删除一个文档的方法
DELETE /library/books/1
DELETE /library
GET /library/books/1



## 多文档操作

### mget 多文档获取

Multi GET,  同时检索多个文档。

mget API 参数 是一个 docs 数组，数组的每个节点定义一个文档的_index, _type, _id 元数据。

eg: 获取获取index:bank 和 shakespeare, type:bank_account， ID为1，3，4 的文档信息

GET /bank/bank_account/1
GET /bank/bank_account/4
GET /shakespeare/line/3

```
curl -XGET 'localhost:9200/_mget?pretty' -H 'Content-Type: application/json' -d '
{   "docs" : [
      {
         "_index" : "bank",
         "_type" :  "bank_account",
         "_id" :    1
      },
      {
         "_index" : "shakespeare",
         "_type" :  "line",
         "_id" :    3
      },
      {
         "_index" : "shakespeare",
         "_type" :  "line",
         "_id" :    4
      }
   ]
}'
```



也可以指定`_source`字段，获取你想要的

```
GET /_mget
{
   "docs" : [
      {
         "_index" : "shakespeare",
         "_type" :  "line",
         "_id" :    6,
         "_source": "play_name"
      },
      {
         "_index" : "shakespeare",
         "_type" :  "line",
         "_id" :    28,
         "_source": ["play_name","speaker","text_entry"] # 指定多个字段
         
      }
   ]
}
```

获取相同 index 相同 type 下的不同ID文档：

```
GET /shakespeare/line/_mget
{
  "docs" : [
      { "_id" : 6 },
      { "_type" : "line", "_id" :   28 }
   ]
}

# 可以这样简便的写
GET /shakespeare/line/_mget
{
   "ids" : [ "6", "28" ]
```



### bulk 批量操作

实现多个文档的create index update delete.

格式： 

```
{ action: {metadata }}\n
{ request body } \n

换行是为了更好的解析。

# action 及行为： 
 create:  文档不存在时创建
 index: 创建或替换已有文档
 update: 局部更新文档。
 delete: 删除一个文档。

eg:
POST /library/books/_bulk
{ "index":  { "_id": 1}}
{ "title":"Elasticsearch: The Definitive Guide","price":5 }
{ "index":  { "_id": 2}}
{ "title":"The Elasticsearch cookbook","price":15 }
{ "index":  { "_id": 3}}
{ "title":"Elasticsearch Blueprints","price":9 }
```

```
POST /library/books/_bulk
{ "delete": { "_index": "library", "_type": "books", "_id": "1" }}
{ "create": { "_index": "music", "_type": "classical", "_id": "1" }}
{ "title": "Ave Verum Corpus" }
{ "index":  { "_index": "music", "_type": "classical" }}
{ "title": "Litaniac de Venerabili Altaris Sacromento" }
{ "update": { "_index": "library", "_type": "books", "_id": "2"} }
{ "doc" : {"price" : "18"} }
```

注意delete下面没有具体的request body

**bulk 处理文档数据大小的最佳值**，

数据加载在每个节点的RAM， 请求数据超过一定的大小，bulk处理的性能就会降低，可以通过监控及时调整。