
---
title: "08-redis-py.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
tags:[消息队列, nosql, database, Redis, python]

### redis-py

GitHub: //github .com/andymccurdy redis-py
官方文档 https: //redis-py.rea dthedocs.io

pip 安装
pip3 install redis
为了验证 redis-py 库是否已经安装成功，可以在命令行下测试 下：

```python
>>> import redis
>>> redis.VERSION
(3, 0, 1)
```



#### Get start

```python
>>> import redis
>>> r = redis.Redis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
'bar'
```



**redis-py 3.0 only accepts user data as bytes, strings or numbers (ints, longs and floats).** 

**Attempting to specify a key or a value as any other type will raise a DataError exception.**



#### Connection Pools

```
>>> pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
>>> r = redis.Redis(connection_pool=pool)
```

减少连接实例



#### Thread Safety

如果用多个redis数据库在相同的应用， 需要创建分离的客户端实例（提供分离的连接池为每个数据库。）

pubsub 或 pipeline 在两个线程间不是安全的。



### 连接方式

使用python连接redis有三种方式：

1. 使用库中的Redis类（或StrictRedis类，其实差不多）；
2. 使用ConnectionPool连接池（可保持长连接）；
3. 使用Sentinel类（如果有多个redis做集群时，程序会自己选择一个合适的连接）。