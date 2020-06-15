
---
title: "js 数据类型及转换.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## Js中的数据类型

Js中的数据类型一共有六种，即number，string，boolean，underfine，null，object。

### number

Number数据类型指的是数字，可以为整型，也可以是浮点数。如

`var a=12,b=12.5;`



### string

字符串由零个或多个字符构成，字符包括字母，数字，标点符号和空格;需要注意的是

字符串必须放在引号里（单引号或双引号）;

如

`var bob=”man”; alert(“bob”); alert(bob);`

浏览器首先会弹出包含有“bob”的字符串，然后弹出包含有“man”的字符串，前者是直接弹出字符串，后者则是弹出变量的值。



### boolean

布尔型数据只能有两种值 true 和 false，在js中true和false是关键字。通常，我们设置布尔值时多用于条件的判断。如：

`var flag=true; if (flag){//js 代码}`

在条件判断语句中我们将所有的判断条件看做一个布尔值（这里需要了解一些布尔值的转换特性）。



### underfine

underfine通常指的是没有赋值的变量，通过typeof可以对数据的类型进行判断。如

```
`var` `a,b=underfine;` `alert(a);` `alert(``typeof` `a);`
```

两次结果都为underfine。



### null

null是一个只有一个值的特殊类型。表示一个空对象引用。如：

var a=null;

将a清空。



### object

对象就是由一些彼此相关的属性和方法集合在一起而构成的一个数据实体。常见的对象有array，window，document等。

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
var weekly=["星期天","星期一","星期二","星期三","星期四","星期五","星期六"]        document.write("today is "+weekly[day]+"<br>")
```

结果将输出今天是礼拜几。



### symbol

es6 新增的类型的值

 

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