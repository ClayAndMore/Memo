tags: [FrontEnd] date: 2016-07-25


### 写在前面
jQuery 是一个兼容多浏览器的javascript库。
核心理念：write less,do more.
极大的简化了JavaScript编程。
jQuery库位于一个javaScript文件，包含了所有的jQuery函数
引用的话就和正常引用一个js文件相似就好了。
通常会把jQuery代码放到head部分的时间处理方法中。
```html
    <head>
        <script type = "text/javascript" src = "jquery.js"></script>
    </head>
```
官方下载地址：http://jquery.com/download/
版本向下兼容

### jQuery语法
jQuery语法是为HTML元素的选取编制的，可以对元素执行某些操作
基础语法：` $(selector).ation()`
$:一个jQuery对象的缩写
selector:选择符，要查找和查询的HTML元素 
action(): 对元素执行的操作

eg:
`$(this).hide()` 通过this选择 隐藏当前的HTML元素
`$("#test").hide()` 通过id选择 隐藏id="test"的元素
`$("p").hide()` 通过标签名选择 隐藏所有`<p>`元素
`$(".test").hide()` 通过class元素选择 隐藏所有class = "test"的元素

### 文档就绪函数
我们所有jQuery函数位于一个document ready函数中。
```js
$(document).ready(function(){
                --some function
})；
```
这是为了防止文档在完全加载（就绪）之前jQuery代码，如果在文档没有完全加载之前就运行函数。操作可能失败。

### jQuery选择器 
#### 元素选择器
jQuery元素选择器和属性允许您通过标签名、属性名或内容对HTML元素进行选择。
jQuery使用CSS选择器来选取HTML元素
`$("div")`选取<div>元素
`$("#demo")`选取所有id="demo"的元素
`$("div.intro")`选取所有class ="intro"的`<div>`元素
`$(“div#demo")`选取所有id = "demo" 的`<div>`元素
`$("p").css("background-color","red");` 所有 p 元素的背景颜色更改为红色：

#### 属性选择器
jQuery使用XPath表达式来选择带有给定属性的元素。
`$("[href]")` 选取所有带有href属性的元素
`$("[href = '#']")` 选取所有带有href值等于”#“的元素。
`$("[href!='#']")`选取所有带有 href 值不等于 "#" 的元素。
`$("[href$='.jpg']")`选取所有 href 值以 ".jpg" 结尾的元素。

### 事件函数
jQuery事件处理方法是jQuery中的核心函数，时间处理程序指的是当HTLM中发生某些事件时所调用的方法。
```js
<script type = "text/javascript">
    $(document).ready(function(){
        &("button").click(function(){
            &("div").hide();
            });
        });
</script>
```

在上面的例子中，当按钮的点击事件被触发时会调用一个函数：
`$("button").click(function(){..执行代码..})`
一些常用的事件函数
`$(selector).click(function)` 单机事件
`$(selector).dblclick(function)` 双击事件
`$(selector).focus(function)` 获得焦点
`$(selector).mouseover(function)` 鼠标悬停事件

### jQuery html 操作
jQuery中非常重要的部分，就是操作DOM的能力

#### 获得/设置内容
text() 设置或返回所选元素的文本内容
html() 设置或返回元素的内容（包括HTML标签）
val()  设置或返回表单字段的值
`var aima = $("#aima").text();`
`("#aima").text("Hello aima!");`

#### 添加新内容的四个jQuery方法：
append() 在被选元素的结尾插入内容
prepend() 在被选元素的开头插入内容
after() 在被选元素之后插入内容
before() 在被选元素之前插入内容
![](http://7xs1eq.com1.z0.glb.clouddn.com/jQuery%E6%B7%BB%E5%8A%A0%E5%86%85%E5%AE%B9%E7%9A%84%E6%96%B9%E6%B3%95.png)
黄色框内为被选内容

### 将您的jquery函数单独放到一个js文件中
如果您的网站包含许多页面，并且您希望您的 jQuery 函数易于维护，那么请把您的 jQuery 函数放到独立的 .js 文件中。
当我们在教程中演示 jQuery 时，会将函数直接添加到 <head> 部分中。不过，把它们放到一个单独的文件中会更好，就像这样（通过 src 属性来引用文件）：
```js
<head>
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript" src="my_jquery_functions.js"></script>
</head>
```


### easyUI

#### 引入必要文件
```xml
//引入 jQuery 核心库，这里采用的是 2.0
<scripttype="text/javascript"src="easyui/jquery.min.js"></script> 
//引入 jQuery EasyUI 核心库，这里采用的是 1.3.6
<scripttype="text/javascript"src="easyui/jquery.easyui.min.js"></script>
//引入 EasyUI 中文提示信息
<scripttype="text/javascript"src="easyui/locale/easyui-lang-zh_CN.js"></script> 
//引入自己开发的 JS 文件,没有可不写
<scripttype="text/javascript"src="js/index.js"></script> 
//引入 EasyUI 核心 UI 文件 CSS
<linkrel="stylesheet"type="text/css"href="easyui/themes/default/easyui.css"/> 
//引入 EasyUI 图标文件
<linkrel="stylesheet"type="text/css"href="easyui/themes/icon.css"/>
```

#### 加载UI组件的两种方式
* 使用class加载，格式：easyui-组件名
```xml
    <div class="easyui-dialog" id="box" title="标题" style="width:400px;height:200px;"> 内容部分 </div>
```
* 使用js调用加载
  `$('$box').dialog();`
  把上面的class属性去掉，再新建个js文件，在开头部分有引用，就可以用了

#### 来看一个完整的实例：
```xml
<!DOCTYPE html>
<html>
<head>
    <title>jQuery easyUI test</title>
    <meta charset="UTF-8" />

    <script type="text/javascript" src="easyui/jquery.min.js"></script>
    <script type="text/javascript" src="easyui/jquery.easyui.min.js"></script>
    <script type="text/javascript" src="easyui/locale/easyui-lang-zh_CN.js"></script>
    <script type="text/javascript" src="js/index.js"></script>
    <link rel="stylesheet" type="text/css" href="easyui/themes/default/easyui.css" />
    <link rel="stylesheet" type="text/css" href="easyui/themes/icon.css" />
</head>
<body>
    <!--这里是第一种方式-->
    <!--<div id = "box" class = "easyui-dialog" style = "width:400px;height:200px">
        内容部分
    </div>-->
     <!--这里是第二种方式-->
     <div id = "box" style = "width:400px;height:200px">
        内容部分
    </div>
</body>
</html>
```
index.js文件：
```js
 $(function () {
     $('box').dialog();
 });
```

#### parser解析器
Parser 解析器是专门解析渲染各种 UI 组件了，一般来说，我们并不需要使用它即可 自动完成 UI 组件的解析工作。当然，有时可能在某些环境下需要手动解析的情况。
```xml
//关闭自动解析功能，放在$(function() {})外 
$.parser.auto = false;

//解析所有 UI 
$.parser.parse();
//解析指定的 UI 
$.parser.parse('#box');
PS：使用指定 UI 解析，必须要设置父类容器才可以解析到。比如：
<divid="box"> <divclass="easyui-dialog"title="标题"style="width:400px;height:200px;"> <span>内容部分</span> </div> </div>
//UI 组件解析完毕后执行，放在$(function () {})外
$.parser.onComplete = function () { alert('UI 组件解析完毕！'); };
```

#### 面板组件
加载方式：
```xml
<!--class-->
<!--中间的data-options是说可以关闭，有个关闭选框--->
<div class-"easyui-panel" data-options="closable:true" title="面板" style="width:500px">
<!---js-->
$(function () {
$('#box').panel({
    id:''  //面板的id
    title: '面板',
    width: 500,
    height: 150,
    iconCls : 'icon-search'.//设置一个图标
    left : 100,
    top : 100,
});
    $('#box').panel('panel').css('position','absolute');//这样就能设置这个面板的位置了 
    <!--定义如何从ajax应答数据中提取内容，返回提取数据-->
});
```
#### 对话框
```xml
<div class = "easyui-dialog" style="width:400px;height:250px;">

```
对话框继承window window继承panel



### BootStrap

#### 注意事项 
这里先说几个注意事项

* 必须使用HTML5文档类型,也就说下面这样的结构是必须出现的 
```html
<!DOCTYPE html>
<html lang="en">
  ...
</html>
```
* 使用Bootstrap必须导入至少3个文件
    * 新 Bootstrap 核心 CSS 文件
      `<link rel="stylesheet"href="bootstrap.min.css">`
    * jQuery文件。务必在bootstrap.min.js 之前引入
      `<script src="jquery.min.js"></script>`

    * 最新的 Bootstrap 核心 JavaScript 文件
      `<script src="bootstrap.min.js"></script>`