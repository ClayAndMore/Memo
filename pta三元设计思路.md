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

该token的实现方式 是 jwt (json web token),

它由三部分组成:

* 头部(header): 描述该jwt的基本信息:

  ```
  {
  "alg": "HS256", //加密算法
  "tpe : "JWT" 
  }
  ```

  头部用base64编码得到: key1 

* 核载(payload)

  ```
  可以放三种信息:
  标准中注册的声明 (建议但不强制使用) ：

  iss: jwt签发者
  sub: jwt所面向的用户
  aud: 接收jwt的一方
  exp: jwt的过期时间，这个过期时间必须要大于签发时间
  nbf: 定义在什么时间之前，该jwt都是不可用的.
  iat: jwt的签发时间
  jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

  公共的声明 ：
  公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.

  私有的声明 ：
  私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

  对于pta:
  我们考虑这里带上用户名和用户权限,为的是解码后减少数据库的查询
  ```

  这部分也用来base64编码得到key2

* 签证信息

  需要用key1+key2 通过hearder中声明的加密方式进行加盐secret组合加密. 这个secret 是全局的,要保护好.



**使用jwt的目的**: 通过上面步骤,我们可以发现jwt通过第一部分和第二部分是可以解密出我们的信息的,所以jwt的目的并不是为了加密传输,是为了两点: 第一,防止token篡改,即使别人知道了我们前两部分的信息,他也不能修改,因为第三部分没有密钥是无法篡改的.  第二, 是减少服务端存session的压力,每次我们解密就好无需做一个session的单独存储,毕竟现在cpu的效率要比你读取数据库的效率高.



如果是登录请求，我们可以获得加密过的账号和密码，解密和后台db读取的另一种加密密码对比。

请求成功返回一个token。这里的加密算法还要再考虑.



传输用https ，防止中途拦截。



#### 2.校验token

目前有两种方案校验token ：

* 每次请求都将token输入一个功能函数来解密，得到用户信息。

  缺点：

  * 因为每次api请求都要解密，有些繁琐。

  优点：

  * 由于这是CPU的计算，不会影响性能
  * 分布式部署情况下可用
  * 这也是使用jwt的好处之一

* 第二种方案是将token和其相关的用户信息存入内存

  每次用户登陆都在内存种设立一种：`token->用户信息` 的对应表。

  api请求要将其token和内存种的匹配，匹配成功返回用户信息。

  缺点：

  * 分布式部署下不可用
  * 增加了对内存信息的管理，如删除登出的用户
  * 当用户多时，影响内存

  优点：

  * 省去解密过程，简化程序，减少计算量。



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

目前考虑两个表,用户表和日志表,日志表的记录一直再增长,而存储相同过多汉字会浪费太多内存.

这个设计待讨论.



### 新API的增加

现在API 都在startup.py的管理中,考虑是否分离出新的文件来管理新的api.

原来的startup.py 都属于操作员的API.

我们可以为每种权限单独增加一个API文件.  便于分离管理.





