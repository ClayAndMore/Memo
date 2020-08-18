---
title: "nginx.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["linux软件"]
categories: ["linux"]
author: "Claymore"

---


## nginx

### 常用操作

* ngxin  -v  查看版本
* nginx    启动ngxin
* `nginx -s reload`    修改配置后重启加载生效， 这种方法重启，nginx在重启的时候不会中断服务，因为  nginx在启动后，会有一个master进程和多个worker进程，重启是会先生成新的worker进程去接受reload命令，等老的worker进程执行完毕，master进程在关闭他们，所以服务器不会中断。
* `nginx -s stop`   快速停止nginx 
* `ningx -s quit`   完整有序的停止nginx
* `ningx -t `   测试当前配置文件是正确

### 配置文件



井号注释

指令是以一个变量名开头(例如，worker_processes或pid),然后包含参数

所有指令以 ; 结尾

子指令以花括号包含



#### nginx.conf

在`/etc/nginx/nginx.conf 是nginx的默认配置文件：

```nginx
#运行nginx的用户
user  nginx;
#启动进程设置成和CPU数量相等
worker_processes  1;

#全局错误日志及PID文件的位置
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

#工作模式及连接数上限
events {
        #单个后台work进程最大并发数设置为1024
    worker_connections  1024;
}

http {
    #设定mime类型
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

        #设定日志格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #设置连接超时的事件
    keepalive_timeout  65;

    #开启GZIP压缩
    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```



- daemon off|on  是否以守护进程的方式启动nginx，定位问题时设为off，正常环境为on

- worker_processes Nginx开启的进程数 

  - `worker_processes  1;`
  - `#worker_processes auto;`
  - 以下参数指定了哪个cpu分配给哪个进程，一般来说不用特殊指定。如果一定要设的话，用0和1指定分配方式。这样设就是给1-4个进程分配单独的核来运行，出现第5个进程是就是随机分配了.eg:
  - `#worker_processes 4     #4核CPU `
  - `#worker_cpu_affinity 0001 0010 0100 1000`

- worker_cpu_affinity  nginx 默认没有开启利用多核cpu配置的。需要此参数来充分利用多核cpu.

  ```nginx
  # 两核cpu，开启两个进程，
  # 01 10;表示开启两个进程，第一个进程对应着第一个CPU内核，第二个进程对应着第二个CPU内核。
  worker_processes     2;
  worker_cpu_affinity 01 10;
  
  worker_processes     4;
  worker_cpu_affinity 0001 0010 0100 1000;
  
  # 4核CPU, 开启两个进程
  # 0101表示开启第一个和第三个内核，1010表示开启第二个和第四个内核
  worker_processes     2;
  worker_cpu_affinity 0101 1010;
  ```

- worker_rlimit_nofile

- pid



最后一行包含了其他的配置文件，这个目录下是我们自定义的配置文件，默认包含default.conf


#### default.conf

```nginx
server {
    listen    80;       #侦听80端口，如果强制所有的访问都必须是HTTPs的，这行需要注销掉
    server_name  www.xxx.com;             #域名

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

        # 定义首页索引目录和名称
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #定义错误提示页面
    #error_page  404              /404.html;

    #重定向错误页面到 /50x.html
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```



### 实例

#### 静态HTTP服务器

首先，Nginx是一个HTTP服务器，可以将服务器上的静态文件（如HTML、图片）通过HTTP协议展现给客户端。

配置：

```nginx
server {
	listen 80; # 端口号
	location / {
		root /usr/share/nginx/html; # 静态文件路径
	}
}
```



#### 反向代理服务器

客户端本来可以直接通过HTTP协议访问某网站应用服务器，如果网站管理员在中间加上一个Nginx，客户端请求Nginx，Nginx请求应用服务器，然后将结果返回给客户端，此时Nginx就是反向代理服务器。

```nginx
server {
	listen 80;
	location / {
		proxy_pass http://192.168.20.1:8080; # 应用服务器HTTP地址
	}
}
```



#### 负载均衡

当网站访问量非常大, 因为网站越来越慢，一台服务器已经不够用了。于是将相同的应用部署在多台服务器上，将大量用户的请求分配给多台机器处理。

同时带来的好处是，其中一台服务器万一挂了，只要还有其他服务器正常运行，就不会影响用户使用。

Nginx可以通过反向代理来实现负载均衡。

```nginx
upstream myapp {
	server 192.168.20.1:8080; # 应用服务器1
	server 192.168.20.2:8080; # 应用服务器2
}
server {
	listen 80;
	location / {
		proxy_pass http://myapp;
	}
}
```



#### 虚拟主机

的网站访问量大，需要负载均衡。然而并不是所有网站都如此出色，有的网站，由于访问量太小，需要节省成本，将多个网站部署在同一台服务器上。

例如将 `www.aaa.com` 和 `www.bbb.com` 两个网站部署在同一台服务器上，两个域名解析到同一个IP地址，但是用户通过两个域名却可以打开两个完全不同的网站，互相不影响，就像访问两个服务器一样，所以叫两个虚拟主机。

配置：

```nginx
server {
	listen 80 default_server;
	server_name _;
	return 444; # 过滤其他域名的请求，返回444状态码
}
server {
	listen 80;
	server_name www.aaa.com; # www.aaa.com域名
	location / {
		proxy_pass http://localhost:8080; # 对应端口号8080
	}
}
server {
	listen 80;
	server_name www.bbb.com; # www.bbb.com域名
	location / {
		proxy_pass http://localhost:8081; # 对应端口号8081
	}
}
```

在服务器8080和8081分别开了一个应用，客户端通过不同的域名访问，根据server_name可以反向代理到对应的应用服务器。

虚拟主机的原理是通过HTTP请求头中的Host是否匹配server_name来实现的，有兴趣的同学可以研究一下HTTP协议。

另外，server_name配置还可以过滤有人恶意将某些域名指向你的主机服务器。



#### FastCGI

待补充。



### 其他

#### 跨域

```
location / {
     add_header Access-Control-Allow-Origin https://192.168.18.58;
}
```

允许192.168.18.58 向本机访问。

#### 打印

在nginx中要想打印某个值，完全可以实现直接打印的效果，用不着借助第三方扩展，直接返回结果就好：

```nginx
server    {
    listen 80;
    server_name tmp.kaibuy.cn;
    index index.php;
    root  /home/web/blog/public/www;
    #error_page   404   /404.html;
    location / {
        default_type  text/plain;   
        set $str "This Host : ";
        return 200 "$str $http_host";
    }

    access_log off;
}
```

是指定以文本方式打印，如果不加这句，搞不好会以下载文件的方式出现。当然也可以指定为HTML。

`set $str "This Host : ";`设定一个变量

如果变量内容是单词，

也可以：`set $str MyValue;`，这种不带引号时，中间不能有空格即可。 

`return 200 "$str $http_host";`返回内容体，前面200是状态码，可以是任意符合HTML状态码的代码，这任意。
后面引号里的是两个变量，`$str`是刚才定义的变量，`$http_host`是nginx系统变量。

这儿也可以写成`return 200 $str$http_host;`

也就是不带引号，但变量之间要是连续的，不能有空格。

#### 获取cookie
