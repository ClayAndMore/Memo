Tags:[网络协议]

<http://www.ruanyifeng.com/blog/2016/06/dns.html>



### 查询过程

dig 命令：`yum install bind-utils`



```bash

[root@192.168.18.198 ~]#dig math.stackexchange.com

# 参数和统计
; <<>> DiG 9.9.4-RedHat-9.9.4-73.el7_6 <<>> math.stackexchange.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63259
;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 1

# 查询内容， A为Adress缩写
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;math.stackexchange.com.                IN      A

# DNS服务器的答复， 60是TTL值（Time to live 的缩写），表示缓存时间，即60秒之内不用重新查询
;; ANSWER SECTION:
math.stackexchange.com. 60      IN      A       151.101.1.69
math.stackexchange.com. 60      IN      A       151.101.65.69
math.stackexchange.com. 60      IN      A       151.101.129.69
math.stackexchange.com. 60      IN      A       151.101.193.69

# DNS服务器是10.250.171.2，查询端口是53（DNS服务器的默认端口），
;; Query time: 4 msec
;; SERVER: 10.250.171.2#53(10.250.171.2)
;; WHEN: Mon May 20 10:26:39 CST 2019
;; MSG SIZE  rcvd: 115

```

short 参数：

```
[root@192.168.18.198 ~]#dig +short math.stackexchange.com
151.101.1.69
151.101.65.69
151.101.129.69
151.101.193.69
```

只返回`math.stackexchange.com`对应的4个IP地址



### DNS 服务器

本机一定要知道DNS服务器的IP地址，否则上不了网。通过DNS服务器，才能知道某个域名的IP地址到底是什么。

DNS服务器的IP地址，有可能是动态的，每次上网时由网关分配，这叫做DHCP机制；

也有可能是事先指定的固定地址。

Linux系统里面，DNS服务器的IP地址保存在`/etc/resolv.conf`文件。

上例的DNS服务器是`192.168.1.253`，这是一个内网地址。有一些公网的DNS服务器，也可以使用，其中最有名的就是Google的[`8.8.8.8`](https://developers.google.com/speed/public-dns/)和Level 3的[`4.2.2.2`](https://www.tummy.com/articles/famous-dns-server/)。

本机只向自己的DNS服务器查询，`dig`命令有一个`@`参数，显示向其他DNS服务器查询的结果。

```bash
$ dig @4.2.2.2 math.stackexchange.com
```

上面命令指定向DNS服务器`4.2.2.2`查询。



### 域名层级

`www.example.com`真正的域名是`www.example.com.root`，简写为`www.example.com.`。

因为，根域名`.root`对于所有域名都是一样的，所以平时是省略的。

根域名的下一级，叫做"顶级域名"（top-level domain，缩写为TLD），比如`.com`、`.net`；

再下一级叫做"次级域名"（second-level domain，缩写为SLD），比如`www.example.com`里面的`.example`，这一级域名是用户可以注册的；再下一级是主机名（host），比如`www.example.com`里面的`www`，又称为"三级域名"，这是用户在自己的域里面为服务器分配的名称，**是用户可以任意分配的。**

总结一下，域名的层级结构如下。

> ```bash
> 主机名.次级域名.顶级域名.根域名
> # 即
> host.sld.tld.root
> ```



### 根域名服务器和分级查询

每一级域名都有自己的NS记录，NS记录是指向该级域名的域名服务器。

这些服务器知道下一级域名的各种记录。

所谓"分级查询"，就是从根域名开始，依次查询每一级域名的NS记录，直到查到最终的IP地址。



但是我们的域名服务器怎么知道根域名服务器?

"根域名服务器"的NS记录和IP地址一般是不会变化的，所以内置在DNS服务器里面。

世界上一共有十三组根域名服务器:

```
[root@192.168.18.198 ~]#dig +trace math.stackexchange.com

; <<>> DiG 9.9.4-RedHat-9.9.4-73.el7_6 <<>> +trace math.stackexchange.com
;; global options: +cmd
.                       518400  IN      NS      l.root-servers.net.
.                       518400  IN      NS      m.root-servers.net.
.                       518400  IN      NS      a.root-servers.net.
.                       518400  IN      NS      b.root-servers.net.
.                       518400  IN      NS      c.root-servers.net.
.                       518400  IN      NS      d.root-servers.net.
.                       518400  IN      NS      e.root-servers.net.
.                       518400  IN      NS      f.root-servers.net.
.                       518400  IN      NS      g.root-servers.net.
.                       518400  IN      NS      h.root-servers.net.
.                       518400  IN      NS      i.root-servers.net.
.                       518400  IN      NS      j.root-servers.net.
.                       518400  IN      NS      k.root-servers.net.
;; Received 811 bytes from 10.250.171.2#53(10.250.171.2) in 15 ms

com.                    172800  IN      NS      a.gtld-servers.net.
com.                    172800  IN      NS      b.gtld-servers.net.
com.                    172800  IN      NS      c.gtld-servers.net.
com.                    172800  IN      NS      d.gtld-servers.net.
com.                    172800  IN      NS      e.gtld-servers.net.
com.                    172800  IN      NS      f.gtld-servers.net.
com.                    172800  IN      NS      g.gtld-servers.net.
com.                    172800  IN      NS      h.gtld-servers.net.
com.                    172800  IN      NS      i.gtld-servers.net.
com.                    172800  IN      NS      j.gtld-servers.net.
com.                    172800  IN      NS      k.gtld-servers.net.
com.                    172800  IN      NS      l.gtld-servers.net.
com.                    172800  IN      NS      m.gtld-servers.net.
com.                    86400   IN      DS      30909 8 2 E2D3C916F6DEEAC73294E8268FB5885044A833FC5459588F4A9184CF C41A5766
com.                    86400   IN      RRSIG  
```

根据内置的根域名服务器IP地址，DNS服务器向所有这些IP地址发出查询请求，询问`math.stackexchange.com`的顶级域名服务器`com.`的NS记录。**最先回复的根域名服务器将被缓存，以后只向这台服务器发请求。**



接着上面的后续输出：

```
;; Received 1185 bytes from 192.5.5.241#53(f.root-servers.net) in 453 ms

stackexchange.com.      172800  IN      NS      ns-925.awsdns-51.net.
stackexchange.com.      172800  IN      NS      ns-1029.awsdns-00.org.
stackexchange.com.      172800  IN      NS      ns-cloud-d1.googledomains.com.
stackexchange.com.      172800  IN      NS      ns-cloud-d2.googledomains.com.
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 86400 IN NSEC3 1 1 0 - CK0Q1GIN43N1ARRC9OSM6QPQR81H5M9A NS SOA RRSIG DNSKEY NSEC3PARAM
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 86400 IN RRSIG NSEC3 8 2 86400 20190523044653 20190516033653 3800 com. iapscrQtwpoWzYY0r6yAoNAwHS0EgQ6mHwD+t0bfd0vrbm7bj3HMv0v3 kdRev1ZlkYsKVFtN+b26ctoM1rYSxmEFymRzEz5VZ+Ieu61iiO0RqaDp VRcsCMSrtsnfseMJQtswImnpIOZr8cA13DbvaR8QIKtmpdhghr/fDd5B o3Q=
4OTJBPMM3103AJD1H5IULI2BU3A4BU6A.com. 86400 IN NSEC3 1 1 0 - 4OTJIH269ACIOQ0PK2FM1V02VU0DTN0U NS DS RRSIG
4OTJBPMM3103AJD1H5IULI2BU3A4BU6A.com. 86400 IN RRSIG NSEC3 8 2 86400 20190524042609 20190517031609 3800 com. XtZLIic9dGrYYAq+rvt7BeFtPPxDpNJFdzWrVTyafAZbcl4iQZ52OnjL 7oLnnECWkSz8e89rHudY8BYvr1EeiwP4CPCWTtyt4bB/C7wx5zCVloLb 9JYwleufGbctUfoJq2MDaj9uD9MyRmEDPdVTPTaDka4Vr9s4/s340gYD jmo=
;; Received 759 bytes from 192.52.178.30#53(k.gtld-servers.net) in 738 ms

math.stackexchange.com. 300     IN      A       151.101.193.69
math.stackexchange.com. 300     IN      A       151.101.129.69
math.stackexchange.com. 300     IN      A       151.101.1.69
math.stackexchange.com. 300     IN      A       151.101.65.69
stackexchange.com.      172800  IN      NS      ns-1029.awsdns-00.org.
stackexchange.com.      172800  IN      NS      ns-925.awsdns-51.net.
stackexchange.com.      172800  IN      NS      ns-cloud-d1.googledomains.com.
stackexchange.com.      172800  IN      NS      ns-cloud-d2.googledomains.com.
;; Received 250 bytes from 205.251.196.5#53(ns-1029.awsdns-00.org) in 380 ms
```

* 显示`.com`域名的13条NS记录，
* DNS服务器向这些顶级域名服务器发出查询请求，询问`math.stackexchange.com`的次级域名`stackexchange.com`的NS记录。
* 显示`stackexchange.com`有四条NS记录，同时返回的还有每一条NS记录对应的IP地址。
* DNS服务器向上面这四台NS服务器查询`math.stackexchange.com`的主机名。
* `math.stackexchange.com`有4条`A`记录，即这四个IP地址都可以访问到网站。
* 最先返回结果的NS服务器是`ns-1029.awsdns-00.org`，IP地址为`205.251.196.5`。





### 其他DNS命令



#### host

`host`命令可以看作`dig`命令的简化版本，返回当前请求域名的各种记录。

> ```bash
> $ host github.com
> 
> github.com has address 192.30.252.121
> github.com mail is handled by 5 ALT2.ASPMX.L.GOOGLE.COM.
> github.com mail is handled by 10 ALT4.ASPMX.L.GOOGLE.COM.
> github.com mail is handled by 10 ALT3.ASPMX.L.GOOGLE.COM.
> github.com mail is handled by 5 ALT1.ASPMX.L.GOOGLE.COM.
> github.com mail is handled by 1 ASPMX.L.GOOGLE.COM.
> 
> $ host facebook.github.com
> 
> facebook.github.com is an alias for github.map.fastly.net.
> github.map.fastly.net has address 103.245.222.133
> ```

`host`命令也可以用于逆向查询，即从IP地址查询域名，等同于`dig -x <ip>`。

> ```bash
> $ host 192.30.252.153
> 
> 153.252.30.192.in-addr.arpa domain name pointer pages.github.com.
> ```



#### whois

`whois`命令用来查看域名的注册情况。

`$ whois github.com`



