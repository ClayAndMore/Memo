
---
title: "nginx配置https.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "nginx配置https.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[nginx, linux_software]

### SSL证书



#### 查看

1. 浏览器, 输入框左侧

2. openssl 工具:

   ```
   [llmode@cert]# openssl x509 -in signed.crt -noout -dates #signed.crt为证书
    
   notBefore=Nov 21 15:13:14 2017 GMT
   notAfter=Feb 19 15:13:14 2018 GMT
   ```




#### 自行颁发不受浏览器信任的SSL证书

```
# 生成一个CA的RSA私钥, 这里需要我们输入两次密码 
$ openssl genrsa -des3 -out server.key 1024
 
# 生成一个证书请求，输入刚才输入的密码
$ openssl req -new -key server.key -out server.csr
 
# 去除 key 的密码：
cp server.key server.origin
openssl rsa -in server.origin -out server.key # 输入之前的密码

# 自己签发证书，
$ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# ls 
server.crt  server.csr  server.key  server.key.origin
```

第2步是生成证书请求，会提示输入省份、城市、域名信息等，重要的是，email一定要是你的域名后缀的。还会让你输入密码，我们可以不填



#### nginx 配置

```nginx
server
{
        listen       443;      # listen 443 ssl; 这种方式在新版推荐。
        ssl                  on;
        ssl_certificate      nginx.crt;
        ssl_certificate_key  nginx.key;
 
}     
```

这个nginx.crt 和 nginx.key 是和nginx.conf 同级的文件目录, 这里也可以填写绝对路径.



#### 受信任的证书

要获取受浏览器信任的证书，则需要到证书提供商处申请。证书授证中心，又叫做CA机构，为每个使用公开密钥的用户发放一个数字证书。浏览器在默认情况下内置了一些CA机构的证书，使得这些机构颁发的证书受到信任。[VeriSign](http://www.verisign.com/cn/)即是一个著名的国外CA机构，工行、建行、招行、支付宝、财付通等网站均使用VeriSign的证书，而网易邮箱等非金融网站采用的是中国互联网信息中心 CNNIC颁发的SSL证书。一般来说，一个证书的价格不菲，以VeriSign的证书为例，价格在每年8000元人民币左右。

据说也有免费的证书可以申请。和VeriSign一样，[StartSSL](http://www.startssl.com/)也 是一家CA机构，它的根证书很久之前就被一些具有开源背景的浏览器支持（Firefox浏览器、谷歌Chrome浏览器、苹果Safari浏览器等）。后 来StartSSL竟然搞定了微软：在升级补丁中，微软更新了通过Windows根证书认证（Windows Root Certificate Program）的厂商清单，并首次将StartCom公司列入了该认证清单。现在，在Windows 7或安装了升级补丁的Windows Vista或Windows XP操作系统中，系统会完全信任由StartCom这类免费数字认证机构认证的数字证书，从而使StartSSL也得到了IE浏览器的支持。



### 80 转 443

```nginx
server {
    listen       443 ssl;
    server_name  域名;
    charset utf-8;
    access_log  /var/log/nginx/webhook.iminho.me/access.log;
    add_header X-Xss-Protection 1;
    ssl_certificate /etc/nginx/cert/证书.pem;
    ssl_certificate_key /etc/nginx/cert/证书.key;

    location / {
        try_files /_not_exists_ @backend;
    }
    location @backend {
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host            $http_host;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name 域名;
    rewrite ^(.*)$ https://${server_name}$1 permanent;
}
```





### 问题

#### cannot load certificate key 

```
看nginx日志：
cannot load certificate key "/etc/nginx/ssl/server.key": PEM_read_bio_PrivateKey() failed (SSL: error:2807106B:UI routines:UI_process:processing error:while reading strings error:0906406D:PEM routines:PEM_def_callback:problems getting password error:0906A068:PEM routines:PEM_do_header:bad password read)
```

很有可能是你的key有密码，没有像上面那样去掉密码。