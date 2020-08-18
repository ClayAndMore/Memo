---
title: "suricata 控制 kvm.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: false
tags: ["suricata"]
categories: ["监控服务"]
author: "Claymore"

---
### 环境

环境： derbian 10,
kvm:

```
root@debian-wy:~# virsh list
 Id   Name       State
--------------------------
 2    Alpine     running
 3    Alpine-2   running
```
sricata规则：
```
root@debian-wy:~# cat /etc/suricata/rules/topsec.rules
drop tcp any any -> any any (msg:"TTTTTTTTTTTT"; content:"GET";http_method;  sid:5445555; rev:1;)
```
从任意源到任意目的的get 方法的 http流量 drop 掉。

suricata 配置：
```yaml
utputs:
  # a line based alerts log similar to Snort's fast.log
  - fast:
      enabled: yes
      filename: fast.log
      append: yes

  - eve-log:
      enabled: yes
      filetype: unix_stream
      filename: /tmp/suricata-stats.sock
      xff:
        enabled: yes
        mode: extra-data
        deployment: reverse
        header: X-Forwarded-For

      types:
        - alert:
           payload: yes             # enable dumping payload in Base64
           payload-buffer-size: 4kb # max size of payload buffer to output in eve-log
           payload-printable: yes   # enable dumping payload in printable (lossy) format
           # packet: yes              # enable dumping of packet (without stream segments)
           http-body: yes           # enable dumping of http body in Base64
           http-body-printable: yes # enable dumping of http body in printable format
           tagged-packets: yes

        - http:
           extended: yes
           custom: [Accept-Encoding, Accept-Language, Authorization, Forwarded, From, Referer, Via] 
```
只保留了 http 和 alert 事件。


### 监控virbr0

suricata -c /etc/suricata/suricata.yaml -i virbr0

在一个虚拟机上监听服务：
```
# virsh console 2
# ip r
default via 192.168.122.1 dev eth0  metric 202
192.168.122.0/24 dev eth0 scope link  src 192.168.122.200
# python -m SimpleHTTPServer 9999
Serving HTTP on 0.0.0.0 port 9999 ...

```

进入另一个虚拟机，发起请求：
```
# virsh console 3
# ip r
default via 192.168.122.1 dev eth0  metric 202
# wget 192.168.122.200:9999
Connecting to 192.168.122.200:9999 (192.168.122.200:9999)
wget: can't open 'index.html': File exists

```


eve.log:
```
{"timestamp":"2020-06-15T10:16:53.051373+0800","flow_id":1598066500414523,"in_iface":"virbr0","event_type":"alert","src_ip":"192.168.122.193","src_port":41426,"dest_ip":"192.168.122.200","dest_port":9999,"proto":"TCP","tx_id":0,"alert":{"action":"allowed","gid":1,"signature_id":5445555,"rev":1,"signature":"TTTTTTTTTTTT","category":"","severity":3},"http":{"hostname":"192.168.122.200","http_port":9999,"url":"\/","http_user_agent":"Wget","http_method":"GET","protocol":"HTTP\/1.1","status":200,"length":0},"app_proto":"http","flow":{"pkts_toserver":4,"pkts_toclient":4,"bytes_toserver":355,"bytes_toclient":649,"start":"2020-06-15T10:16:53.044091+0800"},"payload":"R0VUIC8gSFRUUC8xLjENCkhvc3Q6IDE5Mi4xNjguMTIyLjIwMDo5OTk5DQpVc2VyLUFnZW50OiBXZ2V0DQpDb25uZWN0aW9uOiBjbG9zZQ0KDQo=","payload_printable":"GET \/ HTTP\/1.1\r\nHost: 192.168.122.200:9999\r\nUser-Agent: Wget\r\nConnection: close\r\n\r\n","stream":1}
{"timestamp":"2020-06-15T10:16:53.052013+0800","flow_id":1598066500414523,"in_iface":"virbr0","event_type":"http","src_ip":"192.168.122.193","src_port":41426,"dest_ip":"192.168.122.200","dest_port":9999,"proto":"TCP","tx_id":0,"http":{"hostname":"192.168.122.200","http_port":9999,"url":"\/","http_user_agent":"Wget","http_content_type":"text\/html","http_method":"GET","protocol":"HTTP\/1.1","status":200,"length":222}}

```
ids 模式下可以监控到虚拟机之间的流量。


### ips 模式 虚拟机间相互访问

`iptables -I FORWARD -j NFQUEUE --queue-num 0`

`suricata -c /etc/suricata/suricata.yaml -q 0`


尝试几种转发：
```
iptables -I FORWARD -i virbr0 -o virbr0 -j NFQUEUE
iptables -I FORWARD -i ens160 -o virbr0 -j NFQUEUE
iptables -I FORWARD -i virbr0 -o ens160 -j NFQUEUE
````
ips模式下均没有日志呈现。


### ips 模式 虚拟机访问外网。
我们配置 虚拟网卡 和 主机网卡间的规则 ：
```
iptables -I FORWARD -i ens160 -o virbr0 -j NFQUEUE
iptables -I FORWARD -i virbr0 -o ens160 -j NFQUEUE
```
ips 模式启动：
`suricata -c /etc/suricata/suricata.yaml -q 0`

虚拟机访问外网：
```
# ips启动前：
# wget www.baidu.com
Connecting to 192.168.59.241:8888 (192.168.59.241:8888)
wget: can't open 'index.html': File exists

# ips 启动后：
# wget www.baidu.com
Connecting to 192.168.59.241:8888 (192.168.59.241:8888)
wget: download timed out
```

日志：
```
{
    "timestamp":"2020-06-15T11:48:44.994198+0800",
    "flow_id":885914039230876,
    "event_type":"alert",
    "src_ip":"192.168.122.193",
    "src_port":48398,
    "dest_ip":"192.168.59.241",
    "dest_port":8888,
    "proto":"TCP",
    "tx_id":0,
    "alert":{
        "action":"blocked",
        "gid":1,
        "signature_id":5445555,
        "rev":1,
        "signature":"TTTTTTTTTTTT",
        "category":"",
        "severity":3
    },
    "http":{
        "hostname":"www.baidu.com",
        "url":"http://www.baidu.com/ ",
        "http_user_agent":"Wget",
        "http_method":"GET",
        "protocol":"HTTP/1.1",
        "length":0
    },
    "app_proto":"[http](http://json.cn/http)",
    "flow":{
        "pkts_toserver":3,
        "pkts_toclient":1,
        "bytes_toserver":260,
        "bytes_toclient":60,
        "start":"2020-06-15T11:48:44.991644+0800"
    },
    "payload":"R0VUIGh0dHA6Ly93d3cuYmFpZHUuY29tLyBIVFRQLzEuMQ0KSG9zdDogd3d3LmJhaWR1LmNvbQ0KVXNlci1BZ2VudDogV2dldA0KQ29ubmVjdGlvbjogY2xvc2UNCg0K",
    "payload_printable":"GET http://www.baidu.com/ HTTP/1.1
Host: www.baidu.com
User-Agent: Wget
Connection: close
",
    "stream":1
}

{"timestamp":"2020-06-15T12:13:46.000256+0800","flow_id":885914039230876,"event_type":"http","src_ip":"192.168.122.193","src_port":48398,"dest_ip":"192.168.59.241","dest_port":8888,"proto":"TCP","tx_id":0,"http":{"hostname":"www.baidu.com","url":"http:\/\/www.baidu.com\/","http_user_agent":"Wget","http_method":"GET","protocol":"HTTP\/1.1","length":0}}

```
可以看到 alert 事件中 action 已经 blocked。
在不代理的情况下访问其他主机服务也被阻断：
```
localhost:~# wget 172.19.19.16:9999 -Y off
Connecting to 172.19.19.16:9999 (172.19.19.16:9999）
wget: download timed out
```


### kvm 网络模式
通过 ` virsh edit Alpine`  我们找到：

![图片描述](/tfl/captures/2020-06/tapd_33000826_base64_1592202604_82.png)

可以看出网络模式为 bridge.

![图片描述](/tfl/captures/2020-06/tapd_33000826_base64_1592202807_6.png)

虚拟网桥（Virtual Bridge）：这网络模式下客户机与宿主机处于同一网络环境，类似于一台真实的宿主机，直接访问网络资源，设置好后客户机与互联网，客户机与主机之间的通信都很容易。

即客户机通过网桥连接到宿主机网络环境中，可以使客户机成为网络中具有独立IP的主机

网桥的基本原理就是创建一个桥接接口，并把物理主机的eth0绑定到网桥上，客户机的网络模式需要配置为桥接模式
 __这是生产上使用较多的一种模式，到这里我们也能够明白为什么配置 ens160 和 vribr0 的规则后，ips可以生效的原因，但是 虚拟机直接的访问控制还没有解决__



### 尝试修改 iptables

原：
```
root@debian-wy:~# iptables -L -n -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
RETURN     all  --  192.168.122.0/24     224.0.0.0/24
RETURN     all  --  192.168.122.0/24     255.255.255.255
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

```

尝试各种链转发到nfq 0:
```
iptables -t nat -A PREROUTING -d 192.168.122.0/24 -j NFQUEUE
iptables -t nat -A POSTROUTING -d 192.168.122.0/24 -j NFQUEUE
iptables -t nat -I POSTROUTING -d 192.168.122.0/24 -j NFQUEUE
iptables -t nat -I POSTROUTING -s 192.168.122.0/24 -d 192.168.122.0/24 -j NFQUEUE
iptables -t nat -I OUTPUT -s 192.168.122.0/24 -d 192.168.122.0/24 -j NFQUEUE
iptables -t nat -I INPUT -s 192.168.122.0/24 -d 192.168.122.0/24 -j NFQUEUE
```
修改后的nat表：
```
root@debian-wy:~# iptables -L -n -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
NFQUEUE    all  --  0.0.0.0/0            192.168.122.0/24     NFQUEUE num 0

Chain INPUT (policy ACCEPT)
target     prot opt source               destination
NFQUEUE    all  --  192.168.122.0/24     192.168.122.0/24     NFQUEUE num 0

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
NFQUEUE    all  --  192.168.122.0/24     192.168.122.0/24     NFQUEUE num 0
NFQUEUE    all  --  0.0.0.0/0            192.168.122.0/24     NFQUEUE num 0
RETURN     all  --  192.168.122.0/24     224.0.0.0/24
RETURN     all  --  192.168.122.0/24     255.255.255.255
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24
NFQUEUE    all  --  0.0.0.0/0            192.168.122.0/24     NFQUEUE num 0

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
NFQUEUE    all  --  192.168.122.0/24     192.168.122.0/24     NFQUEUE num 0

```
使用suricata还是没有抓到流量。


### 解决
参考篇文章：
https://serverfault.com/questions/457262/configure-iptables-on-kvm-host-to-block-guest-bridge-traffic 

 __网桥是一个交换机，在第2层上运行。iptables规则适用于第3层。 所以我们现在主机所配的规则不会对其生效__ 

如果  __net.bridge.bridge-nf-call-iptables＝1__ 

 __也就意味着二层的网桥在转发包时也会被iptables的FORWARD规则所过滤，这样就会L3层的iptables rules去过滤L2的包__ （

我们做如下尝试：
开启 bridge-nf-call-iptables:

```sh
root@debian-wy:~# echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
-bash: /proc/sys/net/bridge/bridge-nf-call-iptables: 没有那个文件或目录
root@debian-wy:~# modprobe br_netfilter
root@debian-wy:~# echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
```
注意使用 `modprobe br_netfilter ` 开启内核的 br_netfiler 模块

forward 转发到 nfq 0:
``` 
root@debian-wy:~# iptables -I FORWARD -j NFQUEUE --queue-num 0
root@debian-wy:~# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
NFQUEUE    all  --  anywhere             anywhere             NFQUEUE num 0

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```
和之前一样，在虚拟机内部访问一台虚拟机，suricata此时抓到并阻断了流量：
```json
root@debian-wy:~# nc -l -U /tmp/suricata-stats.sock

{
    "timestamp":"2020-06-16T13:56:09.877912+0800",
    "flow_id":872964433730976,
    "event_type":"alert",
    "src_ip":"192.168.122.193",
    "src_port":41482,
    "dest_ip":"192.168.122.200",
    "dest_port":9999,
    "proto":"TCP",
    "tx_id":0,
    "alert":{
        "action":"blocked",
        "gid":1,
        "signature_id":5445555,
        "rev":1,
        "signature":"TTTTTTTTTTTT",
        "category":"",
        "severity":3
    },
    "http":{
        "hostname":"192.168.122.200",
        "http_port":9999,
        "url":"/",
        "http_user_agent":"Wget",
        "http_method":"GET",
        "protocol":"HTTP/1.1",
        "length":0
    },
    "app_proto":"[http](http://json.cn/http)",
    "flow":{
        "pkts_toserver":3,
        "pkts_toclient":1,
        "bytes_toserver":247,
        "bytes_toclient":60,
        "start":"2020-06-16T13:56:09.875936+0800"
    },
    "payload":"R0VUIC8gSFRUUC8xLjENCkhvc3Q6IDE5Mi4xNjguMTIyLjIwMDo5OTk5DQpVc2VyLUFnZW50OiBXZ2V0DQpDb25uZWN0aW9uOiBjbG9zZQ0KDQo=",
    "payload_printable":"GET / HTTP/1.1
Host: 192.168.122.200:9999
User-Agent: Wget
Connection: close
",
    "stream":1
}
```
当把drop改成 alert 时又放行了流量：
```json

{
    "timestamp":"2020-06-16T13:57:28.734465+0800",
    "flow_id":1266954673860592,
    "event_type":"alert",
    "src_ip":"192.168.122.193",
    "src_port":41488,
    "dest_ip":"192.168.122.200",
    "dest_port":9999,
    "proto":"TCP",
    "tx_id":0,
    "alert":{
        "action":"allowed",
        "gid":1,
        "signature_id":5445555,
        "rev":1,
        "signature":"TTTTTTTTTTTT",
        "category":"",
        "severity":3
    },
    "http":{
        "hostname":"192.168.122.200",
        "http_port":9999,
        "url":"/",
        "http_user_agent":"Wget",
        "http_method":"GET",
        "protocol":"HTTP/1.1",
        "length":0
    },
    "app_proto":"[http](http://json.cn/http)",
    "flow":{
        "pkts_toserver":3,
        "pkts_toclient":1,
        "bytes_toserver":247,
        "bytes_toclient":60,
        "start":"2020-06-16T13:57:28.733168+0800"
    },
    "payload":"R0VUIC8gSFRUUC8xLjENCkhvc3Q6IDE5Mi4xNjguMTIyLjIwMDo5OTk5DQpVc2VyLUFnZW50OiBXZ2V0DQpDb25uZWN0aW9uOiBjbG9zZQ0KDQo=",
    "payload_printable":"GET / HTTP/1.1
Host: 192.168.122.200:9999
User-Agent: Wget
Connection: close
",
    "stream":1
}

```





### 一些补充

#### kernel 的 nfnetlink 模块

确保内核 大于 2.6.14，切开启了 netfiter 模块

``` sh
[root@localhost ~]# lsmod | grep queue
# Module                Size  Used by
nfnetlink_queue        15825  0
nfnetlink               8634  1 nfnetlink_queue
```

suricata 占用 0 队列后：

``` sh
[root@localhost ~]# lsmod | grep queue
nfnetlink_queue        15825  1
nfnetlink               8634  2 nfnetlink_queue
```

如果lsmod 没有找到该模块，我们需要把它加载进去：

开启后内存中会有：

```
[root@localhost ~]# ls /proc/net/netfilter/
nf_log  nfnetlink_queue
```



**内核模块的开机自动加载：**

```sh
echo "nfnetlink_queue" >> /etc/modules-load.d/nfnnetlink.conf
echo "nfnetlink" >> /etc/modules-load.d/nfnnetlink.conf
echo "br_netfiler" >> /etc/modules-load.d/nfnnetlink.conf
chmod -R -x /etc/modules-load.d/
```

centos 中是这样，其他系统可能是 加到/etc/modules 里。

