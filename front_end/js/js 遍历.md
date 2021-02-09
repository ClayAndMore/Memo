---
title: "js 遍历.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
### while 循环

``` js
var ourArray = [];
var i = 0;
while(i < 5) {
  ourArray.push(i);
  i++;
}
```

还有 `do...while`循环，它会先执行`do`里面的代码，如果`while`表达式为真则重复执行，反之则停止执行。。

``` js
var ourArray = [];
var i = 0;
do {
 ourArray.push(i);
 i++;
} while (i < 5);
```





### for 循环

```
for ([初始化]; [条件判断]; [计数器])
```

`初始化`语句只会在执行循环开始之前执行一次。它通常用于定义和设置你的循环变量。

`条件判断`语句会在每一轮循环的开始执行，只要条件判断为`true`就会继续执行循环。当条件为`false`的时候，循环将停止执行。这意味着，如果条件在一开始就为`false`，这个循环将不会执行。

`计数器`是在每一轮循环结束时执行，通常用于递增或递减。



### 判断元素类型

```js
//1
var temp = Object.prototype.toString.apply("abcdef");
alert(temp);  //[Object String] 数组，字典，null都会输出Object
//2
typeof "hello" // "string"
//3
var haorooms=[];
console.log(haorooms instanceof Array) //返回true 
//4
console.log([].constructor == Array);
console.log({}.constructor == Object);
console.log("string".constructor == String);
console.log((123).constructor == Number);
console.log(true.constructor == Boolean);
//5
Array.isArray([1,2,3]) 
//ECMAScript5将Array.isArray()正式引入JavaScript，目的就是准确地检测一个值是否为数组。
```



### 遍历

#### for of

```js
for( let i of arr){
    console.log(i);
}
```

for-of遍历 是ES6新增功能,or-of循环不仅支持数组，还支持大多数类数组对象，例如DOM [NodeList对象]。

for-of循环也支持字符串遍历

```js
for(let x of {'a':'aa','b':'bb'}){   //并不支持对象
    console.log(x)
}
VM5981:1 Uncaught TypeError: {(intermediate value)(intermediate value)} is not iterable
    at <anonymous>:1:14
// 数组
for(let x of [11,22]){
    console.log(x)
}
11
22
//字符串
for(let x of 'abcd'){
    console.log(x)
}
a
b
c
d
```

**for-of是为遍历数组而设计的，不适用于遍历对象。**



#### for in

```js
for(let x in {'a':'aa','b':'bb'}){
    console.log(x)
}
VM5904:2 a
VM5904:2 b
undefined
for(let x in [11,22]){
    console.log(x)
}
VM5933:2 0
VM5933:2 1
undefined
for(let x in 'abcd'){
    console.log(x)
}
VM5970:2 0
VM5970:2 1
VM5970:2 2
VM5970:2 3
```

**可以看出let in方式得到的都是下标或索引值**, 	**for-in是为遍历对象而设计的，不适用于遍历数组。**

**遍历数组的缺点：数组的下标index值是数字，for-in遍历的index值"0","1","2"等是字符串**



#### 数组遍历

```js
//1，普通for循环，经常用的数组遍历
var arr = [1,2,0,3,9];
 for ( var i = 0; i <arr.length; i++){
    console.log(arr[i]);
}

//2，优化版for循环:使用变量，将长度缓存起来，避免重复获取长度，数组很大时优化效果明显
for(var j = 0,len = arr.length; j < len; j++){
    console.log(arr[j]);
}

//3，forEach，ES5推出的,数组自带的循环，主要功能是遍历数组，实际性能比for还弱
arr.forEach(function(value,i){
　　console.log('forEach遍历:'+i+'--'+value)
})
//forEach这种方法也有一个小缺陷：你不能使用break语句中断循环，也不能使用return语句返回到外层函数。

//4,map遍历，map即是 “映射”的意思 用法与 forEach 相似
arr.map(function(value,index){
    console.log('map遍历:'+index+'--'+value);
});
//map遍历支持使用return语句，支持return返回值 
//forEach、map都是ECMA5新增数组的方法，所以ie9以下的浏览器还不支持
```





向数组插入数据

```js
let myArray=[11,22,33];
console.log('原数组：',myArray);
myArray.push(44,55);
console.log('用push在数组后面插入元素：',myArray);
myArray.unshift(66,77);
console.log('用unshift在数组前面插入元素：',myArray);
myArray.splice(2,0,'肾虚少年');
console.log('用splice在数组指定位置插入元素：',myArray);
//splice接收多个参数，分别是索引，要删除的元素个数，新加的元素(可多个，用逗号隔开)；


```





判断数组中是否有某个值：

https://segmentfault.com/a/1190000014202195



三元运算

```js
condition ? expr1 : expr2

//eg1
if(isMember){
    fee="$2.00";
}else{
    fee="$10.00";
}
fee=isMember ? "$2.00" : "$10.00";

//eg2 多语句
age > 18 ? (
 car = "奇瑞QQ",
 school = "清华第一幼儿园"
    //do someting
) : (
 alert("Sorry, you are much too young!")
)

//eg3, +问题
var isMember = false;
console.log("当前费用" + isMember ? "$2.00" : "$10.00");
// 实际上："当前费用false" ? "$2.00" : "$10.00"
// ？号的优先级比＋号低，所以实际运行的语句是
```





json处理

变成json字符串：

```js
JSON.stringify(jsObj, null, "\t"); // 缩进一个tab  
JSON.stringify(jsObj, null, 4);    // 缩进4个空格 
```

变成对象：

`var obj = str.parseJSON(); 



### 字符串操作

常用方法整理：https://www.cnblogs.com/ndxy/p/6634626.html

判断以某个字符开头：https://www.cnblogs.com/sghy/p/9604813.html

去掉前后两边的引号：

`var str='"13"23"';`
`str.replace(/^\"|\"$/g,'') //去除str 前后的双引号`





### 判断

注意==和===的区别



#### 判断数组或对象的key是否存在

`ary.hasOwnProperty(key); 或 obj.hasOwnProperty(key);`

```js
// 数组
['a','b','c'].hasOwnProperty('a')
false
['a','b','c'].hasOwnProperty('1')
true
['a','b','c'].hasOwnProperty('3')
false

//对象
ss={'a':'aa','b':'bb','c':'cc'}
{a: "aa", b: "bb", c: "cc"}
ss.hasOwnProperty('a')
true
```

