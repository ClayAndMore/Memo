## tcpdump

网络数据包截获分析工具。支持针对网络层、协议、主机、网络或端口的过滤



### 指定网卡

tcpdump -i eth0 

tcpdump -i any # 监听所有的网卡

### 指定主机

tcpdump host 192.168.33.206

例子：监听本机跟主机`192.168.33.206`之间往来的通信包。

备注：出、入的包都会被监听。

关于类型的关键字，主要包括host，net，port

例如，
host 210.27.48.2，指明 210.27.48.2是一台主机，net 202.0.0.0 指明202.0.0.0是一个网络地址，port 23 指明端口号是23。

如果没有指定类型，缺省的类型是host.



### 指定源和目的

``` sh
# 指定源是hostname
tcpdump src host hostname
# 指定目的是hostname
tcpdump dst host hostname

# 关于传输方向的关键字:src,dst,dst or src,dst and src
src 210.27.48.2   # 指明ip包中源地址是210.27.48.2 , 
dst net 202.0.0.0 # 指明目的网络地址是202.0.0.0 。
#如果没有指明方向关键字，则缺省是src or dst关键字。

```



### 指定协议

``` sh
tcpdum tcp  # udp, icmp
tcpdump tcp and src host 123.207.116.169  # 监听源是123。。和本机的tcp流量，这里使用了and
```

### 指定端口

``` sh
tcpdump port 3000
tcpdump portrange 21-23 # 端口范围
tcpdumo dst port ! 22 # 不抓取目标端口是22的数据包
```

### 保存到文件

tcpdump默认会将输出写到缓冲区，只有缓冲区内容达到一定的大小，或者tcpdump退出时，才会将输出写到本地磁盘

```bash
tcpdump -n -vvv -c 1000 -w /tmp/tcpdump_save.cap
```

也可以加上`-U`强制立即写到本地磁盘（一般不建议，性能相对较差）



### 其他参数

``` sh
tcpdump tcp -i eth1 -t -s 0 -c 100 and dst port ! 22 and src net 192.168.1.0/24 -w ./target.cap
```

* tcp: ip icmp arp rarp 和 tcp、udp、icmp这些选项等都要放到第一个参数的位置，用来过滤数据报的类型
* -t : 不显示时间戳
* -s 0 : 抓取数据包时默认抓取长度为68字节。加上-s 0 后可以抓到完整的数据包
* -c 100 : 只抓取100个数据包
* src net 192.168.1.0/24 : 数据包的源网络地址为192.168.1.0/24

``` sh
tcpdump -nnvXSs 0 -c2 icmp -i ens160
```

- `-n` 表示不要解析域名，直接显示 ip。

- `-nn` 不要解析域名和端口

- `-X` 同时用 hex 和 ascii 显示报文的内容。

- `-XX` 同 `-X`，但同时显示以太网头部。

- `-S` 显示绝对的序列号（sequence number），而不是相对编号。

- `-v, -vv, -vvv`：显示更多的详细信息

- `-A`： 只使用 ascii 打印报文的全部数据，不要和 `-X` 一起使用。不包括链路层的头，这对分析网页来说很方便；

  截取 http 请求的时候可以用 `sudo tcpdump -nSA port 80`！

``` sh
tcpdump: listening on ens160, link-type EN10MB (Ethernet), capture size 262144 bytes

11:35:15.173880 IP (tos 0x0, ttl 64, id 45020, offset 0, flags [DF], proto ICMP (1), length 84)
    172.19.19.200 > 172.19.19.16: ICMP echo request, id 7736, seq 1, length 64
        0x0000:  4500 0054 afdc 4000 4001 0bce ac13 13c8  E..T..@.@.......
        0x0010:  ac13 1310 0800 ea9f 1e38 0001 7348 c75e  .........8..sH.^
        0x0020:  0000 0000 f3ac 0200 0000 0000 1011 1213  ................
        0x0030:  1415 1617 1819 1a1b 1c1d 1e1f 2021 2223  .............!"#
        0x0040:  2425 2627 2829 2a2b 2c2d 2e2f 3031 3233  $%&'()*+,-./0123
        0x0050:  3435 3637                                4567
11:35:15.173938 IP (tos 0x0, ttl 64, id 9926, offset 0, flags [none], proto ICMP (1), length 84)
    172.19.19.16 > 172.19.19.200: ICMP echo reply, id 7736, seq 1, length 64
        0x0000:  4500 0054 26c6 0000 4001 d4e4 ac13 1310  E..T&...@.......
        0x0010:  ac13 13c8 0000 f29f 1e38 0001 7348 c75e  .........8..sH.^
        0x0020:  0000 0000 f3ac 0200 0000 0000 1011 1213  ................
        0x0030:  1415 1617 1819 1a1b 1c1d 1e1f 2021 2223  .............!"#
        0x0040:  2425 2627 2829 2a2b 2c2d 2e2f 3031 3233  $%&'()*+,-./0123
        0x0050:  3435 3637                                4567
2 packets captured
2 packets received by filter
0 packets dropped by kernel
```



### 报文解读

``` sh
IP (tos 0x0, ttl 64, id 45646, offset 0, flags [DF], proto TCP (6), length 64)
    192.168.1.106.56166 > 124.192.132.54.80: Flags [S], cksum 0xa730 (correct), seq 992042666, win 65535, options [mss 1460,nop,wscale 4,nop,nop,TS val 663433143 ecr 0,sackOK,eol], length 0

IP (tos 0x0, ttl 51, id 0, offset 0, flags [DF], proto TCP (6), length 44)
    124.192.132.54.80 > 192.168.1.106.56166: Flags [S.], cksum 0xedc0 (correct), seq 2147006684, ack 992042667, win 14600, options [mss 1440], length 0

IP (tos 0x0, ttl 64, id 59119, offset 0, flags [DF], proto TCP (6), length 40)
    192.168.1.106.56166 > 124.192.132.54.80: Flags [.], cksum 0x3e72 (correct), ack 2147006685, win 65535, length 0
```

最基本也是最重要的信息就是数据报的源地址/端口和目的地址/端口，上面的例子第一条数据报中，源地址 ip 是 `192.168.1.106`，源端口是 `56166`，目的地址是 `124.192.132.54`，目的端口是 `80`。

 **`>` 符号代表数据的方向。**

上面的三条数据还是 tcp 协议的三次握手过程，第一条就是 `SYN` 报文，这个可以通过 `Flags [S]` 看出。下面是常见的 TCP 报文的 Flags:

- `[S]`： SYN（开始连接）
- `[.]`: 没有 Flag
- `[P]`: PSH（推送数据）
- `[F]`: FIN （结束连接）
- `[R]`: RST（重置连接）

**而第二条数据的 `[S.]` 表示 `SYN-ACK`，就是 `SYN` 报文的应答报文。**

对于下面这种：

``` sh
  0x0000:  4500 0054 26c6 0000 4001 d4e4 ac13 1310  E..T&...@.......
  0x0010:  ac13 13c8 0000 f29f 1e38 0001 7348 c75e  .........8..sH.^
```

0x000.. 是指的以16进制显示包内容， 对应的是-X,

` E..T&...@.......` 这便是 Ascii 编码输出。



#### 传输内容

我们这里做一个实验，用nc命令本地做一个监听：

shell1:

```sh
nc -l 9999 #监听本地9999端口
abcd
1234567
```

shell2:

``` sh
nc localhost 9999 # 与本地9999端口建立连接
abcd
1234567
```

abcd 和 1234567 是建立连接后发送的内容

我们通过tcpdum来看下内容：

shell3:

``` sh
tcpdump  port 9999 -i lo -vvv -X
tcpdump: listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
13:51:38.429590 IP (tos 0x2,ECT(0), ttl 64, id 53961, offset 0, flags [DF], proto TCP (6), length 57)
    localhost.localdomain.9999 > localhost.localdomain.35720: Flags [P.], cksum 0xfe2d (incorrect -> 0xf5b1), seq 1079740985:1079740990, ack 1783936537, win 342, options [nop,nop,TS val 1094043794 ecr 1093913161], length 5
        0x0000:  4502 0039 d2c9 4000 4006 69f1 7f00 0001  E..9..@.@.i.....
        0x0010:  7f00 0001 270f 8b88 405b 8a39 6a54 b619  ....'...@[.9jT..
        0x0020:  8018 0156 fe2d 0000 0101 080a 4135 c892  ...V.-......A5..
        0x0030:  4133 ca49 6162 6364 0a                   A3.Iabcd.
13:51:38.429605 IP (tos 0x0, ttl 64, id 61086, offset 0, flags [DF], proto TCP (6), length 52)
    localhost.localdomain.35720 > localhost.localdomain.9999: Flags [.], cksum 0xfe28 (incorrect -> 0xc634), seq 1, ack 5, win 342, options [nop,nop,TS val 1094043795 ecr 1094043794], length 0
        0x0000:  4500 0034 ee9e 4000 4006 4e23 7f00 0001  E..4..@.@.N#....
        0x0010:  7f00 0001 8b88 270f 6a54 b619 405b 8a3e  ......'.jT..@[.>
        0x0020:  8010 0156 fe28 0000 0101 080a 4135 c893  ...V.(......A5..
        0x0030:  4135 c892                                A5..


13:52:52.748742 IP (tos 0x2,ECT(0), ttl 64, id 53962, offset 0, flags [DF], proto TCP (6), length 60)
    localhost.localdomain.9999 > localhost.localdomain.35720: Flags [P.], cksum 0xfe30 (incorrect -> 0xd32b), seq 5:13, ack 1, win 342, options [nop,nop,TS val 1094118115 ecr 1094043795], length 8
        0x0000:  4502 003c d2ca 4000 4006 69ed 7f00 0001  E..<..@.@.i.....
        0x0010:  7f00 0001 270f 8b88 405b 8a3e 6a54 b619  ....'...@[.>jT..
        0x0020:  8018 0156 fe30 0000 0101 080a 4136 eae3  ...V.0......A6..
        0x0030:  4135 c893 3132 3334 3536 370a            A5..1234567.
13:52:52.748755 IP (tos 0x0, ttl 64, id 61087, offset 0, flags [DF], proto TCP (6), length 52)
    localhost.localdomain.35720 > localhost.localdomain.9999: Flags [.], cksum 0xfe28 (incorrect -> 0x8189), seq 1, ack 13, win 342, options [nop,nop,TS val 1094118115 ecr 1094118115], length 0
        0x0000:  4500 0034 ee9f 4000 4006 4e22 7f00 0001  E..4..@.@.N"....
        0x0010:  7f00 0001 8b88 270f 6a54 b619 405b 8a46  ......'.jT..@[.F
        0x0020:  8010 0156 fe28 0000 0101 080a 4136 eae3  ...V.(......A6..
        0x0030:  4136 eae3                                A6..
13:56:26.534752 IP (tos 0x0, ttl 64, id 61088, offset 0, flags [DF], proto TCP (6), length 52)
```

每次发送内容会有两个数据包，在其中第一个数据包[Flags p.]中是推送的内容的ascii码中可以看到我们发送的内容。

