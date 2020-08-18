clearLog.sh

``` sh
#!/bin/bash

echo "run clear script"
date

checkDir="/var/log/"
if [ $1 ];then
    checkDir=$1
fi

ls -l $checkDir |grep "^-" | awk '{print $NF, $5}' > /tmp/clearFileAndSize


while read -r file size ; do
  # echo "file: $file,  size: $size " # 大于 1M则clear
  if [ ${size} -gt 1000000 ];then
      clearFile=${checkDir}${file}
      echo "clear file: " $clearFile "size: " $size
      echo "" > ${clearFile} # 清空该文件
  fi
done < /tmp/clearFileAndSize
```

clearC.sh

``` sh
docker exec topsec-scan-api      bash -c 'echo "" > /var/log/anchore/anchore-api.log'
docker exec topsec-scan-policy   bash -c 'echo "">/var/log/acnhore/anchore-policy-engine.log'
docker exec topsec-scan-analyzer bash -c 'echo "" > /var/log/anchore/anchore/anchore-worker.log'
docker exec topsec-scan-simpleq  bash -c 'echo "" > /var/log/anchore/anchore/anchore-simplequeue.log'
docker exec topsec-scan-catalog  bash -c 'echo "" > /var/log/anchore/anchore/anchore-catalog.log'
```





### 实际情况

镜像扫描容器，simples 2G多，其他的都10M左右， 

e s: 276M

Ips: 770M

其他的都几B