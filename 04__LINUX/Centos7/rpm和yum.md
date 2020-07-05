---
title: "centos7 包管理 rpm 和 yum.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-04-03 19:50:52 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---



## rpm

 RedHat Package Manager 

这个软件管理
的机制是由 Red Hat 这家公司发展出来的。 RPM 是以一种数据库记录的方式来将你所需要
的软件安装到你的 Linux 系统的一套管理机制

他最大的特点就是将你要安装的软件先编译过， 并且打包成为 RPM 机制的包装文件，通过
包装好的软件里头默认的数据库记录， 记录这个软件要安装的时候必须具备的相依属性软
件，当安装在你的 Linux 主机时， RPM 会先依照软件里头的数据查询 Linux 主机的相依属性
软件是否满足， 若满足则予以安装，若不满足则不予安装。那么安装的时候就将该软件的信
息整个写入 RPM 的数据库中，以便未来的查询、验证与反安装！这样一来的优点是：

1. 由于已经编译完成并且打包完毕，所以软件传输与安装上很方便 （不需要再重新编
   译）；
2. 由于软件的信息都已经记录在 Linux 主机的数据库上，很方便查询、升级与反安装



### rpm 安装包

安装软件是 root 的工作，因此你得要是 root 的身份才能够操作 rpm 这指令的。

```shell
[root@study ~]# rpm -ivh package_name
选项与参数：
-i ：install 的意思
-v ：察看更细部的安装信息画面
-h ：以安装信息列显示安装进度

# 范例一：安装原版光盘上的 rp-pppoe 软件
[root@study ~]# rpm -ivh /mnt/Packages/rp-pppoe-3.11-5.el7.x86_64.rpm
Preparing... ################################# [100%]
Updating / installing...
1:rp-pppoe-3.11-5.el7 ################################# [100%]

# 范例二、一口气安装两个以上的软件时：
[root@study ~]# rpm -ivh a.i386.rpm b.i386.rpm *.rpm
# 后面直接接上许多的软件文件！

# 范例三、直接由网络上面的某个文件安装，以网址来安装：
[root@study ~]# rpm -ivh http://website.name/path/pkgname.rpm
```



rpm 安装时常用的选项与参数说明:

| 选项     | 代表意义， 使用时机                                          |
| -------- | ------------------------------------------------------------ |
| --nodeps | 当发生软件属性相依问题而无法安装，但你执意安装时。危险性： 软件会有相依性的原因是因为彼此会使用到对方的机制或功能，如果强制安装而不考虑软件的属性相依， 则可能会造成该软件的无法正常使用！ |

| --replacefiles  | 如果在安装的过程当中出现了“某个文件已经被安装在你的系统上面”的信息，又或许出现版本不合的讯息 （confilcting files） 时，可以使用这个参数来直接覆盖文件。危险性： 覆盖的动作是无法复原的！
所以，你必须要很清楚的知道被覆盖的文件是真的可以被覆盖喔！否则会欲哭无泪！ |
| --force         | 这个参数其实就是 --replacefiles 与 --replacepkgs 的综合体！  |
| --test          | 想要测试一下该软件是否可以被安装到使用者的 Linux 环境<br/>当中，可找出是否有属性相依的问题。范例为：
rpm -ivh pkgname.i386.rpm --test |
| --justdb        | 由于 RPM 数据库破损或者是某些缘故产生错误时，可使用这<br/>个选项来更新软件在数据库内的相关信息。 |
| --nosignature   | 想要略过数码签章的检查时，可以使用这个选项。                 |
| --prefix 新路径 | 要将软件安装到其他非正规目录时。举例来说，你想要将某软件安装到 /usr/local 而非正规的 /bin, /etc 等目录， 就可以使用“ --prefix/usr/local ”来处理了。 |
| --noscripts     | 不想让该软件在安装过程中自行执行某些系统指令。说明：<br/>RPM 的优点除了可以将文件放置到定位之外，还可以自动执行一些前置
作业的指令，例如数据库的初始化。 如果你不想要让 RPM 帮你自动执行
这一类型的指令，就加上他吧！ |

建议直接使用 -ivh

**eg: 从光盘中安装：**

在没有网络的前提下，你想要安装一个名为 pam-devel 的软件，你手边只有原版光
盘，该如何是好？答：你可以通过挂载原版光盘来进行数据的查询与安装。请将原版光盘放
入光驱，下面我们尝试将光盘挂载到 /mnt 当中， 并据以处理软件的下载啰：
挂载光盘，使用： `mount /dev/sr0 /mnt`
找出文件的实际路径：`find /mnt -name 'pam-devel*'`
测试此软件是否具有相依性：` rpm -ivh pam-devel... --test`
直接安装：` rpm -ivh pam-devel...`
卸载光盘： `umount /mnt`



### rpm 升级与更新

就以 -Uvh 或 -Fvh 来升级即可，-U 与 -F 的意义还是不太一样的，基本的差别是这
样的：

| UVh  | 后面接的软件即使没有安装过，则系统将予以直接安装； 若后面接的软件有安装<br/>过旧版，则系统自动更新至新版 |
| ---- | ------------------------------------------------------------ |
| Fvh  | 如果后面接的软件并未安装到你的 Linux 系统上，则该软件不会被安装；亦即只<br/>有已安装至你 Linux 系统内的软件会被“升级”！ |



### rpm 查询

```shell
rpm -qa # 已安装软件

选项与参数：
查询已安装软件的信息：
-q ：仅查询，后面接的软件名称是否有安装；
-qa ：列出所有的，已经安装在本机 Linux 系统上面的所有软件名称；
-qi ：列出该软件的详细信息 （information），包含开发商、版本与说明等；
-ql ：列出该软件所有的文件与目录所在完整文件名 （list）；
-qc ：列出该软件的所有配置文件 （找出在 /etc/ 下面的文件名而已）
-qd ：列出该软件的所有说明文档 （找出与 man 有关的文件而已）
-qR ：列出与该软件有关的相依软件所含的文件 （Required 的意思）
-qf ：由后面接的文件名称，找出该文件属于哪一个已安装的软件；
-q --scripts：列出是否含有安装后需要执行的脚本档，可用以 debug 喔！
查询某个 RPM 文件内含有的信息：
-qp[icdlR]：注意 -qp 后面接的所有参数以上面的说明一致。但用途仅在于找出
某个 RPM 文件内的信息，而非已安装的软件信息！注意！
```

一般使用-qa, -ql就可以了



### rpm 卸载

解安装的过程一定要由最上层往下解除

移除的选项很简单，就通过 -e 即可移除。不过，很常发生软件属性相依导致无法移除某些软
件的问题

```shell
# 1. 找出与 pam 有关的软件名称，并尝试移除 pam 这个软件：
[root@study ~]# rpm -qa | grep pam
fprintd-pam-0.5.0-4.0.el7_0.x86_64
pam-1.1.8-12.el7.x86_64
gnome-keyring-pam-3.8.2-10.el7.x86_64
pam-devel-1.1.8-12.el7.x86_64
pam_krb5-2.4.8-4.el7.x86_64
[root@study ~]# rpm -e pam
error: Failed dependencies: # 这里提到的是相依性的问题
libpam.so.0（）（64bit） is needed by （installed） systemd-libs-208-20.el7.x86_64
libpam.so.0（）（64bit） is needed by （installed） libpwquality-1.2.3-4.el7.x86_64
....（以下省略）....
# 2. 先尝试移除 pam-devel
[root@study ~]# rpm -e pam-devel # ps,不会出现任何讯息
[root@study ~]# rpm -q pam-devel
package pam-devel is not installed

```



由于 RPM 文件常常会安装/移除/升级等，某些动作或许可能会导致 RPM 数据库 /var/lib/rpm/
内的文件破损。果真如此的话，那你该如何是好？别担心，我们可以使用 --rebuilddb 这个选
项来重建一下数据库:

`[root@study ~]# rpm --rebuilddb <==重建数据库`



## srpm

Source RPM, 的扩展名是以 *.src.rpm 这种格式来命名的

也就是这个 RPM 文件里面含有源代码,并没有经过编译。

既然 SRPM 提供的是源代码，那么为什么我们不使用 Tarball 直接来安装就好了？

这是因为 SRPM 虽然内容是源代码， 但是他仍然含有该软件所需要的相依性软件说明、以及所有 RPM 文件所提供的数据。
同时，他与 RPM 不同的是，他也提供了参数配置文件（就是 configure 与 makefile）

* 先将该软件以 RPM 管理的方式编译，此时 SRPM 会被编译成为 RPM 文件；
* 然后将编译完成的 RPM 文件安装到 Linux 系统当中



## yum

rpm是redhat公司的一种软件包管理机制，直接通过rpm命令进行安装删除等操作，最大的优点是自己内部自动处理了各种软件包可能的依赖关系。

| 説明                       | [Redhat](http://d.hatena.ne.jp/keyword/Redhat)系             | [Debian](http://d.hatena.ne.jp/keyword/Debian)系             |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 更新缓存                   | yum makecache                                                | [apt](http://d.hatena.ne.jp/keyword/apt)-get update          |
| 更新包                     | [yum](http://d.hatena.ne.jp/keyword/yum) update              | [apt](http://d.hatena.ne.jp/keyword/apt)-get upgrade         |
| 检索包                     | [yum](http://d.hatena.ne.jp/keyword/yum) search              | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) search |
| 检索包内文件               | [yum](http://d.hatena.ne.jp/keyword/yum) provides            | [apt](http://d.hatena.ne.jp/keyword/apt)-file search         |
| 安装指定的包               | [yum](http://d.hatena.ne.jp/keyword/yum) install             | [apt](http://d.hatena.ne.jp/keyword/apt)-get install         |
| 删除指定的包               | [yum](http://d.hatena.ne.jp/keyword/yum) remove              | [apt](http://d.hatena.ne.jp/keyword/apt)-get remove          |
| 显示指定包的信息           | [yum](http://d.hatena.ne.jp/keyword/yum) info                | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 显示包所在组的一览         | [yum](http://d.hatena.ne.jp/keyword/yum) grouplist           | -                                                            |
| 显示指定包所在组的信息     | [yum](http://d.hatena.ne.jp/keyword/yum) groupinfo           | -                                                            |
| 安装指定的包组             | [yum](http://d.hatena.ne.jp/keyword/yum) groupinstall        | -                                                            |
| 删除指定的包组             | [yum](http://d.hatena.ne.jp/keyword/yum) groupremove         | -                                                            |
| 参考库的设定文件           | /etc/[yum](http://d.hatena.ne.jp/keyword/yum).repos.d/*      | /etc/[apt](http://d.hatena.ne.jp/keyword/apt)/sources.list   |
| 安装完的包的列表           | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qa                 | dpkg-query -l                                                |
| 显示安装完的指定包的信息   | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qi                 | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 安装完的指定包内的文件列表 | [rpm](http://d.hatena.ne.jp/keyword/rpm) -ql                 | dpkg-query -L                                                |
| 安装完的包的信赖包的列表   | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[qR](http://d.hatena.ne.jp/keyword/qR) | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) depends |
| 安装完的文件信赖的包       | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[q](http://d.hatena.ne.jp/keyword/qR)f | dpkg -S                                                      |

查看某些包的可用版本：

``` 
yum list | grep pcre
或：
yum list pcre
```



### 只下载 rpm 不安装

`sudo yum install --downloadonly --downloaddir=/tmp <package-name> `

注意，如果下载的包包含了任何没有满足的依赖关系，yum将会把所有的依赖关系包下载，但是都不会被安装。

另外一个重要的事情是，在CentOS/RHEL 6或更早期的版本中，你需要安装一个单独yum插件(名称为 yum-plugin-downloadonly)才能使用--downloadonly命令选项：

`sudo yum install yum-plugin-downloadonly `

如果没有该插件，你会在使用yum时得到以下错误：

Command line error: no such option: --downloadonly



### yum 源代理

在/etc/yum.conf后面添加以下内容：

```
proxy=http://192.168.1.1:8080
proxy_username=username # 可选
proxy_password=123456   # 可选
```



## repo 源

一些源：

Base.repo：

```
# CentOS 5
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-5.repo
# CentOS 6
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
# CentOS 7
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

```

epel源：EPEL官网地址：https://fedoraproject.org/wiki/EPEL

```
yum install epel-release
```



查看 有哪些源：

```
yum repolist
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * elrepo: mirrors.tuna.tsinghua.edu.cn
 * epel: mirrors.tuna.tsinghua.edu.cn
repo id                                                                    repo name                                                                                                 status
base/7/x86_64                                                              CentOS-7 - Base - 163.com                                                                                 10,019
docker-ce-stable/x86_64                                                    Docker CE Stable - x86_64                                                                                     52
elrepo                                                                     ELRepo.org Community Enterprise Linux Repository - el7                                                       124
*epel/x86_64                                                               Extra Packages for Enterprise Linux 7 - x86_64                                                            13,347
extras/7/x86_64                                                            CentOS-7 - Extras - 163.com                                                                                  435
kubernetes                                                                 Kubernetes                                                                                                   385
updates/7/x86_64                                                           CentOS-7 - Updates - 163.com                                                                               2,500
repolist: 26,862
```



### 缓存

重新生成缓存：

yum clean all  #清空缓存 

rm -rf /var/cache/yum/*

yum makecache  #重新生成缓存 



### 问题

#### http://people.centos.org/tru/devtools-2/7/x86_64/RPMS/repodata/repomd.xml: [Errno 14]

先yum update，一般还是会出现这个问题。去 /etc/yum.repos.d 里去掉devtools-2.repo(其实只要替换它的后缀)。

yum update此时可更新，但这个repo仍是个问题，目前怀疑是centos包太旧的问题。



#### Error: failure: repodata/-filelists.sqlite.bz2 from epel: [Errno 256] No more mirrors to try.

是yum镜像数据库的原因，更新：

```
# yum clean all
# rpm --rebuilddb
# yum update
```

