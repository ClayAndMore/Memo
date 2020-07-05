---
title: "09-shell和环境变量.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-04-17 19:54:27 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


### shell

Shell 是指“提供给使用者使用界面”的软件（命令解析器），类似于 DOS 下的 command（命令行）和后来的 cmd.exe。普通意义上的 Shell 就是可以接受用户输入命令的程序。它之所以被称作 Shell 是因为它隐藏了操作系统底层的细节。同样的 Unix/Linux 下的图形用户界面 GNOME 和 KDE，有时也被叫做“虚拟 shell”或“图形 shell”。

shell简而言之就是一个与系统内核交互的壳。

在 UNIX/Linux 中比较流行的常见的 Shell 有 bash，zsh，ksh，csh 等等，Ubuntu 终端默认使用的是 bash，（我们可以去/bin/ 下看一下。）

centos 下所有shell: 

```shell
[root@]# cat /etc/shells 
/bin/sh
/bin/bash
/sbin/nologin
/bin/dash
```



/etc/passwd 中会指定用户登录后用的shell:

```shell
[dmtsai@study ~]$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
....
```







### 环境变量

`$PATH`可看当前的环境变量

`export PATH = $PATH:/home/study`添加/home/study环境变量

`export hello=/home/study`

`cd hello`



所有用户的环境变量：/etc/profile文件
root用户的环境变量：~/.bashrc文件
非root用户的环境变量：/home/非root用户名/.bashrc文件



更新上方环境变量后需要刷新后让其生效： source + 上方文件



#### 修改环境变量

- 当前终端

  在当前终端中输入：`export PATH=$PATH:<你的要加入的路径>`

  不过上面的方法只适用于当前终端，一旦当前终端关闭或在另一个终端中，则无效。

   **注意**这个方法会让其他环境变量无效，尽量不要用这样的方式。

- 当前用户

  在用户主目录下有一个 .bashrc 隐藏文件，可以在此文件中加入 PATH 的设置如下：

  `vi ~/.bashrc`

  加入：

  `export PATH=<你的要加入的路径>:$PATH`

  如果要加入多个路径，只要：

  `export PATH=<你要加入的路径1>:<你要加入的路径2>: ...... :$PATH`

  当中每个路径要以冒号分隔。

  这样每次登录都会生效

- 所有用户

  `sudo vi /etc/profile `

  加入：
  export PATH=<你要加入的路径>:$PATH

  就可以了。

  终端输入：echo $PATH 可以查看环境变量

#### source和.

先介绍下sh命令：

```
。当然，linux中sh是链接到bash上的，所以sh与bash在功能上是没有区别的。
还有就是在执行脚本的时候是用sh + 脚本名的方式来执行，
大部分的时候，简单脚本只要权限设置正确，可以直接执行，不需要sh命令的
```

source命令：
source命令也称为“点命令”，也就是一个点符号（.）,是bash的内部命令。
功能：使Shell读入指定的Shell程序文件并依次执行文件中的所有语句
source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。
用法：
`source filename 或 . filename`
source命令(从 C Shell 而来)是bash shell的内置命令;点命令(.)，就是个点符号(从Bourne Shell而来)是source的另一名称。

source filename 与 sh filename 及./filename执行脚本的区别在那里呢？
1. 当shell脚本具有可执行权限时，用sh filename与./filename执行脚本是没有区别得。./filename是因为当前目录没有在PATH中，所有"."是用来表示当前目录的。
2. sh filename 重新建立一个子shell，在子shell中执行脚本里面的语句，该子shell继承父shell的环境变量，但子shell新建的、改变的变量不会被带回父shell，除非使用export。
3. source filename：这个命令其实只是简单地读取脚本里面的语句依次在当前shell里面执行，没有建立新的子shell。那么脚本里面所有新建、改变变量的语句都会保存在当前shell里面。



#### echo, 变量设置，unset

* 变量的取用， echo

  ```
  [root@bogon wangyu]# echo $HOME
  /root
  [root@bogon wangyu]# echo ${HOME}
  /root
  ```

* 变量的设置

  ```shell
  [root@b] myname = haha   # 注意不能有空格
  -bash: myname: command not found
  [root@b] myname=haha
  [root@b] echo $myname
  haha
  
  # 更多规则
  [root@b] var="lang is $LANG"  # 双引号内的特殊字符如 $ 等，可以保有原本的特性
  [root@b] echo $var
  lang is en_US.UTF-8
  [root@b] var='lang is $LANG'  # 单引号内的特殊字符则仅为一般字符（纯文本）
  [root@b] echo $var
  lang is $LANG
  
  [root@b] myname=ha\ ha   # 空格逃脱，其实就是转义
  [root@b] echo $myname
  ha ha
  [root@b] myname=ha\$ha     # 逃脱$
  [root@b] echo $myname
  ha$ha
  
  
  # 获取其他语句执行结果， 反引号 或 $()
  [root@b] version=`uname -r`
  [root@b] echo $version
  4.11.6-1.el6.elrepo.x86_64
  [root@b] version1=$(uname -r)
  [root@b] echo $version1
  4.11.6-1.el6.elrepo.x86_64
  [root@b] uname -r
  4.11.6-1.el6.elrepo.x86_64
  [root@b] ls  /lib/modules/`uname -r`/kernel
  arch  block  crypto  drivers  fs  lib  mm  net  sound  virt
  
  
  [root@b]# 通常大写字符为系统默认变量，自行设置变量可以使用小写字符
  
  # 累加， 则可用 "$变量名称"或${变量}累加内容
  [root@b] PATH="$PATH":/home/bin
  [root@b] PATH=${PATH}:/home/bin
  [dmtsai@study ~] name=$nameyes # 我要将 name 的内容多出 "yes" 呢, 我们并没有nameyes这个变量
  [dmtsai@study ~] name="$name"yes
  [dmtsai@study ~] name=${name}yes # 以此例较佳！
  
  # 若该变量需要在其他子程序执行，则需要以 export 来使变量变成环境变量： “export PATH”
  [dmtsai@study ~] name=VBird
  [dmtsai@study ~] bash # 进入到所谓的子程序
  [dmtsai@study ~] echo $name # 子程序：再次的 echo 一下；
  # 嘿嘿！并没有刚刚设置的内容喔！
  [dmtsai@study ~] exit # 子程序：离开这个子程序
  [dmtsai@study ~] export name
  [dmtsai@study ~] bash 
  [dmtsai@study ~] echo $name #子程序, 再次执行
  VBird
  ```

* unset





### Bash

bash 兼容了sh，是它的加强版本。

bash 用历史记录功能， 记录你输入过的命令在~/.bash_history中， 不过是记录上次登录的内容，

本次登录的内容都记录在内存中。



#### alias

命令别名设置， `alias l = 'ls -al'`

终端关闭之后，我们设置的别名全部失效。需要添加到.bas_profile里永久生效。

几个常用的别名设置：

```sh
alias untar='tar -zxvf'
alias ping='ping -c 5' #一般我们ping五次即可。
alias www='python -m SimpleHTTPServer 8000' #随时的启动一个web服务器
alias de='docker exec -it'
```

取消 alias

```
语法:``unalias``(选项)(参数)
选项:-a：取消所有命令别名。
参数:命令别名：指定要取消的命令别名。
```

Eg:

```
# alias ll
alias ll='ls -l --color=auto'
```

**携带参数：**

`alias cd='func() { cd $1; ls;}; func'`

eg

```
root@:~# cd /tmp
go-build052349483  go-build461530498  go-build672423576 
```



#### type

查询指令是否为 Bash shell 的内置命令： type

` type [-tpa] name`

不加任何选项与参数时，type 会显示出 name 是外部指令还是 bash 内置指令

* -t ：会将 name 以下面这些字眼显示出他的意义：
  file ：表示为外部指令；
  alias ：表示该指令为命令别名所设置的名称；
  builtin ：表示该指令为 bash 内置的指令功能；
* -p ：如果后面接的 name 为外部指令时，才会显示完整文件名；
* -a ：会由 PATH 变量定义的路径中，将所有含 name 的指令都列出来，包含 alias

```shell
[dmtsai@study ~]$ type ls
ls is aliased to `ls --color=auto' #未加任何参数，列出 ls 的最主要使用情况
[dmtsai@study ~]$ type -t ls
alias                              # 仅列出 ls 执行时的依据
[dmtsai@study ~]$ type -a ls
ls is aliased to `ls --color=auto' # 最先使用 aliase
ls is /usr/bin/ls                  # 还有找到外部指令在 /bin/ls

# 那么 cd 呢？
[dmtsai@study ~]$ type cd
cd is a shell builtin              # 看到了吗？ cd 是 shell 内置指令

# 自己写的sh
[root@bogon wangyu]# type apiup
apiup is /ng8w/bin/apiup
[root@bogon wangyu]# type -a apiup
apiup is /ng8w/bin/apiup
[root@bogon wangyu]# type -t apiup
file
[root@bogon wangyu]# type -p apiup
/ng8w/bin/apiup
```



#### 指令下达和快捷键

逃脱指令： `\[逃脱键]` ,  一般是 \回车， 用来多行输入， 注意其中没有空格。



| 组合键             | 功能                                                         |
| ------------------ | ------------------------------------------------------------ |
| ctrl + u /ctrl + k | 分别是从光标处向前删除指令串 （ctrl+u） 及向后删除指令串（）ctrl]+k） |
| ctril +a /ctrl + e | 分别是让光标移动到整个指令串的最前面 （ctrl+a） 或最后面（ctrl+e）。 |
| ctrl + r           | 搜索曾经输入过的命令。                                       |





#### ps1

```bash
hostname  #当前hostname
hostname aaa  # 更新hostname
退出终端，再重新连接
```





