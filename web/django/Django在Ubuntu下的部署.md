---
title: jjjj
date: 2017-05-05 13:11:53
categories:
header-img:
tags:
---

### Nginx

`apt-get install nginx`

启动，停止和重启

```
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
```

#### 配置转发

nginx的默认安装路径在/usr/local/nginx下. 
nginx的默认配置在/etc/nginx下.

把80端口指向8080端口, 方法如下:

修改nginx.conf：

最后http中会有以下两句：

`include /etc/nginx/conf.d/*.conf;`

`include /etc/nginx/sites-enabled/*;`

这样你就可以把已经配置好的各种 server conf 放在 sites-available 里.

默认情况下sites-enabled目录下会放一个sites-available/default的软链接,在sites-available/default已经对localhost进行设置, 导致无论你怎么修改nginx.conf对本地端口进行配置都不会生效. 一直报404错误.

所以此处要把sites-enabled注掉. 或者把该软链接换掉.



在该http配置项中添加以下内容：在上面两句后面，最后一句注释掉了：

```
server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://localhost:8080;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
```

重启nginx，这样在8080端口开启服务，外网也能访问了。




### 防火墙的开启

安装ufw :

`apt-get install ufw`

开启：

`sudo ufw enable`

 `sudo ufw default deny`

运行以上两条命令后，开启了防火墙，并在系统启动时自动开启。

打开或者关闭某个端口：

`sudo ufw allow|deny `

eg: `sudo ufw allow 22/tcp `       开通22端口

删除某条规则：

```
ufw delete allow 22
```

查看防火墙的状态：

`sudo ufw status`

关闭防火墙：

`sudo ufw disable`



### 开启安全组

记得去官网开启安全组



### django

Setting app 中记得加你云服务器IP.

`runserver 127.0.0.1`

这是允许本地访问，一般用nginx来跳转。

`runserver 0.0.0.0` 

这是所有ip都可以访问。



### uwsgi

通过pip 来安装：

`pip install uwsgi`

我们可以这样检测下安装的uwsgi:

```python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
```

运行：

`uwsgi --http :8000 --wsgi-file test.py`

访问本地8000端口，可以看到输出hello world(可以起另一个终端，用curl访问)



具体：http://www.cnblogs.com/fnng/p/5268633.html