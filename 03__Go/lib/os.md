---
title: "os.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-01-16 18:29:52 +0800
draft: false
tags: ["go lib"]
categories: ["go"]
author: "Claymore"

---


os	包以跨平台的⽅式，提供了⼀些与操作系统交互的函数和变量。程序的命令⾏参数可从os包的Args变量获取；os包 外部使⽤os.Args访问该变量。

os.Args变量是⼀个字符串（string）的切⽚（slice）

os.Args的第⼀个元素：os.Args[0]，是命令本身的名字

``` go
package main

import (
    "fmt"
    "os"
)

func main() {
    var s, sep string
    for i :=1; i < len(os.Args); i++ {
        s += sep + os.Args[i]
        sep = " "
    }

    fmt.Println(s)
}

// 输出

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go de 111
de 111

root@wy:~/go/workspace/src/ch1/osEcho# go run main.go de 111 你好
de 111 你好
```



### 获取系统变量

导入”os”包通过os包中的Getenv方法来获取

`func Getenv（key string） string {}`


示例代码：

```go
package main

import "fmt"
import "os"

func main(){
    var JAVAHOME string
    JAVAHOME = os.Getenv("JAVA_HOME")
    fmt.Println(JAVAHOME)
}
```

还可以通过： Environ()

``` go
func Environ() []string // Environ返回表示环境变量的格式为"key=value"的字符串的切片拷贝
fmt.Println(os.Envriron) // [USER=root GOPATH=/root/go/workspace PWD=/root/go/workspace/src HOME=/root]
```





### 获取文件信息 os.Stat()

``` go
func Stat(name string) (fi FileInfo, err error) 

// FileInfo 结构体， 它用来描述一个文件对象
type FileInfo interface {
    Name() string       // base name of the file
    Size() int64        // length in bytes for regular files; system-dependent for others
    Mode() FileMode     // file mode bits
    ModTime() time.Time // modification time
    IsDir() bool        // abbreviation for Mode().IsDir()
    Sys() interface{}   // underlying data source (can return nil)
}
```

* 如果指定的文件对象是一个符号链接，返回的FileInfo描述该符号链接指向的文件的信息，本函数会尝试跳转该链接，如果不想跳转连接，可使用 func Lstat(name string) (fi FileInfo, err error)

* 如果文件不存在 它返回 nil 和 错误

  ``` go 
   <nil> stat ./aaa: no such file or directory
  ```

* eg，判断文件是否存在：

  ``` go
  func fileExist(file string) bool {
  	info, err := os.Stat(file)
  	if err != nil {
  		return false
  	}
  	return !info.IsDir()
  }
  ```





### 执行系统命令 os/exec

执行命令可以使用`Run()`或者`Start()`方法，**`Run()`是阻塞的执行，`Start()`是非阻塞的执行**：

``` go
package main

import (
    "fmt"
    "os/exec"
)

func main() {
    command := exec.Command("ping","www.baidu.com")
    err := command.Run() // 阻塞执行
    if err != nil{
        fmt.Println(err.Error())
    }
}
```

golang下的os/exec包执行外部命令,它将os.StartProcess进行包装使得它更容易映射到stdin和stdout。这点和python下的command、os.system等功能是一样的



#### 获取输出。

``` go
var stdout bytes.Buffer
var stderr bytes.Buffer
cmd := exec.Command("bash", "-c", command)
// 指定标准，错误输出
cmd.Stdout = &stdout
cmd.Stderr = &stderr
err := cmd.Run()
return err, stdout.String(), stderr.String()
```

或者使用output方法：

``` go
out, err := exec.Command("bash", "-c", cmd).Output()
if err != nil {
    panic("some error found")
}
return string(out) // out是切片
```

**Output方法内部时间上调用的是Run方法，** 返回的是标准输出切片和错误：

``` go
func (c *Cmd) Output() ([]byte, error) {
	if c.Stdout != nil {
		return nil, errors.New("exec: Stdout already set")
	}
	var stdout bytes.Buffer
	c.Stdout = &stdout

	captureErr := c.Stderr == nil
	if captureErr {
		c.Stderr = &prefixSuffixSaver{N: 32 << 10}
	}

	err := c.Run()
	if err != nil && captureErr {
		if ee, ok := err.(*ExitError); ok {
			ee.Stderr = c.Stderr.(*prefixSuffixSaver).Bytes()
		}
	}
	return stdout.Bytes(), err
}
```



#### 使用管道 pipe

如果我们调用有持续性输出的命令，直接读取 Output 只是最后所有的结果，而不能拿到每次输出的结果，比如我们ping 4 次：

``` go
    cmd := exec.Command("/bin/bash", "-c", `ping 172.19.19.202 -w 4`)

    out1,_ := cmd.Output()
    fmt.Println("out1: ",string(out1))
```

可以使用管道配合start阻塞按行读取输出：

``` go

import (
    "bufio"
    "fmt"
    "os/exec"
)

func main() {
    cmd := exec.Command("/bin/bash", "-c", `ping 172.19.19.202 -w 4`)

    // out1,_ := cmd.Output()
    //fmt.Println("out1: ",string(out1))

    //创建获取命令输出管道
    stdout, err := cmd.StdoutPipe()
    if err != nil {
        fmt.Printf("Error:can not obtain stdout pipe for command:%s\n", err)
        return
    }

    //执行命令
    if err := cmd.Start(); err != nil {
        fmt.Println("Error:The command is err,", err)
        return
    }

    //使用带缓冲的读取器
    outputBuf := bufio.NewReader(stdout)
    for {
        //一次获取一行,_ 获取当前行是否被读完
        output, _, err := outputBuf.ReadLine()
        if err != nil {
            // 判断是否到文件的结尾了否则出错
            if err.Error() != "EOF" {
                fmt.Printf("Error :%s\n", err)
            }
            return
        }
        fmt.Printf("%s\n", string(output))
    }

    //wait 方法会一直阻塞到其所属的命令完全运行结束为止
    if err := cmd.Wait(); err != nil {
        fmt.Println("wait:", err.Error())
        return
    }
}
// output:
PING 172.19.19.202 (172.19.19.202) 56(84) bytes of data.
64 bytes from 172.19.19.202: icmp_seq=1 ttl=64 time=0.475 ms
64 bytes from 172.19.19.202: icmp_seq=2 ttl=64 time=0.377 ms
64 bytes from 172.19.19.202: icmp_seq=3 ttl=64 time=0.483 ms
64 bytes from 172.19.19.202: icmp_seq=4 ttl=64 time=0.390 ms

--- 172.19.19.202 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 76ms
rtt min/avg/max/mdev = 0.377/0.431/0.483/0.050 ms
```



#### 其他方法

```sh
func Command(name string, arg ...string) *Cmd
 `方法返回一个*Cmd， 用于执行name指定的程序(携带arg参数)
func (c *Cmd) Run() error
 `执行Cmd中包含的命令，阻塞直到命令执行完成
func (c *Cmd) Start() error
 `执行Cmd中包含的命令，该方法立即返回，并不等待命令执行完成
func (c *Cmd) Wait() error
 `该方法会阻塞直到Cmd中的命令执行完成，但该命令必须是被Start方法开始执行的
func (c *Cmd) Output() ([]byte, error)
 `执行Cmd中包含的命令，并返回标准输出的切片
func (c *Cmd) CombinedOutput() ([]byte, error)
 `执行Cmd中包含的命令，并返回标准输出与标准错误合并后的切片
func (c *Cmd) StdinPipe() (io.WriteCloser, error)
 `返回一个管道，该管道会在Cmd中的命令被启动后连接到其标准输入
func (c *Cmd) StdoutPipe() (io.ReadCloser, error)
 `返回一个管道，该管道会在Cmd中的命令被启动后连接到其标准输出
func (c *Cmd) StderrPipe() (io.ReadCloser, error)
 `返回一个管道，该管道会在Cmd中的命令被启动后连接到其标准错误
```





### 读文件

os包提供了两种打开文件的方法：

``` go
Open(name string) (*File, error) // 以只读的方式去打开文件，如果文件不存在或者程序没有足够的权限打开这个文件，Open函数会返回错误
func OpenFile(name string, flag int, perm FileMode) (*File, error) // 你可以设置打开文件的方式，以及文件的操作权限
```

#### Open

一个常规的读文件：

``` go 
func Read1()  (string){
    //获得一个file
    f, err := os.Open("file/test")
    if err != nil {
        fmt.Println("read fail")
        return ""
    }
    defer f.Close() // 记得提前关闭
    
    var chunk []byte  //把file读取到缓冲区中
    buf := make([]byte, 1024)

    for {
        n, err := f.Read(buf)  //从file读取到buf中
        if err != nil && err != io.EOF{
            fmt.Println("read buf fail", err)
            return ""
        }
        if n == 0 {         //说明读取结束
            break
        }
        //读取到最终的缓冲区中
        chunk = append(chunk, buf[:n]...) // [:n]是为了最后一次的读取
    }

    return string(chunk)
    //fmt.Println(string(chunk))
}
```

n==0 读取结束可以用：

``` go 
if err != io.EOF {
		mt.Println(err)
}
break
```

对于循环的每次迭代，都会更新内部文件指针。 下次读取时，将返回从文件指针偏移开始直到缓冲区大小的数据。 该指针不是语言的构造，而是操作系统之一。 在Linux上，此指针是要创建的文件描述符的属性。 所有的read / Read调用（分别在Ruby / Go中）在内部都转换为系统调用并发送到内核，并且内核管理此指针。



#### ReadAt

`file.ReadAt()`方法可以手动指定每次读取位置的偏移量。而不是默认设置。

``` go
    buf1 := make([]byte,1024)
    offset := 0
    for {
        len1, _ := file.ReadAt(buf1, int64(offset))
        offset = offset + len1
        if len1 == 0 {
            break
        }
        fmt.Println(string(buf1))
    }
```





#### OpenFile

OpenFile函数的第二个参数是文件的打开模式：

```go
const (
	// Exactly one of O_RDONLY, O_WRONLY, or O_RDWR must be specified.
	O_RDONLY int = syscall.O_RDONLY // 只读模式
	O_WRONLY int = syscall.O_WRONLY //只写模式
	O_RDWR   int = syscall.O_RDWR   // 读写混合模式
	// The remaining values may be or'ed in to control behavior.
	O_APPEND int = syscall.O_APPEND // 写模式的时候将数据附加到文件末尾
	O_CREATE int = syscall.O_CREAT  // 文件如果不存在就新建
	O_EXCL   int = syscall.O_EXCL   // 和 O_CREATE模式一起使用, 文件必须不存在
	O_SYNC   int = syscall.O_SYNC   //打开文件用于同步 I/O.
	O_TRUNC  int = syscall.O_TRUNC  // 打开文件时清空文件
)
// 注意  O_CREATE 文件不存在会新建文件，文件如果存在，会从文件开始处用新内容覆盖原始内容，(如果新内容只有5个字符，原始内容有10个，那么只有开始5个是新内容，后面5个还是以前的内容)
```

OpenFile函数的第三个参数是文件的权限，跟linux文件权限一致：

```
r ——> 004
w ——> 002
x ——> 001
```

eg:

``` go
func main() {
    //以读写方式打开文件，如果不存在，则创建
    openFile, e := os.OpenFile("c:/1.txt", os.O_RDWR|os.O_CREATE, 777)
    if e != nil {
        fmt.Println(e)
    }
    buf := make([]byte,1024)
    for {
        len, _ := openFile.Read(buf)
        if len == 0 {
            break
        }
        fmt.Println(string(buf))
    }
    openFile.Close()
}
```

通常情况如果你只是读文件操作，权限是可以被忽略的，第三个参数可以传0。而在写文件的时候，就需要传666，以确保你有足够的权限执行写入。



### 写文件

上面已经提到了写文件模式，一个demo:

``` go 
func main() {
    openFile, e := os.OpenFile("c:/1.txt", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 777)
    if e != nil {
        fmt.Println(e)
    }
    str := "overwrite to file"
    openFile.WriteString(str)
    openFile.Close()
}
```





### 常用方法

``` go
func Hostname() (name string, err error) // Hostname返回内核提供的主机名

func Getpid() int // Getpid返回调用者所在进程的进程ID
func Exit(code int) // Exit让当前程序以给出的状态码code退出。一般来说，状态码0表示成功，非0表示出错。程序会立刻终止，defer的函数不会被执行

func Getwd() (dir string, err error) // Getwd返回一个对应当前工作目录的根路径
func Mkdir(name string, perm FileMode) error // 使用指定的权限和名称创建一个目录
func MkdirAll(path string, perm FileMode) error // 使用指定的权限和名称创建一个目录，包括任何必要的上级目录，并返回nil，否则返回错误
func Remove(name string) error // 删除name指定的文件或目录
func TempDir() string // 返回一个用于保管临时文件的默认目
```

