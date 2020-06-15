
---
title: "suricata规则.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


## 规则

官方开源规则地址：https://rules.emergingthreats.net/open/，Emerging Threats维护的规则，我们一般常用的就是这个规则库。很强大的规则库，规则数量有20000+。

其他开源规则：

https://github.com/ptresearch/AttackDetection， PT的Suricata规则库，根据恶意软件、黑客的网络通讯协议以及漏洞的poc去编写

https://sslbl.abuse.ch/blacklist/  瑞士的非盈利组织abuse.ch维护的项目。他们维护的这个黑名单是标识恶意软件与僵尸网络相关的。他们提供了一个Suricata的规则，可以根据黑名单检测网络中的恶意连接。



suricata 通过配置文件的default-rule-path设置规则目录,*rule-files*来选择启用那些规则

``` yaml
default-rule-path: /etc/suricata/rules

rule-files:
 - botcc.portgrouped.rules
 - botcc.rules
 - ciarmy.rules
 - compromised.rules
 - drop.rules
 - dshield.rules
 - emerging-activex.rules
 - emerging-adware_pup.rules
 - emerging-attack_response.rules
 - emerging-chat.rules
 - emerging-coinminer.rules
 - emerging-current_events.rules
 - emerging-deleted.rules
 - emerging-dns.rules
# - emerging-dos.rules
...
```



### ET 规则集

https://doc.emergingthreats.net/bin/view/Main/EmergingFAQ#What_is_the_general_intent_of_ea

```sh
app-layer-events.rules # 针对应用协议的规则
botcc.portgrouped.rules botcc.rules #这些是已知和确认的活动僵尸网络和其C&C(command and control)服务器。由一些组织生成。每天更新。
ciarmy.rules # 封锁被ciArmy.com标记出来的Top Attackers（ciArmy.com是个威胁数据库，对全球的任意ip地址提供准确的及时的评分）。定期更新。
compromised.rules # 这是一个已知的受影响的主机列表。每天更新。
decoder-events.rules # 解码器事件，里面包含了对解码器解码所产生的事件，比如包无效、包过大、过小等
dnp3-events.rules # 包含对dnp3（分布式网络协议）的一些规则，不多，只有几条
dns-events.rules  # 包含对dns协议的一些规则，比如dnsflooded事件等，不多，只有几条
drop.rules        # 每天更新的Spamhaus DROP(Don't Route or Peer)列表，列出了著名的、专业的垃圾邮件发送者。每天更新。
dshield.rules     # 每天更新的DShield top attackers。十分可靠。
emerging-activex.rules # 主要用来检测与 ActiveX 控件有关的攻击
emerging-attack_response.rules # 这些规则是为了捕获成功攻击的结果，诸如“id=root”之类的东西，或者表示可能发生妥协的错误消息（即虽然产生了错误消息，但是攻击已经成功）。注意：木马和病毒感染后的活动一般在VIRUS规则集里，不是在这个规则集里。
emerging-chat.rules # 主要检测聊天软件、即时通讯软件的攻击，大部分是国外的一些软件，比如facebook，雅虎，msn
emerging-current_events.rules # 这些规则是不打算在规则集中长期保存的，或者是考虑纳入之前需要进行测试的规则。大多数情况下，这些都是针对当天的大量二进制URL的简单sigs，用来捕获CLSID新发现的易受攻击的应用程序，我们没有这些漏洞的任何细节。这些sigs很有用，却不是长期有效的。
emerging-deleted.rules # 里面都是被注释掉的规则，可能删除后的规则放在这里
emerging-dns.rules # 检测dns协议相关的攻击
emerging-dos.rules # 目的是捕获入站的DOS（拒绝服务）活动和出站指示。
emerging-exploit.rules # 用来检测exp的规则。一般来说，如果你正在找windows的exp，在这个规则里可以找到。就像sql注入一样，exploits有着自己的体系。 总之就是用来检测exploits漏洞的。
emerging-ftp.rules # 检测ftp协议相关的攻击
emerging-games.rules # 魔兽世界、星际争霸和其他流行的在线游戏都在这里。我们不打算把这些东西贴上邪恶的标签，只是它们不适合所有的攻击环境，所以将它们放在了这里。
emerging-icmp_info.rules emerging-icmp.rules # 检测与icmp协议相关的攻击
emerging-imap.rules # 检测与imap相关的攻击
emerging-inappropriate.rules # 色情、儿童色情，你不应该在工作中访问的网站等等。WARNING：这些都大量使用了正则表达式，因此存在高负荷和频繁的误报问题。只有当你真正对这些规则感兴趣时才去运行这些规则。
emerging-info.rules # 看了一些规则后，似乎是检测与信息泄露、信息盗取等事件的规则，里面会检测后门、特洛伊木马等与info相关的攻击
emerging-malware.rules # 这一套最初只是间谍软件，这就足够了。间谍软件和恶意软件之间的界限已经很模糊了。这里不仅仅是间谍软件，但是请放心，这里没有任何东西是你想在自己的网络或者PC上运行的。已知的更新模式、已知的恶意软件的UserAgent字符串和大量的其它有用的东西。如果你只准备运行一个规则集来保证安全性，这个规则集是首选。
emerging-misc.rules # 检测混杂的攻击，这种攻击一般没有确切的分类，或者使用了多种技术
emerging-mobile_malware.rules # 检测移动设备上的恶意软件
emerging-netbios.rules # 检测与netbios协议有关的攻击
emerging-p2p.rules # P2P(Peer to Peer)之类的。我们并不想将它定义为有害的，只是不适合出现在IPS/IDS的网络环境中。
emerging-policy.rules # 对于经常被公司或组织政策禁止的事务的规则。Myspace、Ebay之类的东西。
emerging-pop3.rules # 检测与pop3协议有关的攻击
emerging-rpc.rules # 检测与rpc（远程过程调用协议)有关的攻击
emerging-scada.rules # 检测与SCADA（数据采集与监控系统）相关的攻击
emerging-scan.rules # 检测探测行为。Nessus，Nikto，端口扫描等这样的活动。这是攻击前准备时期的警告。
emerging-shellcode.rules # 检测shellcode，shellcode是一段用于利用软件漏洞而执行的代码，以其经常让攻击者获得shell而得名。
emerging-smtp.rules # 检测与smtp协议相关的攻击
emerging-snmp.rules # 测与snmp协议相关的攻击
emerging-sql.rules # 这是一个巨大的规则集，用于捕获在特殊应用程序上的特殊攻击。这里面有一些普遍的SQL注入攻击规则，效果很好，可以捕获大多数攻击。但是这些规则根据不同的app和不同的web服务器，有很大的差别。如果你需要运行非常严格的web服务或者很重视信息的安全性，请使用这个规则集。
emerging-telnet.rules # 检测与telnet协议相关的攻击，例如暴力破解等
emerging-tftp.rules # 检测与tftp协议相关的攻击
emerging-trojan.rules # 检测trojan木马
emerging-user_agents.rules # 检测异常的user-agents
emerging-voip.rules # 检测voip相关的异常，它是一个新兴的规则集，目前还很小，但是我们预计它很快就会增长。
emerging-web_client.rules # 检测web客户端的攻击
emerging-web_server.rules # 检测web服务端的攻击
emerging-web_specific_apps.rules # 检测相关应用组件的漏洞（CVE）
emerging-worm.rules # 检测蠕虫
http-events.rules  # http事件规则
modbus-events.rules # 检测modbus事件
rbn-malvertisers.rules rbn.rules # Rbn的规则，该规则已经过时了，可忽略。
smtp-events.rules # 检测smtp事件
stream-events.rules # 检测stream事件
tls-events.rules # 检测tls事件
tor.rules # 检测使用tor进行匿名通信的流量，tor本身没有威胁，但却是很可疑的行为
```





### eg

```
drop tcp $HOME_NET any -> $EXTERNAL_NET any (msg:"ET TROJAN Likely Bot Nick in IRC (USA +..)"; flow:established,to_server; flowbits:isset,is_proto_irc; content:"NICK "; pcre:"/NICK .*USA.*[0-9]{{3,}}/i"; reference:url,doc.emergingthreats.net/2008124; classtype:trojan-activity; sid:2008124; rev:2;)
```



### action 


drop为action(动作)

 - pass   
 Suricata将停止扫描数据包并跳到所有规则的末尾（仅针对当前数据包）

 - drop
 这只涉及IPS/inline模式。如果程序找到匹配的包含drop的签名，它将立即停止。数据包将不再发送。缺点：接收器没有接收到正在发生的事情的消息，从而导致超时（当然是TCP）。Suricata为此数据包生成警报。


 - reject
 这是对数据包的主动拒绝。接收端和发送端都接收到拒绝数据包。有两种类型的拒绝数据包将被自动选择。如果有问题的数据包与TCP有关，它将是一个重置数据包。对于所有其他协议，它将是一个ICMP错误包。Suricata也会生成警报。当处于inline/ips模式时，违规数据包也将像“drop”操作一样被删除

 - alert
 如果签名匹配并包含alert，则该数据包将被视为任何其他非威胁性数据包，但此数据包除外，Suricata将生成警报。只有系统管理员才能注意到此警报。




### Protocol

``` 
tcp为Protocol(协议)

TCP（用于TCP通信）
UDP 
ICMP
ip（同时用与TCP与UDP）

应用层协议：
http
ftp
tls (this includes ssl)
smb
dns
dcerpc
ssh
smtp
imap
modbus (disabled by default)
dnp3 (disabled by default)
enip (disabled by default)
nfs (depends on rust availability)
ikev2 (depends on rust availability)
krb5 (depends on rust availability)
ntp (depends on rust availability)
dhcp (depends on rust availability)
```





### 源 / 目的地

``` 
$HOME_NET			来源地
$EXTERNAL_NET		目的地

可选参数：
../..					 IP ranges (CIDR notation)
!						  exception/negation
[.., ..]				grouping

例子：
$HOME_NET					yaml配置文件中的 HOME_NET
[$EXTERNAL_NET, !$HOME_NET]						配置文件中的EXTERNAL_NET 以及非HOME_NET
! 1.1.1.1						除了1.1.1.1外的任意IP
```



### port 端口

```
any  为port(端口)，第一个为源地址的端口，第二个为目标地址的端口

可选参数：
:				端口系列
!					除...外
[.., ..]			组内所有端口

例子：
[80, 81, 82]			端口 80, 81和 82
[80: 82]				80到82端口
[1024: ]			1024以后的端口
!80						除 80端口外
[80:100,!99]				80到100中除了99外的端口
[1:80,![2,4]]				1到80端口中除2到4的其他端口
```



###  direction 方向

```
->  为direction(方向)
只有方向与签名中相同的数据报才能匹配

可选参数：
source -> destination				源到目标，单向匹配
source <> destination				双向都匹配
```



### meta

后面括号内的为meta信息：

```
alert http any any -> any any (msg:"SURICATA HTTP Request abnormal Content-Encoding header"; classtype:protocol-command-decode; sid:2221033; rev:1;)
```

#### **事件信息选项：**

1. msg(message 消息）：对规则的描述，可以理解为规则的“名称”

2. sid(signature ID 特征标识符）：用于唯一性地标识规则，sid不能重复，且只能为数值
    a. 0-10000000：为Sourcefire VRT保留
    b. 20000000-29999999：为 Emerging Threats（ET）保留
    c. 30000000+ ：公用

3. rev(revision 修订）：用于表示规则发生了修改，可以理解为规则的版本号
    a. 当创建一条新规则时，制定 rev:1; ，以表明该规则为第一版本
    b. 当规则被改变时，无需创建新规则，可保持sid不变，使rev递增
    c. sid通常与rev一起使用, 一般而言，sid在rev之前，它们是签名的最后两个

4. reference （引用）：用于链接外部信息来源，从而为规则提供附加的情景资料
   好处：保持规则整洁，减小规则长度，使其更易编辑管理

   ```
    a. 直接指定： reference:<reference type>,<reference>;
                reference:url,doc.emergingthreats.net/2010235
   
    b. 可通过在suricata.yaml配置reference.config文件来定义引用类型
       文件中使用格式：config reference:<reference type><reference prefix>;
       例如  文件中：config reference:cve http://cve.mitre.org/cgi-bin/cvename.cgi?name=
            规则中：reference:cve,2001-0414
            实际引用：reference:cve,http://cve.mitre.org/cgi-bin/cvename.cgi?name=2001-0414
   ```

5. priority (优先级)：用于手动指定规则的优先级，提升分析员查看警报的效率
   此选项可以任意整数设置，可使用0-10之间的数指定优先级，0最高，10最低

6. 类别（classtype）：用于根据规则所检测的活动类型为规则分类
   规则中指定方式：`classtype:<Classification Name>;`,  eg: `classtype:trojan-activity;`
   通过在suricata.yaml配置classification .config文件来描述规则中的类别

   文件中格式：`config classification: <classification name>,<classification description>,<classification privoroty>`
       classification name：类别名称
       classification description：类别描述
       classification privoroty：类别指定的默认优先级，当规则使用类别时以此处优先级为准

7. gid (group ID)

    gid关键字可用于为不同的签名组提供另一个ID值（如在sid中）。Suricata默认使用gid 1。可以修改这个。它将被改变是不常见的，改变它没有技术上的影响。您只能在警报中注意到它。

    下面例子中，[1:2008124:2]，其中1表示gid，2008124表示sid，2表示rev

    ```
    10/15/09-03:30:10.219671 [**] [1:2008124:2] ET TROJAN Likely Bot Nick in IRC (USA +..) [**] [Classification: A Network Trojan was Detected] [Priority: 3] {TCP} 192.168.1.42:1028 -> 72.184.196.31:6667
    ```



#### Payload 检查内容

1. content （检查内容）：检查数据包内容中是否包含某个字符串
   如：content:"evilliveshere";    
   指定多个匹配项：content:"evilliveshere";  content:"here";  
      a. 使用感叹号！对匹配项的否定：content:!"evilliveshere"; 
      b. 将字符串的十六进制用管道符（|）进行包围：content:"|FF D8|"; 
      c. 字符串与十六进制混合使用：content:"|FF D8|evilliveshere"; 
      d. 匹配内容区分大小写
      e. 保留字符（; \ "）须进行转义或十六进制转码
   
   eg:
   
   ```sh
   alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"Outdated Firefox on
   Windows"; content:"User-Agent|3A| Mozilla/5.0 |28|Windows|3B| ";
   content:"Firefox/3."; distance:0; content:!"Firefox/3.6.13";
   distance:-10; sid:9000000; rev:1;)
   
   # 如果Firefox的版本不是3.6.13就会生成警告
   ```
   
2. 检测内容修饰语：通过在匹配内容之后添加一些修饰语，可以精确控制IDS引擎在网络数据中匹配内容的方式。\

     a. nocase：匹配内容不区分大小写，修饰前面最近的一个content, 如 `content:"root";nocase;`

     b. offset：用于表示从数据包载荷的特定位置开始内容匹配，从载荷其实位置算起
       注意载荷开始位置从0字节处开始，而不是1字节处, `content:"root";offset:5;`

     c. depth：用于限制搜索匹配内容的结束位置。

       若使用了offset，则开始位置为offset，否则为载荷开始位置: ` content:"root";offset:5;depth:7;`

     d. distance：用于指定上一次内容匹配的结束位置距离本次内容匹配的开始位置的距离
     
     e. within：用于限制本次匹配必须出现在上一次匹配内容结束后的多少个字节之内 
     
     f. within和distance联合使用，判断第二个content是否在第一个content+within个字节范围内:
          eg: `content:"evilliveshere";  content:"here"; distance:1;within:7;`
     在匹配字符串“evilliveshere”后的1到7个字节范围内对字符串“here”进行匹配     
     
    d.  startswith: 匹配以..开头，不能与 `depth` ， `offset` ， `within` 或 `distance` 混合使用
    
    `content:"GET|20|"; startswith;`  匹配内容以`GET|20|`开头等价于 `content:"GET|20|"; depth:4;offset:0;`
    
    g. endswith: 匹配以.. 结尾， 不能与 `depth` ， `offset` ， `within` 或 `distance` 混合使用
     `content:".php"; endswith;` 等价于 `content:".php";isdatat:!1,relative`



#### tcp

```
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:”GPL DELETED typot trojan traffic”; flow:stateless; flags:S,12; window:55808; reference:mcafee,100406; classtype:trojan-activity; sid:2182; rev:8;)
```

1、seq

seq关键字可以在签名中用于检查特定的TCP序列号。序列号实际上是由TCP连接的两个端点随机生成的数字。客户机和服务器都创建了一个序列号，序列号随着发送的每个字节的增加而增加。所以两边的序列号是不同的。连接两侧必须确认此序列号。TCP通过序列号处理确认、排序和重传。它的数目随着发送方发送的每个数据字节的增加而增加。seq帮助跟踪字节所属的数据流中的位置。如果syn标志设置为1，那么数据第一个字节的序列号就是这个数字加1

2、ack

ACK是对接收到TCP连接另一端发送的所有以前（数据）字节的确认。在大多数情况下，TCP连接的每个包在第一个SYN之后都有一个ACK标志，ACK号随着每个新数据字节的接收而增加。ACK关键字可用于签名中，以检查特定的TCP确认号。

3、window

TCP窗口大小是一种控制数据流的机制。该窗口由接收器（接收器公布的窗口大小）设置，并指示可以接收的字节数。在发送方可以发送相同数量的新数据之前，接收方必须先确认此数据的大小。此机制用于防止接收器被数据溢出。

4、tcp.mss

匹配tcp mss选项值。如果选项不存在，将不匹配

```
tcp.mss:<min>-<max>;
tcp.mss:[<|>]<number>;
tcp.mss:<value>;
e.g.
alert tcp $EXTERNAL_NET any -> $HOME_NET any (flow:stateless; flags:S,12; tcp.mss:<536; sid:1234; rev:5;)
```

5、tcp.hdr

在整个TCP头上匹配的粘性缓冲区。

```
alert tcp $EXTERNAL_NET any -> $HOME_NET any (flags:S,12; tcp.hdr; content:”|02 04|”; offset:20; byte_test:2,<,536,0,big,relative; sid:1234; rev:5;)
```





#### http 

http内容修饰语：针对检测http流量的规则，Suricata提供了http流重组能力，同时提供了用于编写HTTP流量相关的更高效的规则修饰器, 例如：

```
    alert tcp any any -> any 80 (msg:"Evil Doamin www.appliednsm.com"; "content:"GET";http_method;  content:"www.appliednsm.com";http_uri; sid:5445555; rev:1;)
```

常用http内容修饰语：
http_client_body       HTTP客户端请求的主体内容
http_cookie         HTTP头字段的“Cookie”内容
http_header         HTTP请求或响应头的任何内容
http_method         客户端使用的HTTP方法（GET，POST等）
http_uri               HTTP客户端请求的URI内容
http_stat_code       服务器响应的HTTP状态字段内容
http_stat_message     服务器响应的HTTP状态消息内容
http_encode         在HTTP传输过程中所使用的编码类型



#### flow

flow是特定时间内具有相同数据的数据包（5元组信息）同属于一个流，suricata会将这些流量保存在内存中。

```
alert tls any any  -> any any (msg:"SURICATA TLS invalid record type"; flow:established; app-layer-event:tls.invalid_record_type; flowint:tls.anomaly.count,+,1; classtype:protocol-command-decode; sid:2230002; rev:1;)
```

Flow关键字可用于匹配流的方向，例如to/from客户端或to/from服务器。它还可以匹配是否建立了流。流关键字还可以用来表示签名必须只在流上匹配（只在流上匹配）或只在包上匹配（不在流上匹配）。

``` sh
to_client  # 在从服务器到客户端的数据包上匹配
to_server  # 在从客户端到服务器的数据包上匹配
	
from_client # 在从客户端到服务器的数据包上匹配(等同于to_server)
from_server # 在从服务器到客户端的数据包上匹配 (等同于to_client)
	
established # 匹配已建立的连接
not_established # 匹配不属于已建立连接的数据包	
stateless # 匹配属于或不属于已建立连接的数据包

only_stream # 匹配流引擎重新组装的数据包
no_stream # 匹配流引擎未重新组装的数据包。与重新组装的数据包不匹配
only_frag # 匹配从片段中重新组装的数据包
no_frag # 匹配未从片段重新组合的数据包
```

flowbits,存在属于一个流的多个数据包，suricata会将这些信息保存在内存中。只有当两个数据包匹配时才会生成警报。因此，当第二个包匹配时，Suricata必须知道第一个包是否也是匹配的。如果一个包匹配，那么FlowBits会标记该流，因此当第二个包匹配时，它会生成一个警报。

```sh
flowbits: set, name # 如果flow中存在，就会设置 条件/名字
	
flowbits: isset, name # 可以在规则中使用，以确保当规则匹配并且在流中设置了条件时，它会生成警报
	
flowbits: toggle, name # 反转当前设置。因此，例如，如果设置了某个条件，它将被取消设置，反之亦然。

flowbits: unset, name # 可用于取消设置flow中的条件

flowbits: isnotset, name # 可以在规则中使用，以确保它在匹配且flow中未设置条件时生成警报。

flowbits: noalert # 此规则不会生成警报
```





### 参考

https://www.cnblogs.com/linagcheng/p/12559922.html