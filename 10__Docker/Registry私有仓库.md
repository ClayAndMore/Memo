

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
$ docker run --entrypoint htpasswd registry:2 -Bbn foo foo123  > auth/htpasswd
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
   registry:2
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



