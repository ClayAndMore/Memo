tags:[python, spider, py_lib]

## requests

python内置的`urllib`和`urllib2`其实已经算是蛮好用了，但用urllib时在处理网站验证和cookies时不太方便，需要Opener和handler来处理。

为了更方便的实现这些操作，有了更强大等库requests。

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





### 基本用法

```python
import requests
r = requests.get("http://httpbin.org/get") # post/put/delete/head/options
print(r.text) 
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.22.0"
  },
  "origin": "222.128.57.46, 222.128.57.46",
  "url": "https://httpbin.org/get"
}
```

携带get参数：

```python
r = requset.get("http://httpbin.org/get?name=germey&age=22")
# 上述方式也可以不过有更方便的：
data = {'name': 'germey', 'age':22}
r = requsets.get("http://httpbin.org/get", params=data)
```

post请求：

上述get参数方式把get改为post即为post请求方式。

```python
//post有参数，使用data
r = requests.post('https://httpbin.org/post', data = {'key1':'value1', 'key2': 'value2'})
# 但是接收方接收的数据可能是这样的。。
key1=value1&key2=value2

# 所以说发送post请求还是要带上json.dumps
r = requests.post('https://httpbin.org/post', data = json.dumps(  {'key1':'value1', 'key2': 'value2'}))

# 更好一些的方式：
r = requests.post('https://httpbin.org/post', json = {'key1':'value1', 'key2': 'value2'})
        
```



### 返回结果

接口等返回类型是str类型， 但是它很特殊，是json格式的，如果直接像得到一个字典格式的话可以直接调用json方法： `r.json()`

其他属性：

```python
>>> r
<Response [200]>
>>> dir(r)
['...', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']

>>> r.content
b'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Host": "httpbin.org", \n    "User-Agent": "python-requests/2.22.0"\n  }, \n  "origin": "222.128.57.46, 222.128.57.46", \n  "url": "https://httpbin.org/get"\n}\n'

>>> r.ok
True
>>> r.url
'http://httpbin.org/get'
>>> r.status_code
200
>>> r.reason
'OK'
>>> r.raw
<urllib3.response.HTTPResponse object at 0x7f2f7efce250>
>>> r.json() # 算是字典类型
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.22.0'}, 'origin': '222.128.57.46, 222.128.57.46', 'url': 'https://httpbin.org/get'}
```

【注意】看下这些返回值的类型：

```python
>>> type(r.text)
<class 'str'>
>>> type(r.content)
<class 'bytes'>
>>> import json
>>> json.loads(r.text) # 注意这里，说明r.text是json话的结果
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.22.0'}, 'origin': '222.128.57.46, 222.128.57.46', 'url': 'https://httpbin.org/get'}
```





### 添加header

```python
# coding:utf-8
"""
爬知乎发现页
"""

import re
import requests
from pprint import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (Machtosh: Inter Mac OS X 10_11_4) AppleWebKit/573.36(KHTML, like Gecko Chrmoe/52.0.2743.116 Safari/537.36"
}

r = requests.get("https://www.zhihu.com/explore", headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
titles = re.findall(pattern, r.text)
pprint(titles)
```



### 下载和上传图片

抓取二进制数据， 以抓取GitHub的站点图标为例：

```python
import requests
r = requestsget("https://github.com/favicon.ico")
with open("favicon", "wb") as f:
    f.write(r.content)
```



文件上传：

```python
import requests
files = {'file': open('favicon.ico', 'rb')}
r.requests.post("htt://httpbin.org/post",files=files)
```



### Cookies

获取：

```python
r.cookies
for k, v in r.cookes.items():
```

添加：

```python
cookies = '_xsrf=Dhuf0hZqRKrxh9ozrBl8B3VqsUNcCDAA; _zap=6413d60b-9274-4405-a865-843fd0ea7bf9; d_c0="AKBll72CLg6PToOk8gK2ZiPuuNyugOR_q5c=|1536419449"; z_c0="2|1:0|10:1536419453|4:z_c0|92:Mi4xeEdkOEFBQUFBQUFBY0tTR3ZZSXVEaVlBQUFCZ0FsVk5mVFNCWEFDVzhlRDkzQjBaa3VyNWx4V0JBSWpKM1F1Z0VR|b5976fac18600eb4352b671c760309d9331ef1aa64a803c4df7a5b711321a2f6"; __utmv=51854390.100-1|2=registration_date=20140916=1^3=entry_date=20140916=1; q_c1=0f634672ca5b4e4d8d90c43854feed8e|1539524068000|1536419453000; tst=r; __utmc=51854390; __utmz=51854390.1540707323.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/wangyu-1994/collections; __utma=51854390.127633611.1536419518.1540707323.1541227447.3; __utmb=51854390.0.10.1541227447; tgw_l7_route=61066e97b5b7b3b0daad1bff47134a22'
header ={ "Cookie": ""}
r = requests.get("", headers = headers)
# 或者
jar = requests.cookies.RequestsCookieJar()
for c in cookies.split(';'):
    k,v = c.split('=',1)
    jar.set(key, value)
r = request.get("", cookies=jar)
```

添加的两种方式实现的效果是一样的。



### 会话维持

如何像正常登录网站时那样维持登录状态呢 而不是每次都是一个新的请求？

你可能说是设置Cookie， 但是每次设置它太繁琐。

那么便用到了Session对象。

```python
import requests
s = requests.Session()
s.get = ('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http:///httpbin.org/cookies')
print(r.text)
# 输出
{
    "cookies":{
        "number": "123456789"
    }
}
```



### SSL 证书验证

默认是会检查SSL证书的， 我们知道12306的证书之前是没有的，我们访问那样的网站会有问题：

```python
res = requests.get("https://www.12306.cn")
print(res.status_code)
# 异常：
requests.exceptions.SSLError
```

忽略证书检查：

`res = requests.get("https://www.1206.cn", verify=False)`

指定本地证书用作客户端证书：

`res = requests.get("https://www.12306.cn", cert=('/path/server.crt', '/path/key'))`



### 代理设置

```python
proxies = {
    "http": "http://10.10.1.10:3128",
    "https" "http://10.10.1.10:1080"
}
requests.get("https://www.taobao.com",proxies=proxies)
```

或需要使用HTTP Basic Auth, 类似： http://user:password@host:port

需要安装 :`pip install 'requests[socks]'`

```python
import requests
proxies = {
    'http': 'socks5://user:password@host:port',
    'https': 'socks5://user:password@host:port'
}
requests.get('', proxies=proxies)
```



### 身份认证

```python
from requests.auth import HTTPBasicAuth

r = requests.get("", auth=HTTPBasicAuth("username", "password"))

# 或直接简写
r = requests.get("", auth=("username", "password")) #和上面两行一样
```



OAuth认证：

需要安装oauth包

`pip install requests_oauthlib`

```python
from requests_oauthlib import OAuth1
auth = OAuth1("YOUR_APP_KEY", "YOUR_APP_SECRET",
             "USER_OAUTH_TOKEN", "USER_OAUTH_TOKEN_SECRET")
requests.get(url, auth=auth)
```



### Request

在urlib时 ，我们知道所有参数都可以放到一个Request对象里，requests也提供了这个功能。

```python
from requsets import Requset, Session
data={}
headers ={}
req = Reqeust('POST', url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)
```

这个对象在队列调度时非常方便。