

---
title: "nginx日志采集.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-10-16 18:06:24 +0800
draft: false
tags: ["linux软件"]
categories: ["linux"]
author: "Claymore"

---


### 获取远端真实ip

```nginx
  location /
        {
            proxy_pass http://172.17.0.1:8000;
            proxy_set_header        Host            $host;
            proxy_set_header        X-Real-IP       $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```





### 日志配置

默认：

```nginx
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for" $request_time';

    access_log  /var/log/nginx/access.log  main;
...
}
```

日志输出：

```
222.128.57.34 - - [15/May/2019:06:23:26 +0000] "GET /static/css/bootstrap-treeview.css HTTP/1.1" 200 1149 "https://claymore.wang/p/post/content/PyPy.md/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36" "-"

222.128.57.37 - - [15/May/2019:06:23:28 +0000] "GET /static/js/themes/a.min.css HTTP/1.1" 200 46 "https://claymore.wang/p/post/content/PyPy.md/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36" "-"
222.128.57.37 - - [15/May/2019:06:23:28 +0000] "GET /static/js/themes/bootstrap-responsive.min.css HTTP/1.1" 200 15961 "https://claymore.wang/p/post/content/PyPy.md/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36" "-"
```

access.log文件里面的$1、$2...对应于nginx配置文件里面的`$remote_addr、$remote_use` 。

含义解释：

1. remote_addr : 客户端地址
2. remote_user : 客户端用户名
3. time_local : 服务器时间
4. request : 请求内容，包括方法名，地址，和http协议
5. http_host : 用户请求是使用的http地址
6. status : 返回的http 状态码
7. request_length : 请求大小
8. body_bytes_sent : 返回的大小
9. http_referer : 来源页
10. http_user_agent : 客户端名称
11. request_time : 整体请求延时



### 统计访问量

几个概念：

**PV（Page View）**：即页面浏览量或者点击量，用户每一次对网站中每个页面访问均记录1个PV。用户对同一页面的多次访问，访问量累积。

**UV（Unique Visitor）**：指通过互联网浏览这个网页的人，电脑称为一个访客、手机也称为一个访客，一天之内相同的客户端只能被计算一次。

**IP（Internet Protocol）**：指独立IP访问站点的IP总数，一天内相同IP只能算一次。

**VV（Visit View）**：指所有访客一天内访问网站的次数，当访客完成所有浏览并最终关闭网站的所有页面时变完成了一次访问，同一访客一天内可能有多次访问行为，访问次数累积。



**查看各个访问量：**

**1.根据访问IP统计UV**

```
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $1}' access.log|sort | uniq -c |wc -l
2
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $1}' access.log|sort | uniq -c
      9 222.128.57.34
     14 222.128.57.37
```



**2.统计访问URL统计PV**

```
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $7}' access.log|wc -l
23
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $7}' access.log
/p/post/content/PyPy.md/
/favicon.ico
/p/post/content/PyPy.md/
/static/css/bootstrap.min.css
/static/css/strapdown.css
/static/js/jquery-3.1.1.min.js
/static/js/bootstrap-treeview.js
/static/js/strapdown.js
...
```



**3.查询访问最频繁的URL**

```
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $7}' access.log|sort | uniq -c |sort -n -k 1 -r|more
      2 /static/js/jquery-3.1.1.min.js
      2 /static/js/bootstrap.min.js
      2 /static/css/strapdown.css
      2 /static/css/bootstrap.min.css
      2 /p/post/content/PyPy.md/
      1 /static/wechar.png
      1 /static/js/themes/bootstrap-responsive.min.css
      1 /static/js/themes/a.min.css
      1 /static/js/strapdown.js
```



**4.查询访问最频繁的IP**

```
root@VM-0-6-ubuntu:~/nginx/logs# awk '{print $1}' access.log|sort | uniq -c |sort -n -k 1 -r|more
     14 222.128.57.37
      9 222.128.57.34
```



**5.根据时间段统计查看日**志

```
cat  access.log| sed -n '/15\/May\/2019:06/,/15\/May\/2019:07/p'|more
```







针对每天的访问信息写一个脚本，并将统计信息输出到/pv.html文件里面，之保留30天的信息。方便直接浏览此页面查看，但要限制特定IP才能访问此页面，其他IP的403!

```
year=`date +%Y`  
month=`date +%m`
datedate=`date +%F`
date=`date +%Y%m%d`

pv=`awk '{print $7}' /xx/logs/nginx/xxx/"$year"/"$month"/"$datedate"-access.log | wc -l`
ip=`awk '{print $1}' /xx/logs/nginx/xxx/"$year"/"$month"/"$datedate"-access.log | sort -n | uniq -c | wc -l`

echo -e "\n$date Pv is $pv;; $date Ip is $ip.." >> /xx/xxx/pv.htm l sort -rn /xx/xxx/pv.html | sed -i '31d' /xx/xxx/pv.html | sort -r

此外还要修改nginx配置文件：
location = /pv.html {
 allow  xxx.xxx.xxx.xxx;
 deny allow;
}

nginx -r
dervice nginx reload

最后，将pv.sh加入定时任务：

crontab -e

```
