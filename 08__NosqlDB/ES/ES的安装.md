Tags:[database, nosql]

### 写在前面

Elasticsearch 是一个开源的搜索引擎，建立在一个全文搜索引擎库 [Apache Lucene™](https://lucene.apache.org/core/) 基础之上。 Lucene 可以说是当下最先进、高性能、全功能的搜索引擎库--无论是开源还是私有。

但是 Lucene 仅仅只是一个库。为了充分发挥其功能，你需要使用 Java 并将 Lucene 直接集成到应用程序中。 更糟糕的是，您可能需要获得信息检索学位才能了解其工作原理。Lucene *非常* 复杂。

Elasticsearch 也是使用 Java 编写的，它的内部使用 Lucene 做索引与搜索，但是它的目的是使全文检索变得简单， 通过隐藏 Lucene 的复杂性，取而代之的提供一套简单一致的 RESTful API。

然而，Elasticsearch 不仅仅是 Lucene，并且也不仅仅只是一个全文搜索引擎。 它可以被下面这样准确的形容：

- 一个分布式的实时文档存储，*每个字段* 可以被索引与搜索
- 一个分布式实时分析搜索引擎
- 能胜任上百个服务节点的扩展，并支持 PB 级别的结构化或者非结构化数据



### 下载和安装

#### 确保Java 8环境

```
java -version
```

如果没有则安装：

去官网，或者http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

下载java相关的压缩包，放到linux下解压，

将解压后的bin/java放入环境变量：

```bash
# vim /etc/profile
export JAVA_HOME=/home/jdk1.8.0_211
export PATH=$PATH:$JAVA_HOME/bin
```

这里建议把jdk安装在非root用户可以访问的地方。



#### elasticsearch安装

https://www.elastic.co/cn/downloads/elasticsearch

$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.zip
$ unzip elasticsearch-5.5.1.zip
$ cd elasticsearch-5.5.1/ 

启动：

```
./bin/elasticsearch
```

 错误提示：

```
don't run elasticsearch as root. at org.elasticsearch
```

这是出于系统安全考虑设置的条件。由于ElasticSearch可以接收用户输入的脚本并且执行，为了系统安全考虑，  建议创建一个单独的用户用来运行ElasticSearch。


- 创建elsearch用户和elsearch用户

  `groupadd elsearch`

  `useradd -m elsearch -g elsearch -p elasticsearch`  

  创建归为用户组elsearch的elsearch用户， 密码设置为elasticsearch。

- 更改刚才解压的文件夹的所属用户及组为elsearch;elsearch

  `chown -R elsearch:elsearch  elasticsearch-5.5.1`

- 切换到elsearch用户并再次启动：

  `su elsearch cd elasticsearch-5.5.1/bin` `./elasticsearch`

验证：打开另一个命令行窗口，请求该端口，会得到说明信息：

```
[root@localhost ~]# curl localhost:9200
{
"name" : "7DhJWI4",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "RUMzhPuFSzqAjyQUEXvf0A",
"version" : {
"number" : "5.5.1",
"build_hash" : "19c13d0",
"build_date" : "2017-07-18T20:44:24.823Z",
"build_snapshot" : false,
"lucene_version" : "6.6.0"
},
"tagline" : "You Know, for Search"
}
```




#### 配置文件  

  在Elastic安装目录的config/elasticsearch.yml文件，可以更改network.host的注释 0.0.0.0让任何人都访问。

  配置：

  ```yaml
  # ======================== Elasticsearch Configuration =========================
  ..
  # Please consult the documentation for further information on configuration options:
  # https://www.elastic.co/guide/en/elasticsearch/reference/index.html
  #
  # ---------------------------------- Cluster -----------------------------------
  #
  # Use a descriptive name for your cluster:
  #
  #cluster.name: my-application
  #
  # ------------------------------------ Node ------------------------------------
  #
  # Use a descriptive name for the node:
  #
  #node.name: node-1
  #
  # Add custom attributes to the node:
  #
  #node.attr.rack: r1
  #
  # ----------------------------------- Paths ------------------------------------
#
  # Path to directory where to store the data (separate multiple locations by comma):
#
  path.data: /opt/ELK/es_var/data
  #
  # Path to log files:
  #
  path.logs: /opt/ELK/es_var/log
  #
  # ----------------------------------- Memory -----------------------------------
  #
  # Lock the memory on startup:
  #
  #bootstrap.memory_lock: true
  #
  # Make sure that the heap size is set to about half the memory available
  # on the system and that the owner of the process is allowed to use this
  # limit.
  #
  # Elasticsearch performs poorly when the system is swapping the memory.
  #
  # ---------------------------------- Network -----------------------------------
  #
  # Set the bind address to a specific IP (IPv4 or IPv6):
  #
  #network.host: 192.168.0.1
  #
  # Set a custom port for HTTP:
  #
  #http.port: 9200
  #
  # For more information, consult the network module documentation.
  #
  # --------------------------------- Discovery ----------------------------------
  #
  # Pass an initial list of hosts to perform discovery when this node is started:
  # The default list of hosts is ["127.0.0.1", "[::1]"]
  #
  #discovery.seed_hosts: ["host1", "host2"]
  #
  # Bootstrap the cluster using an initial set of master-eligible nodes:
  #
  #cluster.initial_master_nodes: ["node-1", "node-2"]
  #
  # For more information, consult the discovery and cluster formation module documentation.
  #
  # ---------------------------------- Gateway -----------------------------------
  #
  # Block initial recovery after a full cluster restart until N nodes are started:
  #
  #gateway.recover_after_nodes: 3
  #
  # For more information, consult the gateway module documentation.
  #
  # ---------------------------------- Various -----------------------------------
  #
  # Require explicit names when deleting indices:
  #
  #action.destructive_requires_name: true
  ```

  

### 错误

#### 非root用户找不到java home

原因就是java安装在了root目录，切换到非root用户（因为es需要），找不到javahome, 这个问题坑了我好久。

之后启动，又遇到了：

Error: Could not find or load main class org.elasticsearch.tools.java_version_checker.JavaVersionChecker

也是因为把es放到了root账户下，后放到opt下

注意， es_var 这个数据文件也要在非root的时候创建。