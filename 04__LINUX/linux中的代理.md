---
title: "linux的代理.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---
## proxy 

``` sh
export http_proxy=http://192.168.1.1:8082
export https_proxy=http://192.168.1.1:8082
export no_proxy='localhost,a.test.com,127.0.0.1,2.2.2.2' # 不需要代理的目的地址
```

在 ～/.bashrc 中可以配置 全局的代理变量，他会影响 curl , wget 等软件。



## proxychains

<http://pawelli.com/archives/527>

<https://www.jianshu.com/p/3f392367b41f>

<https://www.hi-linux.com/posts/48321.html#proxychains-ng-%E8%AF%AD%E6%B3%95>

https://guangchuangyu.github.io/cn/2018/09/proxychains/>



## v2ray

下载：

`wget https://install.direct/go.sh`

安装：

` bash go.sh`

```sh
root@wy-server:~/v2ray# bash go.sh
Installing V2Ray v4.22.1 on x86_64
Downloading V2Ray: https://github.com/v2ray/v2ray-core/releases/download/v4.22.1/v2ray-linux-64.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   608  100   608    0     0   1109      0 --:--:-- --:--:-- --:--:--  1107
100 11.6M  100 11.6M    0     0  53206      0  0:03:48  0:03:48 --:--:-- 27378
go.sh: line 144: unzip: command not found
Updating software repo
Installing unzip
Selecting previously unselected package unzip.
(Reading database ... 108587 files and directories currently installed.)
Preparing to unpack .../unzip_6.0-22ubuntu1_amd64.deb ...
Unpacking unzip (6.0-22ubuntu1) ...
Setting up unzip (6.0-22ubuntu1) ...
Processing triggers for mime-support (3.60ubuntu1) ...
Processing triggers for man-db (2.8.5-2) ...
Archive:  /tmp/v2ray/v2ray.zip
  inflating: /usr/bin/v2ray/geoip.dat
  inflating: /usr/bin/v2ray/geosite.dat
  inflating: /usr/bin/v2ray/v2ctl
  inflating: /usr/bin/v2ray/v2ray
PORT:31986
UUID:67d872f2-42db-458b-a6cd-5633d188cee9
Archive:  /tmp/v2ray/v2ray.zip
  inflating: /etc/systemd/system/v2ray.service
Created symlink /etc/systemd/system/multi-user.target.wants/v2ray.service → /etc/systemd/system/v2ray.service.
V2Ray v4.22.1 is installed.
```

此时 /etc/v2ray/config.json 是它的配置文件



### 服务端





### 客户端

配置 config.json 文件，重启v2ray:

```sh
root@:/etc/v2ray# systemctl restart v2ray
root@:/etc/v2ray# vim config.json
root@:/etc/v2ray# lsof -i:1087
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
v2ray   22958 root    5u  IPv4 2348497      0t0  TCP localhost:1087 (LISTEN)
root@:/etc/v2ray# lsof -i:1088
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
v2ray   22958 root    3u  IPv6 2348496      0t0  TCP *:1088 (LISTEN)
```

可以看到 我们本地的代理端口起来了。



## 代理

你的机器 - 代理服务器 - 目标网站



你的个人电脑需要访问某个网站时，将这个请求转发到代理服务器，由代理服务器来帮你访问，访问成功后再将结果再传回给你的个人电脑



### HTTP代理

这种代理是最简单的代理，可以在虚拟主机上使用 Nginx 直接搭建。

```
server {
    resolver 8.8.8.8;
        listen 80;
        location / {
                proxy_pass http://$http_host;
                proxy_set_header Host $http_host;
        }
}
```

原理是「请求改写」，将 HTTP 请求的目标地址换成代理服务器的地址，代理服务器再将请求进行改写传递到目标服务器。

那代理服务器如何知道目标服务器地址呢，通过请求头里面的 HOST 参数，浏览器会自动加上这个请求头，携带的是目标服务器的地址。

上面的 nginx 配置文件中的 $http_host 变量就是目标服务器地址，它是从请求头的 HOST 参数中取出来的。

```
	 --- request --->           --- new request --->
主机					 代理服务器						 目标网站
     <--- response ---          <--- response --- 
```



HTTP 代理的缺点是不支持 https 协议，「请求改写」需要知道请求的内容，https 的内容是加密的无法直接改写。



### HTTPS 代理

HTTP 1.1 协议新增了一种请求类型 CONNECT。

connect是通过TCP连接代理服务器的。加入我想告诉代理服务器向访问`https://www.google.com`网站，就需要首先建立起一条从我的客户端到代理服务器的TCP连接，然后给代理服务器发送一个HTTP报文：

```
CONNECT https://www.jianshu.com/u/f67233ce6c0c:80 HTTP/1.1
Host: www.web-tinker.com:80
Proxy-Connection: Keep-Alive
Proxy-Authorization: Basic *
Content-Length: 0
```

其中`Proxy-Authorization`中，为验证用户名和密码部分。

在发送完这个请求之后，代理服务器会响应请求，返回一个200的信息，但这个200并不同于我们平时见到的OK，而是Connection Established。

```
HTTP/1.1 200 Connection Established
```

接下来代理服务器就开始透传客户端的请求数据直达目标服务器。

它不需要知道 HTTPS 请求数据包的具体内容，直接对数据包进行透传。

缺点就是多了一个 HTTP 握手请求，多了一个网络数据包来回的开销。

这这类型的的代理称之为「隧道代理」。

```
     -- HTTP Connect -> 		--- TCP Connect --> 
     <-- 200 ---                <-- 200 --- 
	 --- request --->           --- new request --->
主机					 代理服务器						 目标网站
     <--- response ---          <--- response --- 
```

CONNECT 请求是明文的, 会被监控。



### SOCKS 

它是基于 TCP Socket 的代理，在请求的开始浏览器和代理服务器交流一下握手信息，握手信息里包括用户名密码认证、目标服务器地址等，待交流成功后直接透传浏览器发过来的请求包到目标服务器，它可以同时代理 HTTP 和 HTTPS 请求。

它不同于隧道代理在于握手协议是简单的自定义二进制协议，易于实现。

Socks 代理协议存在 V4 和 V5 两个版本，V5 是目前比较流行的版本。

SocksV5 代理要比普通的 HTTP 代理网络延迟高一些，因为多了握手阶段，而且握手阶段有 2 个数据包的来回时间.



### ShadowSocks

ShadowSocks 是一款代理软件，常被称为ss, 使用的极为广泛。它采用端到端的加密算法来传输请求响应，避免了中间传输的内容以任何形式被窃听。但是代价也是有的，那就是加密后的数据包总是要比原数据包大不少，影响传输效率。

```
	 --request-->         --加密request-->                 --- new request --->
主机				ss client              代理服务器(含ss server)				目标网站
     <--response--        --加密response-->                <--- response --- 
```



使用它需要在服务器安装 ShadowSocks 服务器软件，同时你的个人电脑要安装 ShadowSocks 客户端，设置好一样的加密算法，就可以正常交流了