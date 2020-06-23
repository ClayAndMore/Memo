
---
title: "CURL.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "CURL.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux, linux_software]

## CURL



### http动词

默认是GET, 使用 -X可以支持其他动词

`curl -X POST www.example.com`



### post

`-d = --data`

post 参数

`curl -d "user=xx&password=12345" url`

or:

`curl -d '{"username":"xyz","password":"xyz"}' url`

json 参数需要**单引号**括起来



post json文件

`curl --data @curl_post_apsc.json http://192.168.122.1/cloud3`



multipart/form-data格式 -F

```
curl -X POST http://10.98.131.145:8010/api/StatisticResult 
-F 'data=[{"key":"data","value":"[{\"key\":\"data\",\"value\":\"{\\\"aaa\\\":\\\"bbb\\\"}\",\"description\":\"\"}]","description":""}]' 
-F md5=666666
```







### https

`curl --insecure https://localhost/your_site/login_page  `







### 一些参数

-d/--data                             設定 http parameters 
-v/--verbose                       输出比较多的讯息
-u/--user                             使用者账号和密码



i 显示头信息(-I只显示头信息):

`curl -i www.javaranger.com`



`-X/--request [GET|POST|PUT|DELETE|…]  `

使用指定的http method发出 http request



#### 添加请求头

```python
curl -H 'Host: 1,1,1,1' -H 'Accept-Language：es' -H 'Cookie ID=1234'
```

加 json格式：

```
curl -H "Content-Type:application/json"  -X POST -d '{"md5":"ae4e71cdcd9d035e21825ea1d7eabcb6","data":"{\"trust\": \"no\"}"}' http://10.98.131.145:8010/api/StatisticResult
```





H发送post信息(-H是添加请求头， -d是请求体):

```
curl -H "Content-Type:application/soap+xml; charset=UTF-8" -d@/tmp/feiren http://113.105.64.226/v1/NorthBoundAPIService.asmx
```



#### 添加User Agent

```
curl --user-agent "[User Agent]"  www.javaranger.com
```



#### 添加cookie

```
curl --cookie "name=xxx" www.javaranger.com
```



### 显示通讯过程

包括头信息等。

` curl -v www.sina.com`





### 问题：

#### ` url: (6) Could not resolve host: application `

解决：

```
# NG
curl -H Content-Type: application/json ~
# OK
curl -H Content-Type:application/json ~
```



#### curl: (60) Peer's Certificate has expired.

可能是由于服务器时间不正确导致https证书认证错误，更新服务器时间即可

例:

`date -s “2017-4-25 12:00:00”`

或者

`ntpdate time.apple.com`

`ntpdate pool.ntp.org`

如果没有ntpdate:

`yum install -y ntpdate`