
---
title: "authore.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "authore.md"
date: 2019-12-13 17:48:06 +0800
lastmod: 2020-01-12 16:27:12 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---




## Anchore Engine

https://github.com/anchore/anchore-engine

Anchore Engine 是提供容器审查，分析，认证的集中服务。

它可以是作为单独的容器镜像 或 被提供给编排平台如 k8s, docker swarm, rancher, Amazon ECS等。

可以直接被RESTful API访问 或者通过 Anchore CLI.

在部署 Anchoe Engine 的环境下， 从 Docker V2 下载的容器镜像 根据安全策略去做出评价。

Anchore Engine 适合单机或网络交互， 作为一个服务和你的CI/CD密切交互，让你安全顺利的实际构建你的pipiline.

或者作为一个组件在容器监控和控制平台通过它的RESTful API.



Anchore Engine 也是 Anchore Enterpise 的基础 OSS 构建， Anchore Enterpise 是统计ui



### 工作原理

通过对容器的layer进行扫描，发现漏洞并进行预警，其使用数据是基于Common Vulnerabilities and Exposures数据库(简称CVE), 各Linux发行版一般都有自己的CVE源，而Anchore则是与其进行匹配以判断漏洞的存在与否，比如HeartBleed的CVE为：CVE-2014-0160, Anchore通过query 命令的 cve-scan选项可以对镜像的CVE进行扫描。





### Anchore - cli 

Anchore客户端叫Anchore-cli，可以管理和检查镜像、策略、订阅通知和镜像仓库。工作原理、安装和使用方式都很简单。

https://github.com/anchore/anchore-engine

安装： pip install anchorecli

出现问题：

```
Cannot uninstall 'certifi'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.
```

解决： pip install anchorecli --ignore-installed



## 安装

Anchore Engine 在 DockerHub 中以镜像的形式被提供。

```sh
root@VM:~# mkdir ~/aevolume
root@VM:~# cd ~/aevolume/
root@VM# ls
root@VM# docker pull docker.io/anchore/anchore-engine:latest
latest: Pulling from anchore/anchore-engine
c8d67acdb2ff: Pull complete
79d11c1a86c4: Pull complete
3e3314154f27: Pull complete
08b81ffc46c7: Pull complete
4e3e22e38b18: Pull complete
f1f8c2e16d22: Pull complete
0ba1c66332fc: Pull complete
cbf0c2b481e0: Pull complete
Digest: sha256:5164ca87cae0f78a4a5a68a92ec2ffbc6dd5478eeb3cf2fded01d50e592bafa4
Status: Downloaded newer image for anchore/anchore-engine:latest
root@VM:~/aevolume# docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
anchore/anchore-engine    latest              492bcf4b64df        3 weeks ago         678MB

# docker create --name ae docker.io/anchore/anchore-engine:latest
# docker cp ae:/docker-compose.yaml ~/aevolume/docker-compose.yaml
# docker rm ae

# docker-compose pull
# docker-compose up -d
```

没启动engine 时的CLI：

```
(base) root@VM# anchore-cli image list
Error: could not access anchore service (user=None url=http://localhost:8228/v1)

(base) root@VM:~/aevolume# docker-compose up -d
Creating network "aevolume_default" with the default driver
Creating volume "aevolume_anchore-db-volume" with default driver
Creating volume "aevolume_anchore-scratch" with default driver
Creating aevolume_anchore-db_1 ... done
Creating aevolume_engine-catalog_1 ... done
Creating aevolume_engine-simpleq_1       ... done
Creating aevolume_engine-api_1           ... done
Creating aevolume_engine-policy-engine_1 ... done
Creating aevolume_engine-analyzer_1      ... done
```



docker ps:

```
root@# docker ps
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS                            PORTS                                      NAMES
88645023af1f        anchore/anchore-engine:v0.5.2   "/docker-entrypoint.…"   10 seconds ago      Up 7 seconds (health: starting)   0.0.0.0:8228->8228/tcp                     aevolume_engine-api_1
e106ad267f90        anchore/anchore-engine:v0.5.2   "/docker-entrypoint.…"   10 seconds ago      Up 7 seconds (health: starting)   8228/tcp                                   aevolume_engine-analyzer_1
bc7789bb1824        anchore/anchore-engine:v0.5.2   "/docker-entrypoint.…"   10 seconds ago      Up 6 seconds (health: starting)   8228/tcp                                   aevolume_engine-policy-engine_1
fa165b199a41        anchore/anchore-engine:v0.5.2   "/docker-entrypoint.…"   10 seconds ago      Up 5 seconds (health: starting)   8228/tcp                                   aevolume_engine-simpleq_1
c86daeb61415        anchore/anchore-engine:v0.5.2   "/docker-entrypoint.…"   11 seconds ago      Up 9 seconds (health: starting)   8228/tcp                                   aevolume_engine-catalog_1
4d1ef329a6db        postgres:9                      "docker-entrypoint.s…"   12 seconds ago      Up 10 seconds                     5432/tcp                                   aevolume_anchore-db_1
```





### 注意

Anchore这个已经被Anchore-Engine替代，目前再使用会出现各种奇怪的问题。
Anchore分为社区版和商业版，社区版只有CLI接口，商业版提供Web页面以及更多的商业支持。

安装docker-compose 注意去官网：https://docs.docker.com/compose/install/





竞品资料： https://yq.aliyun.com/articles/661987