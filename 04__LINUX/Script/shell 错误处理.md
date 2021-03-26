

## 调试和检错 set

set 是值当前的shell 环境变量，sh + 脚本会启动一个信的shell环境，我们可以用set 来指定shell脚本的环境参数。



### set -u

如遇到不存在的变量报错， 原本是shell会直接跳过， 等同于 set -o nounset



### set -x 

 输出内容前，说明是什么语句输出：

```sh
#!/usr/bin/env bash
set -x

echo bar
```

输出：

```sh
$ bash script.sh
+ echo bar
bar
```



### set -e 

只要脚本发生错误就终止运行，默认是跳过继续运行，等同于set -o errexit

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

上面代码中，foo是个未声明的错误语句， `true`使得这一行语句总是会执行成功，后面的`echo bar`会执行。



### set -o pipefail  

`set -o pipefail`用来解决上面这种情况，只要一个子命令失败，整个管道命令就失败，脚本就会终止执行。

```bash
 #!/usr/bin/env bash
 set -eo pipefail
 
 foo | echo a
 echo bar
```

运行后，结果如下。

```bash
 $ bash script.sh
 a
 script.sh:行4: foo: 未找到命令
```






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

