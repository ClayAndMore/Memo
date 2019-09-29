tags: [Go, go_lib]

## log

https://www.flysnow.org/2017/05/06/go-in-action-go-log.html



go 官网 API: https://godoc.org/log#example-Logger



另一个库： `https://github.com/sirupsen/logrus`



eg:

```go
package main

import "log"

func main() {
    log.Println("王大锤", " big 80", "simall 40")
    log.Printf(" ----- ")
    log.Printf(" ===== ")
}
```

out:

```
2019/03/25 11:30:30 王大锤  big 80 simall 40
2019/03/25 11:30:30  -----
2019/03/25 11:30:30  =====
```

* 默认输出日期 时间
* 可多个参数
* Printf 和 Println没有区别



### 定制输出

```go
func init(){
	log.SetFlags(log.Ldate|log.Lshortfile)
}
```

out:

```
2019/03/25 test.go:10: 王大锤  big 80 simall 40
2019/03/25 test.go:11:  -----
2019/03/25 test.go:12:  =====
```

少了时间多了行号。

常量解释：

```go
const (
	Ldate         = 1 << iota     //日期示例： 2009/01/23
	Ltime                         //时间示例: 01:23:23
	Lmicroseconds                 //毫秒示例: 01:23:23.123123.
	Llongfile                     //绝对路径和行号: /a/b/c/d.go:23
	Lshortfile                    //文件和行号: d.go:23.
	LUTC                          //日期时间转为0时区的
	LstdFlags     = Ldate | Ltime //Go提供的标准抬头信息
)
```



#### 设置前缀：

```go
func init(){
	log.SetPrefix("[TEST]")
	log.SetFlags(log.LstdFlags | log.Lshortfile |log.LUTC)
}
```

out:

```
[TEST]2019/03/25 test.go:11: 王大锤  big 80 simall 40
[TEST]2019/03/25 test.go:12:  -----
[TEST]2019/03/25 test.go:13:  =====
```



#### 打印级别





#### Logger

`logger = log.New()`



多级logger:

```go
package main

import (
    "log"
    "os"
    "io"
)

var (
    Info *log.Logger
    Warning *log.Logger
    Error *log.Logger
)

func init(){
    errFile,err:=os.OpenFile("errors.log",os.O_CREATE|os.O_WRONLY|os.O_APPEND,0666)
    if err!=nil{
        log.Fatalln("打开日志文件失败：",err)
    }

    Info = log.New(os.Stdout,"Info:",log.Ldate | log.Ltime | log.Lshortfile)
    Warning = log.New(os.Stdout,"Warning:",log.Ldate | log.Ltime | log.Lshortfile)
    Error = log.New(io.MultiWriter(os.Stderr,errFile),"Error:",log.Ldate | log.Ltime | log.Lshortfile)

}

func main() {
    Info.Println(" da chui 80"," xiao chui 40")
    Warning.Printf("da chui：%s\n","40")
    Error.Pri
```

