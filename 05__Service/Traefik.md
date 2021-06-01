

## Traefik

https://github.com/traefik/traefik/

https://doc.traefik.io/traefik/

https://docs.traefik.cn/，中文文档，更新进度较慢

概念：

`traefik` 与 `nginx` 一样，是一款优秀的反向代理工具，或者叫 `Edge Router`。至于使用它的原因则基于以下几点

- 无须重启即可更新配置
- 自动的服务发现与负载均衡
- **与 `docker` 的完美集成，基于 `container label` 的配置**
- 漂亮的 `dashboard` 界面
- `metrics` 的支持，对 `prometheus` 和 `k8s` 的集成



### start

一个基本的使用配置：

``` yaml
version: '3'
services:
  reverse-proxy:
    image: traefik:v2.2
    # Enables the web UI and tells Traefik to listen to docker
    # 启用webUI 并告诉Traefile去监听docker的容器实例
    command: --api.insecure=true --providers.docker
    ports:
      # traefik暴露的http端口
      - "80:80"
      # webUI暴露的端口(必须制定--api.insecure=true才可以访问)
      - "8080:8080"
    volumes:
      # 指定docker的sock文件来让traefik获取docker的事件，从而实现动态负载均衡
      - /var/run/docker.sock:/var/run/docker.sock

```

docker-compose启动，访问8080端口，可以看到页面

![](https://img2020.cnblogs.com/i-beta/1341090/202003/1341090-20200309143801837-1005863445.png)



### whoami镜像

whoami镜像用于提供一个80端口的服务，访问该端口

``` sh
# docker run --rm -it -p 80:80 containous/whoami
Starting up on port 80
```

另一终端：

``` sh
$ curl localhost:80
Hostname: 745c4ee201cb
IP: 127.0.0.1
IP: 172.17.0.3
RemoteAddr: 172.17.0.1:51304
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.64.0
Accept: */*

$ curl localhost:80/test
Hostname: 1d95fd769bba
IP: 127.0.0.1
IP: 182.18.0.2
RemoteAddr: 182.18.0.1:47940
GET /test HTTP/1.1
Host: localhost
User-Agent: curl/7.64.0
Accept: */*
```

可以看到访问其 80 端口时，会返回客户端的相关信息，包括请求路径和请求头等，也会展示自己的ip信息。



### entrypoint

是访问traefik的网络接入端口，支持http和TCP。

![](https://doc.traefik.io/traefik/assets/img/entrypoints.png)





#### PathPrefix

可以指定路由：

``` yaml
version: '3'
services:
  reverse-proxy:
    image: traefik:v2.2
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.test.address=:7878"
    ports:
      - "80:80"
      - "8080:8080"
      - "7878:7878"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  whoami:
    image: containous/whoami
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.entrypoints=test"
      - "traefik.http.routers.app.rule=PathPrefix(`/sss`)"
```

测试：

``` sh
root@node201:~/clair/traefik# curl localhost:7878
404 page not found
root@node201:~/clair/traefik# curl localhost:7878/sss
Hostname: 25603561057a
IP: 127.0.0.1
IP: 172.19.0.2
RemoteAddr: 172.19.0.3:43010
GET /sss HTTP/1.1
Host: localhost:7878
User-Agent: curl/7.64.0
Accept: */*
Accept-Encoding: gzip
X-Forwarded-For: 172.19.0.1
X-Forwarded-Host: localhost:7878
X-Forwarded-Port: 7878
X-Forwarded-Proto: http
X-Forwarded-Server: 2664d1e02b35
X-Real-Ip: 172.19.0.1
```



https://my.oschina.net/u/4388335/blog/3322063

https://www.developerhome.net/archives/423

https://www.cnblogs.com/xiao987334176/p/12447783.html