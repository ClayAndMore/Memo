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

- `python setup.py sdist`  将其打包成tar.gz或者zip包。
- `python setup.py bdist_rpm`  将其打包成rpm包
- `python setup.py bdist_wininst` 将其打包成exe安装包。



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



### 离线安装

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



指定安装位置：

`  -t, --target <dir>          Install packages into <dir>. By default this`

`bin/python3 bin/pip3 install pymongo -t /ng8w/lib/python3`



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

#### pip install  error: command 'gcc' failed with exit status 1

You need to reinstall gcc , gcc-c++ and dependencies.

For python 2.7

```
$ sudo yum -y install gcc gcc-c++ kernel-devel
$ sudo yum -y install python-devel libxslt-devel libffi-devel openssl-devel
$ pip install "your python packet"
```



#### error: command 'g++' failed with exit status 1





#### python命令行删除和方向键无效

`./python2.7 ./pip install readline`

安装时会提示： gcc failed with exit status

尝试： 

```
yum install patch
yum install ncurses-devel 
yum install readline-devel
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

