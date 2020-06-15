
---
title: "LEK.md"
date: 2019-10-21 09:53:02 +0800
lastmod: 2019-10-25 17:50:12 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
### ELK



前提 下载java 配置 java 的环境变量。

```bash
export JAVA_HOME=/opt/jdk1.8.0_211
export PATH=$PATH:$JAVA_HOME/bin
```

安装和配置ES, 详见同级文章安装和配置ES.

所有下载项均可在： https://elasticsearch.cn/download/ 找到。



### logstash

 ` logstash [lɔɡ] [stæ:ʃ] `

Logstash 是开源的服务器端数据处理管道，能够同时从多个来源采集数据，转换数据，然后将数据发送到您最喜欢的“存储库”中。 官方对Logstash很直观的一个描述，Logstash其实就是一个管道（Pipeline）。

下载 logstash，并配置环境变量

```bash
export LOGSTASH_HOME=/opt/logstash-7.4.0
export PATH=$PATH:$LOGSTASH_HOME/bin
```
验证：
```sh
# logstash -V
logstash 7.4.0

# bin/logstash -e 'input { stdin {} } output { stdout {} }'
```

 -e 的意思是允许你从命令行指定配置 



#### 配置文件

看下 config/logstash-sample.conf:

```
input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    #user => "elastic"
    #password => "changeme"
  }
```

 Logstash 分为 Input、Output、Filter、Codec 等多种plugins。

* Input：数据的输入源也支持多种插件，如elk官网的beats、file、graphite、http、kafka、redis、exec等。
* Output：数据的输出目的也支持多种插件，如本文的elasticsearch，当然这可能也是最常用的一种输出。以及exec、stdout终端、graphite、http、zabbix、nagios、redmine等。
* Filter：使用过滤器根据日志事件的特征，对数据事件进行处理过滤后，在输出。支持grok、date、geoip、mutate、ruby、json、kv、csv、checksum、dns、drop、xml等。
* Codec：编码插件，改变事件数据的表示方式，它可以作为对输入或输出运行该过滤。和其它产品结合，如rubydebug、graphite、fluent、nmap等。



 两个必需的元素，输入和输出，以及可选元素过滤器 等



#### 语法

Logstash 设计了自己的 DSL —— 有点像 Puppet 的 DSL，或许因为都是用 Ruby 语言写的吧 —— 包括有区域，注释，数据类型(布尔值，字符串，数值，数组，哈希)，条件判断，字段引用等。

Logstash 用 {} 来定义区域，区域内可以包括插件区域定义，你可以在一个区域内定义多个插件。插件区域内则可以定义键值对设置。

| 类型   | 示例                                              |
| ------ | ------------------------------------------------- |
| bool   | debug=>true                                       |
| bytes  | my_bytes => "113" # 113 bytes                     |
| string | host => "hostname"                                |
| number | port => 214                                       |
| array  | match =>[ "/var/log/messages", "/var/log/*.log" ] |
| hash   | options => {key1 => "value1",key2 => "value2" }   |

条件判断：

```
等于	==
不等于	!=
小于	<
大于	>
小于等于	<=
大于等于	>=
匹配正则	=~
不匹配正则	!~
包含	in
不包含	not in
与	and
或	or
非与	nand
非或	xor
复合表达式	()
取反符合	!()
```








#### sample nginx 

```
> cd logstash-7.4.0/config  
> vim logstash-nginx.conf    # 创建一个叫logstash-nginx.conf的配置文件
```

logstash-nginx.conf文件的内容是

```
input {
  file {
        path => [ "/var/log/nginx/access.log" ]   # nginx日志的目录
        start_position => "beginning"  # 从文件开头采集
    }
}
filter {
  #Only matched data are send to output.
}
output {
  elasticsearch {
    action => "index"          #The operation on ES
    hosts  => "127.0.0.1:9200"   #ElasticSearch host, can be array.
    index  => "applog"         # 创建一个ES的index
  }
}
```

执行：bin/logstash -f config/logstash-nginx.conf



### kibana

读音：

 `kibana* [kɪbana] kei ba na`

推荐它的版本和es的版本尽量保持一致。



还是配置环境变量：



配置：

```
vim kibana-7.4.0-linux-x86_64/config/kibana.yml

#server.host: "localhost"
server.host: 0.0.0.0
```

开启默认端口的访问权限：

` iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 5601 -j ACCEPT`



启动：

```
root@ubuntu:/opt/ELK# kibana-7.4.0-linux-x86_64/bin/kibana
Kibana should not be run as root.  Use --allow-root to continue.

root@buntu:/opt/ELK# kibana-7.4.0-linux-x86_64/bin/kibana --allow-root
```



### nginx example

```
[root@log-monitor ~]# cat nginx_access.conf
input {
    file {
        path => [ "/data/nginx-logs/access.log" ]
        start_position => "beginning"
        ignore_older => 0
    }
}

filter {
    grok {
        match => { "message" => "%{NGINXACCESS}" }

    }
    geoip {
      source => "http_x_forwarded_for"
      target => "geoip"
      database => "/etc/logstash/GeoLiteCity.dat"
      add_field => [ "[geoip][coordinates]", "%{[geoip][longitude]}" ]
      add_field => [ "[geoip][coordinates]", "%{[geoip][latitude]}" ]
    }

    mutate {
      convert => [ "[geoip][coordinates]", "float" ]
      convert => [ "response","integer" ]
      convert => [ "bytes","integer" ]
      replace => { "type" => "nginx_access" }
      remove_field => "message"
    }

    date {
      match => [ "timestamp","dd/MMM/yyyy:HH:mm:ss Z"]

    }
    mutate {
      remove_field => "timestamp"
    }

}
output {
    elasticsearch {
        hosts => ["127.0.0.1:9200"]
        index => "logstash-nginx-access-%{+YYYY.MM.dd}"
    }
    stdout {codec => rubydebug}
}
```

解释：

```
input：
　file：使用file 作为输入源
　　path： 日志的路径，支持/var/log*.log，及[ "/var/log/messages", "/var/log/*.log" ] 格式
　　start_position: 从文件的开始读取事件。另外还有end参数
　　ignore_older: 忽略早于24小时（默认值86400）的日志，设为0，即关闭该功能，以防止文件中的事件由于是早期的被logstash所忽略。

filter：
　grok：数据结构化转换工具
　match：匹配条件格式，将nginx日志作为message变量，并应用grok条件NGINXACCESS进行转换
　
　geoip：该过滤器从geoip中匹配ip字段，显示该ip的地理位置
　　source：ip来源字段，这里我们选择的是日志文件中的最后一个字段，如果你的是默认的nginx日志，选择第一个字段即可(注：这里写的字段是/opt/logstash/patterns/nginx 里面定义转换后的)
　　target：指定插入的logstash字断目标存储为geoip
　　database：geoip数据库的存放路径
　　add_field: 增加的字段，坐标经度
　　add_field: 增加的字段，坐标纬度
　mutate： 数据的修改、删除、类型转换
　　convert： 将坐标转为float类型
　　convert： http的响应代码字段转换成 int
　　convert： http的传输字节转换成int
　　replace： 替换一个字段
　　remove_field： 移除message 的内容，因为数据已经过滤了一份，这里不必在用到该字段了。不然会相当于存两份
　date: 时间处理，该插件很实用，主要是用你日志文件中事件的事件来对timestamp进行转换，导入老的数据必备！
　　match：匹配到timestamp字段后，修改格式为dd/MMM/yyyy:HH:mm:ss Z
　mutate：数据修改
　　remove_field： 移除timestamp字段。

output段：
　elasticsearch：输出到es中
　　host： es的主机ip＋端口或者es 的FQDN＋端口
　　index： 为日志创建索引logstash-nginx-access-*，这里也就是kibana那里添加索引时的名称
```





### 参考

 https://my.oschina.net/niejimao/blog/819259 