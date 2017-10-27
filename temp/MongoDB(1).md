### 写在前面

MongoDB 是由C++语言编写的，是一个基于**分布式**文件存储的开源数据库系统。

MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。文档结构类似与json对象。

但是我们mongodb的数据存储格式叫： BSON

BSON和JSON的区别：

* 更快的遍历速度：对JSON格式来说，太大的JSON结构会导致数据遍历非常慢。在JSON中，要跳过一个文档进行数据读取，需要对此文档进行扫描才行，需要进行麻烦的[数据结构匹配，比如括号的匹配，而BSON对JSON的一大改进就是，它会将JSON的每一个元素的长度存在元素的头部，这样你只需要读取到元素长度就能直接seek到指定的点上进行读取了。
* 存储变化： 对JSON来说，数据存储是无类型的，比如你要修改基本一个值，从9到10，由于从一个字符变成了两个，所以可能其后面的所有内容都需要往后移一位才可以。而使用BSON，你可以指定这个列为数字列，那么无论数字从9长到10还是100，我们都只是在存储数字的那一位上进行修改，不会导致数据总长变大。当然，在MongoDB中，如果数字从整形增大到长整型，还是会导致数据总长变大的。
* 增加额外数据类型。 JSON是一个很方便的数据交换格式，但是其类型比较有限。BSON在其基础上增加了“byte array”数据类型。这使得二进制的存储不再需要先base64转换后再存成JSON。大大减少了计算开销和数据大小。

当然这些优点，会牺牲掉空间。

### 安装和配置

ubuntu：

`apt-get install -y mongodb`

默认安装在了： `/usr/bin/` 下。

在该路径下：

`./mongod` 可运行MongoDB服务。

`./mongo`   运行MongoDB后台管理shell,它是自带的js shell,当进入时，会默认链接到test文档（数据库）。

eg:

```
$ cd /usr/local/mongodb/bin
$ ./mongo
MongoDB shell version: 3.0.6
connecting to: test
Welcome to the MongoDB shell.
……
> db.runoob.insert({x:10})
WriteResult({ "nInserted" : 1 })
> db.runoob.find()
{ "_id" : ObjectId("5604ff74a274a611b0c990aa"), "x" : 10 }
>
```





### 使用和命令

db（这是个命令，不是说它就是数据库）为默认数据库，默认数据库是test，存储在data目录中。

MongoDB的单个实例可以容纳多个独立的数据库，每一个都有自己的集合和权限，不同的数据库也放置在不同的文件中。

* show dbs 显示就所有数据列表
* db             显示当前数据库对象和集合。
* use  name 可以连接到指定数据库（name)
* show collections 显示集合

数据库也通过名字来标识。数据库名可以是满足以下条件的任意UTF-8字符串。

- 不能是空字符串（"")。
- 不得含有' '（空格)、.、$、/、\和\0 (空字符)。
- 应全部小写。
- 最多64字节。

有一些数据库名是保留的，可以直接访问这些有特殊作用的数据库。

- **admin**： 从权限的角度来看，这是"root"数据库。要是将一个用户添加到这个数据库，这个用户自动继承所有数据库的权限。一些特定的服务器端命令也只能从这个数据库运行，比如列出所有的数据库或者关闭服务器。
- **local:** 这个数据永远不会被复制，可以用来存储限于本地单台服务器的任意集合
- **config**: 当Mongo用于分片设置时，config数据库在内部使用，用于保存分片的相关信息。




还有一些常用的命令： 

* db.collection.count() 看集合的数据条数
* db.collection.find().explain()  在语句后加explain可以看到执行时发生的过程。



#### 创建

use:

```
> use firstdb                                                   
switched to db firstdb                                             
> db                                                              
firstdb                                                                
>   
```

这时用`show dbs` 并不会看到刚才创建的数据库，因为没有数据,插入数据：

```
> db.firstdb.insert({'name':'firstdata'})                    
WriteResult({ "nInserted" : 1 })                              
> show dbs                                                         vmlinuz.old
admin    (empty)                                           
firstdb  0.078GB                                           
local    0.078GB                                                     
test     0.078GB                                                      
>                                                                    
```

一般我们不需要创建集合，集合在插入时没有则自动创建。



#### 删除

MongoDB 删除数据库的语法格式如下：

```
db.dropDatabase()
```

删除当前数据库，默认为 test，你可以使用 db 命令查看当前数据库名。



`db.collection.remove(<query>,<justOne>)`

2,6版以后的为：

```
db.collection.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
```

- **query **:（可选）删除的文档的条件。
- **justOne **: （可选）如果设为 true 或 1，则只删除一个文档。
- **writeConcern **:（可选）抛出异常的级别。

接下来我们移除 title 为 'MongoDB 教程' 的文档：

```
>db.col.remove({'title':'MongoDB 教程'})
WriteResult({ "nRemoved" : 2 })           # 删除了两条数据
>db.col.find()
……                                        # 没有数据
```

如果你只想删除第一条找到的记录可以设置 justOne 为 1，如下所示：

```
>db.COLLECTION_NAME.remove(DELETION_CRITERIA,1)
```

如果你想删除所有数据，可以使用以下方式（类似常规 SQL 的 truncate 命令）：

```
>db.col.remove({})
>db.col.find()
>
```



#### 插入

`db.collection_name.insert(document)`

如果collection_name 没有则创建。

插入文档你也可以使用 db.col.save(document) 命令。如果不指定 _id 字段 save() 方法类似于 insert() 方法。如果指定 _id 字段，则会更新该 _id 的数据。



3.2 版本后还有以下几种语法可用于插入文档:

- db.collection.insertOne():向指定集合中插入一条文档数据
- db.collection.insertMany():向指定集合中插入多条文档数据

```
#  插入单条数据

> var document = db.collection.insertOne({"a": 3})
> document
{
        "acknowledged" : true,
        "insertedId" : ObjectId("571a218011a82a1d94c02333")
}

#  插入多条数据
> var res = db.collection.insertMany([{"b": 3}, {'c': 4}])
> res
{
        "acknowledged" : true,
        "insertedIds" : [
                ObjectId("571a22a911a82a1d94c02337"),
                ObjectId("571a22a911a82a1d94c02338")
        ]
}
```



#### 改

```
db.collection.update(
   <query>,      update的查询条件，类似sql update查询内where后面的。
   <update>,     update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的
   {
     upsert: <boolean>, 可选，如果不存在update的记录，是否插入objNew. true为插入，默认是false，不插入。
     multi: <boolean>, 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新。
     writeConcern: <document>  可选，抛出异常的级别
   }
)
```

eg:

```
>db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })   # 输出信息
> db.col.find().pretty()
{
        "_id" : ObjectId("56064f89ade2f21f36b03136"),
        "title" : "MongoDB",
        "description" : "MongoDB 是一个 Nosql 数据库",
        "tags" : [
                "mongodb",
                "database",
                "NoSQL"
        ],
        "likes" : 100
}
>
可以看到标题(title)由原来的 "MongoDB 教程" 更新为了 "MongoDB"。
以上语句只会修改第一条发现的文档，如果你要修改多条相同的文档，则需要设置 multi 参数为 true。
>db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},{multi:true})
```





#### 查看

`db.collection_name.find(query,projection)`

- query ：可选，使用查询操作符指定查询条件，相当于where条件。
- projection ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）。

如果你需要以易读的方式来读取数据，可以使用 pretty() 方法，语法格式如下：

```
>db.col.find().pretty()
```

pretty() 方法以格式化的方式来显示所有文档。

除了 find() 方法之外，还有一个 findOne() 方法，它只返回一个文档。



#### 条件

mongodb的条件查询语句：

| 等于    | `{<key>:<value>`}        | `db.col.find({"by":"菜鸟教程"}).pretty()`    | `where by = '菜鸟教程'` |
| ----- | ------------------------ | ---------------------------------------- | ------------------- |
| 小于    | `{<key>:{$lt:<value>}}`  | `db.col.find({"likes":{$lt:50}}).pretty()` | `where likes < 50`  |
| 小于或等于 | `{<key>:{$lte:<value>}}` | `db.col.find({"likes":{$lte:50}}).pretty()` | `where likes <= 50` |
| 大于    | `{<key>:{$gt:<value>}}`  | `db.col.find({"likes":{$gt:50}}).pretty()` | `where likes > 50`  |
| 大于或等于 | `{<key>:{$gte:<value>}}` | `db.col.find({"likes":{$gte:50}}).pretty()` | `where likes >= 50` |
| 不等于   | `{<key>:{$ne:<value>}}`  | `db.col.find({"likes":{$ne:50}}).pretty()` | `where likes != 50` |

一些简写说明：

```
$gt -------- greater than  >
$gte --------- gt equal  >=
$lt -------- less than  <
$lte --------- lt equal  <=
$ne ----------- not equal  !=
$eq  --------  equal  =
```





and条件：逗号：

`db.col.find({"by":"菜鸟教程", "title":"MongoDB 教程"}).pretty()`

对应sql:`WHERE by='菜鸟教程' AND title='MongoDB 教程'`

or 条件，`db.col.find({$or:[{"by":"菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()`

联合：`db.col.find({"likes": {$gt:50}, $or: [{"by": "菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()`

对应sql:`where likes>50 AND (by = '菜鸟教程' OR title = 'MongoDB 教程')`

#### $type操作符

检索数据的类型。如：

获取 "col" 集合中 title 为 String 的数据，你可以使用以下命令：

```
db.col.find({"title" : {$type : 2}})
```

类型和对应数字：

Double-1，String-2, Object-3, Array-4, Binary data-5, Objectid-7, Boolean-8,Date-9,Null-10

其他略。可查http://www.runoob.com/mongodb/mongodb-operators-type.html



### 集合

* 集合collection：

  ```
  {"site":"www.baidu.com"}
  {"site":"www.google.com","name":"Google"}
  {"site":"www.runoob.com","name":"菜鸟教程","num":5}
  ```
  类似于表（tables)。

  删除集合： 

  ```
  db.collection.drop()
  ```

  以下实例删除了 runoob 数据库中的集合 site：

  ```
  > use runoob
  switched to db runoob
  > show tables
  site
  > db.site.drop()
  true
  > show tables
  > 
  ```
  清空集合，删除所有文档，但是保留集合：

  `db.collection.remove()`

* capped collections

  为固定大小的collection.

  它有很高的性能以及队列过期的特性(过期按照插入的顺序). 

  必须要显式的创建一个capped collection， 指定一个collection的大小，单位是字节。collection的数据存储空间值提前分配的。


  `db.createCollection("mycoll", {capped:true, size:100000})`

* 元数据

  数据库的信息存在集合中，使用了系统的命名空间：

  | 集合命名空间                   | 描述                      |
  | ------------------------ | ----------------------- |
  | dbname.system.namespaces | 列出所有名字空间。               |
  | dbname.system.indexes    | 列出所有索引。                 |
  | dbname.system.profile    | 包含数据库概要(profile)信息。     |
  | dbname.system.users      | 列出所有可访问数据库的用户。          |
  | dbname.local.sources     | 包含复制对端（slave）的服务器信息和状态。 |




### 常用类型

| 数据类型               | 描述                                       |
| ------------------ | ---------------------------------------- |
| String             | 字符串。存储数据常用的数据类型。在 MongoDB 中，UTF-8 编码的字符串才是合法的。 |
| Integer            | 整型数值。用于存储数值。根据你所采用的服务器，可分为 32 位或 64 位。   |
| Boolean            | 布尔值。用于存储布尔值（真/假）。                        |
| Double             | 双精度浮点值。用于存储浮点值。                          |
| Min/Max keys       | 将一个值与 BSON（二进制的 JSON）元素的最低值和最高值相对比。      |
| Arrays             | 用于将数组或列表或多个值存储为一个键。                      |
| Timestamp          | 时间戳。记录文档修改或添加的具体时间。                      |
| Object             | 用于内嵌文档。                                  |
| Null               | 用于创建空值。                                  |
| Symbol             | 符号。该数据类型基本上等同于字符串类型，但不同的是，它一般用于采用特殊符号类型的语言。 |
| Date               | 日期时间。用 UNIX 时间格式来存储当前日期或时间。你可以指定自己的日期时间：创建 Date 对象，传入年月日信息。 |
| Object ID          | 对象 ID。用于创建文档的 ID。                        |
| Binary Data        | 二进制数据。用于存储二进制数据。                         |
| Code               | 代码类型。用于在文档中存储 JavaScript 代码。             |
| Regular expression | 正则表达式类型。用于存储正则表达式。                       |



### 方法

#### limit

返回记录条数，

eg:

```
> db.col.find({},{"title":1,_id:0}).limit(2)
{ "title" : "PHP 教程" }
{ "title" : "Java 教程" }
>
```

第一个{}表示where条件，为空则返回所有文档。

第二个{}表示制定哪些列显示和不显示（0不显示，1显示），如果都没有制定，则表示显示所有。

#### skip

跳过指定数量数据，

想要读取从 10 条记录后 100 条记录，相当于 sql 中limit (10,100)。

```
> db.COLLECTION_NAME.find().skip(10).limit(100)
```

以上实例在集合中跳过前面 10 条返回 100 条数据。

skip 和 limit 结合就能实现分页。

#### sort

sort()方法对数据进行排序，sort()方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序排列，而-1是用于降序排列。

```
>db.COLLECTION_NAME.find().sort({KEY:1})
```

KEY是字段名称。

当查询时同时使用sort,skip,limit，无论位置先后，最先执行顺序 sort再skip再limit。

#### aggregate（聚合）

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
| ---------------------------------------- |
| $avg      | 计算平均值                   | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$avg : "$likes"}}}]) |
| $min      | 获取集合中所有文档对应值得最小值。       | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$min : "$likes"}}}]) |
| $max      | 获取集合中所有文档对应值得最大值。       | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}]) |
| $push     | 在结果文档中插入值到一个数组中。        | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$push: "$url"}}}]) |
| $addToSet | 在结果文档中插入值到一个数组中，但不创建副本。 | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$addToSet : "$url"}}}]) |
| $first    | 根据资源文档的排序获取第一个文档数据。     | db.mycol.aggregate([{$group : {_id : "$by_user", first_url : {$first : "$url"}}}]) |
| $last     | 根据资源文档的排序获取最后一个文档数据     | db.mycol.aggregate([{$group : {_id : "$by_user", last_url : {$last : "$url"}}}]) |



在聚合函数中是可以管道操作的：http://www.runoob.com/mongodb/mongodb-aggregate.html



### 索引

索引可以理解为一本书的目录，这样就能更快的找到我们的要的内容。



### 副本集（复制）

就是数据备份，一台主节点负责和客户端交互数据，从节点负责定期轮询主节点，获取主节点的操作然后对自己的数据操作，保持数据的一致。

特点是当主节点宕机，其他节点都自动可以当作主节点，保证服务运行。



### 分片

**基本思想**就是将集合切成小块，这些块分散到若干片里，每个片只负责总数据的一部分，最后通过一个均衡器来对各个分片进行均衡（数据迁移）。通过一个名为mongos的路由进程进行操作，mongos知道数据和片的对应关系（通过配置服务器）。大部分使用场景都是解决磁盘空间的问题，对于写入有可能会变差。