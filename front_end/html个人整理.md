---
title: "html个人整理.md"
date: 2016-07-26  17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---



### 说明
B/S系统中服务器端交付给客户端的数据绝大数都是HTML文档。
Web 浏览器的作用是读取 HTML 文档，并以网页的形式显示出它们。
浏览器不会显示 HTML 标签，而是使用标签来解释页面的内容。
就是符合HTML文档规范的字符串。
使用者角度看，有几大功能：
1. 丰富的展现。文字，图像，声音，视频。
2. 超链接。
3. DHTML技术，使用客户端脚本来实现动态内容。


### 规范
先看一个文档示例：

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtmll/DTD/xhtmll-transitional.dtd">

<html xmlns = "http://www.w3c.org/1999/xhtml">
    
    <head>
        <title>这是HTML标题</title>
    </head>
    <body>
        <font color =　"red" >这是HTML内容</font>
        <a href="http://www.cnblogs.cocm/">这是一个超链接</a>
    </body>
</html>
```

有两种理解方式，一种将其理解成字符串，一种理解成树状的数据结构。
​    

* 开头<!DOCTYPE> 元素，说明该HTML文档采用了什么规范。大写的DOCTYPE很重要，特别是对于旧的浏览器
* 通过添加<!DOCTYPE……>标签在第一行，其中…部分是HTML的版本。**对于HTML5，使用`<!DOCTYPE html >`**。
* HTML文档只有一个根节点，就是<html> </html>表示的节点，文本描述网页
* head节点容纳文档标题, 元数据元素，如link、meta、title和style，通常位于head元素内部。
* body节点容纳文档内容，body 与 /body 之间的文本是可见的页面内容
* h1> 与 /h1 之间的文本被显示为标题
* p 与 /p 之间的文本被显示为段落

eg:

```html
<!DOCTYPE html>
<html>
  <head>
    <!-- metadata elements -->
  </head>
  <body>
    <!-- page contents -->
  </body>
</html>
```



### 标签元素类型分类

* 块级元素 ：可以简单的理解为在新行开始的元素，就是内容会显示在下一行
    `<div>标签`：是块级元素，浏览器会在其前后显式折行。
    常用属性，id，class，style
* 内联元素 ：可以简单的理解为没在新行开始的元素，可以都在一个行，内容都在同一行
    `<span>标签`: 是内联元素，可以作为文本的容器，可用于为部分文本设置样式属性
    扩展

* `<div>` 可定义文档中的分区或节（division/section）。
  `<div>` 标签可以把文档分割为独立的、不同的部分。它可以用作严格的组织工具，并且不使用任何格式与其关联。
* `<hr />` 标签在 HTML 页面中创建水平线。
* 注释：开始括号之后（左边的括号）需要紧跟一个叹号，结束括号之前（右边的括号）不需要。
  `<!-- This is a comment -->`
* 当显示页面时，浏览器会移除源代码中多余的空格和空行。所有连续的空格或空行都会被算作一个空格。需要注意的是，HTML 代码中的所有连续的空行（换行）也被显示为一个空格。

```html
<a href = "http://www.w3school.com.cn"> this is a link </a>
<img src="/i/eg_w3school.gif" width="300" height="120" />
```

* 在开始标签中添加斜杠，比如` <br />`，是关闭空元素的正确方法，HTML、XHTML 和 XML 都接受这种方式。
  即使`<br>` 在所有浏览器中都是有效的，但使用 `<br />` 其实是更长远的保障。
* HTML 标签对大小写不敏感：`<P>` 等同于 `<p>`。许多网站都使用大写的 HTML 标签。
  W3School 使用的是小写标签，因为万维网联盟（W3C）在 HTML 4 中推荐使用小写，而在未来 (X)HTML 版本中强制使用小写。
  ​      



### html属性

HTML 标签可以拥有属性。属性提供了有关 HTML 元素的更多的信息。
属性总是以名称/值对的形式出现，比如：name="value"。
属性总是在 HTML 元素的开始标签中规定。
属性值应该始终被包括在引号内。双引号是最常用的，不过使用单引号也没有问题。
在某些个别的情况下，比如属性值本身就含有双引号，那么您必须使用单引号

style属性提供了一种改变所有 HTML 元素的样式的通用方法。
样式是 HTML 4 引入的，它是一种新的首选的改变 HTML 元素样式的方式。通过 HTML 样式，能够通过使用 style 属性直接将样式添加到 HTML 元素，或者间接地在独立的样式表中（CSS 文件）进行定义。



## HTML5

HTML5引入了更多的描述性HTML标签。这些包括主页，页眉，页脚，导航栏，视频，文章，部分和其他。

例如，使用main元素包含子元素：

```html
<main> 
  <h1>Hello World</h1>
  <p>Hello Paragraph</p>
</main>
```



### 文本

h p 等。



### textarea 文本域

当用户输入较多内容的大段文本时
语法：
`<textarea rows = "行数" cols= "列数">文本</textarea>`
列数：每行显示多少字
行数：共有多少行



### img

可以使用img元素加src属性来展示图片：

`<img src = "图片地址" alt = "下载失败时替换文本" title = "提示文本">` 

注意，img 元素是自封闭的。

所有的img元素一定要有 alt 属性，alt属性中的字符串内容用于当图片加载失败时显示在页面上的文字：

`<img src="https://www.freecatphotoapp.com/your-image.jpg" alt="A business cat wearing a necktie.">`



### a （anchor）

a元素可以用于外部网页连接，使用href属性写入链接地址

`<a href="https://freecodecamp.org">this links to freecodecamp.org</a>`

`<a href = "目标网址" title ="鼠标滑过显式的文本">链接显式的文本</a>`

如果用于内部跳转，可以使用href属性中加#加跳转目标的id:

```html
<a href="#contacts-header">Contacts</a>
...
<h2 id="contacts-header">Contacts</h2>
```

p元素内部镶嵌a元素：

``` html
<p>View more <a href="https://freecatphotoapp.com">cat photos</a></p>
```

死链接，有时需要创建 a 元素，但是后续的连接地址不确定，会用js操作，我们可以用“#(hash symbol) 井号” 创建死链接：

`<a href="#"></a> `

a 元素内镶嵌图片：

``` html
<a href="#"><img src="https://bit.ly/fcc-relaxing-cat" alt="A cute orange cat lying on its back."></a>
```

这样图片就可变成可点击的了



### input

语法：
`<input type = "text/password" name = "名称" value ="文本”/>` ,  注意为自封闭的。
type : text 为文本输入框，password： 为密码输入框
name:  为文本框命名，以备后台程序ASP、PHP使用。
value： 为文本输入框设置默认值（一般起到提示作用）

其他属性：

``` html
# Placeholder 占位符，缺省值
<input type="text"  placeholder="cat photo URL" >
# 如果要求input 在 submit 时，必填，可以用 requied 属性
<input type="text" placeholder="cat photo URL" required>
```



### form表单

网站与用户交互,所有表单控件（文本框、文本域、按钮、单选框、复选框） 都必须放在`<form></form>`标签之间（否则用户输入的信息可提交不到服务器）。
语法：
`<form method = "传送方式" action = "服务器文件/服务地址">`
method:传送的方式，(get/post)
action:浏览者输入的数据被传送到的地方，比如一个JSP页面，一个接口地址

```xml
<form method = "post" action="save.do">
    <label for = "username">用户名：</lable>
    <input type = "tesxt" name = "username"/>
    <lable for ="pass">密码:</lable>
    <input type = "password" name = "pass"/>
</form>

<form action="https://freecatphotoapp.com/submit-cat-photo">
    <input type="text" placeholder="cat photo URL">
 </form>
```



### Button 按钮

` <input type = "submit"/"reset" value = "提交">`
type 的值设置为submit时，按钮才有提交作用，为reset时有重置作用
value ：按钮上显示的文字

承接上方表单：

``` html
  <form action="https://freecatphotoapp.com/submit-cat-photo">
    <input type="text" placeholder="cat photo URL">
    <button type="submit">Submit</button>
  </form>
```





### 列表

```xml
<ul> :无序列表
<ol> :有序列表
<li> :列表项
eg:
<ul>
    <li>信息</li>
    <li>信息</li>
</ul>
```

上面显式的信息默认会在每项前面加个原点，如果去除原点需要li{list-style-type:none;
有序标签前面会默认出现数字排序



### table 表格

网上的一些清单，人员信息等，我们就需要的是table标签
包括的元素：table、tbody、tr、td等

* table 整个表格的开始
* tr 表格的一行
* th 表头单元格
* td 表格的一个单元格，一行有几对td
* `<caption>Optional table caption.</caption>` ,表格的标题

几个属性：border，style，class，cellspacing，cellpadding
border： 边框 
cellspacing： 单元格内外部间距
cellpadding:  单元格内的外部间距
合并：
colspan :列合并 
rowspan: 行合并

```xml
<!--行合并-->
<table border = "1" width = "300px">
    <tr height = "30px">
        <td colspan = "2"></td>
    </tr>
    <tr height = "30px">
            <td></td>
            <td></td>
    </tr>
</table>
<!--列合并-->
<table border = "1" width = "300px">
    <tr height =　"30px">
        <td rowspan = "2"></td>
        <td></td>
    </tr>
    <tr height = "30px">
        <td></td>
    </tr>
</table>
```



### label 标签 

`<label for = "空间id名称">显示文字</label>`
for 是当你点击一个label会自动把焦点移动到for对应的控件



### Radio

单选按钮是一种input, 

```html
<label> 
  <input type="radio" name="indoor-outdoor">Indoor 
</label>
```

单选按钮都可以嵌套在其自己的label元素内。 通过将输入元素包装在标签元素内部，它将自动将单选按钮输入与其周围的标签元素相关联。

单选按钮组：

``` html
<label for="indoor"> 
    <input id="indoor" type="radio" name="indoor-outdoor">Indoor 
</label>
<label for="outdoor"> 
    <input id="outdoor" type="radio" name="indoor-outdoor">Indoor 
</label>
```

单选按钮应具有相同的名称属性，以创建单选按钮组。 

for 属性的值和输入元素的id属性值一致，这样就创建了一种链接关系。

选择任何一个单选按钮将自动取消选择同一组中的其他按钮，从而确保用户仅提供一个答案。

设置默认选择：

``` html
使用 checked 选择默认的值
<input type="radio" name="test-name" checked> 
```



### checkbox

复选框为多选按钮，通过设置 input 的 type=“checkbox” 来声明

``` html
  <form action="https://freecatphotoapp.com/submit-cat-photo">
    <label for="loving"><input id="loving" type="checkbox" name="personality"> Loving</label>
    <label for="loving"><input id="loving" type="checkbox" name="personality"> Loving</label>
    <label for="loving"><input id="loving" type="checkbox" name="personality"> Loving</label>
    <br>
    <input type="text" placeholder="cat photo URL" required>
    <button type="submit">Submit</button>
  </form>
```

和 redio，一样，相关的复选框name属性应该设置成一样， 也可以使用checked属性。



### value 属性

提交表单时，数据被发送到服务器，并包含所选选项的条目。类型为radio和checkbox的输入会从value属性报告它们的值。

```html
<label for="indoor">
  <input id="indoor" value="indoor" type="radio" name="indoor-outdoor">Indoor
</label>
<label for="outdoor">
  <input id="outdoor" value="outdoor" type="radio" name="indoor-outdoor">Outdoor
</label>
```



### select下拉列表框
```xml
<select name ="" id = "">
    <option value = "1">第一项(默认显示）</option>
    <option value = "2">第二项</option>
</select>
```