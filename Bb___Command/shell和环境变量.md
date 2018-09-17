### shell

Shell 是指“提供给使用者使用界面”的软件（命令解析器），类似于 DOS 下的 command（命令行）和后来的 cmd.exe。普通意义上的 Shell 就是可以接受用户输入命令的程序。它之所以被称作 Shell 是因为它隐藏了操作系统底层的细节。同样的 Unix/Linux 下的图形用户界面 GNOME 和 KDE，有时也被叫做“虚拟 shell”或“图形 shell”。

shell简而言之就是一个与系统内核交互的壳。

在 UNIX/Linux 中比较流行的常见的 Shell 有 bash，zsh，ksh，csh 等等，Ubuntu 终端默认使用的是 bash，（我们可以去/bin/ 下看一下。）

bash 兼容了sh，是它的加强版本。

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
source命令也称为“[点命令](http://www.51testing.com/?uid-225738-action-viewspace-itemid-206878)”，也就是一个点符号（.）,是bash的内部命令。
功能：使[Shell](http://www.51testing.com/?uid-225738-action-viewspace-itemid-206878)读入指定的Shell程序文件并依次执行文件中的所有语句
source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。
用法：
`source filename 或 . filename`
source命令(从 C Shell 而来)是bash shell的内置命令;点命令(.)，就是个点符号(从Bourne Shell而来)是source的另一名称。

source filename 与 sh filename 及./filename执行脚本的区别在那里呢？
1.当shell脚本具有可执行权限时，用sh filename与./filename执行脚本是没有区别得。./filename是因为当前目录没有在PATH中，所有"."是用来表示当前目录的。
2.sh filename 重新建立一个子shell，在子shell中执行脚本里面的语句，该子shell继承父shell的环境变量，但子shell新建的、改变的变量不会被带回父shell，除非使用export。
3.source filename：这个命令其实只是简单地读取脚本里面的语句依次在当前shell里面执行，没有建立新的子shell。那么脚本里面所有新建、改变变量的语句都会保存在当前shell里面。
