PostgreSQL(也称为`Post-gress-Q-L`)由PostgreSQL全球开发集团(全球志愿者团队)开发。 它不受任何公司或其他私人实体控制。 它是开源的，其源代码是免费提供的。

PostgreSQL是跨平台的，可以在许多操作系统上运行，如Linux，OS X和Microsoft Windows等。

官网：https://www.postgresql.org/download/



### centos 6

可先查看相关版本：

`yum list postgres*`

`yum install postgresql-server -y`

初始化数据库

```
`service postgresql initdb`
```

设置自动启动

```
`chkconfig postgresql on``service postgresql start`
```



配置监听地址为所有IP

默认postgresql只在127.0.0.1上进行监听

进入PGDATA目录(默认在/var/lib/pgsql/data/),找到文件postgresql.conf,增加

```
`cd` `/var/lib/pgsql/data/``vim postgresql.conf``listen_addresses = ``'*'`
```

设置认证模式，内网中采用password密码认证的方式,在文件pg_hba.conf文件中增加

```
`host    all             all             0.0.0.0``/0`               `password`
```

password 或 md5 , 都是密码验证。

修改默认用户postgres的密码

```
`su` `- postgres``psql``alter user postgres with password ``'123456'``;`
```

重新启动postgresql的服务

`service postgresql restart`

登录测试

```
psql -h 192.168.230.128 -p 5432 -U postgres
```

\会提示输入密码，输入刚刚设置过的密码

登录成功表示刚刚设置正确





### 控制命令

运行PostgreSQL的交互式终端程序，它被称为*psql*， 它允许你交互地输入、编辑和执行SQL命令。

登录到相关用户的psql shell 后， 一些命令：

* \?：查看psql命令列表。

* \l：列出所有数据库。

* \c [database_name]：连接其他数据库。

* \d：列出当前数据库的所有表格。

* \d [table_name]：列出某一张表格的结构。

* \du：列出所有用户。

* \conninfo：列出当前数据库和连接的信息。
* \password命令（设置密码）
* \q命令（退出）



基本操作：

```sql
# 创建数据库
create database mydb;
# 删除数据库
drop database mydb;
# 创建新表
CREATE TABLE user_tbl(name VARCHAR(20), signup_date DATE);
# 插入数据
INSERT INTO user_tbl(name, signup_date) VALUES('张三', '2013-12-22');
# 选择记录
SELECT * FROM user_tbl;
# 更新数据
UPDATE user_tbl set name = '李四' WHERE name = '张三';
# 删除记录
DELETE FROM user_tbl WHERE name = '李四' ;
# 添加栏位
ALTER TABLE user_tbl ADD email VARCHAR(40);
# 更新结构
ALTER TABLE user_tbl ALTER COLUMN signup_date SET NOT NULL;
# 更名栏位
ALTER TABLE user_tbl RENAME COLUMN signup_date TO signup;
# 删除栏位
ALTER TABLE user_tbl DROP COLUMN email;
# 表格更名
ALTER TABLE user_tbl RENAME TO backup_tbl;
# 删除表格
DROP TABLE IF EXISTS backup_tbl;
```

