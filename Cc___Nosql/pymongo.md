## pymongo

pymongo是mongo数据库和python中间的连接件，我们可以通过pip来下载：

`pip install pymongo`

使用mongo版本：2.6.10



#### 建立连接

```python
from pymongo import MongoClient
client = MongoClient('localhost',27017) #括号里不指定也是会用的默认连接
另一种方式：
client = MongoClient('mongodb://localhost:27017')
```



#### 访问数据库

`db = client.db_name`   我们可以像访问属性一样，访问一个数据库的名字

我更喜欢这种方式:  `db = client['db_name']`

如果数据库没有则创建，有就用它。

这两种方式都返回了Database类。



删除它：

`db.dn_name.drop()`



#### 访问集合

集合上我们一般不会用单独的步骤去访问集合，在插入语句中如果集合没有就会创建。

获取集合和上方的访问数据库相似：

```
collection = db.collection_name  
collection = db['collection_name'] 
```

都返回的是一个Collection集合类。



**注意**： MongoDB中关于集合(和数据库)的一个重要注意事项是它们是懒创建的 - 上述任何命令都没有在MongoDB服务器上实际执行任何操作。当第一个文档插入集合时才创建集合和数据库。



#### 操作文档

collection.do_something() = db.collection_name.do_something()

我们一直可以用collection.count() 来得到文档的数量。

##### 插入

* insert_one():

  `collection.insert_one( dict )` 

  上述返回`<pymongo.results.InsertOneResult>`  ,后可跟inserted_id 返回_id:

  `id=db.collection_name.insert_one({'dd':'ddd'}).inserted_id`

  本身id是Object对象id : ObjectId('59eff58feccbcd470f19b597')

  打印时会打印真的id,而不是对象。print id : 59eff58feccbcd470f19b597

  可以用ObjectId用于查找： 

  `collection.find_one({'_id':id})`


  旧版本不存在这个方法。

* insert():

  `collection.insert( dict )`

  返回ObjectId

  ​

* insert_many() 批量插入

  `collection.insert_many([{'aa':'aaa'},{'bb':'bbb'}])`  

  注意放入的是一个列表。

  `collection.insert_many([{'aa':'aaa'},{'bb':'bbb'}]).inserted.ids`

  返回`[ObjectId('59effa2eeccbcd470f19b59c'), ObjectId('59effa2eeccbcd470f19b59d')]`

  ​

##### 更新

update():

返回值一直是空的。

```
update(criteria, objNew, upsert, mult)
    criteria: 需要被更新的条件表达式
    objNew: 更新表达式
    upsert: 如目标记录不存在，是否插入新文档。
    multi: 是否更新多个文档。
    
    student.users.update({'gid':last_gid, 'time':l_date}, {'$set':{'gid':last_gid}, '$set':{'time':l_date}, '$addToSet':{'categories':category_data}}, upsert=True)
   #上式表示添加'categories'字段到gid=last_gid,time=l_date的这条记录中。
```

* `$set /$unset`设置/取消某个键的值：

  ` posts.update({"_id":post["_id"]},{"$set": {"content":"Test Update SET...."}})`

* $inc 自增

  `posts.update({"_id":post["_id"]},{"$inc":  {"views":1}})`

* $push,添加数组内的元素

  `posts.update({"_id":post["_id"]},{"$push":{"tags":"Test"}})`

* $addToSet,避免重复，只在数组中该元素不存在时才添加。

  $each 数组添加多个值

  `posts.update({"_id":post["_id"]},{"$addToSet": {"tags":{"$each":["Python","Each"]}}})`

* $pop 可以把数组看成队列，用pop来移除 数组中的元素

  `posts.update({"_id":post["_id"]},{"$pop":{"tags":1}})` 

  这个会删除tags里面最后一个，改成-1则删除第一个。

* $pull 来删除指定的值。它会删除数组中所有批判的值。

  $pullAll 删除所有符合的值：

  `db.users.update({'name':"user2"}, {'$pullAll':{'data':[3,5,6]}}) # 移除 3,5,6`

* $. 如果想修改数组中的一个值，可以先删除再添加。或者用美元符定位修改：

  `posts.update({"tags":"MongoDB"},{"$set":{"tags.$":"Hello"}})`

  这个将先搜索tags中满足”MongoDB”的，如果找到，就把它修改为”Hello”。可以看到上面的update这个函数已经有两个参数了，它还有第3个参数upsert，如果设为”True”，则如果没有找到匹配的文档，就会在匹配的基础上新建一个文档




更新多条：

在pymongo2.x中没有update_one(),update_many()等方法。而update()默认只更新一条记录。

在更新多条数据时，可以将参数：multi=True

`collection.update({'id':{'$gt':0}},{'$set':{'num':0}},multi=True)`

在3.x中可以使用:

`collection.update_many({'id':{'$gt':0}},{'$set':{'num':0}})`

3.x同样支持2.x的方式，但已经不建议使用了



更新所有： `collection.update({'id': {}, {'&set': {}}})`



##### 查询

* find_one()

  返回单个文档，如果没有匹配则返回None. 返回匹配的第一个文档

  注意当`collection.find_one({'_id':id})` 时，这个id一定时ObjectId类型，如果是str，记得转换：

  ```
  from bson.objectid import ObjectId
  id='xxxxxx'
  document = collection.find_one({'_id':ObjectId(id)})
  ```

* find() 

  返回的是一个Cursor对象，我们可以通过遍历它来得到找到的文档

  ```
  In [31]: collection.find()
  Out[31]: <pymongo.cursor.Cursor at 0x7f289dc688d0>

  In [32]: for x in collection.find():
     ....:     print x
     ....:     
  {u'dd': u'ddd', u'_id': ObjectId('59eff585eccbcd470f19b596')}
  {u'dd': u'ddd', u'_id': ObjectId('59eff58feccbcd470f19b597')}
  {u'aa': u'aaa', u'_id': ObjectId('59effa01eccbcd470f19b598')}
  ```
  ObjectId -> str :   str(ObjectId)

* `$gt,$lt`

  `cursor = db.restaurants.find({"grades.score": {"$gt": 30}})`

* $in

  `collection.find({"age":{"$in":(23, 26, 32)}})` 

* $all (全部包含)

  ```python
  # 两条数据：
   db.users.insert({'name':"user3", 'data':[1,2,3,4,5,6,7]})
   db.users.insert({'name':"user4", 'data':[1,2,3]})
  # 查找
   db.users.find({'data':{'$all':[2,3,4]}})  只会显示第一条数据
  ```

* $size 匹配数据属性元素数量

  `db.users.find({'data':{'$size':3}})` 只显示匹配数量的内容。

* $exists

  `collection.find({'sex':{'$exists':True}})` 存在sex键的

  `collection.find({'sex':{'$exists':False}})` 不存在sex键的

* and

  `cursor = collection.find({"cuisine": "Italian", "address.zipcode": "10075"})`

* or 

  `cursor = collection.find({"$or": [{"cuisine": "Italian", "address.zipcode": "10075"}]})`

* sort,skip,limit

  ```python
  cursor = collection.find().sort([
      ("borough", pymongo.ASCENDING),
      ("address.zipcode", pymongo.ASCENDING)
  ])
  ```

  * `pymongo.ASCENDING`表示升序排序。
  * `pymongo.DESCENDING`表示降序排序。

  `collection.find().skip(2).limit(3)` 从第几行开始读取(SLICE)，读取多少行(LIMIT)

* 正则表达

  `connection.find({"name" : {"$regex" : r"(?i)user[135]"}}, ["name"])` 

  查询出 name 为 user1, user3, user5 的

* 多级路径匹配

  ```
  u = 集合名.find_one({"im.qq":12345678})
  # 查询结果如：
  {"_id" : ObjectId("4c479885089df9b53474170a"), "name" : "user1", "im" : {"msn" : "user1@hotmail.com", "qq" : 12345678}}
  ```

* $type:  判断属性类型

  ```
  db.users.find({'t':{'$type':1}}): print u  # 查询数字类型的
  db.users.find({'t':{'$type':2}}): print u  # 查询字符串类型的
  类型值：
  		double:1
          string: 2
          object: 3
          array: 4
          binary data: 5
          object id: 7
          boolean: 8
          date: 9
          null: 10
          regular expression: 11
          javascript code: 13
          symbol: 14
          javascript code with scope: 15
          32-bit integer: 16
          timestamp: 17
          64-bit integer: 18
          min key: 255
          max key: 127
  ```

* $where 用JS代买来代替丑陋的lt.gt

  `db.users.find({"$where":"this.age > 7 || this.age < 3"})`

  `db.users.find().where("this.age > 7 || this.age < 3")`

* find_and_modify 

  没有找到，返回None,

  找到返回更改前的

  `c.user.user.find_and_modify({'_id':uname},update={'$set':{'key':data['sn']}})`

  ​

##### 删除

`collection.remove()`  删除改集合中的所有文档。

`collection.remove( dict )`   

`collection.remove( id )`



#### 索引





#### 技巧

##### cursor conver to json

```python
import pymongo
c = pymongo.MongoClient()
from bson.json_util import dumps
dumps(c.test.test.find())
'[{"_id": {"$oid": "555cb3a7fa5bd85b81d5a624"}}, {"_id": {"$oid": "555cb3a7fa5bd85b81d5a625"}}, {"_id": {"$oid": "555cb3a7fa5bd85b81d5a626"}}, {"_id": {"$oid": "555cb3a7fa5bd85b81d5a627"}}, {"_id": {"$oid": "555cb3a7fa5bd85b81d5a628"}}]'
```


##### ObjectId to str

`str(ObjectID)`



##### find时只返回特定字段

`.find({搜索条件}, {设置字段显示})`

eg: 

`c.user.info.find_one( {'name':'abc'} ,{"_id": 0, "username": 1, "foo": 1}) ` 

0为不显示该字段，1为显示该字段，设置字段显示时，其他字段默认为零。



