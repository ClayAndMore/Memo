---
title: "10_Yarn.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["hadoop"]
categories: ["大数据"]
author: "Claymore"

---
Tags:[大数据] 

### 组成

yarn，资源管理，一个全局的工作调度与资源分配

![](http://claymore.wang:5000/uploads/big/996ffd4a3123576162542c3eba8e1369.png)

- **ResourceManager** 

  - 处理客户端请求 
  - 启动/监控ApplicationMaster 
  - 监控NodeManager 
  - 资源分配与调度 

- **NodeManager** 

  - 单个节点上的资源管理 ， **和 datanode 是1:1的关系，一个 datanode 机器会有个 NodeManger**
  - 处理来自ResourceManager的命令 
  - 处理来自ApplicationMaster的命令 

- **ApplicationMaster** 

  - 数据切分 
  - 为应用程序申请资源，并分配给内部任务 
  - 任务监控与容错 

- **Container** 

  - 对任务运行环境的抽象，封装了CPU、内 存等多维资源以及环境变量、启动命令等任 务运行相关的信息 

    

提交任务后再jps能看到相关进程

YARN 总体上仍然是Master/Slave 结构，在整个资源管理框架中，ResourceManager 为Master，NodeManager 为Slave。

1. ResourceManager 负责对各个NodeManager 上的资源进行统一管理和调度,也是全局的资源管理器整个集群上只有一个。

2. ApplicationMster, 用户每提交的应用程序都包含AM, 与RM调度协商获取资源（用Container), 与NM通信启动和停止任务，监控所有任务运行状态，并在任务运行失败的时候重新申请资源用于重启任务。

3. NodeManager:  NM 会定时向RM汇报本节点的资源使用情况和各个节点的Container的运行状态，另一方面会接收来自AM的Containe启动和停止请求。

4. Container,  是yarn中抽象的概念，它封装cpu, 内存， 多个节点上的多维度资源。它支持Linux内核的Cgroup。

   当AM向RM申请资源，RM返回AM的资源便是Container

   yarn会向每个任务分配一个Container,且该任务只能使用该Container中描述的资源。

   NodeManager会启动一个线程监控Container的资源，默认是1G和1核，如果超出会直接kill掉。

   然后会把该任务分配给其他节点做，有一个重试次数，当次数达到上限，那么整个作业会跑失败。

eg: 图中黄色的相关流程：

当用户client提交一个应用程序(如MR计算)时，client 会先访问ResourceManger,  RM 会挑选一个不忙的NoderManager  去提供一个用以跟踪和管理这个程序的ApplicationMaster，它负责向ResourceManager 申请资源，比如ApplicationMaster 说我有3个MR 需要跑， 这时 Resource Manager 会提供 三个容器在集群中去跑 相关MR.
由于不同的ApplicationMaster 被分布到不同的节点上，因此它们之间不会相互影响.

当其中有 ApplicationMaster 挂掉后，ResourceManager 会再找个机器创建新的。这样解决了单点故障问题。

当然 ResourceManager 也是可以做HA的。当然依靠zk.

ps: client要求的计算框架有很多，如MR, Spark.



### 单点安装

#### 配置Yarn

http://hadoop.apache.org/docs/r2.7.6/hadoop-project-dist/hadoop-common/SingleCluster.html

可以看到YARN on a Single Node

cp mapred-site.xml.template mapred-site.xml

Mapred-site.xml:

```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

指定marpeduce 基于yarn运行， 这个值也可以是local(本机模拟跑，不用于分布式)。

Yarn-site.xml

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

这个配置说的是，指定使用shuffle（拽着走），让 NodeManager 帮助 MR 拉取数据：

每个节点上可以有很多MR进程，每个进程都有拉取数据的代码，这样又是一个重复，所以shuffle模式是把拉取数据的这部分抽取出来，让NM去做，每次MR要拉取数据的时候要向 NM 申请。

上述这两个基本配置是最核心的部分，但是还是没有HA能力。



还有一个官网没有指出：

```xml
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>node198</value>
    </property>
</configuration>
```

指定resourcemanger所在服务器主机名, 其实有时候不用指定也可以，指定容易在页面8088访问不到。

| yarn.resourcemanager.hostname             | 0.0.0.0                               |
| ----------------------------------------- | ------------------------------------- |
| yarn.resourcemanager.webapp.address       | ${yarn.resourcemanager.hostname}:8088 |
| yarn.resourcemanager.webapp.https.address | ${yarn.resourcemanager.hostname}:8090 |
| ....                                      | ....                                  |



#### 启动

```shell
[root@node198 hadoop-2.7.3]#jps
63809 Jps
38171 DataNode
38035 NameNode
38337 SecondaryNameNode
[root@node198 hadoop-2.7.3]#sbin/yarn-daemon.sh start resourcemanager
starting resourcemanager, logging to /opt/moudles/apache/hadoop-2.7.3/logs/yarn-root-resourcemanager-node198.out
[root@node198 hadoop-2.7.3]#sbin/yarn-daemon.sh start nodemanager
starting nodemanager, logging to /opt/moudles/apache/hadoop-2.7.3/logs/yarn-root-nodemanager-node198.out
[root@node198 hadoop-2.7.3]#jps
64382 Jps
64197 NodeManager
38171 DataNode
38035 NameNode
63882 ResourceManager
38337 SecondaryNameNode
```



#### web页面

端口8088



#### 使用

bin/yarn + app + 操作

app和操作有很多，我们可以在使用命令行的时候看下。

这里用一个hadoop自带的案例：

```shell
[root@node198 hadoop-2.7.3]#bin/yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount /test.txt /ouput
19/06/10 20:42:51 INFO client.RMProxy: Connecting to ResourceManager at node198/127.0.0.1:8032
19/06/10 20:42:53 INFO input.FileInputFormat: Total input paths to process : 1
19/06/10 20:42:53 INFO mapreduce.JobSubmitter: number of splits:1
19/06/10 20:42:53 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1560169707030_0001
19/06/10 20:42:53 INFO impl.YarnClientImpl: Submitted application application_1560169707030_0001
19/06/10 20:42:54 INFO mapreduce.Job: The url to track the job: http://localhost:8088/proxy/application_1560169707030_0001/
19/06/10 20:42:54 INFO mapreduce.Job: Running job: job_1560169707030_0001
19/06/10 20:43:00 INFO mapreduce.Job: Job job_1560169707030_0001 running in uber mode : false
19/06/10 20:43:00 INFO mapreduce.Job:  map 0% reduce 0%
19/06/10 20:43:05 INFO mapreduce.Job:  map 100% reduce 0%

```

这里的test.txt 和 output指的是hdfs中的路径。

在运行中可8088页面看到作业进度



### HA 配置

https://hadoop.apache.org/docs/r2.7.6/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html

其中图中有说明，两个 ResourceManager 谁先抢到了 zk， 谁就是active, 形成主备。

看后方的 Sample configurations。

```xml
<property>
  <name>yarn.resourcemanager.ha.enabled</name>
    # 声明开启ha
  <value>true</value>
</property>
<property>
  <name>yarn.resourcemanager.cluster-id</name>
   # 声明所在集群
  <value>cluster1</value>  
</property>
<property>
  <name>yarn.resourcemanager.ha.rm-ids</name>
    # 逻辑分割
  <value>rm1,rm2</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname.rm1</name>
    # 物理，和上方完成逻辑到物理的映射
  <value>master1</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname.rm2</name>
  <value>master2</value>
</property>
<property>
  <name>yarn.resourcemanager.webapp.address.rm1</name>
  <value>master1:8088</value>
</property>
<property>
  <name>yarn.resourcemanager.webapp.address.rm2</name>
  <value>master2:8088</value>
</property>
<property>
  <name>yarn.resourcemanager.zk-address</name>
  <value>zk1:2181,zk2:2181,zk3:2181</value>
</property>
```



