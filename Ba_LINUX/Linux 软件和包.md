Tags:[linux, linux_software]

### 软件源码

#### 可执行文件

在linux真正能运行的是二进制文件。



#### 函数库

提供可调用的函数接口， 比如unix中的一些函数接口，或其他软件提供的接口。

相同功能能够复用。

比如：/usr/include, /lib, /usr/lib 中的函数。

      人能够读懂的代码（源代码） ->  一种编译器  ->  二进制程序 + 库 ->   二进制程序



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

  `tar rvf m.tar m/a/b/j.txt`

  这里的j.txt实际 目录结构要和包里的一致
  
  tar.gz是压缩（-z)，则无法给它追加文件


tar 只是一种压缩文件格式，所以，它只是把文件压缩打包而已。

tar一般包括编译脚本，你可以在你的环境下编译，所以具有通用性。

如果你的包不想开放源代码，你可以制作成rpm，如果开源，用tar更方便了。

tar一般都是源码打包的软件，需要自己解包，然后进行安装三部曲，./configure, make, make install.　来安装软件。

#### gzip

gzip 是由 GNU 计划所开发出来的压缩指令，该指令已经取代了 compress 。
后来 GNU 又开发出 bzip2 及 xz 这几个压缩比更好的压缩指令gzip 可以说是应用度最广的压缩指令了！目前 gzip 可以解开 compress, zip 与 gzip 等软件所压缩的文件。
至于 gzip 所创建的压缩文件为 *.gz 的文件名

选项与参数：
-c ：将压缩的数据输出到屏幕上，可通过数据流重导向来处理；
-d ：解压缩的参数；
-t ：可以用来检验一个压缩文件的一致性～看看文件有无错误；
-v ：可以显示出原文件/压缩文件的压缩比等信息；
-# ：# 为数字的意思，代表压缩等级，-1 最快，但是压缩比最差、-9 最慢，但是压缩比最好！默认是 -6

* 压缩：
  ```shell
  [dmtsai@study tmp]$ gzip -v services
  services: 79.7% -- replaced with services.gz
  ```
  注意： 压缩后，原文件会消失

* 解压：
  `gzip -d services.gz`
  与 gzip 相反， gzip -d 会将原本的 .gz 删除，回复到原本的 services 文件

* services 用最佳的压缩比压缩，并保留原本的文件
  `gzip -9 -c services > services.gz`
  -c 与 >结合可以使用保留原本文件
  ​
读取 zcat/zmore/zless
zcat/zmore/zless 则可以对应于
cat/more/less 的方式来读取纯文本文件被压缩后的压缩文件！ 由于 gzip 这个压缩指令主要想
要用来取代 compress 的，所以不但 compress 的压缩文件可以使用 gzip 来解开，同时 zcat
这个指令可以同时读取 compress 与 gzip 的压缩文件

#### bz2
bzip2 则是为了取代
gzip 并提供更佳的压缩比而来的。 bzip2 真是很不错用的东西～这玩意的压缩比竟然比 gzip
还要好～至于 bzip2 的用法几乎与 gzip 相同


### 安装软件的方式

### 下载源文件编译，安装：

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


### 软件包（安装包）

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



### rpm

 RedHat Package Manager 

这个软件管理
的机制是由 Red Hat 这家公司发展出来的。 RPM 是以一种数据库记录的方式来将你所需要
的软件安装到你的 Linux 系统的一套管理机制

他最大的特点就是将你要安装的软件先编译过， 并且打包成为 RPM 机制的包装文件，通过
包装好的软件里头默认的数据库记录， 记录这个软件要安装的时候必须具备的相依属性软
件，当安装在你的 Linux 主机时， RPM 会先依照软件里头的数据查询 Linux 主机的相依属性
软件是否满足， 若满足则予以安装，若不满足则不予安装。那么安装的时候就将该软件的信
息整个写入 RPM 的数据库中，以便未来的查询、验证与反安装！这样一来的优点是：

1. 由于已经编译完成并且打包完毕，所以软件传输与安装上很方便 （不需要再重新编
    译）；
2. 由于软件的信息都已经记录在 Linux 主机的数据库上，很方便查询、升级与反安装



#### rpm 安装指令

安装软件是 root 的工作，因此你得要是 root 的身份才能够操作 rpm 这指令的。

```shell
[root@study ~]# rpm -ivh package_name
选项与参数：
-i ：install 的意思
-v ：察看更细部的安装信息画面
-h ：以安装信息列显示安装进度
范例一：安装原版光盘上的 rp-pppoe 软件
[root@study ~]# rpm -ivh /mnt/Packages/rp-pppoe-3.11-5.el7.x86_64.rpm
Preparing... ################################# [100%]
Updating / installing...
1:rp-pppoe-3.11-5.el7 ################################# [100%]
范例二、一口气安装两个以上的软件时：
[root@study ~]# rpm -ivh a.i386.rpm b.i386.rpm *.rpm
# 后面直接接上许多的软件文件！
范例三、直接由网络上面的某个文件安装，以网址来安装：
[root@study ~]# rpm -ivh http://website.name/path/pkgname.rpm
```



rpm 安装时常用的选项与参数说明:

| 选项            | 代表意义， 使用时机                                          |
| --------------- | ------------------------------------------------------------ |
| --nodeps        | 当发生软件属性相依问题而无法安装，但你执意安装时。危险性： 软件会有相依性的原因是因为彼此会使用到对方的机制或功能，如果强制安装而不考虑软件的属性相依， 则可能会造成该软件的无法正常使用！ |
| --replacefiles  | 如果在安装的过程当中出现了“某个文件已经被安装在你的系统上面”的信息，又或许出现版本不合的讯息 （confilcting files） 时，可以使用这个参数来直接覆盖文件。危险性： 覆盖的动作是无法复原的！
所以，你必须要很清楚的知道被覆盖的文件是真的可以被覆盖喔！否则会欲哭无泪！ |
| --force         | 这个参数其实就是 --replacefiles 与 --replacepkgs 的综合体！  |
| --test          | 想要测试一下该软件是否可以被安装到使用者的 Linux 环境<br/>当中，可找出是否有属性相依的问题。范例为：
rpm -ivh pkgname.i386.rpm --test |
| --justdb        | 由于 RPM 数据库破损或者是某些缘故产生错误时，可使用这<br/>个选项来更新软件在数据库内的相关信息。 |
| --nosignature   | 想要略过数码签章的检查时，可以使用这个选项。                 |
| --prefix 新路径 | 要将软件安装到其他非正规目录时。举例来说，你想要将某软件安装到 /usr/local 而非正规的 /bin, /etc 等目录， 就可以使用“ --prefix/usr/local ”来处理了。 |
| --noscripts     | 不想让该软件在安装过程中自行执行某些系统指令。说明：<br/>RPM 的优点除了可以将文件放置到定位之外，还可以自动执行一些前置
作业的指令，例如数据库的初始化。 如果你不想要让 RPM 帮你自动执行
这一类型的指令，就加上他吧！ |

建议直接使用 -ivh

例题：在没有网络的前提下，你想要安装一个名为 pam-devel 的软件，你手边只有原版光
盘，该如何是好？答：你可以通过挂载原版光盘来进行数据的查询与安装。请将原版光盘放
入光驱，下面我们尝试将光盘挂载到 /mnt 当中， 并据以处理软件的下载啰：
挂载光盘，使用： `mount /dev/sr0 /mnt`
找出文件的实际路径：`find /mnt -name 'pam-devel*'`
测试此软件是否具有相依性：` rpm -ivh pam-devel... --test`
直接安装：` rpm -ivh pam-devel...`
卸载光盘： `umount /mnt`



#### rpm 升级与更新

就以 -Uvh 或 -Fvh 来升级即可，-U 与 -F 的意义还是不太一样的，基本的差别是这
样的：

| UVh  | 后面接的软件即使没有安装过，则系统将予以直接安装； 若后面接的软件有安装<br/>过旧版，则系统自动更新至新版 |
| ---- | ------------------------------------------------------------ |
| Fvh  | 如果后面接的软件并未安装到你的 Linux 系统上，则该软件不会被安装；亦即只<br/>有已安装至你 Linux 系统内的软件会被“升级”！ |



#### rpm 查询

```shell\
[root@study ~]# rpm -qa &lt;==已安装软件
[root@study ~]# rpm -q[licdR] 已安装的软件名称 &lt;==已安装软件
[root@study ~]# rpm -qf 存在于系统上面的某个文件名 &lt;==已安装软件
[root@study ~]# rpm -qp[licdR] 未安装的某个文件名称 &lt;==查阅RPM文件
选项与参数：
查询已安装软件的信息：
-q ：仅查询，后面接的软件名称是否有安装；
-qa ：列出所有的，已经安装在本机 Linux 系统上面的所有软件名称；
-qi ：列出该软件的详细信息 （information），包含开发商、版本与说明等；
-ql ：列出该软件所有的文件与目录所在完整文件名 （list）；
-qc ：列出该软件的所有配置文件 （找出在 /etc/ 下面的文件名而已）
-qd ：列出该软件的所有说明文档 （找出与 man 有关的文件而已）
-qR ：列出与该软件有关的相依软件所含的文件 （Required 的意思）
-qf ：由后面接的文件名称，找出该文件属于哪一个已安装的软件；
-q --scripts：列出是否含有安装后需要执行的脚本档，可用以 debug 喔！
查询某个 RPM 文件内含有的信息：
-qp[icdlR]：注意 -qp 后面接的所有参数以上面的说明一致。但用途仅在于找出
某个 RPM 文件内的信息，而非已安装的软件信息！注意！

```

一般使用-qa, -ql就可以了



#### rpm 卸载

解安装的过程一定要由最上层往下解除

移除的选项很简单，就通过 -e 即可移除。不过，很常发生软件属性相依导致无法移除某些软
件的问题

```shell
# 1\. 找出与 pam 有关的软件名称，并尝试移除 pam 这个软件：
[root@study ~]# rpm -qa &#124; grep pam
fprintd-pam-0.5.0-4.0.el7_0.x86_64
pam-1.1.8-12.el7.x86_64
gnome-keyring-pam-3.8.2-10.el7.x86_64
pam-devel-1.1.8-12.el7.x86_64
pam_krb5-2.4.8-4.el7.x86_64
[root@study ~]# rpm -e pam
error: Failed dependencies: &lt;==这里提到的是相依性的问题
libpam.so.0（）（64bit） is needed by （installed） systemd-libs-208-20.el7.x86_64
libpam.so.0（）（64bit） is needed by （installed） libpwquality-1.2.3-4.el7.x86_64
....（以下省略）....
# 2\. 若仅移除 pam-devel 这个之前范例安装上的软件呢？
[root@study ~]# rpm -e pam-devel &lt;==不会出现任何讯息！
[root@study ~]# rpm -q pam-devel
package pam-devel is not installed

```



由于 RPM 文件常常会安装/移除/升级等，某些动作或许可能会导致 RPM 数据库 /var/lib/rpm/
内的文件破损。果真如此的话，那你该如何是好？别担心，我们可以使用 --rebuilddb 这个选
项来重建一下数据库:

`[root@study ~]# rpm --rebuilddb <==重建数据库`



### srpm

Source RPM, 的扩展名是以 *.src.rpm 这种格式来命名的

也就是这个 RPM 文件里面含有源代码,并没有经过编译。

既然 SRPM 提供的是源代码，那么为什么我们不使用 Tarball 直接来安装就好了？

这是因为 SRPM 虽然内容是源代码， 但是他仍然含有该软件所需要的相依性软件说明、以及所有 RPM 文件所提供的数据。
同时，他与 RPM 不同的是，他也提供了参数配置文件（就是 configure 与 makefile）

* 先将该软件以 RPM 管理的方式编译，此时 SRPM 会被编译成为 RPM 文件；
* 然后将编译完成的 RPM 文件安装到 Linux 系统当中



### apt

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

### yum
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



#### 只下载 rpm 不安装

`sudo yum install --downloadonly --downloaddir=/tmp <package-name> `

注意，如果下载的包包含了任何没有满足的依赖关系，yum将会把所有的依赖关系包下载，但是都不会被安装。

另外一个重要的事情是，在CentOS/RHEL 6或更早期的版本中，你需要安装一个单独yum插件(名称为 yum-plugin-downloadonly)才能使用--downloadonly命令选项：

`sudo yum install yum-plugin-downloadonly `

如果没有该插件，你会在使用yum时得到以下错误：

Command line error: no such option: --downloadonly





### lsmod

