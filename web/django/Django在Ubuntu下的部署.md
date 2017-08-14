---
title: jjjj
date: 2017-05-05 13:11:53
categories:
header-img:
tags:
---

### Nginx

`apt-get install nginx`

启动，停止和重启

```
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
```

#### 配置转发

nginx的默认安装路径在/usr/local/nginx下. 
nginx的默认配置在/etc/nginx下.

把80端口指向8080端口, 方法如下:

修改nginx.conf：

最后http中会有以下两句：

`include /etc/nginx/conf.d/*.conf;`

`include /etc/nginx/sites-enabled/*;`

这样你就可以把已经配置好的各种 server conf 放在 sites-available 里.

默认情况下sites-enabled目录下会放一个sites-available/default的软链接,在sites-available/default已经对localhost进行设置, 导致无论你怎么修改nginx.conf对本地端口进行配置都不会生效. 一直报404错误.

所以此处要把sites-enabled注掉. 或者把该软链接换掉.



在该http配置项中添加以下内容：在上面两句后面，最后一句注释掉了：

```
server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://localhost:8080;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
```

重启nginx，这样在8080端口开启服务，外网也能访问了。




### 防火墙的开启

安装ufw :

`apt-get install ufw`

开启：

`sudo ufw enable`

 `sudo ufw default deny`

运行以上两条命令后，开启了防火墙，并在系统启动时自动开启。

打开或者关闭某个端口：

`sudo ufw allow|deny `

eg: `sudo ufw allow 22/tcp `       开通22端口

删除某条规则：

```
ufw delete allow 22
```

查看防火墙的状态：

`sudo ufw status`

关闭防火墙：

`sudo ufw disable`



### 开启安全组

记得去官网开启安全组



### django

Setting app 中记得加你云服务器IP.

`runserver 127.0.0.1`

这是允许本地访问，一般用nginx来跳转。

`runserver 0.0.0.0` 

这是所有ip都可以访问。



### uwsgi

通过pip 来安装：

`pip install uwsgi`

我们可以这样检测下安装的uwsgi:

```python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
```

运行：

`uwsgi --http :8000 --wsgi-file test.py`

访问本地(不是本地也可以）8000端口，可以看到输出hello world(可以起另一个终端，用curl访问)



退出：

正常是按`ctrl+c`就能正常退出的，但是一旦控制台关闭就不好办了，查了很多资料这样杀进程才能停止掉：

`kill -s QUIT 主进程id` 

如果有supervisor 管理，最好先停止。不然上面的杀进程也杀不掉。



我们可以用配置文件来启动配置更详细的uwsgi服务：

在manage.py 同级新建uwsgi.ini文件：

```ini
[uwsgi]

socket = :8000   # 端口
chdir = /root/workspacePy/Django/Blog_Django_py3 # 项目路径，可以理解为manage.py所在路径
module = Blog_Django_py3.wsgi # wsgi.py所在文件路径
master = true  # 主线程
processes = 4 # 线程数
vacuum = true  #当服务器退出的时候自动清理环境，删除unix socket文件和pid文件
daemonize = /var/log/uwsgi.log #配置日志，就是启动的时候不在控制台显示了都输出到日志去了。
```

配置好，我们用`uwsgi --ini uwsgi.py` 就能方便的启动了。



最后配置nginx 端口到uwsgi端口，可能涉及到静态文件的配置。参考`python manage.py collectstatic` 的用法，在setting中配置一个文件目录static_root:`STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')`,

用命令`python manage.py collectstatic` 就可以差生这个目录，这个目录要配置到nginx中的location中去。

记得每次静态文件有变化时，记得再运行命令进行同步。



### 遇到的坑

在用uwsgi时 ：

1. `invalid request block size`   , 这时要把配置文件的socket改为http。

2. 我的django 是python3.6的 自带python是3.5的，在我用supervisor 的命令command单独测试时并不能在没有进虚拟环境时启动，提示类似`[ Python error: Py_Initialize: Unable to get the locale encoding`的错误，supervisor命令是通过脚本启动的，在command这填写source等命令并不能生效，于是我command填的是运行一个脚本：

   ```
   command = bash /root/workspacePy/Django/Blog_Django_py3/start_pro.sh
   ```

   相应目录start_pro.sh:

   ```
   source activate py3Django && /root/miniconda2/envs/py3Django/bin/uwsgi --ini /root/works    pacePy/Django/Blog_Django_py3/uwsgi.ini
   ```

   就是先进虚拟环境在运行，其实这两条命令可以分开两行写。

3. 用uwsgi起的服务看时，不能渲染前端静态文件的问题。

   在urls.py 文件中：

   ```python
   from django.conf.urls.static import static
   from django.conf import settings
    
   urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^$', views.index, name = 'index'),
        url(r'^aboutme/$', views.about_me, name = 'aboutMe'),
        url(r'^messages/$', views.message, name = 'messages'),
        url(r'^p/', include('blog.urls')),
    ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   ```

   这里就用把我们上面所说的那个配置文件给配置了.

4. 用uwsgi时，如果视图函数文件里有随之改变的全局变量会失效，因为它是多进程处理的，你的操作在一个进程改变了变量，但是在另一个进程里并不能识别到。 