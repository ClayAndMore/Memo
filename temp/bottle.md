## Bottle

单文件，上手快，配置性高，节约资源。

安装，`pip install bottle` 特别简单。
或者用yum或apt.

基础demo：
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

#### 关于请求
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

#### 动态路由
1. 请求参数放入URL路径中
`/user/<name>`
`/user/<name>/<id>`
2. 指定参数类型
    1. 获取整数参数： `/user/<id:int>`
    2. 获取浮点参数： `/user/<fid:float>`
    3. 获取路径参数： `/user/<mypath:path>`
    4. 指定正则表达： `/user/<ret:re:[a=z]*>`
3. 自定义过滤函数


#### 静态文件
`return static_file(filename,root="",mimetype=""，download=True)`
root是指跟目录，必须参数，如果这个文件在根目录下，root可以为空。
mimetype 是知名文件类型，一般会自动识别，可不填。
download 可选，是强制下载文件，如果设置为True，那么下载的文件名是你资源本来的名字，如果是其他则指定了下载文件名。


#### 错误页面
@error(404) 一个装饰器，参数为定义的错误类型。

#### URL转向
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

视图函数中指定返回字符编码：
`Response.charset='utf-8'`
`Response.content_type='text/html;charset=gbk'`
