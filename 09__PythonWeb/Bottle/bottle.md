---
title: "bottle.md"
date: 2019-11-18 17:54:22 +0800
lastmod: 2019-11-18 17:54:22 +0800
draft: false
tags: ["bottle"]
categories: ["python web"]
author: "Claymore"

---


## Bottle

单文件，上手快，配置性高，节约资源。

安装，`pip install bottle` 特别简单。
或者用yum或apt.

### 启动

基础demo.py：

```python
 from bottle import route,run

 @route('/')
 def index():
     return 'I am bottle!'
    
run(host='localhost',port='80')
```
这样就可作为一个简单的服务而启动了。

run的其他两个参数：
* debug=True  用于调试时页面给我们具体的错误信息
* reload=True 当我们修改代码时，服务会重新启动




一种特别的启动方式，可方便用于启动多个bottle进程，

`python bottle.py -b 127.0.0.1:8080 demo`

demo是文件demo.py  这里不能写绝对路径




### 关于请求
指定请求
* @route('/name')
* @route('/name',method="POST")
* @route('/name',method=["GET","POST"])
* @get()/@post
  eg:
```python
@get('/name')
@post('/name')
def index():
```

在视图函数内分别是什么请求：
```python
from bottle import requet
if request.method == "GET":
if request.method == "POST":
```
当用get查传递参数时：
```python
name = request.query.name
tel = request.query.telphone
```
不存在则返回空。
当用post传递参数时：
```python
name = request.forms.get('name')
tel = request.forms.get('tel')
email = request.forms.get('email')
```

如果或得所有参数： `all = json.loads(request.body.read())`





### 动态路由

1. 请求参数放入URL路径中
    `/user/<name>`
    `/user/<name>/<id>`
2. 指定参数类型
    1. 获取整数参数： `/user/<id:int>`

    2. 获取浮点参数： `/user/<fid:float>`

    3. 获取路径参数： `/user/<mypath:path>`

    4. 指定正则表达： `/user/<ret:re:[a=z]*>`

    5. 另一种表达方式：

       `@route(’/hello/:name’) `

       ` @route('/object/:id#[0-9]+#') `
3. 自定义过滤函数


### 静态文件
`return static_file(filename,root="",mimetype=""，download=True)`
root是指跟目录，必须参数，如果这个文件在根目录下，root可以为空。
mimetype 是知名文件类型，一般会自动识别，可不填。
download 可选，是强制下载文件，如果设置为True，那么下载的文件名是你资源本来的名字，如果是其他则指定了下载文件名。


### 错误页面
@error(404) 一个装饰器，参数为定义的错误类型。

### URL转向
abort()
```python
@error(500)
def index(err):
    print err
    return "这是500错误"

@route('/abort')
def index():
    abort(500,'err 404')
```
这里abort的第二个参数还没有明确

edirect('/'),跳转到首页。
```python
@route('/')
def index():
    return '这是首页'

@route('/de')
def index():
    redirect('/')
```

### 为客户端返回不同的数据类型
对于WSGI来说，PYthon中的数据类型不能直接被视图函数中返回给客户端，
bottle提供了对某些类型和编码的转换支持。

对于bottle来说可以直接返回给客户端的类型：
* 字典，转换为JSON，Content-Type 设置为application/json
* 空值（None,False,'',{},[]） 返回空，Content-Length设置为0
* 字符串 ,y依据Content-Type 对其进行编码后返回
* 字节 ， 转换为字符串
* 列表和元祖， 转换为字符串，但是不能有嵌套的列表和元祖。 列表中元素应为字符串，返回时会自动合并：
    ```python
    @route('/')
    def index():
        return ['aa','cc','dd']
    ```

视图函数中指定返回字符编码,两种方式：
`Response.charset='utf-8'`
`Response.content_type='text/html;charset=gbk'`



### header

响应的头文件如 `Cache-Control` 或者 `Location` 等都是通过 @Response.set_header() 函数定义的，该函数接受两个参数：一个头文件名称和一个值，名称部分是区分大小写的：

```python
@route('/wiki/page')
def wiki(page):
    response.set_header('Content-Language', 'en')
```

绝大多数头文件都仅仅只能定义一次，但是有一些特别的头文件却可以多次定义，这个时候我们在第一次定义时使用`Response.set_header()` ，但是第二次定义时，就需要使用 `Response.add_header()` 了：

```
response.set_header('Set-Cookie','name=value')
response.add_header('Set-Cookie','name1=value1')
```



### cookie

#### 添加cookie

```python
import response 
response.set_cookie('name','value')
```

这时我们到浏览器去看，会看到相关cookie (name,value)

set_cookie 有几个参数：

* max_age = x (seconds)  设置会话过期时间
* expires = datetime  
* domain =  默认设置为当前域
* path = '/'
* secure = off/on , 限制必须为HTTPS连接
* httponly = on/off 

`response.get_cookie('name')`   得到cookie的值



#### 加密cookie

`response.set_cookie('name','value',secret='...')` 

secret 是我们的密钥。

`request.get_cookie('name',secret='...')`

得到加密的cookie,密钥要和设置的相同。



#### 中文cookie

当cookie中有中文时，未加密

可用urllib.parse.quote对其进行URL编码，

用urllib.parse.unquote 对其进行URL解码。

```python
from urllib.parse import quote,unquote
response.set_cookie('myname',quote('我'))
```



加密则直接使用，不用处理。



### 返回图片

 using stream instead of static_file 

```python
from PIL import Image
@route('/image')
def video_image():
    image_buffer = BytesIO()
    #pi_camera.capture(image_buffer, format='jpeg') # This works without a problem
    my_iamge = Image.new('RGB', (self.width, self.height), self.clo)
    my_image.save(image_buffer, 'jpeg')

    image_buffer.seek(0) # this may not be needed
    bytes = image_buffer.read()
    response.set_header('Content-type', 'image/jpeg')
    return bytes
```



### 内建模版引擎

嵌入变量：

```python
from bottle import template
template('Hello {{name}})',name='Bottle')
template('Str with{{a}} many {{b}} values',**dict) #可以用字典传递参数。

# 传递html代码
link = '<a href="www.baidu.com">百度</a>'
template('进入{{ !link }}',link=link)  #变量前加入！使模版停止对htnml转义成字符串。
```

陷入python代码：



### 部署

run(server='gunicorn')

pip install gunicorn 

这样启动就是不用了bottle自带的服务器，而是用gunicorn服务器。



### 实践出真知

api多了 ，可以分文件划分，这样看起来整洁，

在run.py: 

```
import other_api_file
```



### 问题

#### Broken pip

在` /usr/lib/python2.7/wsgiref/handlers.py"` 中有时有  `[[Errno 32\] Broken pipe]` 的异常，可能是api请求过于频繁导致的。