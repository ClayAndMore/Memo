### 写在前面

几件事情： 

1， 统计一个大文件（5G）中，某个单词的数量？

2， 计算某数据库中，男性和女性中的数据？

3，统计北京市中，各大品牌汽车的数量

这些问题最好最快的解决方式是分多任务并行，然后归总到一起。这也是MapReduce的核心思想。



### 为什么叫MapReduce?

分为两大步： Map Task -> Reduce Task, 

map的结果聚到一起给Reduce:

![](http://claymore.wang:5000/uploads/big/0aa53ff729d412716281235f0c7922c7.png)

1. 从HDFS输入，再输出到HDFS, 中间不会再次牵扯到HDFS， HDFS-map-HDFS.

2. Split, 切片是一个逻辑概念，默认是一个split对应一个block，或者对应一行。这里的一个切片对于一个map程序。

3. map的数量由split来决定，reduce的数量最好由核心数来决定，较少进程切换。

MR 原语：
map输出k:v的形式，如统计表格：男：1， 输出后sort 分组，比如男的一组，女的一组。

**相同的key为一组，调用一次reduce方法，方法内迭代这一组数据进行计算。**



把一个map task 和 一个 Reduce task 拆出来看：

![](http://claymore.wang:5000/uploads/big/6dab98ba388c374463781455914baf50.png)

map task:

1. map->buffer直接输出的其实是 k-v-p(partition分区)
2. 输入->map->buffer, 都是在内存中进行，直到buffer满(默认100M), 做一次io,到硬盘，不是HDFS，而是系统的文件系统。
3. 到硬盘的同时会跟进partition来分块。此时内部有序，外部无序。
4. 所有的硬盘上的buffer输出会合成一个文件
5. 不同的partition拉取自己的块(fetch)， 拉取块的过程称之为shuffer.

reduce

1. 归并排序 merge，然后计算
2. 合成两个文件就可以计算。



注意一点：如果一个文件每行都是 hello,  统计次数的话， 如果进map,输出也是hello:1, hello:1, hello:1 …



计算向数据移动

1.x  jobTracker(主) 和 taskTracker(从)

弊端： 

* jobTracker 负载过重， 单点故障。
*  资源管理与计算强度强耦合，其他计算框架需要重复实现资源管理
* 不同框架对资源不能全局管理， 对同一资源可能会冲突

2.x

为了解决jobTracker的弊端，

新资源管理 YARN 代替了jobTracker。每次计算都要向 YARN 申请资源。