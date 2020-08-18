
---
title: "suricat 日志到influxdb.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "suricat 日志到influxdb.md"
date: 2020-06-12 19:01:02 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## suricat 日志到 influxdb.

参考：https://www.influxdata.com/blog/network-security-monitoring-with-suricata-and-telegraf/

前提，下载好suricata 和 telegraf 和 influxdb

https://fauie.com/2016/06/27/suricata-stats-to-influx-dbgrafana/, 这个用了 logstash ,时间比较久，logstash 比较重。



### 配置 Suricata 

vim /etc/suricata/suricata.yaml:

``` sh
- eve-log:
    enabled: yes
    filetype: unix_stream
    filename: /tmp/suricata-stats.sock
    types:
      - stats:
         threads: yes
```

再添加一组 -eve-log 和原来的并列，这样可以输出到sock同时输出到json文件。

我们可以用 来建立一个 socket :`nc -U -l /tmp/suricata-stats.sock` 监听这个socket, 启动suricata， 看nc这边的输出。



### 配置 Telegraf 的 Suricata Input Plugin

https://github.com/influxdata/telegraf/tree/master/plugins/inputs/suricata

打开 输入插件： vim /etc/telegraf/telegraf.conf:

``` sh
[[input.suricata]]
  ## Data sink for Suricata stats log.
  # This is expected to be a filename of a
  # unix socket to be created for listening.
  source = "/tmp/suricata-stats.sock"

  # Delimiter for flattening field keys, e.g. subitem "alert" of "detect"
  # becomes "detect_alert" when delimiter is "_".
  delimiter = "_"
```

插件报告了Suricata IDS/IPS引擎的内部性能计数器，例如捕获的流量、内存使用、正常运行时间、流量计数器等等。它为Suricata日志输出提供了一个套接字，以便将JSON统计输出写入其中，并处理传入的数据以符合Telegraf的格式。

后续要整理出自己想要的字段。



### 输出 

启动suricata, 观察 influxdb 日志：

``` sh
root@node201:~# journalctl -u influxdb -f
-- Logs begin at Tue 2020-03-17 22:30:28 CST. --
May 29 18:10:40 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:10:40 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" a5f98650-a194-11ea-964a-000000000000 141113
May 29 18:10:50 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:10:50 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" abef27a0-a194-11ea-964b-000000000000 58239
May 29 18:11:00 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:00 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" b1e4dc84-a194-11ea-964c-000000000000 92939
May 29 18:11:10 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:10 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" b7daed1b-a194-11ea-964d-000000000000 258950
May 29 18:11:20 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:20 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" bdd0c474-a194-11ea-964e-000000000000 125664
May 29 18:11:30 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:30 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" c3c6d170-a194-11ea-964f-000000000000 291336
May 29 18:11:40 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:40 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" c9bc83d3-a194-11ea-9650-000000000000 51888
May 29 18:11:50 node201 influxd[863]: [httpd] 127.0.0.1 - - [29/May/2020:18:11:50 +0800] "POST /write?db=suricata_test HTTP/1.1" 204 0 "-" "Telegraf/1.14.3" cfb31831-a194-11ea-9651-000000000000 46730
```





## 问题 

### /tmp/suricata-stats.sock no such file

suricata 和 telegraf 都配置了 socket 文件，但是对都不会主动去建立该sock文件，我们需要自己创建。

可以使用 nc 创建： `nc -U -l /tmp/suricata-stats.sock`， 

使用 unlink 可以删掉sock文件。

实际上telegraf可以创建sock，不过指定目录为/tmp下，不然一般容易出现权限问题。



### Telegraf sock bind: address already in use

当我们修改Telegraf 配置文件，systemctl restart telegraf ，重启telegraf , systemctl status telegraf 显示重启失败。

观察日志 journalctl -u telegraf.service -f ：

``` sh
ay 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Starting Telegraf 1.14.3
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Loaded inputs: cpu kernel swap suricata system disk diskio mem processes
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Loaded aggregators:
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Loaded processors:
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Loaded outputs: influxdb
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! Tags enabled: host=node201
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z I! [agent] Config: Interval:10s, Quiet:false, Hostname:"node201", Flush Interval:10s
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z E! [agent] Service for [inputs.suricata] failed to start: listen unix /tmp/suricata-stats.sock: bind: address already in use
May 28 18:07:28 node201 telegraf[6533]: 2020-05-28T10:07:28Z E! [telegraf] Error running agent: listen unix /tmp/suricata-stats.sock: bind: address already in use
May 28 18:07:28 node201 systemd[1]: telegraf.service: Main process exited, code=exited, status=1/FAILURE
May 28 18:07:28 node201 systemd[1]: telegraf.service: Failed with result 'exit-code'.
May 28 18:07:29 node201 systemd[1]: telegraf.service: Service RestartSec=100ms expired, scheduling restart.
May 28 18:07:29 node201 systemd[1]: telegraf.service: Scheduled restart job, restart counter is at 5.
May 28 18:07:29 node201 systemd[1]: Stopped The plugin-driven server agent for reporting metrics into InfluxDB.
May 28 18:07:29 node201 systemd[1]: telegraf.service: Start request repeated too quickly.
May 28 18:07:29 node201 systemd[1]: telegraf.service: Failed with result 'exit-code'.
May 28 18:07:29 node201 systemd[1]: Failed to start The plugin-driven server agent for reporting metrics into InfluxDB.
```

显示我的 /tmp/suricata-stats 已经被占用，可以用 netstats 抓一下 ，看是哪个程序占用，但是没有找到相关进程，也用 losf 抓过。

可以尝试使用 `unlink [SOCKET NAME]`, 来释放该 socket

重启机器，可以看到 teleraf 的日志正常。