## Redis

Red is 是一个基于内存的高效的非关系型数据库, C语言实现。
### 相关链接
官方 https: //redis. io
官方文档 https ://redis.io/documentation
中文官网 https://www.redis.cn
GitHub: https://github.com/antirez/redis
中文教程 http ://www.runoob.com/redis/dis-tutorial.html



### 安装

CentOS Red Hat
```
首先添加 EPEL 仓库，然后更新 yum 源：
sudo yum install epel release
sudo yum update

然后安装 数据库：
sudo yum -y install redis

安装好后启动服务即可
sudo systemctl start redis

可以使用 redis-cli 进入 命令行模式操作:
$ redis-cli
121.0.0.1:6379> set ’ name ’ ’Germey'
OK
121.0.0.1:6379> get ’ name'
”Germey”
```

配置远程连接

为了可以使 Redis能被远程连接，需要修改配置文件，路径为/etc/redis.conf：

```
首先，注释这一行
bind 127.0 . 0.1
另外，推荐给redis设置密码，取消注释这一行：
requirepass foobared
foobared 即当前密码，可以自行修改
```

然后重启 服务，使用的命令如下：
systemctl restart redis 



编译安装：

https://redis.io/download

