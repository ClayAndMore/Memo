---
title: "计划任务 crontab"
date: 2018-07-07 17:53:13 +0800
lastmod: 2018-07-07 17:53:13 +0800
draft: true
tags: [""]
categories: ["linux"]
author: "Claymore"

---



## 计划任务crontab

我们会有写定期定时的任务。

该命令从输入设备读取指令，并将其放在crontab中，供之后读取和执行。

通常，crontab储存的指令被守护进程激活，crond为其守护进程，常常在后台执行，每一分钟会检查一次是否有预定的作业要执行。

* 启动日志rsyslog

  启动日志来看我们的任务是否真的被执行

  `sudo service rsyslog start`

* 启动crontab

  `sudo cron -f &`

* 查看添加了那些任务

  `crontab -l`

  虽然我们添加了任务，但是cron的守护进程没有启动不会检测到有任务，我们可以通过下面两种方式来确定我们的cron是否在后台启动：

  `pa aux | grep cron`

  `pgrep cron`

* 看执行任务命令在日志的信息

  `sudo tail -f /var/log/syslog`

* 删除任务

  `crontab -r`

### 添加任务

添加一个计划任务

`crontab -e`

第一次启动会让你选择一个编辑器，我们选择vim

后续会进入到一个编辑界面，这边是添加计划的地方，与一般的配置文档相同，以#开头的是注释, 进来是一堆注释，可以在注释中看到一个例子：

```
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/ 
```

它的意思是每周一5点执行

规则如下：

``` 
分     小时    日       月       星期     命令
 0-59   0-23   1-31   1-12     0-6     command     
 (取值范围,0表示周日， 一般一行对应一个任务)
 记住几个特殊符号的含义:

 “*”代表取值范围内的数字, 任何时候都匹配
 “/”代表”每”,
 “-”代表从某个数字到某个数字,
 “,”分开几个离散的数字
```

为了方便记忆，前面五个数字可以记成：minute hour day month week (美好日月星辰)

一些例子：

``` sh

# 每晚21:30 重启apache
30 21 * * * service httpd restart      
# 每月1、10、21日的4:45重启apache
45 4 1,10,21 * * service httpd restart

# 每月 1到10日的4:45 重启 apache 
45 4 1-10 * * service httpd restart
      
# 每隔2分钟重启apache
(偶数)  */2 * * * * service httpd restart
(奇数)  1-59/2 * * * * service httpd restart

# 晚上11点到早上7点之间，每隔一小时重启apache
0 23-7/1 * * * service httpd restart
     
# 每天18:00 至 23:00 之间每隔30分钟重启apache
0,30 18-23 * * * service httpd restart
0-59/30 18-23 * * * service httpd restart

# 半分钟执行一次
*/1 * * * * date>> tmp/date.log
*/1 * * * * sleep30;date>> tmp/date.log
```





### 系统的默认定时

每次用`crontab -e`都会添加计划任务，都会在/var/spool/cron/crontabs中添加一个该用户自己的任务文档。这样是为了隔离

所以，**系统级别的任务需要sudo权限编辑/etc/crontab文件就可以。**

cron 服务监测时间最小单位是分钟，所以 cron 会每分钟去读取一次 /etc/crontab 与 /var/spool/cron/crontabs 里面的內容。

在 /etc 目录下，cron 相关的目录有下面几个：

```
# ls /etc/cron.
cron.d/       cron.daily/   cron.hourly/  cron.monthly/ cron.weekly/
```

每个目录的作用：

1. /etc/cron.daily，目录下的脚本会每天执行一次，在每天的6点25分时运行；
2. /etc/cron.hourly，目录下的脚本会每个小时执行一次，在每小时的17分钟时运行；
3. /etc/cron.mouthly，目录下的脚本会每月执行一次，在每月1号的6点52分时运行；
4. /etc/cron.weekly，目录下的脚本会每周执行一次，在每周第七天的6点47分时运行；

系统默认执行时间可以根据需求进行修改。



### 检测 crontab 是否正常运行

1.看日志，cat /var/log/cron。如果日志中有执行记录。
 2.检查执行权限，要赋予执行权限，如 chmod +x xxx.sh   就是给xxx.sh这个脚本赋予执行权限。
 3.确保能在当前用户下面正确执行。
 4.检查用户到命令，因为crontab里面用不到当前用户的环境变量，所以在命令行里面一定要用全路径
 5.看日志，cat /var/log/cron，没有脚本执行记录，crontab -l 查看列表没问题，这时可能的原因是，编辑定时任务时带了中文空格，最好的解决办法crontab -e进入编辑界面，把任务删了重新写一遍，切记，一定不能带中文。

检测

``` sh
# 检测crontab是否在test.txt文件中写入数据
*/1 * * * * root echo 111 >> /tmp/test.txt
```

