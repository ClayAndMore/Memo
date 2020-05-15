

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