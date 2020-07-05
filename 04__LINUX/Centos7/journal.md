---
title: "centos7 journal.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-03-26 18:40:49 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---


### 命令格式

```sh 
journalctl [-nrpf] [--since TIME] [--until TIME] _optional
选项与参数：
默认会秀出全部的 log 内容，从旧的输出到最新的讯息
-n ：秀出最近的几行的意思～找最新的信息相当有用
-r ：反向输出，从最新的输出到最旧的数据
-p ：指定日志等级
-u --unit=UNIT           Show logs from the specified unit
-f ：类似 tail -f 的功能，持续显示 journal 日志的内容（实时监测时相当有帮助！）
--since --until：设置开始与结束的时间，让在该期间的数据输出而已
  -S --since=DATE          Show entries not older than the specified date
  -U --until=DATE          Show entries not newer than the specified date
_SYSTEMD_UNIT=unit.service ：只输出 unit.service 的信息而已
_COMM=bash ：只输出与 bash 有关的信息
_PID=pid ：只输出 PID 号码的信息
_UID=uid ：只输出 UID 为 uid 的信息
SYSLOG_FACILITY=[0-23] ：使用 syslog.h 规范的服务相对序号来调用出正确的数据！
```



**指定错误等级：**

找出讯息严重等级为错误 （error） 的讯息！

`journalctl -p err`

**.查看指定服务的日志**

journalctl /usr/lib/systemd/systemd

**.查看指定进程的日志**

journalctl  _PID=1

**.查看某个路径的脚本的日志**

journalctl  /usr/bin/bash 

**.查看某个Unit的日志**

journalctl -u nginx.service

journalctl -u nginx.service --since today

实时滚动显示某个Unit的最新日志：

journalctl -u nginx.service -f

**.以JSON格式（多行）输出**，可读性更好，建议选择多行输出

journalctl -b -u httpd.service -o json-pretty



只找出 crond.service 的数据，同时只列出最新的 10 笔即可
`journalctl _SYSTEMD_UNIT=crond.service -n 10`



时间：

```sh
# 仅显示出 2015/08/18 整天
journalctl --since "2015-08-18 00:00:00" --until "2015-08-19 00:00:00"
# 仅显示出今天
journalctl --since today
# 仅显示出昨天的数据日志内容
journalctl --since yesterday --until today
```





#### 重启

`systemctl restart systemd-journald`

有时新加的服务没有详细的日志输出，你可能需要重启一下



### 日志位置

``` sh
[root@10.250.123.10 centos7]#ls /run/log
journal
[root@10.250.123.10 centos7]#ls /run/log/journal/
13f96ca8cf154bc9ae48fc698a0b2436
[root@10.250.123.10 centos7]#ls /run/log/journal/13f96ca8cf154bc9ae48fc698a0b2436/
system@71fc63abe0964300a6b770aa02470b29-00000000003b88cc-0005abf727bd11e5.journal
system@71fc63abe0964300a6b770aa02470b29-00000000003dcc14-0005ac02effcaf76.journal
.....
system@71fc63abe0964300a6b770aa02470b29-000000000082769b-000590ba340775a8.journal
system.journal
```

