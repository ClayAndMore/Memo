---
title: jjj
date: 2017-04-30 19:20:20
categories:
header-img:
tags:
---



### Tmux

下载：`apt-get install Tmux`

进入：`tmux`

此时下面有一条绿线，这时就说可以进入成功了。

Tmux 的配置文件 `~/.tmux.conf`

快捷键；`ctr+b` ，当按下这个快捷键时，就说明进入了tmux的快捷键，再按其他的键，可以实现相关功能。

#### 会话（session）

显示所有会话：按相应号码可进入相关会话

`ctrl-b s`

新建会话：

`ctrl-b new`

没有输入tmux前新建会话：

`tmux new -s <name-of-my-session>`



#### 窗口（wind）

显示所有窗口：

`ctrl-b w`

创建新窗口

`ctrl-b+c`

切换到下个窗口：

`ctrl-b+n`

切换到上个窗口：

`ctrl-b+p`

最后一个窗口：

`ctrl-b+l`

`c-b o `在小窗口中切换 这种方法一次只能切换一次,再想切换再c-b o,适合两个窗口的时候使用.如果在当前窗口分割了好多小窗口的话,就要用下面的两个指令了.

​     ` c-b (方向键)上` 上一个窗口

​     ` c-b (方向键)下` 下一个窗口  要指出的是,按一次c-b,可以上上下下的选,直到选到你想要的那个窗口,这点和c-b o不一样噢.

​      `c-b ! `关闭所有小窗口

​    ` c-b x` 关闭当前光标处的小窗口



给当前窗口改名：

`c-b ,`



退出窗口，从会话中断开，稍后可以重新连接：

`ctrl + d`

接入会话：

可以简单地输入 `tmux a` 命令，这样可以接入第一个可用的会话。

或者可以通过参数指定一个想接入的会话：

`$ tmux a -t session-name`



关闭会话：

要关闭会话的话，可以使用如下的命令，该命令和接入会话时所使用的命令很像：

`$ tmux kill-session -t session-name`

提示：关闭窗口时也可以使用类似的命令，只不过要把 kill-session 换成 kill-window。另外，还可以使用 tmux killall 同时关闭 tmux。



### 安装和配置git

先看有没有,命令：`git`

没有则安装：`apt-get install git`

配置：

`git config --global user.name "xxx" `

`git config --global user.email "你的邮箱"`

创建公钥：

`ssh-keygen -C 'youxiang' -t rsa .`

会在目录~/.ssh/下建立密钥文件，注意可能是隐藏的，用`ll`可以看到

将id_rsa.pub文件中的内容，复制到github你的新建公钥

测试连接：

`ssh -T git@git.com`

出现hello,你的名字，you've successfully....则说明成功。



### VIM

配置文件 ubuntu `/etc/vim/vimrc` 

普通模式：p 当前位置插入注释符号（偶然得知，不知道哪个插件）



### vundle

这是管理vim插件的工具，本身也是一款插件。

下载：`git clone https://github.com/VundleVim/Vundle.vim.git` 

配置，打开vimrc 配置文件。

输入：

```
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim //这里填你vundle的安装路径
call vundle#begin()

Plugin 'git://github.com/Yggdroot/indentLine.git'

call vundle#end()            " require
filetype plugin indent on    " required
```

begin和end里放入你要安装的插件。注意这里不是注释，要带上#begin()和#end()

这个插件一般github的 用户名/仓库名
尽量手打，防止出现Not an editor command: z.

and: ^M 你肯定复制人家配置了！而且从windows上传的！dos2unix咯....



进入vim:

安装插件：`:PluginInstall`

显示插件：`PluginList`



### NEATree

左侧文件树

在vundle中安装。

`Plugin 'scrooloose/nerdtree'`

安装后：vim 输入NERDTree 即可看到左侧有个文件目录。

NERDTree配置：在vimrc中加入：

```
map <F1> :NERDTreeToggle<CR>   "F1为打开NEATree的快捷键。
map <C-F1> :NERDTreeFind<CR>   "在右侧编辑时可以按，在左侧树目录找到当前文件
let NERDTreeChDirMode=2  "选中root即设置为当前目录
let NERDTreeQuitOnOpen=1 "打开文件时关闭树
let NERDTreeShowBookmarks=1 "显示书签
let NERDTreeMinimalUI=1 "不显示帮助面板
let NERDTreeDirArrows=1 "目录箭头 1 显示箭头  0传统+-|号
nnoremap <C-l> gt  "切换tab,修改快捷键，将原来的gt改为ctrl+l
nnoremap <C-h> gT
autocmd VimEnter * NERDTree 打开vim,默认开启nerdtree	
```

常用快捷键（在打开NerdTree时）：

ctrl+w+w,在左侧文件树和右侧之间来回切换

P 回到上层目录

p 回到根目录

X 合拢当前目录的父目录

x 合拢当前节点所有目录

t       在新 Tab 中打开选中文件/书签，并跳到新 Tab

T       在新 Tab 中打开选中文件/书签，但不跳到新 Tab

m 显示文件系统菜单（添加、删除、移动操作）





### TagList

跳转到类或函数定义区

安装方式：

1. 下载CTAGS: http://ctags.sourceforge.net/

2. 解压安装， configure, make

3. 下载Taglist: http://vim-taglist.sourceforge.net/installation.html

4. 解压得到两个文件： 

   ```
   plugin/taglist.vim - main taglist plugin file
   doc/taglist.txt    - documentation (help) file
   ```

5. 放入~/.vim下，：

   ```
   vim/plugin/taglist.vim 
   vim/doc/taglist.txt   
   ```

6. 在vimrc( 一般是在/etc下)中配置环境变量：

   `let Tlist_Ctags_Cmd='/home/wangyu/vim_plugin/ctags-5.8/ctags'`

7. 重启vim

8. 在vim中`:Tlista`  开启/关闭

9. 开启后ctrl + w 移动到list窗口，回车进入定义处。



### python-mode

命令一般都在vim下的命令模式下执行`:命令`

也在vim的配置文件中配置，

```
let g:pymode = 1    开启整个插件
let g:pymode_warnings = 1 关闭插件的警告
let g:pymode_options = 1 设置默认的选项
let g:pymode_options_max_line_length = 79  设置最长的长度
let g:pymode_python = 'python' 设置python版本，可选python，python3，disable,当设置为disable，插件失效
let g:pymode_indent = 1 设置PEP8风格，如果不符合，代码下将有下划线（波浪状）
let g:pymode_folding = 1  启用代码折叠
let g:pymode_motion = 1 支持代码间用vim的快捷键
let g:pymode_run = 1 支持代码运行，
let g:pymode_run_bind = '<leader>r' 代码运行快捷键
let g:python_lint = 1 开启代码检查，
命令输入： 
PymodeLint: 检查目前buffer中的代码
PymodeLintToggle: 代码检查的toggle
PymodeLintAuto: 自动修复PEP8的错误，在目前buffer中。

let g: pymode_rope_completion = 1  开启代码补全
let g: pymode_rope_completion_on_dot = 1 开启自动补全当按下句号
let g: pymode_rope_completion_bind = '<C-Space>'  自动补全的映射

# 找代码定义
let g: pymode_rope_goto_defiition_bind = '<C-c>g'  这里也是默认键 
```



### YouCompleteMe

相比其他自动补全插件，它的特别和强大之处是基于语义的自动补全。

确保vim 版本在7.2 以上，确保有python支持。可通过

`vim --version`

来看我们版本信息，其中有+python说明有python支持



用vundle安装：

`Plugin  'Valloric/YouCompleteMe'`

在～/.vim/bundle/,再进入 YouCompleteMe文件夹，需要进行编译：

但在次之前我们需要安装cmake:

`apt install cmake`

编译：

`./install.py`

这里可能它会提示安装包；

`git submodule update --init --recursive`

那就安吧，然后在编译。



### 补充：

* 文档中有提示快捷键`<header>`是`\'`意思。`<C-b>`一般是ctrl+b的意思。

  设置`<header>`:`let mapleader=";"`