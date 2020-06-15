
---
title: "web安全.md"
date: 2019-09-29 19:29:06 +0800
lastmod: 2019-09-29 19:29:06 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[安全, web] date: 2017-06-29



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


#### 跨站请求伪造csrf

Cross—Site Request Forgery

攻击者发现CSRF漏洞——构造代码——发送给受害人——受害人打开——受害人执行代码——完成攻击.

eg: 假如受害者的网站为a.cn,  攻击者的网站为b.cn,  发现a添加管理员的接口没有做验证，那么我们可以在我们的b.cn地上构建一个b.cn/index.html , 里面写上增加管理员的post接口和数据，然后发邮件（或者放在xss）中让a的管理员登陆后触发，然后就能添加一个我们预定的管理员账户了。



Django使用专门的中间件（CsrfMiddleware）来进行CSRF防护。具体的原理如下：

1. 它修改当前处理的请求，向所有的 POST 表单增添一个隐藏的表单字段，使用名称是 csrfmiddlewaretoken，值为当前会话 ID 加上一个密钥的散列值。 如果未设置会话 ID，该中间件将不会修改响应结果，因此对于未使用会话的请求来说性能损失是可以忽略的。
2. 对于所有含会话 cookie 集合的传入 POST 请求，它将检查是否存在 csrfmiddlewaretoken 及其是否正确。 如果不是的话，用户将会收到一个 403 HTTP 错误。 403 错误页面的内容是检测到了跨域请求伪装。 终止请求。
   该步骤确保只有源自你的站点的表单才能将数据 POST 回来。






### DOS 攻击

 DOS是denial of service，也就是拒绝服务攻击 , 不是命令行窗口那个dos。



### MIME Type

浏览器中的内容有HTML，XML，GIF,Flash等，浏览器是如何区分的呢，是Mime type  是媒体类型。

媒体类型是通过HTTP协议，由服务器告知浏览器的，通过Content-Type 来表示的，如：

`Content-Type: text/HTML`

这样的text/HTML是由标准发布的。

如果是客户端自己定义的格式，一般只能以application/x- 开头。

有些浏览器会做默认处理，如和系统中的配置文件有关，操作系统中可以给文件配置Mime Type 信息，在windos下HKEY_LOCAL_MACHINESOFTWAREClassesMIMEDatabaseContent Type”主键，你可以看到所有 MIME Type 的配置信息。




### C&C服务器（C2）
被攻击者（已经感染了木马）---vps(c&c服务器)--- 控制端（攻击者）
被攻击者和攻击者都在内网中（路由），攻击者购买vps（为了获得一个固定的公网ip）通过ppp协议来监听被攻击者的流量，从而获得信息。
比较出名的是15年俄罗斯黑客通过twitter 作为C&C服务器。
