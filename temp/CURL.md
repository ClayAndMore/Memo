## CURL



### post

`-d = --data`

post 参数

`curl -d "user=xx&password=12345" url`

or:

`curl -d '{"username":"xyz","password":"xyz"}' url`

json 参数需要**单引号**括起来



post json文件

`curl --data @curl_post_apsc.json http://192.168.122.1/cloud3`



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



H发送post信息(-H是添加请求头， -d是请求体):

```
curl -H "Content-Type:application/soap+xml; charset=UTF-8" -d@/tmp/feiren http://113.105.64.226/v1/NorthBoundAPIService.asmx
```

添加User Agent

```
curl --user-agent "[User Agent]"  www.javaranger.com
```

添加cookie

```
curl --cookie "name=xxx" www.javaranger.com
```





### 问题：

` url: (6) Could not resolve host: application `

解决：

```
# NG
curl -H Content-Type: application/json ~
# OK
curl -H Content-Type:application/json ~
```

