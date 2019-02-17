
tags​:[Django, python] date:​ 2017-05-10



### Request 和 Response

HttpRequest是django自动创建的，表示客户端一个单独的http请求，是将请求request数据的一个封装，

几个属性：

* `request.method == "POST"`

* 类字典对象属性GET,POST

* COOKIES，字典形式

* user。 一个django.contrib.auth.models.User。 表示当前登录对象，若没有登录user自动设置为django.contrib.auth.models.AnonymousUser的一个实例。可以用`is_authenticated()`来区分：

  ```
  if request.user.is_authenticated():
  ...
  else:
  ...
  ```

* session, 字典形式，除了session属性，其他都被看作只读的。

* FILES,  上传文件。

* META.     是一个Python字典，包含了本次所有http请求的Header信息，如用户ip,浏览器名称，版本号

  * HTTP_REFERRER: 进站前的链接网页
  * HTTP_USER_AGENT:  用户的user_agent字符串
  * REMOTE_ADDR:  用户ip.

HttpResponse:

一个请求只返回一个HttpResponse，可构造，设置Header,用它的子类。



### URL映射

每个项目中都有个urls.py文件来维护url:

```python
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'year/2015/$',views.moments_2015),
]
```

urlpatterns中每个元素都是django.conf.urls.url的实例，函数url的第一个参数是HTTP路径，第二个参数是被映射到的函数。

调用形式：`moments_2015(request)`

request 是用户请求对象。我们在视图中会有讲解。

不需要添加一个前导的反斜杠，因为每个URL 都有.不要这样：`r'/year/2015/$`



#### 带参的url

**1 无参数情况**

配置URL及其视图如下：

```python
(r'^hello/$', hello)
 
def hello(request):
    return HttpResponse("Hello World")
```

访问http://127.0.0.1:8000/hello，输出结果为“Hello World”



**2 传递一个参数**
配置URL及其视图如下,URL中通过正则指定一个参数：

```python
(r'^plist/(.+)/$', helloParam）
 
def helloParam(request，param1):
    return HttpResponse("The param is : " + param1)
```

访问http://127.0.0.1:8000/plist/china，输出结果为”The param is : china”

调用形式： `helloParam(request,china)`

上面是使用简单的通过圆括号来捕获URL中的位置参数。



高级做法中使用命名的正则来捕获参数，此时捕获的值就是关键字参数了。

命名正则表达式组的语法是`(?P<name>pattern)`，其中`name` 是组的名称，`pattern` 是要匹配的模式。

```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    #没有使用命名组
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
]
```

捕获的值作为关键字参数而不是位置参数传递给视图函数。例如：

- `/articles/2005/03/` 请求将调用`views.month_archive(request, year='2005', month='03')`函数，而不是`views.month_archive(request, '2005', '03')`。
- `/articles/2003/03/03/` 请求将调用函数`views.article_detail(request, year='2003', month='03', day='03')`。

在实际应用中，这意味你的URLconf 会更加明晰且不容易产生参数顺序问题的错误 —— 你可以在你的视图函数定义中重新安排参数的顺序。当然，这些好处是以简洁为代价；有些开发人员认为命名组语法丑陋且繁琐。



**3 传递多个参数**
参照第二种情况，以传递两个参数为例，配置URL及其视图如下,URL中通过正则指定两个参数：

```python
(r'^plist/p1(\w+)p2(.+)/$', helloParams）
 
def helloParams(request，param1,param2):
    return HttpResponse("p1 = " + param1 + "; p2 = " + param2)
```

访问http://127.0.0.1:8000/plist/p1chinap22012/
输出为”p1 = china; p2 = 2012″

从这里可以看出，视图的参数是根据URL的正则式，按顺序匹配并自动赋值的。虽然这样可以实现任意多个参数的传递，但是却不够灵活，URL看起来很混乱，而且由于是正则匹配，有些情况下容易出错。



**4 通过传统的”?”传递参数**
例如，http://127.0.0.1:8000/plist/?p1=china&p2=2012，url中‘?’之后表示传递的参数，这里传递了p1和p2两个参数。

通过这样的方式传递参数，就不会出现因为正则匹配错误而导致的问题了。在Django中，此类参数的解析是通过request.GET.get方法获取的。

配置URL及其视图如下：

```python
(r'^plist/$', helloParams1）
 
def helloParams(request):
    p1 = request.GET.get('p1')
    p2 = request.GET.get('p2')
    return HttpResponse("p1 = " + p1 + "; p2 = " + p2)
```

输出结果为”p1 = china; p2 = 2012″



#### 分布式URL映射

一个项目中，一个项目中可以能包含多个Django应用。

Django用include()函数提供了分布式URL映射的功能，使得URL映射可以被编写在多个urls.py文件中。

```python
from django.conf.urls import include,url
urlpatterns=[
  url(r'^momnets/',include('djangosite.app.urls'))
]
```



#### 反向解析

从映射名到URL地址的解析。这样使得我们减少了写url路径的地方，提高了维护性。

```python
from django.conf.urls import include,url
urlpatterns=[
  url(r'^year/2017/$',views.year_moments,name="moments_2017")
]
```

通过name参数映射名为moments_2017。

在模版文件中：

```django
<a href="{% url 'moments_2017' %}">  
 查看2015年信息
</a>
```

解析后为`<a href="/year/2017/">`

带参数的解析：`<a href="{% url 'moments_2017',参数1 %}">`

eg ;

`<a href="{% url 'posts_list' post_class='language' post_type='python' %}">Python</a>`



在代码中使用reverse()函数来解析：

```python
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def redirect_to_year_2017(request):
	return HttpResponseRedirect(reverse('moments_2017'))
```

带参数：`return HttpResponseRedirect(reverse('moments_2017',args=(参数1,)))`



### 表单

新建djangosite/app/form.py

```python
from django.forms import ModelForm #Django表单类的基类
from .models import  Moment        #引入数据模型，与表单关联

class MomentForm(ModelForm):
    class Meta:					   #定义子类，在这里声明，模型和字段
        model=Moment
        fields='__all__'		   #这里是全部导入
        #fields=('conten','user_name','kind')  # 部分导入
```



#### 绑定状态

一个表单对象在实例化后被赋予数据，我们称它处于绑定（bound）状态。

通过is_bound属性来检查bound状态。

```
>>> f=MomentForm()
>>> print f.is_bound
False
>>> f=MomentForm({'beadline':'hello'})
>>> print f.is_bound
True
```

如果通过验证，我们通常这样验证表单：

`form = MomentForm(request.POST)`



#### 数据验证

用is_valid()函数在代码中获得表单验证是否通过的信息。

用errors或得错误提示信息。

```
>>> f=MomentForm({'user_name':'David'})
>>> print f.is_valid()
False
>>> print f.error
{'content':['This field is required.']}
```



#### cleaned_data

通过数据验证的(is_valid())form的cleaned_data才有值，不然为{}，这个字典中只有通过验证的字段，没有通过验证的字段将不再这里出现。



#### 自定义逻辑验证

通过重载Form类的clean函数进行定义。

```python
from django.forms import ModelForm,ValiationError
from app.models import Moment

class MomentForm(ModelForm):
	class Meta:
		model=Moment
		fields='__all__'
		
	def clean(self):
		cleaned_data=super(MomentForm,self).clean()
		content=cleaned_data.get("content")
		if content is None:
			raise ValidationError("请输入Content内容！")
		elif content.find("ABCD")>=0:
			raise ValidationError("不能输入敏感字段ABCD")
		return cleaned_data
```

这个在调用Form.is_valid()时自动被调用。



#### 检查变更字段

has_changed()来判断用户是否修改过表单数据。

```python
def view_moment(request):
	data={'content':'Please input the conten',
		'user_name':'匿名',
		'kind':'python技术'}
	f=MomentForm(request.POST,initial=data)
	if f.has_changed():
		# 此处编写保存f的代码
```

request.POST: Django从其中解析出用户的输入数据。

initial: Form 的初始值，调用has_changed 时，用initial中的字段值与初始字段值比较，如果有变化则返回True .

判断那些字段做了修改，changed_data 是包含字段名的列表。

```python
if f.has_changed():
	print '如下字段进行了修改：%s'
	for field in f.changed_data:
		print field
```



#### save()，获取表单值并修改。

当我们用ModelForm时，一般用`form=ContentForm(request.POST)`来获取表单值，通过form.save()来保存。

但是当我们要根据用户填写的数据动态的来为模型赋值保存我们可以这样：

```python
form = ContentForm(request.POST)
if form.is_valid():
    form_temp = form.save(commit=False) # 这里form_temp 得到的是一个model对象，很方便吧。
    form_temp.ip= '我想要的数'
    form_temp.save()  # 这时才真正保存。
```

commit 默认是True，这里为False时，并不真正保存，会获得model对象，涉及到关系模型去官网看。



### 模版文件

手动建立目录：djangosite/app/templates.

建立文件：`moments_input.html`:

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="?" method="post">
        <fieldset>
            <legend>请输入并提交</legend>
            {{form.as_p}}
            <input type="submit" value="submit"/>
        </fieldset>
    </form>
</body>
</html>
```

这是Django自己的模版语言。

from.as_p是定义表单的输入字段。后续详细补充。

http://python.usyiyi.cn/translate/django_182/ref/forms/api.html

这里api能看出`from.as_p` 可替换的东西，这里他都用print来打印，但是我们在模版中不能用print，在模版中我们将其中的`form['subject']`变为`form.subject` ,

从而：

```
lst = ['a', 'b', 'c']
di = {'a': 'a'}
class Foo:
   def bar(self): pass
```

You can do:

```
{{ lst.0 }}
{{ di.a }}
{{ foo.bar }}
```

就是说语句中所有的形式在模版中都是点的形式，包括方法。



### 视图

#### 创建视图

一段最简单的视图：

```
from django.http import HttpResponse
def hello(request):
	return HttpResponse("hello world")
```

每个视图函数中至少有一个参数-request，是django.http.HttpRequest 的一个实例，包含了当前web请求信息的对象。



#### 例子

djangosite/app/views.py:

```python
import os
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import MomentForm

def welcome(request):
    return HttpResponse("<h1>welcome to my tiny twitter!<h1>")

def moments_input(request):
    if request.method=='POST':
        form = MomentForm()
        if form.is_valid():
            moment=form.save()
            moment.save()
            return HttpResponseRedirect(reverse("app.views.welcome"))  #提交表单后重定向到欢迎页面。reverse这种用法在1.8中已经被弃用。最好用url文件中为函数分配的名字，直接reverse("name")

    else:
        form=MomentForm()
    PROJECT_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request,os.path.join(PROJECT_ROOT,'app\\templates','moments_input.html'),
                  {'form':form})
```

在djangosite/app/urls.py文件中添加该视图函数的路由映射：

```python
from django.conf.urls import url
from . import  views

urlpatterns=[
    url(r'^monents_input',views.moments_input),
    url(r'',views.welcome),
]
```

访问127.0.0.1:5000/app.moments_input:

![](http://ojynuthay.bkt.clouddn.com/moment_input.png)





### Admin

#### 创建管理员

忘记管理员的账号和密码也可以这么创建

```
python manage.py createsuperuser
#输入登录名
#输入email
#输入两次密码，八位，字母和数字。
```

修改用户密码：

`python manage.py changepassword username`





