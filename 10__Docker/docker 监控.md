

### docker.sock

**/var/run/docker.sock**它是**Docker守护进程(Docker daemon)**默认监听的**Unix域套接字(Unix domain socket)**，容器中的进程可以通过它与Docker守护进程进行通信。

所以一些监控类的容器需要挂载该项，获得一些容器的信息。

你也可以创建其他的 监听端口：https://docs.docker.com/engine/reference/commandline/dockerd/#bind-docker-to-another-host-port-or-a-unix-socket



## docker Engine API

我们可以发送一些api请求到docker.sock

具体的使用可以看：

https://docs.docker.com/engine/api/v1.24/#1-brief-introduction



### 获取镜像和容器

``` sh
curl -XGET --unix-socket /var/run/docker.sock http://localhost/images/json

curl -XGET --unix-socket /var/run/docker.sock http://localhost/containers/json
```





### 创建容器

``` sh
# curl命令通过Unix套接字发送{“Image”:”nginx”}到Docker守护进程的/containers/create接口
curl -XPOST --unix-socket /var/run/docker.sock -d ‘{“Image”:”nginx”}’ -H ‘Content-Type: application/json’ http://localhost/containers/create
# response
{“Id”:”fcb65c6147efb862d5ea3a2ef20e793c52f0fafa3eb04e4292cb4784c5777d65",”Warnings”:null}
```



### 启动容器

使用返回的容器ID，调用**/containers//start**接口，即可启动新创建的容器。

```
curl -XPOST --unix-socket /var/run/docker.sock http://localhost/containers/fcb6...7d65/start
```



### 监听事件流

在alpine容器内，可以通过Docker套接字发送HTTP请求到**/events**接口。这个命令会一直等待Docker daemon的事件。当新的事件发生时(例如创建了新的容器)，会看到输出信息。

```
curl --unix-socket /var/run/docker.sock http://localhost/events
```



## GO SDK

GO和python的都有封装的sdk去调用 docker api:

https://docs.docker.com/engine/api/sdk/examples/