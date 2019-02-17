Tags:[python, spider]

### 安装

pip3 install pyspider 

可能会报错：

```
Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-install-z0pgtmll/pycurl/setup.py", line 913, in <module>
        ext = get_extension(sys.argv, split_extension_source=split_extension_source)
      File "/tmp/pip-install-z0pgtmll/pycurl/setup.py", line 582, in get_extension
        ext_config = ExtensionConfiguration(argv)
      File "/tmp/pip-install-z0pgtmll/pycurl/setup.py", line 99, in __init__
        self.configure()
      File "/tmp/pip-install-z0pgtmll/pycurl/setup.py", line 227, in configure_unix
        raise ConfigurationError(msg)
    __main__.ConfigurationError: Could not run curl-config: [Errno 2] No such file or directory: 'curl-config'
```

这是因为pycurl的原因, 安装pycurl, 一定要用pycurl的方式：

```
pip uninstall pycurl
export PYCURL_SSL_LIBRARY=nss
easy_install pycurl
```

验证pyspider:

```
(spiderPy3) [root@claymore spider]# pyspider all
[W 181119 15:24:39 run:413] phantomjs not found, continue running without it.
[I 181119 15:24:41 result_worker:49] result_worker starting...
[I 181119 15:24:42 processor:211] processor starting...
[I 181119 15:24:42 tornado_fetcher:638] fetcher starting...
[I 181119 15:24:42 scheduler:647] scheduler starting...
[I 181119 15:24:42 scheduler:782] scheduler.xmlrpc listening on 127.0.0.1:23333
[I 181119 15:24:42 scheduler:586] in 5m: new:0,success:0,retry:0,failed:0
[I 181119 15:24:42 app:76] webui running on 0.0.0.0:5000
```

时 pyspider Web 服务就会在本地 5000 端口运行 直接在浏览器中打开 即：loca lhost:5000
即可进入 pyspider WebUI 管理页面



### 结构

pyspider 带有强大的 WebUI 、脚本编辑器、任务监控器、项目管理器以及结果处理器，它支持多
种数据库后端 多种消息队列、 JavaScript 渲染页面的爬取，使用起来非常方便

pyspider 的架构主要分为

*  Scheduler （调度器）

* Fetcher 抓取器）

*  Processer （处理器

  整个爬取过程受到 Monitor （监控器）的监控，抓取的结果被 Result Worker （结果处理器）处理，

```
--->  Scheduler         |
|		  |				|  monitor & webui
|	   Fetcher			|
|         |				|
| --- Processer 		|
		  |
		 输出
```



Scheduler 发起任务调度， Fetcher 责抓取网页内容， Processer 负责解析网页内容，然后将新
成的 Request 发给 Scheduler 进行调度，将生成的提取结果输出保存



### 使用

访问localhost:5000, 点击creat 创建一个任务， url可以填：https://movie.douban.com/top250，再点击create， 会自动生成代码（右侧），左侧是调试页面，所有的逻辑在Handler这个类中即可完成。

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-19 15:42:01
# Project: qunawang

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):  # 
        self.crawl('http://travel.qunar.com/travelbook/list.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

```

* on_start()方法是爬取入口，初始的爬取请求会在这里产生，
* 该方法通过调用 crawl()方法,即可新建一个爬取请求，第 1个参数是爬取的 URL ，这里自动替换成我们所定义的 URL crawl ()方法
* 还有 个参数 callback ，它指定了这个页面爬取成功后用哪个方法进行解析，代码中指定为 index_page()
  方法，即如果这个 URL 对应的页面爬取成功了，那 Response 将交给 index_page()方法解析
* index_page ()方法恰好接收这个 Re sponse 参数， Response 对接了pyquery 我们直接调用 doc()
  方法传入相应的 ss 选择器，就可以像 query 一样解析此页面，
* 代码中默认是 `a[href"="http ”］`
  也就是说该方法解析了页面的所有链接，然后将链接遍历，再次调用了 crawl()方法生成了新的爬
  请求
* 同时再指定了 callback detail_page ，意思是说这些页面爬取成功了就调用 detail_page  方法
  解析 这里
* index_page  实现了两个功能，一是将爬取的结果进行解析， 二是生成新的爬取请detail_page 同样接收 
* Response 作为参数 detail_page ()抓取的就是详’情页的信息，就不会生
  成新的请求，只对 Response 对象做解析，解析之后将结果以字典的形式返回 当然我们也可以进行
  续处理， 如将结果保存到数据库