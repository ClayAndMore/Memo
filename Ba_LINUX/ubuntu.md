### uwf

**ufw show added** 查看已经添加 过的规则。





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