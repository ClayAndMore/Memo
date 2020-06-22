---
title: "oauth认证.md"
date: 2020-03-17 18:47:27 +0800
lastmod: 2020-03-17 18:47:27 +0800
draft: false
tags: [""]
categories: ["安全"]
author: "Claymore"

---
### 应用场景

假如我有个网站，用户浏览我的网站想留言，可以有两种方式：

* 注册、登录，使用在我的网站注册账户留言
* 使用第三方来登录，如Github, 在你的 GIthub 账户授权后，可以使用github的账户信息来留言



第二种方式就用到了oauth 授权。



### OAuth 的思路

OAuth在"客户端"与"服务提供商"之间，设置了一个授权层（authorization layer）。"客户端"不能直接登录"服务提供商"，只能登录授权层，以此将用户与客户端区分开来。登录后授权层会给与一个令牌(token)。与用户的密码不同。用户可以在登录的时候，指定授权层令牌的权限范围和有效期。

"客户端"登录授权层以后，"服务提供商"根据令牌的权限范围和有效期，向"客户端"开放用户储存的资料。

文档： http://www.rfcreader.com/#rfc6749 

```
     +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+
```

几个名词：

```
（1） Third-party application：第三方应用程序，又称"客户端"（client），即上面我的网站。

（2）HTTP service：HTTP服务提供商，即上面Github。

（3）Resource Owner：资源所有者，本文中又称"用户"（user,你）。

（4）User Agent：用户代理，指浏览器。

（5）Authorization server：认证服务器，即服务提供商（github）专门用来处理认证的服务器。

（6）Resource server：资源服务器，即服务提供商存放用户生成的资源的服务器。它与认证服务器，可以是同一台服务器，也可以是不同的服务器
```

（A）用户打开客户端以后，客户端要求用户给予授权。

（B）用户同意给予客户端授权。

（C）客户端使用上一步获得的授权，向认证服务器申请令牌。

（D）认证服务器对客户端进行认证以后，确认无误，同意发放令牌。

（E）客户端使用令牌，向资源服务器申请获取资源。

（F）资源服务器确认令牌无误，同意向客户端开放资源。



### 以 github 为例

#### github 和 我网站之间的协商

这一步对应的是A之前。

如果我的网站可以使用github登录，Github 会要求我，先在它的平台上注册一个应用，在申请的时候标明需要获取用户信息的哪些权限，用多少就申请多少，并且在申请的时候填写你的网站域名，Github 只允许在这个域名中获取用户信息。

Github 会对用户的权限做分类，比如读取仓库信息的权限、写入仓库的权限、读取用户信息的权限、修改用户信息的权限等等。如果我想获取用户的信息，

此时我的网站已经和 Github 之间达成了共识，Github 也给我发了两张门票，**一张门票叫做 Client Id，另一张门票叫做 Client Secret。**



#### 用户和github之间的协商

用户进入我的网站，点击 github 登录按钮的时候，我的网站会把上面拿到的 Client Id 交给用户，让他进入到 Github 的授权页面，Github 看到了用户手中的门票，就知道这是我的网站让他过来的，于是它就把我的网站想要获取的权限摆出来，并询问用户是否允许我获取这些权限。(A)

我的网站此时向github的网络请求：

```
// 用户登录 github，协商
GET https://github.com/login/oauth/authorize

// 协商凭证
params = {
  client_id: "xxxx",
  redirect_uri: "http://my-website.com"
}
```

如果用户觉得我的网站要的权限太多，或者压根就不想我知道他这些信息，选择了拒绝的话，整个 OAuth 2.0 的认证就结束了，认证也以失败告终。

如果用户觉得 OK，在授权页面点击了确认授权后，页面会跳转到我预先设定的**`redirect_uri` 并附带一个盖了章的门票 code。** （B）

```
// 协商成功后带着盖了章的 code
Location: http://my-website.com?code=xxx
```

这个时候，用户和 Github 之间的协商就已经完成，**Github 也会在自己的系统中记录这次协商**，表示该用户已经允许在我的网站访问上直接操作和使用他的部分资源。



#### 我的网站拿到github的信息

上一步我们拿到了code, 只能表明，用户允许我的网站从 github 上获取该用户的数据，如果我直接拿这个 code 去 github 访问数据一定会被拒绝，因为任何人都可以持有 code，github 并不知道 code 持有方就是我本人。

还记得之前申请应用的时候 github 给我的两张门票么，Client Id 在上一步中已经用过了，接下来轮到另一张门票 Client Secret。

```json
POST https://github.com/login/oauth/access_token

// 协商凭证包括 github 给用户盖的章 code 和 github 发给网站的Client Secret
params = {
  code: "xxx",
  client_id: "xxx",
  client_secret: "xxx",
  redirect_uri: "http://my-website.com"
}

// 返回值： 拿到最后的绿卡
response = {
  access_token: "e72e16c7e42f292c6912e7710c838347ae178b4a"
  scope: "user,gist"
  token_type: "bearer",
  refresh_token: "xxxx"
}
```

对应上次的C，D步骤。

通过asscess_token 我们可以获取用户的信息，获取权限在scope中说明了，也就是只能获取user组和gist组两个小组的权限，user组包含了用户的名字和邮箱等信息。

```json
// 访问用户数据
GET https://api.github.com/user?access_token=e72e16c7e42f292c6912e7710c838347ae178b4a

// 告诉我用户的名字和邮箱
response = {
  username: "barretlee",
  email: "barret.china@gmail.com"
}
```

整个 OAuth2 流程在这里也基本完成了，文章中的表述很粗糙，比如 access_token 这个绿卡是有过期时间的，如果过期了需要使用 refresh_token 重新签证



### 认证模式

OAuth 2.0定义了四种授权方式。

- 授权码模式（authorization code）
- 简化模式（implicit）
- 密码模式（resource owner password credentials）
- 客户端模式（client credentials）

授权码模式
授权码（authorization code）方式，指的是第三方应用先申请一个授权码，然后再用该码获取令牌。

它是功能最完整、流程最严密安全的授权模式。它的特点就是通过客户端的 **后台服务器**，与"服务提供商"的认证服务器进行互动。 如上方的github。
授权码通过前端传送，令牌则是储存在后端，而且所有与资源服务器的通信都在后端完成。这样的前后端分离，可以避免令牌泄漏。 



简化模式（
有些 Web 应用是纯前端应用，没有后端。这时就不能用上面的方式了，必须将令牌储存在前端。RFC 6749 就规定了第二种方式，允许直接向前端颁发令牌。这种方式没有授权码这个中间步骤。

其他两个用的少。



### OAuth2的安全问题

state 值： https://juejin.im/post/5cc81d5451882524f72cd32c 




参考： 

https://www.zhihu.com/question/19781476 

 https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html 

 https://juejin.im/post/5cc81d5451882524f72cd32c 