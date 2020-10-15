---
title: "docker 容器磁盘占用和清理.md"
date: 2020-08-13 17:53:13 +0800
lastmod: 2020-08-13 14:45:42 +0800
draft: false
tags: [""]
categories: ["Docker"]
author: "Claymore"

---

## 磁盘占用

一般来说，我们可以通过下面几个方式来观察磁盘占用

### docker ps -s

``` sh
# docker ps -s 
NAMES                   SIZE
ui               8.18kB (virtual 157MB)
backend          0B (virtual 165MB)
scan-api         3.41MB (virtual 802MB)
ips              30MB (virtual 1.26GB)
webshell         679B (virtual 128MB)
scan-policy      20.4MB (virtual 819MB)
scan-analyzer    13.3MB (virtual 812MB)
scan-simpleq     4.61GB (virtual 5.41GB)
scan-catalog     37.2MB (virtual 835MB)
relationship-s   0B (virtual 222MB)
relationship-c   83B (virtual 222MB)
elastic          1.36MB (virtual 573MB)
postgres         63B (virtual 225MB)
mongo            0B (virtual 462MB)
# 其他列的输出被删掉
```

### size 和 virtual size 的区别

**因为 容器挂载的是一个只读的docker镜像。而我们对于这个镜像的任何改动是作用于其上的一个写入层。**

这样设计的目的是对于产生于同一docker镜像的容器，让只读镜像可以在其中共享，而写入层是它们的区别所在。

- **Size -- 每个容器的写入层在磁盘中的大小**
- **Virtual size - 只读的镜像尺寸 + 写入层大小**

所以一般我们只关注size的尺寸，比如有一个nginx镜像17.8MB ，用它起10个容器，每个容器的size为2B, virtual size 为17.8MB +2B,  10个这样的nginx容器总占用磁盘  17.8MB + 2B*10 。

如果你往一个容器中拷贝了一个 8 M的文件，那么它的size为25.8M



**需要特别注意的是，这里的尺寸并不是容器所使用的所有磁盘空间。**当前没有包含在计算中的有：

- 日志文件所使用的磁盘空间（如果使用的是json-file日志驱动）- 如果您的容器产生了很多的日志文件，或者log-rotaion未被配置（max-file/max-size日志选项）
- 容器使用的卷
- 容器配置文件所使用的磁盘空间（hostconfig.json, config.v2.json, hosts, hostname, resolv.conf） - 尽管这些文件很小
- 内存写入磁盘（假设swapping 打开）
- Checkpoints（如果您使用了一些试验性的功能，如checkpoint/restore）



对于上方有个 scan-simpleq 的size 使用了 4.6 G的size, 我们进去看下：

``` sh
docker exec -it 4e61569fe8e2 sh

anchore@4e61569fe8e2:/$ du -h -d1 /
757M    /usr
4.0K    /media
4.0K    /boot
4.4G    /var
....
4.0K    /analysis_scratch
16K     /config
4.0K    /workspace
5.1G    /

anchore@4e61569fe8e2:/$ du -h -d1 /var/log/
64K     /var/log/apt
4.3G    /var/log/anchore
4.3G    /var/log/
anchore@4e61569fe8e2:/$ du -h -d1 /var/log/anchore/
4.3G    /var/log/anchore/
anchore@4e61569fe8e2:/$ ls /var/log/anchore/
anchore-simplequeue.log
anchore@4e61569fe8e2:/$ du -h /var/log/anchore/anchore-simplequeue.log
4.3G    /var/log/anchore/anchore-simplequeue.log

# 最后定位到这个日志文件过大，导致的size过大，删除日志文件或者定制日志清理任务。
```



### docker system df

Docker 的内置 CLI 指令docker system df，可用于查询镜像（Images）、容器（Containers）和本地卷（Local Volumes）等空间使用大户的空间占用情况。

``` sh
# docker system df
TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              30                  13                  5.34GB              2.438GB (45%)
Containers          20                  14                  347.1MB             241.3MB (69%)
Local Volumes       9                   5                   833.6MB             0B (0%)
```

最后的 `RECLAIMABLE` 是可回收大小。

可以进一步通过-v参数查看空间占用细节，以确定具体是哪个镜像、容器或本地卷占用了过高空间：

``` sh
Images space usage:

REPOSITORY  TAG                 IMAGE ID            CREATED ago         SIZE                SHARED SIZE         UNIQUE SiZE         CONTAINERS
xxxxxxx-64  debug               90b6776eb64e        7 weeks ago ago     170.5MB             107MB               63.52MB             0
...
docker-hub  latest              c8a3d229c103        3 months ago ago    157.1MB             123MB               34.07MB             1
docker-hub  latest              9163235c5315        6 months ago ago    1.23GB              107MB               1.123GB             1
docker-hub  0.4                 0733a1ac3bd4        7 months ago ago    798.3MB             107MB               691.3MB             5


Containers space usage:

CONTAINER ID        IMAGE    COMMAND   LOCAL VOLUMES       SIZE        CREATED ago         STATUS                NAMES
7a11830cb174        docke    "/entry   0                   8.18kB      2 weeks ago     Up 9 days                  ui
7e6f769f2fc7        docke    "/entry   0                   0B          2 weeks ago     Up 9 days (healthy)        backend
...
cbb24df88f53        docke    "/run.s   1                   0B          2 months ago    Exited (255) 9 days ago    etcd01
61e8e9da6b71        docke    "relati   0                   83B         2 months ago    Up 9 days (healthy)        relationship-c
bdf5480c8cbb        docke    "/opt/e   0                   1.36MB      2 months ago    Up 9 days                  elastic
9469b52e26d9        docke    "docker   1                   63B         2 months ago    Up 9 days                  postgres
ba38b92eb01f        docke    "docker   2                   0B          2 months ago    Up 9 days                  mongo

Local Volumes space usage:

VOLUME NAME                                                        LINKS               SIZE
15suo_etcd01-data                                                  1                   144.8MB
15suo_mongodb-data                                                 1                   412.7MB
15suo_postgres-db-volume                                           1                   276.1MB
15suo_topsec-dsec-logs                                             0                   0B
15suo_topsec-registry-data                                         0                   0B
15suo_anchore-scratch                                              1                   0B
15suo_psql-data                                                    0                   0B
90770dfa786b764a2ffd4e54101df749701f1b9261aa751d6907174f4a0f8068   0                   0B
fe867ac64ed74141e023c24fd07a1b78ec87d92a058a1419a559133786e34b48   1                   0B
root@sw2:/src/jiangwei/15-suo# docker volume ls -q
15suo_anchore-scratch


Local Volumes space usage:

VOLUME NAME                                                 LINKS               SIZE
etcd01-data                                                  1                   144.8MB
mongodb-data                                                 1                   412.7MB
postgres-db-volume                                           1                   276.1MB
topsec-dsec-logs                                             0                   0B
topsec-registry-data                                         0                   0B
anchore-scratch                                              1                   0B
psql-data                                                    0                   0B
fa786b764a2ffd4e54101df749701f1b9261aa751d6907174f4a0f8068   0                   0B
c64ed74141e023c24fd07a1b78ec87d92a058a1419a559133786e34b48   1                   0B
```







## 限制和清理

### 限制容器日志的大小

上方说过，容器会有日志文件，它可以通过 docker logs 观看，这部分日志实际上是 执行容器endpoint启动命令的程序所输出的终端输出，docker-compose文件中的logging配置可以实现这部分日志的大小和轮询数量：

```dockerfile
nginx:
    image: nginx:1.12.1
    restart: always
    logging:
        driver: "json-file"
        options:
            max-size: "200k"
            max-file: "10"
```





### 清理

``` sh
# 删除停止的容器 
docker container prune

# 删除不用的镜像
docker image prune

# 清除不用的挂载卷
docker volume prune

# 一键清理
docker system prune
WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - all dangling build cache
Are you sure you want to continue? [y/N]
```

