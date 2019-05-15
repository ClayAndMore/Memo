Tags:[sql, database] date: 2016-12-06




## 解压安装

将下载好的 zip 压缩包解压到自己喜欢的文件夹，为了避免可能出现的错误，建议文件路径中不包含中文名以及空格。下文以 C:\mysql 这一路径为例进行讲解。



## 配置环境变量

将路径 `C:\mysql\bin`  加入到 PATH 环境变量之后，用户变量或者系统变量即可，毕竟我们的个人电脑一般都是一个用户。

这一部的目的主要是为了在非 `C:\mysql\bin` 的其他路径下也能使用 mysql 命令。如果不添加环境变量，那么我们每次在命令中执行 mysql 命令还需进入到 `C:\mysql\bin` 路径下才能执行。



## 编辑配置文件

路径 `C:\mysql` 下有一份初始的默认配置文件，即 `my-default.ini` 文件。在此路径下，新建一份自己的配置文件 `my.ini` (不要使用其他名称)，然后将 `my-default.ini` 中的内容复制过来并保存。

使用文本编辑器打开 `my.ini` ，修改以下几项。还有其他很多参数也都可自定义，感兴趣的同学可以继续研究。下面这几个是最重要的也是我们必须要修改的。

``` ini
# 默认字符集
default-character-set = utf8
# mysql 安装路径
basedir = C:\mysql
# mysql 数据文件夹路径，不要怕，我们现在确实还没有创建这个 data 文件夹
datadir = C:\mysql\data
# mysql 服务器监听的 TCP/IP 端口号
prot = 3306
```



## 安装 mysql 服务

以管理员身份打开命令提示符，进入到 `C:\mysql\bin` 路径下，执行：

``` shell
$ mysqld install
```

**！！！注意：** 是 `mysqld` 而不是 `mysql` 。

此时，Win+R 运行键入 `services.msc` 打开服务，我们可以看到服务列表中已经有了 M有SQL 服务，说明安装成功。



## 初始化 data 文件夹

免安装版的 M有SQL 解压安装之后，在其安装根目录下是没有 data 文件夹，需要我们手动初始化生成，这是最重要的一步。

以管理员身份打开命令提示符，进入到 `C:\mysql\bin` 路径下，执行：

``` shell
$ mysqld --initialize --console
```

执行上述命令，命令提示符会出现一堆提示信息，我们只关注最后一行的提示信息：

``` sh
[Note] A temporary password is generated for root@localhost: ******
```

注意到冒号之后的字符串，那是 MySQL 为我们生成的初始密码，请记住，接下来会用到。



## 启动 MySQL 服务

打开命令提示符，执行下面命令以启动 MySQL 服务：

``` shell
$ net start mysql
```



## 修改 MySQL 初始密码

在启动了 MySQL 服务之后，键入以下命令登录到 MySQL 数据库：

``` shell
$ mysql -u root -p
```

回车执行上述命令时，会提示我们输入密码，把刚才 MySQL 生成的初始密码键入以登录。

一旦登录进数据之后，直接执行命令：

``` shell
SET PASSWORD = PASSWORD('这里输入你要设置的新密码');
```

回车执行即可完成登录密码的修改。

修改完密码之后，退出数据库，重新启动 M有SQL 服务才会生效。



## Mysql 一些命令

- 管理员进cmd,进入安装目录。

  cd C:\Program Files\MySQL\MySQL Server 5.7\bin

- 输入：mysqld install   显式 Service successfully installed 服务成功启动

- mysql -u root -p   进入根用户 下面会让你输入密码

- show databases;  显示有哪些数据库

- create database fist charset=utf8;  创建一个数据库 ，first是我数据库的名字,并指定了字符集。

- use first;       选择刚才创建的数据库

- show tables;  看看选择的数据库中有什么表

- create table birthday(name varchar(10),sex char(1),birth DATE,birthAdd VARCHAR(20));   创建一个birthday的表，姓名，性别，出生日期，出生城市。

- 这时候可以再看看有什么表 show tables;

- describe birthday;  显式表的结构



## ubuntu下安装

1. sudo apt-get install mysql-server
2. apt-get isntall mysql-client
3. sudo apt-get install libmysqlclient-dev

中间提示输入用户密码。

`sudo netstat -tap | grep mysql`

成功的话会显示监听端口。但不是连接mysql的端口。

`show global variables like 'port'`

显示mysql的端口。（先进入mysql）



查看mysql状态：service mysql status （查看所有服务的状态： service --status-all）

启动mysq: service mysql start

关闭mysql: service mysql stop



## navicat远程连接Linux中的mysql

安装好后，在：

`vi /etc/mysql/mysql.conf.d/mysqld.cnf` 中修改访问限制ip,默认只有本地可以访问：

其中一行 bind-address = 127.0.0.1 
前边加 #注释掉 保存（可能会遇到提示 readonly 请自行修改权限）

接下来进入mysql:

执行：

```
mysql>grant all privileges on *.*  to  'root'@'%'  identified by 'youpassword' with grant option;
mysql>flush privileges;
```

防火墙开启3306 端口。

如果是云服务器，确认开启安全组。



## 修改mysql字符集

当前mysql支持的字符集，字符序和字符集占用的最大长度等信息：

`show character set;`

查看当前MySql会话使用的字符集：

`show variables like 'character%';`

character_set_client: 客户端来源数据使用的字符集 
character_set_connection: 数据通信链路的字符集，当MySQL客户机向服务器发送请求时，数据以该字符集进行编码 
character_set_database: 数据库字符集
character_set_filesystem: MySQL服务器文件系统的字符集，该值是固定的binary。
character_set_results: 结果集的字符集，MySQL服务器向MySQL客户机返回执行结果时，执行结果以该字符集进行编码 character_set_server: 内部操作字符集(MySQL服务实例字符集) 
character_set_system: 元数据(字段名、表名、数据库名等)的字符集默认为utf8

### 修改默认编码集

先关闭MySql服务：`service mysql stop`

`vi /etc/mysql/mysql.conf.d/mysqld.cnf`

在`[mysqld]`中相关配置中最下方加入：`character_set_server = utf8`

保存后重启服务：`service mysql start;`

现在可再次进入mysql查看编码集。



## windows 导出数据库到 linux

进入mysql的data 目录，进入命令行：

执行：`mysqldump -u root -p --databases 数据库名 > D:/database_out/graduation.sql`



### Django 连接Mysql

安装mysql后需要安装 Mysql-python ,

`pip install Mysql-python`

但是会提示：mysql_config not found

这时我们需要安装一个包，

`apt-get install libmysqlclient-dev`

这时再安装就可以了。