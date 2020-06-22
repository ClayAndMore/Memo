---
title: "centos7.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-02-08 12:28:55 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux]

### firwalld

在centos7里使用firewalld代替了iptables。在启动firewalld之后，iptables还会被使用，属于引用的关系。

1. FirewallD 使用区域和服务而不是链式规则。
2. FirewallD可以动态修改单条规则，而不需要像iptables那样，在修改了规则后必须得全部刷新才可以生效。

在RHEL7里有几种防火墙共存：FirewallD、iptables、ebtables，默认是使用FirewallD来管理netfilter子系统，不过底层调用的命令仍然是iptables等。



#### firewalld的基本使用

启动： systemctl start firewalld

关闭： systemctl stop firewalld

查看状态： systemctl status firewalld 

开机禁用  ： systemctl disable firewalld

开机启用  ： systemctl enable firewalld

 

 

#### 使用systemctl

systemctl是CentOS7的服务管理工具中主要的工具，它融合之前service和chkconfig的功能于一体。

启动一个服务：systemctl start firewalld.service
关闭一个服务：systemctl stop firewalld.service
重启一个服务：systemctl restart firewalld.service
显示一个服务的状态：systemctl status firewalld.service
在开机时启用一个服务：systemctl enable firewalld.service
在开机时禁用一个服务：systemctl disable firewalld.service
查看服务是否开机启动：systemctl is-enabled firewalld.service
查看已启动的服务列表：systemctl list-unit-files|grep enabled
查看启动失败的服务列表：systemctl --failed

查看服务的具体信息： ` systemctl cat docker`



#### 配置firewalld-cmd

查看版本： firewall-cmd --version

查看帮助： firewall-cmd --help

显示状态： firewall-cmd --state

查看所有打开的端口： firewall-cmd --zone=public --list-ports

更新防火墙规则： firewall-cmd --reload

查看区域信息:  firewall-cmd --get-active-zones

查看指定接口所属区域： firewall-cmd --get-zone-of-interface=eth0

拒绝所有包：firewall-cmd --panic-on

取消拒绝状态： firewall-cmd --panic-off

查看是否拒绝： firewall-cmd --query-panic

 

#### 开启一个端口

添加

firewall-cmd --zone=public --add-port=80/tcp --permanent    （--permanent永久生效，没有此参数重启后失效）

重新载入

firewall-cmd --reload

查看

firewall-cmd --zone=public --query-port=80/tcp

删除

firewall-cmd --zone= public --remove-port=80/tcp --permanent



### 关闭SELinux

```shell
# 查看状态：sestatus
[root@rdo ~]# sestatus  
SELinux status:                 enabled  
SELinuxfs mount:                /sys/fs/selinux  
SELinux root directory:         /etc/selinux  
Loaded policy name:             targeted  
Current mode:                   enforcing  
Mode from config file:          enforcing  
Policy MLS status:              enabled  
Policy deny_unknown status:     allowed  
Max kernel policy version:      28  

```



临时关闭： `setenforce 0`

永久关闭：

```
vi  /etc/selinux/config
#SELINUX=enforcing  
SELINUX=disabled 
```

重启后：

```
[root@rdo ~]# sestatus  
SELinux status:                 disabled  
```



