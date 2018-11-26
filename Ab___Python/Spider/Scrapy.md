## scrapy

Scrap是一个基于 Twisted的异步处理框架,是纯 Python实现的爬虫框架,其架构清晰,模块之
间的耦合程度低,可扩展性极强,可以灵活完成各种需求。

我们只需要定制开发几个模块就可以轻松实现一个爬虫。

另外，scrapy的操作很django有些很相似的地方，很方面有python的django经验的人上手。

### 架构

**scrapy分为以下几个部分：**



![](https://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)

- 引擎(Engine): 用来处理整个系统的数据流处理, 触发事务(框架核心)
- 调度器(Scheduler): 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
- 下载器(Downloader): 用于下载网页内容, 并将网页内容返回给蜘蛛(Spider)
- 项目（Item）, 定义了爬虫的数据结构， 爬取的数据会被赋值成该Item对象。
- 爬虫(Spiders): 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
- 项目管道(Pipeline): 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
- 下载器中间件(Downloader Middlewares): 位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
- 爬虫中间件(Spider Middlewares): 介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。
- 调度中间件(Scheduler Middewares): 介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。



### 数据流

**而scrapy的流程如图，并且可归纳如下：**

![](https://github.com/ClayAndMore/MyImage/blob/master/scrapy_data_stream.png?raw=true)



1.Spider将要爬取页面的URL构造Request对象，提交给Engine；图1

2.Request由Engine进入Scheduler，按照某种调度算法排队，之后某个时候从队列中出来，由Engine提交给Downloader；图2、3、4

3.Downloader根据Request中的URL地址发送一次HTTP请求到目标网站服务器，接受服务器返回的HTTP响应并构建一个Response对象（图5）并由Engine将Response提交给Spider（图6）

4.Spider提取Response中的数据，构造出item对象或者根据新的链接构造出Request对象，如果是Item对象，由Engine提交给Item pipeline，如果是新的Request，由Engine提交给Scheduler；（图7、8）

5.这个过程反复进行，直到爬完所有的数据，同时，数据对象在出入Spider和Downloader的时候可能会经过Middleware的进一步处理



### 安装

pip install Scrapy



### 项目结构

创建一个 Scrap项目,项目文件可以直接用 crapy命令生成,命令如下所示:
`scrapy startproject tutorial`

这个项目会直接创建一个tutorial的文件夹。

```
(spiderPy3) [root@claymore tutorial]# tree
.
|-- scrapy.cfg                 # 部署时用到的文件
`-- tutorial				   # 项目模块，可引入
    |-- __init__.py            # 
    |-- items.py               # Items的定义， 定义爬取的数据结构
    |-- middlewares.py 		   # 定义爬取的中间件
    |-- pipelines.py		   # 定义数据管道
    |-- __pycache__         
    |-- settings.py			   # 配置文件
    `-- spiders                # 放置Spiders的文件夹
        |-- __init__.py
        `-- __pycache__
```



### 初始

#### 创建Spider

Spider是自己定义的类, Scrap用它来从网页里抓取内容,并解析抓取的结果。

不过这个类必须继承 Scrap提供的 Spider类 scrap. Spider,还要定义 Spider的名称和起始请求,以及怎样处理爬取
后的结果的方法。

也可以使用命令行创建一个 Spider。比如要生成 Quotes这个 Spider,可以执行如下命令:`

```
cd tutorial
scrapy genspiderquotes quotes.toscrape.com
```

执行 genspider 命令 第一个参数是 Spider 名称，第二个参数是网站域名

这时spider 里多了个文件quotes.py:

```python
# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes' 
    allowed_domains = ['quotes.toscrape.com']  
    start_urls = ['http://quotes.toscrape.com/'] 

    def parse(self, response):
        pass
```

* name 是每个项目唯一的名字，用来区分不同的 Spider
* allowed_domains: 允许爬取的域名，如果初始或后续的请求链接不是这个域名下的，则会被过滤掉
* start_urls: 包含了 Spider 在启动时爬取的 url 列表，初始请求是由它来定义的
* parse, 被调用时 start_urls 里面的链接构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数 该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求



#### 创建Item

Item 是保存爬取数据的容器，它的使用方法和字典类似 不过，相比字典， Item 多了额外的保护
机制，可以避免拼写错误或者定义字段错误.
创建 Ite 需要继承 scrapy.Item 类，并且定义类型为 scra py.Field 字段 观察目标网站，

我们可以获取到到内容有 text, author,  tags
定义 Item ，此时将 items.py 修改如下：

```python
import scrapy
class Quoteitem(scrapy. Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field() 
```

定义了三个字段，接下来爬取时我们会使用到这个 Item



#### 解析Response

http://quest.toscrape.com的页面结构：

```html
<body>
    
<div class="container">
    <div class="row">
    
        <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
            <span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>
            <span>by <small class="author" itemprop="author">Albert Einstein</small>
                <a href="/author/Albert-Einstein">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <meta class="keywords" itemprop="keywords" content="change,deep-thoughts,thinking,world"> 

                <a class="tag" href="/tag/change/page/1/">change</a>

                <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>

                <a class="tag" href="/tag/thinking/page/1/">thinking</a>

                <a class="tag" href="/tag/world/page/1/">world</a>

            </div>
        </div>
        
        --重复--
```



我们把quotes改成：

```python
import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
       
        quotes = response.css('.quote')  
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags.tag::text').extract()
            yield item
        next = response.css('.pager.next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
~                                                                 
```

* `reponse : <class 'scrapy.http.response.html.HtmlResponse'> `, 这个类里面提供了可以解析网页的选择器： css选择器和XPath选择器

* `response.css('.quote')` 获取了所以class为.quote的对象

* `quote.css('.text::text').extract_first()` , 获取class为.text的text属性，就是标签内容， 会返回一个所以当前节点class为.text的 text **列表**， 因为当下节点只有一个.text我们获取第一个extract_first()

  如获取第一个节点我们可以这样：`quote.css('.text').extract_first()`

* `quote.css('.tags.tag::text').extract()`  tag则要获取全部



下一页的HTML:

```html
<ul class="pager">
            
            <li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">→</span></a>
            </li>            
</ul>
```

全链接是：`http://quotes.toscrape.com/page/2`，通过这个链接我们就可以构造下 一个请求

* 通过css 选择器获取下一个页面的链接，即要获取 超链接中的 href 属性,用到了`::attr(href)`操作
* urljoin方法可以将相对 URL 构造成 个绝对的 URL 例如，
  获取到的下一页地址是／page/2, urljoin处理后得到的结果就是 `http://quotes.toscrape.com/page/2`
* 构造下一个请求时需要用到 scrapy.Request 这里我们传递两个参数：`url`, `callback`
  * url 请求链接
  * callback 回调函数， 当指定了该回调函数的请求完成之后，获取到响应，引 擎会将该
    响应作为参数传递给这个回调函数， 这样就构成了一个抓取循环。





### 运行

进入quotes.py目录， `scrapy crawl quotes`

 输出 了当前的版本 ,项目名称 , settings.py重写后的配置 

然后输出了当前所应用 Middlewares 和Pipelines 

Middlewares 默认是启用的 ，可settings.py 中修改 Pipelines 默认是空 ，同样也可以在 settings py 中配置。
可以看到爬虫 边解析， 边翻页，直至将所有内取完毕
最后， Scrapy 输出 了整个抓取过程的统计信息，如请求的字节数、请求次 响应次数 、完成原因等



#### 保存到文件

我们想将上面 结果保存成 JSON 文件，可以执行如下命令：
`scrapy crawl quotes -o quotes.json`

另外我们还可以每一个 Item 输出一行 JSON ，输出后 jl ，为 jsonline 的缩写，命 如下所
`scrapy crawl quotes -o quotes.jl`
`scrapy crawl quotes -o quotes.jsonlines `

输出格式还支持很多种，例如 csv xml pickle marsha 等，还支持 ftp s3 等远程输出，另外
还可以通过自定义 ItemExporter 来实现其他的输出
例如，下面命令对应的输出分别为 csv xml pickle marshal 格式以及句远程输出

```shell
scrapy crawl quotes -o quotes .csv
scrapy crawl quotes -o quotes.xml
scrapy crawl quotes -o quotes.pickle
scrapy crawl quotes -o quotes.marshal
scrapy crawl quotes -o ftp://user:pass@ftp .example.com/path/to/quotes.csv 
```



### 使用Item Pipeline

Item Pipeline 作为项目管道，当Item生成后，会自动被送到Item Pipeline处理。

常用Item Pipeline做如下操作：

* 清理HTML数据。
* 验证爬取数据,检查爬取字段。
* 查重并丢弃重复内容。
* 将爬取结果保存到数据库。

在项目的目录结构中已经为我们生成了一个pipelines.py:

```python
class TutorialPipeline(object):
    def process_item(self, item, spider):
        """
        item: Spider生成的Item都会作为参数传递过来
        spider: Spider的实例。
        """
        return item
```

要实现 Item Pipeline 很简单，只需要定义 类并实现 process_item方法即可. Item Pipeline 会自动调用这个方法 

process_item 方法必须返回包含数据的字典或 Item 对象，或者抛出 Dropltem 异常

* Item对象， ，那么此 Item 会被低优先级的 Item Pipeline 的 process_item 方法
  处理，直到所有的方法被调用完毕

* Drop Item 异常，那么此 Item 会被丢弃，不再进行处理

可以把原来自带Pipeline删掉，

实现一个Item Pipeline实例：

```python
from scrapy.exceptions import DropItem

class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        """
        文字长度限定为50，超出50后，变为省略号。
        """
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem("Missing Text")
~                                                             
```

接下来，我们将处理后的 item 存入 MongoDB 定义另外 Pipeline 同样在 pipelines.py
我们实现另 个类 MongoPipeline：

```python
import pymongo
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

```

MongoPipeline 类实现了 API 定义的另外几个方法:

* from crawler 它是一个类方法，用＠classmethod 标识， 是一种依赖注入的方式 它的参数
  就是 crawler ，通过 crawler 我们可以拿到全局配置的每个配置信息 在全局配置 settings.py
  中，我们可以定义 MONGO_URI MONGO_DB 来指定 MongoDB 接需要的地址和数据库名称，
  到配置信息之后返回 对象即可 所以这个方法的定义主要是用来获取 settings.py 中的配置
* open_spider,  Spider 开启时，这个方法被调用 上文程序中主要进行了 些初始化操作
* close_spider,  Spider 关闭时，这个方法会调用 上文程序中将数据库连接关闭

最主要的 process_item方法则执行了数据插入操作

我们还要在setting.py 中加入：

```
ITEM_PIPELINES =  {
    'tutorial.pipelines.TextPipeline': 300,
    'tutorial.pipelines.MongoPipeline': 400
}
MONGO_URI = 'localhost'
MONGO_DB = 'tutorial'
```

300,400是对应的Pipeline优先级，数字越小对应的Pipeline越先被调用。

