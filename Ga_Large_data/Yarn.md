

### 配置Yarn

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

指定marpeduce 基于yarn运行

Yarn-site.xml

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

这个配置说的是，指定使用shuffle

还有一个官网没有指出：

```xml
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>node198</value>
    </property>
</configuration>
```

指定resourcemanger所在服务器主机名



### 启动

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



### web页面

端口8088



### 使用

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



### 组成

再说明一下yarn，资源管理，一个全局的工作调度与资源分配

![](http://claymore.wang:5000/uploads/big/996ffd4a3123576162542c3eba8e1369.png)

* **ResourceManager** 
  * 处理客户端请求 
  * 启动/监控ApplicationMaster 
  * 监控NodeManager 
  * 资源分配与调度 

* **ApplicationMaster** 
  * 数据切分 
  *  **NodeManager** 
  * 单个节点上的资源管理 
  * 处理来自ResourceManager的命令 
  * 处理来自ApplicationMaster的命令 

Ø为应用程序申请资源，并分配给内部任务 Ø任务监控与容错 

u **Container** 

Ø对任务运行环境的抽象，封装了CPU、内 存等多维资源以及环境变量、启动命令等任 务运行相关的信息 