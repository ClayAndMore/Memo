---
title: "dpkg 和 apt.md"
date: 2020-04-07 08:49:48 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---


## dpkg

dpkg 是用于管理 deb 包的包管理工具, 类似于rpm

**dpkg的缺陷**

- 不能主动从镜像站点获取软件包
- 安装软件包的时候不能自动安装相关依赖包



### 安装 deb 文件

使用  `dpkg -i <deb file>` 来安装 deb 文件,  如果失败它会说需要依赖。

之后可以尝试 `apt-get update`  然后会提示  "dependencies are ready to install"  再使用 `apt-get install -f`.

在这之后,  再用 `dpkg -i` 

ps:  `gdebi` 工具可以更好的做这件事  `gdebi [deb file]`.



### 查看 apt 安装的软件路径

dpkg -L 软件名

例如：dpkg -L gedit

```undefined
dpkg -L gedit  
/.  
/usr  
/usr/bin  
/usr/bin/gedit  
/usr/share  
/usr/share/applications  
/usr/share/applications/gedit.desktop  
```

dpkg -l 查看所有安装的软件

dpkg -L package  列出安装包清单

dpkg --contents 包的具体文件



### 移除包

dpkg -r package 移除包

dpkg -P package 移除包和配置文件





### apt



- apt-get 用于管理软件包，包括安装、卸载、升级

  apt-get install package （搜索本地一个数据库，详情看软件源）

  apt-get update   从软件镜像服务器上下载/更新用于本地软件源的软件包列表

  apt-get upgrade 自动升级软件包到最新版本

  apt-get check 检查当前apt管理里面的依赖包情况

  apt-get -f install 修复依赖包关系

  apt-get remove 卸载（但是卸载不干净，不包括软件包的配置文件）

  apt-get remove --purge package (完全卸载)

  apt-get --reinstall install package  重新安装




- 一些位置：

  apt source 镜像站点地址存在哪儿

  /etc/apt/sources.list

  apt的本地索引存在哪儿

  /var/lib/apt/lists/*

  apt的下载deb包存在哪里

  /var/cache/apt/archives









## apt

apt 是ubuntu系统的软件包管理工具



### apt-get

通过apt-get安装制定版本：

`apt-get install <<package name>>=<<version>>`

apt-get 可以缩写成apt 



**--no-install-recommends 参数**

默认情况下，Ubuntu安装推荐而不是建议的软件包。使用——no-install- recommendations，只安装主要的依赖项(Depends字段中的包)。

ps: `apt-get -y install --no-install-recommends suricata supervisor`

这样做在docker中可以减少镜像体积。



### 只下载不安装

apt-get 只下载不安装:

apt-get install -d PachageName

如果软件包已经安装:

apt-get install -d --reinstall PackageName

文件下载目录:

/var/cache/apt/archives



### update 和 upgrade 

update的作用是从/etc/apt/source.list文件中定义的源中去同步包的索引文件，即运行这个命令其实并没有更新软件，而是相当于windows下面的检查更新，获取的是软件的状态。

而upgrade则是更据update命令同步好了的包的索引文件，去真正地更新软件。

而dist-upgrade则是更聪明的upgrade，man文档中说它以更聪明的方式来解决更新过程中出现的软件依赖问题，它也是从/etc/apt/source.list文件中获得地址，然后从这些地址中检索需要更新的包。

每回更新之前，我们需要先运行update，然后才能运行upgrade和dist-upgrade，因为相当于update命令获取了包的一些信息，比如大小和版本号，然后再来运行upgrade去下载包



### apt list 

```text
apt list --installed
```

**这个会显示使用 `apt` 命令安装的所有的软件包**。

同时也会包含由于依赖而被安装的软件包。也就是说不仅会包含你曾经安装的程序，而且会包含大量库文件和间接安装的软件包。

可以结合 grep 找我们需要的包：`apt list --installed | grep program_name`

或者 我们可以使用 dpkg:

可以列出 Debian 系统的所有已经安装的软件包。

```text
dpkg-query -l
```



### apt-chache 

apt-cache :用于查询软件包信息，一般用于在安装某个包之前。

apt-cache show package 显示软件包信息

apt-cache policy package 显示软件包安装状态

apt-cache depends package 显示软件包依赖关系

apt-cache search package 在source某个名称的软件

列举版本列表：

0、通过网站搜索：https://packages.[ubuntu](https://www.centos.bz/tag/ubuntu/).com/

1、`apt-cache madison <<package name>>`

将列出所有来源的版本。如下输出所示：

```sh
# apt-cache madison vim
vim | 2:7.3.547-1 | http://debian.mirrors.tds.net/debian/ unstable/main amd64 Packages
vim | 2:7.3.429-2 | http://debian.mirrors.tds.net/debian/ testing/main amd64 Packages
vim | 2:7.3.429-2 | http://http.us.debian.org/debian/ testing/main amd64 Packages
vim | 2:7.3.429-2 | http://debian.mirrors.tds.net/debian/ testing/main Sources
vim | 2:7.3.547-1 | http://debian.mirrors.tds.net/debian/ unstable/main Sources
```


madison是一个apt-cache子命令，可以通过man apt-cache查询更多用法。



2、`apt-cache policy <<package name>>`

将列出所有来源的版本。信息会比上面详细一点，如下输出所示：

```
apt-cache policy gdb
gdb:
  Installed: 7.7.1-0ubuntu5~14.04.2
  Candidate: 7.7.1-0ubuntu5~14.04.2
  Version table:
 *** 7.7.1-0ubuntu5~14.04.2 0
        500 http://fr.archive.ubuntu.com/ubuntu/ trusty-updates/main amd64 Packages
        100 /var/lib/dpkg/status
     7.7-0ubuntu3 0
        500 http://fr.archive.ubuntu.com/ubuntu/ trusty/main amd64 Packages
        500 http://archive.ubuntu.com/ubuntu/ trusty/main amd64 Packages
```



## apt 源

可以手动替换为 清华源： https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/

### 添加源

```
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial main
EOF
```

或：

```
echo "deb [arch=amd64] https://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list
```

然后执行 apt-get update:

```
root@# apt-get update
Hit:1 http://mirrors.tencentyun.com/ubuntu xenial InRelease
Hit:2 http://mirrors.tencentyun.com/ubuntu xenial-security InRelease
Hit:3 http://mirrors.tencentyun.com/ubuntu xenial-updates InRelease
Get:4 https://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial InRelease [8,993 B]
Ign:4 https://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial InRelease
Hit:5 https://download.docker.com/linux/ubuntu xenial InRelease
Fetched 8,993 B in 0s (10.1 kB/s)
Reading package lists... Done
W: GPG error: https://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 6A030B21BA07F4FB
W: The repository 'https://mirrors.ustc.edu.cn/kubernetes/apt kubernetes-xenial InRelease' is not signed.
N: Data from such a repository can't be authenticated and is therefore potentially dangerous to use.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

刚添加后基本会报这个GPG error.

#### 添加GPG公钥

```
gpg --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 
gpg --export --armor E084DAB9 | sudo apt-key add - 
```

E084DAB9 是提示的NO_PUBLICKEY公匙的后八位

timeout 问题：

```
gpg --keyserver keyserver.ubuntu.com --recv-keys 94558F59
gpg: requesting key 94558F59 from hkp server keyserver.ubuntu.com
gpg: keyserver timed out
gpg: keyserver receive failed: keyserver error
```

这通常是由防火墙阻止端口`11371`引起的。您可以取消阻止防火墙中的端口。如果您无法访问防火墙，您可以：

强制它使用端口`80`而不是`11371`

```
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 94558F59
```

解决：

```
root@VM:~/k8s# gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys BA07F4FB
gpg: requesting key BA07F4FB from hkp server keyserver.ubuntu.com
gpg: /root/.gnupg/trustdb.gpg: trustdb created
gpg: key BA07F4FB: public key "Google Cloud Packages Automatic Signing Key <gc-team@google.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
root@VMu:~/k8s# gpg --export --armor BA07F4FB | sudo apt-key add -
OK
```

再次 apt-get update



### apt 使用代理

vim /etc/apt/apt.conf.d/proxy.conf（没有可以建立）

```
Acquire::http::proxy "http://192.168.59.241:8888/";
Acquire::https::proxy "http://192.168.59.241:8888/";
```

及时配置上方的bashrc 中的代理也要单独配置apt的代理，不然在apt update会提示：` Cannot initiate the connection to archive.ubuntu.com:80`

这里我也是将s去掉，坑。

**取消代理，很多时候把文件注释或者改名都没有停止掉代理，我们可以直接在配置文件里明确停止掉**：

`Acquire::http::Proxy "false";`



### 其他问题

####  配置镜像源  && update 时 的 404 问题

``` sh
root@node201:~/ids/suricata-5.0.3# apt-get update
Hit:1 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial InRelease
Ign:2 http://archive.ubuntu.com/ubuntu disco InRelease
Ign:3 http://archive.ubuntu.com/ubuntu disco-updates InRelease
Ign:4 http://archive.ubuntu.com/ubuntu disco-backports InRelease
Ign:5 http://archive.ubuntu.com/ubuntu disco-security InRelease
Err:6 http://archive.ubuntu.com/ubuntu disco Release
  404  Not Found [IP: 192.168.59.241 8888]
Err:7 http://archive.ubuntu.com/ubuntu disco-updates Release
  404  Not Found [IP: 192.168.59.241 8888]
Err:8 http://archive.ubuntu.com/ubuntu disco-backports Release
  404  Not Found [IP: 192.168.59.241 8888]
Err:9 http://archive.ubuntu.com/ubuntu disco-security Release
  404  Not Found [IP: 192.168.59.241 8888]
Reading package lists... Done
E: The repository 'http://archive.ubuntu.com/ubuntu disco Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
E: The repository 'http://archive.ubuntu.com/ubuntu disco-updates Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
E: The repository 'http://archive.ubuntu.com/ubuntu disco-backports Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
E: The repository 'http://archive.ubuntu.com/ubuntu disco-security Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

```

软件源服务器地址可以在/etc/apt/sources.list里面看到。

一般上面这样是连接到 http://archive.ubuntu.com/ubuntu 404， 我们可以把源换成阿里云的：

``` sh
mv sources.list sources.list.origin
vim sources.list

deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse


apt-get update -y
apt-get upgrade -y # 看需要
```



**如果系统版本比较新，推荐其他方式：**

其他解决方式：

You need to update your repository targets to the Eoan Ermine (19.10) release of Ubuntu. This can be done like so:

```sh
sudo sed -i -e 's|disco|eoan|g' /etc/apt/sources.list
rm -r /var/lib/apt/lists/*
sudo apt update
```

我们使用的是ubuntu 18 版本， 这里大致是换到了19的源。

参考：

https://stackoverflow.com/questions/53800051/repository-does-not-have-a-release-file-error

https://stackoverflow.com/questions/53800051/repository-does-not-have-a-release-file-error



#### 包依赖 && aptitude

比如18.04 替换阿里云的镜像源后后，安装有的软件，由于阿里云版本老， 会出现这种情况：

```
The following packages have unmet dependencies:
 libcap-ng-dev : Depends: libcap-ng0 (= 0.7.7-3.1) but 0.7.9-2 is to be installed
 libmagic-dev : Depends: libmagic1 (= 1:5.32-2ubuntu0.4) but 1:5.35-4ubuntu0.1 is to be installed
 libpcap-dev : Depends: libpcap0.8-dev but it is not going to be installed
 libpcre3-dbg : Depends: libpcre3 (= 2:8.39-9) but 2:8.39-12 is to be installed
 libpcre3-dev : Depends: libpcre3 (= 2:8.39-9) but 2:8.39-12 is to be installed
```

如果安装几个包出现这种，我们可以使用 aptitude 来修复， 它代替 apt-get 命令，先安装它：

```sh
apt-get install aptitude

# 使用 aptitude 代替 apt-get 去安装：
aptitude install PACKAGENAME

# 如果还不行，尝试 删除：
rm /var/lib/apt/lists/lock
rm /var/cache/apt/archives/lock
```

参考：https://askubuntu.com/questions/1032126/upgraded-to-18-04-and-now-have-many-broken-packages-and-unmet-dependencies

如果安装的包太多，还是放弃这种修复方式，放弃阿里源