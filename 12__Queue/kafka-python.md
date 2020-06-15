
---
title: "kafka-python.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
目前已有的python客户端：

https://cwiki.apache.org/confluence/display/KAFKA/Clients#Clients-Python



我们选择：https://github.com/dpkp/kafka-python， 因为它star数最多。



安装： `pip install kafka-python`



### 基本使用

#### 消费端

`consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['localhost:9092'])`

- 第1个参数为 topic的名称
- group_id : 指定此消费者实例属于的组名，可以不指定
- bootstrap_servers ： 指定kafka服务器

eg:

```python
>>> from kafka import KafkaConsumer
>>> consumer=KafkaConsumer('test', bootstrap_servers='localhost:9092')
>>> for msg in consumer:
...  print msg
... 
ConsumerRecord(topic=u'test', partition=1, offset=10, timestamp=1563437749438, timestamp_type=0, key=None, value='message0', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=8, serialized_header_size=-1)
...
ConsumerRecord(topic=u'test', partition=0, offset=24, timestamp=1563437749441, timestamp_type=0, key=None, value='message6', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=8, serialized_header_size=-1)
...
ConsumerRecord(topic=u'test', partition=1, offset=16, timestamp=1563437749442, timestamp_type=0, key=None, value='message9', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=8, serialized_header_size=-1)
```



#### 生产端

```python
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send('my_topic' , key= b'my_key', value= b'my_value', partition= 0)
```

- 第1个参数为 topic名称，必须指定
- key ： 键，必须是字节字符串，可以不指定（但key和value必须指定1个），默认为None
- value ： 值，必须是字节字符串，可以不指定（但key和value必须指定1个），默认为None
- partition ： 指定发送的partition，由于kafka默认配置1个partition，固为0。
  - 在多partion中，如不指定则按默认方式发送：有key的按key算，无key的轮询发。

eg:

```python
>>> from kafka import KafkaProducer
>>> producer=KafkaProducer(bootstrap_servers='localhost:9092')
>>> for i in range(10):
...  producer.send('test', 'message%s'%i)
... 
<kafka.producer.future.FutureRecordMetadata object at 0x7f3e0ca9a3d0>
<kafka.producer.future.FutureRecordMetadata object at 0x7f3e0caaa090>
...
<kafka.producer.future.FutureRecordMetadata object at 0x7f3e0cabfe50>

>>> future=producer.send('test', 'message9')
>>> result=future.get(timeout=10)
>>> print result
RecordMetadata(topic='test', partition=1, topic_partition=TopicPartition(topic='test', partition=1), offset=17, timestamp=1563439001362, checksum=None, serialized_key_size=-1, serialized_value_size=8, serialized_header_size=-1)
```

future.get函数等待单条消息发送完成或超时

#### ConsumerRecord

这个为发送端或者接收端的消息：

- topic， partition
- offset ： 这条消息的偏移量
- timestamp ： 时间戳
- timestamp_type ： 时间戳类型
- key ： key值，字节类型
- value ： value值，字节类型
- checksum ： 消息的校验和
- serialized_key_size ： 序列化key的大小， key=Noe时，大小为-1
- serialized_value_size ： 序列化value的大小，value=None时，大小为-1
- serialized_header_size：




### KafkaConsumer 

#### 手动分配partition

```python
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'])
consumer.assign([TopicPartition(topic= 'my_topic', partition= 0)])
for msg in consumer:
    print(msg)
```



#### 超时处理

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['localhost:9092'], consumer_timeout_ms=1000)
for msg in consumer:
    print(msg)
```

若不指定 consumer_timeout_ms，默认一直循环等待接收，若指定，则超时返回，不再等待

consumer_timeout_ms ： 毫秒数



#### 订阅多个topic

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'])
consumer.subscribe(topics= ['my_topic', 'topic_1'])
#consumer.subscribe(pattern= '^my.*'), 也可用正则订阅一类topic
for msg in consumer:
    print(msg)
```

可同时接收多个topic消息



#### 解码json数据

编码（生产者）：value_serializer

解码（消费者）：value_deserializer

1.先看producer发送的json数据

```python
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
future = producer.send('my_topic' ,  value= {'value_1' : 'value_2'})
```

 收到的数据（未解码前）：

```
ConsumerRecord(topic=u'test', partition=0, offset=27, timestamp=1563441200503, timestamp_type=0, key=None, value='{"value_1": "value_2"}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=22, serialized_header_size=-1)
```

2.consumer解码：

```python
consumer = KafkaConsumer('test', bootstrap_servers= ['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))
for msg in consumer:
    print(msg)
    
ConsumerRecord(topic=u'test', partition=1, offset=19, timestamp=1563442029736, timestamp_type=0, key=None, value={u'value_1': u'value_2'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=22, serialized_header_size=-1)
```

可以看到接收结果中，value已经自动解码，并为字符串类型

不仅value可以json，key也可以，**只需指定 key_deserializer**


  

### KafkaProducer

#### 可压缩消息发送

`compression_type='gzip'`

若消息过大，还可压缩消息发送，可选值为 ‘gzip’, ‘snappy’, ‘lz4’, or None

```python
roducer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip')
future = producer.send('my_topic' ,  key= b'key_3', value= b'value_3', partition= 0)
future.get(timeout= 10)
```



#### 发送msgpack

msgpack为MessagePack的简称，是高效二进制序列化类库，比json高效

```python
>>> import msgpack
>>> producer=KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=msgpack.dumps)
>>> producer.send('test', value={'value_1' : 'value_2'})
<kafka.producer.future.FutureRecordMetadata object at 0x7f3e0c240990>
```

