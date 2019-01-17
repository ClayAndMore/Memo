

Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。

Redis 客户端可以订阅任意数量的频道。

下图展示了频道 channel1 ， 以及订阅这个频道的三个客户端 —— client2 、 client5 和 client1 之间的关系：

![](https://code.ziqiangxuetang.com/media/uploads/2014/11/pubsub1.png)



当有新消息通过 PUBLISH 命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端：

![](https://code.ziqiangxuetang.com/media/uploads/2014/11/pubsub2.png)



### psubscribe  

`psubsribe pattern [pattern]`

订阅一个或多个符合给定模式的频道



### subscribe

`subscribe channel [channel ...]`

订阅给定的一个或多个频道的信息。



### unsubscribe

`unsubscribe [channel [channel ...]]`

指退订给定的频道



### pubsub

`PUBSUB subcommand [argument [argument ...\]]]`
查看订阅与发布系统状态。



### publish 

`publish channel messge`

将信息发送到指定的频道





### punsubscribe

`punsubscribe [pattern [pattern ..]]`

退订给所有给定模式的频道