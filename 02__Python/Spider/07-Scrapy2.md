Tags:[python, spider]

### Selector

Scrapy 提供了自己的数据提取方法，即 Se lector （选择器）

Selector 是基于 lxml来构建的，支持XPath 选择器 css 选择器以及正则表达式

Selector 主要是与 Scrapy 结合使用，如 Scrapy 的回调函数中的参数目sponse 直接调用 xpath()
或者 css （）方法来提取数据



#### 直接使用

```python
from scrapy import Selector
body= '<html><head><title>Hello World</title></head><body></body></ html> ’
selector = Selector(text=body)
title = selector.xpath('//title/text()').extract_first()
print(title)

hello world
```

没有在 Scrapy 框架中运行 而是把 Scrapy 中的 Selector 单独拿出来使用了，构建的时候传入 tex 参数，就生成了 Selector 选择器对象，然后就可以像前面我们所用的 Scrapy 中的解
析方式一样，调用 xpath , css 等方法来提取了



#### Scrapy shell

和python shell一样，它方便我们调试抓取的网页，其实就是模拟的Scrapy的一次请求，返回一些可以操作的变量：

```
scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html 

...

[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f61e7c68e80>
[s]   item       {}
[s]   request    <GET http://doc.scrapy.org/en/latest/_static/selectors-sample1.html>
[s]   response   <200 https://doc.scrapy.org/en/latest/_static/selectors-sample1.html>
[s]   settings   <scrapy.settings.Settings object at 0x7f61e6917d68>
[s]   spider     <DefaultSpider 'default' at 0x7f61e58fc048>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser

>>> response.headers
{b'Age': [b'45389'], b'X-Amz-Cf-Id': [b'hs850On3lDTMwzjFQcCXmLkuKDr_ne0gjbUsr4R49car_0cIAd8utw=='], b'Via': [b'1.1 91085d9a0810fca6dacd51dae7dd6a32.cloudfront.net (CloudFront)'], b'X-Deity': [b'web02'], b'X-Cname-Tryfiles': [b'True'], b'Etag': [b'W/"5b40c434-235"'], b'Date': [b'Tue, 20 Nov 2018 07:54:35 GMT'], b'Content-Type': [b'text/html'], b'X-Served': [b'Nginx'], b'Server': [b'nginx/1.14.0 (Ubuntu)'], b'Vary': [b'Accept-Encoding'], b'X-Cache': [b'Hit from cloudfront'], b'Last-Modified': [b'Sat, 07 Jul 2018 13:46:28 GMT']}

```



#### Xpath选择器

上方response.body提供操作实例：

```html
<html>
<head>
<title> Example website</title>
</head>
<body>
<div id='images'>
<a href='image1.html'>Name: My image 1 <br /><img src='image1 thumb.jpg' /></a>
<a href='image2.html'>Name: My image 2 <br /><img src='image2 thumb.jpg' /></a>
<a href='image3.html'>Name: My image 3 <br /><img src='image3 thumb.jpg' /></a>
<a href='image4.html'>Name: My image 4 <br /><img src='image4 thumb.jpg' /></a>
<a href='image5.html'>Name: My image 5 <br /><img src='image5 thumb.jpg' /></a>
</div>
</body>
</html>
```

通过scrapy shell来解析， 

response 有一个属性 selector ，我们调用 response.selector 返回的内容就相当于用 response的
**body** 构造了 Selector 对象

```
>> result = response.selector.xpath ('//a') 
>> result
[<Selector xpath=’//a ’ data=’< a href=”image1.html”>Name: My image 1 <’ >,
<Selector xpath=’ //a ’ data=’<a href＝”image2.html">Name ：My image 2 <’>,
<Selector xpath='//a ’  data=’<a href＝”image3.html">Name ：My image 3 <’>,
<Selector xpath='//a ’  data=’<a href＝”image4.html">Name ：My image 4 <’>,
<Selector xpath= '//a’  data='<a href="images.html“>Name: My image S <’>]
>> type(result)
scrapy.selector.unified.Selectorlist

>> result. xpath('./img ’)
[<Selector xpath='./img ’ data=' <img src=" image1_thumb.jpg">'>,
<Selector xpath=’./img ’  data=’ <img src=” image2 thumb.jpg”>’>,
<Selector xpath=’./img '  data=’ <img src=” image3_thumb.jpg”>’>,
<Selector xpath='./img ’  data=' <img src ＝”image4_thumb.jpg >’>，
<Se lector xpath=’./img'  data=’ <img src = "images_thumb .jpg”>’>]
```

用`//` 从html节点里进行选取。

用`.`从当前节点里进行选取。



我们刚才使用了 response.selector.xpath 方法对数据进行了提取 Scrapy 提供了两个实用的捷方法， 

response .xpath 和 response. css ，它们二者的功能完全等同于 response.selector.xpath和response.selector.css, 方便起见，以后最好常用前者。

```shell
>>> result = response.xpath('//a')
>>> result
[<Selector xpath='//a' data='<a href="image1.html">Name: My image 1 <'>, 
<Selector xpath='//a' data='<a href="image2.html">Name: My image 2 <'>, 
<Selector xpath='//a' data='<a href="image3.html">Name: My image 3 <'>, 
<Selector xpath='//a' data='<a href="image4.html">Name: My image 4 <'>, 
<Selector xpath='//a' data='<a href="image5.html">Name: My image 5 <'>]
>>> result[0]
<Selector xpath='//a' data='<a href="image1.html">Name: My image 1 <'>
>>> result.extract()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', '<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>', '<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>', '<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>', '<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

>>> response.xpath('//a/text()').extract()
['Name: My image 1 ', 'Name: My image 2 ', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
>>> response.xpath('//a/@href').extract()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

>>> response.xpath('//a[@href="image1.html"]/text()').extract()
['Name: My image 1 ']
>>> response.xpath('//a[@href="image1.html"]/text()').extract()[0]
'Name: My image 1 '

>>> response.xpath('//a[@href="image1.html"]/text()').extract_first()
'Name: My image 1 '
>>> response.xpath('//a[@href="image1.html"]/text()').extract_first('Default')
'Name: My image 1 '
```

* result[0] 使用下标 像真正数组一样访问SelectorList
* extract可以获取到真正数据内容
* /text() 获取节点内部文本
* @href获取节点href属性， @后面内容就是要获取的属性名称。
* 使用[]限制匹配范围
* 尽量使用extract_first代替[0]， 因为前者不会因没有结果报错，还可以传递默认值。



#### CSS 选择器

```shell
>>> response.css('a')
[<Selector xpath='descendant-or-self::a' data='<a href="image1.html">Name: My image 1 <'>, <Selector xpath='descendant-or-self::a' data='<a href="image2.html">Name: My image 2 <'>, <Selector xpath='descendant-or-self::a' data='<a href="image3.html">Name: My image 3 <'>, <Selector xpath='descendant-or-self::a' data='<a href="image4.html">Name: My image 4 <'>, <Selector xpath='descendant-or-self::a' data='<a href="image5.html">Name: My image 5 <'>]

>>> response.css('a[href="image1.html"]').extract()  #属性选择
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>']

# 嵌套选择， a节点中的img节点 空格+属性
>>> response.css('a[href="image1.html"] img').extract() 
['<img src="image1_thumb.jpg">']

# 获取文本属性需要::text()和::attr()的写法
>>> response.css('a[href="image1.html"]::text').extract_first()
'Name: My image 1 '
>>> response.css('a[href="image1.html"] img::attr(src)').extract_first()
'image1_thumb.jpg'

#和xpat一起使用：
>>> response.xpath ('//a').css('img').xpath('@src').extract()
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']

```



#### 正则匹配

a节点文本类似于： `Name: My image 1`,   我们想把Name后面的提取出来

```shell
>>> response.xpath('//a/text()').re('Name:\s(.*)')
['My image 1 ', 'My image 2 ', 'My image 3 ', 'My image 4 ', 'My image 5 ']
>>> response.xpath('//a/text()').re('(.*?):\s(.*)')
['Name', 'My image 1 ', 'Name', 'My image 2 ', 'Name', 'My image 3 ', 'Name', 'My image 4 ', 'Name', 'My image 5 ']

# 返回第一个
>>> response.xpath('//a/text()').re_first('(.*?):\s(.*)')
'Name'
>>> response.xpath('//a/text()').re_first('Name:\s(.*)')
'My image 1 '

# re不能直接跟response对象，要衔接一个选择器方法
>>> response.xpath('.').re('Name:\s(.*)<br>')
['My image 1 ', 'My image 2 ', 'My image 3 ', 'My image 4 ', 'My image 5 ']
>>> 

```





### Downloader Middleware 

下载中间件， 看架构图

* Scheduler 调度出队列的 Request 发送给 Doanloader下载之前，也就是我们可以在 request
  执行下载之前对其进行修改
* 在下载后生成 Response 发送给 Spider 之前，也就是我们可以在生成 Resposne Spider 解析
  之前对其进行修改

修改 User-Agent 处理重定向 、设置代理、失败重试、设置 cookies 等功能都需要借助它来实现

Scrapy已经内置了很多Downloader Middleware， 在DOWNLOADER_MIDDLEWARES_BASE所定义：

```
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware' : 100,
	’scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware ’: 300,
	'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware’: 350,
	’scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware ' : 400,
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware ’: 500,
	’scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
	’scrapy.downloadermiddlewares.ajaxcrawl .AjaxCrawlMiddleware ’: 560,
	'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares .httpcompression.HttpCompressionMiddleware' : 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware' : 600,
    ’scrapy.downloadermiddlewares.cookies.CookiesMiddleware’ : 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware’: 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats’; 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900, 
}
```

数值越小越接近Scrapy Engine, 越大越接近Downloader, 数字小的会被先调用

我们可以自己定义Downloader Middleware,  需要修改scrapy提供的另一个变量： DOWNLOADER_MIDDLEWARES,  可以禁用base里的Middleware,

我们只要定义一个有方法的类就可以实现自定义，几个核心方法：



#### process_request

process_request(request, spider)

Request Scrapy 引擎调度给 Downloader 之前， process_request 方法就会被调用，也就是在
Request 从队列里调度出来到 Down loader 下载执行之前。

方法的返回值必须为 None， Response 对象 ，Request 对象之一 ，或者抛州 IgnoreRequest异常

返回结果：

* None ，crapy 将继续处理该 Request ，接着执行其他 Downloader Middlewared的
  process_request 方法，一直到 Downloader Request 执行后得到 Response 才结束

  这个过程其实就是修改 Request 的过程，不同的 Downloader Middleware 按照设置的优先级顺序依次
  Request 进行修改，最后送至 Downloader 执行

* Response, 更低优先级的 Downloader Middleware process _request和process_exception方法就不会被继续调用，每个 Downloader Middleware的process response方法转而被依次调用 

  调用完毕之后，直接将 Response 对象发送给 Spider 来处理

* Request,  更低优先级的 Downloader Middleware process_request方法会停止执行

   这个 Request 会重新放到调度队列里，其实它就是一个全新 Request 等待被调度。
    如果被 Scheder 调度了，那么所有的 Downloader Middleware process request方法被重新按照顺序执行

* Igno reRequest 异常抛出， 则所有的 Downloader Middleware process_exception方法依次执行 

  如果没有 个方法处理这个异常，那么 Request的 errorback方法就会回调
  如果该异常还没有被处理，那么它便会被忽略



#### process_response

process_reponse(request, response, spider）

* request Request 对象， 即此 Response 对应的 Request
* response Response 象， 即此被处理的 Response
* spider ，是 Spider 对象， 即此 Response 对应的 Spider

Down loader 执行 Request 下载之后，会得到对应的 Response。Scrapy 引擎便会将 Response 发送给
Spider进行解析。

 在发送之前，我们都可以用 process_response方法来对 Response 进行处理 

方法的返回值必须为 Request 对象 Response 对象之 一，或者抛出 IgnoreRequest异常

返回值：

* Request ，更低优先级的 Downloader Middleware的process_response 方不会继续调用。

  Request 对象会重新放到调度队列里等待被调度，它相当于 个全新的Request。

  然后，该Request 会被 process_request 方法依次处理

* Respons ，更低优先级的 Downloader Middleware的process_response方法会继续调用，继续对该 Response 对象进行处理
* IgnoreRequest 异常抛向，则 Request errorback方法会回调 如果该异常还没有被处理，那么它便会被忽略



#### process_exception

process_exception(request, exception, spider)

Downloader process_request方法抛出异常时，例如抛出 IgnoreRequest 异常，
process_exception 方法就会被调用。

方法的返回值必须为 None Response 对象 Request 对象之一。

返回值：

* None ，更低优先级的 Downloader Middleware process_exception会被继续顺次调用，直到所有的方法都被调度完毕
* Response ，更低优先级的 Down loader Middleware process_exception 方法不再被继续调用，每个 Downloader Middleware proce ss _response 方法转而被依次调
* Request ，更低优先级的 Downloader Middleware proce ss_exception也不再被继续调用，该 Request 对象会重新放到调度队列里面等待被调度，它相当于一个全新的Request 然后，该 Request 又会被process_request 方法顺次处理



#### 实例

新建一个项目，新建Spider httpbin:

```python
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    #start_urls = ['http://httpbin.org/']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        self.logger.debug(response.text)
```

out:

```
{
"headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Encoding": "gzip,deflate", 
    "Accept-Language": "en", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "Scrapy/1.5.1 (+https://scrapy.org)"
  }, 
  "origin": "211.159.177.235", 
  "url": "http://httpbin.org/get"
}

```

我们发现User-Agent是scrapy设置的， 它其实是内置的UserAgentMiddleware设置的。

##### 修改User-Agent

设置请求的User-Agent有两种方式：

* 在setting里加一会USER_AGENT变量：

  `USER_AGENT='Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0'`

* 如果想要随机，更灵活的方式，需要Downloader Middlerware实现：

  在middlewares.py里添加一个类：

  ```python
  import random
  
  class RandomUserAgentMiddleware():
      def __init__(self):
          self.user_agents = [
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0',
              ]
      def process_request(self, request, spider):
          request.headers['User-Agent'] = random.choice(self.user_agents)
                                                                                   
  ```

  接着去settings.py里取消注释，并添加我们刚加入的Middleware

  ```
  DOWNLOADER_MIDDLEWARES = {
  #    'downloadertest.middlewares.DownloadertestDownloaderMiddleware': 543,
      'downloadertest.middlewares.RandomUserAgentMiddleware': 543,
  }
  ```





### Spider Middleware





