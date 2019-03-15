tags: [docker]
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

https://www.liquidweb.com/kb/how-to-install-docker-on-centos-6/

https://docs.docker.com/install/linux/docker-ce/centos/

https://blog.csdn.net/kinginblue/article/details/73527832



#### 配置

默认配置文件：`/etc/default/docker` 

服务管理脚本：`/etc/init.d/docker`

​               日志： `/var/log/upstart/docker.log`



#### 命令

确保服务正常运行：`docker version`

服务停止和重起等，都和服务命令一样： `docker  start | relstart | stop`



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



### 待补充

docker各版本的区别：

https://segmentfault.com/a/1190000009915050