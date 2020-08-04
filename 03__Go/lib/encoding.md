---
title: "encoding.md"
date: 2020-01-16 18:29:52 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: ["go lib"]
categories: ["go"]
author: "Claymore"

---
Go语⾔对于这些标准格式的编码和解码都有良好的⽀持，由标准库中的encoding/json、encoding/xml、encoding/asn1 等包提供⽀持（译注：Protocol	Buffers的⽀持由	github.com/golang/protobuf	包提供），并且这类包都有着相似的API 接⼝

### json

基本的JSON类型有数字（⼗进制或科学记数法）、布尔值（true或false）、字符串，其中字符串是以双引号包含的 Unicode字符序列，⽀持和Go语⾔类似的反斜杠转义特性，**不过JSON使⽤的是	\Uhhhh	转义数字来表示⼀个UTF-16编 码**（译注：UTF-16和UTF-8⼀样是⼀种变⻓的编码，有些Unicode码点较⼤的字符需要⽤4个字节表示；⽽且UTF-16还 有⼤端和⼩端的问题），⽽不是Go语⾔的rune类型。

#### marshaling

将⼀个Go语⾔中类似movies的结构体slice转 为JSON的过程叫编组（marshaling）。编组通过调⽤json.Marshal函数完成

``` go
package main

import (
    "fmt"
    "encoding/json"
)

func main(){
    type Movie struct {
    Title string
    Year  int
    Color bool
    Actors []string
    }

    var movies = []Movie{
        {Title: "A", Year: 1942, Color: false,  Actors: []string{"aa", "bb"}},
        {Title: "B", Year: 1981, Color: true,   Actors: []string{"cc", "dd", "ee"}},
        {Title: "C", Year: 1999, Color: false,  Actors: []string{"ff"}},
    }
    data, err := json.Marshal(movies)
    if err != nil {
        fmt.Printf("Error: ", err)
    }
    fmt.Printf("%s\n", data)
}
```

输出

```sh
root@wy:~/go/workspace/src/ch1/jsonTest# go run main.go
[{"Title":"A","Year":1942,"Color":false,"Actors":["aa","bb"]},{"Title":"B","Year":1981,"Color":true,"Actors":["cc","dd","ee"]},{"Title":"C","Year":1999,"Color":false,"Actors":["ff"]}]
```

Marshal函数返还⼀个编码后的字节slice，包含很⻓的字符串，并且没有空⽩缩进；



#### 美化输出-pretty

**为了⽣成便于阅读的格式，另⼀个json.MarshalIndent函 数将产⽣整⻬缩进的输出。**

该函数有两个额外的字符串参数⽤于表示每⼀⾏输出的前缀和每⼀个层级的缩进:

``` go
data, err = json.MarshalIndent(movies, "", "    ")
fmt.Printf("%s\n", data)
```

输出：

```json
[
    {
        "Title": "A",
        "Year": 1942,
        "Color": false,
        "Actors": [
            "aa",
            "bb"
...
        ]
    }
]
```

如果只有一个json 字符串，想要美化输出，难道我们还要 解码 再 MarshalIndent 么，显然这很繁琐，这个时候就需要用到Indent：

``` go
import (
    "bytes"
    "encoding/json"
    "fmt"
)

var ex4 = `
{
    "timestamp":"2020-05-30T00:01:46.900195+0800",
    "flow_id":151151474019711,
    "event_type":"http",
    "dest_port":80,
    "proto":"TCP",
    "tx_id":0,
    "http":{
        "hostname":"172.19.19.200",
        "url":"/WSSmCommUpper/WSSmCommUpper",
        "http_user_agent":"Python-urllib/2.7",
        "http_content_type":"text/xml",
        "protocol":"HTTP/1.1",
        "status":200
    }
}
`

var prettyJSON bytes.Buffer
error := json.Indent(&prettyJSON, []byte(ex4), "", "\t")
if error != nil {
    fmt.Println("JSON parse error: ", error)
    return
}

fmt.Println("json pretty byte:", string(prettyJSON.Bytes()))
```





#### 编码 与 结构体 tag

将上述结果体加如下tag:

```go
type Movie struct {
    Title string
    Year  int  `json:"released"`
    Color bool `json:"color,omitempty"`
    Actors []string
}
```

查看输出：

```json
[
    {
        "Title": "A",
        "released": 1942,
        "Actors": [
            "aa",
            "bb"
        ]
    },
    {
        "Title": "B",
        "released": 1981,
        "color": true,
        "Actors": [
            "cc",
            "dd",
            "ee"
        ]
    },
    {
        "Title": "C",
        "released": 1999,
        "Actors": [
            "ff"
        ]
    }
]
```

可以看到 Year 变成了 released,  color 当为true时才显示。

结构体tag可是任意的字符串面值， 通常是 key:"value"键值对序列， 因为值中含有双引号字符，所以 tag 一般用原生字符串面值的形式书写（反引号）

* **json开头键名对应的值⽤于控制encoding/json包的编码和 解码的⾏为，**并且encoding/...下⾯其它的包也遵循这个约定。
* 成员Tag中json对应值的第⼀部分⽤于指定JSON对象的 名字，Year -> released
* Color成员的Tag还带了⼀个**额外的 omitempty选项，表示当Go语⾔结构体成员为空或零值时不⽣成该JSON对象**（这⾥false为零值



#### unmarshaling

编码的逆操作是解码，对应将JSON数据解码为Go语⾔的数据结构，Go语⾔中⼀般叫unmarshaling，通过 json.Unmarshal函数完成。下⾯的代码将JSON格式的电影数据解码为⼀个结构体slice，结构体中只有Title成员。通过 定义合适的Go语⾔数据结构，我们可以选择性地解码JSON中感兴趣的成员。当Unmarshal函数调⽤返回，slice将被只 含有Title信息的值填充，其它JSON成员将被忽略。

``` go
var	titles []struct{ Title string } 
if	err	:=	json.Unmarshal(data, &titles);
err	!=	nil	{				
    log.Fatalf("JSON	unmarshaling	failed:	%s",	err) } fmt.Println(titles)
```



#### 转换一个结构体到map

From `struct` to `map[string]interface{}`

```go
package main

import (
    "fmt"
    "encoding/json"
)

type MyData struct {
    One   int
    Two   string
    Three int
}

func main() {   
    in := &MyData{One: 1, Two: "second"}

    var inInterface map[string]interface{}
    inrec, _ := json.Marshal(in)
    json.Unmarshal(inrec, &inInterface)

    // iterate through inrecs
    for field, val := range inInterface {
            fmt.Println("KV Pair: ", field, val)
    }
}
```



#### 解码未知结构的json数据

实际开发过程中，有时候我们可能并不知道要解码的 JSON [数据结构]是什么样子的，这个时候应该怎么处理呢？



``` go
package jsonTest

import (
	"encoding/json"
	"fmt"
	"testing"
)

func TestJson(t *testing.T) {
	testByte := []byte(`{"name": "王大锤", "website": "http://test.net/", "course": ["Golang", "PHP", "JAVA", "C"]}`)
	//var test interface{}  // 用这个也可以解码成功，但是没有下面这样好理解
	var test1 map[string]interface{}
	err := json.Unmarshal(testByte, &test1)
	if err != nil {
		fmt.Printf("JSON 解码失败：%v\n", err)
		return
	}
	fmt.Printf("JSON 解码结果: %#v\n", test1)
}
```

输出：

```
JSON 解码结果: map[string]interface {}{"course":[]interface {}{"Golang", "PHP", "JAVA", "C"}, "name":"王大锤", "website":"http://test.net/"}
```





#### json的流式读写

Go语言内置的 encoding/json 包还提供了 Decoder 和 Encoder 两个类型，用于支持 JSON 数据的流式读写，并提供了 NewDecoder() 和 NewEncoder() 两个函数用于具体实现：

``` go
func NewDecoder(r io.Reader) *Decoder
func NewEncoder(w io.Writer) *Encoder
```

从标准输入流中读取 JSON 数据，然后将其解码，最后再写入到标准输出流中：

```go
package main
import (    
  "encoding/json"    
  "log"    
  "os")
func main() {    
  dec := json.NewDecoder(os.Stdin)    
  enc := json.NewEncoder(os.Stdout)    
  for {        
    var v map[string]interface{}       
    if err := dec.Decode(&v); err != nil {            
      log.Println(err)            
      return        
    }        
    if err := enc.Encode(&v); err != nil {            
      log.Println(err)        
    }    }}
```

执行上面的代码，我们需要先输入 JSON 结构数据供标准输入流 os.Stdin 读取，读取到数据后，会通过 json.NewDecoder 返回的解码器对其进行解码，最后再通过 json.NewEncoder 返回的编码器将数据编码后写入标准输出流 os.Stdout 并打印出来.

使用 Decoder 和 Encoder 对数据流进行处理可以应用得更为广泛些，比如读写 HTTP 连接、WebSocket 或文件等，Go语言标准库中的 net/rpc/jsonrpc 就是一个应用了 Decoder 和 Encoder 的实际例子：

```go
// NewServerCodec returns a new rpc.ServerCodec using JSON-RPC on conn.
func NewServerCodec(conn io.ReadWriteCloser) rpc.ServerCodec {    
  return &serverCodec{        
    dec:     json.NewDecoder(conn),        
    enc:     json.NewEncoder(conn),        
    c:       conn,        
    pending: make(map[uint64]*json.RawMessage),  
  }
}
```