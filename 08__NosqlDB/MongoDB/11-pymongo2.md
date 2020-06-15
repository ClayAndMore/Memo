
---
title: "11-pymongo2.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[nosql, database, mongodb, python]

### db.command

向mongodb 发送一个命令。

```
 db.command("buildinfo")  # 实际发送的是{buildinfo: 1}
 db.command("collstats", collection_name) 
 #实际发送的是{collstats: collection_name}， 查询某个集合的状态
 
 >>> c.file.command('dbstats')   # 查询数据库的状态
{u'storageSize': 262144, u'indexStorageSize': 1573376, u'avgObjSize': 510.27450980392155, u'db': u'file', u'indexes': 46, u'objects': 102, u'collections': 7, u'ok': 1.0, u'dataSize': 52048, u'indexSize': 5983}

```





### 聚合



eg:

```python
{"user": "adam", "position": "attacker", "goals": 8}
{"user": "bart", "position": "midfielder", "goals": 3}
{"user": "cedric", "position": "goalkeeper", "goals": 1}

pipe = [{'$group': {'_id': None, 'total': {'$sum': '$goals'}}}]
db.goals.aggregate(pipeline=pipe)

Out[8]: {u'ok': 1.0, u'result': [{u'_id': None, u'total': 12.0}]}
```







### statistics

```python
from pymongo import MongoClient

client = MongoClient()
db = client.test

# print collection statistics
print db.command("collstats", "col_name") 

# print database statistics
print db.command("dbstats")
```

上述打印出来的大小单位为Bytes

