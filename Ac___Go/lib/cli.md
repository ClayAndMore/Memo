Tags:[Go, go_lib]



## 写在前面

GIthub: `https://github.com/urfave/cli`

API: `https://godoc.org/github.com/urfave/cli`

### Get Start

```go
package main

import (
  "log"
  "os"

  "github.com/urfave/cli"
)

func main() {
  err := cli.NewApp().Run(os.Args)
  if err != nil {
    log.Fatal(err)
  }
}
```

`go build -> cli -> ./cli:`

```
NAME:
   cli - A new cli application

USAGE:
   cli [global options] command [command options] [arguments...]

VERSION:
   0.0.0

COMMANDS:
     help, h  Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h     show help
   --version, -v  print the version
```

补冲说明：

```go
app := cli.NewApp()
app.Name = "boom"
app.Usage = "make an explosive entrance"
app.Version = "1.2.3"
```



### Action

所有动作的触发在这里：

```go
  app.Action = func(c *cli.Context) error {
    fmt.Println("boom! I say!")
    return nil
  }
```



#### 位置参数

```go
  app := cli.NewApp()
  app.Action = func(c *cli.Context) error {
    fmt.Printf("Hello %q \n", c.Args().Get(0))
    return nil
  }
```

调用：

```
./cli
Hello "" 
./cli ss
Hello "ss" 
./cli 123
Hello "123" 
```

注意这里c.Args()拿到的是所有传入的参数



### Flags

#### 配置可选参数

```go
  app := cli.NewApp()

  app.Flags = []cli.Flag {
    cli.StringFlag{
      Name: "lang",
      Value: "english",
      Usage: "language for the greeting",
    },
  }

  app.Action = func(c *cli.Context) error {
    name := "Nefertiti"
    if c.NArg() > 0 {
      name = c.Args().Get(0)
    }
    if c.String("lang") == "spanish" {
      fmt.Println("Hola", name)
    } else {
      fmt.Println("Hello", name)
    }
    return nil
  }

```

测试：

```
GLOBAL OPTIONS:
   --lang value   language for the greeting (default: "english")
   --help, -h     show help
   --version, -v  print the version
2019/02/19 13:23:12 flag needs an argument: -lang
root@VM# ./flags --lang ss
Hello Nefertiti
root@VM# ./flags --lang spanish
Hola Nefertiti
```

`Value: "english"` 是默认值， 没有value则没有默认值

除了StringFlag 还有 IntFlag 等。



人性化提示：

```
Usage: "language for the `FILE`",
```

out:

`--lang FILE, -l FILE  language for the FILE (default: "english")`



#### 简短命令行

`Name: "lang",`  -> `Name: "lang, l",`

```
GLOBAL OPTIONS:
   --lang value, -l value  language for the greeting (default: "english")
```



#### 命令行映射到变量

```go
var language string   // changed

app := cli.NewApp()

app.Flags = []cli.Flag {
    cli.StringFlag{
        Name:        "lang",
        Value:       "english",   
        Usage:       "language for the greeting",
        Destination: &language,  // changed
    },
}

app.Action = func(c *cli.Context) error {
    name := "someone"
    if c.NArg() > 0 {
      name = c.Args()[0]
    }
    if language == "spanish" {  // changed
      fmt.Println("Hola", name)
    } else {
      fmt.Println("Hello", name)
    }
    return nil
  }
```



#### Ordering

命令排序

正常来说帮助信息里的flag是按照代码里的声明顺序排列的



#### EnvVar

默认值根据环境变量

`EnvVar: "APP_LANG",`

`--lang FILE, -l FILE  language for the FILE (default: "english") [$APP_LANG]`

#### Filpath

默认值根据环境变量, 该默认值会覆盖EnvVar



### Commands

#### 固定参数

```go
package main
  
import (
    "os"
    "log"
    "fmt"
    "github.com/urfave/cli"
)

func main() {
    app := cli.NewApp()
    app.Commands = []cli.Command {
    {
        Name: "add",
        Aliases: []string{"a"},
        Usage: "calc 1+1",
        //Category: "arithmetic",  分类
        Action: func(c *cli.Context) error {
            fmt.Println("1 + 1 = ", 1 + 1)
            return nil
        },
    },
    }
    err := app.Run(os.Args)
    if err != nil {
        log.Fatal(err)
    }
}
```

使用：

```
NAME:
   command - A new cli application

USAGE:
   command [global options] command [command options] [arguments...]

VERSION:
   0.0.0

COMMANDS:
     add, a   calc 1+1
     help, h  Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h     show help
   --version, -v  print the version
   
   
root@VM# ./command a
1 + 1 =  2
root@VM# ./command add
1 + 1 =  2
```



#### subcommands

```go
  app := cli.NewApp()

  app.Commands = []cli.Command{
    {
      Name:    "add",
      Aliases: []string{"a"},  // 起别名
      Usage:   "add a task to the list",
      Action:  func(c *cli.Context) error {
        fmt.Println("added task: ", c.Args().First())
        return nil
      },
    },
    {
      Name:    "complete",
      Aliases: []string{"c"},  // 起别名
      Usage:   "complete a task on the list",
      Action:  func(c *cli.Context) error {
        fmt.Println("completed task: ", c.Args().First())  // 拿到c后的参数
        return nil
      },
    },
    {
      Name:        "template",
      Aliases:     []string{"t"},
      Usage:       "options for task templates",
      Subcommands: []cli.Command{
        {
          Name:  "add",
          Usage: "add a new template",
          Action: func(c *cli.Context) error {
            fmt.Println("new task template: ", c.Args().First())
            return nil
          },
        },
        {
          Name:  "remove",
          Usage: "remove an existing template",
          Action: func(c *cli.Context) error {
            fmt.Println("removed task template: ", c.Args().First())
            return nil
          },
        },
      },
    },
  }

```

help command:

```
COMMANDS:
     add, a       add a task to the list
     complete, c  complete a task on the list
     template, t  options for task templates
     help, h      Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h     show help
   --version, -v  print the version
```

test:

```
root@VM# ./subcommands a dachui
added task:  dachui
root@#:~/go_workspace/src/cli# ./subcommands c dachui
completed task:  dachui
root@# ./subcommands t   # 注意这里的提示信息，有子命令的帮助信息
NAME:
   subcommands template - options for task templates

USAGE:
   subcommands template command [command options] [arguments...]

COMMANDS:
     add     add a new template  
     remove  remove an existing template

OPTIONS:
   --help, -h  show help
   
root@VM# ./subcommands t add dachui
new task template:  dachui
```



### before/after

在命令行解析前和后做的事情

	app.Before = func(c *cli.Context) error {
		fmt.Println("app Before")
		return nil
	}
	app.After = func(c *cli.Context) error {
		fmt.Println("app After")
		return nil
	}

