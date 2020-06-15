
---
title: "httptest.md"
date: 2020-02-10 14:02:16 +0800
lastmod: 2020-02-10 14:02:16 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


可以很容易的进行 Web 开发。为此，Go 标准库专门提供了 httptest 包专门用于进行 http Web 开发测试。

本节我们通过一个社区帖子的增删改查的例子来学习该包。



### 一个简单的http 应用：

data.go:

``` go
package main

import (
	"errors"
	"time"
)

type Topic struct {
	Id       int       `json:"id"`
	Title    string    `json:"title"`
	Content  string    `json:"content"`
	CreateAt time.Time `json:"created_ad"`
}

// 保存  Topic , 没有考虑并发问题
var TopicCache = make([]*Topic, 0, 16)

func checkIndex(id int) error {
	if id > 0 && len(TopicCache) <= id-1 {
		return errors.New("topic is not exists!")
	}
	return nil
}

func FindTopic(id int) (*Topic, error) {
	if err := checkIndex(id); err != nil {
		return nil, err
	}
	return TopicCache[id-1], nil
}

func (t *Topic) Create() error {
	t.Id = len(TopicCache) + 1
	t.CreateAt = time.Now()
	TopicCache = append(TopicCache, t)
	return nil
}

func (t *Topic) Update() error {
	if err := checkIndex(t.Id); err != nil {
		return err
	}
	TopicCache[t.Id-1] = t
	return nil
}

// 简单的将对应的 slice 位置置为 nil
func (t *Topic) Delete() error {
	if err := checkIndex(t.Id); err != nil {
		return err
	}
	TopicCache[t.Id-1] = nil
	return nil
}
```



Server.go：

``` go
package main

import (
	"encoding/json"
	"net/http"
	"path"
	"strconv"
)


// 获取一个帖子， 如 get /topic/1
func handleGet(w http.ResponseWriter, r *http.Request) error {
	id, err := strconv.Atoi(path.Base(r.URL.Path))
	if err != nil {
		return err
	}
	topic, err := FindTopic(id)
	if err != nil {
		return err
	}
	output, err := json.MarshalIndent(&topic, "", "\t\t")
	w.Header().Set("Content-Type", "application/json")
	w.Write(output)
	return nil
}

// 增加一个帖子 // POST /topic/
func handlePost(w http.ResponseWriter, r *http.Request) (err error)  {
	body := make([]byte, r.ContentLength)
	r.Body.Read(body)  // ?
	var topic = new(Topic)
	err = json.Unmarshal(body, &topic)
	if err != nil {
		return
	}

	err = topic.Create()
	if err != nil {
		return
	}
	w.WriteHeader(http.StatusOK)
	return
}

// 更新一个帖子  PUT /topic/1
func handlePut(w http.ResponseWriter, r *http.Request) error {
	id, err := strconv.Atoi(path.Base(r.URL.Path))
	if err != nil {
		return err
	}
	topic, err := FindTopic(id)
	if err != nil {
		return err
	}
	body := make([]byte, r.ContentLength)
	r.Body.Read(body)
	json.Unmarshal(body, topic)  // 这里没有 & , 表示疑问
	err = topic.Update()
	if err != nil {
		return  err
	}
	w.WriteHeader(http.StatusOK)
	return nil
}

// 删除一个帖子 Delete /topic/1
func handleDelete(w http.ResponseWriter, r *http.Request) (err error) {
	id, err := strconv.Atoi(path.Base(r.URL.Path))
	if err != nil{
		return
	}
	topic, err := FindTopic(id)
	if err != nil {
		return
	}
	err = topic.Delete()
	if err != nil {
		return
	}
	w.WriteHeader(http.StatusOK)
	return
}

// main handler function
// /topic/ 开头的请求都交由 handleRequest 处理，它根据不同的 Method 执行相应的增删改查，
func handlerRequest(w http.ResponseWriter, r *http.Request){
	var err error
	switch r.Method {
	case http.MethodGet:
		err = handleGet(w, r)
	case http.MethodPost:
		err = handlePost(w, r)
	case http.MethodPut:
		err = handlePut(w, r)
	case http.MethodDelete:
		err = handleDelete(w, r)
	}
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func main() {
	http.HandleFunc("/topic/", handlerRequest)
	http.ListenAndServe(":2017", nil)
}
```

启动 运行： `go run server.go data.go`



#### 通过 curl 进行简单的测试

``` bash
# 增
~ curl -i -X POST http://localhost:2017/topic/ -H 'content-type: application/json' -d '{"title":"The Go Standard Library","content":"It contains many packages."}'
HTTP/1.1 200 OK
Date: Sat, 08 Feb 2020 15:55:36 GMT
Content-Length: 0

# 查
~ curl -i -X GET http://localhost:2017/topic/1
HTTP/1.1 200 OK
Content-Type: application/json
Date: Sat, 08 Feb 2020 15:55:48 GMT
Content-Length: 146

{
		"id": 1,
		"title": "The Go Standard Library",
		"content": "It contains many packages.",
		"created_ad": "2020-02-08T23:55:36.401109+08:00"
}%   

# 改
~ curl -i -X PUT http://localhost:2017/topic/1 -H 'content-type: application/json' -d '{"title":"The Go Standard Library By Example","content":"It contains many packages, enjoying it."}'
HTTP/1.1 200 OK
Date: Sat, 08 Feb 2020 15:55:59 GMT
Content-Length: 0

~ curl -i -X GET http://localhost:2017/topic/1
HTTP/1.1 200 OK
Content-Type: application/json
Date: Sat, 08 Feb 2020 15:56:04 GMT
Content-Length: 170

{
		"id": 1,
		"title": "The Go Standard Library By Example",
		"content": "It contains many packages, enjoying it.",
		"created_ad": "2020-02-08T23:55:36.401109+08:00"
}%   

# 删
~ curl -i -X DELETE http://localhost:2017/topic/1
HTTP/1.1 200 OK
Date: Sat, 08 Feb 2020 15:56:20 GMT
Content-Length: 0

~ curl -i -X GET http://localhost:2017/topic/1
HTTP/1.1 200 OK
Content-Type: application/json
Date: Sat, 08 Feb 2020 15:56:22 GMT
Content-Length: 4

null%                                                                                              
```



### httptest

现在，我们通过 `net/http/httptest` 包进行测试。

``` go
package main

import (
	"encoding/json"
	"strings"
	"testing"
	"net/http"
	"net/http/httptest"
)

// 先测试创建帖子，也就是测试 handlePost 函数。
func TestHandlePost(t *testing.T) {
  
  // 跟待测试代码一样，配置上路由，对 /topic/ 的请求都交由 handleRequest 处理。
	mux := http.NewServeMux()
	mux.HandleFunc("/topic/", handlerRequest)

  //因为 handlePost 的函数签名是 func handlePost(w http.ResponseWriter, r *http.Request) error
  // 为了测试它，我们必须创建 http.ResponseWriter 和 http.Request 的实例。
	reader := strings.NewReader(`{"title":"The Go Standard Library","content":"It contains many packages."}`)
	r, _ := http.NewRequest(http.MethodPost, "/topic/", reader)

  // 通过 httptest.NewRecorder() 可以获得 httptest.ResponseRecorder 结构，而此结构实现了http.ResponseWriter 接口。 ？
	w := httptest.NewRecorder()

  // 这里直接调用 handlePost(w, r) 也是可以的，但调用 mux.ServeHTTP(w, r) 会更完整地测试整个流程。
	mux.ServeHTTP(w, r)
  resp := w.Result()
	if resp.StatusCode != http.StatusOk {
		t.Errorf("Response code if %v", resp.StatusCode)
	}
}

func TestHandleGet(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/topic/", handlerRequest)

	r, _ := http.NewRequest(http.MethodGet, "/topic/1", nil)
	w := httptest.NewRecorder()

	mux.ServeHTTP(w, r)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Response code if %v", resp.StatusCode)
	}
	topic := new(Topic)
	json.Unmarshal(w.Body.Bytes(), topic)
	if topic.Id != 1 {
		t.Errorf("Cannot get topic")
	}

}
```

数据没有落地存储，为了保证后面的测试正常，请将 `TestHandlePost` 放在最前面。

最后，通过 `go test -v` 运行测试:

```
~/Documents/go/src/gotest/httpTest go test -v              
=== RUN   TestHandlePost
--- PASS: TestHandlePost (0.00s)
=== RUN   TestHandleGet
--- PASS: TestHandleGet (0.00s)
PASS
ok      gotest/httpTest 0.017s
```



### 代码改进 testMain:

待补充