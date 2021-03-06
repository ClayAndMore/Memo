---
title: "Grafana.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["监控服务"]
author: "Claymore"

---


Grafana是一个纯html/js的web应用，是一个开源仪表盘工具，访问InfluxDB时不会存在跨域访问的限制，只要配置好数据源后，即可展示监控数据。

特点：

1. 丰富的数据源接口，支持InfluxDB、MySQL、ElasticSearch、PostgreSQL等多数据源

2. 丰富的API接口，方便自动化程序调用

3. 监控dashboard导入导出，制作好模板后导入后修改参数即可实现实时监控

4. 支持复杂的告警规则及邮件告警

### 安装

Docker 版：

先搜一下：
`docker search grafana/grafana`

当然是用start数最多的官方的了。

`docker run -d --name grafana  -p 8000:3000 grafana/grafana grafana`

 暴露容器3000端口到宿主机8000, 页面访问8000端口就可以看到grafana的页面了。

### 配置

第一次进会让登录用户名和密码：

```
docker exec -it grafana bash
进入容器，
找到  /etc/grafana/grafana.ini ， 里面的default admin user, admin password
一般初始用户密码都是amdin, 会让你在进入第一次时改掉。
```

如果再次启动会取消掉我们配置的密码， 解决办法：

用环境变量：

```
docker run \ 
       -d --name grafana  -p 8080:3000 \ 
       -e "GF_SERVER_ROOT_URL=http://grafana.server.name" \
       -e "GF_SECURITY_ADMIN_PASSWORD=newpwd" \
       grafana/grafana grafana

说明：
设置服务的默认域名 ：-e "GF_SERVER_ROOT_URL=http://grafana.server.name"

设置admin的密码为newpwd ： -e "GF_SECURITY_ADMIN_PASSWORD=newpwd"
```

### 挂载数据文件，设置Grafana数据持久化

```
docker run \
       -d --name grafana  -p 3000:3000 \
       -e "GF_SERVER_ROOT_URL=http://grafana.server.name" \
       -e "GF_SECURITY_ADMIN_PASSWORD=newpwd" \
       --volume "/root/data:/var/lib/grafana" \
       grafana/grafana grafana
```

挂载本地目录/root/data

 本地挂载目录记得加权限：`chmod a+rwx`

或使用Z标志(1.7 up) : `run -v ./api:/usr/src/app:Z`,  它可对*SELinux*等有效。

### Dashboard

模板 [https://grafana.com/dashboards](https://grafana.com/dashboards)

支持导入
