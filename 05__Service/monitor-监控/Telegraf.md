
---
title: "Telegraf.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux, 监控]

### 写在前面

Telegraf是一个用Go语言编写的代理程序，可采集系统和服务的统计数据，并写入InfluxDB数据库。Telegraf具有内存占用小的特点，通过插件系统开发人员可轻松添加支持其他服务的扩展。目前，最新版Telegraf支持的插件主要有：

* Apache
* DNS query time
* Docker
* http Listener
* MySQL
* Network Response
* Tomcat
* Zookeeper

### 配置和安装

下载地址：[https://github.com/influxdata/telegraf/releases](https://github.com/influxdata/telegraf/releases)



#### 容器

推荐docker下载安装：

```bash
docker pull telegraf
# 先启动下容器
# 把telegraf相关配置拷贝到宿机
docker cp telegraf:/etc/telegraf/telegraf.conf ./telegraf
```

把配置文件中的inputs.docker 取消掉注释：

```ini
[[inputs.docker]]
endpoint = "unix:///var/run/docker.sock"
container_names = []
container_name_include = []
container_name_exclude = []
timeout = "5s"
perdevice = true
total = false
tag_env = ["JAVA_HOME", "HEAP_SIZE"]
docker_label_include = []
docker_label_exclude = []
```

outputs.infuxdb 打开 urls:

```ini
[[outputs.influxdb]]
  ## The full HTTP or UDP URL for your InfluxDB instance.
  ##
  ## Multiple URLs can be specified for a single cluster, only ONE of the
  ## urls will be written to each interval.
  # urls = ["unix:///var/run/influxdb.sock"]
  # urls = ["udp://127.0.0.1:8089"]
  urls = ["http://server_ip:8086"]  #  这里是influxdb服务的ip,最好不要写成localhost
```

Telegraf非常方便的一点就在于其配置驱动的特点。通过直接修改.conf配置文件即可实时将数据写入数据源。

修改一些监控项：

```ini
[[inputs.cpu]]
[[inputs.disk]]
...
```

启动：

```bash
docker run -d --name=telegraf -v /root/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf -v /var/run:/var/run telegraf
```

通过-v参数，把本地的telegraf.conf放到容器中覆盖默认的配置，同时把/var/run也放入容器内，因为其中有docker.sock这个文件是与docker通信的接口。



#### apt 源

在Ubuntu 18.04上安装telegraf是从Influxdata存储库完成的，添加repo后，可以使用apt包管理器安装包，将InfluxData存储库添加到文件/etc/apt/sources.list.d/influxdata.list中：

``` sh
# cat /etc/apt/sources.list.d/influxdata.list
deb https://repos.influxdata.com/ubuntu bionic stable

# 导入apt key:
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

# 开始安装
apt-get update
apt-get install telegraf

# 启动并启用服务以在启动时启动：

$ sudo systemctl start telegraf
$ sudo  systemctl enable telegraf
$ sudo systemctl is-enabled telegraf
enabled
$ systemctl status telegraf
```



#### deb 文件安装

`dpkg -i telegraf_1.14.3-1_amd64.deb`



### 配置NGINX

小提示:需要nginx开启`--with-http_stub_status_module`模块

增加nginx server 配置

```php
server {
    listen  30000;
    server_name localhost;

    location /nginx-status {
       # 允许的ip
       allow 127.0.0.1;
       deny all;
       stub_status on;
       access_log off;
    }

}
```

telegraf配置

```php
[[inputs.nginx]]
    urls = ["http://127.0.0.1:30000/nginx-status"]
    response_timeout = "5s"
```

测试是否生效

```php
systemctl restart telegraf
telegraf --config telegraf.conf --input-filter nginx --test
```





### 构建体积较小的镜像

只使用需要的插件：

https://www.influxdata.com/blog/bring-your-own-telegraf/

https://hub.docker.com/r/rawkode/telegraf