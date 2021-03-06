---
title: "libvirt 命令.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: false
tags: [""]
categories: ["虚拟化"]
author: "Claymore"

---





## virsh 

一些常用的虚拟机命令：

``` sh
# KVM虚拟机开机
virsh start oeltest01
# virsh关机
virsh shutdown oeltest01 
# 强制关闭电源
virsh destroy wintest01
 
# 通过配置文件启动虚拟机
virsh create /etc/libvirt/qemu/wintest01.xml
# 配置开机自启动虚拟机
virsh autostart oeltest01
 
# 导出KVM虚拟机配置文件
virsh dumpxml wintest01 > /etc/libvirt/qemu/wintest02.xml
 
# 编辑KVM虚拟机配置文件
virsh edit wintest01
# virsh edit将调用vi命令编辑/etc/libvirt/qemu/wintest01.xml配置文件。也可以直接通过vi命令进行编辑，修改，保存。
 
# virsh console 控制台管理linux虚拟机
virsh console oeltest01 
```



所有：

``` sh
autostart      #自动加载指定的一个虚拟机
connect        #重新连接到hypervisor
console        #连接到客户会话
create         #从一个SML文件创建一个虚拟机
start          #开始一个非活跃的虚拟机
destroy        #删除一个虚拟机
define         #从一个XML文件定义一个虚拟机
domid          #把一个虚拟机名或UUID转换为ID
domuuid        #把一个郁闷或ID转换为UUID
dominfo        #查看虚拟机信息
domstate       #查看虚拟机状态
domblkstat     #获取虚拟机设备快状态
domifstat      #获取虚拟机网络接口状态
dumpxml        #XML中的虚拟机信息
edit           #编辑某个虚拟机的XML文件
list           #列出虚拟机
migrate        #将虚拟机迁移到另一台主机
quit           #退出非交互式终端
reboot         #重新启动一个虚拟机
resume         #重新恢复一个虚拟机
save           #把一个虚拟机的状态保存到一个文件
dump           #把一个虚拟机的内核dump到一个文件中以方便分析
shutdown       #关闭一个虚拟机
setmem         #改变内存的分配
setmaxmem      #改变最大内存限制值
suspend        #挂起一个虚拟机
vcpuinfo       #虚拟机的cpu信息
version        #显示virsh版本
```



### 备份

```bash
virsh dumpxml ubuntu16 > ubntu16.xml
```



## 其他命令

### virt-edit

它是对镜像文件修改的命令，记得要把该镜像运行的虚拟机关掉：

virsh shutdown vm

用virt-edit进行修改，例如我们修改一下/etc/hosts文件：

`virt-edit -d vm /etc/hosts`

具体使用：http://libguestfs.org/virt-edit.1.html