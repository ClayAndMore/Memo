Tags:[python]

## python编译 和 链接库



#### pyc, pyo, pyd

* pyc  是 py文件经过python 的 **编译器** 得到的 字节码(bytecode),  pyc文件通过python的**解释器**变成机器代码,去执行.

  生成方式：`python -m py_compile xxx.py`

* pyo文件,是python编译优化后的字节码文件, 这个优化没有多大作用,只是移除了断言。

  生成方式: `python -O -m py_compile xxxx.py `

* pyd 是动态链接库文件, 在windows上为dll,  linux下为so.  

  一般是其他语言写的python库, 多为c/c++综合而成的D语言. 比如select库.

pyc 和 pyo 对比py的速度比较:

**其实运行速度是不会改变的,只是加载速度会变快一点, import的时候会先找pyc**



### gcc 和 g++

g++ 和 gcc 都是编译器。

g++ 可以编译c++和c, gcc 只能调用c.

yum下的安装:

```
yum install gcc
yum install gcc-c++

安装时的错误：
No more mirrors to try 解决方法：
1.yum clean all
2.yum makecache
3.yum update
```



### 链接库

本质上来说库是一种可执行代码的二进制形式，可以被操作系统载入内存执行。库有两种：静态库（.a、.lib）和动态库（.so、.dll）

Window与Linux执行文件格式不同：

* 在Windows系统下的执行文件格式是PE格式，动态库需要一个**DllMain****函数做出初始化的入口，通常在导出函数的声明时需要有_declspec(dllexport)****关键字**。


* Linux下gcc编译的执行文件默认是ELF格式，**不需要初始化入口，亦不需要函数做特别的声明，**编写比较方便。

一个程序文件变成可执行程序过程：

```
源文件(.h, cpp等) -> 预编译 -> 编译 -> 汇编 -> 链接 -> 可执行文件
                                               ^
                                               |
                                               静态库（.a/.lib)
                                               动态库（.so/.dll)
```



#### 静态链接库

静态链接库：**在链接阶段，汇编生成的目标文件.o + 引用到的库一起链接打包到可执行文件中。因此对应的链接方式称为静态链接。**

特点：

* 静态库对函数库的链接是放在编译时期完成的。


* 程序在运行时与函数库再无瓜葛，移植方便。


* 浪费空间和资源，因为所有相关的目标文件与牵涉到的函数库被链接合成一个可执行文件。

形态：linux 下为.lilb ， windows下为.a

将.o 文件变成.a 文件：

Linux下使用**ar**工具、Windows下vs使用**lib.exe**，将目标文件压缩到一起，并且对其进行编号和索引，以便于查找和检索。

大一点的项目会编写makefile文件（CMake等等工程管理工具）来生成静态库，输入多个命令太麻烦了。





#### 动态链接库

因为静态库的一些缺点，我们使用了静态库：

* 空间浪费是静态库的一个问题：

  静态库在内存中存在多分拷贝，一个程序用一个静态库的话，2000个这样的程序将用2000个这样的静态库。

* 另一个问题是静态库对程序的更新、部署和发布页会带来麻烦。如果静态库liba.lib更新了，所以使用它的应用程序都需要重新编译、发布给用户。



**动态库在程序编译时并不会被连接到目标代码中，而是在程序运行是才被载入**

不同的应用程序如果调用相同的库，那么在内存里只需要有一份该共享库的实例。

动态库在程序运行是才被载入，也解决了静态库对程序的更新、部署和发布页会带来麻烦。用户只需要更新动态库即可。





#### python调用c的so库

现在,我们首先生成.so文件

首先, 我们写一个a.c文件;

```c
#include <stdio.h>
 
void show() {
    printf("this is a test\n");
}
 
int add(int a, int b) {
    return a + b;
}
```



``gcc a.c -fPIC -shared -o a.so`

 在当前目录下会产生一个a.so文件

其中 -fPIC是position independent code(位置无关代码)的意思

-shared是产生一个可以与其他对象连接来形成一个可执行文件的共享对象的一个参数

python 调用：

```python
from ctypes import cdll
 
cur = cdll.LoadLibrary('./a.so')
 
cur.show()
 
print cur.add(1, 2)

======= output
this is a test
3
```





##### 查看依赖库的共享库：

ldd



#### 总结

二者的不同点在于**代码被载入的时刻不同**。

* 静态库在程序编译时会被连接到目标代码中，程序运行时将不再需要该静态库，**因此体积较大**。
* 动态库在程序编译时并不会被连接到目标代码中，而是在程序运行是才被载入，因此在程序运行时还需要动态库存在，**因此代码体积较小**

