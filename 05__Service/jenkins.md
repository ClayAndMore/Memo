## jenkins

https://www.jenkins.io



### 下载 in docker

https://www.jenkins.io/doc/book/installing/#linux

下载地址：https://www.jenkins.io/zh/download/

推荐使用 docker hub 的 [`jenkinsci/blueocean`](https://hub.docker.com/r/jenkinsci/blueocean/) 镜像，它包含了 Blue Ocean插件。

[Getting started with Blue Ocean](https://www.jenkins.io/doc/book/blueocean/getting-started)

安装过程：

``` sh
# 1. 创建一个jenkins 网桥
docker network create jenkins
# 2. 创建挂载卷， 将 TLS 证书 和 jenkins 一些永久的数据挂载出来
docker volume create jenkins-docker-certs
docker volume create jenkins-data
# 这种创建方式会在主机 /var/lib/docker/volumes/jenkins-data 和 /var/lib/docker/volumes/jenkins-docker-certs 创建目录


# 3. 
docker container run \
  --name jenkins-docker \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind
```







## 问题

### 重置管理员密码

进到 jenkinds 容器，找到 它的admin/config.xml 文件：

``` sh
bash-4.2$ find / -name config.xml
/opt/openshift/configuration/users/admin/config.xml
/opt/openshift/configuration/jobs/OpenShift Sample/config.xml
/opt/openshift/configuration/config.xml
...
/var/lib/jenkins/users/admin/config.xml # 一般是在这个目录
/var/lib/jenkins/jobs/OpenShift Sample/config.xml
...
bash-4.2$ vi /var/lib/jenkins/users/admin/config.xml/var/lib/jenkins/users/admin/config.xml/var/lib/jenkins/users/admin/config.xml^C
bash-4.2$ vi /var/lib/jenkins/users/admin/config.xml # 修改
```

修改admin的加密密码为123456的加密密码 #jbcrypt:$2a$10$MiIVR0rr/UhQBqT.bBq0QehTiQVqgNpUGyWW2nJObaVAM/2xSQdSq

``` xml 
<hudson.security.HudsonPrivateSecurityRealm_-Details>
      <passwordHash>#jbcrypt:$2a$10$MiIVR0rr/UhQBqT.bBq0QehTiQVqgNpUGyWW2nJObaVAM/2xSQdSq</passwordHash>

</hudson.security.HudsonPrivateSecurityRealm_-Details>
```

