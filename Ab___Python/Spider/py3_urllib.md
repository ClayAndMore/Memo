Tags:[python, spider]

## urllib

### 写在前面

在python2 中， 有urllib 和urlib2 两个库来实现请求的发送。而在python 3中，上面两个库已经统一为urllib。

分四个模块：



### request

基本http模块，用来模拟发送请求。

具体方法：

#### urlopen

```python
import urrlib.request
res =  urllib.request.urlopen("https://www.python.org")
print(tpye(res))
< class http.client.HTTPresponse>

res.read() # 返回网页内容
res.status # 返回结果的状态码
res.getheaders() # 返回所有头信息
res.getheader('Server') # 返回头信息的server值

```

其他参数：

```python
# data 参数，post请求
data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8') # 字节流传输
res = urllib.request.urlopen("http:/httpbin.org/post", data=data)

# http:/httpbin.org ，它可以提供http请求测试。 

# timeout 参数
res = urllib.request.urlopen("http:/httpbin.org/get", timeout=1)

一秒后服务器没有响应，抛出
urllib.error.URLERROR
```



#### Request

如果请求中有更多的附加信息，用Request类来构建。

```python
import urllib.request
req = urlib.request.Request(
    url='https://python.org', # 必传
    method, # GET,POST,PUT等
	data,  # 如果post数据，必须传递bytes字节流类型的。
    headers={}, # 或用add_header(), eg: req.add_header('User-Agent': '')
    origin_req_host, # 请求方等host名称或ip
)
```

关于header， 常用的方法是修改User-Agent 来伪装浏览器， 默认是这里Python-urllib,。

伪装火狐： `'User-Agent': Mozilla/5.0 (x11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11`



### Handler

对于一些高级的操作， 如Cookies处理， 代理设置等。 我们需要处理器。

#### Opener

一个比较重要等类是OpenerDirector, 我们可以称之为Opener。 

之前的urlopen这个方法其实就是urllib为我们提供的一个Opener。

这里我们谈更高级的使用方法，而不是之前为我们封装好了的urlopen, 

总之， 我们要利用Handler 来构建Opener.



#### 验证

```python
# coding=utf-8
import urllib.request

auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='PDQ Application',
                          uri='https://mahler:8092/site-updates.py',
                          user='klem',
                          passwd='kadidd!ehopper')
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
urllib.request.urlopen('http://www.example.com/login.html')
```

此处代码为实例代码，用于说明`Handler`和`Opener`的使用方法。

在这里，首先实例化了一个`HTTPBasicAuthHandler`对象，然后利用`add_password()`添加进去用户名和密码，相当于建立了一个处理认证的处理器。

接下来利用`urllib.request.build_opener()`方法来利用这个处理器构建一个`Opener`，那么这个`Opener`在发送请求的时候就具备了认证功能了。接下来利用`Opener`的`open()`方法打开链接，就可以完成认证了。



#### 代理

如果添加代理，可以这样做：

```python
# coding=utf-8
import urllib.request

proxy_handler = urllib.request.ProxyHandler({
    'http': 'http://218.202.111.10:80',
    'https': 'https://180.250.163.34:8888'
})
opener = urllib.request.build_opener(proxy_handler)
response = opener.open('https://www.baidu.com')
print(response.read())
```

此处代码为实例代码，用于说明代理的设置方法，代理可能已经失效。

在这里使用了`ProxyHandler`，`ProxyHandler`的参数是一个字典，key是协议类型，比如`http`还是`https`等，value是代理链接，可以添加多个代理。

然后利用`build_opener()`方法利用这个`Handler`构造一个`Opener`，然后发送请求即可。



#### Cookies

我们先用一个实例来感受一下怎样将网站的`Cookie`获取下来。

```python
import http.cookiejar, urllib.request

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name+"="+item.value)
```

首先我们必须声明一个`CookieJar`对象，接下来我们就需要利用`HTTPCookieProcessor`来构建一个`handler`，最后利用`build_opener`方法构建出`opener`，执行`open()`即可。

运行结果如下：

```
BAIDUID=2E65A683F8A8BA3DF521469DF8EFF1E1:FG=1
BIDUPSID=2E65A683F8A8BA3DF521469DF8EFF1E1
H_PS_PSSID=20987_1421_18282_17949_21122_17001_21227_21189_21161_20927
PSTM=1474900615
BDSVRTM=0
BD_HOME=0
```

可以看到输出了每一条`Cookie`的名称还有值。

不过既然能输出，那可不可以输出成文件格式呢？我们知道很多`Cookie`实际也是以文本形式保存的。

答案当然是肯定的，我们用下面的实例来感受一下：

```python
filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
```

这时的`CookieJar`就需要换成`MozillaCookieJar`，生成文件时需要用到它，它是`CookieJar`的子类，可以用来处理`Cookie`和文件相关的事件，读取和保存`Cookie`，它可以将`Cookie`保存成`Mozilla`型的格式。

运行之后可以发现生成了一个`cookie.txt`文件。



内容如下：

```
# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

.baidu.com	TRUE	/	FALSE	3622386254	BAIDUID	05AE39B5F56C1DEC474325CDA522D44F:FG=1
.baidu.com	TRUE	/	FALSE	3622386254	BIDUPSID	05AE39B5F56C1DEC474325CDA522D44F
.baidu.com	TRUE	/	FALSE		H_PS_PSSID	19638_1453_17710_18240_21091_18560_17001_21191_21161
.baidu.com	TRUE	/	FALSE	3622386254	PSTM	1474902606
www.baidu.com	FALSE	/	FALSE		BDSVRTM	0
www.baidu.com	FALSE	/	FALSE		BD_HOME	0
```

另外还有一个`LWPCookieJar`，同样可以读取和保存`Cookie`，但是保存的格式和`MozillaCookieJar`的不一样，它会保存成与libwww-perl的Set-Cookie3文件格式的`Cookie`。

那么在声明时就改为

```
cookie = http.cookiejar.LWPCookieJar(filename)
```

生成的内容如下：

```
#LWP-Cookies-2.0
Set-Cookie3: BAIDUID="0CE9C56F598E69DB375B7C294AE5C591:FG=1"; path="/"; domain=".baidu.com"; path_spec; domain_dot; expires="2084-10-14 18:25:19Z"; version=0
Set-Cookie3: BIDUPSID=0CE9C56F598E69DB375B7C294AE5C591; path="/"; domain=".baidu.com"; path_spec; domain_dot; expires="2084-10-14 18:25:19Z"; version=0
Set-Cookie3: H_PS_PSSID=20048_1448_18240_17944_21089_21192_21161_20929; path="/"; domain=".baidu.com"; path_spec; domain_dot; discard; version=0
Set-Cookie3: PSTM=1474902671; path="/"; domain=".baidu.com"; path_spec; domain_dot; expires="2084-10-14 18:25:19Z"; version=0
Set-Cookie3: BDSVRTM=0; path="/"; domain="www.baidu.com"; path_spec; discard; version=0
Set-Cookie3: BD_HOME=0; path="/"; domain="www.baidu.com"; path_spec; discard; version=0
```

由此看来生成的格式还是有比较大的差异的。

那么生成了`Cookie`文件，怎样从文件读取并利用呢？

下面我们以`LWPCookieJar`格式为例来感受一下：

```python
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8'))
```

前提是我们首先利用上面的方式生成了`LWPCookieJar`格式的`Cookie`，然后利用`load()`方法，传入文件名称，后面同样的方法构建`handler`和`opener`即可。

### error

异常处理模块。



### parse

工具模块， 提供类许多URL处理方式， 如拆分，解析，合并等。

方便的处理url拼接

```
from urllib.parse import urlencode
>>> urlencode({'a':'aa', 'b':'bb'})
'a=aa&b=bb'
```





### rebotparser

主要用来识别网站等robots.txt文件， 用的比较少。