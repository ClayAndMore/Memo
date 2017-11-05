## Linux 软件和包



### 解压文件

#### 压缩格式

一些压缩格式：`*.zip`,`*.rar`,`*.7z`后缀的压缩文件（windows和linux)

Linux 上面常见常用的除了以上这三种外，

还有`*.gz`,`*.xz`,`*.bz2`,`*.tar`,`*.tar.gz`,`*.tar.xz`,`*tar.bz2`

tar是打包文件，就是将很多文件合成一个文件，并没有压缩

#### gzip

压缩gzip ,没有tar

`gzip hello.c` 压缩hello.c成hello.c.gz，hello.c会消失。

解压

`gzip -d hello.c.gz`   将hello.c.gz解压成hello.c，hello.c.gz会消失

参数：

-o:不提示的情况下覆盖文件；
-d:-d /home/sunny 指明将文件解压缩到/home/sunny目录下

#### tar

tar是打包格式，一般tar后面会有tar.xz等。

压缩：`tar -czvf [desfile] [sourcefile]`  

desfile 要带上压缩后缀，sourcefile 要全路径，全路径压缩的包内容中也是全路径

当前文件夹内容打包到test.tar：

`tar cvf test.tar *`

解压：`tar -xzvf [sourcefile]`  

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



- 删除tar包中的文件

  eg: 删除aaa.tar中的b,c

  `tar --delete -f aaa.tar b.c`



### 安装软件的方式

#### （1）下载源文件编译，安装：

思路：

1. 先到网站下载源代码，方式包括http,ftp,svn,git..
2. 解开压缩包
3. `./configure`意味着在当前目录下进行配置文件进行配置
4. `make`编译  ，编译源代码成二进制文件
5. `make install`

另：卸载`make uninstall`



#### （2）软件包（安装包）

将可执行文件打包，压缩，常见的格式：rpm(红帽系统下),deb

命名格式： 软件包名_版本号-修订版本__体系架构

#### （2）软件包的管理工具

dpkg(deb包常用的管理工具)

dpkg-deb

dpkg -i package 安装包

dpkg -r package 移除包

dpkg -P package 移除包和配置文件

dpkg -L package  列出安装包清单

dpkg --contents 包的具体文件

**dpkg的缺陷**

- 不能主动从镜像站点获取软件包
- 安装软件包的时候不能自动安装相关依赖包

#### (3)apt(常用在线只能管理工具集)

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



#### 软件源

我们要定期从服务器下载一个软件包列表，使用

`sudo apt-get update`命令来保持本地的软件包列表是最新的。



一些问题：

apt source 镜像站点地址存在哪儿

/etc/apt/sources.list

apt的本地索引存在哪儿

/var/lib/apt/lists/*

apt的下载deb包存在哪里

/var/cache/apt/archives



### 卸载软件

查看所有安装的软件：`dpkg -l`

用上面的完全卸载，如果不想保留配置文件的话

