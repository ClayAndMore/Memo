---
title: css
date: 2016-07-27 11:59:57
categories: 前端
tags: [前端,css]
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
```html
span{
    font-size:12px;
    color:red;
}
```

css注释代码，用/*注释语句*/来标明

### css样式代码的插入形式
内联式：
`<span style = "color:red">这里的文字是红色。</span>`
并且css样式代码要写在style=""双引号中，如果多条css样式代码设置可以写在一起，中间用分号隔开：
`<span style = "color.red; font-size:12px;">这里文字是红色</span>`
嵌入式：
把css样式代码写在`<style type = "text/css"></style>"标签之间
```html
<style type = "text/css">
span{
color:red;
}
</style>
```
外部式
把css代码写在一个单独的外部文件中，这个文件以.css为扩展名。在`<head>`内，用'<link>'标签将css样式文件连接到html文件内
`<link href = "aima.css" rel="stylesheet" type = "text/css"/>`
rel = "sylesheet" type = "text/css"是固定写法不可修改

如果三种方式都使用了，那么他们的优先级：
内联式>嵌入式>外部式

### 选择器 
#### 标签选择器
就是html代码中的标签，如`<html>,<body>,<h1>,<p>,<img>`
#### 类选择器
类选择器在css样式代码中是最常用到的.stylename 
语法：`.类选择器名称{css样式代码;}`
英文圆点开头
其中类选择器可以任意起名（英文）
在css文件中是有点的，在html引用的话是没有点的
#### ID选择器
在一个HTML中，id选择器只能使用一次
`#styleName`
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
![](http://7xs1eq.com1.z0.glb.clouddn.com/css%E5%9F%BA%E7%A1%80%E6%A0%B7%E5%BC%8F%E4%BB%8B%E7%BB%8D.png)
#### 基础框模式样式介绍
![](http://7xs1eq.com1.z0.glb.clouddn.com/css%E6%A1%86%E6%A8%A1%E5%BC%8F%E6%A0%B7%E5%BC%8F%E4%BB%8B%E7%BB%8D.png)

#### 空间在网页的位置
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
第一个是绝对位置，就是在页面上的位置，但是会受到其他控件，和观看设备的干扰，容易把图片变形
第二个相对位置，就是相对于于上一级dom结点而言的相对位置。
position用来设定元素的定位类型，有absolute（绝对定位）、relative（相对定位）、static（静态定位，默认值）、fixed（固定定位）四种。

* static：默认。位置设置为 static 的元素，它始终会处于页面流给予的位置（static元素会忽略任何 top、bottom、left 或 right 声明）。
* relative：位置被设置为 relative 的元素，可将其移至相对于其正常位置的地方，因此 "left:20" 会将元素移至元素正常位置左边 20 个像素的位置。
* absolute：位置设置为 absolute 的元素，可定位于相对于包含它的元素的指定坐标。此元素的位置可通过 "left"、"top"、"right" 以及 "bottom" 属性来规定。
* fixed：位置被设置为 fixed 的元素，可定位于相对于浏览器窗口的指定坐标。此元素的位置可通过 "left"、"top"、"right" 以及"bottom" 属性来规定。不论窗口滚动与否，元素都会留在那个位置。工作于 IE7（strict 模式）。