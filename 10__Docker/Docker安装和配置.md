---
title: "Docker安装和配置.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-03-17 18:47:27 +0800
draft: false
tags: [""]
categories: ["Docker"]
author: "Claymore"

---

### 安装

官网：`https://www.docker.com/`

#### 手动安装

ubuntu 为例

系统要求：

- 64位
- 内核版本>=3.10 查看内核版本：`uname -a`
- Ubuntu版本>=12.04 LTS   检查：`more /etc/issue`

具体步骤

1. 安装支持HTTPS的源：

   `apt-get install -y apt-transport-https`

2. 添加源的gpg密钥

   `sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`

3. 获取操作系统的代号（每个版本的系统都会有个代号，和安卓系统类似）

   `lsb_release -c`

4. 添加官方apt软件源：

   ` <<EOF > /etc/apt/sources.list.d/docker.list`:

   ```
   deb https://apt.dockerproject.org/repo ubuntu-xenial main
   EOF
   ```

#### 通过官方脚本安装

`curl -fsSL https://get.docker.com/ | sh`

或： `wget -qO- https://get.docker.com/ | sh`



#### 通过软件管理安装

```
sudo apt install docker.io
```



#### centos

centos 6:

https://www.liquidweb.com/kb/how-to-install-docker-on-centos-6/

https://docs.docker.com/install/linux/docker-ce/centos/

https://blog.csdn.net/kinginblue/article/details/73527832

采用最新`epel`的YUM源可以安装到`docker 1.7`版本

```bash
## centos6下安装epel源
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
sudo rpm -Uvh epel-release-6*.rpm

## centos6安装docker1.7
yum install docker-io
# 如果还是找不到docker-io 
yum install http://yum.dockerproject.org/repo/main/centos/6/Packages/docker-engine-1.7.1-1.el6.x86_64.rpm
```

安装 dokcer 1.9

```
## download
curl -sSL -O https://get.docker.com/builds/Linux/x86_64/docker-1.9.1
## grant privilege
chmod +x docker-1.9.1 
## backup and make new
mv /usr/bin/docker /usr/bin/docker-1.7
cp ./docker-1.9.1 /usr/bin/docker

## restart docker
/etc/init.d/docker restart
```

验证安装：

```
root@pts/0 # docker version
Client:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.3
 Git commit:   a34a1d5
 Built:        Fri Nov 20 17:56:04 UTC 2015
 OS/Arch:      linux/amd64

Server:
 Version:      1.9.1
 API version:  1.21
 Go version:   go1.4.3
 Git commit:   a34a1d5
 Built:        Fri Nov 20 17:56:04 UTC 2015
 OS/Arch:      linux/amd64
```



升级到更高docker版本：

http://www.senra.me/centos6-install-new-docker-191-or-113/



centos 7:

```
$ sudo yum update
```

- 运行Docker的安装脚本

```
$ curl -fsSL https://get.docker.com/ | sh
```

- 启动守护进程

```
$ sudo systemctl start docker
```

设置docker守护线程开机自启动

```
$ sudo systemctl enable docker
```



#### 配置

默认配置文件：`/etc/default/docker` 

服务管理脚本：`/etc/init.d/docker`

​               日志： `/var/log/upstart/docker.log`



#### 命令

确保服务正常运行：`docker version`

服务停止和重起等，都和服务命令一样： `docker  start | relstart | stop`



### debian

到 https://download.docker.com/linux/debian/dists/stretch/pool/stable/amd64/

下载 containerd.io, docker-ce-cli, docker-ce 三个deb包。然后在服务器上 `dpkg -i *.deb`



### 卸载

#### ubuntu:

`dpkg -l | grep -i docker`

确定一下是以下哪种：

```
sudo apt-get purge -y docker-engine docker docker.io docker-ce  
sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce  
```



或直接`sudo apt remove --purge docker*`



删除一下配置文件：

```
sudo rm -rf /var/lib/docker
sudo rm /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock
```

1.13 后有专门的清理命令：

```
root@wy:~/images# docker system prune
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache

Are you sure you want to continue? [y/N] y
Deleted Networks:
docker_gwbridge
x86_default
webui_default
docker-images_dsec_br

Total reclaimed space: 0B
```

专门清理资源(container、image、网络)的命令



#### centos:

搜索已经下载的docker:

` yum list installed|grep docker `
或者使用该命令 

```bash
[root@localhost ~]# rpm -qa|grep docker 
docker.x86_64 2:1.12.6-16.el7.centos @extras 
docker-client.x86_64 2:1.12.6-16.el7.centos @extras 
docker-common.x86_64 2:1.12.6-16.el7.centos @extra
```



删掉镜像等文件：`rm -rf /var/lib/docker`




### 待补充

docker各版本的区别：

https://segmentfault.com/a/1190000009915050