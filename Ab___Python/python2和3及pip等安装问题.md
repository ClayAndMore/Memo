tags: [python, pip] date: 2017-03-18




### python2和python3区别

http://python.jobbole.com/80006/

#### 字符

python2 有基于ASCII的str()类型，可以通过单独的unicode()转换成unicode类型，但没有byte类型。

python2中不要以0开头来创建一些数据。尽量把开头的零去掉，在python3中不会这样。



#### xrange

python2会常用xrange()创建一个可迭代对象，通常出现在for循环或列表，集合，字典，推导式中。

这里的xrange和python3中的range一样，惰性求值，意味这可以在其上面无限取值。

python2 中range()也可以用，通常比xrange快一点，不过不建议多次迭代中用range,因为range()每次都会在内存中重新生成一个列表。



#### 触发异常

raise  IOError,'file error'

raise  IOError('file error')

python3支持第二种。

异常处理：

```
try:
	....
except NameError,err:  #python3中得变成except NameError as err:
	print err,'our error message'
```



#### for循环变量与全局命名空间泄漏

python2:

```python
i=1
print 'before: i=',i
print [i for i in range(5)]
print 'after: i=',i
```

```
before: i=1
[0,1,2,3,4]
after: i=4
```

python3 改进了，after:i=1



#### input输入

python3用户输入默认储存为str的对象。

python2 中，会判断你的输入而储存为相应对象，如输入123，则存为int对象。

为了避免非字符输入的危险行为，使用raw_input()代替input.这时，再输入123，则存为str对象。

```
>>>my_input=raw_input('enter a number')
123
>>>type(my_input)
<type 'str'>
```



#### 返回可迭代对象，而不是列表

python2中有些迭代函数返回的是列表，而不是可迭代类型。

python2:

```
print range(3)
print type((range(3)))
out:
[0,1,2]
<type 'list'>
```

python3:

```
print (range(3))
print (type(range3))
range(0,3)
<class 'range'>
```





这两天申请了一个云服务器，用的centOS,自带python2.7.5没有pip,

为了做东西，更新了2.7到最新版本。装了python3.5,以及两个版本的pip,很繁琐，下面总结下：

### python 系统自带2.7升级到最新2.7.x

下载python2.7.x:

到官网 

`wget + 包的地址`

解压包 ；tar

进入解压目录

安装：`./config`

`make`

`make install`

看python版本信息`python -V`,此时还是旧版本

先把原来的python文件更名

`mv /usr/bin/python /usr/bin/python2.7.5`

建立软链接,使系统默认是python最新版：

` ln -s /usr/local/bin/python2.7 /usr/bin/python`

重新检测python版本

解决yum的python版本，它是根据系统自带旧版的python：

`vi /usr/bin/yum`

将头部的

`#!/usr/bin/python`改为`#! /usr/bin/python2.7.5`也就是刚才你改的那个旧版的文件名。



到`vi /usr/libexec/urlgrabber-ext-down`
把头部的python改成和/usr/bin/yum中一样的

如果是centos6就没有这一步.yum出现File` "/usr/libexec/urlgrabber-ext-down", line 22, in <module>`的错误就是这里的问题



### python2.7安装pip

到官网去下载，

https://pip.pypa.io/en/stable/installing/

它会提供一个get-pip文件：

`wget https://bootstrap.pypa.io/get-pip.py`

运行`python get-pip.py`

它会下载pip和setuptools。pip依赖setuptools.

这期间可能因为网络问题崩掉，换时间多试几次吧。



### python2和python3共存

#### ubuntu

一般linux系统中自带python2，ubuntu下可用apt安装python3:

`sudo apt-get install python3`

##### 同一文件

用py2运行：

`python2 hello.py`

用py3运行：

`python3 hello.py`

如果每次运行都要加入参数-2/-3比较麻烦的，更简单的方法是我们在编写代码时就在代码头部加入说明，表明这个文件应该是由python2解释运行，还是由python3解释运行。说明的方法是在代码文件的最开始加入一行

```
#! python2
# -*- coding: utf-8 -*-12
```

或者

```
#! python3
# -*- coding: utf-8 -*-12
```

分别表示该文件使用Python2或者Python3解释运行。这样，运行时就可以简化为

```
py hello.py
```



##### 分别安装pip

`sudo apt-get install python2-pip`

`sudo apt-get install python3-pip`



##### 分别使用pip

同理根据需求选择性的使用

```
python2 -m pip install xxxx1
```

`sudo pip2 install packagename`

或者

```
python3 -m pip install xxxx
```

`sudo pip3 install packagename`



#### centos

下载python3:

`wget +官网地址`:`wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3rc1.tar.xz`

解压：

`tar xf Python-3.5.3.tar.xz`

进入目录：

`cd Python-3.5.3.tar.xz`

配置，编译，安装：

`./configure`

`make`

`make install`

ok~

### pip共存

![](http://ojynuthay.bkt.clouddn.com/pip2andpip3.png)



### 各个安装组件的关系

#### distutils（setup.py 相关）

`distutils` 是 python标准库的一部分，2000年发布，使用它能够进行python模块的安装和发布。

setup.py 是`distutils` 写成，安装一个模块到当前的python环境中，可以使用这个模块提供的setup.py文件。

eg： `python setup.py install`

发布一个模块：

*  `python setup.py sdist`  将其打包成tar.gz或者zip包。
*  `python setup.py bdist_rpm`  将其打包成rpm包
*  `python setup.py bdist_wininst` 将其打包成exe安装包。



#### setuptools（easy_install相关) 和 distribute

setuptools 是为了增强distutils而开发的集合。2004年发布，它包含了 `easy_install` 这个工具。

简单的说，setuptools 是一个项目的名称，是基础组件。而 `easy_install` 是这个项目中提供的工具，它依赖基础组件工作。

例如，从 PyPI 上安装一个包：


`easy_install SQLObject`


下载一个包文件，然后安装它：


`easy_install http://example.com/path/to/MyPackage-1.2.3.tgz`


从一个 .egg 格式安装：


`easy_install /my_downloads/OtherPackage-3.2.1-py2.3.egg`

格式是 setuptools 引入的一种文件格式，它使用 .egg 扩展名，用于 Python 模块的安装。

distribute是 setuptools 的一个分支版本。分支的原因可能是有一部分开发者认为 setuptools 开发太慢了。但现在，distribute 又合并回了 setuptools 中。因此，我们可以认为它们是同一个东西。事实上，如果你查看一下 `easy_install` 的版本，会发现它本质上就是 distribute 。

```
# easy_install --version
distribute 0.6.28
```



#### pip

2008年发布，它被用作 `easy_install` 的替代品，但是它仍有大量的功能建立在 setuptools 组件之上。

pip 希望不再使用 Eggs 格式（虽然它支持 Eggs），而更希望采用“源码发行版”（使用 `python setup.py sdist` 创建）。这可以充分利用 [Requirements File Format](https://pip.pypa.io/en/latest/reference/pip_install.html#requirements-file-format) 提供的方便功能。



#### wheel

wheel 本质上是一个 zip 包格式，它使用 .whl 扩展名，用于 python 模块的安装，它的出现是为了替代 Eggs。

pip 提供了一个 wheel 子命令来安装 wheel 包。当然，需要先安装 wheel 模块。



###　离线安装

#### 安装python

地址：http://www.python.org/download/

下载source python 源码包：

`tar -zxf  Python-``3.5``.``0``.tar.tg`

##### 指定安装目录，脱离系统环境

上述解压包完，进入目录： 指定了make时的目录。

`./configure --prefix=/usr/local/python3`

make,刚才目录就好:

`make && make install`

完成，如有需求配置软链。



#### 安装setuptools

地址：<https://pypi.python.org/pypi/setuptools> 

下载源码包XXX.tar.gz

拷贝到linux机器，解压，执行：

`python setup.py install`



##### 指定python版本

注意这个python用全路径，这样也就指定了你要安装setuptools的那个python的版本。



#### 安装pip

地址：<https://pypi.python.org/pypi/pip>

跟上面一样。





### 总结

#### pip

安装pip： 

先下载官方脚本：`curl -O https://bootstrap.pypa.io/get-pip.py`

希望哪个python版本下载就用哪个版本的`./bin/python( pypy 也可以)` ,:

`./bin/python get-pip.py ` 

`./bin/pypy install  三方库`



指定安装库的版本：

`./pip install pymongo==2.5.2`

显示版本： `pip show pymongo`



超时设置：

`sudo pip install --default-timeout=100 future`

这样就不会出现：

```
How to solve ReadTimeoutError: HTTPSConnectionPool(host='pypi.python.org', port=443) with pip
```

最好的办法是改国内镜像源：

`pip  install --index https://pypi.mirrors.ustc.edu.cn/simple/ pandas `

`http://mirrors.sohu.com/python/ `



### 问题

#### python命令行删除和方向键无效

`./python2.7 ./pip install readline`

安装时会提示： gcc failed with exit status

尝试： 

```
yum install patch
yum install ncurses-devel 
yum install readline-deve
```

ubuntu:

`apt-get install python-setuptools python-dev ncurses-dev`



#### 离线安装时的：zipimport.ZipImortError

```
zipimport.ZipImportError: can't decompress data; zlib not available
Makefile:1099: recipe for target 'install' failed
make: *** [install] Error 1
```

缺少zlib 的相关工具包
解决：

1. 安装zlib相关依赖包：`yum -y install zlib*`或者`sudo apt-get install zlibc zlib1g-dev`
2. 到python安装目录下执行`sudo ./configure`
3. 进入 python安装包,修改Module路径的setup文件：`vim module/setup`
   找到一下一行代码：
   `#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`
   去掉注释:
   `zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`
   安装完上面的依赖包后，重新进入终端，进入python的安装包路径下执行：
   `make && make install`
   重新编译安装即可

第三步我在安装3.6的时候没有找到， 也可正常安装