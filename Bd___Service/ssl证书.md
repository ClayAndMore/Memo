Tags:[linux, linux_software]

### SSL证书



#### 查看

1. 浏览器, 输入框左侧

2. openssl 工具:

   ```
   [llmode@cert]# openssl x509 -in signed.crt -noout -dates #signed.crt为证书
    
   notBefore=Nov 21 15:13:14 2017 GMT
   notAfter=Feb 19 15:13:14 2018 GMT
   ```

   ​

#### nginx 配置

```nginx
server
{
        listen       443;
        ssl                  on;
        ssl_certificate      nginx.crt;
        ssl_certificate_key  nginx.key;
        #via https://www.wosign.com/support/Nginx.html
        server_name  localhost;
        client_max_body_size 100m;
      
```

这个nginx.crt 和 nginx.key 是和nginx.conf 同级的文件目录, 这里也可以填写绝对路径.



#### 自行颁发不受浏览器信任的SSL证书

```
# 生成一个RSA密钥 
$ openssl genrsa -des3 -out 33iq.key 1024
 
# 拷贝一个不需要输入密码的密钥文件
$ openssl rsa -in 33iq.key -out 33iq_nopass.key
 
# 生成一个证书请求
$ openssl req -new -key 33iq.key -out 33iq.csr
 
# 自己签发证书
$ openssl x509 -req -days 365 -in 33iq.csr -signkey 33iq.key -out 33iq.crt
```

第3个命令是生成证书请求，会提示输入省份、城市、域名信息等，重要的是，email一定要是你的域名后缀的。

我们可以不用第三步,  csr是提交给 ssl 提供商的, 如果没有第三步, 

直接给自己签发证书:

```

```





#### 受信任的证书

要获取受浏览器信任的证书，则需要到证书提供商处申请。证书授证中心，又叫做CA机构，为每个使用公开密钥的用户发放一个数字证书。浏览器在默认情况下内置了一些CA机构的证书，使得这些机构颁发的证书受到信任。[VeriSign](http://www.verisign.com/cn/)即是一个著名的国外CA机构，工行、建行、招行、支付宝、财付通等网站均使用VeriSign的证书，而网易邮箱等非金融网站采用的是中国互联网信息中心 CNNIC颁发的SSL证书。一般来说，一个证书的价格不菲，以VeriSign的证书为例，价格在每年8000元人民币左右。

据说也有免费的证书可以申请。和VeriSign一样，[StartSSL](http://www.startssl.com/)也 是一家CA机构，它的根证书很久之前就被一些具有开源背景的浏览器支持（Firefox浏览器、谷歌Chrome浏览器、苹果Safari浏览器等）。后 来StartSSL竟然搞定了微软：在升级补丁中，微软更新了通过Windows根证书认证（Windows Root Certificate Program）的厂商清单，并首次将StartCom公司列入了该认证清单。现在，在Windows 7或安装了升级补丁的Windows Vista或Windows XP操作系统中，系统会完全信任由StartCom这类免费数字认证机构认证的数字证书，从而使StartSSL也得到了IE浏览器的支持。