Tags:[linux, shell]

#### 开始

在文件头部：`#!` 

这个符号组合告诉系统 该后面的参数来执行该文件.。如：`#!/bin/sh` 或`#!/bin/bash` 

上述位置其实把路径写死了没有通用性，合理写法：

`#!/usr/bin/env bash`

记得该文件的权限要改成可执行。

`chmod +x file`

几点注意：

* 自上而下，自左到右执行。
* 空白行，空白，tab会被忽略掉
* 如果督导一个回车符号（CR），尝试执行改行命令，一行写不下可以用`\Enter` 来扩展下一下行



在shell脚本中可以使用下面三类命令：

* Unix命令
* 管道
* 控制流程（if)




#### 输入输出

输出： echo

输入：read

打印变量内容：

` echo "A is "  echo $a`

`num=2 echo "this is the ${num}nd"`

可用printf 实现更强大的输出功能。



#### 变量

1. 在shell编程中，所有的变量用字符串组成，不需要声明：变量=值 

   `nyname=Bird`  

   等号两边不能有空格，变量开头不能为数字。

2. 取出变量：  `$变量名`  

   `$` 也是个变量，代表shell的pid, eg:`echo $$`  

   ? 是上个变量的回传码，执行成功为零，失败非零，为错误代码。eg:`echo $?`

3. 若有空格用引号，但是：

   双引号可以保有特殊符号原有的特性

   单引号只是输出的纯文本

4. 显示命令执行结果 `echo 'date'`  这里用的是反引号。 out: Thu Jul 24 10:08:46 CST 2014

   或者使用`$(命令)` ，反引号或括号命令将先被执行 

5. 增加变量内容 ：`"$变量名称"累加内容`  或 `${变量名称}累加内容`

   eg: `PATH="$PATH":/home/bin`

6. 反斜杠转义特殊符号

7. export 自定义变量变为环境变量，所有的程序，包括shell启动的程序，都能访问环境变量。

8. 只读变量 readonly , 只读的将不会改变。

9. 删除变量 unset ,  unset variable_name,不能删只读变量

10. 声明变量，declare/typeset 声明变量的类型，后可跟参数

  ```
  sum=100+20 echo $sum
  declare -i sum=100+20 
  echo $sum
  120
  ```


  -a 声明为数组，-i声明为整型，-x 用法和export 一样将variable 变成环境变量，-r,设置成为readonly类型。

  如果不指定，则默认为一个字符串。




#### 字符串

字符串可以单引号，双引号，或者不用引号。双引号里可以有变量。

拼接字符串： `A is $a` ,或者 `A is ${a}`

字符串的拼接：





#### 注释

以#开头。



#### 数组

只支持一维数组，用括号来表示，用空格来分割：

`array=(a b "c" d)`

或array[0]=a，array[1]=b 等

读取数组：`${array_name[index]}`

 获取所有数组：使用`*`和`@`

```
echo "数组的元素为: ${my_array[*]}"
echo "数组的元素为: ${my_array[@]}"
```

获取长度：

`echo "数组元素个数为: ${#my_array[@]}"`

eg: 把ls存到一个数组变量中。

```shell
# 将ls的输出存到filelist数组中：
c=0
for file in `ls`
do
  filelist[$c]=$file
  ((c++))
done

# 或者

set -a myfiles
index=0
for f in `ls`; do myfiles[index]=$f; let index=index+1; done
# 注：用这种方法，如果文件名中有空格的话，会将一个文件名以空格为分隔符分成多个存到数组中，最后出来的结果就是错误的。

# 以下代码，这种赋值方法可以使获取到的文件名正确。
c=0
for file in *
do
  filelist[$c]="$file" # （为了准确起见，此处要加上双引号“”）
  ((c++))
done

#把filelist数组内容输出到屏幕上：
b=0
while [ $b -lt $c ]
do
  echo ${filelist[$b]}
  ((b++))
done
# 或者
b=0
for value in ${filelist[*]}
do 
  echo $value
done


# 在屏幕上输出filelist数组长度：
echo ${#filelist[*]}
```





#### 参数传递

在用脚本的时候会在脚本名后面跟上相应的参数

```shell
echo "Shell 传递参数实例！";
echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";

执行的文件名：./test.sh
第一个参数为：1
第二个参数为：2
第三个参数为：3
```

| 参数处理                                     | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| $#                                       | 传递到脚本的参数个数                               |
| $*   | 以一个单字符串显示所有向脚本传递的参数。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。 |                                          |
| $$                                       | 脚本运行的当前进程ID号                             |
| $!                                       | 后台运行的最后一个进程的ID号                          |
| $@   | 与$*相同，但是使用时加引号，并在引号中返回每个参数。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。 |                                          |
| $-                                       | 显示Shell使用的当前选项，与[set命令](http://www.runoob.com/linux/linux-comm-set.html)功能相同。 |
| $?                                       | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。          |

`echo "传递的参数作为一个字符串显示：$*";`

```
传递的参数作为一个字符串显示：1 2 3
```

`$* 与 $@ 区别：`

只有在双引号中体现出来。假设在脚本运行时写了三个参数 1、2、3，，则 " * " 等价于 "1 2 3"（传递了一个参数），而 "@" 等价于 "1" "2" "3"（传递了三个参数）。



#### 运算

原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 awk 和 expr，expr 最常用。

expr 是一款表达式计算工具，使用它能完成表达式的求值操作。

例如，两个数相加(**注意使用的是反引号 ` 而不是单引号 '**)：

```
#!/bin/bash

val=`expr 2 + 2`
echo "两数之和为 : $val"
```



布尔运算符

| 运算符  | 说明                                 | 举例                                    |
| ---- | ---------------------------------- | ------------------------------------- |
| !    | 非运算，表达式为 true 则返回 false，否则返回 true。 | [ ! false ] 返回 true。                  |
| -o   | 或运算，有一个表达式为 true 则返回 true。         | [ $a -lt 20 -o $b -gt 100 ] 返回 true。  |
| -a   | 与运算，两个表达式都为 true 才返回 true。         | [ $a -lt 20 -a $b -gt 100 ] 返回 false。 |



逻辑运算符： && 和 ||



字符串运算符：

| 运算符  | 说明                      | 举例                    |
| ---- | ----------------------- | --------------------- |
| =    | 检测两个字符串是否相等，相等返回 true。  | [ $a = $b ] 返回 false。 |
| !=   | 检测两个字符串是否相等，不相等返回 true。 | [ $a != $b ] 返回 true。 |
| -z   | 检测字符串长度是否为0，为0返回 true。  | [ -z $a ] 返回 false。   |
| -n   | 检测字符串长度是否为0，不为0返回 true。 | [ -n $a ] 返回 true。    |
| str  | 检测字符串是否为空，不为空返回 true。   | [ $a ] 返回 true。       |



**文件测试运算符** ：

| -b file | 检测文件是否是块设备文件，如果是，则返回 true。               | [ -b $file ] 返回 false。 |
| ------- | ---------------------------------------- | ---------------------- |
| -c file | 检测文件是否是字符设备文件，如果是，则返回 true。              | [ -c $file ] 返回 false。 |
| -d file | 检测文件是否是目录，如果是，则返回 true。                  | [ -d $file ] 返回 false。 |
| -f file | 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 | [ -f $file ] 返回 true。  |
| -g file | 检测文件是否设置了 SGID 位，如果是，则返回 true。           | [ -g $file ] 返回 false。 |
| -k file | 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。   | [ -k $file ] 返回 false。 |
| -p file | 检测文件是否是有名管道，如果是，则返回 true。                | [ -p $file ] 返回 false。 |
| -u file | 检测文件是否设置了 SUID 位，如果是，则返回 true。           | [ -u $file ] 返回 false。 |
| -r file | 检测文件是否可读，如果是，则返回 true。                   | [ -r $file ] 返回 true。  |
| -w file | 检测文件是否可写，如果是，则返回 true。                   | [ -w $file ] 返回 true。  |
| -x file | 检测文件是否可执行，如果是，则返回 true。                  | [ -x $file ] 返回 true。  |
| -s file | 检测文件是否为空（文件大小是否大于0），不为空返回 true。          | [ -s $file ] 返回 true。  |
| -e file | 检测文件（包括目录）是否存在，如果是，则返回 true。             | [ -e $file ] 返回 true。  |





#### 函数

函数和js定义的一样，不过可以省略function.

在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...

函数定义注意函数名左右的空格：

```shell
function show() {
  $1 #第一个参数
}
```

调用和传参， 注意没有括号：

```
show 'a'
```





#### 输入输出重定向

输出重定向：

`command1 > file1` 

上面这个命令执行command1然后将输出的内容存入file1。eg:

`echo "It is a test" > myfile`

注意任何file1内的已经存在的内容将被新内容替代。如果要将新内容添加在文件末尾，请使用>>操作符。



输入重定向：

`command1 < file1`

原本要从键盘的输入现在会从文件中读取。



linux命令运行时，会打开三个文件：

- 标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
- 标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
- 标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。

所以重定向可以这样代替：`$ command 2 > file`



不想再屏幕上看到输出结果：

`$ command > /dev/null`

/dev/null 是一个特殊的文件，写入到它的内容都会被丢弃；如果尝试从该文件读取内容，那么什么也读不到。但是 /dev/null 文件非常有用，将命令的输出重定向到它，会起到"禁止输出"的效果。



#### 文件包含

创建两个 shell 脚本文件。

test1.sh 代码如下：

```
#!/bin/bash
url="http://www.hahaha.com"
```

test2.sh 代码如下：

```
#!/bin/bash

# 使用以下包含文件代码
# source ./test1.sh

echo "地址：$url"
```

接下来，我们为 test2.sh 添加可执行权限并执行：

```
$ chmod +x test2.sh 
$ ./test2.sh 
菜鸟教程官网地址：http://www.hahaha.com
```

> **注：**被包含的文件 test1.sh 不需要可执行权限。





#### 调试和检错 set

set 是值当前的shell 环境变量，sh + 脚本会启动一个信的shell环境，我们可以用set 来指定shell脚本的环境参数。

* set -u   如遇到不存在的变量报错， 原本是shell会直接跳过

* set -x    输出内容前，说明是什么语句输出：

  ```
  #!/usr/bin/env bash
  set -x

  echo bar
  ```

  输出：

  ```
  $ bash script.sh
  + echo bar
  bar
  ```

* set -e  只要脚本发生错误就终止运行，默认是跳过继续运行。

  `set -e`根据返回值来判断，一个命令是否运行失败。但是，某些命令的非零返回值可能不表示失败，或者开发者希望在命令失败的情况下，脚本继续执行下去。这时可以暂时关闭`set -e`，该命令执行结束后，再重新打开`set -e`。

   ```
   set +e
   command1
   command2
   set -e
   ```

  上面代码中，`set +e`表示关闭`-e`选项，`set -e`表示重新打开`-e`选项。

  还有一种方法是使用`command || true`，使得该命令即使执行失败，脚本也不会终止执行。

   ```
   #!/bin/bash
   set -e

   foo || true
   echo bar

   ```

  上面代码中，`true`使得这一行语句总是会执行成功，后面的`echo bar`会执行。

* set -o pipefail  管道的子命令失败，整个脚本就失败




上面这四个命令一般放在一起用：

`set`命令的上面这四个参数，一般都放在一起使用。

 ```
 # 写法一
 set -euxo pipefail

 # 写法二
 set -eux> set -o pipefail

 ```

这两种写法建议放在所有 Bash 脚本的头部。

另一种办法是在执行 Bash 脚本的时候，从命令行传入这些参数。

 ```
 $ bash -euxo pipefail script.sh
 ```



#### 自动输入密码 | EOF

两种方式：

1. 使用管道，上一个命令的 stdout 接到下一个命令的 stdin：

   ```
   echo password | sudo -S apt-get update
   ```

2. 使用文本重定向：

   ``` sh
   #!/bin/bash
   sudo -S apt-get update << EOF 
   你的密码
   EOF
   ```

   在shell脚本中，通常将EOF与 << 结合使用，表示后续的输入作为子命令或子Shell的输入，直到遇到EOF为止，再返回到主Shell,即将‘你的密码’当做命令的输入




#### 通过脚本学习到的linux命令



##### shift

通常用于参数左移，比如第一个参数左移，原本位于第二个位置的参数就变成了第一个参数



##### shopt——set

set命令可以设置shell可以使用的命令，

set -o 看当前的设置。

set -o 选项， 打开当前选项

set +0 选项，关闭当前选项

shopt 是set的升级版，可以使用更多的命令

shopt  看当前的设置。

shopt -s 选项， 打开当前选项

shopt -u 选项，关闭当前选项



##### extglob  模糊匹配



##### readlink

readlink -f 找到文件的真正链接文件，是不是链接文件都会返回一个真正能执行的目录：

`readlink -f docker/build_image.sh`   

输出：/home/wy/docker /build_image.sh



##### dirname ： 会获得文件的目录路径：

`dirname /home/wy/docker /build_image.sh`

会输出：/home/wy/docker



##### exec





#### 其他或问题

##### declare

ubuntu系统可能出现declare:not found的问题，命令：`sudo dpkg-reconfigure dash` 选择NO.



##### unexpected end of file

有可能是把if 的结尾 fi 写反。

或者不是set ff = unxi



##### linux命令执行返回值

上一条命令的返回值： `echo $？`

返回值为零代表执行成功，其他则失败： 

那么如果返回的值不是 0，我们要怎么知道是那里出错了呢？ 大多数的程序出错都会给出提示，如果没有提示的话，可以用 **perror** 这个程序来查看错误的信息，比如返回值是 2，我们可以运行：

```
$ perror 2
OS error code   2:  No such file or directory
```

