Tags:[flask,python]  date: 2017-01-30

### 使用FlaskScipt
`pip install flask-script`

使用它可以创建命令，在程序上下文中执行，这样能对Flask对象进行修改。

flask-script 是 Flask 的一个扩展，它能够创建指令，并且让这些指令在 Flask 的应用上下文中执行，可以达到修改 Flask 对象的目的。 
除此之外，flask-script 还能够启动 Flask 开发环境服务器，和开启包含有应用上下文的 [Python](http://lib.csdn.net/base/python) 指令行。



#### config.py文件

这个文件是应用程序的配置文件：

```python
class Config(object):
    """Base config class."""
    pass

class ProdConfig(Config):
    """Production config class.生产环境"""
    pass

class DevConfig(Config):
    """Development config class.开发环境"""
    # Open the DEBUG
    DEBUG = True
```

DEBUG为Ture进入调试模式，可以在代码修改后重新载入，不能用于生产环境，werkzeug默认启用pin码的身份验证，让调试环境下的攻击者更难利用调试器 

`Debugger pin code:146-867-947`

#### manage.py文件

```python
# import Flask Script object
from flask_script import Manager, Server
import main

# Init manager object via app object
manager = Manager(main.app)

# Create a new commands: server
# This command will be run the Flask development_env server
#可以运行命令：python manage.py server 来运行整个项目
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=main.app)

if __name__ == '__main__':
    manager.run()
```

CLI是Command Line Interface的缩写，即命令行界面

#### main.py文件

```python
from flask import Flask

from config import DevConfig

app = Flask(__name__)

# Get the config from object of DecConfig
app.config.from_object(DevConfig)

if __name__ == '__main__':
    app.run()
```

app.config字典可以用来存储框架，扩展和程序本身的配置变量。这个对象还提供了一些方法，可以从文件或者环境中导入变量值。

通过manage.py运行命令行十分必要，因为一些Flask扩展只有在Flask应用对象被创建后才会被初始化。

### 程序和请求上下文
| 变量名         | 上下文   | 说明                          |
| ----------- | ----- | --------------------------- |
| current_app | 程序上下文 | 当前激活程序的程序实例                 |
| g           | 程序上下文 | 处理请求时用作临时存储的对象，每次请求都会重设这个变量 |
| request     | 请求上下文 | 请求对象，封装了客户端发出的HTTP请求中的内容    |
| session     | 请求上下文 | 用户会话，用于存储请求之间需要“记住”的值的词典    |



### SQLAlchemy

 `pip install flask-sqlachemy`


* 基于数据库抽象出数据模型，我们需要用SQLAlchemy的python包。
* 它在最底层包装了数据库操作接口，在最上层提供了对象关系映射（ORM）。
* ORM是在不同数据结构和系统类型的数据源之间传递和转换数据的技术。
* 这里，把他用来将数据传成Python对象的集合。
* 同时，python这样的语言，允许在不同的对象间建立引用，读取和设置他们的属性。
* 为了将SQLAlchemy绑定到我们的程序上下文中，我们用Flask SQLAlchemy，它在SQLAlchemy上提供了一层包装，这样就可以结合Flask的一些特性来方便的调用SQLAlchemy的功能。

需要一些特定的包，来作为SQLAlchemy与你选择的数据库之间的连接器。
```
#MySql
$ pip install PyMySql
#Oracle
$ pip install cx_Oracle
#sqlite不用
```
#### 创建uri来链接数据库
uri类似url，包含了SQLAlchemy创建连接所有信息。一般形式：
SQLALCHEMY_DATABASE_URI=`datebasetype+driver://user:passeword@ip:port/db_name(数据库名）`
如:config.py
```
#mysql
mysql+pymysql://root:123456@127.0.0.1:3306/datatest?charset=utf8
#sqlite
SQLite : sqlite:////absolute/path/to/database
#Oracle
oracle+cx_oracle://user:password@ip:port/db_name
```
补：sqlite是无需运行服务的sql数据库，所有数据都包含在一个文件中，而且支持python。
SQLite数据库不需要使用服务器，因此不用指定hostname、username和password。URL中的database是硬盘上文件的文件名。

#### 创建数据模型

models.py

```python
from flask_sqlalchemy import SQLAlchemy
from main import app
db = SQLAlchemy(app)     #SQLAlchemy 会从app的配置中读取信息，自动链接到数据库。

class User(db.Model):
     __tablename__= "users" #指定表名
    id=db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    # password1 = db.Column(db.String(255),nullable=True,unique=True,index=1,default="dj")   
    #是否唯一(unique)，是否加索引(index),还有其他的比如：是否可以为空（nullable=True）,默认值（default）

    def __init__(self,username):
        self.username=username

    def __repr__(self):
        return "<User '{}'".format(self.username)
```

继承db.Model，这样我们得到了一个有三个字段的表，这个User类的属性值是db.Colum类的实力，每个属性都代表了这个数据库里的一个字段。

在db.Colum的构造函数里，第一个参数是可选的，对应的是实际数据库中的字段名，没有指定，默认为属性名。
如指定：`username = db.Colum('user_name',db.String(255))`

第二个参数告诉SQLALchemy把什么类型的python类型来处理：

* db.String和db.Text会接受python的字符串，转化为varchar和text类型的字段。
* db.Boolean接收python的True或False值，数据库支持则转，不支持转0，1.
* db.Date,db.DateTime,db.Time使用了python中datetime原生包中的同名类。
* db.Integer和Float会接受python中的任意数值类型。括号参数说明限制该字段的储存长度。

primary_key告诉SQLAlchem这个字段做主键索引，每个模型类必须有个一个主键才能正常工作。
设置表名，默认是该类的小写作为表名，在该类下添加：
`__tablename__='table_name'`
可以更改，或将已经存在的名。

- **__init__()**: 其实我们可以省略定义 class User 的构造器. 这样的话 SQLAlchemy 会自动帮我们创建构造器, 并且所有定义的字段名将会成为此构造器的关键字参数名. **EXAMPLE**:

```
def __init__(self, id, username, password):11
```

- **__repr__()**: 该方法返回一个对象的 *字符串表达式*. 与 **__str__()** 不同, 前者返回的是字符串表达式, 能被 eval() 处理；后者返回的是字符串, 不能被 eval() 处理得到原来的对象, 但与 print 语句结合使用时, 会被默认调用. 与 repr() 类似, 将对象转化为便于供 Python 解释器读取的形式, 返回一个可以用来表示对象的可打印字符串.

```
In [15]:user = User('JMilkfan')

In [16]:user
<Model User `JMilkfan`>    
# 直接调用对象实际上是隐式的调用了 User.__repr__(user) 
# __repr__() 其定义了类实例化对象的可打印字符串表达式
```



#### 在数据库中根据模型创建表
在manager.py文件：
```python
from flask_script import Manager,Server
from main import app
from models import db,User

manager = Manager(app)
manager.add_command("server",Server()) #可以运行命令：python manage.py server 来运行整个项目

@manager.shell
def make_shell_context():  #这个函数会创建python命令行在上下文中执行。
    return dict(app=app,
    			db=db,
    			User=User)    # 返回的字典会告诉FLaskScript在打开命令行时进行一些默认的导入工作,每定义一个数据模型，都要进行导入

if __name__ == "__main__":
    manager.run()
```
在控制台创建表：
`python manager,py shell`
`db.create_all()`

#### SQLAlchemy的CRUD

在 manager shell 中完成:

* create增添数据

**add**: 把数据添加到会话对象中 (数据状态为待保存)

**commit**: 将会话对象中的数据提交 (数据被写入数据库中)

```
>>> from uuid import uuid4
>>> user = User(id=str(uuid4()), username='jmilkfan', password='fanguiju')
>>> db.session.add(user)
>>> db.session.commit()
```



* retrieve 读取数据

通过 **Model.query** 方法对数据进行查询. `Model.query == db.session.query(Model)` 两种写法是等效的. 区别在于前者使用的是 **flask_sqlalchemy.BaseQuery object**, 后者使用的是 **sqlalchemy.orm.query.Query object** . 但两者本质上都是一个 **Query** 对象.

**读取数据有两种情况:**

获取一条记录：

```python
>>> user = User.query.first()
>>> user.username
u'fanguiju'
# 返回表中的第一条记录
# 其中 User.query 返回的是 flask_sqlalchemy.BaseQuery object
# flask_sqlalchemy.BaseQuery object 拥有对数据库操作的所有抽像方法

# or

>>> user = User.query.get('49f86ede-f1e5-410e-b564-27a97e12560c')
>>> user
<Model User `claymore`>
# 返回表中指定主键的一条记录

# or

>>> user = db.session.query(User).filter_by(id='49f86ede-f1e5-410e-b564-27a97e12560c').first()
>>> user
<Model User `claymore`>
# 返回符合过滤条件的第一条记录
# 其中 db.session.query(User).filter_by(id='49f86ede-f1e5-410e-b564-27a97e12560c') 返回的是一个 sqlalchemy.orm.query.Query object 对象
# sqlalchemy.orm.query.Query.first() 才是一个 User 对象
```

Query的过滤器

在查询数据时, 可以根据一定的条件集合来获得过滤后的数据. SQLAlchemy 提供了过滤器 `query.filter_by()` 和 `query.filter()`, 过滤器接受的参数就是过滤条件, 有下面几种形式:

- 字段键值对, EG. `username='fanguiju'`
- 比较表达式, EG. `User.id > 100`
- 逻辑函数, EG. `in_/not_/or_`

```python
>>> user = db.session.query(User).filter(User.username.in_(['fanguiju', 'jmilkfan'])).limit(1).all()   # 当然也可以结合链式函数来使用
>>> user
[<Model User `cc`>]

>>> user = db.session.query(User).filter(not_(User.password == None)).all()
>>> user
[<Model User `cc`>, <Model User `aa`>]

>>> user = db.session.query(User).filter(or_(not_(User.username == None), User.password != None)).all()
>>> user
[<Model User `cc`>, <Model User `aa`>]
```

可以将 `query.filter()` 内置的逻辑函数 `in_/not_/or_` 结合使用来实现更复杂的过滤.

两个过滤器的区别：

实质区别在于filter_by只能使用等号（不是==），应该更快，可以走索引 
filter可以使用>，<取一定范围信息。用==。



获取多条记录：

```python
# 获取多条记录
>>> user = db.session.query(User).filter_by(username='cc').all()
>>> user
[<Model User `cc`>]
# 返回符合过滤条件的所有记录, 将所有 username == fanguiju 的记录都获取

# 获取全部数据
>>> users = User.query.all()
>>> users
[<Model User `cc`>, <Model User `aa`>]
# or
>>> db.session.query(User).all()
[<Model User `cc`>, <Model User `aa`>]

# 获取数量限制数据，这个返回特征常与数据的分页功能结合使用.
>>> users = db.session.query(User).limit(10).all()

# 排序返回的记录
# 正向排序
>>> users = db.session.query(User).order_by(User.username).all()
>>> users
[<Model User `fanguiju`>, <Model User `jmilkfan`>]

# 反向排序
>>> users = db.session.query(User).order_by(User.username.desc()).all()
>>> users
[<Model User `jmilkfan`>, <Model User `fanguiju`>]

# 链式调用，一条读取语句的链式操作都是一个 first() 或 all() 函数结束的. 它们会终止链式调用并返回结果.
>>> users = db.session.query(User).order_by(User.username).limit(10).all()
```

分页函数：

**pagination()**: 是专门设计来实现分页功能的函数, 所以必须由 **flask_sqlalchemy.BaseQuery object** 来调用

```python
>>> User.query.paginate(1,10，False)     # 查询第 1 页,且 1 页显示 10 条内容,false如果没有则返回[],不提示错误
<flask_sqlalchemy.Pagination object at 0x7f214419fe50>

# paginate() 与 first()/all() 不同, 后者返回的是一个 models 对象或 models 对象列表, 而前者返回的是一个 pagination 对象. 而且 pagination 对象还包含了几个特有的属性:
>>> user_page = User.query.paginate(1, 10)

# 获取这一页所包含的数据对象
>>> user_page.items
[<Model User `fanguiju`>, <Model User `jmilkfan`>]

# 获取这一页的页码
>>> user_page.page
1

# 获取总共的页数
>>> user_page.pages
1

# 是否有上一页
>>> user_page.has_prev
False

# 如果有上一页的话, 获取上一页的 pagination 对象
>>> if user_page.has_prev:
...     user_page.prev()
... 

# 是否有下一页
>>> user_page.has_next
False

# 如果有下一页的话, 获取下一个的 pagination 对象
>>> if user_page.has_next:
...     user_page.next()
... 
```

分页模板：

```jinja2
  {#定义宏，pagination是查询后的pagination对象,endpoint是试图函数的名字，我传入了 蓝图名.试图名#}
 {% macro render_pagination(pagination,endpoint) %}  
        <nav aria-label="Page navigation">  //用了BootStrap模板
            <ul class="pagination">		
                <li>						//向前按钮
                    {% if pagination.has_prev %} //如果有前一个pagination对象
                        <a href="{{ url_for(endpoint,page=pagination.prev().page) }}" //为试图连接加上上一页的链接
                           aria-label="Previous">
                    {% else %}
                        <a href="{{ url_for(endpoint,page=1) }}"//如果没有则是第一页
                            aria-label="Previous">
                    {% endif %}
                        <span aria-hidden="true">&laquo;</span>  //‘<<’的编码
                        </a>
                </li>
			{#iter_pages()返回pagination的所有页数的迭代器#}
                {% for page in pagination.iter_pages() %}       
                    {% if page %}   {#如果页数不为零#}
                        {% if page!=pagination.page %} {#页数不是当前页#}
                            <li>
                                <a href="{{ url_for(endpoint, page=page) }}"> {#加上这个页的链接#}
                                    {{ page }}
                                </a>
                            </li>
                        {% else %}
                            <li><a href="">{{ page }}</a></li>{#当前页，就没有链接了，因为已经加载出来了，不需要在为他添加链接#}
                        {% endif %}
                    {% else %}
						<li><a href="">...</a></li>  {#没有任何页面#}
                    {% endif %}
                {% endfor %}
                {#下一页#}
                    <li>
                      {% if pagination.has_next %}  {#如果还有下一页#}
                        <a href="{{ url_for(endpoint, page=pagination.next().page ) }}" aria-label="Next">
                    {% else %}
                        <a href="">
                    {% endif %}
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                    <li>
            </ul>
        </nav>
    {% endmacro %}

```



* update 更新数据

```python
>>> user = db.session.query(User).first()
>>> user.username
u'fanguiju'

>>> user = db.session.query(User).update({'username': 'update_fanguiju'})
>>> db.session.commit()

>>> user = db.session.query(User).first()
>>> user.username
u'update_fanguiju'
```

如上述例子, 先定位到你希望更新的记录, 然后通过 Query 对象的 `update()` 传递要更新内容. **注意**: 更新的内容必须是 Dict 数据类型.

**需要注意的是**: 就如使用原生 SQL 指令来更新记录一样, 如果没有指定要更新具体的哪一条记录的话, 会将该字段所在列的所有记录值一同更新, 所以切记使用过滤条件来定位到具体需要更新的记录.

而且 `update()` 会自动的添加 User 的实例化对象到 session 中, 所以直接 commit 就可以写入到数据库了.

具体更新可有两种方法：

```python
 #一、使用update方法
        self.db.session.query(User).filter(User.id == 12).update({User.age:12})
        self.db.session.commit()
 # 二、使用赋值方法
        userInfo = self.db.query(User).get(12)
        if userInfo:
            userInfo.age = 12
            self.db.commit()
```





* delete 删除数据

```
>>> user = db.session.query(User).first()
>>> user
<Model User `update_fanguiju`>

>>> db.session.delete(user)
>>> db.session.commit()
```



#### model间的关系

* one to many 一对多

  一个用户可以有博客，每篇博客之对应一个作者，它们之间的关系为一对多

  ```python
  class User(db.Model):
      
      __tablename__ = 'users'
      id = db.Column(db.String(45), primary_key=True)
      username = db.Column(db.String(255))
      password = db.Column(db.String(255))
      # Establish contact with Post's ForeignKey: user_id
      #会在 SQLAlchemy 中创建一个虚拟的列，该列会与 Post.user_id (db.ForeignKey) 建立联系
      posts = db.relationship(
          'Post',
          backref='users',
          lazy='dynamic')

  class Post(db.Model):

      __tablename__ = 'posts'
      id = db.Column(db.String(45), primary_key=True)
      title = db.Column(db.String(255))
      text = db.Column(db.Text())
      publish_date = db.Column(db.DateTime)
      # Set the foreign key for Post,user_id 字段是 posts 表的外键
      user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
  ```

如果你没有在父表类指定 `__tablename__` 属性，那么这一条语句我们应该这么写：

```
user_id = db.Column(db.String(45), db.ForeignKey('User.id'))
```

但是一般不建议写成这样，因为在 SQLAlchemy 初始化期间， User 对象可能还没有被创建出来，所以同时也建议在定义 models class 的时候应该指定 `__tablename__` 属性。

**注意：表名长时用下划线，eg:`user_others` 不然外键这会报错`**

* db.relationship

会在 SQLAlchemy 中创建一个虚拟的列，该列会与 `Post.user_id` (db.ForeignKey) 建立联系。

第一个参数是关联的数据模型的类。

`backref`:用于指定表之间的双向关系，如果在一对多的关系中建立双向的关系，这样的话在对方看来这就是一个多对一的关系。

`lazy`:指定 SQLAlchemy 加载关联对象的方式。

- `lazy=subquery`: 会在加载 Post 对象后，将与 Post 相关联的对象全部加载，这样就可以减少 Query 的动作，也就是减少了对 DB 的 I/O 操作。但可能会返回大量不被使用的数据，会影响效率。
- `lazy=dynamic`: 只有被使用时，对象才会被加载，并且返回式会进行过滤，*如果现在或将来需要返回的数据量很大，建议使用这种方式*。Post 就属于这种对象。

to use:

```python
>>> from uuid import uuid4
# 实例化一个 User 的对象
>>> user = User(id=str(uuid4()), username='jmilkfan', password='fanguiju')
# 写入一条 users 记录     
>>> db.session.add(user)
>>> db.session.commit()

>>> user.posts
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x22bc410>

# 现在因为还没有添加 posts 的记录所以为空，这个posts是posts=db.relationship中的posts
>>> user.posts.all()
[]

# 实例化一个 Post 的对象
>>> post_one = Post('First Post')
# 主键值是非空的，必须指定一个，否则会报错
>>> post_one.id = str(uuid4())

# =============重点================
# 指定该 post 是属于哪一个 user 的
>>> post_one.user_id = user.id
>>> db.session.add(post_one)
>>> db.session.commit()

>>> user.posts.all()
[<Model Post `First Post`>]

# 获取一个已经存在数据库中的记录 user 
>>> user = db.session.query(User).first()
>>> user.id
u'ad7fd192-89d8-4b53-af96-fceb1f91070f'

# 实例化一个 Post 的对象 post_second
>>> post_second = Post('Second Post')
# 必须为其设置主键值
>>> post_second.id = str(uuid4())
# 现在该 post_second 对象是没有关联到任何 user 的
>>> post_second.users

# =============重点================
# 为 post_second 指定一个 user 对象，users为表名
>>> post_second.users = user

# 将 post_second 写入数据库
>>> db.session.add(post_second)
>>> db.session.commit()
# 写入完成之后，user 才能够通过关系来访问到属于其下的 posts
>>> user.posts.all()
[<Model Post `Second Post`>, <Model Post `First Post`>]
```

* many to many 多对多

一个博客和tag标签之间的关系是多对多：

多对多关系会在两个类之间增加一个关联表。 这个关联的表在 `relationship()` 方法中通过 **secondary** 参数来表示。通常的，这个表会通过 MetaData 对象来与声明基类关联， 所以这个 ForeignKey 指令会使用链接来定位到远程的表：

```python
posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))

class Post(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
  
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,#会告知 SQLAlchemy 该 many to many 的关联保存在 posts_tags 表中
        backref=db.backref('posts', lazy='dynamic'))

class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
```

**backref**：声明表之间的关系是双向，帮助手册 `help(db.backref)`。需要注意的是：在 one to many 中的 backref 是一个普通的对象，而在 many to many 中的 backref 是一个 List 对象。

实际上 db.Table 对象对[数据库](http://lib.csdn.net/base/mysql)的操作比 db.Model 更底层一些。后者是基于前者来提供的一种对象化包装，表示数据库中的一条记录。 **posts_tags** 表对象之所以使用 db.Table 不使用 db.Model 来定义，是因为我们不需要对 **posts_tags** (self.name)进行直接的操作(不需要对象化)，**posts_tags** 代表了两张表之间的关联，会由数据库自身来进行处理。

to use:

```python
>>> db.create_all()
>>> posts = db.session.query(Post).all()
>>> posts
[<Model Post `Second Post`>, <Model Post `First Post`>]
>>> post_one = posts[1]
>>> post_two = posts[0]

# 实例化 3 个 Tag 的对象
>>> from uuid import uuid4
>>> tag_one = Tag('JmilkFan')
>>> tag_one.id = str(uuid4())
>>> tag_two = Tag('FanGuiju')
>>> tag_two.id = str(uuid4())
>>> tag_three = Tag('Flask')
>>> tag_three.id = str(uuid4())

# 将 Tag 的实例化对象赋值给 Post 实例化对象的 tags 属性
# 即指定 Tag 和 Post 之间的关联状态
# post_one 对应一个 tag
# post_two 对应三个 tags
# tag_one/tag_three 对应一个 post
# tag_two 对象两个 posts
>>> post_one.tags
[]
#==============重点=================
>>> post_one.tags = [tag_two]  #这个tags不是指的表名，而是关系字段
>>> post_two.tags = [tag_one, tag_two, tag_three]

>>> db.session.add(post_one)
>>> db.session.add(post_two)
>>> db.session.commit()

#================重点=========================
#在上面说过了 many to many 的 backref 是一个 List 对象，所以我们还可以反过来为 tags 添加一个 posts 对象(引用)。
>>> tag_one.posts.all()  #这个posts是表名
[<Model Post `Second Post`>]
>>> tag_one.posts.append(post_one)
>>> tag_one.posts.all()
[<Model Post `Second Post`>, <Model Post `First Post`>]
>>> post_one.tags
[<Model Tag `FanGuiju`>, <Model Tag `JmilkFan`>]
# 因为修改了 tag_one 的 posts 属性(添加了 post_one 的引用)，所以需要重新提交 tag_one 才会被写入到数据库。
>>> db.session.add(tag_one)
>>> db.session.commit()
```



#### 数据库迁移

工具Alembic可根据我们的SQLAlchemy模型的变化自动创建数据库迁移记录，保存了我们数据库结构变化的历史信息。

不然通过db.drop_all()和db.create_all()这样的方式会摧毁旧数据。

让我们升级或者降级到某个已保存的版本。这些历史文件本身就是python程序文件。
我们不会直接使用Alembic,而是会使用Flask-Migrate，这是为SQLAlchemy专门创建的一个扩展，并且可以跟Flask Script一起使用。
pip:`pip install Flask-Migrate`
添加到manage.py中：

```python
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand 

from main import app,db,User,Post,Tag
migrate = Migrate(app,db)

manager=Manager(app)
manager.add_command("server",Server())
#Flask-Migrate提供MigrateCommand类来连接Flask-Script的manager对象。
manager.add_command('db',MigrateCommand) 

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Tag=Tag_

if __name__ == "__name__"
    manager.run()
```
通过app对象和SQLAlchemy的实例初始化了Migrate对象，通过命令来调用。
运行下面命令可以看到可用命令列表：
`$python manage.py db`
开始跟踪我们的数据库变更：
`$python manage.py db init`
上面这个命令会在项目目录里面创建一个叫migrations的文件夹，所有的记录文件都会被保存在里面。我们可以进行首次迁移：
`python manage.py db migrate -m"initial migration`
上面这个命令会让Alembic扫描我们所有的SQLAlchemy对象，找到在此之前没有被记录过的所有表和列，-m参数来提交保存信息，通过提交保存信息寻找所需的迁移记录版本是最容易的方法。
每个迁移记录文件都被保存在migrations/version/文件中。

执行下面命令，把迁移记录应用到数据库上，并改变数据库的结构：

每次改变表结构的时候更新就好了。原有数据还不会清除。

`python manage.py db upgrade`
要返回以前的版本通过history命令找到版本号：
`python manage.py db history`
再把版本好给downgrade命令：
`pyhon manage.py db downgrade 7ded34bc4fb`
同git一样，每个迁移记录都由一个哈希值来表示。可以将迁移记录和git提交记录对应起来。

#### 补充

* 回滚`db.session.rollback()`
* 分组查询`db.session.query(User).group_by(User.name).all()`
* 常用的SQLAlchemy 查询执行器：

![](http://ojynuthay.bkt.clouddn.com/sqlalchemy.png) 

* 对于给定的查询还可以检查SQLAlchemy生成的原生SQL查询，并将查询对象转换为一个字符串：

  ` str(User.query.filter_by(role=user_role))`

请看： https://blog.csdn.net/levon2018/article/details/82683906



### WTForm

#### 基础
Flask提供的请求对象能提供用于处理web表单的信息，如request.form能获取post请求中提交的表单数据。WTForm是一个服务端表单检验库，它可对常见的表单类型进行输入合法性验证。
Flask WTForm是基于WTForm的Falsk扩展，增加了一些特性：JinjiaHTML渲染，预防跨域请求伪造（CSRF）和SQL注入攻击。
安装：`pip install Flask-WTF`
为了让WTForm的安全工作能够正常工作，我们需要一个密钥，来生成加密的签名。

这个密钥可以在多个扩展中使用。

在config.py里的Config对象：

```
class Config(object):
    SECRET_KEY='你的密钥'
```
WTForm 由三部分组成：

* 字段：对输入的初步检查
* 检验器：在字段上加的函数，用来确保输入字符的限制条件。
* 表单：一个python类，
  forms.py加入如下内容
```python
from flask_wtf import Form # 最新改为FlaskFrom
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

  class NameForm(FlaskForm):           #使用Flask-WTF时，每个web表单都继承一个From类。
    name = StringField('What is your named',validators=[DataRequired(method="添加内容不能为空")]) #这里自定义错误内容，会在后面的模板文件中显示-errors
    submit = SubmitField('Submit')
```
Form基类由Flask-WTF扩展定义，从flask_wtf中导入。
字段和验证函数可以直接从wtforms包中导入。

字段类的第一个参数为输入框标题,如果是按钮就是按钮名字，第二个参数为绑定到该字段的检验器列表，由 wtforms.validators 提供



#### 支持的html字段
| 字段名称                | 说明                         |
| ------------------- | -------------------------- |
| StringField         | 文本字段                       |
| TextAreaField       | 多行文本字段                     |
| PasswordField       | 密码文本字段                     |
| HiddenField         | 隐藏文本字段                     |
| DateField           | 文本字段，值为datetime.date格式     |
| DateTimeField       | 文本字段，值为datetime,datetime格式 |
| IntegerField        | 文本字段，值为整数                  |
| DecimalField        | 值为decimal.Decimal          |
| FloatField          | 文本字段，值为浮点数                 |
| BooleanField        | 复选框，值为True和False           |
| RadioField          | 一组单选框                      |
| SelectField         | 下拉列表                       |
| SelectMultipleField | 下拉列表，可以选多个值                |
| FileField           | 文件上传字段                     |
| SubmitField         | 表单提交按钮                     |
| FormField           | 把表单作为字段嵌入另一个表单             |
| FieldList           | 一组指定类型的字段                  |

#### 表单验证函数
如上文的参数validators,它定义了该数据的验证器列表，如DataRequired()代表了输入值不能为空。
| 验证函数         | 说明                     |
| ------------ | ---------------------- |
| DataRequired | 字段不能为空                 |
| Emai         | 验证电子邮箱                 |
| EqualTo      | 比较两个字段的值，常用与输入两次密码进行确认 |
| IPAddress    | 验证IPv4的网络地址            |
| Length       | 验证输入字符串的长度             |
| NumberRange  | 验证输入的值在数字范围内           |
| Optional     | 无输入值时跳转其他验证函数          |
| Regexp       | 使用正则表达式验证输入值           |
| URL          | 验证URL                  |
| AnyOf        | 确保输入值在可选值列表中           |
| NoneOf       | 确保输入值不在可选值列表中          |

#### 自定义检验器
定义一个函数，接受表单对象和字段对象为参数，不符合要求抛出一个WTForm.ValidationError：
```
import re 
import wtforms
def custom_email(form,field):
    if not re.match(r"[^@]+@[^@
```
#### 视图函数中处理表单
```python
@app.route('/'.methods=['GET','POST'])
def index():
    name = None    # 局部变量存放表单中输入的有效名字
    form = NameForm() # 这里就是上面定义的表单函数了
    if form.validate_on_submit():
        name = form.name.data  #接受输入框传来的数据
        form.name.data=''      #将数据清空返回输入框
        return render_template('index.html',form=form,name=name)
```
methods参数告诉函数注册为POST和GET的请求提交。
get提交的数据以字符串的形式附加到URL中，大多数以post提交。
validate_on_submit函数，如果数据能被所有验证函数接受，返回True。否则false。

#### 模板接收表单
```jinja2
<form method="post">
<!--Form 类有一个 hidden_tag 方法， 它在一个隐藏的 DIV 标签中渲染任何隐藏的字段，包括 CSRF 字段-->
    {{form.hidden_tag()}}
    {{form.name.label}}{{form.name(id='may-text-field',class="form-control",placeholder="邮箱)}}
    {#显示错误信息，如果不用循环显示，页面上会显示‘{}（）’等符号#}
     {% if formHtml.userEmail.errors %}
                {% for e in formHtml.userEmail.errors %}
                    <p class="help-block" style="color: red">{{ e }}</p>
                {% endfor %}
     {% else %}
                 <br>
     {% endif %}
    
    {{form.submit()}}
</form>
```
这里的form就是我们传过来的那个参数。

label ,是定义表单类中国要显示的名字，form.name是定义的输入框，后面的可以定义控件的样式,'邮箱'是默认显示内容

但是这种方式太过于繁琐，我们更推荐用Flask-Bootstrap

```
{%import "bootstrap/wtf.html" as wtf%}
{{wtf.quick_form(form)}}
```

如果validate_on_submit()没有响应，记得加：

`{{ form.csrf_token }}`

在csrf保护中会讲

#### 重定向和用户会话session

当用户刷新时，浏览器会有提示框，因为刷新页面时浏览器会重新发送之前已经发送过的最后一个请求。
解决方案：不让Web程序把POST请求作为浏览器发送的最后一个请求——重定向。、
并在刷新后记住上次填的内容，用到session。
```
from flask import Flask,render_template,session,url_for,redirect
@app.route('/',methods=['GET','POST'])
def index():
    name = None
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        session['name'] = nameForm.name.data
        nameForm.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html',form=nameForm,name=session.get('name'))

```

* session['name']存储了同一个会话的中文本框中的内容
* redirect（）是个辅助函数，用来生成http重定向响应，参数是重定向的URL
* url_for(),当然redirect(url_for('index'))也可以写成redirect('/'),但是推荐使用url_for()生成URL，因为这个函数使用URL映射生成URL，从而保证URL和定义的路由兼容，而且修改路由名字后依然后依然可用。``url_for()```函数的第一个且唯一必须指定的参数是端点名，即路由的内部名字，默认情况下，路由的端点是**相应视图函数的名字**，在这个示例中，处理跟地址的视图函数是index(),因此传给url_for()函数的名字是index。
* session.get('name')直接从会话中中读出name参数的值，也可以使用session['name']读取，但是推荐使用session.get('name'),使用get()获取字典中键对应的值以避免未找到键的异常情况，因为对于不存在的键，get()会返回默认值None.

#### flush消息
用户提交了一项有错误的登陆表单后，服务器发回的相应重新渲染了登陆表单，并在表单上显示一个消息，提示用户用户名或密码错误。
这是Flask的核心特性，flash函数可以实现这种效果。

```python
from flask import Flask,render_template,session,redirect,url_for,flash
@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name') # 和上次的名字做比较
        if old_name is not None and old_name!=from.name.data:
            flash('你已经改变了名字')
        session['name']=fomr.name.data #存储上这次的名字
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))
```

这个示例中，每次提交的名字会储存在用户会话中的名字进行比较，而会话中存储的名字是前一次在这个表单中提交的数据。如果两个名字不一样，就会调用flash()函数，再发给客户端的下一个相应中显示一个消息。

我们要将flush消息显示出来：

```html
{% block content %}
    
<div class="container">

{% for message in get_flashed_messages() %}
<div class="alert alert-warning">
<button type="button" class="close" data-dismiss="alert">&times;</button>
{{ message }}
</div>
{% endfor %}

  {% block page_content %}{% endblock %}
</div>
{% endblock %}
```

在模板中使用循环是因为在之前的请求循环中每次调用flash()函数都会生成一个消息，所以可能有多个消息在排队，get_flashed_messages()函数获取的消息在下次调用时不会再次返回，只显示一次就消失。



### CSRF保护

CSRF（Cross-site request forgery）跨站请求伪造，也被称为“One Click Attack”或者Session Riding，通常缩写为CSRF或者XSRF，CSRF则通过伪装来自受信任用户的请求来利用受信任的网站。

用flask_wft实现的表单已经免受CSRF的威胁,，尽管如此没有包含表单的试图，仍需要保护。

为了能够让所有的视图函数受到 CSRF 保护，你需要开启 `CsrfProtect` 模块:

```
from flask_wtf.csrf import CsrfProtect

CsrfProtect(app)
```

可惰性加载：

```python
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
```

```jinja2
<form method="post" action="/">
    {{ form.csrf_token }}
</form>
```

但是如果模板中没有表单，你仍然需要一个 CSRF 令牌:

```
<form method="post" action="/">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
</form>

```

无论何时未通过 CSRF 验证，都会返回 400 响应。你可以自定义这个错误响应:

```
@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400
```

CSRF 保护的大部分功能都能工作(除了 `form.validate_on_submit()`,所以我们在用的时候，记得在渲染模板时加上：`{{ form.csrf_token }}`