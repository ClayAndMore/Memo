
---
title: "net-http.md"
date: 2019-10-12 17:45:41 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "net-http.md"
date: 2019-10-12 17:45:41 +0800
lastmod: 2020-02-08 12:27:11 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Golang自带的http包已经实现了htpp客户端和服务端，我们可以利用它更为快速的开发http服务。



## 服务端

```go
package main

import (
    "fmt"
    "net/http"
)

func IndexHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "hello world")
}

func main() {
    http.HandleFunc("/", IndexHandler)
    http.ListenAndServe("127.0.0.0:8000", nil)
}
```

main函 数将所有发送到/路径下的请求和handler函数关联起来，/开头的请求其实就是所有发送到当前站点上的请求，服务监听 8000端⼝。



### handler

ListenAndServe函数需要⼀个例如“localhost:8000”的服务器地址，和⼀个所有请求都可以分派的Handler接⼝实例。

想象⼀个电⼦商务⽹站，为了销售，将数据库中物品的价格映射成美元。下⾯这个程序可能是能想到的最简单的实现 了。它将库存清单模型化为⼀个命名为database的map类型，我们给这个类型⼀个ServeHttp⽅法，这样它可以满⾜ http.Handler接⼝。

``` go
package main

import (
    "fmt"
    "net/http"
)

type dollars float32
func (d dollars) String() string {return fmt.Sprintf("$%.2f", d) }

type database map[string]dollars
func (db database) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    for item, price := range db {
        fmt.Fprintf(w, "%s: %s\n", item, price)
    }
}

func main() {
    db := database{"shoes": 50, "socks": 5}
    http.ListenAndServe("0.0.0.0:8000", db)
}
```

可以通过浏览器，或者后面的仿CURL工具：

```
root@:~/go/workspace/src/ch1/httpFetch# ./fetch http://127.0.0.1:8000
shoes: $50.00
socks: $5.00
```



### 不同URL

改造 ServeHTTP，使调用 /list 来调用以及存在的这个行为并添加 另一个/price 调用表明单个货品的价格：` /price?item=socks`

```go
func (db database) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    switch req.URL.Path {
    case "/list":
        for item, price := range db {
            fmt.Fprintf(w, "%s: %s\n", item, price)
        }
    case "/price":
        item := req.URL.Query().Get("item") // 获取url参数
        price, ok := db[item]
        if !ok {
            w.WriteHeader(http.StatusNotFound) // 404
            fmt.Fprintf(w, "no such item: %q\n", item)
            return
        }
        fmt.Fprint(w, "%s\n", price)
    default:
        w.WriteHeader(http.StatusNotFound) // 404
        fmt.Fprintf(w, "no such page: %s\n", req.URL)
        // 可以使用下面更适用的方式：
        // msg := fmt.Sprintf( "no such page: %s\n", req.URL)
        // http.Error(w, msg, http.StatusNotFound)
    }
}
```

调⽤w.WriteHeader(http.StatusNotFound)返回客户端⼀个HTTP错误。

```
root@# ./fetch http://127.0.0.1:8000/aaa
no such page: /aaa
root@# ./fetch http://127.0.0.1:8000/price?item=ooo
no such item: "ooo"
```



### 多路器ServeMux

net/http包提供了⼀个请求多路器ServeMux来简化URL和handlers的联系。

⼀个ServeMux将⼀批 http.Handler聚集到⼀个单⼀的http.Handler中。再⼀次，我们可以看到满⾜同⼀接⼝的不同类型是可替换的：web服务 器将请求指派给任意的http.Handler⽽不需要考虑它后⾯的具体类型。
对于更复杂的应⽤，⼀些ServeMux可以通过组合来处理更加错综复杂的路由需求

``` go
package main

import (
    "fmt"
    "net/http"
)


type dollars float32
func (d dollars) String() string {return fmt.Sprintf("$%.2f", d) }

type database map[string]dollars

func (db database) list(w http.ResponseWriter, req *http.Request) {
    for item, price := range db {
        fmt.Fprintf(w, "%s: %s\n", item, price)
    }
}

func (db database) price(w http.ResponseWriter, req *http.Request) {
    item := req.URL.Query().Get("item")
    price, ok := db[item]
    if !ok {
        w.WriteHeader(http.StatusNotFound) // 404
        fmt.Fprintf(w, "no such item: %q\n", item)
        return
    }
    fmt.Fprint(w, "%s\n", price)
}

func main() {
    db := database{"shoes": 50, "socks": 5}
    mux := http.NewServeMux()
    mux.Handle("/list", http.HandlerFunc(db.list))
    mux.Handle("/price", http.HandlerFunc(db.price))
    http.ListenAndServe("0.0.0.0:8000", mux)
}
```

因为handler通过这种⽅式注册⾮常普遍，ServeMux有⼀个⽅便的HandleFunc⽅法,在⼀个应⽤程序的多个⽂件中定义HTTP	handler也是⾮常典型的，如果 它们必须全部都显式地注册到这个应⽤的ServeMux实例上会⽐较麻烦。

所以为了⽅便，**net/http包提供了⼀个全局的ServeMux实例DefaultServerMux和包级别的http.Handle和 http.HandleFunc函数。**现在，为了使⽤DefaultServeMux作为服务器的主handler，我们不需要将它传给 ListenAndServe函数；nil值就可以⼯作:

``` go
   //mux := http.NewServeMux()
    //mux.Handle("/list", http.HandlerFunc(db.list))
    //mux.Handle("/price", http.HandlerFunc(db.price))
    http.HandleFunc("/list", db.list)
    http.HandleFunc("/price", db.price)
    http.ListenAndServe("0.0.0.0:8000", nil)
```



### 锁机制

web服务器在⼀个新的协程中调⽤每⼀个handler，所以当handler 获取其它协程或者这个handler本身的其它请求也可以访问到变量时，⼀定要使⽤预防措施，⽐如锁机制.

待补充。



## 客户端

Get，Head，Post和PostForm发出HTTP（或HTTPS）请求



### Get

```go
package main

import (
    "fmt"
    "net/http"
    "io/ioutil"
)

func main(){
    url := "https://httpbin.org/get"
    resp, err := http.Get(url)
    if err != nil {
        fmt.Println(err)
    }
    defer resp.Body.Close()   // 客户端再结束后必须关闭response body。
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(string(body))
}
```

bk:

```
{
  "args": {},
  "headers": {
    "Accept-Encoding": "gzip",
    "Host": "httpbin.org",
    "User-Agent": "Go-http-client/1.1"
  },
  "origin": "222.128.57.45, 222.128.57.45",
  "url": "https://httpbin.org/get"
}
```



### post

```go
package main

import (
    "fmt"
    "net/http"
    "io/ioutil"
    "bytes"
)

func main() {
   body := "{\"title\":\"xxxx\"}"
   //post 方法参数，第一个参数为请求url,第二个参数 是contentType, 第三个参数为请求体
   responce, err := http.Post("https://httpbin.org/post", "application/json", bytes.NewBuffer([]byte(body)))
   if err != nil {
       fmt.Println("net http post method err,", err)
   }
   defer responce.Body.Close()
   rlt, _ := ioutil.ReadAll(responce.Body)
   fmt.Println(string(rlt))
}
```

bk:

```
{
  "args": {},
  "data": "{\"title\":\"xxxx\"}",
  "files": {},
  "form": {},
  "headers": {
    "Accept-Encoding": "gzip",
    "Content-Length": "16",
    "Content-Type": "application/json",
    "Host": "httpbin.org",
    "User-Agent": "Go-http-client/1.1"
  },
  "json": {
    "title": "xxxx"
  },
  "origin": "222.128.57.45, 222.128.57.45",
  "url": "https://httpbin.org/post"
}
```



### postform

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "net/url"
)

func main() {
    resp, err := http.PostForm("https://accounts.douban.com/j/mobile/login/basic", url.Values{"name": {"xx@xx.com"}, "password": {"12356"}})
    fmt.Println(resp.Request.URL)
    if err != nil {
        fmt.Println(err)
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(string(body))
}
```



### client

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "time"
)

func main() {
    client := &http.Client{
        Timeout: 3 * time.Second,
    }
    req, err := http.NewRequest("GET", "http://www.baidu.com", nil)
    req.Header.Add("X-Requested-With", "XMLHttpRequest")
    if err != nil {
        fmt.Println(err)
    }
    resp, err := client.Do(req)
    
    if err != nil {
        fmt.Println(err)
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(string(body))
}
```



### 仿CURL

fetch.go:

``` go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
)

func main(){
    for _, url  := range os.Args[1:]{
        resp, err := http.Get(url)
        if err != nil {
            fmt.Fprintf(os.Stderr, "fetch: %v\n", err)
            os.Exit(1)
        }
        b, err := ioutil.ReadAll(resp.Body)
        resp.Body.Close()
        if err != nil {
            fmt.Fprintf(os.Stderr, "fetch: reading %s: %v\n", url, err)
            os.Exit(1)
        }
        fmt.Printf("%s", b)
    }
}
```

使用：

```
./fetch http://www.baidu.com
<!DOCTYPE html><!--STATUS OK--><html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"><meta content="always" name="referrer"><meta name="theme-color" content="#2932e1"><link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" /><link rel="search" type="application/opensearchdescription+xml" href="/content-search.xml" title="百度搜索" /><link rel="icon" sizes="any" mask href="//www.baidu.com/img/baidu_85beaf5496f291521eb75ba38eacbd87.svg"><link rel="dns-prefetch" href="//s1.bdstatic.com"/><link rel="dns-prefetch" href="//t1.bai
```

