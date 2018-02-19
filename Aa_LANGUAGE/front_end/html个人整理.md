---
title: html个人整理
date: 2016-07-26 10:53:00
categories: 前端
tags: [前端,html]
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

有两种理解方式，一种将其理解成字符串，一种理解成树状的数据结构。
​    
* 开头<!DOCTYPE> 元素，说明该HTML文档采用了什么规范。
* HTML文档只有一个根节点，就是<html> </html>表示的节点，文本描述网页
* head节点容纳文档标题
* body节点容纳文档内容，body 与 /body 之间的文本是可见的页面内容
* h1> 与 /h1 之间的文本被显示为标题
* p 与 /p 之间的文本被显示为段落

#### 标签元素类型分类
* 块级元素 ：可以简单的理解为在新行开始的元素，就是内容会显示在下一行
    `<div>标签`：是块级元素，浏览器会在其前后显式折行。
    常用属性，id，class，style
* 内联元素 ：可以简单的理解为没在新行开始的元素，可以都在一个行，内容都在同一行
    `<span>标签`: 是内联元素，可以作为文本的容器，可用于为部分文本设置样式属性
  扩展

* `<div>` 可定义文档中的分区或节（division/section）。
  `<div>` 标签可以把文档分割为独立的、不同的部分。它可以用作严格的组织工具，并且不使用任何格式与其关联。
* 链接通过a标签定义的 语法：
  `a href = "目标网址" title ="鼠标滑过显式的文本">链接显式的文本</a>`
* 图像是通过img定义的 语法：
  `<img src = "图片地址" alt = "下载失败时替换文本" title = "提示文本">` 
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
###table标签
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

### html属性
HTML 标签可以拥有属性。属性提供了有关 HTML 元素的更多的信息。
属性总是以名称/值对的形式出现，比如：name="value"。
属性总是在 HTML 元素的开始标签中规定。
属性值应该始终被包括在引号内。双引号是最常用的，不过使用单引号也没有问题。
在某些个别的情况下，比如属性值本身就含有双引号，那么您必须使用单引号


#### style属性
提供了一种改变所有 HTML 元素的样式的通用方法。
样式是 HTML 4 引入的，它是一种新的首选的改变 HTML 元素样式的方式。通过 HTML 样式，能够通过使用 style 属性直接将样式添加到 HTML 元素，或者间接地在独立的样式表中（CSS 文件）进行定义。


#### 背景颜色
background-color 属性为元素定义了背景颜色：
```html
<html>
<body style="background-color:yellow">
<h2 style="background-color:red">This is a heading</h2>
<p style="background-color:green">This is a paragraph.</p>
</body>
</html>
```
font-family、color 以及 font-size 属性分别定义元素中文本的字体系列、颜色和字体尺寸：
```html
<body>
<h1 style="font-family:verdana">A heading</h1>
<p style="font-family:arial;color:red;font-size:20px;">A paragraph.</p>
</body>
</html>
```
text-align 属性规定了元素中文本的水平对齐方式：
```html
<html>
<body>
<h1 style="text-align:center">This is a heading</h1>
<p>The heading above is aligned to the center of this page.</p>
</body>
</html>
```
#### form表单
网站与用户交互,所有表单控件（文本框、文本域、按钮、单选框、复选框） 都必须放在<form></form>标签之间（否则用户输入的信息可提交不到服务器）。
语法：
`<form method = "传送方式" action = "服务器文件">`
method:传送的方式，(get/post)
action:浏览者输入的数据被传送到的地方，比如一个JSP页面。
```xml
<form method = "post" action="save.do>
    <label for = "username">用户名：</lable>
    <input type = "tesxt" name = "username"/>
    <lable for ="pass">密码:</lable>
    <input type = "password" name = "pass"/>
</fom>
```
<br>
#### input文本输入框，密码输入框
语法：
`<input type = "text/password" name = "名称" value ="文本”/>`
type : text 为文本输入框，password： 为密码输入框
name:  为文本框命名，以备后台程序ASP、PHP使用。
value： 为文本输入框设置默认值（一般起到提示作用）
<br>
#### textarea 文本域
当用户输入较多内容的大段文本时
语法：
`<textarea rows = "行数" cols= "列数">文本</textarea>`
列数：每行显示多少字
行数：共有多少行
<br>
```
#### radio，checkbox单选框、复选框
语法：
`<input type = "radio/checkbox" value = "值”  name ="名称" checked = "checked"`
checke默认选中

#### select下拉列表框
​```xml
<select name ="" id = "">
    <option value = "1">第一项(默认显示）</option>
    <option value = "2">第二项</option>
</select>
```

#### Button 按钮
` <input type = "submit"/"reset" value = "提交">`
type 的值设置为submit时，按钮才有提交作用，为reset时有重置作用
value ：按钮上显示的文字

#### label 标签 

`<label for = "空间id名称">显示文字</label>`
for 是当你点击一个label会自动把焦点移动到for对应的控件