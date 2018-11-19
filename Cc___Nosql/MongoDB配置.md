### 安装和配置

ubuntu：

`apt-get install -y mongodb`

默认安装在了： `/usr/bin/` 下。

在该路径下：

`./mongod` 可运行MongoDB服务。

`./mongo`   运行MongoDB后台管理shell,它是自带的js shell,当进入时，会默认链接到test文档（数据库）。

eg:

```
$ cd /usr/local/mongodb/bin
$ ./mongo
MongoDB shell version: 3.0.6
connecting to: test
Welcome to the MongoDB shell.
……
> db.runoob.insert({x:10})
WriteResult({ "nInserted" : 1 })
> db.runoob.find()
{ "_id" : ObjectId("5604ff74a274a611b0c990aa"), "x" : 10 }
>
```



#### 离线安装

去官网下载相关包：https://www.mongodb.com/download-center?jmp=nav#community

或者这里直接 wget 包下载路径(这里脱离了主题离线)

tar 解压。进入bin目录,monogd是服务端，mongo是客户端要：`./mongo`运行。

注意运行前要有/data/db路径，这里是默认存放数据的文件夹，如果自己要指定：

```
mongod --dbpath <path to data directory>
```



#### 后台运行

后台运行需要指定日志文件,并携带--fork参数：

```
/home/mongodb-linux-x86_64-rhel62-3.4.10/bin/mongod \
         --dbpath /data/db/ --fork --logpath /data/log/mongo.log
```





### 启动

mongod 服务器，监听27017端口。

还启动个简单的HTTP服务器，端口28017， 访问`http://localhost:28017` 能获取数据库的管理信息。



#### shell 执行脚本

将js文件传给shell, 

```
$ mongo js1.js js2.js js3.js
MongoDb shell version: 2.4.0
connecting to :test
1.js
2.js
3.js
$
```

会执行依次传入的脚本，然后退出。

还可以使用指定主机正运行的脚本。



#### .mongorc.js文件

会在启动shell自动执行，如果没有可以创建，如在启动shell时有句欢迎语：

```js
print("hello, you're looking intelligent~")
```

或为了实用， 可以创建全局变量。 

或移除危险的辅助函数，只能预防自己手误：

```
//禁止删除数据库
db.dropDatabase = DB.prototype.dropDatabase = no;
```



