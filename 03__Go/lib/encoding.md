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

为了⽣成便于阅读的格式，另⼀个json.MarshalIndent函 数将产⽣整⻬缩进的输出。

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
        ]
    },
    {
        "Title": "B",
        "Year": 1981,
        "Color": true,
        "Actors": [
            "cc",
            "dd",
            "ee"
        ]
    },
    {
        "Title": "C",
        "Year": 1999,
        "Color": false,
        "Actors": [
            "ff"
        ]
    }
]
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
* Color成员的Tag还带了⼀个额外的 omitempty选项，表示当Go语⾔结构体成员为空或零值时不⽣成该JSON对象（这⾥false为零值



#### unmarshaling

编码的逆操作是解码，对应将JSON数据解码为Go语⾔的数据结构，Go语⾔中⼀般叫unmarshaling，通过 json.Unmarshal函数完成。下⾯的代码将JSON格式的电影数据解码为⼀个结构体slice，结构体中只有Title成员。通过 定义合适的Go语⾔数据结构，我们可以选择性地解码JSON中感兴趣的成员。当Unmarshal函数调⽤返回，slice将被只 含有Title信息的值填充，其它JSON成员将被忽略。

``` go
var	titles []struct{ Title string } 
if	err	:=	json.Unmarshal(data, &titles);
err	!=	nil	{				
    log.Fatalf("JSON	unmarshaling	failed:	%s",	err) } fmt.Println(titles)
```

