
Tags:[slq, 数据库] date: 2016-07-18

## MySql

### 配置（免安装版）

- 解压安装

将下载好的 zip 压缩包解压到自己喜欢的文件夹，为了避免可能出现的错误，建议文件路径中不包含中文名以及空格。下文以 C:\mysql 这一路径为例进行讲解。

- 配置环境变量

将路径 `C:\mysql\bin`  加入到 PATH 环境变量之后，用户变量或者系统变量即可，毕竟我们的个人电脑一般都是一个用户。

这一部的目的主要是为了在非 `C:\mysql\bin` 的其他路径下也能使用 mysql 命令。如果不添加环境变量，那么我们每次在命令中执行 mysql 命令还需进入到 `C:\mysql\bin` 路径下才能执行。

- 编辑配置文件

路径 `C:\mysql` 下有一份初始的默认配置文件，即 `my-default.ini` 文件。在此路径下，新建一份自己的配置文件 `my.ini` (不要使用其他名称)，然后将 `my-default.ini` 中的内容复制过来并保存。

使用文本编辑器打开 `my.ini` ，修改以下几项。还有其他很多参数也都可自定义，感兴趣的同学可以继续研究。下面这几个是最重要的也是我们必须要修改的。

```ini
# 默认字符集
default-character-set = utf8
# mysql 安装路径
basedir = C:\mysql
# mysql 数据文件夹路径，不要怕，我们现在确实还没有创建这个 data 文件夹
datadir = C:\mysql\data
# mysql 服务器监听的 TCP/IP 端口号
prot = 3306
```

- 安装 mysql 服务

以管理员身份打开命令提示符，进入到 `C:\mysql\bin` 路径下，执行：

```shell
$ mysqld install
```

**！！！注意：** 是 `mysqld` 而不是 `mysql` 。

此时，Win+R 运行键入 `services.msc` 打开服务，我们可以看到服务列表中已经有了 M有SQL 服务，说明安装成功。

- 初始化 data 文件夹

免安装版的 M有SQL 解压安装之后，在其安装根目录下是没有 data 文件夹，需要我们手动初始化生成，这是最重要的一步。

以管理员身份打开命令提示符，进入到 `C:\mysql\bin` 路径下，执行：

```shell
$ mysqld --initialize --console
```

执行上述命令，命令提示符会出现一堆提示信息，我们只关注最后一行的提示信息：

```sh
[Note] A temporary password is generated for root@localhost: ******
```

注意到冒号之后的字符串，那是 MySQL 为我们生成的初始密码，请记住，接下来会用到。

- 启动 MySQL 服务

打开命令提示符，执行下面命令以启动 MySQL 服务：

```shell
$ net start mysql
```

- 修改 MySQL 初始密码

在启动了 MySQL 服务之后，键入以下命令登录到 MySQL 数据库：

```shell
$ mysql -u root -p
```

回车执行上述命令时，会提示我们输入密码，把刚才 MySQL 生成的初始密码键入以登录。

一旦登录进数据之后，直接执行命令：

```shell
SET PASSWORD = PASSWORD('这里输入你要设置的新密码');
```

回车执行即可完成登录密码的修改。

修改完密码之后，退出数据库，重新启动 M有SQL 服务才会生效。

### 命令操作

- 管理员进cmd,进入安装目录。

  cd C:\Program Files\MySQL\MySQL Server 5.7\bin

- 输入：mysqld install   显式 Service successfully installed 服务成功启动

- mysql -u root -p   进入根用户 下面会让你输入密码

- show databases;  显示有哪些数据库

- create database fist;  创建一个数据库 ，first是我数据库的名字

- use first;       选择刚才创建的数据库

- show tables;  看看选择的数据库中有什么表

- create table birthday(name varchar(10),sex char(1),birth DATE,birthAdd VARCHAR(20));   创建一个birthday的表，姓名，性别，出生日期，出生城市。

- 这时候可以再看看有什么表 show tables;

- describe birthday;  显式表的结构
  ​



## NoSql
绝大部分非关系型数据库都是NoSQL数据库，这以为着不能支持JION之类的操作，这是一种权衡的结果，因为这样就能够做到读取的速度更快，以及通过数据分别存储到不同的服务器甚至不同的数据中心，方便的实现去中心化的数据存储。
现代的nosql数据库分四类：

### 键值数据库
用起来和python字典非常相似，每个键和一个单独的值相关联，通过键可以取出值，不支持值的查询。值可以是任意数据。不论数据库数据量有多大，读取的速度都不会改变。因为这样的特性，对于大多数应用来说不适合做主数据库，适合保存在一段时间会过期的简单对象，比如保存用户的会话数据和购物车数据。另外键值数据库普遍用来为引用和其他数据库做缓存。
最流行的键值数据库是`Redis,Riak和Amazon DynamoDB`

### 文档数据库
在数据库保存的**键值对集合**叫做文档，是无固定表结构，就是说一个文档的结构不需要跟另外一个文档一样。
在文档创建后，可以添加更多的键值。
大多数文档数据库会把数据库以JSON(Java Script Object Notation)或JSON的超集或XML的格式来储存。
最流行的文档数据库是`MongoDB,CouchDB及Couchbase`

### 列式数据库和基于图的数据库
这里先不做记录，接触的比较少。

___

## MongoDB
MongoDB是最流行的NoSql数据库，是一种用文档存储的数据库。
文档是由BSON个数定义的。BSON是JSON的超集，意思是二进制的json(Binary JSON)。
BSON允许把JSON存为二进制格式，而不是字符串格式，这样能洁身大量空间。

安装：
https://www.mongodb.com/download-center#community
默认给按到cpan 
安装后，cmd进入bin目录（或者在path环境变量中配置）：
启动mongod：
![](http://7xs1eq.com1.z0.glb.clouddn.com/QQ%E5%9B%BE%E7%89%8720170108112334.png)
你会看到有exception in initAndListen: 29 Data directory C:\data\db\ not found., terminating的错误。
把命令改成：`mongod --dbpath D:\MongoDB\data`
当然，前提你得建立这个文件夹。
![](http://7xs1eq.com1.z0.glb.clouddn.com/QQ%E6%88%AA%E5%9B%BE20170111120031.png)
窗口关闭，服务就关闭了。

### 可视化工具Robomongo
https://robomongo.org/download.
用法很简单，相信你能看会。



















