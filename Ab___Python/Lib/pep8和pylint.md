Tags:[python, py_lib]

## PEP 8

Python社区则利用他们的无穷智慧，提出了编写Python代码的PEP 8[③](https://www.kancloud.cn/epubit/python3/301709#anchor13)（[http://www. python.org/dev/peps/pep-0008/](http://www.python.org/dev/peps/pep-0008/)）标准。这些规范可以归纳成下面的内容。

- 每个缩进层级使用4个空格。

- 每行最多79个字符。

- 顶层的函数或类的定义之间空两行。

- 采用ASCII或UTF-8编码文件。

- 在文件顶端，注释和文档说明之下，每行每条`import`语句只导入一个模块，

  **同时要按标准库、第三方库和本地库的导入顺序进行分组。**

- 在小括号、中括号、大括号之间或者逗号之前没有额外的空格。

- 类的命名采用骆驼命名法，如`CamelCase`；

  异常的定义使用`Error`前缀（如适用的话）；

  函数的命名使用下划线分隔的小写字母，如`separated_by_underscores`；

  用下划线开头定义私有的属性或方法，如`_private`。

这些规范其实很容易遵守，而且实际上很合理。大部分程序员在按照这些规范写代码时并没有什么不便。





## Pylint

Pylint 是一个 Python 代码分析工具，它分析 Python 代码中的错误，查找不符合PEP8的代码风格标准和有潜在问题的代码。

安装：`pip install pylint`



### 调用

`pylint [options] module_or_package_pyfile`

- 进入这个模块所在的文件夹，运行 `pylint [options] module.py`
  这种调用方式是一直可以工作的，因为当前的工作目录会被自动加入 Python 的路径中。
-  不进入模块所在的文件夹，运行 `pylint [options] directory/module.py`
  这种调用方式当如下条件满足的时候是可以工作的：directory 是个 Python 包 ( 比如包含一个 __init__.py 文件 )，或者 directory 被加入了 Python 的路径中。
- 进入这个包所在文件夹，运行 `pylint [options] pakage。`
  这种调用方式是一直可以工作的，因为当前的工作目录会被自动加入 Python 的路径中。



eg:

下面是一段毫无意义的程序style.py，有一个bug和风格规范问题：

```python
a = 1
b = 2
print a
print b
print c
```

下面是pylint输出的内容：

```
$ pylint style.pyNo config file found, using default configuration************* Module style
C:  5, 0: Final newline missing (missing-final-newline)
C:  1, 0: Missing module docstring (missing-docstring)
C:  1, 0: Invalid constant name "a" (invalid-name)
C:  2, 0: Invalid constant name "b" (invalid-name)
E:  5, 6: Undefined variable 'c' (undefined-variable) 
------------------------------------
Your code has been rated at -8.00/10
```

* MESSAGE_TYPE 有如下几种：

  (C) convention,惯例。违反了编码风格标准

  (R) refactor,重构。写得非常糟糕的代码。

  (W) warning,警告。某些 Python 特定的问题。

  (E) error, 错误。很可能是代码中的错误。

  (F) fatal 致命错误。阻止 Pylint 进一步运行的错误。

* 5,6 5,0 等表示所在文件中的行号和列号。
* 上面内容的最后一行是我们的分数：-8.00（最高为 10.0）

改进：

```python
# -*- coding: UTF-8 -*-
 
'''这里是模块文档字符串'''
 
def func():
    '''函数的文档字符串在这里。妈妈我在这儿！'''
    first = 1
    second = 2
    third = 3
    print first
    print second
    print third
 
func()

```

调用：

```
$ pylint style.py
No config file found, using default configuration
 
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: -8.00/10, +18.00)
```

在代码开头添加了文档，起了更有意义的变量名， 最后一行还会比较上次的结果



### 常用命令行参数

#### 配置文件

- `-h``,``--help`显示所有帮助信息。

- `--persistent=<y_or_n>` Pickle collected data for later comparisons. [current: yes], 简单理解收集数据用于比较

- `--generate-rcfile`可以使用 pylint –generate-rcfile 来生成一个配置文件示例。

  可以使用重定向把这个配置文件保存下来用做以后使用。

  也可以在前面加上其它选项，使这些选项的值被包含在这个产生的配置文件里。

  如：`pylint --persistent=n --generate-rcfile > pylint.conf`，查看 pylint.conf，可以看到 persistent=no，而不再是其默认值 yes。

- `--rcfile=<file>`指定一个配置文件。把使用的配置放在配置文件中，这样不仅规范了自己代码，也可以方便地和别人共享这些规范。

#### 输出格式

- `-i <y_or_n>, --include-ids=<y_or_n>`在输出中包含 message 的 id, 有些版本没有

-  `--help-msg=<msg-id>`来查看这个错误的详细信息，这样可以具体地定位错误。

- ` -d <msg ids>, --disable=<msg ids>` ， 过滤掉某些输出。

- `-r <y_or_n>, --reports=<y_or_n>`默认是 y, 表示 Pylint 的输出中除了包含源代码分析部分，也包含报告部分。

  有些版本默认是yes

- `--msg-template` ,  输出格式， eg:

  `pylint --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}({symbol})'`



#### 输出形式

- `--files-output=<y_or_n>`将每个 module /package 的 message 输出到一个以 pylint_module/package. [txt|html] 命名的文件中，如果有 report 的话，输出到名为 pylint_global.[txt|html] 的文件中。默认是输出到屏幕上不输出到文件里。
- `-f <format>, --output-format=<format>`设置输出格式。可以选择的格式有 text, parseable, colorized, msvs (visual studio) 和 html, 默认的输出格式是 text。
- `--disable-msg=<msg ids>`禁止指定 id 的 message. 比如说输出中包含了 W0402 这个 warning 的 message, 如果不希望它在输出中出现，可以使用 `--disable-msg= W0402`



#### 配置文件添加项

```
[REPORTS]

# Template used to display messages. This is a python new-style format string
# used to format the message information. See doc for all details
msg-template='{msg_id}:{line:3d},{column}:{obj}:{msg}({symbol})'


[MISCELLANEOUS]

# List of note tags to take in consideration, separated by a comma.
notes=FIXME,
      XXX
#TODO   # 去掉TODO,如果有需要的话


```



#### hook

```
[Master]
init-hook='sys.path = ["/path/myapps/bin/", "/path/to/myapps/lib/python3.3/site-packages/", ... many paths here])'

or

[Master]
init-hook='sys.path = list(); sys.path.append("/path/to/foo")
```



当在代码中换环境导包时， 可以忽略：

```python
import sys

sys.path.insert(0, './bar')

#pylint: disable=wrong-import-position

from bar.eggs import Eggs
from foo.ham import Ham

#pylint: enable=wrong-import-position

Ham()

# Still caught
import something_else
```





#### 常见id

* C0103:  

  ```
  *%s name "%s" doesn't conform to %s*
  eg： 
  Constant name "Shift" doesn't conform to UPPER_CASE naming style # 常量没有全部大写
  ```

* C0111:Missing function docstring(missing-docstring)，  函数没有写注释。

* C0121: should be 'expr is None'(singleton-comparison），不是==None, 而是is None

* C0301:Line too long， 一行太长

* C0303： trailing-whitespace， 多空行

* C0326: Exactly one space required after comma，逗号后期望空格

* C0330:Wrong continued indentation ， 不规范的缩进, 或括回没有和括号在一条竖线上

* C0413:  should be placed at the top of the module(wrong-import-position), 在导入之前有语句，见上方hook部分。

* C1801：Do not use `len(SEQUENCE)` to determine if a sequence is empty(len-as-condition)， 不要使用len(0) 做判断

* C1001: Old-style class defined.(old-style-class)

  ```python
  class NewStyleClass(object):
      pass
  
  class AnotherNewStyleClass(NewStyleClass):
      pass
     
  # Old-style classes don't.
  class OldStyleClass():
      pass
  ```

  

* R0912:Too many branches (18/12)(too-many-branches)  太多if判断

* R914:Too many local variables (20/15)(too-many-locals) 函数太多变量

* R0915:Too many statements (54/50)(too-many-statements)  函数太长

* R1702:Too many nested blocks (6/5)(too-many-nested-blocks) 函数里太多嵌套

* R1701:832,11:Consider merging these isinstance calls to isinstance(which, (str, unicode))(consider-merging-isinstance)：可以合并的语句

  eg:

  ```
  if isinstance(which,str) or isinstance(which,unicode): 
  -> 
  if  isinstance(which, (str, unicode)):
  ```

* R1702:Too many nested blocks (6/5)(too-many-nested-blocks)， 太多的缩进块

* R1710: (inconsistent-return-statements, 应该返回同一个类型，return值的类型应该是相同的。

* W0511， fixme:

  注释中的TODO会引发。

* W0603: 使用了global全局变量，最好避免

* W0612:Unused variable 'e'(unused-variable) , 没有使用的变量

* W0613:unused-argument, 声明了参数没有使用
* W0621: redefined-outer-name， 函数内部定义了和外部一样的名字
* W0622: Redefining built-in 'hash'(redefined-builtin), 起了和内部变量一样的名字
* W0702: bare-except, 没有具体的捕获异常，而是捕获所有异常。
* W0703：Catching too general exception Exception(broad-except) 和上类似
* E0401: 25,0::Unable to import (import-error) ， 不能导入某模块。





建议忽略的ID: C0103,C0303, C0111, W0702, W0703，C1801