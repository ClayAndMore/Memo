## Mongo 检查和问题记录



### 0

#### 内存

MongoDB使用的是内存映射存储引擎,即Memory Mapped Storage Engine，简称MMAP。

MMAP可以把磁盘文件的一部分或全部内容直接映射到内存，这样文件中的信息位置就会在内存中有对应的地址空间，这时对文件的读写可以直接用指针来做，而不需要read/write函数了，但这并不代表将文件map到物理内存**，只有访问到这块数据时才会被操作系统以Page的方式换到物理内存**。

MongoDB将内存管理工作交给操作系统的虚拟内存管理器来完成，这样就大大简化了MongoDB的工作，同时操作系统会将数据刷新保存到磁盘上，下图就是MMAP的简要工作原理图:

![](http://ovolonhm1.bkt.clouddn.com/mongo%E5%86%85%E5%AD%98%E6%98%A0%E5%B0%84.png)



看机器是否对内存做了限制：`ulimit -a | grep memery`

```
[root@bogon img]# ulimit -a | grep memory
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
virtual memory          (kbytes, -v) unlimited
```

如做了限制，我们修改限制：

`[root@f1-mongo1 ~]$ ulimit -m unlimited`
`[root@f1-mongo1 ~]$ ulimit -v unlimited`



#### 硬盘

mongodb 不会释放已经占用的硬盘空间，即使drop collection也不行，除非drop database。如果一个db曾经有大量的数据一段时间后又删除的话，硬盘空间就是一个问题。

一般用repairDatabase(), 即在mongo shell中运行

```
db.repairDatabase()
```

, 或者

```
db.runCommand({ repairDatabase: 1 })
```

, 第二种方法可以带其他几个参数

```
{ repairDatabase: 1,
 preserveClonedFilesOnFailure: <boolean>,
 backupOriginalFiles: <boolean> }

```

repairDatabase是官方文档中认为唯一可以回收硬盘空间的方法。

repairDatabase()会花费大量的时间。



### 1

#### mongostat

![](http://ojynuthay.bkt.clouddn.com/mongostat.png)

参数说明：

```
1.inserts/s 每秒插入次数
2.query/s 每秒查询次数
3.update/s 每秒更新次数
4.delete/s 每秒删除次数
5.getmore/s 每秒执行getmore次数
6.command/s 每秒的命令数，比以上插入、查找、更新、删除的综合还多，还统计了别的命令
7.flushs/s 每秒执行fsync将数据写入硬盘的次数。
8.mapped/s 所有的被mmap的数据量，单位是MB，
9.vsize 虚拟内存使用量，单位MB
10.res 物理内存使用量，单位MB
11.faults/s 每秒访问失败数（只有Linux有），数据被交换出物理内存，放到swap。不要超过100，否则就是机器内存太小，造成频繁swap写入。此时要升级内存或者扩展
12.locked % 被锁的时间百分比，尽量控制在50%以下吧
13.idx miss % 索引不命中所占百分比。如果太高的话就要考虑索引是不是少了
14.q t|r|w 当Mongodb接收到太多的命令而数据库被锁住无法执行完成，它会将命令加入队列。这一栏显示了总共、读、写3个队列的长度，都为0的话表示mongo毫无压力。高并发时，一般队列值会升高。
15.conn 当前连接数
16.time 时间戳
```









#### mongotop

```
                          ns       total        read       write  2018-03-07T10:08:35
                  file.info       257ms       257ms         0ms
             file.analyzing        10ms        10ms         0ms
             lfTEFOR1VBR0U=         0ms         0ms         0ms
               VEVNSU5GTw==         0ms         0ms         0ms
                Rk8uTUVNT1J         0ms         0ms         0ms
             Q09NUFVURVJOQU         0ms         0ms         0ms
kk_summary.RklORFdJTkRPVw==         0ms         0ms         0ms
kk_summary.RklOREJST1dTRVI=         0ms         0ms         0ms
kk_summary.RklMRVBPUy5UQUlM         0ms         0ms         0ms
```

这里要留意读写的时长



### 1.5 mongo存储结构

#### 基础

##### Data files

每个mongo 有命名空间文件，日志文件和数据文件，数据文件是所有数据和索引所居住的地方。

每个数据文件(data files)有BSON文档，索引和mongo存储结构关系（被成为extents）.

每个data files 都 由很多复杂的extens组成。

##### Extents

由上提及， extens是在data files内存储文档和索引的。

![](http://ovolonhm1.bkt.clouddn.com/mongo_datafile.png)

* 一个extent 只能包含一个集合或一个集合内的索引
* 一个新的exten创建将会用剩余的data files，如果没有将会创建新的data files

#### db.stats()之前

这里我们理解下： db.stats的dataSize, storageSize 和 fileSize

![](http://ovolonhm1.bkt.clouddn.com/db_stats.png)

* dataSize 图中黄色部分，当你删除文档时会使dataSize减少，但是当你减少你文档中的内容并不会减少， 因为原文档的空间已经被分配出去了，不能提供给其他文档使用。

  或者你更新一个文档用更多的数据，它的dataSize仍然不变，只要这些数据在padding范围内。

* storageSize

  这个大小其实等于所有data extents(不包括index)大小, 它要比dataSize大， 其中有data删除的，移动的，没有设置的空间。

  storageSize不会减少，当你删掉文档或者减少文档中的数据

* fileSize

  fielSize 是所有data extents,index extents 和 没有配置的空间，这表示数据库在你硬盘的存储空间。

  只有你删掉一个库会减少，删掉集合或文档都不会减少。




### 2

下方方法都是进入到 mongo里执行：

#### stats()

显示当前数据库状态，包含数据库名称，集合个数，当前数据库大小, 单位为byte

```json
>db.stats()
{
"db" : "yc_driver", //当前数据库
"collections" : 5, //当前数据库多少表
"objects" : 2911281, //当前数据库所有表多少条数据
"avgObjSize" : 240.28991086741541, //每条数据的平均大小
"dataSize" : 699551452, //所有数据的总大小
"storageSize" : 858513408, //所有数据占的磁盘大小
"numExtents" : 21,
"indexes" : 5, //索引数
"indexSize" : 569229472, //索引大小
"fileSize" : 2080374784, //预分配给数据库的文件大小
"nsSizeMB" : 16,
"dataFileVersion" : {
    "major" : 4,
    "minor" : 5
    },
"extentFreeList" : {
    "num" : 0,
    "totalSize" : 0
    },
"ok" : 1
}
```







#### serverStatus()

##### 当前库使用的内存

`>db.serverStatus().mem`

```
{
"bits" : 64,
"resident" : 46662,
"virtual" : 326198,
"supported" : true,
"mapped" : 161399,
"mappedWithJournal" : 322798
}
```

注意resident 这里指的是占用内存大小，单位为M



##### stack

mongo中每一个连接都是一个线程，需要一个stack,查看当前连接数：

`db.serverStatus().connections`

查看stack的限制：

```
[root@bogon img]# ulimit -a | grep stack
stack size              (kbytes, -s) 8192
```

查看当前mongo连接数：

```
> db.serverStatus().connections
{
"current" : 2372,
"available" : 48828,
"totalCreated" : NumberLong(185449264)
}
```



调节stack大小：`ulimit -s 1024`



#### currentOp()

`db.currentOp()`   显示当前库所有正在操作的进程列表：

```json
>db.currentOp()
{ "inprog" :   
    [   
        {  
            "opid" : 3434473,//操作的id  
            "active" : <boolean>,//是否处于活动状态  
            "secs_running" : 0,//操作运行了多少秒  
            "op" : "<operation>",//具体的操作行为,包(insert/query/update/remove/getmore/command) 
            "ns" : "<database>.<collection>",//操作的命名空间，如：数据库名.集合名  
            "query" : {//具体的操作语句  
        				},  
            "client" : "<host>:<outgoing>",//连接的客户端信息  
            "desc" : "conn57683",//数据库连接描述  
            "threadId" : "0x7f04a637b700",//线程id  
            "connectionId" : 57683,//数据库连接id  
            "locks" : {//锁的相关信息  
                "^" : "w",  
                "^local" : "W",  
                "^<database>" : "W"  
                },  
            "waitingForLock" : false,//是否在等待并获取锁，  
            "msg": "<string>"  
            "numYields" : 0,  
            "progress" : {  
                "done" : <number>,  
                "total" : <number>  
                }  
            "lockStats" : {  
            "timeLockedMicros" : {//此操作获得以下锁后,把持的微秒时间  
                "R" : NumberLong(),//整个mongodb服务实例的全局读锁  
                "W" : NumberLong(),//整个mongodb服务实例的全局写锁  
                "r" : NumberLong(),//某个数据库实例的读锁  
                "w" : NumberLong() //某个数据库实例的写锁  
                },  
            "timeAcquiringMicros" : {//此操作为了获得以下的锁，而耗费等待的微秒时间  
                "R" : NumberLong(),//整个mongodb服务实例的全局读锁  
                "W" : NumberLong(),//整个mongodb服务实例的全局写锁  
                "r" : NumberLong(),//某个数据库实例的读锁  
                "w" : NumberLong()//某个数据库实例的写锁  
                }  
                    }  
            },  
            .....  
          
    ]   
}  
```

可以用 db.killOp( opid ) , 杀掉异常的操作，opid在上方。

如果没有返回一个空数组

杀掉当前所有的opid: 

```js
db.currentOp().inprog.forEach(function(cop){
db.killOp(cop.opid)
})
```



### 3导入导出

解决问题前可以把数据先导出备份



### 4其他

#### 建索引

观察日志： /var/log/mongodb/mongod.log

发现一些查询语句, 然后看它的索引是否存在 `db.col.getIndexes()`  或者： `db.system.indexes.find() `

不存在则建立索引`db.brands.ensureIndex({name:1},{unique:true})`  unique 要考虑



####getMongo

```
> db.getMongo()
connection to 127.0.0.1
```

查看当前数据库的链接机器地址 



#### MongoDB释放内存的命令

`mongo> db.runCommand({closeAllDatabases:1})`



#### com.mongodb.MongoException: Lock not granted. Try restarting the transaction 

1. 内存不够
2. qurey响应的条件没有建立索引