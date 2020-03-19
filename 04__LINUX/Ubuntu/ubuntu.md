Tags:[linux]

### uwf

默认安装

```bash
# 1. 启用
ufw enable
# 2. 开启/禁用
sudo ufw allow|deny [service]

sudo ufw allow smtp　允许所有的外部IP访问本机的25/tcp (smtp)端口

sudo ufw allow 22/tcp 允许所有的外部IP访问本机的22/tcp (ssh)端口

sudo ufw allow 53 允许外部访问53端口(tcp/udp)

sudo ufw allow from 192.168.1.100 允许此IP访问所有的本机端口

sudo ufw allow proto udp 192.168.0.1 port 53 to 192.168.0.2 port 53

sudo ufw deny smtp 禁止外部访问smtp服务

sudo ufw delete allow smtp 删除上面建立的某条规则

# 防火墙状态
ufw status
```



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



### 添加root用户

新装的ubuntu主机是没有root账户的，
需要我们手动添加：`passwd root`
sudo passwd root



### 允许root登陆

**sudo vim /etc/ssh/sshd_config**后进入配置文件中修改**PermitRootLogin**后的默认值为**yes**

重启 sshd



### 安装gcc

sudo apt update

sudo apt install build-essential

gcc --version



### 配置ip, dns

查看网关：netstat -rn` 或 `route -n

```
root@: netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         172.19.19.254   0.0.0.0         UG        0 0          0 ens160
172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
172.19.19.0     0.0.0.0         255.255.255.0   U         0 0          0 ens160
172.20.0.0      0.0.0.0         255.255.0.0     U         0 0          0 br-c9e6e96e0382
root@: route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.19.19.254   0.0.0.0         UG    0      0        0 ens160
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
172.19.19.0     0.0.0.0         255.255.255.0   U     0      0        0 ens160
172.20.0.0      0.0.0.0         255.255.0.0     U     0      0        0 br-c9e6e96e0382
```





#### 使用netplan

`Netplan` 是 Ubuntu 17.10 中引入的一种新的命令行网络配置实用程序，用于在 Ubuntu 系统中轻松管理和配置网络设置。 它允许您使用 `YAML` 格式的描述文件来抽像化定义网络接口的相关信息。

`Netplan` 可以使用 `NetworkManager` 或 `Systemd-networkd` 的网络守护程序来做为内核的接口。`Netplan` 的默认描述文件在 `/etc/netplan/*.yaml` 里，`Netplan` 描述文件采用了 `YAML` 语法。

在 Ubuntu 18.04 中如果再通过原来的 `ifupdown` 工具包继续在 `/etc/network/interfaces` 文件里配置管理网络接口是无效的。

改一下默认的配置文件：vim /etc/netplan/50-cloud-init.yaml

```yaml
network:
    renderer: NetworkManager
    ethernets:
        enp0s31f6:
            addresses:[210.72.92.28/24] # IP及掩码
            gateway4: 210.72.92.254 # 网关
            dhcp4: false
            optional: true
            nameservers:
                addresses: [192.168.18.2, 114.114.114.114] #dns
    version: 2
```

把DNS和ipv4地址配置在一个文件里了，不用再修改/etc/resolv.conf 文件。

重启网络服务使配置生效

```cpp
sudo netplan apply
```

https://www.hi-linux.com/posts/49513.html



