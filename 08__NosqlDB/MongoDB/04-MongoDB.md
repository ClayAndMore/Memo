
---
title: "04-MongoDB.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "04-MongoDB.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[nosql, database, mongodb]

### 关系

指文档之间的逻辑关系，(1：1)，(1：N),  (N:1) , (N:N)

user:

```
{
   "_id":ObjectId("52ffc33cd85242f436000001"),
   "name": "Tom Hanks",
   "contact": "987654321",
   "dob": "01-01-1991"
}
```

address:

```
{
   "_id":ObjectId("52ffc4a5d85242602e000000"),
   "building": "22 A, Indiana Apt",
   "pincode": 123456,
   "city": "Los Angeles",
   "state": "California"
} 
```



#### 嵌入式

```
  "_id":ObjectId("52ffc33cd85242f436000001"),
   "contact": "987654321",
   "dob": "01-01-1991",
   "name": "Tom Benzamin",
   "address": [
      {
         "building": "22 A, Indiana Apt",
         "pincode": 123456,
         "city": "Los Angeles",
         "state": "California"
      },
      {
         "building": "170 A, Acropolis Apt",
         "pincode": 456789,
         "city": "Chicago",
         "state": "Illinois"
      }]
} 
```

查用户地址：

```
>db.users.findOne({"name":"Tom Benzamin"},{"address":1})
```

但是这样的结构，在地址不断增加的情况下会影响读写性能。

#### 引用式

通过引用文档的 **id** 字段来建立关系。

```
{
   "_id":ObjectId("52ffc33cd85242f436000001"),
   "contact": "987654321",
   "dob": "01-01-1991",
   "name": "Tom Benzamin",
   "address_ids": [
      ObjectId("52ffc4a5d85242602e000000"),
      ObjectId("52ffc4a5d85242602e000001")
   ]
}
```

这种方法需要两次查询，第一次查询用户地址的对象id（ObjectId），第二次通过查询的id获取用户的详细地址信息。

```
>var result = db.users.findOne({"name":"Tom Benzamin"},{"address_ids":1})
>var addresses = db.address.find({"_id":{"$in":result["address_ids"]}})
```





### aggregate（聚合）

#### aa

用于数据处理，返回计算后的数据结果。有点类似sql中的count。

`db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)`



```
db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : 1}}}])
```

以上实例类似sql语句：

```
select by_user as _id, count(*) as num_tutorial from mycol group by by_user
```

| $sum      | 计算总和。                   | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : "$likes"}}}]) |
| ------------------------------------------------------------ |
| $avg      | 计算平均值                   | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$avg : "$likes"}}}]) |
| $min      | 获取集合中所有文档对应值得最小值。       | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$min : "$likes"}}}]) |
| $max      | 获取集合中所有文档对应值得最大值。       | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}]) |
| $push     | 在结果文档中插入值到一个数组中。        | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$push: "$url"}}}]) |
| $addToSet | 在结果文档中插入值到一个数组中，但不创建副本。 | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$addToSet : "$url"}}}]) |
| $first    | 根据资源文档的排序获取第一个文档数据。     | db.mycol.aggregate([{$group : {_id : "$by_user", first_url : {$first : "$url"}}}]) |
| $last     | 根据资源文档的排序获取最后一个文档数据     | db.mycol.aggregate([{$group : {_id : "$by_user", last_url : {$last : "$url"}}}]) |



在聚合函数中是可以管道操作的：http://www.runoob.com/mongodb/mongodb-aggregate.html



#### 聚合方式

##### Aggregation Pipelines

```
db.col.aggregate(
				{ $match: { status: "A"} },
				{ $group: { _id: "$cust_id", total: { $sum: "$amount"}}},
				{ $sort: { total: -1 } }
)

[{ _id: "A123", total: 750}, {_id: "B212", total:200}]
```

或可用`$skip $match, $limit`





##### Map-Reduce

```
db.col.mapReduce(
				fucn
)
```







##### Single Purpose Aggregation Operations



* count()

  * cousor.count()  这个我们熟知
  * db.collection.count({a:1})  会返回a字段为1的样本

* distinct()

  返回一个字段先存在的可能情况：

  ```
  { a: 1, b: 0 }
  { a: 1, b: 1 }
  { a: 1, b: 1 }
  { a: 1, b: 4 }
  { a: 2, b: 2 }
  { a: 2, b: 2 }

  db.records.distinct( "b" )

  [ 0, 1, 4, 2 ]
  ```

  

* group()

  和sql的GROUP BY相似， 用法： db.col.group():

  ```
  {
    group:
     {
       ns: <namespace>,
       key: <key>,
       $reduce: <reduce function>,
       $keyf: <key function>,
       cond: <query>,
       finalize: <finalize function>
     }
  }
  ```

  

  ```
  eg：
  { a: 1, count: 4 }
  { a: 1, count: 2 }
  { a: 1, count: 4 }
  { a: 2, count: 3 }
  { a: 2, count: 1 }
  { a: 1, count: 5 }
  { a: 4, count: 4 }

  db.records.group( {
     key: { a: 1 },
     cond: { a: { $lt: 3 } },
     reduce: function(cur, result) { result.count += cur.count },
     initial: { count: 0 }
  } )

  [
    { a: 1, count: 15 },
    { a: 2, count: 4 }
  ]
  ```

  

  