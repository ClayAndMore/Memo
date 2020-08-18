---
title: "JWT.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["网络原理"]
author: "Claymore"

---


### 结构

json web token

一直token 的格式, 结构： `xxxxx.yyyyy.zzzzz`

header.playload.signatrue

如：`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VySWQiOjEyMywiVXNlck5hbWUiOiJhZG1pbiJ9.Qjw1epD5P6p4Yy2yju3-fkq28PddznqRj3ESfALQy_U`

- header

  ```
  {
    "alg": "HS256",  # 加密算法
    "typ": "JWT"     # token类型
  }
  ```

  base64后成jwt结构的第一部分

- Payload负载

  ```python
  {
      "iss": "lion1ou JWT", # 签发者
      "iat": 1441593502,    # 签发时间
      "exp": 1441594722,    # 过期时间
      "aud": "www.example.com", # 接受方
      "sub": "lion1ou@163.com"  # 面向的用户
  }
  ```

  这些都是预定义的字段，官方推荐最好使用上述字段， 还可以增加你自己想增的字段。

  这里也用base64编码组成第二部分

- Signature 签名

  前面两部分都是使用 Base64 进行编码的，即前端可以解开知道里面的信息。Signature 需要使用编码后的 header 和 payload 以及我们提供的一个密钥，然后使用 header 中指定的签名算法（HS256）进行签名(非对称）。**签名的作用是保证 JWT 没有被篡改过。**

  具体可参考rsa库。

### 优点特性

1. 负载中保留了信息， 不能被篡改，还带时间用来做过期认证。

    这样我们可以省去数据库。

2. 一般讲改token增加到header中， 便于其他设备后台验证， 简洁了url

3. 在通信的双方之间使用JWT对数据进行编码是一种非常安全的方式，由于它的信息是经过签名的，可以确保发送者发送的信息是没有经过伪造的。



但是负载内容是可被看的， 不能穿隐私信息。