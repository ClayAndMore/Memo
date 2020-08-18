---
title: "06-mongodb索引.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Mongodb"]
categories: ["Nosql"]
author: "Claymore"

---


## 索引

索引可以理解为一本书的目录，这样就能更快的找到我们的要的内容。

创建索引需要使用文档的附加结构，**在一个集合中只放入一种类型的文档，可以更有效地对集合进行索引**，



### 创建

`db.users.ensureIndex({"username": 1})`

1 升序，从最小到最大， -1降序。

创建索引根据机器性能需要几分钟时间， 可以在另一个shell中db.currentOp()或者检查mongod日志来查看索引创建进度。

对于每添加一个索引，每次写操作（插入，更新，删除）都会消耗更多时间，因为没更新一个文档还要更新文档的所有索引。

索引值是按照一定顺序排列的，所以使用索引键对文档排序非常快，如果按照索引查询， 查询结果则是按照索引顺序排列的，可以不用再排列。



### 复合索引

`db.user.ensureIndex({"age": 1, "username": 1})`

索引先按age排序，相同age再按username排序。索引大概是这个样子：

```
[15, user1003] -> 0xOc965234 // 年龄， 用户，-> 硬盘wwv
[15, user1004] -> 0xOc933d34
[15, user1014] -> 0xOc965234
...
[60, user8992] -> 0xOc96d234
```

三种对上述索引的主要操作：

```js
1. 单值操作
db.users.find({"age": 21}).sort({"username": -1}) 
// 由于username在21处已经排序，所以只需要从后往前反数据就可以, 上述是一个高效操作。
2. 多值查询
db.users.find({"age": {"$gte": 21, "$lte": 30}}))
// 会使用第一个索引键来查询，没什么问题
3. 排序的多值查询
db.users.find({"age": {"$gte": 21, "$lte": 30}}).sort({"username":1})
//username此时并不是有序的,因为有多个age, 会在内存中排序再返回，没有上面高效

上面的使用的索引是{"age": 1, "username": 1}， 针对第三种我们使用相反的索引：｛"username": 1，"age": 1｝会怎么样呢？

相反的索引会在以username为顺序逐项检查符合age的条件，会遍历一遍所有， 但是遍历后结果不用再排序。

```

针对上面的情况，我们可以强制使用特定的索引： hint

```js
db.user.find({"age": {"$gte": 21, "$lte": 30}})
    .sort({"username":1})
	.hint({"username": 1, "age":1}) //强制使用索引

这样查会很慢很慢， 如果情况3花费3s， 上面的情况可能会有15s.
但是如果加上limit限制，比如后面都加上limit(1000), 新的赢家就产生了：
如情况3花费2s, 那么加上限制的上面只有不到1/5s.
```



#### 覆盖索引

如果查询只需要返回索引中的字段，没有必要返回文档。

这样不用去获取实际的文档。推荐使用。

比如上例中只返回索引`{_id:0, username:1, age:1}` 

explan()的indexOnly字段。



#### 隐式索引

```
{"age": 1, "username": 1} 索引， age字段会字段排序， 可以和{"age": 1}索引一样使用

如果我有{"a":1, "b":1, "c":1, "d":1, "e":1} 索引， 那么我可以使用{"a": 1, "b": 1},{"a":1,"b":1,"c":1}等索引。
但是不能使用{"a":1, "c":1}
```

**只有使用索引前缀的查询才可以从中受益**



### 唯一索引

唯一索引：`db.users.ensureIndex({"username": 1},{'unique':true})`

复合唯一索引，`db.users.ensureIndex({"username": 1，"age": 1},{'unique':true})`

两个值组合不能一样。

去除重复，在已有的集合上创建唯一索引时可能会失败，因为集合中可能已经存在重复键。

可以使用语句去除重复内容，或者使用dropDups保留第一个。之后重复的文档都会被删除：

`db.people.ensureIndex({"username":1}, {"unique": true,"dropDups": true})`

这种方式比较粗暴。



### 稀疏索引

如果唯一索引在某个文档中不存在，是不能插入集合的。

但是我们希望当这个键存在时是唯一的，不存在也可以加入，这时需要unique和sparse

使用sparse 就可以创建稀疏索引。

如有一个可选的email字段，如果提供了这个字段，那么它的值必须是唯一的：

`db.ensureIndex({"email": 1}, {"unique": true, "sparse": true})`

**稀疏索引并不必是唯一的**， 去掉unique选项，就可以创建一个非唯一的稀疏索引。



### 哈希索引

不同于传统的B-树索引,哈希索引使用hash函数来创建索引。
例如:`db.users.createIndex({username : 'hashed'});`

* 在索引字段上进行精确匹配,但不支持范围查询,不支持多键hash；
*  Hash索引上的入口是均匀分布的,在分片集合中非常有用；



### 操作符中使用索引

#### 低效率的操作符

`$where` 和 `$exists` 完全无法使用索引，

`$ne` 可以使用索引，但不是很高效

`$not`, 大多数not会退化为全表扫描。



#### 范围

如 gt, lt等范围操作符，

针对于复合索引来说， 将索引前缀用于精确匹配，后面用于范围，如：

```
索引： {"age": 1, "username": 1}
db.users.find({"age": 47, "username": {"$gt": "user5", "$lt": "user8"}})
```

如果索引反过来，那么，会糟糕一些，遍历索引条目会多一些。



####  OR

Mongo只能在一次查询中使用一个索引， 如果你在{"x": 1} 和 {"y":1}上都有索引， 在{"x": 123, "y":342}上搜索时会使用一个索引，但是or是个例外，可以对每个子句使用各自的索引，它本质是两次查询结果的合集。

`db.foo.find({"$or": [{"x":123, {"y": 456}}]}`)

但是通常来说，两次的结果不如用一次in的效率高。



### 索引对象和数组

mongo准许在文档内部做索引，如字典和数组

#### 内嵌文档

```js
{
    username: sid
    loc: {
        ip: 1,1,1,1
        city:: beijing
    }
}

db.users.ensureIndex({"loc.city": 1})
```

对于loc建索引和loc.city索引的效果是不同的，对子文档建索引只会提高子文档的速度。

#### 数组

```
{
    username: sid
    loc: {
    	[
         	ip: 1,1,1,1,
        	city:: beijing 
    	],
    	[
         	ip: 1,1,1,1,
        	city:: tianjing 
    	]
    }
}

db.users.ensureIndex({"loc.city": 1}) //对子数组建立索引
```

对数组建立索引，其实是对数组中的每个元素建立一个索引条目，而不是对数组本身建立索引。



#### 多键索引

如果一个索引的字段在某个文档中是数组，那么这个索引就被标记为多键索引。

即使所有该字段的数组文档删除，也不会恢复为非多键索引。

多键索引会比索引慢一些。

explan()的isMultikey字段。



### 查询优化器

如果同时有好几个索引都适合你的查询，每次查询都不是单纯的一个执行方案，mongo后台会并行执行几个查询计划，谁先返回就用谁的，explain()的 allPlans字段显示了本次查询尝试过的计划。



### 索引基数/颗粒

如果发现查询时间相对长，那么就需要做优化。首选就是为待查询的字段建立索引，不过需要特别注意的是，索引不是万能灵药。如果需要查询超过一半的集合数据，索引还不如直接遍历来的好。

索引的原理是通过建立指定字段的B树，通过搜索B树来查找对应document的地址。这也就解释了如果需要查询超过一半的集合数据，直接遍历省去了搜索B树的过程，效率反而会高。

关于索引，索引列颗粒越小越好，什么叫颗粒越小越好？在索引列中每个数据的重复数量称为颗粒，也叫作索引的基数。如果数据的颗粒过大，索引就无法发挥该有的性能。例如，我们拥有一个"age"列索引，如果在"age"列中，20岁占了50%，如果现在要查询一个20岁，名叫"Tom"的人，我们则需要在表的50%的数据中查询，索引的作用大大降低。所以，我们在建立索引时要尽量将数据颗粒小的列放在索引左侧，以保证索引发挥最大的作用。





### 使用explain()和hint()

```js
>db.users.find({"age":42}).explain()
{
    "cursor": "BtreeCursor age_1_username_1",  //使用的索引 {age:1, username:1}
    "isMultiKey": false, // 是否使用多键索引
    "n": 8332,  //实际返回的文档数量。
    "nscannedObjects":8332,  //所扫描文档数量。
    "nscanded":8332,  //索引条目
    "nscandedObejectsAllPlans: 8332,
    "nscandedAllPlans: 8332,
    "scanAndOrder": false, //对结果集进行排序。
    "indexOnly": false, //覆盖索引 
    "nYields": 0, // 本次操作暂停的次数，如有写入请求，会有暂停操作。
    "nChunkSkips": 0,
    "millis": 91, //查询执行速度，如果有多个查询计划，那么这个不是我们希望看到的最优时间。
    "indexBounds":{ //索引使用情况， age从42到42精确查找，username没有限制，负无穷到正无穷。
        "age": [
            [
                42,
                42
            ]
        ],
        "username": [
            [
                { "minElement": 1},
                { "maxElement": 1}
            ]
        ]
    }
    "server": "ubuntu:27017"
}
```



如果发现Mongo使用的索引和你希望使用的不一致，可以用hint强制使用某个索引：

`db.c.find({"age": 14, "username": /.*/}).hint("username": 1, "age": 1)`



### 何时不应该使用索引

* 数据集教小
* 结果集在原数据集所占比例教大
* 非选择性查询，没有条件，需要做全表扫描。



{"$natural": 1}强制数据库做全表扫描， 按照磁盘顺序读取，适用于只插入的集合。

那样我们就可以一直拿最新的或者最早的这样需求的数据。



### 管理索引

所有等索引信息都存储在system.indexes集合中， 只能通过ensureIndex或dropIndexes对其操作。

不能直接插入或删除。

* `db.col.getIndexes()` 来看指定集合上的所有索引信息。

* 每一个索引都有自己的名称

  默认是keyname1_dir1_keyname2_dir2_..

  如果包含很多索引这种名字就比较笨重，我们可以标识索引：

  `do.foo.ensureIndex({a:1,b:1,c:1}, {"name": "abc"})`

* 如下索引：

  ```
     {
        "v" : 1,
        "key" : { "cat" : -1 },
        "ns" : "test.pets",
        "name" : "catIdx"
     },
  ```

#### 创建索引

`db.collection.createIndex(keys, options)`

语法中 Key 值为要创建的索引字段,1为指定按升序创建索引,如果你想按降序来创建索引指定为-1,也可以指定为hashed（哈希索引）

options: 

| 属性名     | 类型    | 说明                                                         |
| ---------- | ------- | ------------------------------------------------------------ |
| background | boolean | 是否在后台创建索引，在生产环境中，如果数据量太大，构建索引可能会消耗很长时间，为了不影响业务，可以加上此参数，后台运行会为其他操作让路 |
| unique     | bollean | 是否为唯一索引                                               |
| name       | string  | 索引名字                                                     |
| sparse     | boolean | 是否为稀疏索引，索引仅引用具有指定字段的文档                 |

 单键唯一索引:db.users. createIndex({username :1},{unique:true});
 单键唯一稀疏索引:db.users. createIndex({username :1},{unique:true,sparse:true});
 复合唯一稀疏索引:db.users. createIndex({username:1,age:-1},{unique:true,sparse:true});
 创建哈希索引并后台运行:db.users. createIndex({username :'hashed'},{background:true});

#### 删除索引

  删除索引： `db.people.dropIndex("catIdx")`  , 参数name

  或者`db.pets.dropIndex( { "cat" : -1 } )`

 根据索引名字删除某一个指定索引:db.users.dropIndex("username_1");
 删除某集合上所有索引:db.users.dropIndexs();
 重建某集合上所有索引:db.users.reIndex();
 查询集合上所有索引:db.users.getIndexes();

