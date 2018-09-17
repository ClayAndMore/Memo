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

#### 新建目录（mkdir）

`mkdir mydir`  创建一个名为mydir的空目录

`mkdir -p father/son/grandson`  -p创建一个多级目录

#### 新建文件（touch)

`touch test`创建一个空白文件test

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

#### 查看文件

* 使用cat,tac和nl查看文件

cat为正序显示，tac倒序显示

nl 添加行号并打印

* more 和 less命令分页查看，他俩功能基本一致 ，用man命令看细节

`more test`

* 用head和tail命令查看文件，一个只看头10行（默认）,一个只看尾10行
* 使用file查看文件类型


#### state

查看文件状态，eg: `state filename`



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

​	r 可读。

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



#### 删除符合条件的文件

eg： 删除当下目录的所有pyc文件

```
find . -name \*.pyc -delete
```



#### 查找文件中的字符串

我们用grep命令来查找：
`grep -rn "x" *  `

-rn表示递归查找，x表示要查找的字符，*表示当前目录下的所有文件
