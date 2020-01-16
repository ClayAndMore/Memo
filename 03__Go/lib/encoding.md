Go语⾔对于这些标准格式的编码和解码都有良好的⽀持，由标准库中的encoding/json、encoding/xml、encoding/asn1 等包提供⽀持（译注：Protocol	Buffers的⽀持由	github.com/golang/protobuf	包提供），并且这类包都有着相似的API 接⼝

### json

基本的JSON类型有数字（⼗进制或科学记数法）、布尔值（true或false）、字符串，其中字符串是以双引号包含的 Unicode字符序列，⽀持和Go语⾔类似的反斜杠转义特性，**不过JSON使⽤的是	\Uhhhh	转义数字来表示⼀个UTF-16编 码**（译注：UTF-16和UTF-8⼀样是⼀种变⻓的编码，有些Unicode码点较⼤的字符需要⽤4个字节表示；⽽且UTF-16还 有⼤端和⼩端的问题），⽽不是Go语⾔的rune类型。

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

