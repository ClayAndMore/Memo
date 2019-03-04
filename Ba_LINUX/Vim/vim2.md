Tags:[linux, vim]

### 打开其他文件

`:E`

**你可以用 j, k 键上下移动，然后回车，进入一个目录，或是找开一个文件** 

- 【 – 】 到上级目录
- 【D】删除文件（大写）
- 【R】改文件名（大写）
- 【s】对文件排序（小写）
- 【x】执行文件



#### gf命令

打开光标处所指的文件 ， 当然是当前目录能找到的。



#### 缓冲区

` :ls`， 会看到当前缓冲区里的文件（如上述打开的文件）

切换：

```
:buffer 2 打开2号文件
:bnext      缩写 :bn
:bprevious   缩写 :bp
:blast  缩写 :bl
:bfirst 缩写 :bf
```



### 窗口分屏

当前窗口上下分屏：

```
:He   全称为 :Hexplore  （在下边分屏浏览目录, 并打开令一个文件）
:He!  （在上分屏浏览目录）
```

当前窗口左右分屏：

`:Ve 全称为 :Vexplore （在左边分屏间浏览目录，要在右边则是 :Ve! `



切换分屏：

**先按Ctrl + W，然后按方向键：h j k l** 



#### 分屏同步移动

要让两个分屏中的文件同步移动，很简单，你需要到需要同步移动的两个屏中都输入如下命令（相当于使用“铁锁连环”）：

> **:set scb**

如果你需要解开，那么就输入下面的命令：

> **:set scb!**

注：set scb 是 set scrollbind 的简写。



#### 保存会话

如果你用Tab或Window打开了好些文件的文件，还设置了各种滚屏同步，或是行号……，那么，你可以用下面的命令来保存会话：（你有兴趣你可以看看你的 mysession.vim文件内容，也就是一个批处理文件）

> **:mksession ~/.mysession.vim**

如果文件重复，vim默认会报错，如果你想强行写入的话，你可以在mksession后加! ：

> **:mksession! ~/.mysession.vim**

于是下次，你可以这样打开这个会话：

> **vim -S ~/.mysession.vim**

保存完会话后，你也没有必要一个一个Tab/Windows的去Close。你可以简单地使用：

> **:qa   – 退出全部** 
>
> **:wqa  -保存全部并退出全**