### 环境

一个编译器，一个编辑器

#### linux

centos: `yum insatll gcc`

`gcc --version`

vim

ubuntu:



### hello world

```c
#include <stdio.h>

int main(int argc, char** argv) {
    puts("hello world1")；
    return 0;
}
```



 对代码进行编译和连接，并生成可执行文件

```
gcc hello.c -o hello.exe
```

   hello.c为源文件，-o 表示编译并链接，hello.exe为编译结果，可以自定义输出名



### 变量类型

| 类型名   | 描述                   | 举例                                    |
| -------- | ---------------------- | --------------------------------------- |
| `void`   | 空类型                 |                                         |
| `char`   | 单个的字符/字节        | `char last_initial = 'H';`              |
| `int`    | 整数                   | `int age = 32;`                         |
| `long`   | 可以表示更大的数的整数 | `long age_of_universe = 13798000000;`   |
| `float`  | 浮点数                 | `float liters_per_pint = 0.568f;`       |
| `double` | 精度更高的浮点数       | `double speed_of_swallow = 0.01072896;` |

 声明：

`int count = 10`



### 函数声明

```
int add_together(int x, int y) {
  int result = x + y;
  return result;
}
```

调用函数时，首先写上函数名，然后函数参数紧跟其后，包裹在一对圆括号里，参数之间用逗号分开。比如说，我们调用上面的函数，并将计算结果保存到 `added` 变量中：

```
int added = add_together(10, 18);
```





### 结构体声明

结构体用来声明一个新的类型。它可以将多个变量捆绑在一起。

我们可以使用结构体表示更加复杂的数据类型。例如，为了表示一个二维空间里的点，我们可以创建一个名为 `point` 的结构体将两个 `float` 类型的变量 `x`，`y` 绑在一起。我们可以同时使用 `struct` 和 `typedef` 来声明一个结构体：

```
typedef struct {
  float x;
  float y;
} point;
```

注意，我们应该将结构体放在所有用到它的函数的上方。这个类型和内建的基本数据类型的用法没有任何区别。获取结构体内部的变量时，需要使用小数点 `.`，后面紧跟要获取的变量名：

```
point p;
p.x = 0.1;
p.y = 10.0;

float length = sqrt(p.x * p.x + p.y * p.y);
```



### 指针

指针类型是普通类型的变体，只需普通类型的后面添加 `*` 后缀即可。比如，`int*` 就是一个 `int`类型的指针。在之前的 `main` 函数的输入参数列表中，我们还见过一个 `char**` 类型，这是一个 `char` 类型的指针的指针。 



### 字符串

在 C 语言中，字符串由 `char*` 类型表示。它是由一串字符(`char`)组成的，并以一个空终结字符结尾。字符串是 C 语言的一个重要且复杂的部分，我们会在接下来的几章中详细的学习它。

字符串还可以字面量来表示，将要表示的字符串包裹在双引号 `"` 中就可以了。比如说我们之前用过的 `"Hello, world!"` 。现在，你只需要记住，只要看到 `char*` 类型，就当成字符串来看待就可以了。



### 条件和循环

条件：

```
if (x > 10 && x < 100) {
  puts("x is greater than 10 and less than 100!");
} else {
  puts("x is less than 11 or greater than 99!");
}
```

循环：

```
int i = 10;
while (i > 0) {
  puts("Loop Iteration");
  i = i - 1;
}

for (int i = 0; i < 10; i++) {
  puts("Loop Iteration");
}
```



#### switch

```python
int main ()
{
   /* 局部变量定义 */
   char grade = 'B';
 
   switch(grade)
   {
   case 'A' :
      printf("很棒！\n" );
      break;
   case 'B' :              #注意这里 如是BC 输出内容一样， 或写成这样case 'B':case 'C':
   case 'C' :
      printf("做得好\n" );
      break;
   case 'D' :
      printf("您通过了\n" );
      break;
   case 'F' :
      printf("最好再试一下\n" );
      break;
   default :
      printf("无效的成绩\n" );
   }
   printf("您的成绩是 %c\n", grade );
 
   return 0;
}
```



### 枚举





### typedef

https://www.jianshu.com/p/740f87e97be1



### 交互

https://ksco.gitbooks.io/build-your-own-lisp/Interactive.html



#### 预处理器（preprocessor ）







