
---
title: "Flask整理（三）.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[flask,python]  date: 2017-03-30

### Itsdangerous

当我们注册一个网站的账号时，总会让我们点击注册邮箱的链接来确定认证，这个认证过成就用到了itsdangerous中的加密过程。

官网：https://pythonhosted.org/itsdangerous/

下面是一个为邮件加密的过程，

fortoken.py：

```python
from itsdangerous import  URLSafeSerializer

def generote_confirmation_token(app,email):
    serializer=URLSafeSerializer(app.config['SECRET_KEY'],salt=app.config['SECURITY_PASSWORD_SALT'])
    return serializer.dumps(email)

def back_confirmation_token(app,token):
    serializer=URLSafeSerializer(app.config['SECRET_KEY'],salt=app.config['SECURITY_PASSWORD_SALT'])
    return serializer.loads(token)  #返回email

```

第一个函数是根据用户邮箱来生成token，第二个函数是根据上一个函数生成的token来反向获取邮箱达到确认的目的。



### Flask_Mail

用qq邮箱发邮箱。

```python
from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)
#下面是SMTP服务器配置，可以在相关邮件代理查到，比如我这个用的就是腾讯的。
app.config['MAIL_SERVER'] = 'smtp.qq.com' #电子邮件服务器的主机名或IP地址
app.config['MAIL_PORT'] = '465' #电子邮件服务器的端口
app.config['MAIL_USE_SSL'] = True #启用安全套接层
app.config['MAIL_USERNAME'] = '4xxxxxxx@qq.com' #你的邮件账户用户名
app.config['MAIL_PASSWORD'] = 'mnwasfnnmrnwbgdd' #邮件账户的授权码,会通过手机发送

mail = Mail(app)

@app.route('/')
def index():
    msg = Message('主题', sender=app.config['MAIL_USERNAME'], recipients=['384399322@qq.com'])
    msg.body = '这是body'
    msg.html = '<b>HTML,板砖板砖，我是熊猫，收到请回答，over</b>'
    mail.send(msg)

    return '<h1>邮件发送成功</h1>'

if __name__ == '__main__':
    app.run()

```



### Flask_Security

非常强大，提供：

* 角色管理，权限管理
* 用户东路，邮箱验证
* 密码重置，密码加密

安装：

`pip install flask-security`

官方文档：http://pythonhosted.org/Flask-Security/

它集成了很多其他扩展：

```
Flask-Login
Flask-Mail
Flask-Principal
Flask-Script
Flask-WTF
itsdangerous
passlib
```

提供七种基本模板，要用的话，在模板目录下创建security的文件目录：添加相关模板：

```
security/forgot_password.html
security/login_user.html
security/register_user.html
security/reset_password.html
security/change_password.html
security/send_confirmation.html
security/send_login.html
```

如果指定自己的页面，设置变量`SECURITY_LOGIN_USER_TEMPLATE`这是指定登陆界面，其他可到官网查。

后续再写。这个扩展比较大。

### Flask_Admin

* 安装：

  `pip install Flask-Admin`

* 初始化：

  ```python
  from flask_admin import Admin
  admin=Admin(name='导航栏显示的名字')
  #注册到app中：
  admin.init_app(app)
  ```


启动服务，访问/admin 就可以看到效果

* 有三种视图类：

#### BaseView: 基础视图

能够生成最基本的视图, 并添加到 Admin 页面上, 如果你希望在 Admin 页面上加入一些 JavaScript 图表的话, 就可以使用 BaseView.

webapp/controllers/admin.py

```python
from flask_admin import BaseView, expose

class CustomView(BaseView):
    @expose('/')       #和bluprint.route一样，每个BaseView必须有根视图函数
    def index(self):
        return self.render('admin/custom.html')  #self.render和renter_template使用方法一样

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')
```

模板文件/templates/admin/custom.html：

```jinja2
{% extends 'admin/master.html' %}
{% block body %}
  This is the custom view!
  <a href="{{ url_for('customview.second_page') }}">Link</a> #注意这里可以跳转视图函数
{% endblock %}
```

将 CustiomView 注册到 flask_admin 对象中：

```python
def create_app(objet_name):
...
    #### Init the Flask-Admin via app object
    flask_admin.init_app(app)
    # Register view function `CustomView` into Flask-Admin
    flask_admin.add_view(CustomView(name='Custom'))#这个名字是显示的名字
```



#### ModelView: 模型视图

webapp/extensions.py

```python
from flask_admin import Admin,ModeView
admin=Admin(name='后台管理', template_mode='bootstrap3')

admin.add_view(ModeView(User,db.session,name='用户'))
admin.add_view(ModeView(Role,db.session,name='权限'))
```

剩下的在工厂函数中初始化就可以了：`admin.init_app(app)`

这时启动服务就会看到相关的数据和操作了。

加管理员权限认证：

```python
class needAdminView(ModelView):
    def is_accessible(self):
        role_list=current_user.roles
        if role_list:
            #遍历用户所有的权限：
            for role in role_list:
               if role.permissions==Permission.ADMINISTER:
                   return True
            # 没有管理员权限
            return False
        # 如果没有登陆
        return False

admin.add_view(needAdminView(User,db.session,name='用户'))
admin.add_view(needAdminView(Role,db.session,name='权限'))
```



上面的方式，是导航栏中会添加每一项数据模型，如果把这些数据模型放到下拉列表：

```python
models = [Role, Tag, Reminder, BrowseVolume]
    for model in models:
        admin.add_view(
            needAdmin	(model, db.session, category='Models'))   
```

category 关键字参数会告诉 Flask-Admin 将拥有相同 category 值的对象放进同一个下拉框中. EG. 这里的 Role, Tag, Reminder, BrowseVolume 对象, 它们会出现在同一个下拉框中.



#### FileAdmin: 本地文件系统管理

提供文件管理的内容。

```python
from flask_admin import FileAdmin
class CustomFileAdmin(FileAdim):
	pass

#初始化
from webapp/controllers import admin

    #### Init the Flask-Admin via app object
    flask_admin.init_app(app)
...
    # Register and define path of File System for Flask-Admin
    admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), 'static'),
            '/static',
            name='Static Files'))
```

`os.path.join(os.path.dirname(__file__), 'static')` 的值为 你需要管理的文件目录在系统中的全路径. name 参数指定了在管理页面显示 Label 的名字.



### Flask_Uploads

`install flask-uploads`

初始：

```python
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

icon=UploadSet('TEST')  #uploadset是个集合，第一参数是名字，也就是你给这个要上传的功能取的名字
configure_uploads(app,icon)  # 这个可以放在工厂模式里

```

在config.py中的配置：

```python
from flask_uploads import IMAGES  
  
UPLOADED_TEST_DEST=r'E:\flasky\app\flask_upload'  
UPLOADED_TEST_ALLOW=IMAGES  #允许上传的类型，这里只允许了图片
```

路由：

```python
from werkzeug.utils import secure_filename  # 确认文件名，但是会摒弃带中文的文件名
@community_blue.route('/personalInfo.html',methods=['GET','POST'])
def persionalInfo():
    form=ChangeImage()
    if form.validate_on_submit():
        file=form.browse.data     #上传的文件
        filename=secure_filename(file.filename) 
        icon.save(file,name=filename)
        return '上传完成'
    return render_template('personalInfo.html',form=form)
```

filename需要以.+文件格式，如.jpg。不然会报`UploadNotAllowed()`的错误。

表单：

```python
class ChangeImage(FlaskForm):
    browse=FileField(
        '上传',
        validators=[DataRequired()]
    )
    upload=SubmitField(
        '完成',
    )
```

模板：

```jinja2
<form action="" method=post enctype=multipart/form-data>
        {{ form.csrf_token }}
        {{ form.browse }}
        
        {% if form.browse.errors %}
            {% for e in form.browse.errors %}
                <p class="help-block" style="color: red">{{ e }}</p>
            {% endfor %}
        {% else %}
            <br>
        {% endif %}
        
        {{ form.upload }}
    </form>
```

注意form中的enctype.

设置上传文件的大小。

设置这个的目的是，防止有人给你捣乱，消耗你的流量。

放在manage.py里面执行，我把文件大小设置成了102400，也就是100KB，他默认是16MB

`flaskext.uploads.patch_request_class(app.size=102400)`



### PIL

`pip install  Pillow`

pil 不是一个单独的库了，已经包含在pillow中。丰富的图片处理库。
