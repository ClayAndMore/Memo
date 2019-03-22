Tags:[linux]

### 文件系统

文件系统是一种存储和组织计算机文件和资料的方法，linux中一切皆文件，无扩展名。

文件格式，正如window系统的FAT32,NTFS格式。

linux有EXT3（主文件系统）和SWAP（交换文件系统）

文件系统数据结构:引导块，超级块（定义数据单元大小）,

data(文件数据)，inode (索引)



ext3基于日志记录的文件系统，所有操作会记录日志，所以重新开机会发现关机前的东西还在。同mac

swap概念同window的虚拟内存，在物理内存不够用时可用虚拟内存。


### 目录结构

以往的 Windows 一直是以存储介质为主的，主要以盘符（C 盘，D 盘...）及分区的来实现文件管理，然后之下才是目录，目录就显得不是那么重要，除系统文件之外的用户文件放在任何地方任何目录也是没有多大关系。所以通常 Windows 在使用一段时间后，磁盘上面的文件目录会显得杂乱无章（少数善于整理的用户除外吧）。然而 UNIX/Linux 恰好相反，UNIX 是以目录为主的，Linux 也继承了这一优良特性。 Linux 是以树形目录结构的形式来构建整个系统的，可以理解为一个用户可操作系统的骨架。虽然本质上无论是目录结构还是操作系统内核都是存储在磁盘上的，但从逻辑上来说 Linux 的磁盘是“挂在”（挂载在）目录上的，每一个目录不仅能使用本地磁盘分区的文件系统，也可以使用网络上的文件系统。举例来说，可以利用网络文件系统（Network File System，NFS）服务器载入某特定目录等。

![](http://ojynuthay.bkt.clouddn.com/linux%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84.png)

/bin: 存放系统可执行文件

/sbin: super bin 存放管理员可用的执行文件

/etc: 系统配置文件

/lib: 共享的类库

/dev: 外设，设备

/tmp: 临时文件

/boot:  启动文件

/root: root用户目录

/home :  相当与win的users ，比如你的用户a,会有home/a

/mnt: 设备挂载

/opt: 优化目录，临时装一下的东西

/usr: 用户程序目录，

--/bin

--/sbin

/var: 系统变量

/proc: 虚拟文件系统，vfs

/lost and found 找回文件



### 目录颜色

![](http://ojynuthay.bkt.clouddn.com/linuxColor.png)



### 目录和文件操作

#### 查看（ls）

看似简单， 如果用全了很有帮助， 默认显示的只有：非隐藏文件的文件名、 以文件名进行
排序及文件名代表的颜色显示如此而已。

看下一些重要的参数吧

* -a: 全部的文件，连同隐藏文件（ 开头为 . 的文件） 一起列出来（常用）

* -d: 仅列出目录本身，而不是列出目录内的文件数据（常用）

* -l ：长数据串行出，包含文件的属性与权限等等数据；（常用）,  **ll 为缩写**

* --full-time ：以完整时间模式 （包含年、月、日、时、分） 输出

  ```
  [root@study ~]# ls -al --full-time ~
  total 56
  dr-xr-x---. 5 root root 4096 2015-06-04 19:49:54.520684829 +0800 .
  dr-xr-xr-x. 17 root root 4096 2015-05-04 17:56:38.888000000 +0800 ..
  -rw-------. 1 root root 1816 2015-05-04 17:57:02.326000000 +0800 anaconda-ks.cfg
  -rw-------. 1 root root 6798 2015-06-04 19:53:41.451684829 +0800 .bash_history
  -rw-r--r--. 1 root root 18 2013-12-29 10:26:31.000000000 +0800 .bash_logout
  -rw-r--r--. 1 root root 176 2013-12-29 10:26:31.000000000 +0800 .bash_profile
  -rw-rw-rw-. 1 root root 176 2013-12-29 10:26:31.000000000 +0800 .bashrc
  ```

* --time={atime,ctime} ：输出 access 时间或改变权限属性时间 （ctime）, 而非内容变更时间 （modification time）, 具体看下面文件变动时间

#### 文件变动时间

是有三个主要的变动时间，那么三个时间的意义是什么呢？

* modification time （mtime）： 当该文件的“内容数据”变更时，就会更新这个时间！内
  容数据指的是文件的内容，而不是文件的属性或权限喔！
* status time （ctime）： 当该文件的“状态 （status）”改变时，就会更新这个时间，举
  例来说，像是权限与属性被更改了，都会更新这个时间啊。
* access time （atime）： 当“该文件的内容被取用”时，就会更新这个读取时间
  （access）。举例来说，我们使用 cat 去读取 /etc/man_db.conf ， 就会更新

```shell
ls -l /etc/man_db.conf
-rw-r--r--. 1 root root 5171 Jun 10 2014 /etc/man_db.conf 
# 2014/06/10 创建的内容（mtime）， 默认显示显示这个时间，修改文件内容也会更新这个时间，如 vi后 wq

ls -l --time=atime /etc/man_db.conf
-rw-r--r--. 1 root root 5171 Jun 15 23:46 /etc/man_db.conf 
# 在 2015/06/15 读取过内容（atime）

ls -l --time=ctime /etc/man_db.conf
-rw-r--r--. 1 root root 5171 May 4 17:54 /etc/man_db.conf 
# 在 2015/05/04 更新过状态（ctime）
```

如果从其他地方复制一个文件过来， ctime时间回变成当前，但是atime和mtime 还是原来旧文件的，这样来说对新文件不合理，那么如何更改atime和mtime呢， 请看touch.



#### 新建文件（touch)

`touch test`创建一个空白文件test



修改文件时间参数：

-a ：仅修订 access time；
-m ：仅修改 mtime ；
-c ：仅修改文件的时间ctime，若该文件不存在则不创建新文件；
-t ：后面可以接欲修订的时间而不用目前的时间，格式为[YYYYMMDDhhmm]

eg:  bashrc 日期改为 2014/06/15 2:02

```
[dmtsai@study tmp]# touch -t 201406150202 bashrc
[dmtsai@study tmp]# date; ll bashrc; ll --time=atime bashrc; ll --time=ctime bashrc
Tue Jun 16 00:54:07 CST 2015
-rw-r--r--. 1 dmtsai dmtsai 231 Jun 15 2014 bashrc
-rw-r--r--. 1 dmtsai dmtsai 231 Jun 15 2014 bashrc
-rw-r--r--. 1 dmtsai dmtsai 231 Jun 16 00:54 bashrc
# 注意看看，日期在 atime 与 mtime 都改变了，但是 ctime 则是记录目前的时间！
```






#### 新建目录（mkdir）

`mkdir mydir`  创建一个名为mydir的空目录

`mkdir -p father/son/grandson`  -p创建一个多级目录



#### 复制(cp)

复制文件：

`cp test father/son/grandson`

复制目录：

`cp -r father dirFolder` 要带参数-r才能将father及整个子目录复制到dirFolder

不让出现“overwrite”：

`cp -r -f sourcefile targetdir`
-r  递归复制，也就是复制文件夹及其下所有文件。
-f 遇到同名的文件时不提示，直接覆盖。

但是为什么加上-f了，还出现“overwrite”的提示呢？

这是因为系统为防止我们误操作，覆盖了不该覆盖的文件，而使用了命令的别名。使用alias命令查看一下：

```
 # alias
alias cp='cp -i'
alias l.='ls -d .* --color=tty'
alias ll='ls -l --color=tty'
alias ls='ls --color=tty'
alias mv='mv -i'
alias rm='rm -i'
```

我们输入的cp命令，其实是“cp -i”命令。

解决办法：

```
在cp前加上一个"\"符号就不使用别名运行了，如下：
# \cp -f sourcefile targetdir
第二种解决办法：
编辑文件，注释掉别名。
# vi ~/.bashrc
在alias cp='cp -i'前加上“#”注释掉这行，wq!保存推出，然后重新登陆就可以了。
```



#### 删除（rm)

`rm test` 可删除文件，若有保护的文件 可加参数-f强制删除

删除目录一定要加上-r

`rm -r father`

#### 移动/重命名（mv)

`mv 源目录文件 目的目录`

`mv 旧的文件名 新的文件名`



-v ，verbose 输出详细的移动过程

-n,   no--clobber   不覆盖已存在文件



#### 查看文件

* 使用cat,tac和nl查看文件

cat为正序显示，tac倒序显示

nl 添加行号并打印

* more 和 less命令分页查看，他俩功能基本一致 ，用man命令看细节

`more test`

* 用head和tail命令查看文件，一个只看头10行（默认）,一个只看尾10行
* 使用file查看文件类型


#### stat

查看文件状态，eg: `state filename`



#### basename, dirname

```
[root@study ~]# basename /etc/sysconfig/network
network &lt;== 很简单！就取得最后的文件名～
[root@study ~]# dirname /etc/sysconfig/network
/etc/sysconfig &lt;== 取得的变成目录名了！
```





### 文件权限

#### 查看文件权限

`ls -l`使用较长文件格式列出文件

会看到一些排列

解释：![](http://ojynuthay.bkt.clouddn.com/%E6%96%87%E4%BB%B6%E6%9D%83%E9%99%90.png)

![](http://ojynuthay.bkt.clouddn.com/%E6%96%87%E4%BB%B6%E6%9D%83%E9%99%902.png)

* linux的文件类型：

`·`一般文件

d 目录文件

l 链接文件（link)，如windows下的快捷方式

b 块设备（block），以块为单位存储的文件

c 字符设备 ，charactor,串口通信时用

s 网络通信设备，socket

p 管道，把一个文件的出口写入一个文件的入口

* 权限设定

r  read 设置为1

w write 设置为2

x 设置为4  ，x 对于文件夹来说是可进入，对于文件来说是可执行。

这样可以简化文件的写法，如7（1+2+4）代表就有rwx的权限



#### 修改文件权限

`chmod [who][+-=][mode] 文件名`

eg:  `chmod u+x myflie`

who 为参数，可选：

u (用户user) 文件或目录的所有者

g (组 group)  同组用户具有的权限

o (其他用户 other)

a （所有用户，系统默认值）



操作参数：

`+` 添加某个权限

`-`减少某个权限

`=` 赋予给定权限，并取消其他权限如果有的话。



mode 参数：

	r 可读。

　　w 可写。

　　x 可执行。

　　X 只有目标文件对某些用户是可执行的或该目标文件是目录时才追加x 属性。

　　s 在文件执行时把进程的属主或组ID置为该文件的文件属主。方式“u＋s”设置文件的用户ID位，“g＋s”设置组ID位。

　　t 保存程序的文本到交换设备上。

　　u 与文件属主拥有一样的权限。

　　g 与和文件属主同组的用户拥有一样的权限。

　　o 与其他用户拥有一样的权限。



文件名：以空格分开的要改变权限的文件列表，支持通配符。



数字修改： `chmod  664 myfile`    数字对应的权限范围是： u,g,o



#### 文件默认权限 umask

查看默认权限的方式：

```shell
[root@study ~]# umask
0022 &lt;==与一般权限有关的是后面三个数字！
[root@study ~]# umask -S
u=rwx,g=rx,o=rx
```



若使用者创建为“文件”则默认“没有可执行（ x ）权限”，亦即只有 rw 这两个项目，也就
是最大为 666 分，默认权限如下： -rw-rw-rw

若使用者创建为“目录”，则由于**x 与是否可以进入此目录有关**，因此默认为所有权限均开
放，亦即为 777 分，默认权限如下： drwxrwxrwx



umask 数值指的是**需要减掉的权限**:

```
0 - user, 2 - group, 2 - others
所以创建文件时 ， 用户自己不用减，其他-2， 666 - 022 = 644 = -rw-r--r--

所以创建目录时 ， 用户自己不用减，其他-2， 777 - 022 = 755 = drwxr-xr-x
```



#### **文件隐藏属性**

下面的chattr指令只能在Ext2/Ext3/Ext4的 Linux 传统文件系统上面完整生效， 其他的文件系统可能就无法完整的支持这个指令了，例如 xfs 仅支持部份参数而已。

```shell
[root@study ~]# chattr [+-=][ASacdistu] 文件或目录名称
选项与参数：
+ ：增加某一个特殊参数，其他原本存在参数则不动。
- ：移除某一个特殊参数，其他原本存在参数则不动。
= ：设置一定，且仅有后面接的参数
A ：当设置了 A 这个属性时，若你有存取此文件（或目录）时，他的存取时间 atime 将不会被修改，
可避免 I/O 较慢的机器过度的存取磁盘。（目前建议使用文件系统挂载参数处理这个项目）
S ：一般文件是非同步写入磁盘的（原理请参考[前一章sync](../Text/index.html#sync)的说明），如果加上 S 这个属性时，
当你进行任何文件的修改，该更动会“同步”写入磁盘中。
a ：当设置 a 之后，这个文件将只能增加数据，而不能删除也不能修改数据，只有root 才能设置这属性
c ：这个属性设置之后，将会自动的将此文件“压缩”，在读取的时候将会自动解压缩，
但是在储存的时候，将会先进行压缩后再储存（看来对于大文件似乎蛮有用的！）
d ：当 dump 程序被执行的时候，设置 d 属性将可使该文件（或目录）不会被 dump 备份
i ：这个 i 可就很厉害了！他可以让一个文件“不能被删除、改名、设置链接也无法写入或新增数据！”
对于系统安全性有相当大的助益！只有 root 能设置此属性
s ：当文件设置了 s 属性时，如果这个文件被删除，他将会被完全的移除出这个硬盘空间，
所以如果误删了，完全无法救回来了喔！
u ：与 s 相反的，当使用 u 来设置文件时，如果该文件被删除了，则数据内容其实还存在磁盘中，可以使用来救援该文件喔！

```

注意1：属性设置常见的是 a 与 i 的设置值，而且很多设置值必须要身为 root 才能设置
注意2：xfs 文件系统仅支持 AadiS 而已



范例：请尝试到/tmp下面创建文件，并加入 i 的参数，尝试删除看看。

```shell
[root@study ~]# cd /tmp
[root@study tmp]# touch attrtest &lt;==创建一个空文件
[root@study tmp]# chattr +i attrtest &lt;==给予 i 的属性
[root@study tmp]# rm attrtest &lt;==尝试删除看看
rm: remove regular empty file `attrtest'? y
rm: cannot remove `attrtest': Operation not permitted
# 看到了吗？呼呼！连 root 也没有办法将这个文件删除呢！赶紧解除设置！
范例：请将该文件的 i 属性取消！
[root@study tmp]# chattr -i attrtest
```



查看文件隐藏属性：

```shell
[root@study ~]# lsattr [-adR] 文件或目录
选项与参数：
-a ：将隐藏文件的属性也秀出来；
-d ：如果接的是目录，仅列出目录本身的属性而非目录内的文件名；
-R ：连同子目录的数据也一并列出来！
[root@study tmp]# chattr +aiS attrtest
[root@study tmp]# lsattr attrtest
--S-ia---------- attrtest
```



####  文件特殊权限： SUID, SGID, SBIT

待续





### 软链接和硬链接

软连接，也叫符号链接（Symbolic Link），可以理解为window上的快捷方式

`sudo ln -s 源文件 目标文件`

**ln -s a b **中的 a 就是源文件，b是链接文件名,其作用是当进入b目录，实际上是链接进入了a目录。 这时的b 是不存在的。

删除软链接：

`rm -rf  b`  注意不是`rm -rf  b/`



硬连接，源文件名和链接文件名都指向相同的物理地址，目录不能够有硬连接，文件在磁盘中只有一个复制，可以节省硬盘空间，由于删除文件要在同一个索引节点属于唯一的连接时才能成功，因此可以防止不必要的误删。

**ln  a b **是建立硬链接


#### whereis, which

`whereis name`可看name文件所在的位置


### /proc
Linux 下的/proc文件系统是由内核提供的，它不是一个真正的文件系统，只是一些系统运行时的信息，

只在内存中，不占用外存空间。

以文件系统的形式，为访问内核数据提供接口。

```
# ls /proc
1      2      262    32212  733        execdomains  locks         stat
10     221    27     32370  8          fb           mdstat        swaps
113    224    2799   330    8820       filesystems  meminfo       sys
12     226    27990  37     9          fs           misc          ...
```

会看到有很多数字的文件夹，这个数字代表pid, 里面内容：

```
/proc/N
/proc/N/cmdline        进程启动时的命令
/proc/N/cwd            链接到当前进程的工作目录
/proc/N/environ        进程环境变量列表
/proc/N/exe            链接到进程的执行命令文件
/proc/N/fd             进程相关的所有文件描述符
/proc/N/maps           与进程相关的内存映射信息
/proc/N/mem            代指进程持有的内存，不可读
/proc/N/root           链接到进程的根目录
/proc/N/stat           进程的状态
/proc/N/statm          进程使用的内存状态
/proc/N/status         进程状态信息，比stat更具可读性
/proc/self/            链接到当前正在运行的进程
```





### Mount


`mount [-t 文件系统][-L label名][-o 额外选项]] 设备名称名 挂载点`

* 单纯输mount 会显示当前的挂载信息， 加上`-l `会显示label名
* -t 欲挂载的文件系统类型： ext2,ext3 等。
* -L 除了利用设备文件名（如/dev/hdc6）, 还可以用它的卷标名称（Label)来进行挂载。
* -o 可以跟上额外选项，如账号，密码， 读写权限等。

eg:

将`/dev/hdc6`挂载到`/mnt/hdc6` 上：

`mkdir /mnt/hdc6`

`mount /dev/hdc6 /mnt/hdc6`

仅仅这样我们就可以进行方便的挂载，可以通过df查看， 为什么如此方便，因为该命令会自动匹配我们的super block


### find 查找文件

` find  [指定查找目录][查找规则]  [查找完后执行的action]`

eg:

`find /etc /tmp /root -name passwd`

注意的是目录之间要用空格分开

查找规则：

   （1）根据文件名查找

           -name     //根据文件名查找（精确查找）
    
           -iname       //根据文件名查找，但是不区分大小写
    
    附文件通配：
    
    *表示  通配任意的字符
    
    `find /etc -name pass*`
    
    ？表示  通配任意的单个字符
    
    `find /etc -name passw?`
    
    [ ] 表示 通配括号里面的任意一个字符
    
    `find /tmp -name "[ab].sh"`

（ 2） 根据文件时间

```
假如在一个目录中保留最近30天的文件，30天前的文件自动删除
 
find /tmp -mtime +30 -type f -name *.sh[ab] -exec rm -f {} \;

 /tmp  --设置查找的目录；
 -mtime +30 --设置时间为30天前；相同的 还有atime,ctime
 -type f --设置查找的类型为文件；
 -name *.sh[ab] --设置文件名称中包含sha或者shb；

 -exec rm -f --查找完毕后执行删除操作；
 
"-atime"、"-ctime"、"-mtime"参数
回忆一下这三个参数的使用方法：

-atime：访问时间，文件被读取或执行的时间。
-ctime：属性改变时间，文件的inode被修改的时间
-mtime：内容修改时间
参数后面会跟上具体的数字：

# 下面的1 这些参数待确定
# -1：24小时之内操作过的
# 1：24小时之外,48小时之内操作过的
# +1：48小时之外操作过的
 
提示：将此命令写入crontab后即可自动完成查找并删除的工作
  
另外的方法大同小异
find . -mtime +30 -type f | xargs rm -rf
这种会快一些：
find /home/file/  -ctime +10 -name "*.txt" -delete 


```

指定时间
```
eg:
# 查看2016-11-03日的数据
find . -newermt '2016-11-03' ! -newermt '2016-11-04' -exec ls -l {} \;

"-newermt"参数

find /dir1 -type f -newermt '2018-5-26 21:00' ! -newermt '2018-5-26 22:00' -exec cp {} /dir2 \;
#将/dir1目录下2018-5-26 21:00到2018-5-26 22:00时间段内修改或生成的文件拷贝到/dir2目录下
该参数中的m其实就表示mtime，t表示绝对时间，那同样还存在：-newerat、-newerct

```



注意：
在使用过程中发现，可能出现这样的错误提示 find: I cannot figure out how to interpret \'2018-05-26' as a date or time
出现这样的问题，一般是因为系统版本低或者在脚本中使用缺少执行环境造成的，可以将单条命令调整为：

cmd="find /dir1 -type f -newermt '2018-5-26 21:00' ! -newermt '2018-5-26 22:00' -exec cp {} /dir2 \;"
echo $cmd | sh



#### 删除符合条件的文件

eg： 删除当下目录的所有pyc文件

```
find . -name \*.pyc -delete
```



#### 查找文件中的字符串

我们用grep命令来查找：
`grep -rn "x" *  `

-rn表示递归查找，x表示要查找的字符，*表示当前目录下的所有文件





### 目录切换

#### OLDPWD

我们知道使用`cd -` 可以换到之前的目录，实际上，`cd -`中，`-`就相当于变量$OLDPWD。`cd -`就相当于cd $OLDPWD`。下面是一个例子：

```
$ pwd
/home/lfqy
$ cd /
$ echo $OLDPWD
/home/lfqy
$ cd $OLDPWD
$ pwd
/home/lfqy
$ 
```



#### dirs

dirs保存了目录栈， 栈顶永远是存放当前的目录

dirs常用的参数：

| 选项 | 含义                                          |
| ---- | --------------------------------------------- |
| -p   | 每行显示一条记录                              |
| -v   | 每行显示一条记录，同时展示该记录在栈中的index |
| -c   | 清空目录栈                                    |



```
[root@localhost ~]# dirs
~
[root@localhost ~]# cd /boot/
[root@localhost boot]# dirs
/boot
[root@localhost boot]# dirs -v
 0  /boot
[root@localhost boot]# 
```



#### pushd

每次pushd命令执行完成之后，默认都会执行一个dirs命令来显示目录栈的内容

* pushed  目录

  pushd后面如果直接跟目录使用，会切换到该目录并且将该目录置于目录栈的栈顶。

  时时刻刻都要记住，目录栈的栈顶永远存放的是当前目录。

  如果当前目录发生变化，那么目录栈的栈顶元素肯定也变了

  反过来，如果栈顶元素发生变化，那么当前目录肯定也变了。

  ```
   $ pwd
   /home/lfqy
   $ pushd /
   / ~
   $ dirs -v
    0  /
    1  ~
   $ pushd ~/Music/
   ~/Music / ~
   $ dirs -v
    0  ~/Music
    1  /
    2  ~
  ```

* pushd 无参数

  pushd不带任何参数执行的效果就是，将目录栈最顶层的两个目录进行交换。前面说过，栈顶目录和当前目录一个发生变化，另一个也变。这样，实际上，就实现了`cd -`的功能。

  ```
  $ dirs -v
    0  ~/Music
    1  /
    2  ~
   $ pushd
   / ~/Music ~
   $ dirs -v
    0  /
    1  ~/Music
    2  ~
   $ pushd
   ~/Music / ~
   $ dirs -v
    0  ~/Music
    1  /
    2  ~ 
  ```

* pushd +n

  `pushd +n`切换到目录栈中的第n个目录(这里的n就是`dirs -v`命令展示的index)，并将该目录以栈循环的方式推到栈顶, 注意这样带来栈的变化：

  ```
   $ dirs -v
    0  ~/Music
    1  /
    2  ~
   $ pushd +2
   ~ ~/Music /
   $ dirs -v
    0  ~
    1  ~/Music
    2  /
   $ pushd +1
   ~/Music / ~
   $ dirs -v
    0  ~/Music
    1  /
    2  ~
   $ 
  ```


#### popd

每次popd命令执行完成之后，默认都会执行一个dirs命令来显示目录栈的内容

* popd 不带参数

  将栈顶推出，删掉并进入栈顶后的目录

  ```
  [root@localhost home]# pushd /root
  ~ /home /
  [root@localhost ~]# dirs -v
   0  ~
   1  /home
   2  /
  [root@localhost ~]# popd
  /home /
  [root@localhost home]# pwd
  /home
  [root@localhost home]# dirs -v
   0  /home
   1  /
  ```


* popd +n

  将栈中第n个删除，不会引起当前目录的变化：

  ```
  root@localhost ~]# dirs -v
   0  ~
   1  /home
   2  /
  [root@localhost ~]# pop +2
  -bash: pop: command not found
  [root@localhost ~]# popd +2
  ~ /home
  [root@localhost ~]# dirs -v
   0  ~
   1  /home
  ```
