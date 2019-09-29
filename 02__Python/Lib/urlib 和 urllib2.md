#### urllib

在3.x的版本中，urllib与urllib2已经合并为一个urllib库。

在2.x的版本中，urllib与urllib2并不是可以代替的，只能说2是一个补充。



- urllib 仅可以接受URL，不能创建 设置了headers 的Request 类实例；

- 但是 urllib 提供 urlencode 方法用来GET查询字符串的产生，而 urllib2 则没有。（这是 urllib 和 urllib2 经常一起使用的主要原因）,帮我们将key:value这样的键值对转换成"key=value"这样的字符串

  ```python
  >>> import urllib
  >>> urllib.urlencode({'a':'aa', 'b':'bb'})
  'a=aa&b=bb'
  ```

- url编解码工作:

  ```python
  >>> urllib.quote('http://some.cn?ss=s1')
  'http%3A//some.cn%3Fss%3Ds1'
  >>> a=urllib.quote('http://some.cn?ss=s1')
  >>> urllib.unquote(a)
  'http://some.cn?ss=s1'
  ```

#### urllib2

urlopen方法是urllib2模块最常用也最简单的方法，它打开URL网址，url参数可以是一个字符串url或者是一个Request对象。

　　对于可选的参数timeout，阻塞操作以秒为单位，如尝试连接（如果没有指定，将使用设置的全局默认timeout值）。实际上这仅适用于HTTP，HTTPS和FTP连接。

　　先看只包含URL的请求例子：

```
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
```

　　urlopen方法也可通过建立了一个Request对象来明确指明想要获取的url。调用urlopen函数对请求的url返回一个response对象。这个response类似于一个file对象，所以用.read()函数可以操作这个response对象

```
import urllib2
req = urllib2.Request('http://python.org/')
response = urllib2.urlopen(req)
the_page = response.read()
```

这里用到了`urllib2.``Request`类，对于上例，我们只通过了URL实例化了Request类的对象，其实Request类还有其他的参数。

```python
class urllib2.Request(url[, data][, headers][, origin_req_host][, unverifiable])

data:
    是一个字符串，指定额外的数据发送到服务器，如果没有data需要发送可以为“None”。目前使用data的HTTP请求是唯一的。当请求含有data参数时，HTTP的请求为POST，而不是GET。
    数据应该是缓存在一个标准的application/x-www-form-urlencoded格式中。
    eg:  req = urllib2.urlopen(url, dumps(target))
        
```





设置超时时间：

`socket.setdefaulttimeout(5); # 超时 5秒`

疑问？ 这个设置超时和urlopen(timeout=)的区别：

https://stackoverflow.com/questions/27327787/python-urllib2-does-not-respect-timeout

https://stackoverflow.com/questions/8464391/what-should-i-do-if-socket-setdefaulttimeout-is-not-working



关闭连接：

close()会释放链接资源但是不会立即关闭，如果需要立即关闭可以用shutdown()

```python
 fdurl = urllib2.urlopen(req,timeout=self.timeout)
    realsock = fdurl.fp._sock.fp._sock** # we want to close the "real" socket later 
    req = urllib2.Request(url, header)
    try:
             fdurl = urllib2.urlopen(req,timeout=self.timeout)
    except urllib2.URLError,e:
              print "urlopen exception", e
    finally:
    	realsock.close() 
    	fdurl.close()
```

