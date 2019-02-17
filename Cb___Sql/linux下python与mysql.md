Tags:[slq, 数据库, linux_software] date: 2017-03-14 

### 安装mysql

* 更新源

  `sudo apt-get update`

* 可以先看下mysql的版本，确定是否存在：

  `mysql -V`或`mysql> status`

* 安装服务

  `sudo apt-get install mysql-server`

### mysql和python的中间件

* 安装 python-dev

  `sudo apt-get install python3-dev`

  linux发行版通常会把类库的头文件和相关的pkg-config分拆成一个单独的xxx-dev(el)包.    //pkg=package,包裹

  以python为例, 以下情况你是需要python-dev的

  - 你需要自己安装一个源外的python类库, 而这个类库内含需要编译的调用python api的c/c++文件  //如：安装使用WiringpisPi库需要python-dev
  - 你自己写的一个程序编译需要链接libpythonXX.(a|so)

* 安装MySQL-python

  要想使python可以操作mysql 就需要**MySQL-python**驱动，MySQLdb是用于Python链接Mysql数据库的接口。

  `sudo pip3 install MySQL-python`

* 测试是否安装成功：

  `python 3`

  `>>>import MySQLdb`

上述方法是一种，但是一直存在依赖等问题，在我用django 的时候，用`pip install mysqlclient `就解决了在我migration时需要安装中间件的问题。



### 进入mysql

开启服务：

`sudo service mysql start`

`mysql -u用户 -p` 然后输入密码

但是当我输入 `mysql -uroot -p`后会提示：

ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO) denied for user 'root'@'localhost' (using password: NO)

这是由于我们安装mysql时没有设置密码造成的。

解决方法：

1. ```shell
   #mysqld stop
   #mysqld_safe --user=mysql --skip-grant-tables --skip-networking &
   ```

   //此时进入了数据库，我们可以更改root用户的密码

   ```
   update mysql.user set authentication_string='123456' where user='root';
   ```

   * 5.7以后password改成了authentication_string
   * mysql表user中存储了数据库的用户

2. 直接使用/etc/mysql/debian.cnf文件中[client]节提供的用户名和密码: 

   ```mysql
   # mysql -udebian-sys-maint -p 

   Enter password: <输入[client]节的密码> 

   mysql> UPDATE user SET Password=PASSWORD(’newpassword’) where USER=’root’; 

   mysql> FLUSH PRIVILEGES; 

   mysql> quit 

   # mysql -uroot -p 

   Enter password: <输入新设的密码newpassword> 
   ```



### 数据库基本使用

* 看所有数据库：

  `show databases`

* 使用数据库

  `use datebasename`

* 看此数据库中的所有表

  `show tables`

* 看表的结构

  `desc tablename`

  ​

### 创建用户和创建数据库

* 创建用户

`create User 'username'@'localhost' identified by 'password'`

* 创建用户并授权

  格式：grant select on 数据库.* to 用户名@登录主机 identified by "密码"

  eg:

  增加一个用户user001密码为123456，让他可以在任何主机上登录，并对所有数据库有查询、插入、修改、删除的权限。首先用以root用户连入MySQL，然后键入以下命令：

  ` mysql> grant select,insert,update,delete on *.* to user001@"%" Identified by "123456";`

  eg:

  增加一个用户user002密码为123456,让此用户只可以在localhost上登录,也可以设置指定IP，并可以对数据库test进行查询、插入、修改、删除的操作 .

  这样用户即使用知道user_2的密码，他也无法从网上直接访问数据库，只能通过MYSQL主机来操作test库。

  首先用以root用户连入MySQL，然后键入以下命令：

  ` mysql>grant select,insert,update,delete on test.* to user002@localhost identified by "123456";`

* 创建数据库


  `create database 库名 `

* 创建表

  `create table 表名(字段设定)`

  eg:

  ```mysql
  mysql> create table name(
      -> id int auto_increment not null primary key ,  //auto_increment 自增
      -> uname char(8),
      -> gender char(2),
      -> birthday date );
  ```

  ​

* 删除表和删除库

  `drop table 表名`

  `drop database 库名`

* 备份数据库

  `mysqldump -u root -p --opt 数据库名>备份名; //进入到库目录`

* 恢复数据库

  `mysql -u root -p 数据库名<备份名; //恢复时数据库必须存在，可以为空数据库`