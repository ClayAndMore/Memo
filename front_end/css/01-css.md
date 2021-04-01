---
title: "01-css.md"
date: 2016-07-27  17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["css"]
categories: ["前端"]
author: "Claymore"

---



### CSS 概述
* CSS 指层叠样式表 (Cascading Style Sheets),主要是定义于定义HTML内容在浏览器的显式样式
* 样式定义如何显示 HTML 元素
* 样式通常存储在样式表中
* 把样式添加到 HTML 4.0 中，是为了解决内容与表现分离的问题
* 外部样式表可以极大提高工作效率
* 外部样式表通常存储在 CSS 文件中
* 多个样式定义可层叠为一
* 通过定义某个样式，可以让不同网页位置的文字有着统一的字体、字号或者颜色等。

### css 语法
css样式由选择符合声明组成，声明由属性和值组成
选择符又称选择器，指明网页中应用样式规则的元素
声明：在{}中的就是声明，属性和值之间用:，多条声明用;

```css
span{
    font-size:12px;
    color:red;
}
```

css注释代码，用/*注释语句*/来标明

**注意CSS是区分大小写的，所以要注意大小写。**



### css样式代码的插入形式
#### 内联式

``` css
<span style = "color:red;">这里的文字是红色。</span>
<span style = "color.red; font-size:12px;">这里文字是红色</span>
```

并且css样式代码要写在style=""双引号中，如果多条css样式代码设置可以写在一起，中间用分号隔开, 注意不要丢失分号。

#### 嵌入式
在html文件中，把css样式代码写在`<style type = "text/css"></style >"标签之间

```html
<style type = "text/css">
span{
color:red;
}
</style>
```
这样所有的 span 元素都是 红色的。

#### 外部式

把css代码写在一个单独的外部文件中，这个文件以.css为扩展名。

在`<head>`内，用'<link>'标签将css样式文件连接到html文件内

``` html
<link href = "aima.css" rel="stylesheet" type = "text/css"/>
```


rel = "sylesheet" type = "text/css"是固定写法不可修改

如果三种方式都使用了，那么他们的优先级：
**内联式>嵌入式>外部式**



### 选择器 
#### 标签选择器
就是html代码中的标签，如`<html>,<body>,<h1>,<p>,<img>`
#### 类选择器
类选择器在css样式代码中是最常用到的.stylename 
语法：`.类选择器名称{css样式代码;}`

``` html
<style>
  .blue-text {
    color: blue;
  }
</style>

<h2 class="blue-text">CatPhotoApp</h2>
```

英文圆点开头,其中类选择器可以任意起名（英文）, 对应某个元素的类


#### ID选择器
在一个HTML中，id选择器只能使用一次
`#styleName`



#### 属性选择器

我们可以使用某些属性来规定有该属性组件的样式：

``` html
<style>
  [type='checkbox'] {
  margin: 10px 0px 15px 0px;
  }
</style>

<label><input type="radio" name="indoor-outdoor" checked> Indoor</label>
<label><input type="radio" name="indoor-outdoor"> Outdoor</label><br>
<label><input type="checkbox" name="personality" checked> Loving</label>
<label><input type="checkbox" name="personality"> Lazy</label>
<label><input type="checkbox" name="personality"> Energetic</label><br>
```





#### 子选择器
即大于符号（>） 
```html
<div> class = "aaa"
    <div> class = "bbb"
    </div>
</div>
```
可以通过.aaa>.bbb来选择第二个div层
#### 通用选择器
它是功能最强大的选择器，用一个星号指定，匹配html中所有标签元素，如：
`*{color:red;}` 这样热议标签元素字体颜色全部设置为红色

#### 伪类选择器
它允许给html中不存在的标签（标签的某种状态）设置样式，比如说我们给html中一个标签元素的鼠标滑过的状态来设置字体颜色
如：`a:hover{color:red;}`
hover ：鼠标滑过
link: 链接状态
active:活动当中的，比如选中
visit：点击过的

#### 分组选择符
当想为html中多个标签设置同一个样式时，可以使用分组选择符，就是一个逗号
`h1,span{color:red;}`
相当于如下：

'h1{color:red;} span{color:red;}'

### 基础样式介绍

#### 文字样式

文字大小

``` html
<p style="font-size: 30px;">Click here to view more</p>
<!-- 还可以改变默认的元素大小 -->
h4 {
	font-size: 27px;
}
```



设置字体：

``` html
<p style="font-family: monospace;">Click here to view more</p>

<!-- 导入其他字体 -->
<link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet" type="text/css">
<style>
  h2 {
    font-family: Lobster;
  }

</style>
<h2>CatPhotoApp</h2>

<!--备用字体 -->
font-family: FAMILY_NAME, GENERIC_NAME;
GENERIC_NAME 是可选的，当其他指定的字体不可用时，它是备用字体。
```

https://fonts.google.com/ 上有很多免费字体， 我们可以通过link来导入

**标签和样式等效**

| 功能   | tag    | css                                      |
| ------ | ------ | ---------------------------------------- |
| 加粗   | strong | font-weight: bold;  或 font-weight: 800; |
| 下划线 | u      | text-decoration: underline;              |
| 斜体   | em     | font-style: italic;                      |
| 删除线 | s      | text-decoration: line-through;           |

eg，如加粗：

``` html
<style>
p{
	font-weight: bold;
}
</style>
<p> sss </p>
<!-- 实际等效于 -->
<p>
    <strong>sss</strong>
</p>
```

**使用 text-transform 改变文字内容**

这是一种方便的方法，可以确保网页上的文本一致地显示，而不必更改实际HTML元素的文本内容。

``` html
h4 {
text-transform: uppercase;
} 
<h4> transform me </h4>
```

最终显示为 TRANSFOR ME

几个可选项：

* lowercase  -  transform me
* uppercase  -  TRANSFOR ME
* capitalize   -  Transform Me
* initial        -    默认值
* inherit     - 使用父元素的 text-transform 值
* none     -   用原始的元素内容

**使用 line-height 设置行高：**

CSS提供了line-height属性来改变文本块中每行的高度。顾名思义，它更改每行文本所获得的垂直空间的大小。

``` css
  p {
    font-size: 16px;
    line-height: 25px;
  }
```





#### 尺寸

width 宽度，我们可以设置图片宽度

``` html
<style>
  .smaller-image {
    width: 100px;
  }
</style>
<a href="#"><img class="smaller-image" src="https://bit.ly/fcc-relaxing-cat" alt="A cute orange cat lying on its back."></a>
```

height 和 width 相似。

CSS 属性`transform`里面的`scale()`函数，可以用来改变元素的显示比例。下面的例子把页面的段落元素放大了 2 倍：

``` css
p {
  transform:scale(2);
}
```





#### 边框

``` html
<style>
 .smaller-image {
    width: 100px;
 }
.thick-green-border {
    border-color: green;
    border-width: 10px;
    border-style: solid;
 }
</style>

<img class="smaller-image thick-green-border" src="https://bit.ly/fcc-relaxing-cat" alt="A cute orange cat lying on its back.">

```

ps，可以使用多个类来申明元素。

圆角：

``` html
border-radius: 10px;
border-radius:3px 4px 5px 6px;
<!-- 代表设置对象左上角3px圆角、右上角4px圆角、右下角5px圆角、左下角6px圆角。-->

<!-- 还可以设置为百分比：-->
border-radius: 50%;
```



#### 背景

```css
.green-background {
  background-color: green;
}
<div class="green-background"> ... </div>
```

也可以使用特殊的图片纹理作为背景，结合url函数：

```css
 background: url(https://cdn-media-1.freecodecamp.org/imgr/MJAkxbh.png);
```





#### 继承和覆盖

``` html
<style>
  body {
    background-color: black;
    color: green;
    font-family: monospace;
  }
  h1 {
    background-color: yellow;
  }

</style>

<body>
  <h1>Hello World</h1>
</body>  
```

 我们为body元素设置了绿色和字体，此时的hello world 继承了body的样式，字体为绿色，字体也替换为 monospace, 而h1的背景颜色被覆盖变为黄色。

再看一个例子：

``` html
<style>
  body {
    background-color: black;
    font-family: monospace;
    color: green;
  }
  
  .blue-text {
    color: blue;
  }

  .pink-text {
    color: pink;
  }

</style>
<h1 class="pink-text blue-text">Hello World!</h1>
```

此时我们为h1设置了两个类，两个颜色，那么此时h1的颜色会是什么呢？

**注意，class中引用的类顺序并不重要，然而，<style>部分中类声明的顺序是重要的。**

所以h1此时是粉色。

**如果有id属性的样式声明，那么id属性会覆盖class的属性**

```html
<h1 id="orange-text" class="pink-text blue-text">Hello World!</h1>
```

此时hello world的属性为橙色。

如果有内联样式声明呢，**显然内联样式是比id和类更优先的**：

``` html
<h1 id="orange-text" class="pink-text blue-text" style="color: white;" >Hello World!</h1>
```

此时字体为白色

为什么要覆盖css样式？

在许多情况下，会使用CSS库。这些可能会意外地覆盖你自己的CSS。因此，**绝对需要确保某个元素具有特定的CSS时，可以使用!important**：

``` html
<style>
#orange-text {
    color: orange;
  }
  .pink-text {
    color: pink !important; 
  }
  .blue-text {
    color: blue;
  }
</style>
<h1 id="orange-text" class="pink-text blue-text" style="color: white">Hello World!</h1>
```

此时，hello world 绝对是粉色



####  颜色

我们可以使用 6个16进制数字表示颜色：

`color: #000000 `

前面两个数字代表红色，中间两个数字代表绿色，后面两个代表蓝色。

R(red), G(green), B(blue), 000000  为黑色， FFFFFF 为白色。

数字0是十六进制代码中最小的数字，代表完全没有颜色。

数字F是十六进制代码中的最高数字，代表最大可能的亮度。

颜色数值还可以缩写：

|  Color  | Short Hex Code |
| :-----: | :------------: |
|  Cyan   |     `#0FF`     |
|  Green  |     `#0F0`     |
|   Red   |     `#F00`     |
| Fuchsia |     `#F0F`     |

每个数字代表两个，0代表00， F代表FF



另一种方式是使用 rgb 定义颜色

``` css 
body {
  background-color: rgb(255, 165, 0);
}
```

每个数字是0-255

#### 透明度

我们可以使用rgba()  a = alpha/level of opacity, α/不透明度水平来实现颜色的透明度，它的值为0到1，如创建一个透明的灰色背景：

` background-color: rgba(45, 45, 45, 0.1);`

也可以使用 opacity 属性来设置不通明度, 它的值为 0 到 1

值1是不透明的，它根本就不是透明的。值为0.5是半透明的。值为0是完全透明的。如：

``` css
opacity: 0.7;
```

也可以使用 background-color:transparent; 来定义透明的颜色。



### 变量

ccs 可以声明变量，起到一次修改，多处引用的效果，极大方便了外观使用，

声明一个自定义属性，属性名需要以两个减号（`--`）开始，属性值则可以是任何有效的CSS值。也可以是其他定义过的css值。

下面是一个用css画出来的企鹅：

``` html
<style>
  .penguin {

    /* 声明变量 */
    --penguin-skin: gray;
    --penguin-belly: white;
    --penguin-beak: orange;

    position: relative;
    margin: auto;
    display: block;
    margin-top: 5%;
    width: 300px;
    height: 300px;
  }

  .penguin-top {
    top: 10%;
    left: 25%;
    background: var(--penguin-skin, gray);
    width: 50%;
    height: 45%;
    border-radius: 70% 70% 60% 60%;
  }

  .penguin-bottom {
    top: 40%;
    left: 23.5%;
    background: var(--penguin-skin, gray);
    width: 53%;
    height: 45%;
    border-radius: 70% 70% 100% 100%;
  }

  .right-hand {
    top: 0%;
    left: -5%;
    background: var(--penguin-skin, gray);
    width: 30%;
    height: 60%;
    border-radius: 30% 30% 120% 30%;
    transform: rotate(45deg);
    z-index: -1;
  }

  .left-hand {
    top: 0%;
    left: 75%;
    background: var(--penguin-skin, gray);
    width: 30%;
    height: 60%;
    border-radius: 30% 30% 30% 120%;
    transform: rotate(-45deg);
    z-index: -1;
  }

  .right-cheek {
    top: 15%;
    left: 35%;
    background: var(--penguin-belly, white);
    width: 60%;
    height: 70%;
    border-radius: 70% 70% 60% 60%;
  }

  .left-cheek {
    top: 15%;
    left: 5%;
    background: var(--penguin-belly, white);
    width: 60%;
    height: 70%;
    border-radius: 70% 70% 60% 60%;
  }

  .belly {
    top: 60%;
    left: 2.5%;
    background: var(--penguin-belly, white);
    width: 95%;
    height: 100%;
    border-radius: 120% 120% 100% 100%;
  }

  .right-feet {
    top: 85%;
    left: 60%;
    background: var(--penguin-beak, orange);
    width: 15%;
    height: 30%;
    border-radius: 50% 50% 50% 50%;
    transform: rotate(-80deg);
    z-index: -2222;
  }

  .left-feet {
    top: 85%;
    left: 25%;
    background: var(--penguin-beak, orange);
    width: 15%;
    height: 30%;
    border-radius: 50% 50% 50% 50%;
    transform: rotate(80deg);
    z-index: -2222;
  }

  .right-eye {
    top: 45%;
    left: 60%;
    background: black;
    width: 15%;
    height: 17%;
    border-radius: 50%;
  }

  .left-eye {
    top: 45%;
    left: 25%;
    background: black;
    width: 15%;
    height: 17%;
    border-radius: 50%;
  }

  .sparkle {
    top: 25%;
    left: 15%;
    background: white;
    width: 35%;
    height: 35%;
    border-radius: 50%;
  }

  .blush-right {
    top: 65%;
    left: 15%;
    background: pink;
    width: 15%;
    height: 10%;
    border-radius: 50%;
  }

  .blush-left {
    top: 65%;
    left: 70%;
    background: pink;
    width: 15%;
    height: 10%;
    border-radius: 50%;
  }

  .beak-top {
    top: 60%;
    left: 40%;
    background: var(--penguin-beak, orange);
    width: 20%;
    height: 10%;
    border-radius: 50%;
  }

  .beak-bottom {
    top: 65%;
    left: 42%;
    background: var(--penguin-beak, orange);
    width: 16%;
    height: 10%;
    border-radius: 50%;
  }

  body {
    background:#c6faf1;
  }

  .penguin * {
    position: absolute;
  }
</style>
<div class="penguin">
  <div class="penguin-bottom">
    <div class="right-hand"></div>
    <div class="left-hand"></div>
    <div class="right-feet"></div>
    <div class="left-feet"></div>
  </div>
  <div class="penguin-top">
    <div class="right-cheek"></div>
    <div class="left-cheek"></div>
    <div class="belly"></div>
    <div class="right-eye">
      <div class="sparkle"></div>
    </div>
    <div class="left-eye">
      <div class="sparkle"></div>
    </div>
    <div class="blush-right"></div>
    <div class="blush-left"></div>
    <div class="beak-top"></div>
    <div class="beak-bottom"></div>
  </div>
</div>
```

#### 备用值

当给定的css变量值无效，我们可以使用一个备用值：

```css
background: var(--penguin-skin, black);
background-color: var(--my-var, --my-background, pink); /* 或者使用多个 */
background-color: var(--my-var, var(--my-background, pink)); /* 或者嵌套使用 */

```

如果你的变量没有设置，这将把background设置为黑色。**注意，这对于调试很有用。**

#### 兼容性

古老的IE是不支持css变量的，我们可以在使用变量前，给一个默认值，这样可以兼容旧浏览器

``` css
  .red-box {
    background: red;
    background: var(--red-color);
   }
```



#### 全局变量

:root是一个伪类选择器，它匹配文档的根元素，通常是html元素。

通过在:root中创建变量，它们将是全局可用的，并且可以从样式表中的任何其他选择器访问。

``` html
<style>
  :root {
    --penguin-skin: gray;
    --penguin-belly: pink;
    --penguin-beak: orange;
  }

  body {
    --pengui-beak: white; /* 会覆盖上方的 --pengui-beak 变量 */
    background: var(--penguin-belly, #c6faf1);
  }
</style>        
```





### 伪类和伪元素

伪类用于当已有元素处于的某个状态时，为其添加对应的样式，

伪元素用于创建一些不在文档树中的元素，并为其添加样式

**伪类的操作对象是文档树中已有的元素，而伪元素则创建了一个文档数外的元素。**

#### 伪类

一个例子：

``` html
<ul>
    <li class="first-item">我是第一个</li>
    <li>我是第二个</li></ul>

li.first-item {color: orange}
```

如果不用添加类的方法，我们可以通过给设置第一个`<li>`的`:first-child`伪类来为其添加样式。

这个时候，被修饰的`<li>`元素依然处于文档树中。

```text
li:first-child {color: orange}
```



#### 伪元素

一个例子：

```html
<p>Hello World, and wish you have a good day!</p>
```

如果想要给该段落的第一个字母添加样式，可以在第一个字母中包裹一个元素，并设置该span元素的样式：

```html
<p><span class="first">H</span>ello World, and wish you have a good day!</p>

.first {font-size: 5em;}
```

如果不创建一个`<span>`元素，我们可以通过设置`<p>`的`:first-letter`伪元素来为其添加样式。

这个时候，看起来好像是创建了一个虚拟的`<span>`元素并添加了样式，但实际上文档树中并不存在这个`<span>`元素。

```html
<p>Hello World, and wish you have a good day!</p>
p:first-letter {
    font-size: 5em;}
```



#### 冒号

CSS3规范中的要求使用双冒号(::)表示伪元素，以此来区分伪元素和伪类，比如::before和::after等伪元素使用双冒号(::)，:hover和:active等伪类使用单冒号(:)。

除了一些低于IE8版本的浏览器外，大部分浏览器都支持伪元素的双冒号(::)表示方法。

然而，除了少部分伪元素，如::backdrop必须使用双冒号，大部分伪元素都支持单冒号和双冒号的写法，比如::after，写成:after也可以正确运行。

虽然CSS3标准要求伪元素使用双冒号的写法，但也依然支持单冒号的写法。为了向后兼容，我们建议你在目前还是使用单冒号的写法。



#### 具体用法

![](https://pic2.zhimg.com/v2-a85036113478c3bc36062f76ef8e66bd_r.jpg)



![](https://pic4.zhimg.com/80/v2-e44eab840072dc00011854928fb0bcaf_720w.jpg)

 还需要再整理：

https://segmentfault.com/a/1190000000657084