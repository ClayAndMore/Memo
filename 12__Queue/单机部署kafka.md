### 下载和配置java

去官网下载 https://www.java.com/zh_CN/download/manual.jsp

mkdir -p /opt/module

tar xvfz dk-8u211-linux-x64.tar.gz -C /opt/module



添加环境变量：

```shell
vim /etc/profile
export JAVA_HOME=/opt/module/jdk1.8.0_211
export PATH=$PATH:$JAVA_HOME/bin

# 使环境变量生效
source /etc/profile

# 验证：
[root@node101 ~]# java -version
java version "1.8.0_211"
Java(TM) SE Runtime Environment (build 1.8.0_211-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.211-b12, mixed mode)
```

   

### 下载和配置kafka

去官网：https://kafka.apache.org/downloads， 点击下载二进制的选项可以看到各镜像和各版本的下载链接。

```

```





#### config

在安装目录需要修改：server.properties 文件

`broker.id`是broker的唯一标示，集群中的broker标识必须唯一。
`listeners`是broker监听的地址和端口, 默认是9092，其中`PLAINTEXT`是协议。
`log.dirs`是日志数据的存放目录，也就是producer产生的数据存放的目录。
`zookeeper.connect`配置是zookeeper的集群，broker启动之后将信息注册到zookeeper集群中。

log.dirs, 日志文件， 默认：`log.dirs=/tmp/kafka-logs`





### 启动

```sh
# 启动zk服务
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > logs/zookeeper.log &

# 启动kafka服务
nohup bin/kafka-server-start.sh config/server.properties > logs/kafka.log 
```



### topic 创建

```sh
# 建立一个队列
bin/kafka-topics.sh --create --zookeeper 10.250.123.10:2181 --topic test --replication-factor 1 --partitions 2
Created topic test.
## --create 指定命令为创建
## --zookeeper 指定Zookeeper的服务
## --topic 指定队列名称
## --replication-factor 指定队列的副本数，这个副本数需要和集群的节点数相对应
## --partitions 指定队列的分片数量，适当的分片可以提升性能


# 查看队列列表
bin/kafka-topics.sh --zookeeper 10.250.123.10:2181 --list
test

# 查看指定队列
bin/kafka-topics.sh --zookeeper 10.250.123.10:2181 --topic test --describe
Topic:test	PartitionCount:2	ReplicationFactor:1	Configs:
	Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	Topic: test	Partition: 1	Leader: 0	Replicas: 0	Isr: 0
## --topic 指定需要查看的队列名
## --describe 该命令用于描述topic队应的基础信息
	
# 删除队列
bin/kafka-topics.sh --zookeeper 10.250.123.10:2181 --topic test --delete
Topic test is marked for deletion.
Note: This will have no impact if delete.topic.enable is not set to true.
```



### 生产和消费

```sh
# producer 发送一些消息
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
>This is first message
>Second message

# consumer 消费消息
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
Second message
This is first message

```

