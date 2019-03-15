tags: [python, py_lib] date: 2017-02-20 


### 写在前面

pdb 是 python 自带的一个包，为 python 程序提供了一种交互的源代码调试功能，主要特性包括设置断点、单步调试、进入函数调试、查看当前代码、查看栈片段、动态改变变量的值等。pdb 提供了一些常用的调试命令，详情见表 

| 命令             | 解释              |
| -------------- | --------------- |
| break 或 b 设置断点 | 设置断点            |
| continue 或 c   | 继续执行程序，一直跑到下个断点 |
| list 或 l       | 查看当前行的代码段       |
| step 或 s       | 进入函数            |
| return 或 r     | 执行代码直到从当前函数返回   |
| exit 或 q       | 中止并退出           |
| next 或 n       | 执行下一行           |
| p              | 打印变量的值          |
| help           | 帮助              |

### 基本用法

一个python文件：pdbtest.py:

```python
import pdb

a='aaa'
pdb.set_trace()
b='bbb'
c='ccc'
final=a+b+c
print(final)
```

执行：python pdbtest.py。

out:

```
> d:\workspace\pyworkspace\follow\pdbtest.py(5)<module>()
-> b='bbb'
```

说明在这个文件的第五行代码`b= bbb `处停下，但是是这句代码的上面，这句话并没有执行。

这时你的光标会停在（pdb）后面，输入上方表格指令，可实现相关操作。比如我输入：

`(pdb)n`按下回车就会执行`b=bbb`这条语句。

other:再按下回车会执行上面一样的语句。

#### 打印变量

`(pdb)p final`

则会输出最后final的值

#### 看当前代码所调试在的位置

`(pdb)l` 

out:

```
  1     import pdb
  2
  3     a='aaa'
  4     pdb.set_trace()
  5  -> b='bbb'
  6     c='ccc'
  7     final=a+b+c
  8     print(final)
[EOF]
```

箭头所指向的位置就是当前调试的位置。

#### 进入函数

输入n会直接执行函数的不会进入函数内部，在调试有函数语句的地方直接输入s,可进入函数进行单步调试。再按r退出函数



#### 调试中改变变量的值

```
(VirtualEnv16Y12M) D:\WorkSpace\pyWorkSpace\Follow>python pd
btest.py
> d:\workspace\pyworkspace\follow\pdbtest.py(5)<module>()
-> b='bbb'
(Pdb) !b='zzz'
(Pdb) p b
'zzz'
(Pdb) n
> d:\workspace\pyworkspace\follow\pdbtest.py(6)<module>()
-> c='ccc'
(Pdb) p b
'bbb'
(Pdb) !b='vvv'
(Pdb) p b
'vvv'
(Pdb) c
aaavvvccc

```

`!变量名`可以改变调试的变量值，上面的示例是在b=bbb语句前就改变了变量值这样会被原语句赋值回来，所以我们要执行到断点在c=ccc处再对b赋值。