tags: [java] date: 2016-07-23


### 相关配置
![](http://7xs1eq.com1.z0.glb.clouddn.com/mybatis.png)

### 传参

* 传递多参数 
  根据id改变 name 和 age
  `public void updataData(int id,String name,int age);`

```xml
<mapper>
<update id = "updataDdata">   
update record_t t set t.name = #{1},t.age = #{2} where t.id = #{0}
/update>
</mapper>
```
上面的数字代表updataData中参数的位置，注意，这样写就不要写 parameType了。

* 传递多参数之绑定用法（这个好）
  还是上面的函数

```java
public void updateData( @Param(value = "pId") int id,
                        @Param(value = "pName") String name,
                        @Param(value = "pAge") int age);
```

```xml
<mapper>
<update id = "updateDdata">   
update record_t t 
set 
    t.name = #{pName},
    t.age = #{pAge} 
    where t.id = #{pId}
/update>
</mapper>
```
这样可以直接使用上面方法的参数来用，这样语义明了，也不用写parameType,推荐这样写。

* 传入javaBean实体entity
  javabean(entity) :
```java
package com.aim.entity
public class RoleScore{
    private String _Name;
    private int _Score;
    private int _Id;
    
    //get set 方法
}

```
repo ：
```java
package com.aim.repo;
public inteface PlayScoreRepo{
    public void updateData( RoleScore entity);
}
```
mapper：
```xml
<mapper namespace = "com.aim.repo.PlayScoreRepo">
<update id = "updateDdata" parameterType = "com.aim.entity.RoleScore >   
update record_t t 
set 
    t.name = #{_Name},
    t.age = #{_Age} 
    where t.id = #{_Id}
/update>
</mapper>
```
此时，如果RoleScore类里面多了个类，比如RoleScoreInside类，这个类里面有两个属性，sex,time. 

```java
public class RoleScore{
    private String _Name;
    private int _Score;
    private int _Id;
    private RoleScoreInside other;
    
    //get set 方法
}
```

这时传参其他都没变，就多了调用，如：

```xml
<mapper namespace = "com.aim.repo.PlayScoreRepo">
<update id = "updateDdata" parameterType = "com.aim.entity.RoleScore >   
update record_t t 
set 
    t.name = #{_Name},
    t.age = #{_Age} ,
    t.sex = #{other.sex},
    t.time = #{other.time},
    where t.id = #{_Id}
/update>
</mapper>
```
### sql id 及inclusde refid用法
通过这个语句达到SQL最大的复用

```xml
<Mapper namespace = "" >
<sql id = "aim_column"> 
    id,name,sex,score
</sql>
<select id = "" parameterType = "" resultType = "">
select <include refid = "aim_colum"> from t where id = #{id}
</select>

```

### sql复用
在mybatis中，我们可以將sql语句中公共的部分提取出来，然后需要该段sql的地方通过include标签引入即可，这样可以达到sql语句复用的目的。 
例如我们有两条相似的查询语句：

```java
<select id="queryUserInfoByName" parameterType="string"  resultType="user">
        select * from User where username = #{username}
</select>
<select id="queryUserInfoByPhone" parameterType="string"  resultType="user">
        select * from User where phone = #{phone}
</select>
```

我们可以通过``标签，把公共的部分定义成一个块：

```java
<sql id="queryUserInfo">
        select * from User where 
</sql>
```

则上面的查询语句可以改写成：

```java
<select id="queryUserInfoByName" parameterType="string"  resultType="user">
        <include refid="queryUserInfo"></include> username = #{username}
</select>
<select id="queryUserInfoByPhone" parameterType="string"  resultType="user">
        <include refid="queryUserInfo"></include> phone = #{phone}
</select>
```


### if标签
拿查询语句举例：
在severs层里得写if(score!=null)
```xml
<!--普通做法-->
select * from 表名 where id = 2 and score => 25
```
用if写法：
```xml
<select id = "" parateType = "entity" resultType = "entity">
select * from 表名 where id = 2
<if test = "score!=null">
and score > 25
</if>
</select>
</select>
```

### where 标签
在where标签处会动态生成where
不需要关心标签中的输出
去除多余的and 和 or
例子：
当id!= null 时用id查，否则不使用id查
当score!=null 时用score查询，否则不使用score查询

```xml
select * from 表 
where 
<if test ="id!=null">
id = #{id}
</if>
<if  test = "score != null">
and score score >25
</if>

```
动态where
```xml
select * from 表 
<where>
<if test = "id!= null">
id = #{id}
</if>
<if test = "score !=null">
and score >25
</if>
</where>
```
这里动态where标签会自动的判断他包括的sql语句，会使其符合sql语句的规范而输出，比如省略and,两个if都不满足就不输出等。

### set 标签 
在update语句时，set后会有多个if标签，参考前面的where标签，这个标签也是动态的识别标签内的值，去掉逗号等多余的语句。
```xml
update 表名
<set>
<if test = " name != null and name !=' '">
    name = #{name},
</if>
<if test = "score ! = null and score !=''">
    score = #{score},
</if>
<if test = "role!= null and role!=''">
    role = #{role}
</if>
</set>
where id = #{id}

```









