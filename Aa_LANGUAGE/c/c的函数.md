### printf

`printf("23+56=%d\n", 23+56);`

%d 说明后面有一个整数要输出在这个位置上



### sizeof

为了得到某个类型或某个变量在特定平台上的准确大小，您可以使用 **sizeof** 运算符。表达式 *sizeof(type)* 得到对象或类型的存储字节大小。下面的实例演示了获取 int 类型的大小：

```c
#include <stdio.h> 
#include <limits.h>   
int main() {    
	printf("int 存储大小 : %lu \n", sizeof(int));        
	return 0;
}
```



