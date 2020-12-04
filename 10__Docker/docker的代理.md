---
title: "docker的代理.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: ["Docker"]
author: "Claymore"

---
### 配置镜像源

/etc/docker/daemon.json(在centos7 中可能没有该文件，需要自己手动创建)

```json
{
    "registry-mirrors": ["https://o9wm45c3.mirror.aliyuncs.com"],
}
```

重启docker



### docker 使用代理

docker 拉取镜像的时候出现网络问题：

```
root@wy:/home/wangyu# docker pull hello-world
Using default tag: latest
Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
```

在公司有代理情况下需要配置代理，或者本地有代理端口开放：

```sh
root@wy:/etc/systemd/system# mkdir docker.service.d
root@wy:/etc/systemd/system# cd docker.service.d/
root@wy:/etc/systemd/system/docker.service.d# vim http-proxy.conf

加入配置：
[Service]
Environment=http_proxy=http://IP:PORT/
Environment=no_proxy=localhost,127.0.0.0/8,172.16.0.0/12,192.168.0.0/16
Environment=https_proxy=http://IP:PORT/

root@wy:/etc/systemd/system/docker.service.d# systemctl daemon-reload
root@wy:/etc/systemd/system/docker.service.d# systemctl  restart docker
root@wy:/etc/systemd/system/docker.service.d# docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:4fe721ccc2e8dc7362278a29dc660d833570ec2682f4e4194f4ee23e415e1064
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
root@wy:/etc/systemd/system/docker.service.d# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        11 months ago       1.84kB

# 重启后使用如下命令看配置的环境变量
# systemctl show --property=Environment docker
Environment=http_proxy=http://10.61.72.66:8080/ https_proxy=http://10.61.72.66:8080/ no_proxy=localhost,127.0.0.0/8,172.16.0.0/12,192.168.0.0/16,19.244.0.0/16,172.19.0.0/16


```



#### docker build 使用代理

``` sh
docker build -t"xxx" . --build-arg HTTP_PROXY=http://10.61.72.70:2080 --build-arg HTTPS_PROXY=http://10.61.72.70:2080
```





### docker 容器内部使用代理

有两种方式：

#### 配置文件

```sh
[root ~]# mkdir .docker
[root ~]# vim  ~/.docker/config.json
cat: vim: No such file or directory
{
"proxies":
{
   "default":
   {
     "httpProxy": "http://127.0.0.1:8118",
     "httpsProxy": "http://127.0.0.1:8118",
     "noProxy": "localhost"
   }
}
}
```

重启 docker 服务。

**然后起容器的时候使用 --net host 模式**，让它可以跟宿主机共用一个 Network Namespace。

```sh
[root@x ~]# docker run -it --net host  --name golang-1.10-1  kbz/golang-1.10
root@x:/app# curl cip.cc
IP    : 119.xx.xx.79
地址    : 中国  香港  tencent.com

数据二    : 新加坡 | 腾讯云

数据三    : 中国香港香港 | 腾讯

URL    : http://www.cip.cc/119.xx.xx.79
```



#### 命名行

``` sh
docker run   -d   \
--name=enforcerd   \ 
--privileged=true   \
--net=host     --pid=host     \
-e HTTPS_PROXY=socks5://192.168.0.106:1080  imageName
```

此时注意把代理的地址调成 0.0.0.0:1080， 不然容器内部访问不到127.

在内部设置变量：

```sh
/ # export http_proxy=http://192.168.59.241:8888/
/ # export https_proxy=http://192.168.59.241:8888/
/ # printenv
HOSTNAME=de8b50a18d94
SHLVL=1
HOME=/root
PKG_RELEASE=1
https_proxy=http://192.168.59.241:8888/
http_proxy=http://192.168.59.241:8888/
TERM=xterm
NGINX_VERSION=1.17.10
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NJS_VERSION=0.3.9
PWD=/
/ # wget www.baidu.com
Connecting to 192.168.59.241:8888 (192.168.59.241:8888)
saving to 'index.html'

```





### k8s 使用代理

k8s 使用的是容器的代理，可以进入pod里printenv, 看下是否用proxy变量

https://stackoverflow.com/questions/53173487/how-to-set-proxy-settings-http-proxy-variables-for-kubernetes-v1-11-2-cluste

或者在yaml里使用代理变量：

https://stackoverflow.com/questions/52191439/kubernetes-docker-containers-behind-proxy