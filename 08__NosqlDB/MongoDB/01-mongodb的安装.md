---
title: "01-mongodb的安装.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Mongodb"]
categories: ["Nosql"]
author: "Claymore"

---
### 环境

centos 7

安装 mongodb 4.x

官网：https://www.mongodb.com/download-center/community

官网安装里是没有centos的（也是，野生版本），只有REHL.



所以我们看网上那些让下个tgz包就可以使用的不适合centos7。

适合我们的只有改yum源和下载rpm自己搞。我们这里去下载rpm；

https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/RPMS/

https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.2/x86_64/RPMS/



### 下载

去repo网站上下载相关rpm

server 服务端

mongos 客户端

shell  客户端

tools 一些工具，如导入导出



rpm 安装：

```sh

[root@10.250.123.10 mongodb]#rpm -ivh mongodb-org-server-4.2.0-1.el7.x86_64.rpm
warning: mongodb-org-server-4.2.0-1.el7.x86_64.rpm: Header V3 RSA/SHA1 Signature, key ID 058f8b6b: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mongodb-org-server-4.2.0-1.el7   ################################# [100%]
Created symlink from /etc/systemd/system/multi-user.target.wants/mongod.service to /usr/lib/systemd/system/mongod.service.
[root@10.250.123.10 mongodb]#rpm -ivh mongodb-org-mongos-4.2.0-1.el7.x86_64.rpm
warning: mongodb-org-mongos-4.2.0-1.el7.x86_64.rpm: Header V3 RSA/SHA1 Signature, key ID 058f8b6b: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mongodb-org-mongos-4.2.0-1.el7   ################################# [100%]
[root@10.250.123.10 mongodb]#rpm -ivh mongodb-org-shell-4.2.0-1.el7.x86_64.rpm
warning: mongodb-org-shell-4.2.0-1.el7.x86_64.rpm: Header V3 RSA/SHA1 Signature, key ID 058f8b6b: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mongodb-org-shell-4.2.0-1.el7    ################################# [100%]
[root@10.250.123.10 mongodb]#rpm -ivh mongodb-org-tools-4.2.0-1.el7.x86_64.rpm
warning: mongodb-org-tools-4.2.0-1.el7.x86_64.rpm: Header V3 RSA/SHA1 Signature, key ID 058f8b6b: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mongodb-org-tools-4.2.0-1.el7    ################################# [100%]
[root@10.250.123.10 mongodb]#rpm -ivh mongodb-org-4.2.0-1.el7.x86_64.rpm
warning: mongodb-org-4.2.0-1.el7.x86_64.rpm: Header V3 RSA/SHA1 Signature, key ID 058f8b6b: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mongodb-org-4.2.0-1.el7          ################################# [100%]
```



### 配置

默认生成/etc/mongod.conf 配置文件： 

```yaml
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log   # 指明了 mongoDB 的系统运行日志的路径

# Where and how to store data.
storage:
  dbPath: /var/lib/mongo  #指明了 mongoDB 运行时进程文件存放路径
  journal:
    enabled: true
#  engine:
#  wiredTiger:

# how the process runs
processManagement:
  fork: true  # fork and run in background
  pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile
  timeZoneInfo: /usr/share/zoneinfo

# network interfaces
net:
  port: 27017
  bindIp: 127.0.0.1  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting. # 意味着默认情况下只能本机连接 mongoDB。


#security:
#operationProfiling:
#replication:
#sharding:
## Enterprise-Only Options
#auditLog:

#snmp:
```

修改为自己使用的配置：

```yaml

systemLog:
  destination: file
  logAppend: true
  path: /ng8w/opt/mongodb/log/mongo.log

# Where and how to store data.
storage:
  dbPath: /ng8w/opt/mongodb/data
  journal:
    enabled: true
#  engine:
#  wiredTiger:

# how the process runs
processManagement:
  fork: true  # fork and run in background
  pidFilePath: /ng8w/opt/mongodb/mongod.pid  # location of pidfile
  timeZoneInfo: /usr/share/zoneinfo

# network interfaces
net:
  port: 27017
  bindIp: 127.0.0.1
```





### 启动

```
[root@10.250.123.10 mongodb]#mongod -f mongod.conf
about to fork child process, waiting until server is ready for connections.
forked process: 20899
child process started successfully, parent exiting
```

