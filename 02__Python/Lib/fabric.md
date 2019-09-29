Tags:[python, py_lib]

## Fabric

Fabric是一个Python的库，提供了丰富的同SSH交互的接口，可以用来在本地或远程机器上自动化、流水化地执行Shell命令。

非常适合用来做应用的远程部署及系统维护。简单易用，只需懂得基本的Shell命令。

- HomePage：<http://www.fabfile.org/>
- Docs：<http://docs.fabfile.org/>
- GitHub：<https://github.com/fabric/fabric/>
- ChangeLog：<http://www.fabfile.org/changelog.html>

python > 2.7

### 版本和安装

目前fabric1.x还不支持python3。虽然fabric官方称fabric2.x 会支持python3, 但至少目前还没有看到确切的时间。

在fabirc2.x发布之前，可以使用fabric3.

最好使用fabric3 支持python 2.7 和 python3

### 快速开始

安装后会有fab可执行文件， 默认执行当下目录的fabfile.py 文件：

```
root@openstack:~# cat fabfile.py
def hello():    # 定义任务
    print 'hello world!'

root@openstack:~# fab hello
hello world!

Done.
```

### 基本命令和api

#### fabric常用参数

| 参数项 | 含义                                                         |
| --- | ---------------------------------------------------------- |
| -l  | 显示可用任务函数名                                                  |
| -f  | 指定fab入口文件,默认为fabfile.py, 指定其他文件： eg:fab -f script.py hello |
| -g  | 指定网关（中转设备），比如堡垒机环境，填写堡垒机IP即可                               |
| -H  | 指定目标主机，多台主机用“，”分隔                                          |
| -P  | 以异步并行方式运行多台主机任务，默认为串行运行                                    |
| -R  | 指定角色（Role）                                                 |
| -t  | 设置设备连接超时时间                                                 |
| -T  | 设置远程主机命令执行超时时间                                             |
| -w  | 当命令执行失败，发出告警，而非默认终止任务                                      |

#### fabric常用API

| 方法         | 说明                                                |
| ---------- | ------------------------------------------------- |
| local      | 执行本地命令，如:local('hostname')                        |
| lcd        | 切换本地目录,lcd('/root')                               |
| cd         | 切换远程目录,cd('cd')                                   |
| run        | 执行远程命令，如：run('hostname')                          |
| sudo       | sudo执行远程命令，如：sudo('echo “123456″                  |
| put        | 上传本地文件到远程主机,如：put(src,des)                        |
| get        | 从远程主机下载文件到本地，如：get(des,src)                       |
| prompt     | 获取用户输入信息，如：prompt（‘please enter a new password:’） |
| confirm    | 获取提示信息确认，如：confirm('failed.Continue[Y/n]?')       |
| reboot     | 重启远程主机，reboot()                                   |
| @task      | 函数修饰符，标识的函数为fab可调用的                               |
| @runs_once | 函数修饰符，表示的函数只会执行一次                                 |

#### fabric全局属性设定

| 属性                     | 含义                                                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| env.host               | 定义目标主机,列表表示，如env.host=['xx.xx.xx.xx','xx.xx.xx.xx']                                                                                 |
| env.exclude_hosts      | 排除指定主机，列表表示                                                                                                                         |
| env.port               | 定义目标主机端口，默认为22                                                                                                                      |
| env.user               | 定义用户名                                                                                                                               |
| env.password           | 定义密码                                                                                                                                |
| env.passwords          | 与password功能一样，区别在于不同主机配置不同密码的应用情景,配置此项的时候需要配置用户、主机、端口等信息，如：env.passwords = {'root@xx.xx.xx.xx:22': '123', 'root@xx.xx.xx.xx':'234'} |
| env.getway             | 定义网关                                                                                                                                |
| env.deploy_release_dir | 自定义全局变量                                                                                                                             |
| env.roledefs           | 定义角色分组                                                                                                                              |

#### 

```
[root@192.168.18.196 py_test]#fab -l
Available commands:

    hello
[root@192.168.18.196 py_test]#fab hello
hello Fabirc

Done.
[root@192.168.18.196 py_test]#ls
fabfile.py  fabfile.pyc
[root@192.168.18.196 py_test]#
[root@192.168.18.196 py_test]#ls
fabfile.py  fabfile.pyc
[root@192.168.18.196 py_test]#vim fabfile.py
[root@192.168.18.196 py_test]#fab hello1
Traceback (most recent call last):
  File "/usr/lib/python2.7/site-packages/fabric/main.py", line 763, in main
    *args, **kwargs
  File "/usr/lib/python2.7/site-packages/fabric/tasks.py", line 427, in execute
    results['<local-only>'] = task.run(*args, **new_kwargs)
  File "/usr/lib/python2.7/site-packages/fabric/tasks.py", line 174, in run
    return self.wrapped(*args, **kwargs)
TypeError: hello1() takes exactly 2 arguments (0 given)
[root@192.168.18.196 py_test]#fab hello1:a=ss,b=111
hello + ss111

Done.
[root@192.168.18.196 py_test]
```

```
[localhost] local: ls -l /home
total 18708
drwxr-xr-x. 4 root root       58 Apr 15 13:53 helm_test
-rw-r--r--. 1 root root 19149273 Apr  8 18:33 helm-v2.11.0-linux-amd64.tar.gz
drwxr-xr-x. 2 root root       64 Sep 26  2018 linux-amd64
drwxr-xr-x. 2 root root       43 Apr 16 09:41 py_test
drwxr-xr-x. 8 root root      121 Apr 12 17:32 saythx
drwxr-xr-x. 8 root root     4096 Apr 13 17:46 saythx_k8s
drwxr-xr-x. 2 root root      117 Apr 14 21:16 work

Done.
```

### 实例

#### 函数传参

任务可以带参数：

```python
def hello(name, value):
        print "hello , %s=%s"%(mame , value)
```

#### 执行本地命令

local()方法可以用来执行本地Shell命令：

```python
from fabric.api import local

def hello():
    local('ls -l /home/bjhee/')
    # output = local("echo Hello", capture=True)
```

capture 参数用来捕获标准输出, 这样，Hello字样不会输出到屏幕上，而是保存在变量output里。

capture 参数的默认值是False。

#### 执行远程命令

```python
from fabric.api import run, env
env.hosts=['192.168.18.198',]
env.user = 'root'
env.password = '000000'

def remote():
    run('ls -l /root')
```

可以把用户直接卸载hosts里：

`env.hosts = ['192.168.18.196', '192.168.18.198']`

另外，多台机器的任务是串行执行的

**run()**：在远程服务器上执行Linux命令，还有一个重要的**参数pty**，如果我们执行命令以后需要有一个常驻的服务进程，那么就需要设置pty=False，避免因为Fabric退出导致进程的退出

```
run('service mysqld start',pty=False)
```

执行返回码：

```
result = run('anetstat -lntup|grep -w 25')
print(result)                                   # 命令执行的结果
print(result.return_code)                       # 返回码，0表示正确执行，1表示错误
```

#### 



#### 多角色执行

```python
#自定义fabfile文件如下
#/root/fab.py
from fabric.api import *

local_node = ['127.0.0.1']
remote_node = ['10.116.97.30']

#定义local和remote角色
env.roledefs['local'] = local_node
env.roledefs['remote'] = remote_node

env.user = 'root'
env.password = 'xxx'

#不同的角色执行不同的命令
@roles('local')
def test_local():
    #run命令在roles为local的主机上执行命令"hostname"
    run("hostname")

@roles('remote')
def test_remote():
    run("hostname")
```

通过`fab -R local test_loacl`,  `fab -R remote test_remote `   来执行

eg2：

```python
from fabric.api import env, roles, run, execute, cd

env.roledefs = {
    'staging': ['ip1','ip2'],
    'build': ['ip3']
}

env.passwords = {
    'staging': '11111',
    'build': '123456'
}

@roles('build')
def build():
    with cd('/home/build/myapp/'):
        run('git pull')
        run('python setup.py')

@roles('staging')
def deploy():
    run('tar xfz /tmp/myapp.tar.gz')
    run('cp /tmp/myapp /home/bjhee/www/')

def task():
    execute(build)
    execute(deploy)
```

执行： fab task

#### 文件上传和下载

工作原理是基于scp命令

**get(remote, local)**: 从远程机器上下载文件到本地

```python
from fabric.api import env, get

env.hosts = ['1,1,1,1',]
env.password = '111111'

def hello():
    get('/var/log/myapp.log', 'myapp-0301.log')
```

将远程机上”/var/log/myapp.log”文件下载到本地当前目录，并命名为”myapp-0301.log”。

**put(local, remote)**: 从本地上传文件到远程机器上

```python
from fabric.api import env, put

env.hosts = ['bjhee@example1.com', 'bjhee@example2.com']
env.password = '111111'

def hello():
    put('/tmp/myapp-0301.tar.gz', '/var/www/myapp.tar.gz')
```

地”/tmp/myapp-0301.tar.gz”文件分别上传到两台远程机的”/var/www/”目录下，并命名为”myapp.tar.gz”。

如果远程机上的目录需要超级用户权限才能放文件，可以在”put()”方法里加上”use_sudo”参数：

`put('/tmp/myapp-0301.tar.gz', '/var/www/myapp.tar.gz', use_sudo=True)`

#### 提示输入

它会在终端显示一段文字来提示用户输入，并将用户的输入保存在变量里：

```python
from fabric.api import env, get, prompt

env.hosts = ['1,1,1,1',]
env.password = '111111'

def hello():
    filename = prompt('Please input file name: ')
    get('/var/log/myapp.log', '%s.log' % filename)
```

还可以对用户输入给出默认值及类型检查：

`port = prompt('Please input port number: ', default=8080, validate=int)`

则port变量即为默认值8080；如果你输入字符串，终端会提醒你类型验证失败，让你重新输入，直到正确为止。

#### exeucte / runs_once

通过”execute()”方法，可以在一个”fab”命令中多次调用同一任务，如果想避免这个发生，就要在任务函数上加上”@runs_once”装饰器。

```python
from fabric.api import execute, runs_once

@runs_once
def hello():
    print "Hello Fabric!"

def test():
    execute(hello)
    execute(hello)
```

execute 多少次hello任务，都只会输出一次 Hello Fabric!

### 上下文管理器

Fabric的上下文管理器是一系列与Python的”with”语句配合使用的方法，它可以在”with”语句块内设置当前工作环境的上下文。让我们介绍几个常用的：

#### cd / lcd

cd: 设置远程机的工作目录   

```python
from fabric.api import env, cd, put

env.hosts = ['1.1.1.1', ]
env.password = '111111'

def hello():
    with cd('/var/www/'):
        put('/tmp/myapp-0301.tar.gz', 'myapp.tar.gz')
```

lcd: 设置本机的工作目录

```python
from fabric.api import env, cd, lcd, put

env.hosts = ['1.1.1.1', ]
env.password = '111111'

def hello():
    with cd('/var/www/'):
        with lcd('/tmp/'):
            put('myapp-0301.tar.gz', 'myapp.tar.gz')
```

#### path / settings / shell_env

**path**: 添加远程机的PATH路径

```python
from fabric.api import env, run, path

env.hosts = ['1,1,1,1' ]
env.password = '111111'

def hello():
    with path('/home/'):
        run('echo $PATH')
    run('echo $PATH')
```

假设我们的PATH环境变量默认是”/sbin:/bin”，在上述”with path()”语句块内PATH变量将变为:

`/sbin:/bin:/home`。

出了with语句块后，PATH又回到原来的值。

**settings**: 设置Fabric环境变量参数

```python
def hello():
    with settings(warn_only=True):
        run('echo $USER')
```

环境参数”warn_only”暂时设为True，这样遇到错误时任务不会退出。等效于：`env.warn_only = True`

**shell_env**: 设置Shell环境变量

```python
def hello():
    with shell_env(JAVA_HOME='/opt/java'):
        run('echo $JAVA_HOME')
        local('echo $JAVA_HOME')
```

可以用来临时设置远程和本地机上Shell的环境变量。

#### prefix

设置命令执行前缀

```python
from fabric.api import env, run, local, prefix

env.hosts = ['1,1,1,1', ]
env.password = '111111'

def hello():
    with prefix('echo Hi'):
        run('pwd')
        local('pwd')
```

run()”或”local()”方法的执行都会加上”echo Hi && “前缀，也就是效果等同于：

`run('echo Hi && pwd')`   and `local('echo Hi && pwd')`

#### hide / show  / quiet

### 错误处理

abric在任务遇到错误时就会退出，如果我们希望捕获这个错误而不是退出任务的话，就要开启”warn_only”参数。

1. `fab -w hello`

2. 设置”env.warn_only”环境参数为True
  
   ```
   from fabric.api import env
   env.warn_only = True
   ```
   
   像”run()”, “local()”, “sudo()”, “get()”, “put()”等SSH功能函数都有返回值。当返回值的”succeeded”属性为True时，说明执行成功，反之就是失败。你也可以检查返回值的”failed”属性，为True时就表示执行失败，有错误发生。在开启”warn_only”后，你可以通过”failed”属性检查捕获错误，并执行相应的操作。
   
   ```python
   from fabric.api import env, cd, put
   
   env.hosts = ['1.1.1.1', ]
   env.password = '111111'
   
   def hello():
       with cd('/var/www/'):
           upload = put('/tmp/myapp-0301.tar.gz', 'myapp.tar.gz')
           if upload.failed:
               sudo('rm myapp.tar.gz')
               put('/tmp/myapp-0301.tar.gz', 'myapp.tar.gz', use_sudo=True)
   ```

### 并行执行

多台机器的任务默认情况下是串行执行的。Fabric支持并行任务，当服务器的任务之间没有依赖时，并行可以有效的加快执行速度。怎么开启并行执行呢？办法也是两个：

1. `fab -P hello`

2. 设置”env.parallel”环境参数为True
  
   ```python
   from fabric.api import env
   
   env.parallel = True
   ```

@parallel 和 @serial

```python
from fabric.api import parallel

@parallel  #某一任务并行, 便并行未开启，”runs_in_parallel()”任务也会并行执行
def runs_in_parallel():
    pass

@serial   #某一任务串行，并行已经开启，”runs_serially()”任务也会串行执行。
def runs_serially():
    pass
```

### 输出颜色

惯上认为绿色表示成功，黄色表示警告，而红色表示错误，Fabric支持带这些颜色的输出来提示相应类型的信息：

```python
from fabric.colors import *

def hello():
    print green("Successful")
    print yellow("Warning")
    print red("Error")
```

  所有颜色：

- blue(text，blod=False)  蓝色
- cyan(text，blod=False)  淡蓝色
- green(text，blod=False)  绿色
- magenta(text，blod=False)  紫色
- red(text，blod=False)  红色
- white(text，blod=False)  白色
- yellow(text，blod=False)   黄色

### 打印

```python
abort('----->abort')     # 执行到这里时，直接退出
warn('----->warn')       # 会发出提示信息，不会退出
puts('----->puts')       # 会打印括号中的信息

# 结合颜色
warn(yellow('----->warn'))  
puts(green('----->puts'))  
```
