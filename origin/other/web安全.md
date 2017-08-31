---
title: jjj
date: 2017-06-29 17:55:09
categories:
header-img:
tags:
---



### SQL注入

基本概念：利用现有应用程序，攻击者将精心构造的SQL的语句注入到后台数据库，使数据库引擎成功执行，这是SQL注入的标准释义。

原理： 攻击者通过扫描器或者自制语句（修改url参数）得知该网站存在漏洞，然后用精心构造的SQL语句通过缺少对用户输入合法性判断的服务器去动态查询数据库。然后获取root账号做恶意的事，最后去后台擦除监控日志。

显注： 输入语句会提示明显的错误提示。

盲注： 页面不会提供错误提示。



 扫描器，探软件

扫描器：AWVS ,APPScan 

抓包代理工具： burpsuite

 验证测试： sqlmap

 

常用测试语句：

```
'    # 在数据库中让引号成单数，使数据库出错
and 1=1  # 在数据库中和上一个真
and 1=2  # 在数据库上或上一个假，使查询出错，或得错误信息。
或者用'and 1=1' ，'and 1=2'

oder by x， x 是一个数，这里可以测试有该表有几个字段，比如测试出x=7,那么下面就可以用union
and 1=2 union select 1，2，3，4，5，6 让页面出错，并看到这七个字段是什么
```

剩下的就是些 sql 知识了。


### 前端攻击
#### 跨站脚本攻击xss

`cross-site-scripting`   为了区别css,我们为它称之为xss.

钓鱼攻击： url中嵌入前端语句，模拟用户登录输入框，为了不显眼，可以将伪造的url编码。

获取cookie  :   url后 或输入框可加入：`<scirpt>alert(document.cookie)</scripte>`等来获取。

#### 跨站请求伪造csrf

在用户已经登录a网站（存在CSRF漏洞）没有退出登录时，就访问了有攻击者的b网站，会携带cookie信息




### MIME Type

浏览器中的内容有HTML，XML，GIF,Flash等，浏览器是如何区分的呢，是Mime type  是媒体类型。

媒体类型是通过HTTP协议，由服务器告知浏览器的，通过Content-Type 来表示的，如：

`Content-Type: text/HTML`

这样的text/HTML是由标准发布的。

如果是客户端自己定义的格式，一般只能以application/x- 开头。

有些浏览器会做默认处理，如和系统中的配置文件有关，操作系统中可以给文件配置Mime Type 信息，在windos下HKEY_LOCAL_MACHINESOFTWAREClassesMIMEDatabaseContent Type”主键，你可以看到所有 MIME Type 的配置信息。


### C&C服务器
被攻击者（已经感染了木马）---vps(c&c服务器)--- 控制端（攻击者）
被攻击者和攻击者都在内网中（路由），攻击者购买vps（为了获得一个固定的公网ip）通过ppp协议来监听被攻击者的流量，从而获得信息。
比较出名的是15年俄罗斯黑客通过twitter 作为C&C服务器。
