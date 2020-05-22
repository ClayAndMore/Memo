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



### 查看网关

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





#### 使用netplan 配置ip 和 dns

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

netplan apply后，会自动重启systemd-resolved.service
该服务会将DNS服务的IP写在/run/systemd/resolve/resolv.conf文件中。



#### ubuntu 18.04+ 

在Ubuntu18.04+版本中，DNS由`systemd`全面接管，接口监听在`127.0.0.53:53`，配置文件在`/etc/systemd/resolved.conf`中。

有时候会导致无法解析域名的问题，可使用如下2种方式来解决：

1.最简单的就是关闭systemd-resolvd服务

```bash
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
```

然后手动修改`/etc/resolv.conf`文件就可以了。

2.更加推荐的做法是修改systemd-resolv的设置：

```bash
sudo vim /etc/systemd/resolved.conf

# 修改为如下
[Resolve]
DNS=1.1.1.1 1.0.0.1
#FallbackDNS=
#Domains=
LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
#DNSStubListener=yes
```

**DNS=**设置的是域名解析服务器的IP地址，这里分别设为1.1.1.1和1.0.0.1
**LLMNR=**设置的是禁止运行LLMNR(Link-Local Multicast Name Resolution)，否则systemd-resolve会监听5535端口。



### 修改hostname

```sh
1. hostnamectl set-hostname newhostname
2. /etc/hosts
3. /etc/cloud/cloud.cfg # 如果有，将 preserve_hostname 改为 true
4. bash

使用 hostnamectl 查看当前的hostname
```



