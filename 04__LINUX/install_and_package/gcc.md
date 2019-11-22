







###  repo 问题

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



 devtoolset 

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