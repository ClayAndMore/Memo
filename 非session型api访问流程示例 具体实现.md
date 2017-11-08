### 写在前面:

这里是三元版本后端的设计,根据三元分离的属性和相关功能,总结了对比与原产品需要增加的改动:

* api的权限检测和账号的登陆认证

* 数据库的增加和改动,如用户信息,操作日志都要记录.

* 为新功能增加新api


目的：完成 接口-账户-权限-资源 的连接


### api的权限检测和账号的登陆认证
非session型api访问流程示例 具体实现

####　1.开始－提取tonken

客户端发起请求,访问api,,我们从header或cookie中获得token.

如果是登录请求，我们可以获得加密过的账号和密码，解密和后台db读取的另一种加密密码对比。

请求成功返回一个token。

考虑可以在token中设访问域。

传输用https ，防止中途拦截。



#### 2.校验token

目前有两种方案校验token ：

* 每次请求都将token输入一个功能函数来解密，得到用户信息。

  缺点：

  * 因为每次api请求都要解密，有些繁琐。

  优点：

  * 由于这是CPU的计算，不会影响性能
  * 分布式部署情况下可用

* 第二种方案是将token和其相关的用户信息存入内存

  每次用户登陆都在内存种设立一种：`token->用户信息` 的对应表。

  api请求要将其token和内存种的匹配，匹配成功返回用户信息。

  缺点：

  * 分布式部署下不可用
  * 增加了对内存信息的管理，如删除登出的用户
  * 当用户多时，影响内存

  优点：

  * 省去解密过程，简化程序，减少计算量。

缺陷： 只有token的验证不是安全的验证。



#### 3.初始话资源和权限检测_rbac

我们用python的rbac库来控制权限,github:https://github.com/tonyseek/simple-rbac

如管理员增加用户接口的操作,我们可用如下demo来看rbac的用法:

```python
# coding:utf-8
from rbac.acl import Registry
from rbac.context import IdentityContext, PermissionDenied

# 注册
acl = Registry()
context = IdentityContext(acl)

# 添加用户类别
acl.add_role("admin")
acl.add_role("audit")
acl.add_role("operator")

# 添加资源
acl.add_resource("user")
acl.add_resource("log")
acl.add_resource("function")

# 添加权限
acl.allow("admin", "add", "user")
acl.allow("audit", "query", "log")
acl.allow("operator", "operat", "function")

# 我们现在是管理员,token取得的权限在这里赋值.
@context.set_roles_loader
def first_load_roles():
    yield "admin"

print "* Now you are %s." % ", ".join(context.load_roles())

@context.check_permission("add","user", message="只有管理员才有权限增加用户")
def add_user_api():
    print "you add a user"

@context.check_permission("query","log", message="只有审计员才有权限查看日志")
def query_log_api():
    print "you query the logs"

add_user_api()
query_log_api()
```

前半部分是初始化角色资源和相关权限,资源和权限很多,我们可以从DB中获取.

或者用yaml做一个单独的配置文件.

当然这个过程是执行一次的,在应用运行的时候.

运行输出:

```
* Now you are admin.
you add a user
Traceback (most recent call last):
  File "rbac_test.py", line 40, in <module>
    query_log_api()
  File "/home/wy/miniconda3/envs/py2.6/lib/python2.6/site-packages/rbac/context.py", line 21, in wrapper
    with self:
  File "/home/wy/miniconda3/envs/py2.6/lib/python2.6/site-packages/rbac/context.py", line 27, in __enter__
    self.check()
  File "/home/wy/miniconda3/envs/py2.6/lib/python2.6/site-packages/rbac/context.py", line 38, in check
    raise self.exception(**self.exception_kwargs)
rbac.context.PermissionDenied: 只有审计员才有权限查看日志
```

当操作不具备的权限时会抛出异常.



#### 4. 访问资源,返回请求数据.

每次资源的请求基本会有相应的内容记录供审计员审计。

这里需要数据库的增操作。



### DB



### 新API的增加

现在API 都在startup.py的管理中,考虑是否分离出新的文件来管理新的api.

原来的startup.py 都属于操作员的API.

我们可以为每种权限单独增加一个API文件.  便于分离管理.





