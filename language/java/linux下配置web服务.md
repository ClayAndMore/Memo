---
title: linux下配置web服务
date: 2016-07-20 10:08:02
categories: linux
tags: [linux,tomcat]
---

### 安装java
* yum list available java* 查看可用的java包
* yum install java-1.8.0  安装上表列出的所有可安装的1.8.0
* java -version 查看java的版本

### 安装tomcat
* yum list available tomcat* 和上面一样，查看可用的tomcat包
* yum install  tomcat tomcat-webapps tomcat-admin-webapps tomcat-docs-webapp tomcat-javadoc 安装必要的组件
* cd etc/tomcat    到这个目录下
* vim tomcat-users.xml 编辑这个文件，添加tomcat用户，找个位置添加：
```xml
<role rolename="admin-gui"/>
<role rolename="manager-gui"/>
<user username="tomcat" password="tomcat" roles="admin-gui,manager-gui"/>
```
<!-- more -->

保存退出：wq

* service tomcat start  启动tomcat
* chkconfig tomcat on  开机启动，添加到快捷启动
* firewall-cmd --zone=public --add-port=8080/tcp --permanent 开启防火墙的8080端口
* firewall-cmd --reload 重新启动防火墙

### 安装Mariadb
* yum  install mariadb*
* service mariadb start
* chkconfig mariadb on
* mysql -u root
* mysql > use mysql;
* mysql > update user set password=password('123456') where user='root'; 设置root用户的密码
* mysql > exit;

```sql
mysql -u root -p   //进入数据库
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '123456' WITH GRANT OPTION;     //让所有同一网段访问此数据库。
flush privileges;  //强制让MySQL重新加载权限，这样刚才修改的就马上生效
```
#### 开放3306端口
*  vim /etc/sysconfig/iptables 进入到这个目录下 添加iptables的内容为：A INPUT -p tcp -m state --state NEW -m tcp --dport 3306 -j ACCEPT
*  保存后重启防火墙：service iptables restart

### 进入数据库
在Navicat中新建Mariadb的连接：
![](http://7xs1eq.com1.z0.glb.clouddn.com/Maria%20DB%20%E8%BF%9E%E6%8E%A5%E5%B1%9E%E6%80%A7.png)
ip地址一般为本机，或者虚拟机的ip

### 进入tomcat
在本机浏览器输入：虚拟机（服务器）ip:8080  
右侧有个按钮：Manager App ,输入上方user-xml配置文件中的用户和密码。
导入war包：
![](http://7xs1eq.com1.z0.glb.clouddn.com/inputWar.png)
然后点击：Deploye