Tags:[web]

服务器向浏览器推送信息，除了WebSocket, 还有种方式： Server-Sent Events(SSE)



### 本质

严格来说，服务器无法**主动** 向浏览器推送信息。

但是有一种变通方法，向客户端声明，发送的是流信息。

也就是说，发送的不是一次性的数据包，而是一个数据流，会连续不断地发送过来。

这时，客户端不会关闭连接，会一直等着服务器发过来的新的数据流，视频播放就是这样的例子。

本质上，这种通信就是以流信息的方式，完成一次用时很长的下载。 



SSE 就是利用这种机制，使用流信息向浏览器推送信息。它基于 HTTP 协议，目前除了 IE/Edge，其他浏览器都支持。 



#### 特点

SSE 与 WebSocket 作用相似，都是建立浏览器与服务器之间的通信渠道，然后服务器向浏览器推送信息。

总体来说，WebSocket 更强大和灵活。因为它是全双工通道，可以双向通信；SSE 是单向通道，只能服务器向浏览器发送，因为流信息本质上就是下载。

如果浏览器向服务器发送信息，就变成了另一次 HTTP 请求。





### 服务端实现



服务器向浏览器发送的 SSE 数据，必须是 UTF-8 编码的文本，具有如下的 HTTP 头信息。

 ```
 Content-Type: text/event-stream
 Cache-Control: no-cache
 Connection: keep-alive
 ```

上面三行之中，第一行的`Content-Type`必须指定 MIME 类型为`event-steam`。



每一次发送的信息，由若干个`message`组成，每个`message`之间用`\n\n`分隔。

每个`message`内部由若干行组成，每一行都是如下格式：


` [field]: value\n`


上面的`field`可以取四个值:

> - data
> - event
> - id
> - retry

此外，还可以有冒号开头的行，表示注释。通常，服务器每隔一段时间就会向浏览器发送一个注释，保持连接不中断。

> ```
> : This is a comment
> ```

下面是一个例子。

> ```
> : this is a test stream\n\n
> 
> data: some text\n\n
> 
> data: another message\n
> data: with two lines \n\n
> ```



四个字段：

#### data 字段

数据内容用`data`字段表示。

> ```
> data:  message\n\n
> ```

如果数据很长，可以分成多行，最后一行用`\n\n`结尾，前面行都用`\n`结尾。

> ```
> data: begin message\n
> data: continue message\n\n
> ```

下面是一个发送 JSON 数据的例子。

> ```
> data: {\n
> data: "foo": "bar",\n
> data: "baz", 555\n
> data: }\n\n
> ```

#### id 字段

数据标识符用`id`字段表示，相当于每一条数据的编号。

> ```
> id: msg1\n
> data: message\n\n
> ```

浏览器用`lastEventId`属性读取这个值。一旦连接断线，浏览器会发送一个 HTTP 头，里面包含一个特殊的`Last-Event-ID`头信息，将这个值发送回来，用来帮助服务器端重建连接。因此，这个头信息可以被视为一种同步机制。

#### event 字段

`event`字段表示自定义的事件类型，默认是`message`事件。浏览器可以用`addEventListener()`监听该事件。

> ```
> event: foo\n
> data: a foo event\n\n
> 
> data: an unnamed event\n\n
> 
> event: bar\n
> data: a bar event\n\n
> ```

上面的代码创造了三条信息。第一条的名字是`foo`，触发浏览器的`foo`事件；第二条未取名，表示默认类型，触发浏览器的`message`事件；第三条是`bar`，触发浏览器的`bar`事件。

下面是另一个例子。

> ```
> event: userconnect
> data: {"username": "bobby", "time": "02:33:48"}
> 
> event: usermessage
> data: {"username": "bobby", "time": "02:34:11", "text": "Hi everyone."}
> 
> event: userdisconnect
> data: {"username": "bobby", "time": "02:34:23"}
> 
> event: usermessage
> data: {"username": "sean", "time": "02:34:36", "text": "Bye, bobby."}
> ```

#### retry 字段

服务器可以用`retry`字段，指定浏览器重新发起连接的时间间隔。

> ```
> retry: 10000\n
> ```

两种情况会导致浏览器重新发起连接：一种是时间间隔到期，二是由于网络错误等原因，导致连接出错。







### python 实现

botte + gevent : https://taoofmac.com/space/blog/2014/11/16/1940