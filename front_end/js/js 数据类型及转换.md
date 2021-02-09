---
title: "js 数据类型及转换.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---


## Js中的数据类型

Js中的数据类型一共有六种，即number，string，boolean，underfine，null，object。

### number

Number数据类型指的是数字，可以为整型，也可以是浮点数。如

`var a=12,b=12.5;`

#### 数字可以是对象

数字可以进行初始化 ，还可以对数字对象初始化

```js
var x = 123;
var y = new Number(123);
typeof(x) // 返回 Number
typeof(y) // 返回 Object
```



#### 无穷大Infinity

当数字运算结果超过了JavaScript所能表示的数字上限（溢出），结果为一个特殊的无穷大（infinity）值，在JavaScript中以Infinity表示。同样地，当负数的值超过了JavaScript所能表示的负数范围，结果为负无穷大，在JavaScript中以-Infinity表示。无穷大值的行为特性和我们所期望的是一致的：基于它们的加、减、乘和除运算结果还是无穷大（当然还保留它们的正负号）。

```js
myNumber=2;
while (myNumber!=Infinity)
{
    myNumber=myNumber*myNumber; // 重复计算直到 myNumber 等于 Infinity
}
```



### string

字符串由零个或多个字符构成，字符包括字母，数字，标点符号和空格;需要注意的是

字符串必须放在引号里（单引号或双引号）;

如

`var bob=”man”; alert(“bob”); alert(bob);`



转义：

通过在引号前面使用反斜杠（`\`）来转义引号。

```
var sampleStr = "Alan said, \"Peter is learning JavaScript\".";
```

有了转义符号，JavaScript 就知道这个单引号或双引号并不是字符串的结尾，而是字符串内的字符。所以，上面的字符串打印到控制台的结果为：

```
Alan said, "Peter is learning JavaScript".
```



#### 字符串属性

当您将新数据引入JavaScript程序时，浏览器会将其保存为数据类型的实例。 每个字符串实例都有一个名为length的属性，该属性存储该字符串中的字符数。 您可以通过在字符串后加上句点和属性名称来检索属性信息：

``` js
console.log('Teaching the world how to code'.length); // 30
```



字符串方法：

``` js
console.log('hello'.toUpperCase()); // Prints 'HELLO'
console.log('Hey'.startsWith('H')); // Prints true
```



#### 字符串的不变性

`字符串`的值是 不可变的，这意味着一旦字符串被创建就不能被改变。

例如，下面的代码：

> var myStr = "Bob";
> myStr[0] = "J";

是不会把变量`myStr`的值改变成 "Job" 的，因为变量`myStr`是不可变的。注意，这*并不*意味着`myStr`永远不能被改变，只是字符串字面量 string literal 的各个字符不能被改变



### boolean

布尔型数据只能有两种值 true 和 false，在js中true和false是关键字。通常，我们设置布尔值时多用于条件的判断。如：

`var flag=true; if (flag){//js 代码}`

在条件判断语句中我们将所有的判断条件看做一个布尔值（这里需要了解一些布尔值的转换特性）。



### null

null是一个只有一个值的特殊类型。表示一个空对象引用。如：

var a=null;

将a清空。



### underfine

underfine通常指的是没有赋值的变量，通过typeof可以对数据的类型进行判断。如

```
`var` `a,b=underfine;` `alert(a);` `alert(``typeof` `a);`
```

两次结果都为underfine。



### symbol

es6 新增的类型的值



### object

对象就是由一些彼此相关的属性和方法集合在一起而构成的一个数据实体。常见的对象有array，window，document等。

对象拥有属性和方法：

* 属性是和对象相关的值，访问方式：`对象名.属性名` 如：`str.length`
* 方法是对象的相关动作，访问方式：`对象名.方法名（）`

#### 创建对象实例

这个例子创建了对象的一个新实例，并向其添加了四个属性：

```js
person=new Object();
person.firstname="John";
person.lastname="Doe";
person.age=50;
person.eyecolor="blue";
```

上面的话可代替之：
`person={firstname:"John",lastname:"Doe",age:50,eyecolor:"blue"};`



例：

```js
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth() + 1;
var day = today.getDay();
```

 通过创建对象实例就可以调用对象的方法了，如上就是创建了一个Date的对象实例today，today通过调用Date的方法得出了现在的年月日等信息。

数组array是作为经常使用的对象，是由多个 (键-值) 所组成的一个多容器。其索引 默认是从0开始的。创建数组有两种方法：1创建数组对象实例 var arr=new Array（1,2,3）；2直接使用面向字面量 var a=[1,2,3];

例

```js
var date = new Date();        
var day=date.getDay(); 
var weekly=["星期天","星期一","星期二","星期三","星期四","星期五","星期六"]        
document.write("today is "+weekly[day]+"<br>")
```

结果将输出今天是礼拜几。



#### 访问对象属性

除了使用点访问，还可以石笋中括号来访问：

``` js
var myObj = {
  "Space Name": "Kirk",
  "More Space": "Spock",
  "NoSpace": "USS Enterprise"
};
myObj["Space Name"]; // Kirk
myObj['More Space']; // Spock
myObj["NoSpace"]; // USS Enterprise

// 访问嵌套对象：
ourStorage.desk.drawer;
```



#### 删除对象属性

delete ourDog.bark; 



#### 字典

对象和字典一样，可以用来存储键/值对。如果你的数据跟对象一样，你可以用对象来查找你想要的值，而不是使用switch或if/else语句。当你知道你的输入数据在某个范围时，这种查找方式极为有效。

``` js
var alpha = {
  1:"Z",
  2:"Y",
  3:"X",
  4:"W",
  ...
  24:"C",
  25:"B",
  26:"A"
};
alpha[2]; // "Y"
alpha[24]; // "C"

var value = 2;
alpha[value]; // "Y"
```



#### 内建对象

Math

``` js
console.log(Math.random()*100); // 19.523999807373514
console.log(Math.floor(Math.random()*100)); // 22
console.log(Math.floor(1.9444)) // 1
console.log(Math.ceil(43.8)); // 44
```

Math.random 生成一个 0 到 1 的随机数(包括0，不包括1）， 然后我们可以乘一些系数。

Math.floor可以降整个数字取它的整数部分, 而ceil方法则是向上取整；

所有方法：https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math



Number

``` js
console.log(Number.isInteger(2017));// true
```

检测是否是整数；

其他方法：

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number



#### 数组

JavaScript的 `**Array**` 对象是用于构造数组的全局对象，数组是类似于列表的高阶对象。

```js
var array = [50,60,70];   // 创建数组
array[0];                // 通过索引访问数组的值 ,值为 50
array[0] =40 ;           // 等于 [40; 60; 70]

// 操作数组
var arr = [1,2,3];
arr.push(4);              // push 尾部添加元素, 现在arr的值为 [1,2,3,4]
var lastOne = arr.pop();   // pop 尾部移出元素, lastOne 为 3， arr 为 [1,2]
var firstOne = arr.shift(); // shift 头部移出第一个元素，  firstOne 为 1， arr 为 [2]
arr.unshift(0);             // unshift 在头部添加元素， arr 为 [0,2]
```



## 算术操作符

1. Add: `+`
2. Subtract: `-`
3. Multiply: `*`
4. Divide: `/`
5. Remainder: `%`

``` js
console.log(3 + 4); // Prints 7
console.log(5 - 1); // Prints 4
console.log(4 * 2); // Prints 8
console.log(9 / 3); // Prints 3
```

数字递增和递减：

```
使用++，我们可以很容易地对变量进行自增或者+1运算。
i++; 等效于 i = i + 1;
i--; 等效于 i = i - 1;
```

同理有复合赋值：

```
+=
-=
*=
/=
```





## 数据类型的查看与转换

 在js中我们经常需要知道某些变量的数据类型，并将其转换为我们所需要的数据类型。

### 数据类型的查看

 通常，我们判断变量的数据类型会用到标识符typeof,如： 

`var mood = "happy";alert(typeof mood); alert(typeof 95)；`



 

### 数据转换

数据的转换中，我们经常用到的是将变量转换成字符串或数字。

转换成字符串要使用toString（），例

`var married = false; alert(married.toString());`

 转换成数字时，有两种方法，parseInt() 转换成整数，parseFloat()转换成浮点数。

 eg:

```js
var test = parseInt(“blue”); //returns NaN 
var test = parseInt(“1234blue”); //returns 1234
var test = parseInt(“22.5”); //returns 22 
var test = parseFloat(“1234blue”); //returns 1234
var test = parseFloat(“22.5”); //returns 22.5`
```