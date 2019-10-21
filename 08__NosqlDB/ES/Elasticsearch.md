Tags:[database, nosql]

### 概念说明

#### 索引

索引，在这里有两个含义，名词： 一个 *索引* 类似于传统关系数据库中的一个 数据库*，是一个存储关系型文档的地方。 索引 (*index*) 的复数词为 indices* 或 *indexes* 。

动词：索引一个文档 就是存储一个文档到一个 *索引* （名词），

这非常类似于 SQL 语句中的 `INSERT` 关键词，除了文档已存在时新文档会替换旧文档情况之外。



#### 文档

一个键值对的json对象我们可以称之为文档，但是术语对象和文档是有些区别的，对象中可以包含子对象等，但是文档值的是根对象或者顶层对象，这个对象被json序列化后存到了es中，指定了唯一的id.



#### 文档元数据

一个文档不仅仅包含它的数据 ，也包含 元数据 （ 有关 文档本身的信息）。 三个必须的元数据元素如下：

* _index   文档存放的位置，是个逻辑区分，你可以理解为数据库的名字。但是这些数据结构可以是不同的，不要真正的按关系数据库去理解。
* _type    文档表示的对象类别，是一个类别划分，比如，你的产品信息都在product索引下，但是产品有不同的品种，生产地等，你可以为些特性去划分type. 你可以理解成原始数据库的table表。
* _id          文档唯一标识

还有其他的文档元数据：

* _version  每个文档都有一个版本号。当每次对文档进行修改时（包括删除）， _version的值会递增。
* _source  数据的具体内容，（先往后看）




### 操作

数据库操作涉及到的无非就是增删改查，这些都用HTTP请求码来得到了实现。

下面操作是格式简单http参数操作，实际要配合curl.

eg:

* GET     :  `curl -i -XGET http://localhost:9200/website/blog/124?pretty`

* 带请求体


  ```c
  curl -XGET 'localhost:9200/statistics_v1/_search?pretty' -d '
  {
  	"query": { 
  		"term": {"analysis-count" : 9354}}}'
  ```

  ​

本文一共涉及两个索引例子，网站博客信息存储`/website/blog/`和公司雇员信息存储`/megacorp/employee/`。

当然这些参数操作除了对文档，也是可以对索引的。

我们通过增删改查来结构化这些参数操作.




#### PUT

##### 创建：

对于雇员目录，我们将做如下操作：

- 每个雇员索引一个文档，包含该雇员的所有信息。
- 每个文档都将是 `employee` *类型* 。
- 该类型位于 索引 `megacorp` 内。
- 该索引保存在我们的 Elasticsearch 集群中。

实践中这非常简单（尽管看起来有很多步骤），我们可以通过一条命令完成所有这些动作：

```
PUT /megacorp/employee/1
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
```

注意，路径 `/megacorp/employee/1` 包含了三部分的信息：

- `megacorp`   索引名称

- `employee`   类型名称

- `1`                特定雇员的ID




##### 更新：

在 Elasticsearch 中文档是 *不可改变* 的，不能修改它们。如果想更新现有的我们需要重建索引或者进行替换。

```
PUT /website/blog/123
```

假设我们这条数据原来已经建立过：

```
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 2,
  "created":   false 
}
```

可以看到_version变为2，`created` 标志设置成 `false` ，是因为相同的索引、类型和 ID 的文档已经存在。

在内部，Elasticsearch 已将旧文档标记为已删除，并增加一个全新的文档。 尽管你不能再对旧版本的文档进行访问，但它并不会立即消失。当继续索引更多的数据，Elasticsearch 会在后台清理这些已删除文档。



##### 只是创建

如果我们只想确认创建一个带自己定义id的新文档，而不是覆盖先有的，我们可以用`_create`

```
PUT /website/blog/123/_create
```



```
{
   "error": {
      "root_cause": [
         {
            "type": "document_already_exists_exception",
            "reason": "[blog][123]: document already exists",
            "shard": "0",
            "index": "website"
         }
      ],
      "type": "document_already_exists_exception",
      "reason": "[blog][123]: document already exists",
      "shard": "0",
      "index": "website"
   },
   "status": 409
}
```

请求成功执行，Elasticsearch 会返回元数据和一个 `201 Created` 的 HTTP 响应码。

另一方面，如果具有相同的 `_index` 、 `_type` 和 `_id` 的文档已经存在，Elasticsearch 将会返回 `409 Conflict` 响应码,以及如上的错误信息。

如果你就想创建一个新文档，用系统的id,可以用下面的POST.



#### POST

上面的put为员工自定义了id，如果需要系统生成id,可用post:`POST /website/blog/`

自动生成的 ID 是 URL-safe、 基于 Base64 编码且长度为20个字符的 GUID 字符串。 

这些 GUID 字符串由可修改的 FlakeID 模式生成，这种模式允许多个节点并行生成唯一 ID ，且互相之间的冲突概率几乎为零。




#### GET

简单地执行 一个 HTTP `GET` 请求并指定文档的地址——索引库、类型和ID。 使用这三个信息可以返回原始的 JSON 文档：

```
GET /website/blog/123
```



我们看一下请求体的响应体：

  GET /website/blog/123?pretty

```
 {
    "_index" :   "website",
    "_type" :    "blog",
    "_id" :      "123",
    "_version" : 1,
    "found" :    true,
    "_source" :  {
        "title": "My first blog entry",
        "text":  "Just trying this out...",
        "date":  "2014/01/01"
    }
  }
```

* `GET` 请求的响应体包括 `{"found": true}` ，这证实了文档已经被找到。 如果我们请求一个不存在的文档，我们仍旧会得到一个 JSON 响应体，但是 `found` 将会是 `false` 。 此外， HTTP 响应码将会是 `404 Not Found` ，而不是 `200 OK` 。
* `pretty` 参数， 正如前面的例子中看到的，这将会调用 Elasticsearch 的 *pretty-print* 功能，该功能 使得 JSON 响应体更加可读。但是， `_source`字段不能被格式化打印出来。



##### `_source`

如果你没有传递参数，默认情况下， `GET` 请求 会返回整个文档，这个文档正如存储在 `_source` 字段中。

但是我们一般只关心几个字段，那么可以这样：

```
GET /website/blog/123?_source=title,text
```

单个字段能用 `_source` 参数请求得到，多个字段也能使用逗号分隔的列表来指定。和url传参很像。

```
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 1,
  "found" :   true,
  "_source" : {
      "title": "My first blog entry" ,
      "text":  "Just trying this out..."
  }
}
```

如果你不需要元数据，只要数据字段：

```
GET /website/blog/123/_source
{
   "title": "My first blog entry",
   "text":  "Just trying this out...",
   "date":  "2014/01/01"
}
```



##### `_search`

我们要实现复杂的查询需要用到`_search` api ：

```
GET /megacorp/employee/_search
```

返回结果包括了所有三个文档，放在数组 `hits` 中,返回结果不仅告知匹配了哪些文档，还包含了整个文档本身：显示搜索结果给最终用户所需的全部信息。:

```json
{
   "took":      6,  #时间消耗，毫秒
   "timed_out": false,   # 是否超时，这个值可以设置
   "_shards": { ... },    # 查询分片数
   "hits": {
      "total":      3,
      "max_score":  1,
      "hits": [
         {
            "_index":         "megacorp",
            "_type":          "employee",
            "_id":            "3",
            "_score":         1,
            "_source": {
               "first_name":  "Douglas",
               "last_name":   "Fir",
               "age":         35,
               "about":       "I like to build cabinets",
               "interests": [ "forestry" ]
            }
         },
         {
            "_index":         "megacorp",
            "_type":          "employee",
            "_id":            "2",
            "_score":         1,
            "_source": {
               "first_name":  "Jane",
               "last_name":   "Smith",
               "age":         32,
               "about":       "I like to collect rock albums",
               "interests": [ "music" ]
            }
         }]}}
```

注： 搜索结果都是放到this中的。

搜索姓氏为 ``Smith`` 的雇员:

`GET /megacorp/employee/_search?q=last_name:Smith`

我们仍然在请求路径中使用 `_search` 端点，并将查询本身赋值给参数 `q=` 。q为自带查询参数。

其他参数：

| 参数      | 说明                                       |
| ------- | ---------------------------------------- |
| fields  | 用于在响应中选择返回字段。                            |
| timeout | 限定搜索时间，响应只包含指定时间内的匹配。默认情况下，无超时。          |
| sort    | 可以通过使用这个参数获得排序结果，这个参数的可能值是`fieldName`，`fieldName:asc`和`fieldname:desc` |

多个参数时用&连接起来：

`curl -XGET 'localhost:9200/statistics_v1/_search?q=analysis-count:9354&pretty'`

记得加引号，不然&后的不生效。



##### 使用查询表达式

Elasticsearch 提供一个丰富灵活的查询语言叫做 *查询表达式* ， 它支持构建更加复杂和健壮的查询，它使我们的查询更灵活易读。

要使用这种查询表达式，只需将查询语句传递给 `query` 参数：

```
GET /_search
{
    "query": YOUR_QUERY_HERE
}
```

我们可能对对用请求体的请求非常吃惊，事实上，http文档上并没有规定带请求体的GET 如何处理，某些特定语言（特别是 JavaScript）的 HTTP 库是不允许 `GET` 请求带有请求体的。

因为带请求体的 `GET` 请求并不被广泛支持，所以 `search` API 同时支持 `POST` 请求：

```
POST /_search
{
  "from": 30,
  "size": 10
}
```



指定了使用一个 JSON 请求，我们可以像这样重写之前的查询所有 Smith 的搜索 ：

```
GET /megacorp/employee/_search
{
    "query" : {
        "match" : {
            "last_name" : "Smith"
        }
    }
}
```

这里用了match,意为包含，即查询last_name中包含Smith的last_name.match这个位置你可以用很多行为。我们称之为**叶子语句**。

其他查询：

| 查询             | 说明                                       |
| -------------- | ---------------------------------------- |
| match_all      | 查询简单的 匹配所有文档。在没有指定查询方式时，它是默认的查询：{ "match_all": {}} |
| match          | 任何字段上进行的是全文搜索还是精确查询, 是你可用的标准查询。它会启用分析器去分析字符串 |
| multi_match    | `multi_match` 查询可以在多个字段上执行相同的 `match` 查询，如果有一条匹配则返回 |
| match_phrase   | 短语搜索，我们想执行这样一个查询，仅匹配同时包含 “rock” *和* “climbing” ，*并且* 二者以短语 “rock climbing” 的形式紧挨着的雇员记录。 |
| range          | `range` 查询找出那些落在指定区间内的数字或者时间. 大于gt, 大于等于gte, 小于lt, 小于等于lte. |
| term           | 被用于精确值 匹配，这些精确值可能是数字、时间、布尔或者那些 `not_analyzed` 的字符串： |
| exists和missing | `exists` 查询和 `missing` 查询被用于查找那些指定字段中有值 (`exists`) 或无值 (`missing`) 的文档 |

补充，分析器是es内置的，当我们用match搜索一个字符串时会默认启用标准分析器，如果你配置的字符串很复杂，它会先分析字符串再搜索。



**复合查询** ：我们用bool语句包含很多叶子语句来组成复合查询。也可以包括bool语句本身，相互嵌套。

```
    "bool": {
        "must":     { "match": { "tweet": "elasticsearch" }},
        "must_not": { "match": { "name":  "mary" }},
        "should":   { "match": { "tweet": "full text" }},
        "filter":   { "range": { "age" : { "gt" : 30 }} }  
    }
}
```



bool的组合查询参数：

* must ： 文档必须匹配这些条件才能被包含进来
* must_not:  文档必须不匹配这些条件才能被包含进来
* should： 如果满足这些语句中的任意语句，将增加 `_score` ，否则，无任何影响。它们主要用于修正每个文档的相关性得分。
* filter : 必须 匹配，但它以不评分、过滤模式来进行。这些语句对评分没有贡献，只是根据过滤标准来排除或包含文档。


这些参数一定要放到bool里才可生效。


更复杂的搜索：

查询姓氏为Smith的雇员，但这次我们需要年龄大于30的。

```
GET /megacorp/employee/_search
{
    "query" : {
        "bool": {
            "must": {
                "match" : {
                    "last_name" : "smith" 
                }
            },
            "filter": {
                "range" : {
                    "age" : { "gt" : 30 } 
                }
            }
 }}}
```

这部分是一个 `range` *过滤器* ， 它能找到年龄大于 30 的文档，其中 `gt` 表示_大于(_great than)。



##### 全文搜索

上面的搜索都相对简单，单个姓名，通过年龄过滤。现在尝试下稍微高级点儿的全文搜索——一项传统数据库确实很难搞定的任务。

搜索下所有喜欢攀岩（rock climbing）的雇员：

```
GET /megacorp/employee/_search
{
    "query" : {
        "match" : {
            "about" : "rock climbing"
        }
    }
}
```

我们在about属性上搜索rock climbing 得到两个结果：

```
{
   ...
   "hits": {
      "total":      2,
      "max_score":  0.16273327,
      "hits": [
         {
            ...
            "_score":         0.16273327, 
            "_source": {
               "first_name":  "John",
               "last_name":   "Smith",
               "age":         25,
               "about":       "I love to go rock climbing",
               "interests": [ "sports", "music" ]
            }
         },
         {
            ...
            "_score":         0.016878016, 
            "_source": {
               "first_name":  "Jane",
               "last_name":   "Smith",
               "age":         32,
               "about":       "I like to collect rock albums",
               "interests": [ "music" ]
            }
         }
     ]}}
```

Elasticsearch 默认按照相关性得分排序，即每个文档跟查询的匹配程度,(_score值)，这说明了全文属性的搜索。





##### 查询情况和过滤情况

我们的查询有两种情况：

* 过滤情况，只是简单的判断文档是否匹配，此时我们可以把这样的查询叫不评分查询（filter)
* 查询情况，除了判断是否匹配，还要计算匹配程度，这则是评分查询(query)

filter的值会被缓存，query的值将不会被缓存。

通常的规则是，使用 查询（query）语句来进行 *全文* 搜索或者其它任何需要影响 *相关性得分* 的搜索。除此以外的情况都使用过滤（filters)。



##### 验证查询

你的查询可能写的非常复杂，我们需要一个api来验证我们的查询结构是否正确：

```
GET /gb/tweet/_validate/query
{
   "query": {
      "tweet" : {
         "match" : "really powerful"
      }}}
```

输出：

```
{
  "valid" :         false,
  "_shards" : {
    "total" :       1,
    "successful" :  1,
    "failed" :      0
  }}
```

以上 `validate` 请求的应答告诉我们这个查询是不合法的：

显示详细的错误信息：`GET /gb/tweet/_validate/query?explain `

```
{
  "valid" :     false,
  "_shards" :   { ... },
  "explanations" : [ {
    "index" :   "gb",
    "valid" :   false,
    "error" :   "org.elasticsearch.index.query.QueryParsingException:
                 [gb] No query registered for [tweet]"
  } ]
}
```



##### 分页

Elasticsearch分页使用的是`from`以及`size`两个参数：

| 参数     | 说明                 |
| ------ | ------------------ |
| `size` | 每次返回多少个结果，默认值为`10` |
| `from` | 忽略最初的几条结果，默认值为`0`  |

假设每页显示5条结果，那么1至3页的请求就是：

```
GET /_search?size=5
GET /_search?size=5&from=5
GET /_search?size=5&from=10
```





#### HEAD

我们用head方法检测文档是否存在，不关心它具体内容：

`HEAD` 请求没有返回体，只返回一个 HTTP 请求报头：

```
curl -i -XHEAD http://localhost:9200/website/blog/123
```

如果文档存在， Elasticsearch 将返回一个 `200 ok` 的状态码：

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8
Content-Length: 0
```

若文档不存在， Elasticsearch 将返回一个 `404 Not Found` 的状态码：

```
curl -i -XHEAD http://localhost:9200/website/blog/124
HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=UTF-8
Content-Length: 0
```

当然，一个文档仅仅是在检查的时候不存在，并不意味着一毫秒之后它也不存在：也许同时正好另一个进程就创建了该文档。



#### DELETE

删除规则很简单，只是使用DELETE方法。

```
DELETE /website/blog/123
```

找到，返回一个 `200 ok` 的 HTTP 响应码，没有 找到，我们将得到 `404 Not Found` 的响应码。

注意：不管找没找到，`_versoin`  都将增加一。





### 其他

#### 高亮

将符合的字段加上html的高亮字段：``<em></em>` `

```
GET /megacorp/employee/_search
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    },
    "highlight": {
        "fields" : {
            "about" : {}
        }
    }
}
```

当执行该查询时，返回结果与之前一样，与此同时结果中还多了一个叫做 `highlight` 的部分。这个部分包含了 `about` 属性匹配的文本片段，并以 HTML 标签 `<em></em>` 封装：

```
{
   ...
   "hits": {
      "total":      1,
      "max_score":  0.23013961,
      "hits": [
         {
            ...
            "_score":         0.23013961,
            "_source": {
               "first_name":  "John",
               "last_name":   "Smith",
               "age":         25,
               "about":       "I love to go rock climbing",
               "interests": [ "sports", "music" ]
            },
            "highlight": {
               "about": [
                  "I love to go <em>rock</em> <em>climbing</em>" 
               ]
            }
         }
     ]}}
```



#### 显示所有索引

`curl 'localhost:9200/_cat/indices?v'`

_cat 提供了一系列集群状态的接口，v 表示显示表头输出。

### 进阶

*  聚合函数
*  maping 映射
*  倒排索引
*  分析器
*  集群
*  处理人类语言
*  监控和部署