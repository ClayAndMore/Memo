---
title: Django(一)
date: 2017-04-27 13:50:03
categories: Django
header-img:
tags: Django
---

### 概述

2003年根据一爵士音乐家Django命名，意味着能优雅的演奏（开发）功能丰富的乐曲（web应用）。

是功能最完善的web框架，意味着各模块间紧密耦合。主要特点：

* 完善的文档。http://usyiyi.cn/translate/django_182/contents.html
* 集成数据访问组件：Django的model层自带数据库ORM组件，使开发者无须学习其他数据库访问技术（dbi,SQLAlchemy)等。
* URL映射技术：正则表达管理URL映射。
* 后台管理系统自动生成，几行配置和代码就可以实现完整的后台数据web控制台
* 错误信息非常完整。调试时的错误信息非常完整。

组成结构：

遵循MVC架构的web开发框架。

* 管理工具（management):内置的创建站点，迁移数据，维护静态文件的命令工具。
* 模型（Model): 提供数据访问接口和模块，包括数据字段，元数据，数据关系的定义和操作。
* 视图（View): Django的试图封装了HTTP Request 和 Response 的一系列操作和数据流，主要包括URL映射，绑定模板
* 模板（Template): 是一套Django自己的页面渲染模板语言，用于内置的tags和filters定义页面的生成方式。
* 表单（Form):通过内置的数据类型和控件生成HTML表单。
* 管理站（Admin): 管理Model,快速生成后台数据管理网站。



### 安装

`pip install django`

验证是否成功：

```
#python
>>>import django
>>>print django.VERSION
```



### 目录

#### 建立项目

用django-admin建立Django项目，语法如下：

`#django-admin startproject 项目名称`

django-admin是安装好DJango组件后再Python目录中生成的Django项目管理工具。

eg:

 `#django-admin startprotject djangosite`

会在当前目录中建立了一个子目录djangosite,并生成了django开发默认的文件，：

​	![](http://ojynuthay.bkt.clouddn.com/startproject.png)

* manage.py: 是管理本项目的命令行工具，之后进行站点运行、数据库自动生成，静态文件收集等都要通过该文件生成。
* 内层`djangosite/`目录中包含了本项目的实际文件，同时应为其中包含`__init__.py`文件，该目录也是一个python包。
* djangosite/settings.py 配置文件，定义了引用的django组件，django项目名等。后续中配置数据库参数等。
* djangosite/urls.py :维护项目的url 路径映射。默认只定义了`/admin`即管理员站点的解释器。
* djangosite/wsgi.py: 定义WSGI的接口信息，用于与其他web服务器集成，一般文件在生成后无需改动。

#### 建立应用

一个项目一般包含多个应用。

一个应用也可以在多个项目中。

`#python manage.py startapp 应用名称`

此时的目录和结构：![](http://ojynuthay.bkt.clouddn.com/startapp.png)

* admin.py:管理站点模型的声明文件，默认为空
* app.py : 应用信息定义文件。生成了类AppConfig,该类用于定义应用名等Meta数据。
* migrations包： 用于在之后定义引用迁移功能。
* models.py包：添加模型层数据类的文件。
* tests.py：测试代码文件。
* views.py： 定义URL响应函数。


每建立一个应用都要在setting.py的INSTALLED_APPS 中添加这个应用的名字。



### Migrate 

数据迁移，makemigrations出错时去删改文件，找错误原因，再makemigrations.

migrate 出错时 去删改文件，删掉django-migrate数据库中的记录，再makemigrations和migrate。



### 开始

在djangosite/app/views.py 中建立一个路由响应函数：

```python
from django.http import HttpResponse

def welcome(request):
	return HttpResponse("<h1>Hello world!</h1>")
```

定义了一个函数，返回被HttpResponse()包装的welcome信息。

下面要通过URL映射将用户的HTTP访问与该函数绑定起来。

diangosite/app/新建urls.py文件，管理app中的所有url映射。

urls.py:

```python
from django.conf.urls import url #所有路由映射函数都由该函数生成。
from . import views
url_patterns=[
  url(r'',view.welcome)
]
```



接下来在djangosite/urls.py中urlpatterns增添一项，声明对应用app中urls.py文件的引用，代码如下：

```python
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    url(r'^app/', include('app.urls')),
    url(r'^admin/', admin.site.urls),
]

```

 **注意** ： url()函数的第一个参数用正则表达式来表达URL路由，第二个参数是被调用函数的名称，不能添加小括号。

上面的代码表示所有以app开头的路由。



#### settings 配置

mysql:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

name 为mysql中的数据库名，要确保你先前已经建立好了一个名为‘djangodb’的数据库。

时区配置：

TIME_ZONE = 'Asia/Shanghai'



url配置：

`ROOT_URLCONF = 'mysite.urls'`

在生成项目时，这个配置就已经存在了，Django会根据文件mysite/urls.py 自动找到url映射关系。



模版配置：

```
TEMPLATE_DIRS=(
	'/home/django/mysite/templates'，
)
或：
TEMPLATE_DIRS=[
  'DIRS':['/home/django/mysite/templates'],
]
```

这里告诉django在哪里加载模版，别忘了逗号

动态构建：

```python
import os.path
TEMPLATE_DIRS=(
	os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
)
或：
TEMPLATE_DIRS=[
  	'DIRS': [os.path.join(BASE_DIR,'templates')],
]
```

python内部变量file，为python文件所在目录，将该目录与‘templates’拼接，如果在window下，会自动改变反斜杠。



静态文件配置：

```
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),) # 主要是这句话，会帮你找js,css等路径，在html文件里直接用src=/static/xxx.js
```





#### 启动

`#python manage.py runserver 127.0.0.1:5000`

`runserver`是启动网站的关键字。

访问127.0.0.1:5000/app/ 即可看到hello world.

这样用的是内置的web服务器，一般用于测试。



### 模型类

django使用自带的ORM（关系对象映射，Object Relational Mapping）

在settings.py设置app中的模型，告诉django需要用其中的模型。

settings.py:

```
INSTALLED_APPS = [
    'app.apps.AppConfig',   #新添，diangosite/app/apps.py中自动生成的AppConfig类。
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

定义一个数据模型：

djangosite/app/models.py:

```python
# -*- coding: utf-8 -*-    #最好在有中文的代码中加上这句话，声明文件用utf-8编码
from django.db import models

KIND_CHOICES=(
    ('python','python1'),
    ('数据库','数据库1'),
    ('前端','前端1'),
)

class Moment(models.Model):
    content=models.CharField(max_length=200)
    user_name=models.CharField(max_length=20,default='匿名')
    kind=models.CharField(max_length=20,choices=KIND_CHOICES,default=KIND_CHOICES[0])
```

模型中的每个字段都是Field子类的某个实例。

#### 字段

几个常用的预定义字段：

* AutoField： 自增整型字段，添加记录时会自动增长。注：这个字段在自己手动建立第三张关系表时要指定。
* BigIntegerField: 64位整型。
* BinaryField: 布尔字段，对应HTML标签是`<input type="checkbox">`
* CharField: 字符串字段（`<input type="text">`）
* TextField: 大容量文本字段（`<textarea>`）
* IntegerField
* FileField:用于保存上传文件的服务器文件系统路径。
* DateTimeField:



每个字段有一些特有的参数，详见模型字段参考例如，`CharField`（和它的派生类）需要`max_length`参数来指定`VARCHAR` 数据库字段的大小。

但有些通用的：

* null 如果为`True`，Django 将用`NULL` 来在数据库中存储空值。 默认值是 `False`.

* blank 如果为`True`，该字段允许为空值默认为`False`。要注意，这与 `null`不同。`null`纯粹是数据库范畴,指数据库中字段内容是否允许为空，而 `blank` 是表单数据输入验证范畴的。如果一个字段的`blank=True`，表单的验证将允许该字段是空值。如果字段的`blank=False`，该字段就是必填的。

* choices 由二项元组构成的一个可迭代对象（例如，列表或元组），用来给字段提供选择项。 如果设置了choices ，默认的表单将是一个选择框而不是标准的文本框，而且这个选择框的选项就是choices 中的选项。

  这是一个关于 choices 列表的例子：

  ```
  YEAR_IN_SCHOOL_CHOICES = (
      ('FR', 'Freshman'),
      ('SO', 'Sophomore'),
      ('JR', 'Junior'),
      ('SR', 'Senior'),
      ('GR', 'Graduate'),
  )
  ```

  每个元组中的**第一个元素**，是存储在数据库中的值；第二个元素是在管理界面或 ModelChoiceField 中用作显示的内容。 在一个给定的 model 类的实例中，想得到某个 choices 字段的显示值，就调用 `get_FOO_display` 方法(这里的 FOO 就是 choices 字段的名称 )。例如：

  ```python
  from django.db import models

  class Person(models.Model):
      SHIRT_SIZES = (
          ('S', 'Small'),
          ('M', 'Medium'),
          ('L', 'Large'),
      )
      name = models.CharField(max_length=60)
      shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

  >>> p = Person(name="Fred Flintstone", shirt_size="L")
  >>> p.save()
  >>> p.shirt_size
  'L'
  >>> p.get_shirt_size_display()
  'Large'
  ```

* primary_key

  如果为true,则为模型的主键。主键是只读的，如果你要是改变主键，django会创建出一个新的，原有的还在。整个模型只能有一个字段指定为主键。

  如果没有指定任何一个字段的主键，django会自动添加一个intergerfield字段作为主键。

  默认情况下，Django 会给每个模型添加下面这个字段：

  ```
  id = models.AutoField(primary_key=True)

  ```

  这是一个自增主键字段。

  如果你想指定一个自定义主键字段，只要在某个字段上指定 `primary_key=True` 即可。如果 Django 看到你显式地设置了`Field.primary_key`，就不会自动添加 `id` 列。

* unique

  如果该值设置为 `True`, 这个数据字段在整张表中必须是唯一的

* 无名参数

  `level=models.CharField("请评级",max_length=1,choices=LEVELS)`  这里我们为level字段定义了人性化名称，如果不定义，字段的本身名称被显示在HTML页面中作为输入提示。



#### Model元数据meta

```python
class Foo(models.Model):
	bar=models.CharField(max_length=30)
	
	class Meta:
		....
```

这个meta子类，是model的元数据，比如表名 。它不是必须选的。有下面几个meta选项：

* app_label 不在应用的models.py文件中。这时候你需要指定整个模型是属于那个应用的，如:`app_label='myapp'`
* db_table 自定义数据库表名：`app_label="myapp"`，默认是 app名_数据类名。强烈推荐小写表名
* `default_related_name`  默认被用于一个关联对象到当前对象的关系，默认为：`<model_name>_set` 
* default_permissions: 默认操作权限，默认为default_permissions=('add','change','delete')
* ordering: 记录的默认排序字段，默认降序，升序需要加负号 `ordering=['user_name','pub_date']`
* 更多稍后看官方网站



#### 导入导出数据

```
python manage.py dumpdata appname > appname.json
python manage.py loaddata appname.json
```



#### 生成数据移植文件

将model.py中的定义的数据模型转换生成脚本的过程。

命令`makemigrations`

`#python manage.py makemigrations app`

这个app就是你项目的名字，也就是setting里导入的项目名字，如果你打错了，会提示你在setting里没有找到。

会提示有0001__initial.py生成，是数据库生成的中间文件，

执行上述命令时，会对比model.py中的模型与已有数据库之间的差异，如果没有差异则不做任何工作。

如果更改，会生成新的中间文件0002省略。。:

```python
class Migration(migrations.Migration):

    # 指定前置版本
    dependencies = [
        ('app', '0001_initial'),
    ]
	#指定对数据库做的更改
    operations = [
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('user_name', models.CharField(default='匿名', max_length=20)),
                ('kind', models.CharField(choices=[('python', 'python1'), ('数据库', '数据库1'), ('前端', '前端1')], default=('python', 'python1'), max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Coment',
        ),
    ]

```



上面只是做了配置记录，而当你要真正使这些修改生效时，你需要运行：

`#python manage.py migrate`

这时，会有一张表的名字：应用名_数据模型名:`app_moment`



迁移到指定版本,如到001_xxx_.py：

`python manage.py migrate app_name 001`



#### 重置

清空数据库，把数据全部清理掉：

`python manage.py flush`

删除原有数据库，重置migration

1.删除数据库所有的表

2.删除项目中的migration模块中的所有文件，除了init.py文件

3.执行脚本：

```
python manage.py makemigrations
python manage.py migrate
```



#### 删除一张表后，重新建立

`python manage.py sqlmigrate myapp 0001 | python manage.py dbshell`  数据库删除表后可用用来重建。

此条件是我在`python manage.py makemigrations myapp` 后，migrate 和 makemigrations 后都不起作用后生效的。



#### 将多个迁移文件变为一个

http://blog.csdn.net/zhuoxiuwu/article/details/52167599



####  添加新的字段

```
python manage.py makemigrations
python manage.py migrate
```



#### 管理器

管理器是Django模型进行数据库查询操作的接口。默认为每个模型添加一个名为objects的管理器。



#### 基本查询

django有两种过滤器用于筛选记录：

* filter(**kwargs): 返回符合筛选条件的数据集
* exclude(** kwargs): 返回不符合筛选条件的数据集。

eg: 

```
Conmment.objects.filter(pub_date__year=2015).exclude(pub_date__month=1).exclude(n_visits__exact=0)
```

查询所有2015年非1月的n_visits不为0的记录。

django独特的字段查询方式：`字段名称__谓词`

用双下划线连接的字段名称和谓词。类似的其他谓词：

* exact  精确等于

* iexact 大小写不敏感的等于 `Comment.objects.filter(headliine__iexact='like')`

* contains 模糊匹配。

* in   包含`Comment.objects.filter(id__in=[1,4,6])`

* gt 大于，gte大于等于，lt 小于，ite小于等于 `Comment.objects.filter(n_visits__gt=30)`

* startswith,以。。开头，endswith 以。。结尾。

* range 在。。范围内， 

  ```
  start_date=datetime.date(2015,1,1)
  end_date=datetime.date(2015,2,1)
  Comment.objects.filter(pub_date__range=(start_date,end_date))
  ```

* year,month,day,week_day 

* isnull 是否为空，`Comment.objects.filter(pub_date__isnull=True)`



#### 关系模型

##### 一对多，一对一

一对一：

在模型中定义OneToOneField 字段，并定义相互之间的一对一关系。

```python
class Account(models.Model):
	user_name=models.CharField(max_length=80)

class Contact(models.Model):
	account=models.OneToOneField(
		Account,
		on_delete=models.CASCADE,
		primary_key=True,
		)
	adress=models.CharField(max_length=10)
```

l两个模型的关系通过Contact中的account字段进行定义。

OneToOneField()的第一个参数定于被关联的模型名。

on_delete参数说明，当Account的记录被删除时本模型的记录如何处理，CASCADE说明本模型的记录也被清除。



一对多：

  `models.ForeignKey(类名,[to_field=True][,..])  `

主键默认关联到对方的主键字段，可以通过主键的 to_field设置关联到的字段。

```python
class Author(models.Model):
	name=models.CharField(max_length=100)
	
class Book(models.Model):
      title =models.CharField(max_length=100)
      
      author =models.ForeignKey("Author")
```

```
book= Book.objects.get(title="Django")
author = Book.author         #获取该图书的作者
books= author.book_set.all() # 获取该作者的所有图书
```

**注意**：`xxxx_set`是Django设定的通过主模型对象访问副模型对象的属性名。可通过related_name

添加书的时候，链接作者主键：

```python
author1 = Author().objects.get(name = 'wang')
book = Book(title = "aaa",author=author1)
```



##### 多对多

`models.ManyToManyFeild(类名,[to_field=True][,..])   `

ORM自动创建第三张表:

```python
class Author(models.Model):
	name=models.CharField(max_length=100)
    
class Book(models.Model):
         title =models.CharField(max_length=100)
        
         authors =models.ManyToManyField(Author)
```

```
book= Book.objects.get(title="Django")
authors = Book.author_set.all()  # 获取该书的作者名单
books= author[2].book_set.all() # 获取第三作者所著的所有图书
```

在哪个模型中设置 `ManyToManyField`] 并不重要，在两个模型中任选一个即可 —— 不要两个模型都设置。

手动创建第三张表，通过through参数 关联（这样可以在第三张表中自定义我们需要的字段）:

```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

与普通多对多字段不同，不能使用add,create和赋值语句。这是因为你不能只创建 `Person`和 `Group`之间的关联关系，你还要指定 `Membership`模型中所需要的所有信息；而简单的`add`、`create` 和赋值语句是做不到这一点的。

remove方法也被禁用，但是clear方法可以用，它可以清空某个实例所用的多对多关系。

```python
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
[<Person: Ringo Starr>]
>>> ringo.group_set.all()
[<Group: The Beatles>]
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
[<Person: Ringo Starr>, <Person: Paul McCartney>]
```

通过创建中介模型的实例来建立对多对多关系后，你就可以执行查询了。

Django会自动在其关联的模型上建立”[model]_set"的属性

 和普通的多对多字段一样，你可以直接使用被关联模型的属性进行查询：

```python
Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
[<Group: The Beatles>]
```

注意members 是Group中的字段，name是Person中的字段。

你也可以利用中介模型的属性进行查询：

```python
Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
[<Person: Ringo Starr]
```

获取中间模型的信息(两种方式)：

```python
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

```python
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```





#### 对模型的api操作

进入交互：`$ python manage.py shell`

数据库接口（QuerySet Api）

从数据库查询出来的结果一般是一个集合，这个集合叫做QuerySet.它是可迭代的:

```python
es=Entry.objects.all()
for e in es:
	print(e.hedalin)
```



##### 增：

```
#方法一：
>>> from people.models import Person
>>> Person.objects.create(name="wangdachui", age=24)
<Person: Person object>
#方法二：
>>> p=Person(name='wdc') 或 p=Person(name='wdc',age=23)
>>> p.age=23
>>> p.save()
#方法三
>>> Person.objects.get_or_create(name='wdc',age=23)

这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.返回值(object, True/False)

#一对多或多对多的增，先把相关对象查询出来。
>>> from blog.models import Entry
>>> entry=Entry.objects.get(pk=1)
>>> chese_blog=Blog.objects.get(name="Cheddar Talk")
>>> entry.blog=cheese_bolg
>>> entry.save()
```

批量增：

```python
a = User(name = 'haha')  # 数据模型
l = []
for x in range(10):
	l.append(a)
User.objects.bulk_create(l)
```





##### 查：

```
#方法一，获取一个对象
>>> Person.objects.get(name="wangdachui")
<Person: Person object>
如果没有相关匹配和多于一个匹配都会报异常
#方法二
>>> Person.objects.all()
#方法三
>>> Person.objects.all()[:10] 
切片操作，获取10个人，不支持负索引，切片可以节约内存
 
===========获取条件============
get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
如果没有则为 []

Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人

Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件
Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人
Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写

Person.objects.filter(name__regex="^abc") # 正则表达式查询
Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写


filter是找出满足条件的，当然也有排除符合某条件的
Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象
Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的

========排序=======
Author.objects.all().order_by('name')
Author.objects.all().order_by('-name') # 在 column name 前加一个负号，可以实现倒序

=======链式查询=====
Author.objects.filter(name__contains="WeizhongTu").filter(email="tuweizhong@163.com")
Author.objects.filter(name__contains="Wei").exclude(email="tuweizhong@163.com")
 
# 找出名称含有abc, 但是排除年龄是23岁的
Person.objects.filter(name__contains="abc").exclude(age=23)

========负索引=====
Person.objects.all()[:10] 切片操作，前10条
Person.objects.all()[-10:] 会报错！！！
 
# 1. 使用 reverse() 解决
Person.objects.all().reverse()[:2] # 最后两条
Person.objects.all().reverse()[0] # 最后一条
 
# 2. 使用 order_by，在栏目名（column name）前加一个负号
Author.objects.order_by('-id')[:20] # id最大的20条

========去重========
当多张表合并时会出现相关问题。
qs1 = Pathway.objects.filter(label__name='x')
qs2 = Pathway.objects.filter(reaction__name='A + B >> C')
qs3 = Pathway.objects.filter(inputer__name='WeizhongTu')
 
# 合并到一起
qs = qs1 | qs2 | qs3
这个时候就有可能出现重复的
 
# 去重方法
qs = qs.distinct()
```

values_list 获取元祖形式结果：

```
获取作者的name和qq:
>>>authors = Author.objects.values_list('name', 'qq')
>>>authors
>>><QuerySet [(u'twz915', u'915792575'), (u'wangdachui', u'353506297'), (u'xiaoming', u'004466315')]>

>>>list(authors)
>>> [(u'twz915', u'915792575'), (u'wangdachui', u'353506297'), (u'xiaoming', u'004466315')]

====获取一个字段=======
>>>Author.objects.values_list('name', flat=True)
>>><QuerySet [u'zhaotiezhu', u'twz915', u'wangdachui', u'xiaoming']>
查询twz915这个人的文章标题
Article.objects.filter(author__name='twz915').values_list('title', flat=True)
```

values 获取字典形式的结果

```
获取作者的 name 和 qq
>>>Author.objects.values('name', 'qq')
>>><QuerySet [{'qq': u'336643078', 'name': u'WeizhongTu'}, {'qq': u'915792575', 'name': u'twz915'}, {'qq': u'353506297', 'name': u'wangdachui'}, {'qq': u'004466315', 'name': u'xiaoming'}]

>>> list(Author.objects.values('name', 'qq'))
>>>[{'name': u'WeizhongTu', 'qq': u'336643078'},
 {'name': u'twz915', 'qq': u'915792575'},
 {'name': u'wangdachui', 'qq': u'353506297'},
 {'name': u'xiaoming', 'qq': u'004466315'}]
 
 查询twz915这个人的文章标题
 >>>Article.objects.filter(author__name='twz915').values('title')
 >>><QuerySet [{'title': u'HTML \u6559\u7a0b_1'}, {'title': u'HTML \u6559\u7a0b_2'}, {'title': u'HTML \u6559\u7a0b_3'}>

```

1. values_list 和 values 返回的并不是真正的 列表 或 字典，也是 queryset，他们也是 lazy evaluation 的（惰性评估，通俗地说，就是用的时候才真正的去数据库查）
2. 如果查询后没有使用，在数据库更新后再使用，你发现得到在是新内容！！！如果想要旧内容保持着，数据库更新后不要变，可以 list 一下
3. 如果只是遍历这些结果，没有必要 list 它们转成列表（浪费内存，数据量大的时候要更谨慎！！！）



查没有显示具体的名字。

为模型添加特殊方法显示：

```python
from django.db import models
 
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
     
    def __unicode__(self):
    # 在Python3中使用 def __str__(self)
        return self.name
```

此时：

```
>>>Person.objects.get(name="wangdachui")
<Persion:wangdachui>
```

补充：https://www.douban.com/note/301166150/



###### 用select_related和prefetch_related优化关系查询

用prefetch_related适合通过“多”查询'一'，以及‘一’查‘一’

作者和文章是一对多的关系，我们现在通过文章查作者：

```
articles = Article.objects.all()[:10]
a1 = articles[0]  # 取第一篇
a1.title#取文章标题
a1.author.name   # 再次查询了数据库，注意！！！
能不能只查询一次，把作者的信息也查出来呢？
articles = Article.objects.all().select_related('author')[:10]
articles[0].author.name # 这时没有查询
```



prefetch_related 适合一对多，多对多的情况。

查询文章同时，查询文章的标签。文章和标签是多对多的关系。

```python
articles = Article.objects.all().prefetch_related('tags')[:3]
for a in articles:
	  print a.title, a.tags.all()
out:
Django 教程_1 <QuerySet [<Tag: Django>]>
Django 教程_2 <QuerySet [<Tag: Django>]>
Django 教程_3 <QuerySet [<Tag: Django>]>
```



###### defer和only

defer排除不需要的字段：

查询文章列表时，只要标题和作者，不必将内容也找出来：


`Article.objects.all().defer('content')`

only仅选择需要的字段，和defer相反。

假如我们只要查询作者的名字：

`Author.objects.all().only('name')`



##### 语句集合 

`from django.db.models import Q`

filter(Q(字段一=‘’))



###### 其他:

1. 如果只是检查 Entry 中是否有对象，应该用 

   `Entry.objects.all().exists()`

2. 用len(es) 可以得到Entry的数量，但是推荐用 `Entry.objects.count()`来查询数量，后者用的是SQL：SELECT COUNT(*)

3. 看queryset执行的SQL

   **print **str(Author.objects.all().query) 可以打印出来。

4. 别名extra,用的少，用的时候可看教程http://www.ziqiangxuetang.com/django/django-queryset-advance.html

5. annotate聚合计数，求和，平均数，可看教程。

   ​

##### 改

` models.Tb1.objects.filter(name='seven').update(gender='0')`  

 将指定条件的数据更新，均支持 **kwargs

修改单条数据:

    # obj = models.Tb1.objects.get(id=1)
    # obj.c1 = '111'
    # obj.save()                                                 
##### 删

删除单个：

`models.Tb1.objects.filter(name='seven').delete() `

删除数据集：

`Comment.objects.filter(pub_date__year=2014).delete()`

删除指定条件的数据，没有任何返回值



#### 性能优化

filter 查的时候，为惰性查询，用到时才启动查询，

`a = Task.objects.filter(***)` 

这样是没有启动查询的，

a[0] 这样才启动了查询。