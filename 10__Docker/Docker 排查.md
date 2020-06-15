
---
title: "Docker 排查.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


#### docker logs <container_id>



#### docker stats <container_id>



#### docker exec -it <container_id> /bin/bash



### 删除docker0

```
ifconfig docker0 down
brctl delbr docker0
```

```sh
docker inspect $(docker ps  | awk '{print $2}' | grep -v ID) | jq .[].RepoTags
```