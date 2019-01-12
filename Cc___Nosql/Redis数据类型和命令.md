

### 数据类型

#### String

string是redis最基本的类型，一个key对应一个value。一个键最大能存储512MB.

string类型是二进制安全的。意思是redis的string可以包含任何数据。比如jpg图片或者序列化的对象 。

```shell
127.0.0.1:6379> set name "dachui"
OK
127.0.0.1:6379> get name
"dachui"
```



#### Hash

Redis hash 是一个键值对集合。每个 hash 可以存储 2(32 - 1) 键值对（40多亿）

Redis hash是一个string类型的field和value的映射表，hash特别适合用于存储对象。

```shell
127.0.0.1:6379> hmset user:1 name dachui pass 123456
OK
127.0.0.1:6379> hgetall user:1
1) "name"
2) "dachui"
3) "pass"
4) "123456"
```



#### List

Redis 列表是简单的字符串列表，按照插入顺序排序。

列表最多可存储 2(32 - 1) 元素 (4294967295, 每个列表可存储40多亿)。

你可以添加一个元素导列表的头部（左边）或者尾部（右边）。

```shell
127.0.0.1:6379> lpush list1 wo shi da chui
(integer) 4

127.0.0.1:6379> lrange list1 0 10
1) "chui"
2) "da"
3) "shi"
4) "wo"
```



#### Set(集合)

Redis的Set是string类型的无序集合。

集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。

集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)

添加一个string元素到,key对应的set集合中，成功返回1,如果元素以及在集合中返回0,key对应的set不存在返回错误。

```shell
127.0.0.1:6379> sadd set1 wo
(integer) 1
127.0.0.1:6379> sadd set1 shi
(integer) 1
127.0.0.1:6379> sadd set1 da
(integer) 1
127.0.0.1:6379> sadd set1 chui
(integer) 1
127.0.0.1:6379> sadd set1 chui
(integer) 0
127.0.0.1:6379> smembes set1
(error) ERR unknown command `smembes`, with args beginning with: `set1`, 
127.0.0.1:6379> smembers set1
1) "da"
2) "wo"
3) "chui"
4) "shi"
```



#### zset(sorted set: 有序集合)

Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。

不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

```shell
127.0.0.1:6379> zadd zset1 0 wo
(integer) 1
127.0.0.1:6379> zadd zset1 1 shi
(integer) 1
127.0.0.1:6379> zadd zset1 2 da
(integer) 1
127.0.0.1:6379> zadd zset1 2 chui
(integer) 1
127.0.0.1:6379> zrangebyscore zset1 0 10
1) "wo"
2) "shi"
3) "chui"
4) "da"

```



### 命令

#### db

选择数据库：`select 0`,  redis默认使用数据库 0，为了清晰起见，这里再显式指定一次。



#### Key

管理redis中的键，语法 ：`command  key_name`

| command                | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| set key                |                                                              |
| get key                |                                                              |
| del key                | 在key存在删除key, 成功返回1， 否则 0.                        |
| type key               | 返回key所存储值的类型                                        |
| rename key newkey      | 修改key的名称                                                |
| renamenx key newkey    | 仅当newkey不存在时， 将key改名为newkey                       |
| dump key               | 序列化给定 key ，并返回被序列化的值。                        |
| exists key             | 检查key是否存在, 存在1，否则0                                |
| expire key seconds     | 为key设置过期时间                                            |
| expireat key timestamp | 为 key 设置过期时间, 接受的时间参数是 UNIX 时间戳(unix timestamp)，eg:EXPIREAT w3ckey 1293840000 |
| persist key            | 移除key的过期时间，key将保持永久                             |
| pttl key               | 以毫秒为单位返回key的剩余过期时间                            |
| ttl  key               | 以秒为单位返回给定key的剩余生存时间                          |



key pattern

key的模式匹配：

查找以 w3c 为开头的 key：

```
redis 127.0.0.1:6379> KEYS w3c*
1) "w3c3"
2) "w3c1"
3) "w3c2"
```

获取 redis 中所有的 key 可用使用 *****。

```
redis 127.0.0.1:6379> KEYS *
1) "w3c3"
2) "w3c1"
3) "w3c2"
```





####  string

get

* get key                                不存在，返回nil, 如果存储的不是string，返回一个错误。

* getrange key start end,  返回key中字符串值的子字符，**包括start和end**
* mget   key [key2..]           获取所有(一个或多个)给定 key 的值。不存在返回nil

set

* set key  v                           设置k的值，会覆盖已有的
* setrange key offset value 用 value 参数覆写给定 key 所储存的字符串值，从偏移量 offset 开始。
* set key v [k v..]                 同时设置一个或多个k-v对

存在与否

* getset key varlue,            将给定 key 的值设为 value ，并返回 key 的旧值(old value)。其他和get返回值一样
* msetnx k v  [k v .. ]          同时设置一个或多个 key-value 对，当且仅当所有给定 key 都不存在返回1，所至少有一个 key 已经存在，那么返回 0
* setnx key value                只有key不存在时设置key的值，设置成功返回1，失败返回0

增减

下面如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR(Other) 操作。

如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。

本操作的值限制在 64 位(bit)有符号数字表示之内

* incr k,                                将key中存储的数字值增一。

* incrby  k increment         将key所存储的值加生给定的增量值

* incrbyfloat k increment   将key所存储的值加生给定的浮点增量值

* decr k                                 将key中存储 的数字值减一

* decrby k decrement        key所存储的值减去给定的增量值

* append k v                        如果 key 已经存在并且是一个字符串，将 value 追加到 key 原来的值的末尾。

  ​                                           如果 key 不存在， 将给定 key 设为 value ，就像执行 SET key value 一样。

* strlen k                              返回 key 所储存的字符串值的长度。

bit位相关:

* getbit                                 对 key 所储存的字符串值，获取指定偏移量上的位(bit)

* setbit key offset value
  对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。

过期相关

* setex key seconds value

  将值 value 关联到 key ，并将 key 的过期时间设为 seconds (以秒为单位),如已存在将会替换旧值。

* psetex key milliseconds v 

  这个命令和 SETEX 命令相似，但它以毫秒为单位设置 key 的生存时间.





#### hash

hget k field                      获取存储在哈希表中指定字段的值，不存在时，返回nil.

hmget k field 1 [field 2] 获取所有给定字段的值

hgetall key                       获取在哈希表中指定 key 的所有字段和值

hkeys   key                       获取所有哈希表中的字段

hvals key                          获取哈希表中的所有值。

hlen    key                        获取哈希表中字段的数量, key不存在时，返回0



hset k field v                  将哈希表 key 中的字段 field 的值设为 value

hmset k f1 v1 [f2 v2]     同时将多个 field-value (域-值)对设置到哈希表 key 中。

hsetnx k f  v                    只有在字段 field 不存在时，设置哈希表字段的值



hexists k field                 查看哈希表 key 中，指定的字段是否存在。

hdel k field1 field2        删除一个或多个哈希表字段，不存在的字段将被忽略



hincrby k f increment   为哈希表 key 中的指定字段的整数值加上增量 increment 。

hincrbyfloat k f increment 为哈希表 key 中的指定字段的浮点数值加上增量 increment 。



`HSCAN key cursor [MATCH pattern][COUNT count]`

迭代哈希变中的键值对



#### list

llen    k                           获取列表长度

lrange k start stop       获取指定范围内的元素



lpushx k  v                     将一个或多个值插入到已存在的列表头部

lpush   k  v [v2...]          将一个或多个值插入到列表头部

rpush  k  v [v2...]          在列表中添加一个或多个值

rpushx  k v                    为已存在的列表添加值



lpop k                             移除并获取列表的第一个元素

rpop k                            移除并获取列表最后一个元素



lindex k  index             通过索引获取列表中的元素

lset  k  index  value     通过索引设置列表元素的值

lrem  k  count value    通过索引设置列表元素的值

rpoplpush source destination

移除列表的最后一个元素，并将该元素添加到另一个列表并返回

BLPOP k1 [k2..] timeout       

移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

BRPOP k1 [k2..]  timeout 

移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

BRPOPLPUSH source destination timeout

从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止