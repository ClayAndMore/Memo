### apt-get

通过apt-get安装制定版本：

`apt-get install <<package name>>=<<version>>`



### apt-chache

列举版本列表：

0、通过网站搜索：https://packages.[ubuntu](https://www.centos.bz/tag/ubuntu/).com/

1、

```
apt-cache madison <<package name>>
```

将列出所有来源的版本。如下输出所示：

[apt-cache](https://www.centos.bz/tag/apt-cache/) madison vim
vim | 2:7.3.547-1 | http://[debian](https://www.centos.bz/tag/debian/).mirrors.tds.net/debian/ unstable/main amd64 Packages
vim | 2:7.3.429-2 | http://debian.mirrors.tds.net/debian/ testing/main amd64 Packages
vim | 2:7.3.429-2 | http://http.us.debian.org/debian/ testing/main amd64 Packages
vim | 2:7.3.429-2 | http://debian.mirrors.tds.net/debian/ testing/main Sources
vim | 2:7.3.547-1 | http://debian.mirrors.tds.net/debian/ unstable/main Sources
madison是一个apt-cache子命令，可以通过man apt-cache查询更多用法。

2、

```
apt-cache policy <<package name>>
```

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

