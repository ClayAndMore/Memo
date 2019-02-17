tags: [前端] date: 2016-08-08


### 写在前面
AJAX = Asynchronous JavaScript and XML（异步的 JavaScript 和 XML）。
AJAX 不是新的编程语言，而是一种使用现有标准的新方法。
AJAX 是与服务器交换数据并更新部分网页的艺术，在不重新加载整个页面的情况下。
这些都是ajax原生态的写法，可跳过，看后面jquery的做法。

在AJAX中，javaScript代替了浏览器想服务器发出请求，服务器会误认为js就是浏览器，于是将信息传送给js,js将信息再写入网页中，所以我们得到了异步塞入信息的效果。

### XMLHttpRequest 对象
所有现代浏览器均支持 XMLHttpRequest 对象（IE5 和 IE6 使用 ActiveXObject）。
XMLHttpRequest 用于在后台与服务器交换数据。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

创建新的 XMLHttpRequest 对象
```html
<script language="javascript" type="text/javascript">
var xmlHttp = new XMLHttpRequest();
</script>
```
* ·open()：建立到服务器的新请求。 
* ·send()：向服务器发送请求。 
* ·abort()：退出当前请求。 
* ·readyState：提供当前 HTML 的就绪状态。 
* ·responseText：服务器返回的请求响应文本。


如需将请求发送到服务器，我们使用 XMLHttpRequest 对象的 open() 和 send() 方法：
```xml
xmlhttp.open("GET","test1.txt",true);
xmlhttp.send();
```

![](http://7xs1eq.com1.z0.glb.clouddn.com/xmlHttpRequest.png)

如果需要像 HTML 表单那样 POST 数据，请使用 setRequestHeader() 来添加 HTTP 头。然后在 send() 方法中规定您希望发送的数据：
```xml
xmlhttp.open("POST","ajax_test.asp",true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("fname=Bill&lname=Gates");
```
### onreadystatechange 事件
当请求被发送到服务器时，我们需要执行一些基于响应的任务。
每当 readyState 改变时，就会触发 onreadystatechange 事件。
readyState 属性存有 XMLHttpRequest 的状态信息。
下面是 XMLHttpRequest 对象的三个重要的属性：
![](http://7xs1eq.com1.z0.glb.clouddn.com/xmlhttpRequest%E5%B1%9E%E6%80%A7.png)
在 onreadystatechange 事件中，我们规定当服务器响应已做好被处理的准备时所执行的任务。
当 readyState 等于 4 且状态为 200 时，表示响应已就绪：
onreadystatechange 事件被触发 5 次（0 - 4），对应着 readyState 的每个变化。

### 来自服务器的响应
如需获得来自服务器的响应，请使用 XMLHttpRequest 对象的 responseText 或 responseXML 属性。
* responseText : 获得字符串形式的响应数据
* responseXML : 获得XML形式的响应数据


### JQuery Ajax
AJAX——核心XMLHttpRequest对象，而JQuery也对Ajax异步操作进行了封装，这里看一下几种常用的方式：
`$.ajax，$.post， $.get， $.getJSON`是一些简单的方法，如果要处理复杂的逻辑，还是需要用到jQuery.ajax()。
一般格式：
```js
$.ajax({
     type: 'POST',
     url: url ,
     data: data ,
     async: true,
     success: success ,
     dataType: dataType
});
```
参数描述:  
type : post和get ，数据的提交方式
url  : 必需。规定把请求发送到哪个 URL。 
data : 可选。映射或字符串值。规定连同请求**发送到服务器**的数据。 
async: 是否支持异步刷新，默认是true，支持异步刷新
success(data, textStatus, jqXHR) : 可选。请求成功时执行的回调函数。 其中的data为服务器根据dataType返回的参数进行处理后的数据，**不要跟上面的data混淆**，你也可以把这个名字改为respond等之类。
dataType : 可选。预期**服务器返回**的数据类型。
默认执行智能判断（xml、json、script 或 html）。

一些说明：

* post和get的区别：
    * get是向服务器取数据，post是改数据，但是本事上没有什么区别 
    * get方法会在IE地址栏里显示表示你提交时候所带的值，post方法不会
    * GET提交是将请求的数据附加到URL之后，用？分割、参数用&连接。并且字符串已经被加密。而post的提交是放到了http包中。从这点看来GET请求的地址栏会改变，RUL附加上了请求的数据
    * 另外一个准则是，可以重复的交互，比如取个数据，跳个页面， 用GET。不可以重复的操作， 比如创建一个条目/修改一条记录， 用POST,因为POST不能被缓存，所以浏览器不会多次提交。

* data主要方式有三种，html拼接的，json数组，form表单经serialize()序列化的；通过dataType指定，不指定智能判断。要求为Object或String类型的参数。如果已经不是字符串，将自动转换为字符串格式。











​	