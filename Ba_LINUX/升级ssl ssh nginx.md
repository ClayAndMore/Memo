Tags:[linux, linux_software]

### 前提

* 安装Zlib ` yum install zlib-devel -y`

  Zlib用于提供压缩和解压缩功能。操作系统已经自带了zlib，版本也符合要求。实际上，openssl和openssh都依赖于zlib。

* 安装PAM ` yum install pam-devel -y`

  PAM(Pluggable Authentication Modules，可插拔认证模块)用于提供安全控制。操作系统也已经自带了PAM，版本也是可以的。

* 安装tcp_wrappers `yum install tcp_wrappers-devel -y`

  tcp_wrappers是一种安全工具，通常，我们在/etc/hosts.allow或/etc/hosts.deny文件中配置的过滤规则就是使用的tcp_wrappers的功能了。openssh在编译时的确是可以选择支持tcp_wrappers的，但我不知道为什么它的安装要求里面没有体现。操作系统自带的tcp_wrappers的版本是可以的。



### telnet

telnet命令通常用来远程登录。telnet程序是基于TELNET协议的远程登录客户端程序。Telnet协议是TCP/IP协议族中的一员，是Internet远程登陆服务的标准协议和主要方式。它为用户提供了在本地计算机上完成远程主机工作的 能力。在终端使用者的电脑上使用telnet程序，用它连接到服务器。终端使用者可以在telnet程序中输入命令，这些命令会在服务器上运行，就像直接在服务器的控制台上输入一样。可以在本地就能控制服务器。要开始一个 telnet会话，必须输入用户名和密码来登录服务器。Telnet是常用的远程控制Web服务器的方法。

但是，telnet因为采用明文传送报文，安全性不好，很多Linux服务器都不开放telnet服务，而改用更安全的ssh方式了。但仍然有很多别的系统可能采用了telnet方式来提供远程登录，因此弄清楚telnet客户端的使用方式仍是很有必要的。

telnet命令还可做别的用途，比如确定远程服务的状态，比如确定远程服务器的某个端口是否能访问。

#### 安装和配置

yum install -y  telnet-server telnet

```bash
vi /etc/xinetd.d/telnet， disable -> no

vi /etc/xinetd.conf

enabled = telnet

chkconfig --list telnet

telnet off

chkconfig telnet on

chkconfig --list telnet

telnet on

# service xinetd restart
Stopping xinetd:                                           [  OK  ]
Starting xinetd:                                           [  OK  ]
```

eg:

```bash
# telnet 192.168.10.10
Trying 192.168.10.10...
Connected to 192.168.10.10
Escape character is '^]'.
[snip]
login: user
Password:
Last login: Sat Nov  2 14:46:57 from 172.168.21.21
```

最好用非root用户登录，默认root用户是不允许的。

` mv /etc/securetty /etc/securetty.old `允许root用户通过telnet登录

eg:

```bash
测试域名：
# telnet baidu.com 80
Trying 123.125.114.144...
Connected to baidu.com (123.125.114.144).         #==>出现Connected表示连通了，说
明百度的80端口开放的
Escape character is '^]'.             #==>按“ctrl+]”退出此地。
^]
telnet> quit
Connection closed.
```

可以用这种方式来测试端口



发现无法连接的话，请关闭防火墙

```
# servcie iptables stop 

# chkconfig iptables off 
```



#### 升级后关闭telnet

```
mv /etc/securetty.old /etc/securetty 

chkconfig xinetd off 

service xinetd stop

# servcie iptables stop 

# chkconfig iptables off 
```



### 升级openssl

安装：[https://www.linuxhelp.com/how-to-install-and-update-openssl-on-centos-6-centos-7](https://www.linuxhelp.com/how-to-install-and-update-openssl-on-centos-6-centos-7)

下载官网：https://www.openssl.org/source/

下载最好通过`curl -O -L `

后续脚本：

```bash
#!/bin/bash

#cd
echo "OpenSSL Origin version: " && openssl version

set -x

timestamp=$(date +%Y_%m_%d_%T)

mv /usr/bin/openssl /usr/bin/openssl-${timestamp}
mv /usr/include/openssl /usr/include/openssl-${timestamp}
mv /usr/lib64/openssl/engines /usr/lib64/openssl/engines-${timestamp}
mv /usr/lib64/openssl /usr/lib64/openssl-${timestamp}

mv /usr/lib/libssl.so.1.0.1e  /usr/lib/libssl.so.1.0.1e.${timestamp}
mv /usr/lib/libcrypto.so.1.0.1e  /usr/lib/libcrypto.so.1.0.1e.${timestamp}

./config --prefix=/opt/openssl --openssldir=/opt/openssl -fPIC  shared 
#./config --prefix=/usr/local/openssl --openssldir=/etc/ssl --shared zlib&& make && make test && make install

ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
ln -s /usr/local/openssl/include/openssl /usr/include/openssl

echo "OpenSSl version upgrades as to lastest:" && openssl version
```

prefix 和 oenpssldir 最好在一个目录，为后来编译openssh做准备。



#### 问题

```
1. rc4test.c:(.text 0x30): undefined reference to `OPENSSL_cpuid_setup'

export CFLAGS=-fPIC, 或者尝试： ./config -fPIC -DOPENSSL_PIC


2.libcrypto.a(e_4758cca.o): could not read symbols: Bad value
./config shard 
make clean 
```





### 升级openssh

官网下载源码包：https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/

```
export LD_LIBRARY_PATH=/opt/openssl1.0.2r/lib
./configure CFLAGS="-I/opt/openssl1.0.2r/include" --prefix=/opt/ssh --with-ldflags="-L/opt/openssl1.0.2r/lib"
```

用openssl 编译, [链接](<https://stackoverflow.com/questions/39270697/openssh-7-3p1-building-configure-only-finds-an-old-version-of-openssl-libraries>)  

成功：

```
[root@localhost openssh-8.0p1]# /opt/ssh/sbin/sshd -V
unknown option -- V
OpenSSH_8.0p1, OpenSSL 1.0.2r  26 Feb 2019
usage: sshd [-46DdeiqTt] [-C connection_spec] [-c host_cert_file]
            [-E log_file] [-f config_file] [-g login_grace_time]
            [-h host_key_file] [-o option] [-p port] [-u len]
```



#### 问题

```
checking whether OpenSSL's headers match the library... no
configure: error: Your OpenSSL headers do not match your
    library. Check config.log for details.
    If you are sure your installation is consistent, you can disable the check
    by running "./configure --without-openssl-header-check".
    Also see contrib/findssl.sh for help identifying header/library mismatches.
```

缺少openssl-devel所致，只需安装openssl-devel即可，执行命令：yum install openssl-devel

`error while loading shared libraries: libcrypto.so.10: cannot open shared object file: No such file or directory`

软链接/usr/lib64/libcrypto.so.10不存在
解决方法：`ln -s /usr/lib64/libcrypto.so.1.0.0 /usr/lib64/libcrypto.so.10`，或者是 ln -s /usr/local/openssl/lib/libcrypto.so.1.0.0 /usr/lib64/libcrypto.so.10（根据openssl的实际安装路径来决定）

 **取消软连接  unlink**



--with-ssl-dir=



### 升级 nginx

`./configure --prefix=/opt/nginx/ --with-http_ssl_module --with-openssl=/root/auto_update_ssh/openssl-1.0.2r`

记得指定ssl源码目录。

#### 问题

```
nginx: [emerg] unknown directive "ssl" in

 没有加--with-httpssl_module

./configure: error: the HTTP rewrite module requires the PCRE library.
yum -y install pcre-devel
yum -y install openssl-devel
```





### 参考

https://docs.junyangz.com/upgrade-openssh-to-7.7p1-in-centos-6

https://blog.51cto.com/lajifeiwomoshu/2163927

https://blog.51cto.com/techsnail/2138927
