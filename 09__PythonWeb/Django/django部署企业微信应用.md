---
title: "django部署企业微信应用.md"
date: 2017-07-04 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: ["Django"]
categories: ["python web"]
author: "Claymore"

---


### 写在前面

先登录企业微信管理后台：

https://work.weixin.qq.com/wework_admin/loginpage_wx。

为了在一个应用上部署我们写好的网站，我们需要设置三个东西：

![](http://claymore.wang:5000/uploads/big/4bbd9d013fb405d49be8406d39873315.png)





### 可信域名

首先是网页授权及JS-SDK，这个域名是用于OAuth2.0授权的时候安全认证，和后来我们要添加的自定义菜单的url有关。

可信域名要是经过ICP备案，正确形式为：www.qq.com  不要加http.



### 接受消息（回调校验）

这里是为了让我们开发好的应用和企业微信的后台进行双向通讯。

![](http://claymore.wang:5000/uploads/big/bc41754266c9bb3144b51fcb0401630d.png)

* 第一个url 在我们保存的时候会触发，这里要填我们在服务器运行的django应用（已经配置好nginx和域名），要具体到触发我们django对微信写的验证函数上。
* 第二个和第三个都可以随意填写（建议还是随机获取），只要在验证函数上一致就可，后面会说。

触发这个第一个url时，微信会自动在我们的url后加参数：

![](http://ojynuthay.bkt.clouddn.com/%E9%AA%8C%E8%AF%81%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0.png)

我们要在验证函数中处理这些参数：

view.py: (一般放在settings同级下)

```python
# -*- coding:utf-8 -*-

import logging
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.reverse import reverse
# from django.shortcuts import render_to_response
from rest_framework.decorators import api_view
from django.http import HttpResponse

from wechat.WXBizMsgCrypt import WXBizMsgCrypt

# logger = logging.getLogger("EngEye")

def wechat_validate(request):
    sToken = "xxx"
    sEncodingAESKey = "xxxxxx"
    sCorpID = "xxxxx"
    wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
    sVerifyMsgSig = request.GET.get("msg_signature")
    sVerifyTimeStamp = request.GET.get("timestamp")
    sVerifyNonce = request.GET.get("nonce")
    sVerifyEchoStr = request.GET.get("echostr")
    ret, sEchoStr = wxcpt.verify_url(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    # if ret != 0:
    #     logger.error("ERR: verify_url ret: " + str(ret))
    #     sys.exit(1)
    return HttpResponse(sEchoStr)
```

配置好相关url,将返回结果给微信后台，返回echostr明文（不加引号，不带bom头，不带换行符），验证生效，则接受消息开启。

开启后可关掉服务，注释掉相关url. settings中间件的配置可以转换状态。



### 自定义菜单

上方验证通过，才可以配置这里。如我们为一个菜单配置网站，用户点击即进入我们的网站：

![](http://claymore.wang:5000/uploads/big/e29b804f013f199f717ee70a8b5f50c1.png)



![](http://claymore.wang:5000/uploads/big/327090d4f1aca9fe81ad68200d001b7e.png)



这里填一个官方url ,你也可以直接填你的域名，当用户点击时会跳转，但是这样没有获取用户信息。

这个url完整的构造如下:

https://open.weixin.qq.com/connect/oauth2/authorize?appid=CORPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&agentid=AGENTID&state=STATE#wechat_redirect

| 参数              | 必须   | 说明                                       |
| --------------- | ---- | ---------------------------------------- |
| appid           | 是    | 企业的CorpID                                |
| redirect_uri    | 是    | 授权后重定向的回调链接地址，请使用urlencode对链接进行处理。注意redirect_uri的域名必须与该应用的可信域名一致。（测试时如果是子域名也可以） |
| response_type   | 是    | 返回类型，此时固定为：code                          |
| scope           | 是    | 应用授权作用域。snsapi_base：静默授权，可获取成员的基础信息；snsapi_userinfo：静默授权，可获取成员的详细信息，但不包含手机、邮箱；snsapi_privateinfo：手动授权，可获取成员的详细信息，包含手机、邮箱。 |
| agentid         | 是    | 企业应用的id。当scope是snsapi_userinfo或snsapi_privateinfo时，该参数必填。 |
| state           | 是    | 重定向后会带上state参数，企业可以填写a-zA-Z0-9的参数值，长度不可超过128个字节 |
| wechat_redirect | 是    | 终端使用此参数判断是否需要带上身份信息                      |


一个完整的实例（调通可用）：

```
https://open.weixin.qq.com/connect/oauth2/authorize?appid=xxxxxxx&redirect_uri=http://xxx.com/phone/my_mission/&response_type=code&scope=snsapi_base&state=1#wechat_redirect
```





