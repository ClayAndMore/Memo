Tags:[nosql, database, mongodb]



db（这是个命令，不是说它就是数据库）为默认数据库，默认数据库是test，存储在data目录中。

MongoDB的单个实例可以容纳多个独立的数据库，每一个都有自己的集合和权限，不同的数据库也放置在不同的文件中。

- show dbs 显示就所有数据列表
- db             显示当前数据库对象和集合。
- use  name 可以连接到指定数据库（name)
- show collections 显示集合
- help / db.help() / db.foo.help()

不启动mongod而启动mongo: `mongo --nodb`

用New Mongo(host)命令就可以连接到想要的mongod了。

```shell
>conn = new Mongo("somehost:3000")
connection to somehost:3000
>db=conn.getDB("myDB")
myDB
```

还有一些常用的命令： 

- db.collection.count() 看集合的数据条数, 注意：**当和limit一起用的时候count是返回符合条件的数。**
- db.collection.find().explain()  在语句后加explain可以看到执行时发生的过程。



### 创建

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



### 删除

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



### 插入

`db.collection_name.insert(document)`

如果collection_name 没有则创建。

插入文档你也可以使用 db.col.save(document) 命令。如果不指定 _id 字段 save() 方法类似于 insert() 方法。如果指定 _id 字段，则会更新该 _id 的数据。

```
var x = db.foo.findOne()
x.num = 42
db.foo.save(x) //如果没有save, 最后一行就有些繁琐了。
```



批量插入： `db.foo.batchInsert({"_id": 0},{"_id": 1})`

批量插入速度快于单条插入。

**如果其中某条失败，那么在该条之前的都插入成功，后面的都失败**

可以使用continueOnError选项， 跳过失败项，shell不支持，驱动都支持。

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



### 改

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



### findAndModify

匹配并更新，返回更新前的值。

db.col.findAndModify({条件}, {field:{key: value}})

fileld:

- update/remove, 匹配的文档从集合里更新/删除, 这两个字段必须选一个。
- new, 布尔类型， 表示返回更新前的文档还是更新后的文档，默认是更新前的文档。
- fields, 文档中需要返回的字段
- upsert ，布尔类型， 值为true时表示没有则创建，默认为false.



### 修改器

- `$set`, 改类型，改已存在或不存在， 改内嵌文档： `{"$set": {"author.name": "joe"}}`

- `$inc` , 增加或减少(传负数)，如果键不存在就创建一个，只能用于整型，长整型，或双浮点。

- `$push`,  数组末尾加一个新元素，如果没有就创建。

  - `$each` , 添加多个元素 ：`{"$push": {'hourly': {"$each": [1,2,3]}}}`

  - `$slice` , 保留几个元素，可形成队列： `{"$push":{"top10": "$each": ['a','b'], "$slice":-10}}`

    如果元素小于10，都会保留，如果大于10， 会去掉先加入的，保证该队列只有10个。slice必须是负整数。

  - `$sort`, 如果添加对象元素，数据对象可能会需要清理：

    ```
    {"$push": {"top10":{
    	"$each":[{'name':'a', 'rating':6.6},{'name':'b','rating':5}],
    	"$slice":-10,
    	"$sort":{"rating":-1}
    }}}
    根据rating的值，排序，保留前10个。
    ```

  - `$ne`, 保证原数组里没有，再加入：

    ```
    db.papers.update({"city": {"$ne": "beijing"}}, {"$push": {"city":"beijing"}})
    ```

- `$addToSet` 用于确保数组不重复更合适， 还可以增加多个值

  ```
  // 单值
  db.users.update({"_id": "dd"}, {"$addToSet": "aa@a.com"}
  // 多个值
  db.users.update({"_id": "dd"}, {"$addToSet":{
      "emails": {
          "$each": ["aa@a.com", "bb@b.com"],
      }
  } )
  ```

- `$pop`， 从数组尾部删除：`"$pop":{"key":1}`, 从头部：`"$pop":{"key":-1}`

- `$pull`:  指定位置删除： `"$pull": {"todo": "laundry"}`

- 数组中的下标

  ```
  // 增加一个评论的投票数量：
  db.blog.update({"post": post_id, "$inc": {"comments.0.votes": 1}})
  //  我们不知道下标的时候，比如我要改评论作者， 需要匹配它的值，使用$:
  db.blog.update({"comments.author": "John"}, {"$set": {"comments.$.author": "jim"}})
  ```

- `$setOnInsert`, 在创建文档时为某字段赋值，之后的所有更新操作中，这个值不再改变。

  `db.users.update({}, {"$setOnInsert":{"createdAt" new Date()}}, true)`





### 修改器速度

在不改变文档大小情况下，修改器的速度是很快的， 但是，改变大小后，原来的文档位置放不下，需要移动到后面。

**但是原来的位置空间就会空掉**，后续添加的文档都会有**填充因子**， 用于扩展文档。 移动的次数越多，扩展因子越大。

可以设置集合块大小都是2的幂：

`db.runCommand({}"collMod": collection, "usePowerOf2Size": true})`

这样适用于经常改集合大小的操作，如果只进行插入和原地更新的话，这个操作会导致写入速度变慢。



### 查询 

`db.collection_name.find(query,projection)`

- query ：可选，使用查询操作符指定查询条件，相当于where条件。
- projection ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）。

如果你需要以易读的方式来读取数据，可以使用 pretty() 方法，语法格式如下：

```
>db.col.find().pretty()
```

pretty() 方法以格式化的方式来显示所有文档。

除了 find() 方法之外，还有一个 findOne() 方法，它只返回一个文档。

指定返回的键：

`db.users.find({}"username":"joe"}, {username:1, age:1, "_id":0})`

1为返回，0为不返回。



#### 条件

mongodb的条件查询语句：

| 等于       | `{<key>:<value>`}        | `db.col.find({"by":"菜鸟教程"}).pretty()`   | `where by = '菜鸟教程'` |
| ---------- | ------------------------ | ------------------------------------------- | ----------------------- |
| 小于       | `{<key>:{$lt:<value>}}`  | `db.col.find({"likes":{$lt:50}}).pretty()`  | `where likes < 50`      |
| 小于或等于 | `{<key>:{$lte:<value>}}` | `db.col.find({"likes":{$lte:50}}).pretty()` | `where likes <= 50`     |
| 大于       | `{<key>:{$gt:<value>}}`  | `db.col.find({"likes":{$gt:50}}).pretty()`  | `where likes > 50`      |
| 大于或等于 | `{<key>:{$gte:<value>}}` | `db.col.find({"likes":{$gte:50}}).pretty()` | `where likes >= 50`     |
| 不等于     | `{<key>:{$ne:<value>}}`  | `db.col.find({"likes":{$ne:50}}).pretty()`  | `where likes != 50`     |

一些简写说明：

```
$gt -------- greater than  >
$gte --------- gt equal  >=
$lt -------- less than  <
$lte --------- lt equal  <=
$ne ----------- not equal  !=
$eq  --------  equal  =
```



其他条件：

- `$ne`,  不等于，适用于所有类型数据。 `db.users.find({"username": {"$ne": "joe"}})`

- `$and`  等于，逗号：`db.col.find({"by":"菜鸟教程", "title":"MongoDB 教程"}).pretty()`

  `db.col.find({$and:[{"by":"菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()`

- or 条件，`db.col.find({$or:[{"by":"菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()`

- 联合：`db.col.find({"likes": {$gt:50}, $or: [{"by": "菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()`

- `$in`,  `db.raffle.find({"ticket_no": {"$in": [1,2,3]}})`,  中奖号码1，2，3

- `$nin`,  不在某个范围。

- `$not`, 元条件语句， 可以在任意条件之上， 

- `$regex`, 正则 `db.posts.find({post_text:{$regex:"runoob"}})`,  也可以写为 `db.posts.find({post_text:/runoob/})`

我们可以发现， $lt在内层文档， ￥inc在外层文档，

so,**条件语句是内层文档的键， 修改器是外层文档的键**



#### 特定类型的查询

如下文档：

```
db.c.find()
{"_id": xx, "y": null}
{"_id": xx, "y": 1}
{"_id": xx, "y": 2}
```

如果查询y为null的文档， db.c.find({"y": null}),确实能返回该值，但是我们执行如下语句：`db.c.find({"z": null})`,

会返回文档中所有文档，因为**这种匹配还会返回缺少这个键的所有文档**

所以正确方法是既要检查该键的值为null,还要检查该键是否存在：

`db.c.find({"z": {"$in":[null], "$exists": true}})`



#### 查询数组

`db.food.insert({"fruit":["apple", "banana", "peach"]})`

* 数组中查找： `db.food.find({"fruit": "banana"})`

* `$all`, 找到既有“apple”, 又有“banana”的文档：`db.food.find({fruit:{$all: {"apple", "banana"}}})`

* 查询数组特定位置，使用key.index语法指定下标：`db.food.find({"fruit.2": "peach"})` 

* `$slice`, 可以返回某个键匹配的数组的一个字集，

  ```
  db.blog.posts.findOne(crit, "comments": {"$slice": 10} ) //返回前10条评论， -10后十条
  ```

* `$elemMatch`  当内嵌的是对象时, 需要操作多个键时会用到：

  ```
  //现有文档：
  {
      "content":"...",
      "comments": [
          {
          	"author": "joe",
          	"score": 3,
          	"comment": "Nice post"
          },
          {
              "author": "mary",
              "score": 6,
              "comment": "terrible post"
          }
      ]
  }
  // 查询条件， 找到由job发表的5分以上的评论
  db.blog.find({"comments": {
      "$elemMatch": {
          "author": "joe",
          "score": {"$gte": 5}
      }
  }})
  ```




#### $type操作符

检索数据的类型。如：

获取 "col" 集合中 title 为 String 的数据，你可以使用以下命令：

```
db.col.find({"title" : {$type : 2}})
```

类型和对应数字：

Double-1，String-2, Object-3, Array-4, Binary data-5, Objectid-7, Boolean-8,Date-9,Null-10

其他略。可查http://www.runoob.com/mongodb/mongodb-operators-type.html





### 快照

我们经常对数据库的操作是把数据取出来，然后做一些操作，最后再存进去：

```
cursor = db.foo.find();
while (cursor.hasNext()) {
    var doc = cursor.next();
    doc = process(doc);
    db.foo.save(doc);
}
```

如果结果比较少，没有什么问题，如果结果比较大，可能会多次返回同一个结果。

当使文档体积变大时，预留空间不够，会把它移动到末尾，这样就有可能再次被遍历到。

应当这个问题就是对查询使用快照（snapshot）, 查询会在id索引上遍历执行，保证每个文档只会返回一次：

`db.foo.find().snapshot()`