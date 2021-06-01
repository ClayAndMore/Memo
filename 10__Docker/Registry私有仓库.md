---
title: "Registry私有仓库.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: ["Docker"]
author: "Claymore"

---


## Docker Registry

https://docs.docker.com/registry/

api: https://docs.docker.com/registry/spec/api/

Registry 私用仓库 是一个无状态，高度可扩展的服务器端应用程序，它存储并允许您分发Docker映像。



### 简单使用

拉取 registry:2， 并启动一个容器：

```sh
docker run -d -p 5000:5000 --name registry registry:2

# 可先拉取
docker pull regstry:2
# 挂载出来方便管理：
-v /root/images/registry:/var/lib/registry
```

向私用库添加容器：

``` sh
# 用tag 使镜像指向私有库：
docker tag nginx:alpine localhost:5000/nginx:alpine
# push 
$ docker push localhost:5000/nginx:alpine
The push refers to repository [localhost:5000/nginx]
6f23cf4d16de: Pushed
531743b7098c: Pushed

alpine: digest: sha256:ef2b6cd6fdfc6d0502b77710b27f7928a5e29ab5cfae398824e5dcfbbb7a75e2 size: 739
```

注意这里使用 本机ip 会有问题：

``` sh 
# docker push 172.19.19.16:5000/nginx:alpine
The push refers to repository [172.19.19.16:5000/nginx]
Get https://172.19.19.16:5000/v2/: http: server gave HTTP response to HTTPS client
```

拉取：

```
docker pull localhost:5000/nginx:alpine
```



### 认证

不同服务器拉取时：

``` sh
docker pull 172.19.19.16:5000/nginx:alpine
Error response from daemon: Get https://172.19.19.16:5000/v2/: http: server gave HTTP response to HTTPS client
```

由于客户端采用https，docker registry未采用https服务所致。一种处理方式是把客户端请求地址请求改为http:

vim /etc/docker/daemon.json

``` sh
{ "insecure-registries":["172.19.19.16:5000"] }
```

重启docker:

``` sh
root@node200:~# systemctl daemon-reload
root@node200:~# systemctl restart docker

root@node200:~# docker pull 172.19.19.16:5000/nginx:alpine
alpine: Pulling from nginx
Digest: sha256:ef2b6cd6fdfc6d0502b77710b27f7928a5e29ab5cfae398824e5dcfbbb7a75e2
Status: Downloaded newer image for 172.19.19.16:5000/nginx:alpine
172.19.19.16:5000/nginx:alpine
```

成功拉取。

当然也可以成功上传：

```
docker tag <imagesname> <ip:port/image>
docker push ip:port/image
```



### 配置https 服务

先生成自认证证书：

``` sh
sudo mkdir -p certs && sudo openssl req \
-newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key \
-x509 -days 365 -out certs/domain.crt
```

这里可以都不填写，或者可以填写一个域名：mydockerhub.com

启用带有认证的registry:

``` sh
docker run -d -p 5000:5000 --name registry \
-v `pwd`certs:/certs \
-v /~/registry:/var/lib/registry \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
-e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
registry:2
```

证书文件`certs/domain.crt`复制到**docker客户端**的宿主机:

`scp certs/domain.crt /etc/docker/certs.d/mydockerhub.com:5000/ca.crt`

当然 没有的目录要创建, 要重启客户端的docker

docker客户端使用域名访问registry

```undefined
docker pull mydockerhub.com:5000/centos
```

如果域名mydockerhub.com尚未指向registry宿主机的ip地址，可以修改hosts文件，将ip与域名做关联。ip还配置局域网地址，这样能加快上传下载速度。

```undefined
vi /etc/hosts
ip  mydockerhub.com
```



### 鉴权

为Registry加上基础鉴权，账户和密码。

账户名 foo, 密码 foo123 生成密码文件：

``` sh
$ mkdir auth
$ docker run --entrypoint htpasswd registry:2.7.0 -Bbn foo foo123  > auth/htpasswd
$ ls auth
htpasswd
```

启动带鉴权功能的Registry:

``` sh
$ docker run -d -p 5000:5000 --restart=always --name registry \
   -v `pwd`/auth:/auth \
   -e "REGISTRY_AUTH=htpasswd" \
   -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
   -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
   -v `pwd`/data:/var/lib/registry \
   -v `pwd`/certs:/certs \
   -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
   -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
   registry:2.7.0
```

登录：

`$docker login mydockerhub.com:5000`

即可完成对其镜像的拉取和推送




## Harbor

Harbor是vmware公司开源的用于企业级docker registry服务。它提供了web-ui界面，角色管理，LDAP支持，restful API等功能，项目地址：[https://github.com/vmware/harbor](https://link.jianshu.com?t=https://github.com/vmware/harbor)。
 我们可以搭建Harbor来代替docker registry。安装的过程参考：

https://github.com/vmware/harbor/blob/master/docs/installation_guide.md

API: https://editor.swagger.io/?url=https://raw.githubusercontent.com/goharbor/harbor/master/api/v2.0/swagger.yaml



## Rancher

文档：https://rancher2.docs.rancher.cn/



### 使用kubectl

使用 rancher 安装的k8s 是没有kubectl 和 ~/.kube 文件夹的

安装kubectl : https://kubernetes.io/docs/tasks/tools/install-kubectl/

创建 ~/.kube 文件夹 和 创建 ~/.kube/config 文件，在rancher的页面可以找到config文件的内容。



## docker v2 api

https://docs.docker.com/registry/spec/api/

我们可以请求 docker 搭建的仓库暴露的 api 获取一些信息， 比如我们搭建的私有仓库， 网络上的共有仓库。

下面是几个比较常用的api:

``` sh
#  获取某仓库的repoes
https://{registryAddr}/v2/_catalog 
$ eg: https://10.8.2.202:5002/v2/_catalog
$ response: {"repositories":["nginx-alpine","ubuntu"]}

# 获取该仓库某个repo的所有tag
https://{registryAddr}/v2/{repo}/tags/list
$ eg:  https://10.8.2.202:5002/v2/ubuntu/tags/list
$ response: {"name":"ubuntu","tags":["16.04"]}
```



### 获取 Manifest

Docker镜像包含两部分内容：一组有序的层(Layer)和相应的创建容器时要用的参数构成。

我们可以分别通过`docker history`和`docker inspect`这两个命令查看层和镜像参数。

Manifest里包含了前面所说的配置文件和层列表。

``` sh
# 获取某个tag的manifest
https://{registryAddr}/v2/{repo}/manifests/{tag}
$ eg: https://10.8.2.202:5002/v2/ubuntu/manifests/16.04
	DockerV2Header    = "application/vnd.docker.distribution.manifest.v2+json,application/vnd.docker.distribution.manifest.list.v2+json"
```

response， 可以观察我们可以获取的信息：

``` json
{
   "schemaVersion": 1,
   "name": "ubuntu",
   "tag": "16.04",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
...
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":..."..."throwaway\":true}"
      },
...
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "4QD3:K6YH:K3XH:KGR4:QATP:YNQE:G7YB:VXSS:RPGV:MS6Q:6QVX:M2IS",
               "kty": "EC",
               "x": "wWFio5li2qEzH-pseX54NJpA9H7HsFErf137H4QnKyY",
               "y": "czMQve4SlWaBXH6n4rYdakyz01SFttPGjjlzogfEJQE"
            },
            "alg": "ES256"
         },
         "signature": "lmlCUAsLS648-BYeU858nkO2gwnIdNtWgQe1OyhwfyUXCXH3KCsyeSG9TdN6nQcS3c12JiUt6pVQL_30PE7DGw",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjU0MDQsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMC0xMS0wOVQwMjo0MDozN1oifQ"
      }
   ]
}
```



### 请求头和响应头中包含的信息

上方api请求中的响应头：

``` sh
Content-Type: application/vnd.docker.distribution.manifest.v1+prettyjws
docker-content-digest: sha256:458989417308c99f6cc6653cb21aede4061330be28967e4175b8d4452adc5ee5
```

这个digest和ubuntu的imageID 和 docker digest 都对不上， 其实这个digest应该是配置文件的sh256,没有什么用。

因为访问接口默认使用v1版本，我们指定v2版本获取下v2 的manifest json:

``` json
curl -k --location --request GET 'https://10.8.2.202:5002/v2/ubuntu/manifests/16.04' --header 'Accept: application/vnd.docker.distribution.manifest.v2+json' --user admin:123456

{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 3621,
      "digest": "sha256:6a2f32de169d14e6f8a84538eaa28f2629872d7d4f580a303b296c60db36fbd7"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 46773527,
         "digest": "sha256:4edc955e886b88915c967acece569a62369ac2a2832c956d14d314600eed6933"
      },
...
   ]
}r
```

这里的的config, digest 的值居然和我们的image id一样，所以不要混淆。 注意，v2 版本的请求头中添加Accept的值.

v2的响应头：

```
Content-Type: application/vnd.docker.distribution.manifest.v2+json
Docker-Content-Digest: sha256:e38518751a839d370a116df0b702b7fd6fa33b44e7bb7dc7d6c05f978ec8f6b2
```



### docker image 和 docker digest

``` sh
# docker ps
10.8.2.202:5002/ubuntu           16.04               6a2f32de169d        3 years ago         117MB
# docker push 10.8.2.202:5002/ubuntu:16.04
The push refers to repository [10.8.2.202:5002/ubuntu]
ab4b9ad8d212: Pushed
....
e86a0c422723: Pushed
16.04: digest: sha256:e38518751a839d370a116df0b702b7fd6fa33b44e7bb7dc7d6c05f978ec8f6b2 size: 1357
```

上方说了我们可以拿到它的image ID， 如何拿到digest呢，其实，**digest就是manifest.json的sh256**:

``` sh
# curl -k --location --request GET 'https://10.8.2.202:5002/v2/ubuntu/manifests/16.04' --header 'Accept: application/vnd.docker.distribution.manifest.v2+json' --user admin:123456 >> manifest.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1357  100  1357    0     0  46793      0 --:--:-- --:--:-- --:--:-- 46793
y# sha256sum manifest.json
e38518751a839d370a116df0b702b7fd6fa33b44e7bb7dc7d6c05f978ec8f6b2  manifest.json
```





## 问题

### x509: certificate signed by unknown authority

需要配置忽略证书：

```  sh
# vim /etc/docker/daemon.json
{ 
  "insecure-registries": ["registry.svc.xxx.cn"]
}
```



### x509: certificate has expired or is not yet valid

证书过期，使用时间同步，或者更改时间，有可能是你的机器比registry的机器时间落后。





### net/http: HTTP/1.x transport connection broken: malformed HTTP response

``` sh
# docker  pull 172.19.19.16:5000/nginx:alpine
Error response from daemon: Get http://172.19.19.16:5000/v2/: net/http: HTTP/1.x transport connection broken: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

需要登录后再拉取



远程仓库的拉取： https://blog.csdn.net/alinyua/article/details/81086124



## 配置不需要忽略证书的私有仓库

### 生成证书

有两种方式来生成：

``` sh
# 编辑：
/etc/ssl/openssl.cnf 
# 在[v3_ca] section 添加： 
subjectAltName = IP:192.168.1.102

# 然后重生成证书
openssl req \
-newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key \
-x509 -days 365 -out certs/domain.crt
```

或者：

``` sh
cd certs
echo subjectAltName = IP:192.168.1.102 > extfile.cnf
openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key \
-x509 -days 365 -out domain.crt -extfile extfile.cnf
```

生成证书的时候要填写仓库地址：

``` sh
Common Name (e.g. server FQDN or YOUR name) []:192.168.1.102:5000
```



### 将证书发送给节点

在非registry所在主机创建证书目录：

``` sh
mkdir -p /etc/docker/certs.d/192.168.1.102:5000
chmod -R 700 /etc/docker/certs.d/192.168.1.102:5000
```

拷贝：

``` sh
cp domain.crt /etc/docker/certs.d/192.168.1.102:5000/ca.crt
```

