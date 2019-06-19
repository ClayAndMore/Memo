为什么叫MapReduce?

分为两大步： Map Task -> Reduce Task, 

map的结果聚到一起给Reduce:

![](http://claymore.wang:5000/uploads/big/0aa53ff729d412716281235f0c7922c7.png)

1. 从HDFS输入，输出到HDFS, 中间不会再次牵扯到HDFS

2. Split, 切片是一个逻辑概念，默认是一个split对应一个block，或者对应一行。这里的一个切片对于一个map程序。

3. map的数量由split来决定，reduce的数量最好由核心数来决定，较少进程切换。

MR 原语：
map输出k:v的形式，如统计表格：男：1， 输出后sort 分组，比如男的一组，女的一组。

**相同的key为一组，调用一次reduce方法，方法内迭代这一组数据进行计算。**



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