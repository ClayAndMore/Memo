### 写在前面

初由LinkedIn公司开发，之后成为Apache项目的一部分 

Kafka 基于zookeeper协调的分布式消息系统 ,



分布式消息系统kafka提供了一个生产者、缓冲区、消费者的模型 

```
 producer     producer     producer
	   \	    |	     /
	     \	    |	   /
	       \	|	 /
	    	kafka cluster
	    	/    |    \
	       /     |	    \
  consumer     conseumer  conseumer
```

Kafka中，客户端和服务器之间的通信是通过简单，高性能，语言无关[TCP协议完成的。此协议已版本化并保持与旧版本的向后兼容性。我们为Kafka提供Java客户端，但客户端有多种语言版本



#### 几个术语

##### topics

kafka给消息提供的分类方式。broker用来存储不同topic的消息数据 。

```
       A topic:
------------------------------------------------
| Partition 0:  0,1,2,3,4,5.....               |
| Partition 1:  0,1,2,3,4,5,6,7,8,9,10, 11 ..  |
| Partition 2:  0,1,2..                        |
------------------------------------------------
time: old  -------------> new
```

* 每个topic又可以拆分成多个partition , partition均匀分配到集群server中 
* 每个partition又由一个一个消息组成 
* 每个消息都被标识了一个递增序列号代表其进来的先后顺序，并按顺序存储在partition中 



**producer选择一个topic，生产消息，消息会通过分配策略append到某个partition末尾** 

**consumer选择一个topic，通过id指定从哪个位置开始消费消息。消费完成之后保留id，下次可以从这个位置开始继续消费，也可以从其他任意位置开始消费** 

这个id, 在Kafaka中被称为offset.



这种组织方式的好处：

1. 消费者可以根据需求，灵活指定offset消费
2. 保证了消息不变性，为并发消费提供了线程安全的保证。每个consumer都保留自己的offset，互相之间不干扰，不存在线程安全问题 。
3. 消息访问的并行高效性。生产、消费消息的时候，会被路由到指定partition，减少竞争，增加了程序的并行能力 
4. 保证消息可靠性。**消息消费完成之后不会删除**，可以通过重置offset重新消费，保证了消息不会丢失 
5. 增加消息系统的可伸缩性。每个topic中保留的消息可能非常庞大，通过partition将消息切分成多个子消息，并通过负责均衡策略将partition分配到不同server。这样当机器负载满的时候，通过扩容可以将消息重新均匀分配 



##### broker（经济人）

指的是中间的kafka cluster，存储消息，是由多个server组成的集群 

Kakfa Broker集群受Zookeeper管理 



##### producer , consumer

数据生产者，消费者

producer和consumer 都是客户端（APP）



#### zookeeper

ZooKeeper 是一个开源的分布式协调服务，由雅虎创建。

在ZooKeeper 集群中机器有三种角色：

* Leader

  一个集群同一时刻只能有一个Leader

* Follower

* Observer



在zookeeper集群中， 当有一个请求从客户端来时，集群中随机一个服务器去相应。

如果是读请求，那么该服务器直接返回结果。

如果是写请求， 那么则通知leader去根据ZAB协议广播。



#### ZAB 协议

ZooKeeper Atomic Broadcast ，Zookeeper自动广播协议。

 ZooKeeper使用的是ZAB协议作为数据一致性的算法 。

协议分为两大块内容：

##### 广播

广播实际上是一个简化的二阶段提交过程。

1. Learder 收到请求消息后，生成一个全局唯一自增ID(zxid).

2. Learder 将该消息携带zxid 作为一个proposal (提案) 分发给所以Follower.

3. 每个Follower都有一个FIFO的队列， 接收2中的proposal 到该队列，TCP实现。

4. Follower 收到proposal 后 ，先将它写到磁盘，成功后向Leader 返回一个ACK.

5. 当Leader收到合法数量的ACK（2f+1 台服务器中的 f+1 台 ）， 向所有follower发送COMMIT命令， 同时会在本地执行该消息。

   当少于这个合法数量，那么该集群就挂了。

6. Follower收到COMMIT后,执行该消息。



##### 恢复

恢复模式是指的Leader挂掉的情况。

* 已经被处理的消息不能丢

  在Leader向各个Follower广播COMMIT，同时也会在本地执行 COMMIT 并向连接的客户端返回「成功」,但是如果在各个 follower 在收到 COMMIT 命令前 leader 就挂了，导致剩下的服务器并没有执行都这条消息。 

  ```
  选举拥有 proposal 最大值（即 zxid 最大） 的节点作为新的 leader：
  由于所有提案被 COMMIT 之前必须有合法数量的 follower ACK，即必须有合法数量的服务器的事务日志上有该提案的 proposal，因此，只要有合法数量的节点正常工作，就必然有一个节点保存了所有被 COMMIT 消息的 proposal 状态。
  
  新的 leader 将自己事务日志中 proposal 但未 COMMIT 的消息处理。
  
  新的 leader 与 follower 建立先进先出的队列， 先将自身有而 follower 没有的 proposal 发送给 follower，再将这些 proposal 的 COMMIT 命令发送给 follower，以保证所有的 follower 都保存了所有的 proposal、所有的 follower 都处理了所有的消息。
  ```

  

* 被丢弃的消息不会再出现

  当 leader 接收到消息请求生成 proposal 后就挂了，其他 follower 并没有收到此 proposal，因此经过恢复模式重新选了 leader 后，这条消息是被跳过的。 此时，之前挂了的 leader 重新启动并注册成了 follower，他保留了被跳过消息的 proposal 状态，与整个系统的状态是不一致的，需要将其删除。

   ```
  Zab 通过巧妙的设计 zxid 来实现这一目的。一个 zxid 是64位，高 32 是纪元（epoch）编号，每经过一次 leader 选举产生一个新的 leader，新 leader 会将 epoch 号 +1。低 32 位是消息计数器，每接收到一条消息这个值 +1，新 leader 选举后这个值重置为 0。这样设计的好处是旧的 leader 挂了后重启，它不会被选举为 leader，因为此时它的 zxid 肯定小于当前的新 leader。当旧的 leader 作为 follower 接入新的 leader 后，新的 leader 会让它将所有的拥有旧的 epoch 号的未被 COMMIT 的 proposal 清除。
   ```

  





#### AMQP

kafka借鉴AMQP协议进行开发 