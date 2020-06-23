---
title: "c.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: ["c"]
author: "Claymore"

---


### hello world

```c
#include <stdio.h>

int main(int argc, char** argv) {
    puts("hello world")；
    return 0;
}
```



 对代码进行编译和连接，并生成可执行文件

```
gcc hello.c -o hello.exe
```

   hello.c为源文件，-o 表示编译并链接，hello.exe为编译结果，可以自定义输出名



### 预处理指令

`#include <stdio.h>`

符号 # 表示这是一个预处理指令，告诉编译器在编译源代码之前，要先执行一些操作。编译器在编译过程开始之前的预处理阶段会处理这些指令。预处理指令的类型相当多，大多放于程序源文件的开头。

编译器要将 stdio.h 文件的内容包含进来，这个文件被称为头文件，因为通常放在程序的开头处。

stdio 是`standard input & output`的缩写，包含了编译器理解 printf() 以及其它输入 / 输出函数所需要的信息。C 语言所有头文件的扩展名都是 .h



### 注释


// 单行注释

**/\* ... */** 用于注释说明

```
/* 
 多行注释
 多行注释
 多行注释
 */
```



### 数据类型

它们也是算术类型，被用来定义在程序中只能赋予其一定的离散整数值的变量。

#### 基本类型

它们是算术类型，包括两种类型：整数类型和浮点类型

| 类型名   | 描述                   | 举例                                    |
| -------- | ---------------------- | --------------------------------------- |
| `char`   | 单个的字符/字节        | `char last_initial = 'H';`              |
| `int`    | 整数                   | `int age = 32;`                         |
| `long`   | 可以表示更大的数的整数 | `long age_of_universe = 13798000000;`   |
| `float`  | 浮点数                 | `float liters_per_pint = 0.568f;`       |
| `double` | 精度更高的浮点数       | `double speed_of_swallow = 0.01072896;` |



#### 枚举类型



#### void类型

类型说明符 *void* 表明没有可用的值。

| 序号 | 类型与描述                                                   |
| ---- | ------------------------------------------------------------ |
| 1    | **函数返回为空** C 中有各种函数都不返回值，或者您可以说它们返回空。不返回值的函数的返回类型为空。例如 **void exit (int status);** |
| 2    | **函数参数为空** C 中有各种函数不接受任何参数。不带参数的函数可以接受一个 void。例如 **int rand(void);** |
| 3    | **指针指向 void** 类型为 void * 的指针代表对象的地址，而不是类型。例如，内存分配函数 **void \*malloc( size_t size );** 返回指向 void 的指针，可以转换为任何数据类型。 |



#### 派生类型

它们包括：指针类型、数组类型、结构类型、共用体类型和函数类型。



### 变量声明

变量的声明有两种情况：

- 1、一种是需要建立存储空间的。例如：int a 在声明的时候就已经建立了存储空间。
- 2、另一种是不需要建立存储空间的，通过使用extern关键字声明变量名而不定义它。 例如：extern int a 其中变量 a 可以在别的文件中定义的。
- 除非有extern关键字，否则都是变量的定义。

```
extern int i; //声明，不是定义
int i; //声明，也是定义
```



### 常量

常量是固定值，在程序执行期间不会改变。这些固定的值，又叫做**字面量**。

整数常量：

```
85         /* 十进制 */
0213       /* 八进制 */
0x4b       /* 十六进制 */
30         /* 整数 */
30u        /* 无符号整数 */
30l        /* 长整数 */
30ul       /* 无符号长整数 */
```

自定义常量：

有两种简单的定义常量的方式：

1. 使用 **#define** 预处理器。

   ```
   #define LENGTH 10   
   #define WIDTH  5
   #define NEWLINE '\n'
   ```

2. 使用 **const** 关键字。

   ```
   const int  LENGTH = 10;
   const int  WIDTH  = 5;
   const char NEWLINE = '\n';
   ```

define 和 const的区别：

**(1) 编译器处理方式不同**

- \#define 宏是在预处理阶段展开。
-  const 常量是编译运行阶段使用。

**(2) 类型和安全检查不同**

-  \#define 宏没有类型，不做任何类型检查，仅仅是展开。
-  const 常量有具体的类型，在编译阶段会执行类型检查。

**(3) 存储方式不同**

- \#define宏仅仅是展开，有多少地方使用，就展开多少次，不会分配内存。（宏定义不分配内存，变量定义分配内存。）
- const常量会在内存中分配(可以是堆中也可以是栈中)。

**(4) const 可以节省空间，避免不必要的内存分配。 例如：**

```c
#define NUM 3.14159 //常量宏
const doulbe Num = 3.14159; //此时并未将Pi放入ROM中 ......
double i = Num; //此时为Pi分配内存，以后不再分配！
double I= NUM; //编译期间进行宏替换，分配内存
double j = Num; //没有内存分配
double J = NUM; //再进行宏替换，又一次分配内存！
```

const 定义常量从汇编的角度来看，只是给出了对应的内存地址，而不是象 #define 一样给出的是立即数，所以，const 定义的常量在程序运行过程中只有一份拷贝（因为是全局的只读变量，存在静态区），而 #define 定义的常量在内存中有若干个拷贝。

**(5) 提高了效率。 编译器通常不为普通const常量分配存储空间，而是将它们保存在符号表中，这使得它成为一个编译期间的常量，没有了存储与读内存的操作，使得它的效率也很高。**

**(6) 宏替换只作替换，不做计算，不做表达式求解;**

宏预编译时就替换了，程序运行时，并不分配内存。



### 存储类

* auto

  **auto** 存储类是所有局部变量默认的存储类。

  ```
  {
     int mount;
     auto int month;
  }
  ```

  上面的实例定义了两个带有相同存储类的变量，auto 只能用在函数内，即 auto 只能修饰局部变量

* register

  **register** 存储类用于定义存储在寄存器中而不是 RAM 中的局部变量。这意味着变量的最大尺寸等于寄存器的大小（通常是一个词），且不能对它应用一元的 '&' 运算符（因为它没有内存位置）。

  ```
  {
     register int  miles;
  }
  ```

  寄存器只用于需要快速访问的变量，比如计数器。还应注意的是，定义 'register' 并不意味着变量将被存储在寄存器中，它意味着变量可能存储在寄存器中，这取决于硬件和实现的限制。

* static

  **static** 存储类指示编译器在程序的生命周期内保持局部变量的存在，而不需要在每次它进入和离开作用域时进行创建和销毁。因此，使用 static 修饰局部变量可以在函数调用之间保持局部变量的值。

  static 修饰符也可以应用于全局变量。当 static 修饰全局变量时，会使变量的作用域限制在声明它的文件内。

  static 是全局变量的默认存储类, 函数外， `static int Count `  = `int Count`

  ```c
  #include <stdio.h>
   
  /* 函数声明 */
  void func1(void);
   
  static int count=10;        /* 全局变量 - static 是默认的 */
   
  int main()
  {
    while (count--) {
        func1();
    }
    return 0;
  }
   
  void func1(void)
  {
  /* 'thingy' 是 'func1' 的局部变量 - 只初始化一次
   * 每次调用函数 'func1' 'thingy' 值不会被重置。
   */                
    static int thingy=5;
    thingy++;
    printf(" thingy 为 %d ， count 为 %d\n", thingy, count);
  }
  ```

  输出 

  ```
  thingy 为 6 ， count 为 9
   thingy 为 7 ， count 为 8
   thingy 为 8 ， count 为 7
   thingy 为 9 ， count 为 6
   thingy 为 10 ， count 为 5
   thingy 为 11 ， count 为 4
   thingy 为 12 ， count 为 3
   thingy 为 13 ， count 为 2
   thingy 为 14 ， count 为 1
   thingy 为 15 ， count 为 0
  ```

* extern

   存储类用于提供一个全局变量的引用，全局变量对所有的程序文件都是可见的。当您使用 'extern' 时，对于无法初始化的变量，会把变量名指向一个之前定义过的存储位置。

  当您有多个文件且定义了一个可以在其他文件中使用的全局变量或函数时，可以在其他文件中使用 *extern* 来得到已定义的变量或函数的引用。可以这么理解，*extern* 是用来在另一个文件中声明一个全局变量或函数。

  **第一个文件：main.c**

  ```c
  #include <stdio.h>
   
  int count ;
  extern void write_extern();
   
  int main()
  {
     count = 5;
     write_extern();
  }
  ```

  **第二个文件：support.c**

  ```c
  #include <stdio.h>
   
  extern int count;
   
  void write_extern(void)
  {
     printf("count is %d\n", count);
  }
  ```

  在这里，第二个文件中的 *extern* 关键字用于声明已经在第一个文件 main.c 中定义的 *count*。现在 ，编译这两个文件，如下所示：

  ```
   $ gcc main.c support.c
  ```

  这会产生 **a.out** 可执行程序，当程序被执行时，它会产生下列结果：

  ```
  count is 5
  ```



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



### 几个系统函数

printf

`printf("23+56=%d\n", 23+56);`

%d 说明后面有一个整数要输出在这个位置上



sizeof

为了得到某个类型或某个变量在特定平台上的准确大小，您可以使用 **sizeof** 运算符。表达式 *sizeof(type)* 得到对象或类型的存储字节大小。下面的实例演示了获取 int 类型的大小：

```c
#include <stdio.h> 
#include <limits.h>   
int main() {    
	printf("int 存储大小 : %lu \n", sizeof(int));        
	return 0;
}
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



### typedef

https://www.jianshu.com/p/740f87e97be1



### 交互

https://ksco.gitbooks.io/build-your-own-lisp/Interactive.html



#### 预处理器（preprocessor ）







