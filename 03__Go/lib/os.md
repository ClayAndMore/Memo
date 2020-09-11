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



### 执行系统命令

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