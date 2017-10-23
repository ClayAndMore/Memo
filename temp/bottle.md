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

#### 动态路由
1. 请求参数放入URL路径中
`/user/<name>`
`/user/<name>/<id>`
2. 指定参数类型
    1. 获取整数参数： `/user/<id:int>`
    2. 获取浮点参数： `/user/<weight:float>`
    3. 获取路径参数： `/user/<mypath:path>`
    4. 指定正则表达： `/user/<re:re:[a=z]*>`
3. 自定义过滤函数
