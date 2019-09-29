Tags:[sql, database] date: 2016-07-16 

## 数据库范式

### 概念
属性：每一列的列名
属性值：属性的值。
完全函数依赖：就是一组属性对应唯一一个其他属性，且这组属性中的任何一个对应其他属性不成立（这组属性的真子集x->y不成立）。
码（候选码）：上面的那组属性。
主属性：码中的属性。
非主属性：除了主属性的其他属性。
范式：nf(normal form)

### 范式
* 第一范式(1NF):属性或属性值不可分割。
* 第二范式（2NF):其他字段**完全依赖**于主键（候选码）。
* 第三范式（3NF):消除多表的数据冗余。
* BCNF：消除主属性对于码的传递性依赖。
  传递性依赖：如 Z 函数依赖于 Y，且 Y 函数依赖于 X （严格来说还有一个X 不包含于Y，且 Y 不函数依赖于Z的前提条件），那么我们就称 Z 传递函数依赖于 X.
  （BCNF)如：

  ```码:仓库名，管理员，物品，
  非主属性：数量，
  传递依赖：管理员->仓库名->物品
  ```

  消除依赖（两张表）：
  `仓库名->管理员`
  `仓库名->物品->数量`

## SQL语言

SQL语言(Structured Query Language,结构化查询语言),是一种通用的关系型数据库访问语言。
SQL语句已经成为一种国际标准，它用于描述需要执行哪些操作，而没有描述如何执行，数据库引擎会解释SQL语句。
数据库CRUD(增查改删）。

### SQL集成工具集

| 语言     | 工具集                               |
| ------ | --------------------------------- |
| java   | JDBC(Java Database Connecivity)   |
| python | Python DB                         |
| c#     | ADO.NET                           |
| c++    | Pro*C(oracle),MySql C Api and DB2 |



### 查询语句
**Select 字段列表 From 数据表名 Where 查询条件 Order By 排序方式 Group By 分组方式**

* 字段列表可以理解成竖着那一列啦
* Select子句和From子句是必须的，其他都是可选的
* 如果查询整个表,比如表明为：工作单位表，Select * From 工作单位表。***是字段通配符，表示该数据表中的所有字段**
* 表中有两列字段（Id啦，单位名称啦），可以这样：
  `Select ID, 单位名称 From 工作单位表`
* 查某值的所有信息 
  `Select * From 工作单位表 Where 单位名称 = “蓝天公司” `
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/QQ%E6%88%AA%E5%9B%BE20160422153431.png)
```
         select birth from birthday where name = '张三';
```

### 新增数据
Insert语句用于新增数据库记录，用法：
**Insert Into 表名 (字段列表) Values（数值列表）**
```
    Insert Into 工作单位表 
                (ID,单位名称，单位地址，负责人）
    Values
                (20,'天海公司','珠江路100号','张三')
```
若字段中有单引号，用两个连续的单引号进行转移
有的数据库引擎是双引号
```
         insert into birthday set name='张三',sex='男',birth='1994-01-01',birthAdd='沈师大门';
         insert into birthday values ('李四','男','1994-03-30','五环');

```

### 修改数据库
Update语句用于修改数据库记录，用法：
**Update 表名 Set 字段名1=数值1，字段名2=数值2 Where 查询条件**
```
    Update 工作单位表 Set 
             单位名称 = '地龙公司',
             单位地址 = '珠江路100号',
             负责人   = '李四',
    Where ID = 20
```
==========
```
        update birthday set birth = '1995-06-06' where name = '张三';
```
注意，要设置Where语句，否则会更改所有记录，造成灾难性的后果。

### 删除数据
Delete语句用于删除数据库记录
**Delete Form 表名 Where 查询条件**

    Delete From 工作单位表
    Where ID = 20 
这个SQL语句能删除ID值为20的所有记录
注意，要设置Where语句，否则删除所有记录，造成灾难性的后果

             delete from birthday where name = '李四';

### 函数
可以在语句中调用函数，这些函数从来源上可以分为三类：

* 标准函数   ANSI SQL标准定义的函数，所有数据库都支持的
* 系统特定函数  由特定数据库定义的函数
* 用户自定义函数 这个不用解释了吧

从功能上可分为：

* 合计函数：
* Count：累计数据库记录的个数，查询结果是个整数，当用Count（*）返回所有记录的个数 用法：
   `Select Count(*) From Orders` //* 可换成字段 如：OrderPrice
* Max：获取字段值的最大值
* Min: 获取字段值的最小值
* Arg: 获取字段值的算术平均值
* Sum：获得字段值的总和  
* 标量函数：
* Abs: 获得数值的绝对值
* Sin：略
* Cos：略

  <hr>
## SQL扩展

### 修改表：
```sql
atler table <表名>     //对表修改
    add<列名><数据类型>[约束] //加一列
    drop。。。                  //删除一列

drop table 表名  //删除一章表 和delete相比，delete删除的是数据

eg:
    alter table students add sclass char{20}
    alter table students add constraint sage check (saga between 15 and 40)
```
### select的修改 
选择列的时候可以做些修改，比如表里有年龄，但是要出生年份，就可以在选择的时候使用2016-sage，这样直接返回的就是出生年份
还可以跟字符串，跟一些函数
或者换一个列名，起一个别名，如下面的汉字
```sql
select snage 姓名,'year of birth:'.2016-sage 出生年份,LOWER(sdept) form student
```
### 一些关键字
* between关键字
  where 条件 可以跟 where age between 17 and 19
* in 关键字 也可以是not in
  select * from biao where age in ('17','18','19')
* like 关键字 近似匹配,也可以是 not like
  跟两种符号连用 % ,_，也可以没有符号，但是会变成精准的匹配
  select * from biao where name like '王%'
  用%表示王后面可以是零到多个字符，如王一一，`_`表示一个字符如'a_'，但是一个汉字是两个字符所以是'王__'
* 转义符
  由上一条可知，如果要找的关键字里有`%_`，可用转义：like 'DB\_Design' escape '\'
* 空值查询
  is null 
  where grade is null，无值的会输出
  不为空 
  is not null 
  where grade is not null ,有值的会输出

* and 和 or 
  where name = 'cs' and grade <20
  where name = 'cs' or name = 'as'

* 对查询结果进行排序
  order by 列名 desc/asc 降序/升序
  select * from Student order by age asc,grade desc
  查询结果按照年龄的升序排序，同一年龄的按照成绩的降序排序

### 嵌套
父查询，子查询用小括号括起
求解顺序由内向外
```xml
select * from student where class in(
select class from student where name = '王红’
)

select * from student where sage = (
    select sage form Student where sno='21212'
)
```
上面第一个是结果多值查询用in 来选择集合，而单值可以用等号
相关子查询exists（存在）,后面跟的是为真或者为假，顺序由外向内
```xml
select name from student where exists(
    select * from sc where sno = student.sno and con = 1
) 
```

### 聚集函数
count ([distinct|all] 去重|不去重 *)表中的行数
count （[distinct|all] 列名）表中的某一列的个数
sum () 求和
max()
min()

```xml
select count(*) from student //求学生表中的行数
select count(distinct sno) form sc // 去掉重复的学号，共有多少
```
分组
```xml
select cno,count(sno) from SC group by cno having count(sno)>2
<!---求男生里面成绩最好的和女生里面成绩最好的-->
select ssex,MAX(grade) from Student,SC where Student.Sno = SC.Sno
group by ssex
```
输出：

| （无列名） | ssex | (无列名) |
| ----- | ---- | ----- |
| 1     | 男    | 98    |
| 2     | 女    | 88    |

上面用了自然连接Student.Sno = SC.Sno将两个表连接起来，注意，分组时ssex目标列在其中没有用到聚集函数，而目标列中有聚集函数，这时，分组group中一定要有没有聚集函数的字段。

### 左连接与右连接

- left join(左联接) 返回包括左表中的所有记录和右表中联结字段相等的记录 
- right join(右联接) 返回包括右表中的所有记录和左表中联结字段相等的记录 
- inner join(等值连接) 只返回两个表中联结字段相等的行 
- full outer join(全连接) 返回两个表中所有数据 (这就不做介绍了)

![](http://7xs1eq.com1.z0.glb.clouddn.com/left%20jion.png) 

```java
  select *from A
  left join B
  on A.aID = B.bID
```

![](http://claymore.wang:5000/uploads/big/6750bff86c5cbc04d5dcb83420a57702.png)

结果说明: left join是以A表的记录为基础的,A可以看成左表,B可以看成右表,left join是以左表为准的. 换句话说,左表(A)的记录将会全部表示出来,而右表(B)只会显示符合搜索条件的记录(例子中为: A.aID = B.bID). B表记录不足的地方均为NULL.**左边外部联接将包含了从第一个（左边）开始的两个表中的全部记录，即使在第二个（右边）表中并没有相符值的记录。**

```java
  select *from A
  right join B
  on A.aID = B.bID.
```

![](http://claymore.wang:5000/uploads/big/ee985b0f789bed23f57a69192ba3d7dd.png)

```java
  select *from A
  innerjoin B
  on A.aID = B.bID
```

![](http://claymore.wang:5000/uploads/big/1af1d5d8894c0be7e3cf18ae7a2ccc6e.png)



语法：FROM table1 LEFT JOIN table2 ON table1.field1 compopr table2.field2 

说明：

- table1, table2参数用于指定要将记录组合的表的名称。 


- field1, field2参数指定被联接的字段的名称。且这些字段必须有相同的数据类型及包含相同类型的数据，但它们不需要有相同的名称。 




### 多表查询

#### 笛卡尔积
![](http://claymore.wang:5000/uploads/big/c4b7b3801bf6da7ea6d4bf250562d01f.png)
selcet * from student ,sc 这样student和sc 会形成一个笛卡尔积的表

#### 多表连接
* 等值与非等值连接
  等值连接
  表1，列1 = 表2，列2
  非等值连接
  表1，列1 > 表2，列2

* 自然连接
  select student。* ,con,grade. 对于上面的等值连接，这样返回的是我们需要的，而且去掉了重复的列表

* 外连接
  左外连接 a left outer join b.以左边的表为基础，其他填充，没有的为空
  右外连接 a right outer join b 以右边的表为基础，其他填充，没有的为空
  全外连接 a full outer join b  全部的行都放在一个表

* 集合操作
  union 并集 与 or 相对应，默认去重
  intersect 交集 与 and 相对应，默认去重
  except 差集 
  操作前提：
  列数相同，每列对应的类型相同
  如这两个语句可以求并集
```xml
select * from student where class = 'cs'
union
select * from student where age >10
```
*  消除重复
   select distinct 列名 这样就是



### 经典题

#### 三表联合查询

A: Student(s_id,s_name)

B: Course(c_id,c_cname)

C:  Score(id,s_id,c_id,score）

学生表，课程表，成绩表

1，检索每个学生缺考的科目：

其实这题看上去会以为缺考是成绩为0,其实是没有记录

所以：

```mysql
select a.s_name ,b.c_name from a,b where not exists
(select * from c where a.s_id=c.s_id and b.c_id = c.id) 
```

2, 检索每个学生的平均成绩。

一看这题一般人会写出这样的答案：

```mysql
select a.s_name,avg(c.score) from a,c where a.s_id=c.s_id 
group by a.s_name
```

但是你没有考虑学生是否缺考的情况，这样的平均值只是现在现有的成绩的平均值

应该把缺考考虑进去：

```mysql
select a.s_name,sum(c.score)/(select count(*) from b) 
from a,c
where a.s_id=c.s_id 
group by a.s_name
```

这里除号后用了个子查询代替了count(b.id)，如果用count(b.id),from后就得跟b,where后得跟id判断。这时笛卡尔积的原因会导致整个符合条件的缺同学的平均成绩不是按总课程算。