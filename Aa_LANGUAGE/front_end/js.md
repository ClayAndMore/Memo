tags: [前端] date: 2016-08-04


###  写在前面
JavaScript语句是发送给浏览器的命令，这些命令的作用是告诉浏览器要做的事情。
是一门脚本语言，主流浏览器都支持js,可以让网页呈现各种动态效果，灵活的实现很多页面交互功能
使用`<script>`标签在网页中插入JavaScript，一般放入head或者body中
`<script type = "text/javascript">`表示在`<script></script>`之间的是文本类型text，javascript是为了告诉浏览器里面的文本是属于JavaScript语言。

### 引用js外部文件
文件后缀通常为.js。
在html中：
`<script src = "script.js"></script>`

```JavaScript
<script type = "text/javascript">
    alert("hello aima!");
</script>
```
行的结束就意味着语句的结束，通常在结尾加上一个分号来表示语句的结束。可以不写，但是养成良好的编码习惯。

### 注释：
单行注释//
多行注释/**/

### 变量
用关键字var
var aima = 8;
可以重复赋值：
var aima = "aima";

### 函数
语法：
function 函数名（）{
​    函数代码；
}
### 输出内容
document.write() ,用于直接先html输出流写内容。

```js
document.write("i love aima");

var aimaWord = "hello aima!";
document.write(aimaWord);
document.write(aimaWord + "i love aima"); 
document.write(aimaWord + "<br>"); //输出helloword后，再输出一个换行符
```

### 警告（alert消息对话框）
我们在访问网站的时候，有时候会弹出小窗口，这个窗口就是用alert来实现的
语法：
alert（字符串或者变量）
```js
<script type = "text/javascript">
    alert("hello!");
</script>
```
弹出消息对话框，肯定要包含一个确定按钮。
常用alert进行调试

### DOM结构
DOM（文档对象模型）将html文档呈现为带有元素、属性和文本的树结构（节点树）。
### 通过id获取元素
document.getElementById("id")  //返回结果null 或 object
### innerHTML属性
innerHTML属性用于获取或替换HTML元素的内容
语法：
​    Object.innerHTML 
eg:
通过id="aima"获取<div>元素，并将元素的内容输出和改变元素内容。
html代码：`<div id="aima"></div>`
js代码：`document.getElementById("aima").innerHTML = " 爱码”`

### 改变HTML样式
DOM允许JavaScript改变HTML元素的样式。
语法：
Object style.property = new style;
object是获取的元素对象。
property 基本属性表
eg:
改变div元素的样式，将字体颜色改为红色，字号改为12px.
```js
<script>
    var aimaChar = document.getElementById("aima");
    aimaChar.style.color = "#ff0000";
    aimaChar.style.fontSize = "12px"
</script>
```
并不是属性表中的属性和html中一样，比如上面的fontSize 和 html 中的font-size

### 控制类名（className属性）
className 属性设置或返回元素的class属性
语法：
object.className = classname
作用：
获取元素的class属性
为网页内的某个元素指定一个css样式来更改该元素的外观
html:`<div id = "aima" class = "aimastyle"> Hello aimaonline!</div>`
js: `var aimaChar = document.getElementById("aima");`
​    `aimaChar.className = "newstyle"`

### js对象
对象拥有属性和方法：
属性是和对象相关的值，访问方式：
`对象名.属性名` 如：`str.length`
方法是对象的相关动作，访问方式：
`对象名.方法名（）`

### 创建对象实例
这个例子创建了对象的一个新实例，并向其添加了四个属性：
```
person=new Object();
person.firstname="John";
person.lastname="Doe";
person.age=50;
person.eyecolor="blue";
```
上面的话可代替之：
`person={firstname:"John",lastname:"Doe",age:50,eyecolor:"blue"};`

### in循环
in语句循环便利对象的属性
```
var person={fname:"John",lname:"Doe",age:25}; 
for (x in person)
{
    txt=txt + person[x];
}
```
输出：JohnDoe25

### 数字对象
* 数字不分为整数类型和浮点型类型，所有的数字都是由浮点型类型。

* 整数（不使用小数点或指数计数法）最多为 15 位。
  小数的最大位数是 17，但是浮点运算并不总是 100% 准确：
  `var x = 0.2+0.1;`// 输出结果为 0.30000000000000004

#### 无穷大（Infinity）
当数字运算结果超过了JavaScript所能表示的数字上限（溢出），结果为一个特殊的无穷大（infinity）值，在JavaScript中以Infinity表示。同样地，当负数的值超过了JavaScript所能表示的负数范围，结果为负无穷大，在JavaScript中以-Infinity表示。无穷大值的行为特性和我们所期望的是一致的：基于它们的加、减、乘和除运算结果还是无穷大（当然还保留它们的正负号）。
```
myNumber=2;
while (myNumber!=Infinity)
{
    myNumber=myNumber*myNumber; // 重复计算直到 myNumber 等于 Infinity
}
```

#### NaN非数字值
NaN 属性是代表非数字值的特殊值。该属性用于指示某个值不是数字。可以把 Number 对象设置为该值，来指示其不是数字值。
你可以使用 isNaN() 全局函数来判断一个值是否是 NaN 值。
```
var x = 1000 / "Apple";
isNaN(x); // 返回 true
var y = 100 / "1000";
isNaN(y); // 返回 false
```

#### 数字可以是数字或者对象
数字可以进行初始化 ，还可以对数字对象初始化
```
var x = 123;
var y = new Number(123);
typeof(x) // 返回 Number
typeof(y) // 返回 Object
```

### 函数
* 函数表达式
  `var x = function(a,b) {return a*b};`
  以上函数是一个匿名函数（函数没有名称）。
  函数存储在变量中，不需要函数名称，通常通过变量名来调用。
* function()构造函数
  函数可以通过内置的函数构造器来定义，
  `var myFunction = new Function("a","b","return a*b");`
  上面可以把new去掉，很多时候要避免new关键字。
* 自调用函数
  函数表达式可以 "自调用"。
  自调用表达式会自动调用。
  如果表达式后面紧跟 () ，则会自动调用。
  不能自调用声明的函数。
  通过添加括号，来说明它是一个函数表达式：
```
(function () {
    var x = "Hello!!";      // 我将调用自己
})();
```
* 函数定义作为对象的属性，称之为对象方法。
  函数如果用于创建新的对象，称之为对象的构造函数。

#### 函数参数
Arguments对象
如果函数调用时设置了过多的参数，参数将无法被引用，因为无法找到对应的参数名。 只能使用 arguments 对象来调用。
JavaScript 函数有个内置的对象 arguments 对象。
argument 对象包含了函数调用的参数数组。
通过这种方式你可以很方便的找到最后一个参数的值：
```
x = findMax(1, 123, 500, 115, 44, 88);
function findMax() {
    var i, max = 0;
    for (i = 0; i < arguments.length; i++) {
        if (arguments[i] > max) {
            max = arguments[i];
        }
    }
    return max;
}
```

#### 函数闭包
函数闭包可以实现对一个变量进行封装，比如一个计数变量，如果声明成全局变量当然谁都可以访问，如果让制定的函数来做，函数内的私有变量在调用函数时初始，在函数执行后会被销毁，那么无法完成基数，所以让函数只执行一次，通过函数内的函数来访问，便可以实现：
```
var add = (function () {
    var counter = 0;
    return function () {return counter += 1;}
})();

add();
add();
add();

// 计数器为 3
```