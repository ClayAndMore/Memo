---
title: "Docker 排查.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---


#### docker logs <container_id>



#### docker stats <container_id>



#### docker exec -it <container_id> /bin/bash



### debug docker

``` sh
[root@localhost ~]# cat /etc/docker/daemon.json
{
    "debug": true
}
```

可以在 journalctl 里看到一些docker 启动时的调试输出。



### 删除docker0

```
ifconfig docker0 down
brctl delbr docker0
```

```sh
docker inspect $(docker ps  | awk '{print $2}' | grep -v ID) | jq .[].RepoTags
```



### attach

有时候我们可以在容器内执行命令，不退出命令而退出容器，这样可以方便调试，或者命令行过长，命令执行失败时比较好用

``` sh
docker run -dit ubuntu bash
docker attach CONTAINER_NAME/id
# 退出容器  ^P^Q （ctrl+P ctrl+Q）
```

