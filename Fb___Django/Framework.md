### RestFramework

#### 建立一个数据模型

```python
   class Task(models.Model):
       title = models.CharField('标题', max_length=100)
       description = models.TextField('描述')
       completed = models.BooleanField('是否完成', default=False)
       create_date = models.DateTimeField('创建时间',auto_now_add=True)
       
       def __unicode__(self):
           return self.title
```

#### 序列化

##### 写在前面

序列化能把Querysets和数据模型实例这样复杂的数据转换成能够轻易转化成JSON，XML的Python数据类型。

先写个简单的例子：

```python
from datetime import datetime
class Comment(object):
    def __init__(self,email,content,created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment (email='hhh@qq.com',content='i see you')
```

序列化：

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email=serializers.EmailField()
    content = serializers.CharField(max_length=100)
    created = serializers.DateTimeField()
```

序列对象：`s = CommentSerializer(comment)`

输出： 

```
>>> s.data
{'email': 'hhh@qq.com', 'content': 'i see you', 'created': '2017-06-02T10:28:10.118514'}
```

上面我们把数据实例转换成python 的原生数据结构（字典）来输出。

在framwork中，我们要注意几点：

* 序列化输出时如果要输出其他内容，通过context属性：

  ```python
  serializer = AccountSerializer(account, context={'request': request})
  serializer.data
  # {'id': 6, 'owner': u'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
  ```

* 如果传入的模型是多个（集合），要加many = True, eg: `s = CommentSerializer(comments,many=True)`



下面我们将其数据变成json结构：

```
>>> from rest_framework.renderers import JSONRenderer
>>> json=JSONRenderer().render(s.data)
>>> json
b'{"email":"hhh@qq.com","content":"i see you","created":"2017-06-02T10:28:10.118514"}' # 得到一个byte类型
```



##### 保存实例和save()方法：

如果你想返回（这在反序列化中常见）一个复杂的被数据验证过的实例，你需要写create()或update()方法。

create() 方法会在新建中被调用，update()会在数据更新时被调用，这里我们可以自己定义准许更新的数据。

```python
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)  # 这里的字段email等，填的是数据模型中的字段。
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save() #如果你的实例django数据模型，你需要写这句话来保存
        return instance
```

save可创建（会调用上面create方法），也可更新（会调用上方update方法）：

```python
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)

# 也可添加另外的参数
serializer.save(owner = request.user)
```

重写save，让他变的更有意义，比如你有个数据实例（邮箱，信息）成功创建后会发邮件：

```python
class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(from=email, message=message)
```



##### 检验器 Validation

反序列化时需要对数据进行检验，is_valid()看是否通过检验，errors看检验的错误信息。

```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': [u'Enter a valid e-mail address.'], 'created': [u'This field is required.']}
```

有单个字段，和整个类的检验，及自定义提示异常，自定义validators。具体可看官网。





##### framwork中的序列化

类似于Form,提供了Serializer类提供response输出请求，

  我们要把数据模型转换成数json格式，和创建表单类有些相似。有两种方法：

1.创建Serializer类

```python
from rest_framework import serializers
from snippets.models import Task

class TaskSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True,max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES,default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    
    def create(self, validated_data):
          # 如果数据合法就创建并返回一个snippet实例
           return Snippet.objects.create(**validated_data)
     
    def update(self, instance, validated_data):
          # 如果数据合法就更新并返回一个存在的snippet实例
           instance.save()
           instance.title = validated_data.get('title', instance.title)
           instance.code = validated_data.get('code', instance.code
           )
           instance.linenos = validated_data.get('linenos', instance.linenos)
           instance.language = validated_data.get('language', instance.language)
           instance.style = validated_data.get('style', instance.style)
           return instance
```


 2.使用ModelSerializers
   ```python
   from rest_framework import serializers
   from .models import Task

   class TaskSerializer(serializers.ModelSerializer):
       class Meta:
           model = Task
           fields = ('id', 'title', 'description', 'completed', 'create_date') 
        # fields = '__all__'则为所有字段
        # fields相对属性exclude = ('title',) 意为除了title之外都被序列化。
   ```

使用ModelSerializers的好处：

1. 自动基于模型创建set
2. 自动创建校验器
3. 默认包括.create()和update()方法。


可以在manage.py 中导入你的序列化ExampleSerializer , s = ExampleSerializer , print(repr(s)) 可以看到序列化的具体内容信息。



##### 一对多关系的处理

```python
 class User(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=50) #名字
 
     class Meta:
         db_table = 'table_user'
 
  class Email(models.Model):
     id = models.AutoField(primary_key=True)
     email = models.CharField(max_length=100)
 
     user = models.ForeignKey(User,#related_name='emails')  
    
     class Meta:
         db_table = 'table_email' 
```

如代码所示，创建了用户和邮箱这样一种一对多的关系，一个用户可以有很多邮箱。

序列化：

```python
 class EmailSerializer(serializers.ModelSerializer):
     class Meta:
         model = Email
         fields = ('__all__')
 
 class UserSerializer(serializers.ModelSerializer):
     email_set = EmailSerializer(many=True) # emails = ...
    
     class Meta:
         model = User
         fields = '__all__'

```

这样在我们输出UserSerializer.data时，可以这样显示：

```
 "用户": [
        {
            "id": 1,
            "email_set": [
                {
                    "id": 1,
                    "email": "123@163.com",
                    "user": 1
                },
                {
                    "id": 2,
                    "email": "123@qq.com",
                    "user": 1
                },
                {
                    "id": 3,
                    "email": "123@outlook.com",
                    "user": 1
                }
            ],
            "name": "用户一"
```



##### 多对多的处理

多对多的关系也和上面一样的，你要根据有没有manytomany字段所在模型来判断。



##### 序列化关系模型

depth: https://my.oschina.net/felony/blog/847913



根据官方的例子来看一下每一个关系模型的介绍。

数据模型如下：

```python
class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('album', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.title)
```



* #### StringRelatedField

使用 `StringRelatedField` 将返回一个对应关系 model 的 `__unicode__()` 方法的字符串。

这个字段是只读的。

参数：

`many` 如果应用于多对多关系，则应将此参数设置为 `True`

序列化模型如下

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
```

序列化结果如下：

```python
{
    'album_name': 'Things We Lost In The Fire',
    'artist': 'Low',
    'tracks': [
        '1: Sunflower',
        '2: Whitetail',
        '3: Dinosaur Act',
        ...
    ]
}
```

* #### PrimaryKeyRelatedField

使用 `PrimaryKeyRelatedField` 将返回一个对应关系 model 的主键。

参数：

- `queryset` 用于在验证字段输入时模型实例查找。 关系必须明确设置 `queryset`，或设置 `read_only = True`
- `many` 如果是对应多个的关系，就设置为 `True`
- `allow_null` 如果设置为 `True`，则该字段将接受 `None` 的值或为空的关系的空字符串。默认为 `False`
- `pk_field` 设置为一个字段以控制主键值的序列化/反序列化。例如，`pk_field = UUIDField（format ='hex'）` 将UUID主键序列化为紧凑的十六进制表示。

序列化模型如下

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
```

序列化结果如下：

```python
{
    'album_name': 'Undun',
    'artist': 'The Roots',
    'tracks': [
        89,
        90,
        91,
        ...
    ]
}
```

* #### HyperlinkedRelatedField

使用 `HyperlinkedRelatedField` 将返回一个超链接，该链接指向对应关系 model 的详细数据，`view-name` 是必选参数，为对应的视图生成超链接。

参数：

- `view_name` 用作关系目标的视图名称。如果使用的是标准路由器类，那么它的格式为 `<modelname>-detail` 的字符串
- `queryset` 验证字段输入时用于模型实例查询的查询器。关系必须明确设置 `queryset`，或设置 `read_only = True`
- `many` 如果应用于多对多关系，则应将此参数设置为 `True`
- `allow_null` 如果设置为 `True`，则该字段将接受 `None` 的值或为空的关系的空字符串。默认为 `False`
- `lookup_field` 应该用于查找的目标上的字段。应该对应于引用视图上的 `URL` 关键字参数。默认值为 `pk`
- `lookup_url_kwarg` 与查找字段对应的 `URL conf` 中定义的关键字参数的名称。默认使用与 `lookup_field` 相同的值
- `format` 如果使用 `format` 后缀，超链接字段将对目标使用相同的 `format` 后缀，除非使用 `format` 参数进行覆盖。

序列化模型如下

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
```

序列化结果如下：

```python
{
    'album_name': 'Graceland',
    'artist': 'Paul Simon',
    'tracks': [
        'http://www.example.com/api/tracks/45/',
        'http://www.example.com/api/tracks/46/',
        'http://www.example.com/api/tracks/47/',
        ...
    ]
}
```

* #### SlugRelatedField

使用 `SlugRelatedField` 将返回一个指定对应关系 model 中的字段，需要擦参数 `slug_field` 中指定字段名称。

参数：

- `slug_field` 应该用于表示目标的字段。这应该是唯一标识任何给定实例的字段。例如 `username` 。这是必选参数
- `queryset` 验证字段输入时用于模型实例查询的查询器。 关系必须明确设置 `queryset`，或设置 `read_only = True`
- `many` 如果应用于多对多关系，则应将此参数设置为 `True`
- `allow_null` 如果设置为 `True`，则该字段将接受 `None` 的值或为空的关系的空字符串。默认为 `False`

序列化模型如下

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
```

序列化结果如下：

```python
{
    'album_name': 'Dear John',
    'artist': 'Loney Dear',
    'tracks': [
        'Airport Surroundings',
        'Everything Turns to You',
        'I Was Only Going Out',
        ...
    ]
}
```

* #### HyperlinkedIdentityField

使用 `HyperlinkedIdentityField` 将返回指定 `view-name` 的超链接的字段。

参数：

- `view_name` 应该用作关系目标的视图名称。如果您使用的是标准路由器类，则它将是格式为 `<model_name>-detail` 的字符串。必选参数
- `lookup_field` 应该用于查找的目标上的字段。应该对应于引用视图上的 `URL` 关键字参数。默认值为 `pk`
- `lookup_url_kwarg` 与查找字段对应的 `URL conf` 中定义的关键字参数的名称。默认使用与 `lookup_field` 相同的值
- `format` 如果使用 `format` 后缀，超链接字段将对目标使用相同的 `format` 后缀，除非使用 `format` 参数进行覆盖

序列化模型如下

```python
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'track_listing')
```

序列化结果如下：

``` python
{
    'album_name': 'The Eraser',
    'artist': 'Thom Yorke',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

* #### 嵌套序列化关系模型

在序列化模型中指定嵌套序列化关系模型将返回一个该嵌套序列化关系模型对应的数据模型中序列化的数据。读起来有些拗口，看例子吧。

参数：

- `many` 如果应用于多对多关系，则应将此参数设置为 `True`

序列化模型如下

```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')
```

序列化结果如下：

```python
 {
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
    ],
}
```



* **StringRelatedField**


  返回一个对应关系 model 的 `__unicode__()` 方法的字符串,这个字符串是只读的。

* SerializerMethodField()

http://blog.csdn.net/kongxx/article/details/50042579


#### Requests和Responses

RestFramework的Requests对象扩展了原生的HttpRequest,提供了更灵活的请求处理。

它的核心属性：request.data

和 requests.POST 类似，但更强大：

- request.POST # 只处理form数据.只接受'POST'方法.
- request.data # 处理任意数据.接受'POST','PUT'和'PATCH'方法.

Reponse对象：

`return Response(data)`  它的返回类型由客户端的请求决定。

#### 为URL添加可选的数据格式后缀

我们的responses支持多种返回格式，利用这点我们可以通过在URL中添加格式后 缀的方法来获取单一数据类型，这意味着我们的URL可以处理类 似	http://example.com/api/items/4/.json	这样的格式。

首先在views添加	format	参数：

```
def	snippet_list(request,	format=None):
def	snippet_detail(request,	pk,	format=None):
```

然后修改	urls.py	，添加	format_suffix_patterns：

```python
from django.conf.urls import url 
from rest_framework.urlpatterns	import format_suffix_patterns 
from snippets import views
urlpatterns	=[
    url(r'^snippets/$',views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$',views.snippet_detail),
]
urlpatterns	=format_suffix_patterns(urlpatterns)
```

我们不需要添加任何额外信息，它给我们一个简单清晰的方法去获取指定格式的数 据。



#### 状态码

数字的HTTP状态码并不好读，扩展为了每个状态码提供了更明显的标志。如`HTTP_400_BAD_REQUEST`

#### 视图

Rest Framework 提供了两种方式来编写视图：

##### 1. 基于视图函数的@api_view

```python
  from rest_framework.decorators import api_view
    
  @api_view(['GET', 'POST'])
  def task_list(request):
       if request.method == 'GET':
           tasks = Task.objects.all()

           serializer = TaskSerializer(tasks, many=True)
           return Response(serializer.data)

       elif request.method == 'POST':
           serializer = TaskSerializer(data=request.data)
           if serializer.is_valid():
               serializer.save()

               return Response(serializer.data, status=status.HTTP_201_CREATED)
           else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   @api_view(['GET', 'PUT', 'DELETE'])
   def task_detail(request, pk):
       try:
           task = Task.objects.get(pk=pk)
       except Task.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)

       if request.method == 'GET':
           serializer = TaskSerializer(task)
           return Response(serializer.data)
       elif request.method == 'PUT':
           serializer = TaskSerializer(task, data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       elif request.method == 'DELETE':
           task.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
```

   

##### 2. 基于类视图的APIView

```python
   class TaskList(APIView):
       def get(self, request, format=None):
           tasks = Task.objects.all()
           serializer = TaskSerializer(tasks, many=True)
           return Response(serializer.data)
           
       def post(self, request, format=None):
           serializer = TaskSerializer(data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
           else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   class TaskDetail(APIView):
       def get_object(self,pk):
           try:
               return Task.objects.get(pk=pk
           except Task.DoesNotExist:
               raise Http404

       def put(self,request,pk,format=None):
           task = self.get_object(pk)
           serializer = TaskSerializer(task, data=request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       def delete(self, request, pk, format=None):
           task = self.get_object(pk)
           task.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
```

   使用类视图的好处是可以方便的重用代码，很多相似的关于增删改查代码封装在了REST Framework的mixins类中。

##### minxins:

```python
from rest_framework import mixins
class TaskListMi(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class TaskDetailMi(mixins.RetrieveModelMixin,
    			   mixins.UpdateModelMixin,
    			   mixins.DestroyModelMixin,
				   generics.GenericAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

   我们可以更进一步,使用通用视图。

##### 通用类视图：

```python
class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailCreate(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

 

#### 权限和认证

并不是所有人都可以对数据模型进行改变。

##### 修改模型

向task模型添加外键owner，也就是添加了一对多的关系：

```python
class Task(models.Model):
    owner = models.ForeignKey('auth.User', related_name='tasks')
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述')
    completed = models.BooleanField('是否完成', default=False)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title
```

添加了作者，auth.User是自带用户模型，可以通过添加admin管理员的方式来添加：

`python manage.py createsuperuser`

##### 修改seralizers

```python
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'owner')
```

添加了一行 owner,这个字段是关系字段，默认不会在TaskSerialzer中，所以我们要手动添加，注意fields里也要添加。

ReadOnlyField 类型，不同于其他字段类型，比如 CharField , BooleanField 等。这种类型是只读的，用于进行序列化时候的展示，并且反序列化时不会被修改。这里我们也可以使用 `CharField(read_only=True)` 来替代它。

source决定了显示那个参数值，这里显示owenr（外键指的是User.）的username用户名属性。



##### 添加permissions.py

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
```

IsAuthenticatedOrReadOnly这个类确保了只有认证用户才有读写权限，未认证用户只有读的权限。

##### 修改views.

```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly

class TaskMixin(object):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class TaskList(TaskMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetail(TaskMixin, RetrieveUpdateDestroyAPIView):
    pass
```



##### 修改URL

task/urls.py

```python
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^tasks/$', views.TaskList.as_view(), name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetail.as_view(), name='task_detail'),

]
```

项目名/urls.py

```python
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/',include('task.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
```

访问http://localhost:8000/api/tasks/ 可看到restframework自带的调试窗口。（需要在settings里配置'app[rest_framework']）,和应用一样，才能看到调试上窗口。



#### Relationships和Hyperlinked

主键模型关系

超链接模型关系，提高内聚性以及可读性。



##### 分页

settings.py:

`REST_FRAMEWORK={'PAGE_SIZE':10}`

所有关于框架的配置都可以在这个字典中配置。



#### ViewSets和Routers

ViewSets,在一种使开发人员聚焦于API的状态和实现，基于常见的约定而自动进行URL配置。

ViewSets,被调用的时候才会和对应的方法进行绑定，通常是Route类管理URL配置的时候。

用UserViewSet来取代UserLIst和UserDetail,移除两个类，添加：

```python
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
```


##### 权衡Views和Viewsets

viewsets是一种很用的抽象，它帮助我们确保URL符合惯例，减少代码编写量，使
你专注于API交互和设计而不是URL配置上。
但这并不意味这总是一种好的选择，就好象函数视图和类视图之间的权衡一样，使
用viewsets相比于显示构建vews，有些隐晦。	

