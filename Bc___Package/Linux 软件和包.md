### 软件源码

#### 可执行文件

在linux真正能运行的是二进制文件。



#### 函数库

提供可调用的函数接口， 比如unix中的一些函数接口，或其他软件提供的接口。

相同功能能够复用。

比如：/usr/include, /lib, /usr/lib 中的函数。



人能够读懂的代码（源代码） ->  一种编译器  ->  二进制程序

​                                                                          库->   二进制程序



#### make 和 configure

每个代码文件都要编译并链接上库文件，整个软件的编译命令则有很多很多， make命令帮我们解决了这个问题。

make命令会在当下的目录搜索Makefile或 makefile这个文件，这个文件里记录了代码如何编译的具体信息。

但是makefile怎么写? 不同内核有的函数库不一样，我们需要个检测程序来校测当前的环境。

这个程序会是同目录下的 configure。

configure 会生成文件Makefile.

所以一个软件的安装通常是 configure后 make.

所以说不能拿make后的软件去另外的机器用。



make install.

make 会根据makefie这个文件里面关于install的选项将make



### 解压文件

#### 压缩格式

一些压缩格式：`*.zip`,`*.rar`,`*.7z`后缀的压缩文件（windows和linux)

Linux 上面常见常用的除了以上这三种外，

还有`*.gz`,`*.xz`,`*.bz2`,`*.tar`,`*.tar.gz`,`*.tar.xz`,`*tar.bz2`

tar是打包文件，就是将很多文件合成一个文件，并没有压缩


#### tar

tar是打包格式，一般tar后面会有tar.xz等。



打包：`tar -czvf [desfile] [sourcefile]`  

desfile 要带上压缩后缀，sourcefile 要全路径，全路径压缩的包内容中也是全路径

* 当前文件夹内容打包到test.tar：

  `tar cvf test.tar *`

* 当前目录打包到test.tar:

  `tar cvf test.tar test`

  这样test.tar里就包含一个test目录



解包：`tar -xzvf [sourcefile]`  

解压到指定文件夹：`tar -xzvf [sourcefile] -C filepath`

命令详解：(这五个必须要用到其中一个，只能一个)

```
    -c: 建立压缩档案
　　-x：解压
　　-t：查看内容
　　-r：向压缩归档文件末尾追加文件
　　-u：更新原压缩包中的文件
```

后面可跟：

```
	-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
	-z: 用gzip来压缩/解压缩文件
	-v: 详细报告tar处理的文件信息。
	-z 支持gzip解压文件
	-j 支持bzip2解压文件
```

注意：

- .tar.gz     格式解压为   `tar   -zxvf   xx.tar.gz`

- .tar.bz2   格式解压为    `tar   -jxvf    xx.tar.bz2`

- 删除tar包中的文件

  eg: 删除aaa.tar中的b,c

  `tar --delete -f aaa.tar b.c`

- 只解压某个文件

  `tar m.tar m/a/b/c.f`

  解压了m包中的/m/a/c.f文件

- 追加到某个文件夹下

  `tar avf m.tar m/a/b/j.txt`

  这里的j.txt实际 目录结构要和包里的一致


tar 只是一种压缩文件格式，所以，它只是把文件压缩打包而已。

tar一般包括编译脚本，你可以在你的环境下编译，所以具有通用性。

如果你的包不想开放源代码，你可以制作成rpm，如果开源，用tar更方便了。

tar一般都是源码打包的软件，需要自己解包，然后进行安装三部曲，./configure, make, make install.　来安装软件。

#### gzip

  压缩gzip ,没有tar

  `gzip hello.c` 压缩hello.c成hello.c.gz，hello.c会消失。

  解压

  `gzip -d hello.c.gz`   将hello.c.gz解压成hello.c，hello.c.gz会消失

  参数：

  -o:不提示的情况下覆盖文件；
  -d:-d /home/sunny 指明将文件解压缩到/home/sunny目录下

  ​



### 安装软件的方式

#### 下载源文件编译，安装：

思路：

1. 先到网站下载源代码，方式包括http,ftp,svn,git..
2. 解开压缩包
3. `./configure`意味着在当前目录下进行配置文件进行配置
4. `make`编译  ，编译源代码成二进制文件
5. `make install`

另：卸载`make uninstall`

工具：
wget:
一个下载工具，和操作系统无关。

基本的语法是：`wget [参数列表] URL。`

1 支持断点下传功能
2 同时支持FTP和HTTP下载方式
3 支持代理服务器
4 设置方便简单
5 程序小，完全免费


#### 软件包（安装包）

将可执行文件打包，压缩，常见的格式：rpm(红帽系统下),deb(Ubuntu).

命名格式： 软件包名_版本号-修订版本__体系架构

rpm 相当于windows中的安装文件，它会自动处理软件包之间的依赖关系。

优缺点来说，rpm一般都是预先编译好的文件，它可能已经绑定到某种CPU或者发行版上面了。


dpkg(deb包常用的管理工具)

dpkg-deb

dpkg -i package 安装包

dpkg -r package 移除包

dpkg -P package 移除包和配置文件

dpkg -l 查看所有安装的软件

dpkg -L package  列出安装包清单

dpkg --contents 包的具体文件

**dpkg的缺陷**

- 不能主动从镜像站点获取软件包
- 安装软件包的时候不能自动安装相关依赖包

#### apt
apt 是ubuntu系统的软件包管理工具

- apt-get 用于管理软件包，包括安装、卸载、升级

  apt-get install package （搜索本地一个数据库，详情看软件源）

  apt-get update   从软件镜像服务器上下载/更新用于本地软件源的软件包列表

  apt-get upgrade 自动升级软件包到最新版本

  apt-get check 检查当前apt管理里面的依赖包情况

  apt-get -f install 修复依赖包关系

  apt-get remove 卸载（但是卸载不干净，不包括软件包的配置文件）

  apt-get remove --purge package (完全卸载)

  apt-get --reinstall install package  重新安装


- apt-cache :用于查询软件包信息：

  apt-cache show package 显示软件包信息

  apt-cache policy package 显示软件包安装状态

  apt-cache depends package 显示软件包依赖关系

  apt-cache search package 在source某个名称的软件


- 软件源

  我们要定期从服务器下载一个软件包列表，使用

  `sudo apt-get update`命令来保持本地的软件包列表是最新的。

- 一些位置：

  apt source 镜像站点地址存在哪儿

  /etc/apt/sources.list

  apt的本地索引存在哪儿

  /var/lib/apt/lists/*

  apt的下载deb包存在哪里

  /var/cache/apt/archives

#### yum
rpm是redhat公司的一种软件包管理机制，直接通过rpm命令进行安装删除等操作，最大的优点是自己内部自动处理了各种软件包可能的依赖关系。

| 説明            | [Redhat](http://d.hatena.ne.jp/keyword/Redhat)系 | [Debian](http://d.hatena.ne.jp/keyword/Debian)系 |
| ------------- | ---------------------------------------- | ---------------------------------------- |
| 更新缓存          | yum makecache                            | [apt](http://d.hatena.ne.jp/keyword/apt)-get update |
| 更新包           | [yum](http://d.hatena.ne.jp/keyword/yum) update | [apt](http://d.hatena.ne.jp/keyword/apt)-get upgrade |
| 检索包           | [yum](http://d.hatena.ne.jp/keyword/yum) search | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) search |
| 检索包内文件        | [yum](http://d.hatena.ne.jp/keyword/yum) provides | [apt](http://d.hatena.ne.jp/keyword/apt)-file search |
| 安装指定的包        | [yum](http://d.hatena.ne.jp/keyword/yum) install | [apt](http://d.hatena.ne.jp/keyword/apt)-get install |
| 删除指定的包        | [yum](http://d.hatena.ne.jp/keyword/yum) remove | [apt](http://d.hatena.ne.jp/keyword/apt)-get remove |
| 显示指定包的信息      | [yum](http://d.hatena.ne.jp/keyword/yum) info | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 显示包所在组的一览     | [yum](http://d.hatena.ne.jp/keyword/yum) grouplist | -                                        |
| 显示指定包所在组的信息   | [yum](http://d.hatena.ne.jp/keyword/yum) groupinfo | -                                        |
| 安装指定的包组       | [yum](http://d.hatena.ne.jp/keyword/yum) groupinstall | -                                        |
| 删除指定的包组       | [yum](http://d.hatena.ne.jp/keyword/yum) groupremove | -                                        |
| 参考库的设定文件      | /etc/[yum](http://d.hatena.ne.jp/keyword/yum).repos.d/* | /etc/[apt](http://d.hatena.ne.jp/keyword/apt)/sources.list |
| 安装完的包的列表      | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qa | dpkg-query -l                            |
| 显示安装完的指定包的信息  | [rpm](http://d.hatena.ne.jp/keyword/rpm) -qi | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) show |
| 安装完的指定包内的文件列表 | [rpm](http://d.hatena.ne.jp/keyword/rpm) -ql | dpkg-query -L                            |
| 安装完的包的信赖包的列表  | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[qR](http://d.hatena.ne.jp/keyword/qR) | [apt](http://d.hatena.ne.jp/keyword/apt)-[cache](http://d.hatena.ne.jp/keyword/cache) depends |
| 安装完的文件信赖的包    | [rpm](http://d.hatena.ne.jp/keyword/rpm) -[q](http://d.hatena.ne.jp/keyword/qR)f | dpkg -S                                  |
