---
title: python爬虫
date: 2017-03-04 20:47:37
categories:
header-img:
tags:
---

### requests库

python内置的`urllib`和`urllib2`其实已经算是蛮好用了，但是非有人不服，于是他做出了更好的一个http库，叫做`request`

requests 文档：http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

安装：

`pip install requests`



新建demo.py文件：

```python
r = requests.get('https://unsplash.com') #像目标url地址发送get请求，返回一个response对象
print(r.text) #r.text是http response的网页HTML
```

运行，网页的HTML内容会输出到控制台

r是一个Response对象。



这里有个http请求，就是get方式，但是http有八种方式都可以用

```
url = 'https://movie.douban.com/'
r = requests.get(url) 
r = requests.post(url) 
r = requests.delete(url) 
r = requests.head(url) 
.....
```

### BeautifulSoup库

Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.Beautiful Soup会帮你节省数小时甚至数天的工作时间.

文档：http://beautifulsoup.readthedocs.io/zh_CN/latest/

安装：`pip install beautifulsoup4`

Demo:

```python
from urlib import urlopen
from bs4 import BeautififulSoup
response = urlopen('http://www.baidu.com')
bs = BeautifulSoup(response.read(), "html.parser")
print bs.title #  获取网页标题的文本内容
```

BeatifuleSoup 实例化接受三种字符类型作为参数：

* `BeautifulSoup("<h1>这是一个测试文档</h1>", "html.parser")`
* `BeautifulSoup("native.html", "html.parser")`  本地文件
* demo中的那种。



Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构，每个节点都是Python对象。所有对象可以归纳为4种类型: Tag , NavigableString , BeautifulSoup , Comment 。

#### tag

tag对象是 XML或HTML原生文档中的元素标签对象，这个就跟HTML或者XML（还能解析XML？是的，能！）中的标签是一样一样的。

###### 提取标签的名字：

`tag.name`

###### 提取标签的属性：

`tag['attribute']`， 属性字典： tag.attrs
我们用一个例子来了解这个类型：

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc, 'lxml')  #声明BeautifulSoup对象
find = soup.find('p')  #使用find方法查到第一个p标签
print("find's return type is ", type(find))  #输出返回值类型
print("find's content is", find)  #输出find获取的值
print("find's Tag Name is ", find.name)  #输出标签的名字
print("find's Attribute(class) is ", find['class'])  #输出标签的class属性值
```

BeautifulSoup对象表示一个文档的全部内容。支持遍历文档树和搜索文档树。



我们使用find()方法返回的类型就是这个tag类型，

使用find-all()返回的是多个该对象的集合，是可以用for循环遍历的。

返回标签之后，还可以对提取标签中的信息。



### scrapy

scrapy是python家族中最负盛名的爬虫框架，其他比较好使的是 `urllib`,`urllib2`,`requests`,`pyquery`等,另外，scrapy的操作很django有些很相似的地方，很方面有python的django经验的人上手。

**scrapy分为以下几个部分：**

![scrapy](http://7xlen8.com1.z0.glb.clouddn.com/scrapy_work.jpeg)

- 引擎(Scrapy): 用来处理整个系统的数据流处理, 触发事务(框架核心)
- 调度器(Scheduler): 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
- 下载器(Downloader): 用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
- 爬虫(Spiders): 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
- 项目管道(Pipeline): 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
- 下载器中间件(Downloader Middlewares): 位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
- 爬虫中间件(Spider Middlewares): 介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。
- 调度中间件(Scheduler Middewares): 介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。

**而scrapy的流程如图，并且可归纳如下：**

- 首先下载器下载request回执的html等的response
- 然后下载器传给爬虫解析
- 接着爬虫解析后交给调度器过滤，查重等等
- 最后交给管道，进行爬取数据的处理

#### XPath

XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。