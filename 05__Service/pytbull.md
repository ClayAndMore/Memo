官网： http://pytbull.sourceforge.net/



## 介绍

pytbull是一个针对Snort，Suricata和任何生成警报文件的IDS / IPS的入侵检测/防御系统（IDS / IPS）测试框架。 它可用于测试IDS / IPS的检测和阻止功能，比较IDS / IPS，比较配置修改以及检查/验证配置。

该框架附带了约300个测试，分为11个测试模块：

* badTraffic：不符合RFC的数据包发送到服务器以测试如何处理数据包。
* bruteForce：测试服务器跟踪暴力攻击（例如FTP）的能力。 利用Snort和Suricata上的自定义规则。
* clientSideAttacks：此模块使用反向外壳为服务器提供下载远程恶意文件的指令。 此模块测试IDS / IPS防御客户端攻击的能力。
* denialOfService：测试IDS / IPS防御DoS企图的能力
* evasionTechniques:：各种逃避技术用于检查IDS / IPS是否可以检测到它们。
* fragmentedPackets：将各种碎片化的有效载荷发送到服务器，以测试其重组和检测攻击的能力。
* ipReputation：测试服务器检测来自低信誉服务器的流量的能力。
* normalUsage：与正常用法相对应的有效负载。
* pcapReplay：可以重播pcap文件
* shellCodes：在端口21 / tcp上向服务器发送各种shellcode，以测试服务器检测/拒绝shellcode的能力。
* testRules：基本规则测试。 这些攻击应该由IDS / IPS随附的规则集检测到。



它易于配置，将来可以集成新模块。

基本上有5种测试类型：

* 套接字：在给定端口上打开套接字，然后将有效负载发送到该端口上的远程目标。

* 命令：使用subprocess.call（）python函数将命令发送到远程目标。

* scapy：根据Scapy语法发送特制的有效载荷

* 客户端攻击：在远程目标上使用反向外壳并向其发送命令以使它们由服务器处理（通常是wget命令）。

* pcap重播：允许基于pcap文件重播流量



## 结构







## 安装



### 客户端

确保 python 2.6.5, 和以下依赖：

``` sh
apt-get install python python-scapy python-feedparser python-cherrypy3
apt-get install nmap hping3 nikto tcpreplay apache2-utils
```

安装 ncrack ，一个网络认证破解的开源工具：

``` sh
$ sudo aptitude install build-essential checkinstall libssl-dev libssh-dev
$ wget https://nmap.org/ncrack/dist/ncrack-0.5.tar.gz
$ tar -xzf ncrack-0.5.tar.gz
$ cd ncrack-0.5
$ ./configure
$ make
$ sudo make install
```

编译安装 ncrack 需要很多依赖。

可以尝试用apt 直接安装： `apt-get install -y ncrack`

安装 pytbull:

```sh
$ cd /usr/local/src/
$ wget https://downloads.sourceforge.net/project/pytbull/pytbull-2.1.tar.bz2 # 到官网复制最新链接
$ bzip2 -cd pytbull-2.0.tar.bz2 | tar xf -
$ sudo mv pytbull/ /opt/
$ cd /opt/python/
```



### server 端

要求：

```sh
sudo apt-get install python
sudo apt-get install vsftpd apache2 openssh-server
# 改 vsftpd 的配置文件：
vim /etc/vsftpd.conf
# Allow anonymous FTP? (Disabled by default)
anonymous_enable=NO
# Uncomment this to allow local users to log in.
local_enable=YES
```

拷贝客户端 pytbull/server 的脚本到服务端：

```
root@node200:~/ids# ls pytbull/server/
pytbull-server.py
```



## 使用

如果选择了clientSideAttacks模块（有关更多信息，请参见配置文件部分），则需要在服务器上启动反向Shell。 以下命令使用端口34567 / tcp：

`./pytbull-server.py -p 34567`

由于文件下载在当前目录中，因此您可以创建pdf /目录并从父位置启动pytbull:

``` sh
$ mkdir pdf/
$ cd pdf/
$ ../pytbull-server.py -p 34567

# eg:
root@node201:~/ids/pytbull/pdf# ../pytbull-server.py -p 34567

                                 _   _           _ _
                     _ __  _   _| |_| |__  _   _| | |
                    | '_ \| | | | __| '_ \| | | | | |
                    | |_) | |_| | |_| |_) | |_| | | |
                    | .__/ \__, |\__|_.__/ \__,_|_|_|
                    |_|    |___/
                       Sebastien Damaye, aldeid.com

Checking root privileges......................................... [   OK   ]
Checking port to use............................................. [   OK   ]

Server started on port: 34567
Listening...

```



在客户端启动，192.168.100.48 是ips/ids 服务端的地址

`sudo ./pytbull -t 192.168.100.48`

```
root@node200:~/ids/pytbull# sudo ./pytbull -d -c conf/config.cfg -t 172.19.19.201

                                 _   _           _ _
                     _ __  _   _| |_| |__  _   _| | |
                    | '_ \| | | | __| '_ \| | | | | |
                    | |_) | |_| | |_| |_) | |_| | | |
                    | .__/ \__, |\__|_.__/ \__,_|_|_|
                    |_|    |___/
                       Sebastien Damaye, aldeid.com

What would you like to do?
1. Run a new campaign (will erase previous results)
2. View results from previous campaign
3. Exit
Choose an option: 1

(standalone mode)
(debug mode)

***ERROR in checkNewVersionAvailable: <urlopen error timed out>
If you use a proxy, check your configuration.
```

这里应该加offline来启动，因为我们是本地服务器：

``` sh
oot@node200:~/ids/pytbull# sudo ./pytbull -d -c conf/config.cfg -t 172.19.19.201 --offline

                                 _   _           _ _
                     _ __  _   _| |_| |__  _   _| | |
                    | '_ \| | | | __| '_ \| | | | | |
                    | |_) | |_| | |_| |_) | |_| | | |
                    | .__/ \__, |\__|_.__/ \__,_|_|_|
                    |_|    |___/
                       Sebastien Damaye, aldeid.com

What would you like to do?
1. Run a new campaign (will erase previous results)
2. View results from previous campaign
3. Exit
Choose an option: 1

(standalone mode)
(debug mode)
(offline)

+------------------------------------------------------------------------+
| pytbull will set off IDS/IPS alarms and/or other security devices      |
| and security monitoring software. The user is aware that malicious     |
| content will be downloaded and that the user should have been          |
| authorized before running the tool.                                    |
+------------------------------------------------------------------------+
Do you accept (y/n)? y

BASIC CHECKS
------------
Checking root privileges......................................... [   OK   ]
Checking remote port 21/tcp (FTP)................................ [   OK   ]
Checking remote port 22/tcp (SSH)................................ [   OK   ]
Checking remote port 80/tcp (HTTP)............................... [   OK   ]
Checking path for sudo........................................... [   OK   ]
Checking path for nmap........................................... [   OK   ]
Checking path for nikto.......................................... [ Failed ]
```



### 组件配置

如上，使用过程中我们要维护组件的正确配置，（ps, 使用dpkg -L nikto 可以看到相关的文件）， 

``` sh
[ENV]
sudo                    = /usr/bin/sudo
nmap                    = /usr/bin/nmap
nikto                   = /usr/bin/nikto
niktoconf               = /etc/nikto/config.txt
```

nikto, 如果 apt 里下载的 nikto 没找到配置文件和 nikto.pl

``` sh
test@ubuntu:~$ wget https://github.com/sullo/nikto/archive/master.zip
test@ubuntu:~$ unzip master.zip
test@ubuntu:~$ cd nikto-master/program
test@ubuntu:~/nikto-master/program$ perl nikto.pl
```

nikto安装和使用，参考：

https://hackertarget.com/nikto-tutorial/

https://cyberops.in/blog/how-to-install-and-use-nikto-in-linux/

配置文件里改成：

``` sh
[ENV]
sudo                    = /usr/bin/sudo
nmap                    = /usr/bin/nmap
nikto                   = /root/ids/nikto-master/program/nikto.pl
niktoconf               = /root/ids/nikto-master/program/nikto.conf.default
```

同理 还有 ncrack 组件：

```
ncrack                  = /usr/bin/ncrack
ncrackusers             = /usr/share/ncrack/default.usr
ncrackpasswords         = /usr/share/ncrack/default.pwd
```





## 配置文件

``` ini
root@node200:~/ids/pytbull# vim conf/config.cfg
[CLIENT]
ipaddr                  = 172.19.19.200  # 客户端的地址，pytbull 被安装的地址
iface                   = ens160  # pytbull 发送 payloads 的网口
useproxy                = 0  #  0 或 1，仅由客户端用于连接到googlecode，以检查是否有较新版本的Pytbull  
proxyhost               =
proxyport               =
proxyuser               =
proxypass               =

[PATHS]
db                      = data/pytbull.db
urlpdf                  = https://github.com/sebastiendamaye/public/raw/master/infected/
pdfdir                  = pdf/malicious
pcapdir                 = pcap
tempfile                = /tmp/pytbull.tmp
#alertsfile              = /var/log/snort/alert
alertsfile              = /var/log/suricata/fast.log


[ENV]
sudo                    = /usr/bin/sudo
nmap                    = /usr/bin/nmap
nikto                   = /data/tools/nikto-2.1.5/nikto.pl
niktoconf               = /data/tools/nikto-2.1.5/nikto.conf
hping3                  = /usr/sbin/hping3
tcpreplay               = /usr/bin/tcpreplay
ab                      = /usr/bin/ab
ping                    = /bin/ping
ncrack                  = /usr/local/bin/ncrack
ncrackusers             = data/ncrack-users.txt
ncrackpasswords         = data/ncrack-passwords.txt
localhost               = 127.0.0.1

[FTP]
ftpproto                = sftp
ftpport                 = 22
ftpuser                 = justme
ftppasswd               = My_AwesomeP4ssword

[TIMING]
sleepbeforegetalerts    = 2
sleepbeforenexttest     = 2
sleepbeforetwoftp       = 2
urltimeout              = 10

[SERVER]
reverseshellport        = 12345   # 定义用于反向Shell的tcp端口， 在clientSideAttacks模式下使用

[TESTS]
clientSideAttacks       = 1
testRules               = 1
badTraffic              = 1
fragmentedPackets       = 1
bruteForce              = 1
evasionTechniques       = 1
shellCodes              = 1
denialOfService         = 1
pcapReplay              = 1
normalUsage             = 1
ipReputation            = 1

[TESTS_PARAMS]
ipreputationnbtests     = 10
```



## 问题

### type object 'datetime.datetime' has no attribute 'datetime'

运行时出现如下问题：

``` sh
CLIENT SIDE ATTACKS
------------
Checking if reverse shell is running on remote host.............. [   OK   ]
TEST #1 - 001e2710555613a82e94156d3ed9c289.......................
Traceback (most recent call last):
  File "./pytbull", line 704, in <module>
    oPytbull.doAllTests()
  File "./pytbull", line 546, in doAllTests
    self.doClientSideAttacksTest( clientSideAttacks.ClientSideAttacks(self._target).getPayloads() )
  File "./pytbull", line 482, in doClientSideAttacksTest
    test_dt_start = datetime.datetime.now()
AttributeError: type object 'datetime.datetime' has no attribute 'datetime'
```

在 pytbull 482 行插入 `import datetime`

根据：https://sourceforge.net/p/pytbull/bugs/24/

```
Traceback (most recent call last):
  File "./pytbull", line 705, in <module>
    oPytbull.doAllTests()
  File "./pytbull", line 551, in doAllTests
    self.doTest( module[1], eval( ('%s.%s'+'(self._target,self._cnf).getPayloads()') % (module[1], module[1][:1].upper()+module[1][1:]) ) )
  File "./pytbull", line 369, in doTest
    test_dt_start = datetime.datetime.now()
AttributeError: type object 'datetime.datetime' has no attribute 'datetime'
```

369行也要加上



## 运行结果

client:

```
CLIENT SIDE ATTACKS
------------
Checking if reverse shell is running on remote host.............. [   OK   ]
TEST #1 - 001e2710555613a82e94156d3ed9c289....................... [  done  ]
TEST #2 - 7b9e1c1b479447506cc046a5d8219eca....................... [  done  ]
TEST #3 - 004e74d54dcf79c641d5cf8a615488a0....................... [  done  ]
TEST #4 - 7d6e9af1018c10f1b7dfa5169a35d941....................... [  done  ]

TEST #5 - 0106fb569e87e02fc88d496064abdf19....................... [  done  ]
TEST #6 - 7f73dd439572409a64bc4dd0d603aacf....................... [  done  ]
TEST #7 - 02bfe34bea55e327cfdead9cff215f33....................... [  done  ]
TEST #8 - 7f7413bd2a4a0f001efd0305f4f56acf....................... [  done  ]
TEST #9 - 030423da29e1e6f4a527518126de4aeb....................... [  done  ]
TEST #10 - 80202a9c51d8544bac7ac273428dd97c...................... [  done  ]
[[1;2DTEST #11 - 03042cc3786dafdb941019488d4cad3e...................... [  done  ]
TEST #12 - 80f20af63314be2e8c79d8ca99eeb713...................... [  done  ]
TEST #13 - 03546e59967af0c2dbf609013934cd07...................... [  done  ]
TEST #14 - 82a5f96d1834411a3b5af9c21ffb14a8...................... [  done  ]
TEST #15 - 04095314d51057a13e21908de1266fc1...................... [  done  ]
TEST #16 - 82a7c8fdacca91b1bd0fdc2407674f50...................... [  done  ]
TEST #17 - 049675afd5c9505b9715872d499b9389...................... [  done  ]
TEST #18 - 82eeda4a754bf163d406e3e205df97e9...................... [  done  ]
TEST #19 - 0700bffe83561c1e2a5156d89de68f6d...................... [  done  ]
TEST #20 - 83220f00d3b3cde40bd3bf58c78ba899...................... [  done  ]
TEST #21 - 0733c4e2122cdfcfdd4699a3cbdc8b40...................... [  done  ]
TEST #22 - 853027bec65b3f2434788a70d4d15d89...................... [  done  ]
TEST #23 - 08da26158b76ca38e0ddb740aaf9b4ff...................... [  done  ]
TEST #24 - 872537348b6f1ef77d74f1d298978d72...................... [  done  ]..
```

server:

```
New connection from 172.19.19.200:53050
--2020-06-09 15:51:54--  https://github.com/sebastiendamaye/public/raw/master/infected/116d92f036f68d325068f3c7bbf1d535
Connecting to 192.168.59.241:8888... connected.
Proxy request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/sebastiendamaye/public/master/infected/116d92f036f68d325068f3c7bbf1d535 [following]
--2020-06-09 15:51:56--  https://raw.githubusercontent.com/sebastiendamaye/public/master/infected/116d92f036f68d325068f3c7bbf1d535
Connecting to 192.168.59.241:8888... connected.
Proxy request sent, awaiting response... 200 OK
Length: 149706 (146K) [application/octet-stream]
Saving to: ‘116d92f036f68d325068f3c7bbf1d535’

116d92f036f68d325068f3c7bbf1d535                    100%[===================================================================================================================>] 146.20K  2.95KB/s    in 4m 50s

2020-06-09 15:56:46 (517 B/s) - ‘116d92f036f68d325068f3c7bbf1d535’ saved [149706/149706]

New connection from 172.19.19.200:53050
--2020-06-09 15:57:00--  https://github.com/sebastiendamaye/public/raw/master/infected/9666cf5956922b4127c600b6a01f8488
Connecting to 192.168.59.241:8888... connected.
Proxy request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/sebastiendamaye/public/master/infected/9666cf5956922b4127c600b6a01f8488 [following]
--2020-06-09 15:57:01--  https://raw.githubusercontent.com/sebastiendamaye/public/master/infected/9666cf5956922b4127c600b6a01f8488
Connecting to 192.168.59.241:8888... connected.
Unable to establish SSL connection.
New connection from 172.19.19.200:53050
--2020-06-09 15:57:05--  https://github.com/sebastiendamaye/public/raw/master/infected/11dbb8d7924595e24c61eca8c9248834
Connecting to 192.168.59.241:8888... connected.
Proxy request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/sebastiendamaye/public/master/infected/11...

```

surIcata, fast.json 告警日志：

```
06/09/2020-15:26:15.204191  [**] [1:2001219:20] ET SCAN Potential SSH Scan [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.253:55146 -> 192.168.32.218:22
06/09/2020-15:45:33.224732  [**] [1:2002823:13] ET POLICY Possible Web Crawl using Wget [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.201:56876 -> 192.168.59.241:8888
06/09/2020-15:48:22.266450  [**] [1:2002823:13] ET POLICY Possible Web Crawl using Wget [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.201:56902 -> 192.168.59.241:8888
06/09/2020-15:49:31.824891  [**] [1:2002823:13] ET POLICY Possible Web Crawl using Wget [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.201:56944 -> 192.168.59.241:8888
06/09/2020-15:50:36.864916  [**] [1:2002823:13] ET POLICY Possible Web Crawl using Wget [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.201:56976 -> 192.168.59.241:8888
06/09/2020-15:51:56.169336  [**] [1:2002823:13] ET POLICY Possible Web Crawl using Wget [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.19.19.201:57004 -> 192.168.59.241:8888
```

