---
title: "es及es6.md"
date: 2016-08-04 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["js"]
categories: ["前端"]
author: "Claymore"

---



### js vs es

![](https://pic3.zhimg.com/80/v2-7e9c591eb2fad6e1738ca0227e217592_720w.png)



一直致力于指定消费电子标准的 ECMA 组织 将 网景和微软的不同浏览器脚本统一规范，发布了ES.

2009 年，ES 5 横空出世，同年，前端界也出了一个大事件——Node.js 发布。Node.js 是一个基于 Google Chrome 的 V8 引擎（2008年发布）的 JS 运行环境。

2015 年发布 ES 6，2016 年的 ES 7 直接更名为 ES 2016.

新填的内容包括：

- 箭头函数
- 类
- 模块
- Promises 对象
- 异步生成器 Generators
- `let`以及`const`语法





### let

ES6 新增了`let`命令，用来声明变量。它的用法类似于`var`，但是所声明的变量，只在`let`命令所在的代码块内有效。

#### 变量覆盖

使用`var`关键字来声明变量，会出现重复声明导致变量被覆盖却不会报错的问题：

``` js
var camper = 'James';
var camper = 'David';
console.log(camper);
// 打印出 'David'
```

在上面的代码中，`camper`的初始值为`'James'`，然后又被覆盖成了`'David'`。

在小型的应用中，你可能不会遇到这样的问题，但是当你的代码规模变得更加庞大的时候，就可能会在不经意间覆盖了之前定义的变量。

这样的行为不会报错，导致了 debug 非常困难。

在 ES6 中引入了新的关键字`let`来解决`var`关键字带来的潜在问题。

如果你在上面的代码中，使用了`let`关键字来代替`var`关键字，结果会是一个报错。

``` js
let camper = 'James';
let camper = 'David'; // 报错
```

你可以在浏览器的控制台里看见这个错误。

与`var`不同的是，当使用`let`的时候，同一名字的变量只能被声明一次。

请注意`"use strict"`。这代表着开启了严格模式，用于检测常见的代码错误以及"不安全"的行为，例如：

``` js
"use strict";
x = 3.14; // x 没有声明导致了报错
```



#### 作用域

当你使用`var`关键字来声明一个变量的时候，这个变量会被声明成全局变量，或是函数内的局部变量。

`let`关键字的作用类似，但会有一些额外的特性。如果你在代码块、语句或表达式中使用关键字`let`声明变量，这个变量的作用域就被限制在当前的代码块，语句或表达式之中。

举个例子：

``` js
var numArray = [];
for (var i = 0; i < 3; i++) {
 numArray.push(i);
}
console.log(numArray);
// 返回 [0, 1, 2]
console.log(i);
// 返回 3
```

当使用`var`关键字的时候，`i`会被声明成全局变量。当`i++`执行的时候，它会改变全局变量的值。这段代码可以看做下面这样:

``` js
var numArray = [];
var i;
for (i = 0; i < 3; i++) {
 numArray.push(i);
}
console.log(numArray);
// returns [0, 1, 2]
console.log(i);
// returns 3
```

如果你在`for`循环中创建了使用`i`变量的函数，那么在后续调用函数的时候，上面提到的这种行为就会导致问题。这是因为函数存储的值会因为全局变量`i`的变化而不断的改变。

``` js
var printNumTwo;
for (var i = 0; i < 3; i++) {
 if(i === 2){
  printNumTwo = function() {
   return i;
  };
 }
}
console.log(printNumTwo());
// 返回 3
```

可以看到，`printNumTwo()`打印了 3 而不是 2。这是因为`i`发生了改变，并且函数`printNumTwo()`返回的是全局变量`i`的值，而不是`for`循环中创建函数时`i`的值。`let`关键字就不会有这种现象：

``` js
'use strict';
let printNumTwo;
for (let i = 0; i < 3; i++) {
 if (i === 2) {
  printNumTwo = function() {
   return i;
  };
 }
}
console.log(printNumTwo());
// 返回 2
console.log(i);
// 返回 "没有定义 i 变量"
```

`i`在全局作用域中没有声明，所以它没有被定义，它的声明只会发生在`for`循环内。在循环执行的时候，`let`关键字创建了三个不同的`i`变量，他们的值分别为 0、1 和 2，所以`printNumTwo()`返回了正确的值。





### const

`let`并不是唯一的新的声明变量的方式。在 ES6里面，你还可以使用`const`关键字来声明变量。

`const`拥有`let`的所有优点，所不同的是，通过`const`声明的变量是只读的。这意味着通过`const`声明的变量只能被赋值一次，而不能被再次赋值。

``` js
"use strict"
const FAV_PET = "Cats";
FAV_PET = "Dogs"; // 报错
```

可以看见，尝试给通过`const`声明的变量再次赋值会报错。你应该使用`const`关键字来对所有不打算再次赋值的变量进行声明。这有助于你避免给一个常量进行额外的再次赋值。一个最佳实践是对所有常量的命名采用全大写字母，并在单词之间使用下划线进行分隔。



#### 声明数组

在现代的 JavaScript 里，`const`声明有很多用法。

一些开发者倾向默认使用`const`来声明所有变量，但如果它们打算在后续的代码中修改某个值，那在声明的时候就会用`let`。

然而，你要注意，对象（包括数组和函数）在使用`const`声明的时候依然是可变的。使用`const`来声明只会保证它的标识不会被重新赋值。

``` js
"use strict";
const s = [5, 6, 7];
s = [1, 2, 3]; // 试图给 const 变量赋值，报错
s[2] = 45; // 与用 var 或 let 声明的数组一样，这个操作也会成功
console.log(s); // 返回 [5, 6, 45]
```



从以上代码看出，你可以改变`[5, 6, 7]`自身，所以`s`变量指向了改变后的数组`[5, 6, 45]`。和所有数组一样，数组`s`中的数组元素是可以被改变的，但是因为使用了`const`关键字，你不能使用赋值操作符将变量标识`s`指向另外一个数组。



### 新类型

S6 中的新类型 [`Symbol`](http://es6.ruanyifeng.com/#docs/symbol) 和 [`BigInt`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/BigInt)。



### 防止对象改变

为了确保数据不被改变，JavaScript 提供了一个函数`Object.freeze`来防止数据改变。

当一个对象被冻结的时候，你不能再对它的属性再进行增、删、改的操作。任何试图改变对象的操作都会被阻止，却不会报错。

``` js
let obj = {
 name:"FreeCodeCamp",
 review:"Awesome"
};
Object.freeze(obj);
obj.review = "bad"; // obj 对象被冻结了，这个操作会被忽略
obj.newProp = "Test"; // 也会被忽略，不允许数据改变
console.log(obj);
// { name: "FreeCodeCamp", review:"Awesome"}
```



### 箭头函数

之前匿名函数这样写：

``` js
const myFunc = function() {
 const myVar = "value";
 return myVar;
}
```

ES6 提供了其他写匿名函数的方式的语法糖。你可以使用箭头函数：

``` js
const myFunc = () => {
 const myVar = "value";
 return myVar;
}
```



当不需要函数体，只返回一个值的时候，箭头函数允许你省略`return`关键字和外面的大括号。这样就可以将一个简单的函数简化成一个单行语句。

> const myFunc= () => "value"

这段代码仍然会返回`value`。



#### 高阶箭头函数

箭头函数在类似`map()`，`filter()`，`reduce()`等需要其他函数作为参数来处理数据的高阶函数里会很好用。

阅读以下代码：

``` js
FBPosts.filter(function(post) {
 return post.thumbnail !== null && post.shares > 100 && post.likes > 500;
})
```

我们写下了`filter`函数，并尽量保证可读性。现在让我们用箭头函数来写同样的代码看看：

``` js
FBPosts.filter((post) => post.thumbnail !== null && post.shares > 100 && post.likes > 500)
```



#### 简洁的对象字面量声明

ES6 添加了一些很棒的功能，以便于更方便地定义对象。

``` js
const getMousePosition = (x, y) => ({
 x: x,
 y: y
});
```

`getMousePosition`是一个返回了拥有2个属性的对象的简单函数。

ES6 提供了一个语法糖，消除了类似`x: x`这种冗余的写法.你可以仅仅只写一次`x，解释器会自动将其转换成x: x。`

下面是使用这种语法重写的同样的函数：

> const getMousePosition = (x, y) => ({ x, y });



### 函数默认参数

ES6 里允许给函数传入默认参数，来构建更加灵活的函数。

``` js
function greeting(name = "Anonymous") {
 return "Hello " + name;
}
console.log(greeting("John")); // Hello John
console.log(greeting()); // Hello Anonymous
```

默认参数会在参数没有被指定（值为 undefined ）的时候起作用。在上面的例子中，参数`name`会在没有得到新的值的时候，默认使用值 "Anonymous"。你还可以给多个参数赋予默认值。

#### rest参数

ES6 推出了用于函数参数的rest参数帮助我们创建更加灵活的函数，可以创建有一个变量来接受多个参数的函数。这些参数被储存在一个可以在函数内部读取的数组中。

``` js
function howMany(...args) {
 return "You have passed " + args.length + " arguments.";
}
console.log(howMany(0, 1, 2)); // 输出：You have passed 3 arguments.
console.log(howMany("string", null, [1, 2, 3], { })); // 输出：You have passed 4 arguments.
```

`rest`操作符可以避免查看`args`数组的需求，并且允许我们在参数数组上使用`map()`,`filter()`，和`reduce()`。

**rest 参数之后不能再有其他参数（即只能是最后一个参数），否则会报错。**

**rest参数和arguments对象的区别**

- rest参数只包含那些没有对应形参的实参；而 arguments 对象包含了传给函数的所有实参。
- arguments 对象不是一个真实的数组；而rest参数是真实的 Array 实例，也就是说你能够在它上面直接使用所有的数组方法。
- arguments 对象对象还有一些附加的属性 (比如callee属性)。

### 扩展操作符

扩展运算符可以看做是 rest 参数的逆运算，将一个数组转为用逗号分隔的参数序列。

```js
console.log(...[1, 2, 3]) // 1 2 3
console.log(1, ...[2, 3, 4], 5) //1 2 3 4 5
```

普通函数的调用：

```js
function push(array, ...items) {
  array.push(...items);
}

function add(x, y) {
  return x + y;
}

var numbers = [4, 38];
add(...numbers) // 42
```

上面代码中，`array.push(...items)`和`add(...numbers)`这两行，都是函数的调用，它们的都使用了扩展运算符。该运算符将一个数组，变为参数序列。

#### 替代 apply 方法调用函数

```js
// ES5 的写法
Math.max.apply(null, [14, 3, 77])

// ES6 的写法
Math.max(...[14, 3, 77]) // 等同于 Math.max(14, 3, 77);

// ES5 的写法
var arr1 = [0, 1, 2];
var arr2 = [3, 4, 5];
Array.prototype.push.apply(arr1, arr2);

// ES6 的写法
var arr1 = [0, 1, 2];
var arr2 = [3, 4, 5];
arr1.push(...arr2);
```

#### 合并数组

```js
var arr1 = ['a', 'b'];
var arr2 = ['c'];
var arr3 = ['d', 'e'];

// ES5的合并数组
arr1.concat(arr2, arr3)  // [ 'a', 'b', 'c', 'd', 'e' ]

// ES6的合并数组
[...arr1, ...arr2, ...arr3]  // [ 'a', 'b', 'c', 'd', 'e' ]
```

#### 与解构赋值结合

```js
const [first, ...rest] = [1, 2, 3, 4, 5];
first // 1
rest  // [2, 3, 4, 5]

const [first, ...rest] = [];
first // undefined
rest  // []

const [first, ...rest] = ["foo"];
first  // "foo"
rest   // []
```

如果将扩展运算符用于数组赋值，只能放在参数的最后一位，否则会报错。

```js
const [...butLast, last] = [1, 2, 3, 4, 5];  // 报错
const [first, ...middle, last] = [1, 2, 3, 4, 5];  // 报错
```

#### 将字符串转为数组

```js
var str = 'hello';

// ES5  
var arr1 = str.split('');  // [ "h", "e", "l", "l", "o" ] 

// ES6  
var arr2 = [...str];  // [ "h", "e", "l", "l", "o" ] 
```

#### 实现了 Iterator 接口的对象

任何 [Iterator](http://es6.ruanyifeng.com/#docs/iterator) 接口的对象，都可以用扩展运算符转为真正的数组。

```js
var nodeList = document.querySelectorAll('div');
var array = [...nodeList];
```

上面代码中，`querySelectorAll`方法返回的是一个`nodeList`对象。它不是数组，而是一个类似数组的对象。这时，扩展运算符可以将其转为真正的数组，原因就在于`NodeList`对象实现了 `Iterator` 。



### 解构赋值

#### 从对象中分配变量

我们之前看到了展开操作符是如何展开数组的内容的。

对于对象，我们也可以做同样的操作。解构赋值 就是可以从对象中直接获取对应值的语法。

看看以下 ES5 的代码：

``` js
var voxel = {x: 3.6, y: 7.4, z: 6.54 };
var x = voxel.x; // x = 3.6
var y = voxel.y; // y = 7.4
var z = voxel.z; // z = 6.54
```

使用 ES6 的解构语法可以完成同样的赋值语句：

`const { x, y, z } = voxel; // x = 3.6, y = 7.4, z = 6.54`

如果你想将`voxel.x`,`voxel.y`,`voxel.z`的值分别赋给`a`,`b`,`c`，可以用以下这种很棒的方式：

`const { x : a, y : b, z : c } = voxel; // a = 3.6, b = 7.4, c = 6.54`

你可以这样理解：“将`x`地址中的值拷贝到`a`当中去。”，等等。



#### 嵌套对象中分配变量

同样，我们可以将 *嵌套的对象*解构到变量中。

``` js
const a = {
 start: { x: 5, y: 6},
 end: { x: 6, y: -9 }
};
const { start : { x: startX, y: startY }} = a;
console.log(startX, startY); // 5, 6
```

在上面的例子里，`a.start`将值赋给了变量`start`，`start`同样也是个对象。



#### 数组中分配变量

在 ES6 里面，解构数组可以如同解构对象一样简单。

与数组解构不同，数组的扩展运算会将数组里的所有内容分解成一个由逗号分隔的列表。所以，你不能选择哪个元素来给变量赋值。

而对数组进行解构却可以让我们做到这一点：

``` js
const [a, b] = [1, 2, 3, 4, 5, 6];
console.log(a, b); // 1, 2
```

变量`a`以及`b`分别被数组的第一、第二个元素赋值。

我们甚至能在数组解构中使用逗号分隔符，来获取任意一个想要的值：

``` js
const [a, b,,, c] = [1, 2, 3, 4, 5, 6];
console.log(a, b, c); // 1, 2, 5
```



#### 将对象作为函数的参数传递

在某些情况下，你可以在函数的参数里直接解构对象。

``` js
const profileUpdate = (profileData) => {
 const { name, age, nationality, location } = profileData;
 // ...
}
```

上面的操作解构了传给函数的对象。这样的操作也可以直接在参数里完成：

``` js
const profileUpdate = ({ name, age, nationality, location }) => {
 /* ... */
}
```

这样的操作去除了多余的代码，使代码更加整洁。

这样做还有个额外的好处：函数不需要再去操作整个对象，而仅仅是操作复制到函数作用域内部的参数。



### 模板字符串

模板字符串是 ES6 的另外一项新的功能。这是一种可以轻松构建复杂字符串的方法。

请看以下代码：

``` js
const person = {
 name: "Zodiac Hasbro",
 age: 56
};

// string interpolation
const greeting = `Hello, my name is ${person.name}!
I am ${person.age} years old.`;

console.log(greeting); // 打印出
// Hello, my name is Zodiac Hasbro!
// I am 56 years old.
```

这段代码有许多的不同：

首先，上面使用的`${variable}`语法是一个占位符。这样一来，你将不再需要使用`+`运算符来连接字符串。当需要在字符串里增加变量的时候，你只需要在变量的外面括上`${`和`}`，并将其放在字符串里就可以了。

其次，在例子使用了反引号（```），而不是引号（`'`或者`"`）将字符串括了起来，并且这个字符串可以换行。

这个新的方式使你可以更灵活的创建复杂的字符串。





### class

ES6 提供了一个新的创建对象的语法，使用关键字`class`。

值得注意的是，`class`只是一个语法糖，它并不像 Java、Python 或者 Ruby 这一类的语言一样，严格履行了面向对象的开发规范。

在 ES5 里面，我们通常会定义一个构造函数，然后使用 `new`关键字来实例化一个对象：

``` js
var SpaceShuttle = function(targetPlanet){
 this.targetPlanet = targetPlanet;
}
var zeus = new SpaceShuttle('Jupiter');
```

`class`的语法只是简单地替换了构造函数的写法：

``` js
class SpaceShuttle {
 constructor(targetPlanet){
  this.targetPlanet = targetPlanet;
 }
}
const zeus = new SpaceShuttle('Jupiter');
```

注意`class`关键字声明了一个新的函数，并在其中添加了一个会在使用`new`关键字创建新对象时调用的构造函数。



#### constructor

`constructor()`方法是类的默认方法，通过`new`命令生成对象实例时，自动调用该方法。一个类必须有`constructor()`方法，如果没有显式定义，一个空的`constructor()`方法会被默认添加。

```javascript
class Point {
}

// 等同于
class Point {
  constructor() {}
}
```

上面代码中，定义了一个空的类`Point`，JavaScript 引擎会自动为它添加一个空的`constructor()`方法。

`constructor()`方法默认返回实例对象（即`this`），完全可以指定返回另外一个对象。

```javascript
class Foo {
  constructor() {
    return Object.create(null);
  }
}

new Foo() instanceof Foo
// false
```

上面代码中，`constructor()`函数返回一个全新的对象，结果导致实例对象不是`Foo`类的实例。

类必须使用`new`调用，否则会报错。这是它跟普通构造函数的一个主要区别，后者不用`new`也可以执行。

```javascript
class Foo {
  constructor() {
    return Object.create(null);
  }
}

Foo()  // // TypeError: Class constructor Foo cannot be invoked without 'new'
```


#### getter 和 setter

与 ES5 一样，在“类”的内部可以使用`get`和`set`关键字，对某个属性设置存值函数和取值函数，拦截该属性的存取行为。

```javascript
class MyClass {
  constructor() {
    // ...
  }
  get prop() {
    return 'getter';
  }
  set prop(value) {
    console.log('setter: '+value);
  }
}

let inst = new MyClass();

inst.prop = 123;
// setter: 123

inst.prop
// 'getter'
```

上面代码中，`prop`属性有对应的存值函数和取值函数，因此赋值和读取行为都被自定义了。

存值函数和取值函数是设置在属性的 Descriptor 对象上的。

```javascript
class CustomHTMLElement {
  constructor(element) {
    this.element = element;
  }

  get html() {
    return this.element.innerHTML;
  }

  set html(value) {
    this.element.innerHTML = value;
  }
}

var descriptor = Object.getOwnPropertyDescriptor(
  CustomHTMLElement.prototype, "html"
);

"get" in descriptor  // true
"set" in descriptor  // true
```

上面代码中，存值函数和取值函数是定义在`html`属性的描述对象上面，这与 ES5 完全一致。





### 严格模式

ES6 的模块自动采用严格模式，不管你有没有在模块头部加上`"use strict";`。

严格模式主要有以下限制。

- 变量必须声明后再使用
- 函数的参数不能有同名属性，否则报错
- 不能使用`with`语句
- 不能对只读属性赋值，否则报错
- 不能使用前缀 0 表示八进制数，否则报错
- 不能删除不可删除的属性，否则报错
- 不能删除变量`delete prop`，会报错，只能删除属性`delete global[prop]`
- `eval`不会在它的外层作用域引入变量
- `eval`和`arguments`不能被重新赋值
- `arguments`不会自动反映函数参数的变化
- 不能使用`arguments.callee`
- 不能使用`arguments.caller`
- 禁止`this`指向全局对象
- 不能使用`fn.caller`和`fn.arguments`获取函数调用的堆栈
- 增加了保留字（比如`protected`、`static`和`interface`）

其中，尤其需要注意`this`的限制。ES6 模块之中，顶层的`this`指向`undefined`，即不应该在顶层代码使用`this`。

## 

