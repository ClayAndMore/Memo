

## io/ioutil

###  读取

``` go
//ReadAll函数被定义为从源中读取数据直到EOF，它是不会去从返回数据中去判断EOF来作为读取成功的依据
func ReadAll(r io.Reader) ([]byte, error)

//读取一个目录，并返回一个当前目录下的文件对象列表和错误信息
func ReadDir(dirname string) ([]os.FileInfo, error)

//读取文件内容，并返回[]byte数据和错误信息
func ReadFile(filename string) ([]byte, error)
```

readall 和 readfile 的区别在于传参, **它们都是将文件中所有内容直接读入内存，在读取大文件时要注意**

readAll:

``` go
    file, err := os.Open("input.txt")   
    if err != nil {
        log.Panicf("failed reading file: %s", err)
    }
    defer file.Close()
    data, err := ioutil.ReadAll(file)
```

readfile:

``` go
    data, err := ioutil.ReadFile("input.txt")
    if err != nil {
        log.Panicf("failed reading data from file: %s", err)
    }
```



### 写入

```javascript
// 写入[]byte类型的data到filename文件中，文件权限为perm
func WriteFile(filename string, data []byte, perm os.FileMode) error
```

eg:

``` go
//[]byte内容写入文件,如果content字符串中没有换行符的话，默认就不会有换行符
func WriteWithIoutil() {
    content := "test.txt"
    data :=  []byte(content)
    if ioutil.WriteFile("test.txt",  "Hello!\n", 0644) == nil {
        fmt.Println("写入文件成功:",content)
    }
}
```





### 转换string

读取出来的byte 在换成string 时，会把 "\n" 当成一个字符：

``` go
package main

import (
    "fmt"
    "io/ioutil"
)

func main(){
    content, _ := ioutil.ReadFile("test.txt")
    fmt.Println(content, len(content))
    fmt.Println(string(content), len(string(content)))
}
```

text.txt:

```
aa
bb
```

执行：

``` sh
# go run readfile.go
[97 97 10 98 98 10] 6
aa
bb
 6
```

所以：

``` go
 if contents,err := ioutil.ReadFile(name);err == nil {
	//因为contents是[]byte类型，直接转换成string类型后会多一行空格,需要使用strings.Replace替换换行符
	result := strings.Replace(string(contents),"\n","",1)
     fmt.Println(result))
 }
```





## 读取速度

**当读取小文件时，使用`ioutil`效率明显优于`os`和`bufio`，但如果是大文件，`bufio`读取会更快。**

ps: https://jishuin.proginn.com/p/763bfbd2adfb