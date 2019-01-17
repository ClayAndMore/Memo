### redis-py

GitHub: ://g ithub .com/andymccurdy redis-py
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