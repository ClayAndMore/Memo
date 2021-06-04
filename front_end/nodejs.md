---
title: "nodejs.md"
date:  2017-06-30 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---



### Node安装

官网：https://nodejs.org/en/download/

 复制Linux Binaries(X86/x64) 64bit 的链接。

在linux下：

`wget 连接地址·` 下载到相关目录下。

解压： `tar vf -c 目标目录`

建立软连接，将node,和npm 放到全局：

`ln -s 解压路径/bin/node /usr/local/bin/`

`ln -s 解压路径/bin/npm /usr/local/bin/`

检查：

`node -v`

`npm -v`



### 升级node

``` sh
# npm install -g n
/usr/local/bin/n -> /usr/local/lib/node_modules/n/bin/n
+ n@7.0.2
added 1 package from 4 contributors in 1.18s
# sudo n stable   # 级到稳定版本
Password:
  installing : node-v14.16.0
       mkdir : /usr/local/n/versions/node/14.16.0
       fetch : https://nodejs.org/dist/v14.16.0/node-v14.16.0-darwin-x64.tar.xz
   installed : v14.16.0 (with npm 6.14.11)
```

最后升级npm到最新版本：

```
sudo npm install npm@latest -g
```

Mdzz@wanglu

### hello world

`vi helloworld.js`

```js
console.log("Hello World");
```

运行：

`node helloworld.js`

会在控制台看到输出



### 基于web的node.js应用

#### 一个可工作的HTTP服务器

server.js:

```js
var http = require("http");

http.createServer(function(request, response) {
  console.log("Request receiced.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}).listen(8000);
```

node server.js  访问8000端口，会看到hello world的网页。

分析：

* 第一行node 自带的http模块。
* http模块提供的函数：createServer,启动一个监听端口的服务器。
* 收到请求，使用response.writeHead()发送一个HTTP状态200和HTTP头的内容类型（content-type）
* 使用response.write()函数在HTTP相应主体中发送文本"Hello World".
* response.end() 完成相应。



#### 回调

事件驱动的回调，回调：给某个方法传递了一个函数A，这个方法在有相应事件时调用这个函数A.

我们的程序在一个进程中，这个函数A指的是这里的`function(request,response)`这个匿名函数，

我们可以自己定义一个：

server.js

```js
var http = require("http");

function onRequest(request, response) {
  console.log("Request received.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}

http.createServer(onRequest).listen(8888);
```



#### 主引导文件

上面server.js 中，加一个start函数，导出服务，让其他文件（主引导文件可调用）改：

```js
var http = require("http");

function start(){
  function onRequest(request, response) {
  console.log("Request received.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}
}

exports.start = start;
```

主导文件index.js:

```js
var server = require("./server");
server.start();
```

导出的函数就这样被我们使用了，此时执行：`node index.js`  运行程序。



#### 路由

提取路由和url参数需要url 和querystring 模块。

获得url：

server.js:

```js
var url = require('url') 
var pathname = url.parse(request.url).pathname;
function start(route){
  route(pathname)
}
```

pathname这里获得的是你的url,如你访问了localhost:8000/update/111,则pathname为`/update/111`

 设置到相应程序上：

router.js:

```js
function route(pathname){
  console.log("About to route a request for " + pathname);
}
exports.route = route;
```

此时主导文件index.js:

```js
var server = require("./server");
var router = require("./router");

server.start(router.route)
```



#### 从路由到业务

路由模块不是处理业务的模块，现在我们新建个文件对不同请求处理不同业务：

requestHandlers.js:

```js
function start(){
  console.log("Request handler 'start' was called");
}
function upload() {
  console.log("Request handler 'upload' was called");
}

exports.start = start;
exports.upload = upload;
```



我们要将路由和路由函数，变成一一映射的关系，那么可以考虑到js中的对象，想象成一个键为字符串的字典。

index.js:

```js
var server = require("./server");
var route = reuquiree("./router");
var requestHandlers = require("./requestHandlers");
 
var handle = {}
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;

server.start(router.route,handle);
```

这样看上去非常干净。



下面配置server.js:

```js
function start(route, handle) { //这里
  function onRequest(request, response) {
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received.");

    route(handle, pathname);  //这里

    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("Hello World");
    response.end();
  }

  http.createServer(onRequest).listen(8888);
  console.log("Server has started.");
}

exports.start = start;
```



修改router.js:

```js
function route(handle, pathname) {
  console.log("About to route a request for " + pathname);
  if (typeof handle[pathname] == 'function') {
    handle[pathname]();
  } else {
    console.log("No request handler found for " + pathname);
  }
}

exports.route = route;
```



#### 阻塞

如果在requestHandlers.js的start函数中写个十秒的操作：

```js
function sleep(second){
  var startTime = new Date().getTime();
  while (new Date().getTime()<startTIme+second);
}
sleep(10000);
```

这时 我们访问/start ，同时访问/upload，居然第二个路由也花费了十秒。getTIme(得到1970.1.1到今天的毫秒)

Node一向是这样来标榜自己的：“在node中除了代码，所有一切都是并行执行的”。

这句话的意思是说，Node.js可以在不新增额外线程的情况下，依然可以对任务进行并行处理 —— Node.js是单线程的。它通过事件轮询（event loop）来实现并行操作，对此，我们应该要充分利用这一点 —— 尽可能的避免阻塞操作，取而代之，多使用非阻塞操作。

要使用非阻塞操作，我们需要回调，将函数作为参数传递给需要花费时间的函数。

比方说，time()是一个需要时间的处理的函数，node线程会跟它说，嘿，你先处理吧，先给我个回调函数，我去干别的，等你处理完了我调用这个回调函数。

**这里服务器的回调函数为onRequest(),，从它这可以获得response对象，该对上的函数可以作为一个回调函数给废时间的函数。**



#### 非阻塞

现在按照上面的思路改我们的程序：

server.js:

```js
var http = require("http");
var url = require("url");

function start(route, handle) {
  function onRequest(request, response) {
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received.");

    route(handle, pathname, response);
  }

  http.createServer(onRequest).listen(8888);
  console.log("Server has started.");
}

exports.start = start;
```

去掉了原有的response 操作，为route函数传递了response.

route.js:

```js
var exec = require("child_process").exec;

function start(response) {
  console.log("Request handler 'start' was called.");

  //无费时
  exec("ls -lah", function (error, stdout, stderr) {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write(stdout);
    response.end();
  });
  
  // 费时 ，
   exec("find /",
    { timeout: 10000, maxBuffer: 20000*1024 },
    function (error, stdout, stderr) {
      response.writeHead(200, {"Content-Type": "text/plain"});
      response.write(stdout);
      response.end();
    });
  
}

function upload(response) {
  console.log("Request handler 'upload' was called.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello Upload");
  response.end();
}

exports.start = start;
exports.upload = upload; 
```

exec() 函数是从nodejs来执行一个shell命令，我们不费时中用它来获取当下目录中所有文件信息，输出到浏览器。

这个函数这里不重要，只知道它是一个费时函数，我们也可以换成其他的费时函数。

现在我们这个应用可以在相应start时同时相应upload了。



#### 处理POST

先为post做一个单独的url,并为我们的页面加一个表单：

requestHandlers.js:：

```js
 function post(response){
      console.log("你访问了post方法");
      var body = '<html>'+
              '<head>'+
              '<meta http-equiv="Content-Type" content="text/html;'+
              'charset=UTF-8"/>'+
              '</head>'+
              '<body>'+
              '<form action="/upload" method="post">'+
              '<textarea name="text" rows="20" cols="60"></textarea>'+
              '<input type="submit" value="Submit text"/>'+
              '</form>'+
              '</body>'+
              '</html>';
      response.writeHead(200,{"Content-Type":"text/html"});
      response.write(body);
      response.end();
  }

exposts.post = post 
```

在index.js 中增加映射，handle['/post']

为了使整个过程非阻塞，Node.js会将POST数据拆分成很多小的数据块，然后通过触发特定的事件，将这些小数据块传递给回调函数。这里的特定的事件有data事件（表示新的小数据块到达了）以及end事件（表示所有的数据都已经接收完毕）。

这些事件触发时，回调哪些函数？

我们在request对象注册监听器来实现，

```js
request.addListener("data", function(chunk) {
  // called when a new chunk of data was received
});

request.addListener("end", function() {
  // called when all chunks of data have been received
});
```

将data和end事件的回调函数直接放在服务器中，在data事件回调中收集所有的POST数据，当接收到所有数据，触发end事件后，其回调函数调用请求路由，并将数据传递给它，然后，请求路由再将该数据传递给请求处理程序。

server.js:

```js
var http = require("http");
var url = require("url");

function start(route, handle) {
  function onRequest(request, response) {
    var postData = "";
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received.");

    request.setEncoding("utf8");

    request.addListener("data", function(postDataChunk) {
      postData += postDataChunk;
      console.log("Received POST data chunk '"+
      postDataChunk + "'.");
    });

    request.addListener("end", function() {
      route(handle, pathname, response, postData);
    });

  }

  http.createServer(onRequest).listen(8888);
  console.log("Server has started.");
}

exports.start = start;
```

在route中多天加这个postData参数：

```js
function route(handle, pathname, response, postData) {
  console.log("About to route a request for " + pathname);
  if (typeof handle[pathname] === 'function') {
    handle[pathname](response, postData);
  } else {
    console.log("No request handler found for " + pathname);
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.write("404 Not found");
    response.end();
  }
}

exports.route = route;
```

相应的在requestHandlers.js中：

```js
function start(response, postData) {
  console.log("Request handler 'start' was called.");

  var body = '<html>'+
    '<head>'+
    '<meta http-equiv="Content-Type" content="text/html; '+
    'charset=UTF-8" />'+
    '</head>'+
    '<body>'+
    '<form action="/upload" method="post">'+
    '<textarea name="text" rows="20" cols="60"></textarea>'+
    '<input type="submit" value="Submit text" />'+
    '</form>'+
    '</body>'+
    '</html>';

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(body);
    response.end();
}

function upload(response, postData) {
  console.log("Request handler 'upload' was called.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("You've sent: " + postData);
  response.end();
}

exports.start = start;
exports.upload = upload;
```

querystring 函数。