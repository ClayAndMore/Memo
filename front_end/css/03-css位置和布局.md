---
title: "03-css 位置和布局.md"
date: 2016-07-27  17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["css"]
categories: ["前端"]
author: "Claymore"

---



### 盒子模型

https://www.cnblogs.com/linjiqin/p/3556497.html

数值调成负值将使元素变大：

``` css
<style>
  .injected-text {
    margin-bottom: -25px;
    text-align: center;
  }

  .box {
    border-style: solid;
    border-color: black;
    border-width: 5px;
    text-align: center;
  }

  .yellow-box {
    background-color: yellow;
    padding: 10px;
  }

  .red-box {
    background-color: crimson;
    color: #fff;
    padding: 20px;
    margin: -15px;
  }

  .blue-box {
    background-color: blue;
    color: #fff;
    padding: 20px;
    margin: 20px;
  }
</style>

<div class="box yellow-box">
  <h5 class="box red-box">padding</h5>
  <h5 class="box blue-box">padding</h5>
</div>
```



### px em rem





### 空间在网页的位置

position用来设定元素的定位类型，有absolute（绝对定位）、relative（相对定位）、static（静态定位，默认值）、fixed（固定定位）四种。CSS偏移属性(top或bottom、left或right)用于调整位置。

```CSS
.myi{
	position:absolute;
	top:0;
	left:0;
	}
.myr{
	position:relative;
	top:-125px;
	left:425px;
	}
```

* static：默认。位置设置为 static 的元素，它始终会处于页面流给予的位置（static元素会忽略任何 top、bottom、left 或 right 声明）。
* relative：位置被设置为 relative 的元素，可将其移至相对于其正常位置的地方，就是相对于于上一级dom结点而言的相对位置。因此 "left:20" 会将元素移至元素正常位置左边 20 个像素的位置。
* absolute：位置设置为 absolute 的元素，可定位于相对于包含它的元素的指定坐标。它将元素锁定在相对于其父容器的位置上。与相对位置不同，这将从文档的正常流中删除元素，因此周围的项将忽略它。
* fixed：位置被设置为 fixed 的元素，可定位于相对于浏览器窗口的指定坐标。不论窗口滚动与否，元素都会留在那个位置。工作于 IE7（strict 模式）。 会从文档的常规流程中删除该元素。固定位置和绝对位置的一个关键区别是，当用户滚动时，固定位置的元素不会移动。

绝对定位的一个细微之处是，它将相对于最接近位置的祖先被锁定。如果你忘记给父项添加位置规则(这通常使用position: relative;)，浏览器将继续查找该链，并最终默认为body标签。


#### float 浮动

float 为浮动属性，浮动元素从文档的正常流中移除，并推到包含它们的父元素的左边或右边。它通常与width属性一起使用，用来指定被浮动元素需要多少水平空间。

``` html
<head>
  <style>
    #left {
      float: left;
      width: 50%;
    }
    #right {
      float: right;
      width: 40%;
    }
    aside, section {
      padding: 2px;
      background-color: #ccc;
    }
  </style>
</head>
<body>
  <header>
    <h1>Welcome!</h1>
  </header>
  <section id="left">
    <h2>Content</h2>
    <p>Good stuff</p>
  </section>
  <aside id="right">
    <h2>Sidebar</h2>
    <p>Links</p>
  </aside>
</body>
```

left 和 right 将在一行排显示



#### z-index 深度

当元素的位置重叠时（例如，使用position：absolute | relative | fixed | sticky），默认情况下，HTML标记中后面出现的元素将显示在其他元素的顶部。

 但是，z-index属性可以指定元素堆叠的顺序。 它必须是整数（即整数，而不是十进制），并且元素的z-index属性的值越高，显示越靠前。

``` html
<style>
  div {
    width: 60%;
    height: 200px;
    margin-top: 20px;
  }

  .first {
    background-color: red;
    position: absolute;
    z-index: 2;
  }
  .second {
    background-color: blue;
    position: absolute;
    left: 40px;
    top: 50px;
    z-index: 1;
  }
</style>

<div class="first"></div>
<div class="second"></div>
```

也可以使用负值降低优先级 ： z-index: -1;



#### 使用 margin 水平居中

另一种定位技术是水平居中块元素。一种方法是将其边值设置为auto。

``` html
<style>
  div {
    background-color: blue;
    height: 100px;
    width: 100px;
    margin: auto;
  }
</style>
<div></div>
```

这种方法也适用于图像。

图像默认为内联元素，但是当你将display属性设置为block时，可以将其更改为块元素。



