
---
title: "单机搭建zookeeper.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
#### zookeeper

ZooKeeper 是一个开源的分布式协调服务，由雅虎创建。

在ZooKeeper 集群中机器有三种角色：

- Leader

  一个集群同一时刻只能有一个Leader

- Follower

- Observer



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

- 已经被处理的消息不能丢

  在Leader向各个Follower广播COMMIT，同时也会在本地执行 COMMIT 并向连接的客户端返回「成功」,但是如果在各个 follower 在收到 COMMIT 命令前 leader 就挂了，导致剩下的服务器并没有执行都这条消息。 

  ```
  选举拥有 proposal 最大值（即 zxid 最大） 的节点作为新的 leader：
  由于所有提案被 COMMIT 之前必须有合法数量的 follower ACK，即必须有合法数量的服务器的事务日志上有该提案的 proposal，因此，只要有合法数量的节点正常工作，就必然有一个节点保存了所有被 COMMIT 消息的 proposal 状态。
  
  新的 leader 将自己事务日志中 proposal 但未 COMMIT 的消息处理。
  
  新的 leader 与 follower 建立先进先出的队列， 先将自身有而 follower 没有的 proposal 发送给 follower，再将这些 proposal 的 COMMIT 命令发送给 follower，以保证所有的 follower 都保存了所有的 proposal、所有的 follower 都处理了所有的消息。
  ```

- 被丢弃的消息不会再出现

  当 leader 接收到消息请求生成 proposal 后就挂了，其他 follower 并没有收到此 proposal，因此经过恢复模式重新选了 leader 后，这条消息是被跳过的。 此时，之前挂了的 leader 重新启动并注册成了 follower，他保留了被跳过消息的 proposal 状态，与整个系统的状态是不一致的，需要将其删除。

  ```
  Zab 通过巧妙的设计 zxid 来实现这一目的。一个 zxid 是64位，高 32 是纪元（epoch）编号，每经过一次 leader 选举产生一个新的 leader，新 leader 会将 epoch 号 +1。低 32 位是消息计数器，每接收到一条消息这个值 +1，新 leader 选举后这个值重置为 0。这样设计的好处是旧的 leader 挂了后重启，它不会被选举为 leader，因为此时它的 zxid 肯定小于当前的新 leader。当旧的 leader 作为 follower 接入新的 leader 后，新的 leader 会让它将所有的拥有旧的 epoch 号的未被 COMMIT 的 proposal 清除。
  ```





#### AMQP

kafka借鉴AMQP协议进行开发 



#### 使用场景

- 消息代理

  使用消息代理有很多原因(为了将处理消息和生产消息解耦开，缓存未被处理的消息等等)。对比大多数的消息系统，Kafka拥有更大的吞吐，内置分区，副本，以及错误容忍，这些特性都是选择Kafka作为大型可扩展消息处理应用的原因。

  从我们的经验角度来看，消息系统通常被用在相对吞吐量不大但是延迟要求低的场景中，并且通常都需要强健的持久化保障

- 网站活动追踪

  最初Kafka被用来搭建网站用户活动追踪的管道，管道中是一系列实时的消息流。站点的活动信息（页面浏览，搜索，以及其他用户的活动）被发布成不同主题下的流。这些流可以被不同场景下的应用订阅，包括但不限于实时处理，实时监控，上载到hadoop，或是构建离线数据仓库。

  活动追踪消息的量通常都很大，因为用户的每一个行为都会产生消息。

- 日志收集

  许多人将Kafka作为日志收集的一个解决方案。典型的日志收集是将物理的日志文件收集起来并且将它们导入到一个集中的地方（比如HDFS）。Kafka将文件细节抽象掉，提供了一个更为简洁的抽象（消息流）。这使得处理延迟变低，且能方便地支持多数据源和多消费者。对比Scribe 或者 Flume这些消息收集工具，Kafka提供了相同的性能，更强的持久化(副本)，以及端到端的低延迟

- 流处理

  许多用户将处理消息分成了多个阶段性的处理过程：原始数据被消费出来并聚合产生成一些新主题的流，被用作进一步的处理。举个例子，一个文章推荐处理的系统通常先是会将文章内容通过RSS抓取下来，发布到一个叫"article"的主题里；后续的处理会将内容进行规范，去重和清洗；最终的阶段会将内容和用户关联匹配上。



#### Quick Start

`https://benjamin-lee.gitbooks.io/kafka-document-chinese/content/chapter1.html`





#### Question

##### 安装java

https://tecadmin.net/install-java-8-on-centos-rhel-and-fedora/



#### `bogon: bogon: Name or service not known`

客户端启动时会获取本地地址：

1. 在报错机器上执行查看主机名命令：

   ```
   root@iZ231wxgt6mZ ~]# hostname
   bogon
   ```

   如果执行命令报错，请检查是否给hostname定义了别名，比如在.bash_profile或者.bashrc中 alias xxx=‘hostname’； 或者命令路径不在$PATH下面。

2. ping主机：

   ```
   [root@iZ231wxgt6mZ ~]# ping iZ231wxgt6mZ
   ```

   ```
   如果无法正常ping通主机名，则需要将本机地址绑定到 /etc/hosts文件中。
   ```

   `127.0.0.1 主机名 localhost.localdomain localhos`

   或是再添加一条

   `127.0.0.1 主机名`

3. 检查/etc/sysconfig/network 中的记录的hostname是否和/etc/hosts中的主机名绑定一致，如果不一致请确保一致。 如果需要修改/etc/sysconfig/network中的内容，修改后需要重启机器才能生效。

以上三部确认ok后，客户端启动就不在会报 UnknownHostException 的异常了。