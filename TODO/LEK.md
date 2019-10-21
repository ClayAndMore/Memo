### logstash

Logstash 是开源的服务器端数据处理管道，能够同时从多个来源采集数据，转换数据，然后将数据发送到您最喜欢的“存储库”中。

下载java 配置 java 的环境变量。

下载 logstash，并配置环境变量

```bash
export JAVA_HOME=/root/ELK/jdk1.8.0_211
export PATH=$PATH:$JAVA_HOME/bin

export LOGSTASH_HOME=/root/ELK/logstash-7.4.0
export PATH=$PATH:$LOGSTASH_HOME/bin
```
验证：
```sh
# logstash -V
logstash 7.4.0
```



### Elasticsearch 

https://www.elastic.co/cn/products/elasticsearch