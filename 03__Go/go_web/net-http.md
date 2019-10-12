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

