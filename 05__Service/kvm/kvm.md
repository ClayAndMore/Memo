---
title: "kvm.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

### 安装



一个镜像下载的地方：<https://mirrors.aliyun.com/centos/7/isos/x86_64/>





### 创建qcow2

```
cd /disk/kvm
qemu-img create -f qcow2 -o preallocation=off /disk/kvm/centos7.qcow2 100G
```

参考：<https://www.ichiayi.com/wiki/tech/centos6_kvm_console>





### 启动配置

尝试成功的启动配置如下：(centos 6)

```
virt-install \
--virt-type=kvm \
--name=CentOS7 \
--vcpus=2 \
--ram=4096 \
--os-type linux \
--disk path=/disk/kvm/centos7.qcow2,format=qcow2,size=100,bus=virtio \
--cdrom /disk/kvm/iso/CentOS-7-x86_64-Minimal-1810.iso \
--network bridge=virbr0 \
--graphics none
```



centos7:

```
virt-install \
--virt-type=kvm \
--name=CentOS7 \
--vcpus=2 \
--ram=4096 \
--os-type linux \
--location=/home/wy/kvm_test/CentOS-7-x86_64-DVD-1810.iso \
--disk path=/home/wy/kvm_test/centos7.qcow2,format=qcow2,size=30,bus=virtio \
--network bridge=virbr0 \
--graphics none \
--extra-args='console=ttyS0'
```





### 设置console

启动后，按下tab，输入：

 console=ttyS0,115200 

<https://www.ichiayi.com/wiki/tech/centos6_kvm_console>

https://www.cnblogs.com/xieshengsen/p/6215168.html



### 配置虚拟机

启动后会出现如下内容：

```
Starting installer, one moment...
anaconda 21.48.22.134-1 for CentOS 7 started.
 * installation log files are stored in /tmp during the installation
 * shell is available on TTY2
 * when reporting a bug add logs from /tmp as separate text/plain attachments
18:21:12 Not asking for VNC because we don't have a network
================================================================================
================================================================================
Installation

 1) [x] Language settings                 2) [!] Time settings
        (English (United States))                (Timezone is not set.)
 3) [!] Installation source               4) [!] Software selection
        (Processing...)                          (Processing...)
 5) [!] Installation Destination          6) [x] Kdump
        (No disks selected)                      (Kdump is enabled)
 7) [ ] Network configuration             8) [!] Root password
        (Not connected)                          (Password is not set.)
 9) [!] User creation
        (No user will be created)
  Please make your choice from above ['q' to quit | 'b' to begin installation |
  'r' to refresh]: 

[anaconda] 1:main* 2:shell  3:log  4:storage-lo> Switch tab: Alt+Tab | Help: F1 
```

此时进入主题，随便玩玩就可以进入了。

一些基本的设置以后，如下显示：

```
Installation

 1) [x] Language settings                 2) [x] Time settings
        (English (United States))                (Asia/Shanghai timezone)
 3) [x] Installation source               4) [x] Software selection
        (Local media)                            (Minimal Install)
 5) [x] Installation Destination          6) [x] Kdump
        (Automatic partitioning                  (Kdump is disabled)
        selected)                         8) [x] Root password
 7) [ ] Network configuration                    (Password is set.)
        (Not connected)
 9) [ ] User creation
        (No user will be created)
  Please make your choice from above ['q' to quit | 'b' to begin installation |
  'r' to refresh]: 
```

基本设置如下：

1. 语言保持不变
2. 时区选择上海
3. 安装源选择本地镜像
4. 软件选择最小安装
5. 安装磁盘选择自动分别，且使用LVM逻辑卷管理
6. 关闭Kdump，虚拟机关系不大
7. 网络先不管，安装之后处理
8. Root 密码设置为 `123456`
9. 不创建新用户

最后，按下`b`开始安装过程。



#### throubleshoot

#### no bootable device

第五步没有设置好



### 安装参考

详解：http://blog.chinaunix.net/uid-30022178-id-5749329.html

centos 6:



centos 7:

https://www.loveyu.org/5538.html

[https://ailitonia.com/archives/centos7-kvm%E8%99%9A%E6%8B%9F%E5%8C%96%E5%B9%B3%E5%8F%B0%E9%83%A8%E7%BD%B2%E6%95%99%E7%A8%8B/]



### console 登录

https://www.oldboyedu.com/zuixin_wenzhang/index/id/366.html

https://www.cnblogs.com/xieshengsen/p/6215168.html



### 克隆虚拟机

```
[root@node198 kvm_test]#virsh list
 Id    Name                           State
----------------------------------------------------
 5     CentOS7                        running

[root@node198 kvm_test]#virsh list
 Id    Name                           State
----------------------------------------------------
 5     CentOS7                        running

[root@node198 kvm_test]#virsh shutdown CentOS7
Domain CentOS7 is being shutdown

[root@node198 kvm_test]#virsh list
 Id    Name                           State
----------------------------------------------------

[root@node198 kvm_test]# virt-clone --original CentOS7 --auto-clone --name CentOS7_102
Allocating 'centos7-clone.qcow2'                          |  30 GB  00:00:02     

Clone 'CentOS7_102' created successfully.
[root@node198 kvm_test]#virsh list
 Id    Name                           State
----------------------------------------------------

[root@node198 kvm_test]#virsh list --all
 Id    Name                           State
----------------------------------------------------
 -     CentOS7                        shut off
 -     CentOS7_102                    shut off

[root@node198 kvm_test]#virsh start CentOS7
Domain CentOS7 started

[root@node198 kvm_test]#virsh start CentOS7_102
Domain CentOS7_102 started

[root@node198 kvm_test]#virsh list
 Id    Name                           State
----------------------------------------------------
 6     CentOS7                        running
 7     CentOS7_102                    running

```

进入 CentOS7_102修改网卡信息。



## Derbian 10 install KVM

### 安装

验证是否开启虚拟化：

` grep --color --perl-regexp 'vmx|svm' /proc/cpuinfo`

如果什么没抓到证明没有开启。

安装 KVM and QEMU：

```
apt update
apt install qemu qemu-kvm qemu-system qemu-utils
```

安装libvirt:

为了方便地创建和管理虚拟机，使用了libvirt。它是KVM和QEMU虚拟化的必备工具。libvirt和所有必需的工具都可以在Debian 10 Buster的官方包库中找到。要安装libvirt和所有必要的工具，运行以下命令:

`apt install libvirt-clients libvirt-daemon-system virtinst`

安装完后看下状态：

`systemctl status libvirtd`

如果没有运行，尝试`systemctl start libvirtd`



### 虚拟机的默认网络

``` sh
# virsh net-list --all
 Name      State      Autostart   Persistent
----------------------------------------------
 default   active     no         yes
```

为了创建虚拟机，默认网络必须被激活

```sh
virsh net-start default
virsh net-autostart default
```



### 创建虚拟机

创建目录：

```
mkdir -pv /kvm/{disk,iso}
/kvm
-- disk/
--Iso/
```

下载镜像：

```sh
cd /kvm/iso
sudo wget http://releases.ubuntu.com/16.04.6/ubuntu-16.04.6-server-amd64.iso
```

安装：

```sh
$ sudo virt-install --name server01 \
--os-type linux \
--os-variant ubuntu16.04 \
--ram 1024\
--disk /kvm/disk/server01.img,device=disk,bus=virtio,size=10,format=qcow2 \
--graphics vnc,listen=0.0.0.0 \
--noautoconsole \
--hvm \
--cdrom /kvm/iso/ubuntu-16.04.6-server-amd64.iso \
--boot cdrom,hd
```

还可以使用 virt-manager 图形界面来创建虚拟机



## 问题

### qemu-kvm: could not open disk image ' ': Permission denied

vim  /etc/libvirt/qemu.conf :

打开 user 和 group 的注释：

```sh
#       user = "100"    # A user named "100" or a user with uid=100
#
user = "root"

# The group for QEMU processes run by the system instance. It can be
# specified in a similar way to user.
group = "root"

# Whether libvirt should dynamically change file ownership
# to match the configured user/group above. Defaults to 1.
```

重启： service libvirtd restart

https://github.com/jedi4ever/veewee/issues/996