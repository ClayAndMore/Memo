---
title: "Burp Suite.md"
date: 2019-09-29 19:29:06 +0800
lastmod: 2019-09-29 19:29:06 +0800
draft: false
tags: [""]
categories: ["安全"]
author: "Claymore"

---




## Burp Suite 使用



Burp Suite 是用于攻击web 应用程序的集成平台。它包含了许多工具，并为这些工具设计了许多接口，以促进加快攻击应用程序的过程。

简单地说，BurpSuite可以帮助我们抓包改包、密码爆破、自动化漏洞探测、编码解码、被动扫描等等等

所有的工具都共享一个能处理并显示HTTP 消息，持久性，认证，代理，日志，警报的一个强大的可扩展的框架:

1.Target(目标)——显示目标目录结构的的一个功能
2.Proxy(代理)——拦截HTTP/S的代理服务器，作为一个在浏览器和目标应用程序之间的中间人，允许你拦截，查看，修改在两个方向上的原始数据流。
3.Spider(蜘蛛)——应用智能感应的网络爬虫，它能完整的枚举应用程序的内容和功能。
4.Scanner(扫描器)——高级工具，执行后，它能自动地发现web 应用程序的安全漏洞。
5.Intruder(入侵)——一个定制的高度可配置的工具，对web应用程序进行自动化攻击，如：枚举标识符，收集有用的数据，以及使用fuzzing 技术探测常规漏洞。
6.Repeater(中继器)——一个靠手动操作来触发单独的HTTP 请求，并分析应用程序响应的工具。
7.Sequencer(会话)——用来分析那些不可预知的应用程序会话令牌和重要数据项的随机性的工具。
8.Decoder(解码器)——进行手动执行或对应用程序数据者智能解码编码的工具。
9.Comparer(对比)——通常是通过一些相关的请求和响应得到两项数据的一个可视化的“差异”。
10.Extender(扩展)——可以让你加载Burp Suite的扩展，使用你自己的或第三方代码来扩展Burp Suit的功能。
11.Options(设置)——对Burp Suite的一些设置



``` sh
# 正常流程
user -- 发送请求包 --> 服务器

# 加入Burp Suite
user -- 发送请求包 --> Burp 代理，修改数据 --> 发送请求包 ---->  服务器
```





### 安装和运行

官网：https://portswigger.net/burp/communitydownload， 会很慢。

用的免安装版，要求有：java 1.8

进入解压目录 ：`java -jar BurpHelper.jar`





### 安装CA证书

打开 Burp, 选择Temporary project -> Next ,

然后访问 http://127.0.0.1:8080/， 点击右上角的CA Certificate, 浏览器会下载个cacert.der,

打开浏览器设置，证书管理， 找到 “手新仍的根证书颁发机构”， 点击导入，导入刚才下载的证书。 





### Proxy

```
用户 -> 浏览器 -> 代理服务器 -> 服务器
```

浏览器开启代理配置相应的IP与端口, 本地ip, 8080端口， options下可更改，还可以添加多个端口。

Scanner的Live scanning子选项卡，在Live Active Scanning控制块中，选择Use suite scope，这样，Burp Scanner将自动扫描经过Burp Proxy的交互信息。 

我们可以拦截post请求，更改post数据， 点击Forward发送修改后的请求，不想发送点击Drop, 

http history 标签页里有曾修改前的和修改后的



### 绕过前端限制

https://rimovni.exeye.run/mecimlif/home

正常修改邮箱的时候不可以添加<>,等注入语句，因为前端做了限制，我们可以通过Burp修改请求绕过前端。

``` sh
# 正常请求
name=123&email=1234%40qq.com&password=123&confirmpass=123
# 修改邮箱
email=<img src=x onerror=alert(1)> 
```

oneerror如果在加载图片时发生错误则执行 JavaScript 



### 密码爆破 intruder

闯入者，Intruder是获取Web应用信息的工具。它可以用来爆破，枚举，漏洞测试等任何你想要用的测试手段，然后从结果中获取数据。

### 

https://burp.twosecurity.xyz/

弱密码：http://resource.host.smartgslb.com/passwords_quick.txt

在页面输入admin账户，密码随意，开启Burp拦截，拦截后的内容（Proxy-intercept），右键 send to Intruder(侵入者).

进入proxy右侧的intruder, 第二页，第一页应该是自带的，Positions选项卡 Attack type选择Sniper(狙击手)

下方有如下请求：

``` sh
Origin: https://burp.twosecurity.xyz
Connection: close
Referer: https://burp.twosecurity.xyz/
Upgrade-Insecure-Requests: 1

username=§admin§&password=§111111§&login-button=§§
```

其中被§包围起来的是参数，我们先点击右侧的clear§清除所有参数

选中11111 点击右侧的Add§ 添加参数，即添加密码为默认的爆破参数。

选择选项卡的Payloads,  Payload set 默认为1， Payload type默认为 Simple list

点击下方的Payload Options 中的 Load 导入我之前下载的的弱密码txt.

然后点击右上方的Start attack按钮开始攻击。

然后观察请求的返回值等判定是否攻击成功。



### Burp Repeater 

Burp Repeater 是一个HTTP 发包模块，通常我们使用它来重放抓包的请求，可以更加方便的修改包内容以及进行测试。



### Spider

爬虫

http://www.kali.org.cn/thread-21482-1-1.html



### Scanner

* Scan queue  扫描队列，这里将显示扫描队列的状态 进度 结果等


* Live scanning  实时扫描，两种模式：

  * Live Active Scanning：积极扫描。当浏览时自动发送漏洞利用代码。

    Scanner的Live scanning子选项卡，在Live Active Scanning控制块中，选择Use suite scope，这样，Burp Scanner将自动扫描经过Burp Proxy的交互信息。 

  * Live Passive Scanning：被动扫描。只分析流量不发送任何请求。

* Issue Definitions 漏洞列表，列出了burp可以扫描到的漏洞详情



