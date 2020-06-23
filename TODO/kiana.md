
---
title: "kiana.md"
date: 2019-10-25 17:50:12 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "kiana.md"
date: 2019-10-25 17:50:12 +0800
lastmod: 2019-10-25 17:50:12 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
根据官方样例：

 https://www.elastic.co/guide/cn/kibana/current/tutorial-load-dataset.html 



### 导入数据

解压样本：

```sh
# gunzip logs.jsonl.gz
# ls
accounts.zip  logs.jsonl  shakespeare_6.0.json
# unzip accounts.zip
# ls
accounts.json  accounts.zip  logs.jsonl  shakespeare_6.0.json
```



设置映射：

 **映射把索引中的文档按逻辑分组并指定了字段的属性，比如字段的可搜索性或者该字段是否是 *tokenized* ，或分解成单独的单词。** 

```sh
elsearch@10.250.123.10 root $ curl -X PUT "localhost:9200/shakespeare?pretty" -H 'Content-Type: application/json' -d'
{
 "mappings": {
   "properties": {
    "speaker": {"type": "keyword"},
    "play_name": {"type": "keyword"},
    "line_id": {"type": "integer"},
    "speech_number": {"type": "integer"}
   }
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "shakespeare"
}
```

- 因为 *speaker* 和 *play_name* 字段是关键字字段，它们不需要分析。字符串即使包含多个词也仍被视为一个整体。
- *line_id* 和 *speech_number* 字段是整数。

es版本7后的导入映射的形式不一样：

```
"mappings":{    
      "books":{     
        "properties":{        
            "title":{"type":"text"},
            "name":{"type":"text","index":false}
            }}}}

变为：

"mappings":{    
        "properties":{        
            "title":{"type":"text"},
            "name":{"type":"text","index":false},
		   }}}}
```





日志数据集映射需要利用 `geo_point` 类型来标记经度/纬度地理位置字段。

使用下面的命令来为日志建立 `geo_point` 映射:

```sh
 # curl -X PUT "localhost:9200/logstash-2015.05.18?pretty" -H 'Content-Type: application/json' -d'
{
  "mappings": {
      "properties": {
        "geo": {
          "properties": {
            "coordinates": {
              "type": "geo_point"
            }
          }
        }
    }
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "logstash-2015.05.18"
}
```

其他导入，略



加载数据集：

```
curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/bank/account/_bulk?pretty' --data-binary @accounts.json
curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/shakespeare/doc/_bulk?pretty' --data-binary @shakespeare_6.0.json
curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/_bulk?pretty' --data-binary @logs.jsonl
```





验证：

```sh
[root@node198 logs]#curl -X GET "localhost:9200/_cat/indices?v&pretty"
health status index               uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   logstash-2015.05.20 L8Wqf6HgSXm8GA2j0FxRVg   5   1          0            0      1.1kb          1.1kb
yellow open   logstash-2015.05.18 BJ38FlygTa2ypoDzlaM1GQ   5   1          0            0      1.1kb          1.1kb
yellow open   logstash-2015.05.19 shKEEonBQyqR3n86yHmR9g   5   1          0            0      1.1kb          1.1kb
yellow open   bank                atvqMUYcT3WWlOmdp5QOvw   5   1       1000            0    474.7kb        474.7kb
yellow open   shakespeare         nBBdSuiQS9KflqJGNc3yrg   5   1          0            0      1.1kb          1.1kb
```



### 定义自己的索引模式

 加载到 Elasticsearch 的每组数据都有一个索引模式（Index Pattern）。 在上面，
为莎士比亚数据集创建了名为 `shakespeare` 的索引，
为 accounts 数据集创建了名为 `bank` 的索引。

**一个 *索引模式* 是可以匹配多个索引的带可选通配符的字符串。**

例如一般在通用日志记录中，一个典型的索引名称一般包含类似 YYYY.MM.DD 格式的日期信息。例如一个包含五月数据的索引模式： `logstash-2015.05*` 。 





尝试选择 `ba*` 索引模式并在查询栏中输入以下字符串：

```text
account_number:<100 AND balance:>47500
```

 它返回5个结果：帐户号码8，32，78，85和97。 

 每个匹配的文档默认显示所有字段。可以将鼠标悬停在可用字段上并点击您想要展示字段旁边的 **add** 按钮来添加需要展示的字段。例如，如果您仅仅添加 `account_number` ，就只会显示5个简单的账户号码的列表, 还可以点击remove



### 可视化

DIscover: 可以在 Discover 页面下查看搜索结果并在 Visualize 页面下生成已保存搜索的可视化效果。 

 Visualize: 开始可视化您的数据。 

 * **Create a visualization**：

   * pie
   *  Vertical bar
   *  Coordinate map
   *  Markdown widget

   每个建立完都save

 **Dashboard**  : 使用仪表板汇总我们刚刚save的数据模板。