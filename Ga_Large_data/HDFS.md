

### 存储模型

无论什么文件数据，都换成**字节**（byte）

文件线性切割成块（Block）,偏移量 offset （byte）,  eg:  100bytes,分成10块，每块，10bytes

```
+-----+
|0    |       第一块的偏移量为0，
| 10byte      则第二块的偏移量要加第一块的长度，及0+10=10
+-----+
|10   |
| 10byte
+-----+
| 20  |
|     |
+-----+
|     |
|     |
|...  |
|     |
|     |
+-----+
|     |
|     |
+-----+

```

* Block分散存储在集群节点中，每块分散在不同节点

* 单一文件Block大小一致，每块大小一样，最后一块不一定，可能会小点。

* 文件与 文件可以不一致，  A文件可以按10byte切， B文件可以按20byte切。

* Block可以设置副本数，副本分散在不同节点中，每个块有副本（replice,备份)，最少三个副本，分散在不同节点。在用的时候用谁都一样，提高性能，所以副本越多，并行计算的可能性越大。

* 副本数不要超过节点数量， 不然容易副本和真块在一起，没有意义。

* 文件上传可以设置Block大小和副本数，默认block(128M), 最小1M. 副本默认3个。

* 已上传的文件Block副本数可以调整，大小不变，大小不可更改。

* 只支持一次写入多次读取，同一时刻只有一个写入者

* 可以append追加数据

如果一个文件大小 小于块大小，是不会占据块的整个空间，多个这样的文件是不会共享块的，小文件的缺陷。

### 副本放置策略

![](http://211.159.177.235:5000/uploads/big/4b31e433b4e1e92befe4e3dab72583e2.png)

RackA 和 RackB 是两个机架。

假设一个文件被分割成了N个副本，

–第一个副本：如果客户端和datanode在一个节点 （如RackA），放置在上传文件的DN(datanode)；

如果是集群外提交，则随机挑选一台磁盘不太满，CPU不太忙的节点。

–第二个副本：放置在于第一个副本**不同的 机架**的节点上。

–第三个副本：与第二个副本相同机架的节点。

–更多副本：随机节点

### 特点

优点：

1. 上传的数据自动保存多个副本，通过增加副本的数据，来增加它的容错性
2. 如果hdfs的某一个副本丢失，很复制其他机器的副本，拷贝到自己磁盘当中
3. 处理超大的数据文件
4. 运行的廉价的计算机集群上
5. 流式的访问数据

缺点：

1. 无法存储大量小文件（淘宝开源了TFS,参考hfds）,可调整block块大小。
2. 不适合低延迟数据的访问，它本身比较慢
3. 不支持多用户写入
4. 不支持修改，仅支持文件追加。



### 目录

```shell
[root@node198 hadoop-2.7.3]#tree data/tmp/dfs/name/current/
data/tmp/dfs/name/current/
├── edits_0000000000000000001-0000000000000000007
├── edits_0000000000000000008-0000000000000000009
├── edits_inprogress_0000000000000000010
├── fsimage_0000000000000000007
├── fsimage_0000000000000000007.md5
├── fsimage_0000000000000000009
├── fsimage_0000000000000000009.md5
├── seen_txid
└── VERSION
```

fsimage: 记录某一次永久检查点时整个hdfs中的元数据信息。

edits:     所有对于hdfs的写操作都会记录在此文件中。



### 操作

```
[root@node198 hadoop-2.7.3]#bin/hdfs 
Usage: hdfs [--config confdir] [--loglevel loglevel] COMMAND
       where COMMAND is one of:
  dfs                  run a filesystem command on the file systems supported in Hadoop.
。。。
```



```
[root@node198 hadoop-2.7.3]#bin/hdfs dfs
Usage: hadoop fs [generic options]
	[-appendToFile <localsrc> ... <dst>]
	[-cat [-ignoreCrc] <src> ...]
。。。。
```





#### 上传

```shell
vim test.txt
1 2 3
4 5 6
7 8 9

bin/hdfs dfs -put test.txt /

[root@node198 hadoop-2.7.3]#cat data/tmp/dfs/data/current/BP-1797506382-127.0.0.1-1560153263953/current/finalized/subdir0/subdir0/blk_1073741825
1 2 3
4 5 6
7 8 9
```



#### 查看

```
[root@node198 hadoop-2.7.3]#bin/hdfs dfs -ls /
Found 1 items
-rw-r--r--   1 root supergroup         18 2019-06-10 16:09 /test.txt
```

