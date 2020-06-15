
---
title: "Flask整理（二）.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[flask,python]  date: 2017-01-31



### 使用BootStrap

**Bootstrap**: 是一个基于 HTML/CSS/JavaScript 的前端框架, 兼容大部分的 jQuery 插件, 它简洁灵活, 提供了大量内置的样式接口，使得 Web 开发更加简单快捷.

* 下载

到官网下载https://getbootstrap.com/，会有三个下载源，第一个（bootstrap)是简易压缩版的,第二个（source code）是源文件，第三个是sass本版的。第一个就足够用

将下载的解药到static文件下。

* 继承

  这里用于一个基础模板用于继承：base.html

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,, initial-scale=1">
    <!-- Will be replace the page title -->
    <title>{% block title %}Home{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
  </head>
  <body>
    <div class="container">
      <div class="jumbotron">
        <!-- Replace the route function to URL: `/` -->
        <h1><a href="{{ url_for('home')}} ">Claymore's Blog</a></h1>
          <p>Welcome to the blog!</p>
      </div>
      {% block body %}
          body_content
      {% endblock %}
    </div>
    <script src="{{ url_for('static', filename='js/jquery.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
  </body>
  </html>
  ```


其他文件继承上面的文件则 代码块里 ：extends “base.html"

在主程序中：

```
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
```



### 使用蓝图创建控制器（controller）

mvc中，最后一块是控制器，我们在main.py中已经了解了试图函数的基本用法，我们需要更强大更复杂的方式来将视图函数组织成更机密的整体。

#### 请求构建和销毁，和全局变量
请求中会访问全局变量，所有函数都会访问到它。
Flask中装饰器函数`@app.before_request`会在每个请求被创建的时候**之前**执行它所装饰的函数。
`@app.teardown_request`会在每个请求结束的时候执行。
全局变量g（为每个特点请求临时存储特定数据，并且是线程安全的。）

#### 自定义错误页面
如果向用户显示浏览器默认的错误页面，会显得特别突兀，而且没有让用户返回主页。
Flask的abort()返回错误页面时，可以用errorhandler装饰器来显示你自己定义的模板。

```python
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pageNotFound.html'),404
```
app.errorhandle可以接收一个或者多个http状态码。

#### 使用类描述视图
如果很多视图处理函数都会用到一些通用的功能，我们把他总结成几个函数比较好，这时用类来体现，享受继承的好处。
```python
from falsk.views import View  # 导入视图类 

class GenericView(View):
    def __init__(self,template):
        self.template= template
        super(GenericView,self).__init__()
        
    def dispatch_request(self):
        return render_template(self,template)
    
app.add_url_rule(
    '/',
    view_func=GenericView.as_view(
    'home',template='home.html'
    )
)
```
View类是flask代替视图函数注册路由的另一种实现方式。
dispatch_request函数是一个普通函数，返回了一个HTML字符串。
app.add-url_rule()跟app.route()作用类似，同样是把一个路由返回到一个函数上。
第一个参数定义了绑定的路由,
view_func变量定义了用来处理路由的函数，as_view会把类转成一个试图函数，所以这里第一个参数定义了转成试图函数的名字，使得url_for()之类的函数能够通过这个名字找到，后面的其他参数会直接传递给该试图类的`__int__()`方法。
**非get方式**：
跟普通的函数一样，在使用view类试图的时候，除GET为的其他http请求需要被显式的声明才能使用。
```python
class GenericView(View):
    methonds=['GET','POST']
    ...
    def dispatch_request(self):
        if request.method == 'GET':
            return render_template(self.template)
        elif request.method == 'POST':
```
#### 方法视图
处理多种HTTP请求时，会写大量的判断语句：
```
@app.route('/user',method=['GET','POST','PUT','DELETE'])
def users():
    if request.method=='GET':
    ...
    elif request.method=='POST':
    ...
    elif request.method=='PUT':
    ...
    elif request.method=='DELETE':
    ...
```
我们用MethonView(方法视图）来解决。他把每种http请求写成一个同名的类方法。
```
from flask.views import MethodView

class UserView(MethodView):
    def get(self):
    ...
    def post(self):
    ...
    def put(self):
    ...
    def delete(self):
    ...
    app.add_url_rule(){
    '/user'.
    view_func=UserView.as_view('user')}
```
app.add-url_rule()跟app.route()作用类似，同样是把一个路由返回到一个函数上。
第一个参数定义了绑定的路由.
View_func变量地冠以了处理路由的函数。

#### 蓝图
在Flask中，蓝图（blueprint)是一种用来扩展自已有Flask应用结构的方式。
把共有的东西统一起来，让结构更紧密。
```python
from flask import Blueprint
blueprint=Blueprint(
    'blogblue',   #蓝图名
    __name__,      # 当前包的名字，我们只要把__name__传给它就可以了。
    template_folder='templates/blog',  #所有模板文件都放到blog文件夹下
    static_folder='static/example',
    url_prefix='/hh'        
)
@example.route('/')
def home():
    return render_template('home.html')
```
前两个参数是固定的，其他参数规定蓝图去什么位置找文件，如上，对应的页面会渲染templates/blog/home.html.
url_prefix选项会自动把URL前缀添加在这个蓝图所有的路由之前。所以渲染上面的模板实际路径是：`127.0.0.1：5000/hh/`
**使用url_for**:
在蓝本中使用url_for()函数和原来在程序中使用不一样，蓝本中的全部端点上加入一个命名空间。

其实这个命名空间就是蓝图的名字（如上blogblue），所以home（函数名）的端点名是bolgblue,其url使用`url_for('bolgblue.home')`可以省略蓝本名:`url_for('.index')`
**注册**：
最后的`if __name__='__main__':`语句之前注册蓝图：
`app.register_blueprint(blueprint)`
要在末尾导入，因为其他文件也要导入蓝本，这样可以避免循环导入依赖。



### 工厂模式生成应用对象

**工厂模式**：就是通过某一个接口函数或对象来创建另一个对象，而这个接口函数也称之为工厂函数。 工厂模式使一个类的实例化延迟到其子类。也就是说**工厂模式可以推迟到在程序运行的时候才动态决定要创建哪个类的实例，而不是在编译时就必须知道要实例化哪个类**。

eg:

```python
class Circle(object):
    def draw(self):
        print 'draw circle'

class Rectangle(object):
    def draw(self):
        print 'draw Rectangle'

class ShapeFactory(object):
    def create(self, shape):
        if shape == 'Circle':
            return Circle()
        elif shape == 'Rectangle':
            return Rectangle()
        else:
            return None

fac = ShapeFactory()
obj = fac.create('Circle')
obj.draw()
```

在主函数main.py中：

```python
from flask import Flask, redirect, url_for

from models import db
from controllers import blog

def create_app(object_name):
    """Create the app instance via `Factory Method`"""
    app = Flask(__name__)
    # Set the app config 
    app.config.from_object(object_name)

    # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object
    db.init_app(app)

    @app.route('/')
    def index():
        # Redirect the Request_url '/' to '/blog/'
        return redirect(url_for('blog.home'))

    # Register the Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)

    return app
```

这时，app.config.from_object(object_name)变为了一个变量，我们在manage.py中将变量传入：

```python
from Flask main import creat_app
# Get the ENV from os_environ
env = os.environ.get('BLOG_ENV', 'dev') #如果没有环境变量，则环境变量BLog_env的值为dev
# Create thr app instance via Factory Method
app = create_app('jmilkfansblog.config.%sConfig' % env.capitalize())#capitalize() 首字母大写
```



### 目录结构

![](http://7xs1eq.com1.z0.glb.clouddn.com/snipaste20170104_120159.png)

### 需求文件
一个txt文件，写了各个扩展的版本
`pip freeze>requirements.txt`
创建一个新的和上面版本一样的虚拟环境：
`pip install -r requirements.txt`



### Bcrypt密文存储账户信息

使用明文的方式存储账户数据是一个非常严重的安全隐患，要保护用户的密码，就要使用 **哈希算法的单向加密方法**。 
**哈希算法**：对于相同的数据，哈希算法总是会生成相同的结果。 
**单向加密**：就是信息在加密之后，其原始信息是不可能通过密文反向计算出来的。 
所以，为了账户信息的安全，在[数据库](http://lib.csdn.net/base/mysql)中存储的密码应该是被哈希过的哈希值。但是需要注意，哈希算法的种类很多，其中大多是是不安全的，可以被黑客 **暴力破解**。 
**暴力破解**：通过遍历各种数据的哈希值，来找到匹配的哈希值，从而获取你的密码权限。 
所以这里我们使用 **Bcrypt** 哈希算法，这是一种被刻意设计成抵消且缓慢的哈希计算方式，从而极大的加长了暴力破解的时间和成本，以此来保证安全性。

安装：

`pip install Flask-Bcrypt`

extensions.py

```python
from flask.ext.bcrypt import Bcrypt

# Create the Flask-Bcrypt's instance
bcrypt = Bcrypt()
```

在main.py（`__init__`py）:导入bcrypt,然后。bcrypt,init_app(app)

数据模型models.py中，对要加密的模型：

```python
def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
```

- `set_password(self, password)`：在设定密码的时候，将明文密码转换成为 Bcrypt 类型的哈希值。
- `check_password(self, password)`：检验输入的密码的哈希值，与存储在数据库中的哈希值是否一致。



### reCAPTCHA实现验证码

reCAPTCHA 的使用起来并不复杂，在注册一个 Google 用户名后，进入到 reCAPTCHA 官网 并输入你的 blog 名(随意填写)和域名(只支持域名和子域名，现在我们暂时使用 localhost，等部署到线上之后也需要将新的域名填入)，就会得到一个 Public Key，就可以把它用在你的 reCAPTCHA 插件上了，同时 reCAPTCHA 也支持多个站点。

```python
class Config(object):
    """Base config class."""
    # WTForm secret key
    SECRET_KEY = 'WTForms key'
    # reCAPTCHA Public key and Private key
    RECAPTCHA_PUBLIC_KEY = "<your public key>"  #网站上的Site key
    RECAPTCHA_PRIVATE_KEY = "<your private key>" #网站上的Secret key
```

添加验证码控件：

```python
class RegisterForm(Form):
    """Register Form."""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    comfirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()

```

页面实现：register.html,去掉继承和括号，以为这里会影响到我的博客。

```jinja2
{% 继承(extends) "base.html" %}                                      

{% block title %}                                                          
  Register                                                                 
{% endblock %}                                                             

{% block captcha %}                                                        
  <script src='https://www.google.com/recaptcha/api.js'></script>          
{% endblock %}

{% block body %}                                                           
<div class="col-lg-3">
  <!-- Set the form -->                                                    
  <form method="POST" action="{{ url_for('main.register')                  
    }}">
    {{ form.hidden_tag() }}
    <div> 
      {{ form.username.label }}                                            
      {{ form.username(class_="form-control") }}                           
    </div>
    <div class="form-group">                                               
      {{ form.password.label }}                                            
      {{ form.password(class_='form-control') }}                           
    </div>
    <div class="form-group">
      {{ form.comfirm.label }}
      {{ form.comfirm(class_='form-control') }}                            
    </div>
    <input class="btn btn-primary" type="submit" value="Register">         
    <div class="g-recaptcha" data-sitekey="<Your public key>"></div>
  </form>
</div>
{% endblock %}
```

在模板 register 中需要按照 reCAPTCHA 官档给出的方法将 `` 和 `` 应用到该模板中, 验证码才会生效.



### Flask Login保护登陆安全
**我们每个页面都需要对用户的身份进行认证。**在这样的应用场景下, 保存用户的登录状态的功能就显得非常重要了. 为了实现这一功能:

- 第一种方法, 用得最多的技术就是 session 和 cookie，我们会把用户登录的信息存放在客户端的 cookie 里，这样，我们每个页面都从这个 cookie 里获得用户是否已经登录的信息，从而达到记录状态，验证用户的目的.
- 第二种方法, 我们这里会使用 Flask-Login 扩展是提供支撑.

**NOTE**: 两种方法是不能够共存的.

安装：

`pip install flask-login`

初始化对象：

extensions.py

```python
from flask.ext.login import LoginManager

login_manager=LoginManager()
```

设置loginManager对象的参数

extensions.py

```python
# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more stronger auth-protection.
#     3. Show the information when you are logging.
#     4. Set the Login Messages type as `information`.
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from models import User
    return User.query.filter_by(id=user_id).first()
```

**NOTE 1**: login_view 指定了登录页面的视图函数 
**NOTE 2**: session_protection 能够更好的防止恶意用户篡改 cookies, 当发现 cookies 被篡改时, 该用户的 session 对象会被立即删除, 导致强制重新登录. 
**NOTE 3**: login_message 指定了提供用户登录的文案 
**NOTE 4**: login_category 指定了登录信息的类别为 info 
**NOTE 5**: 我们需要定义一个 `LoginManager.user_loader` 回调函数，它的作用是在用户登录并调用 `login_user()` 的时候, 根据 user_id 找到对应的 user, 如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.

修改用户的数据模型：

```python

#检验 User 的实例化对象是否登录了.
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

#检验用户是否通过某些验证
    def is_active(self):
        return True

#检验用户是否为匿名用户
    def is_anonymous(self):
        """Check the user's login status whether is anonymous."""

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

 # 返回user实例化对象的唯一标识id
    def get_id(self):
        """Get the user's uuid from database."""
        return str(self.id)  # unicode

```



### 构建RESTful Flaks API

Rest是人们对通信所做的约束，

* 客户端和服务端关心的业务是完全分离的
* 服务端是无状态的，处理请求所需要的信息都u要求储存在客户端、
* 所有资源必须有同意接口的形式

等，当一个系统满足了所有这些约束，可以被认为它是一个RESTful系统。最常见的形式是由http和json构建的。每种资源都有自己url来定位。

| http请求方法 | url                    | 操作                  |
| -------- | ---------------------- | ------------------- |
| get      | http://host/resource   | 返回该资源所有的条目          |
| get      | http://host/resource/1 | 返回id为1的资源           |
| post     | http://host/resource   | 通过post的表单内容创建一个新的资源 |
| put      | http://host/resource/1 | 修改id为1的已存在的资源       |
| delete   | http://host/resource/1 | 删除id为1的资源           |

**URI**: `protocol://hostname[:port]/path` 定义了某一类资源 
**URL**: `protocol://hostname[:port]/path/[;parameters][?query]#fragment` 定义了某一个具体的资源单位

#### 为什么要构建restful api

对于一个 blog application 而言, 其实完全可以不用到 restful api 也能满足日常所需. 加入 restful api 的唯一目标就是加强该项目的可扩展性, 为后期所要实现的诸如: 博客迁移/数据备份/功能扩展 提供统一且可靠的接口.



### 使用ajax

