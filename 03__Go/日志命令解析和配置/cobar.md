## cobar

https://github.com/spf13/cobra

### 安装

`go get -v github.com/spf13/cobra/cobra`

若成功安装则在 `$GOBIN` 即 `$GOPATH/bin` 下出现cobra可执行程序。

```sh
E:\gitCompany\src\SomeTest>E:\gitCompany\bin\cobra.exe -h
Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.

Usage:
  cobra [command]

Available Commands:
  add         Add a command to a Cobra Application
  help        Help about any command
  init        Initialize a Cobra Application

Flags:
  -a, --author string    author name for copyright attribution (default "YOUR NAME")
      --config string    config file (default is $HOME/.cobra.yaml)
  -h, --help             help for cobra
  -l, --license string   name of license for the project
      --viper            use Viper for configuration (default true)

Use "cobra [command] --help" for more information about a command.
```

E:\gitCompany 是我的GOPYTH.



### 创建程序 init

cobra的使用可以快速生成命令行文件程序，构建一个命令行程序的框架。

有两种情况，一个是已经有了程序文件目录，一个是从零开始构建。

1. 如果已经有了程序目录，执行：

   `E:\gitCompany\src\SomeTest>E:\gitCompany\bin\cobra.exe init --pkg-name SomeTest`

   会更改我的main.go文件，在当前目录下多加一个 cmd 文件夹

2. 目前还没有工程文件，

   `E:\gitCompany\src\SomeTest>E:\gitCompany\bin\cobra.exe init --pkg-name SomeTest SomeTest`, 后面要接新目录的名字。

构成的目录结构如下：

``` go
agenda/
    cmd/
	  root.go
    main.go
    LICENSE
```

此时，main.go:

``` go
package main

import "SomeTest/cmd"

func main() {
	cmd.Execute()
}
```

root.go

``` go
package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"os"

	homedir "github.com/mitchellh/go-homedir"
	"github.com/spf13/viper"
)

var cfgFile string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "SomeTest",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	//	Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.SomeTest.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
		// Find home directory.
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// Search config in home directory with name ".SomeTest" (without extension).
		viper.AddConfigPath(home)
		viper.SetConfigName(".SomeTest")
	}

	viper.AutomaticEnv() // read in environment variables that match

	// If a config file is found, read it in.
	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}
}
```



### 添加命令 add

尝试添加一个子命令 son：

`E:\gitCompany\src\SomeTest>E:\gitCompany\bin\cobra.exe add son`

此时 多了一个文件 cmd/son.go:

``` go 
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// sonCmd represents the son command
var sonCmd = &cobra.Command{
	Use:   "son",
	Short: "A brief description of your command",
	Long: `..`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("son called")
	},
}

func init() {
	rootCmd.AddCommand(sonCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// sonCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// sonCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
```



添加子命令的子命令：

```bash
# 在父命令config命令下创建子命令create,若没有指定-p,默认的父命令为rootCmd。
cobra add create -p 'configCmd' -a 'author name <email>'
```



### Flag 选项

cobra 有两种 flag，一个是全局变量，一个是局部变量。全局什么意思呢，就是所以子命令都可以用。局部的只有自己能用。

如 init 里：

``` go
var cfgFile string
func init() {
	// Cobra supports persistent flags, which, if defined here,
	// 全局 flag
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.SomeTest.yaml)")

	// Cobra also supports local flags, which will only run, 当前flag
	// when this action is called directly.
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
    // 一个长选项的测试
    rootCmd.Flags().Bool("toggle1", false, "Help message for toggle")
    rootCmd.Flags().String("name", "tom", "a person name")
}
```

输出：

``` sh
Flags:
      --config string   config file (default is $HOME/.SomeTest.yaml)
      --name string     a person name (default "tom")
  -t, --toggle          Help message for toggle
      --toggle1         Help message for toggle
```

我们可以发现：

* **全局flag 使用PersistentsFlags, local flag 使用 Flages**
* flag后的type分为四种： **type typeP typeVar typeVarP**
* **typeP 的为短选项， type (不带p)的为长选项**
* **ypeVar 的需要传入地址，不带Var的不需要**



#### 取值

对于上述有地址传入类型的typeVar, typeVarP,我们可以轻易的取值(实际上用这种方式的也比较多)，对于另外两种类型可以这样取值：

``` go
var rootCmd = &cobra.Command{
	Use:   "SomeTest",
	Short: "一个对应用的简短描述",
	Long: `一个对应用使用的长描述.`,

	Run: func(cmd *cobra.Command, args []string) {
		toggle, _ := cmd.Flags().GetBool("toggle")
			if toggle == false {
				fmt.Println("toggle 为 flase")	
			}
		name, _ := cmd.Flags().GetString("name")
			if name != ""{
				fmt.Println("名字: ", name)
			}
	},
}
```

输出：

``` sh
E:\gitCompany\src\SomeTest>go run main.go
toggle 为 flase
名字:  tom

E:\gitCompany\src\SomeTest>go run main.go --name xiaoming #也可使用 --name=xiaoming
toggle 为 flase
名字:  xiaoming
```



#### 必传参数

```go
	rootCmd.Flags().String("name", "tom", "a person name")
	rootCmd.MarkFlagRequired("name")
```

如果没有使用--name, 输出:

``` sh
Use "SomeTest [command] --help" for more information about a command.

required flag(s) "name" not set
```





### Run 

通过上方可见 cobra.Command 里有个Run的函数，其实还有很多：先后执行顺序如下：

- PersistentPreRun
- PreRun
- Run
- PostRun
- PersistentPostRu

他们接收`func(cmd *Command, args []string)`类型的函数，Persistent的能被下面的子命令继承

还有一种 可以返回错误类型的 RunE, 先后执行顺序如下：

- PersistentPreRunE
- PreRunE
- RunE
- PostRunE
- PersistentPostRunE

它们 接收`func(cmd *Command, args []string) error`的函数。



### Args

`&cobra.Command{}` 还可以传一个 Args, 我们称之为参数验证器：

``` go
var rootCmd = &cobra.Command{
	Use:   "SomeTest",
	Short: "一个对应用的简短描述",
	Long: `一个对应用使用的长描述.`,

	Args: cobra.MinimumNArgs(1),
}
```

这里 Args处验证了如果小于1个参数，那么将报错：

``` 
Use "SomeTest [command] --help" for more information about a command.

requires at least 1 arg(s), only received 0
```

其他验证函数：

- `NoArgs`: 如果存在任何位置参数，该命令将报告错误。
- `ArbitraryArgs`: 该命令将接受任何args。
- `OnlyValidArgs`: 如果存在任何不在ValidArgs字段中的位置参数，该命令将报告错误Command。
- `MinimumNArgs(int)`: 如果没有至少N个位置参数，该命令将报告错误。
- `MaximumNArgs(int)`: 如果有多于N个位置参数，该命令将报告错误。
- `ExactArgs(int)`: 如果没有确切的N位置参数，该命令将报告错误。
- `RangeArgs(min, max):` 如果args的数量不在预期args的最小和最大数量之间，则该命令将报告错误

自定义验证函数：

``` go
var cmd = &cobra.Command{
  Short: "hello",
  Args: func(cmd *cobra.Command, args []string) error {
    if len(args) < 1 {
      return errors.New("requires a color argument")
    }
    if myapp.IsValidColor(args[0]) {
      return nil
    }
    return fmt.Errorf("invalid color specified: %s", args[0])
  },
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello, World!")
  },
}
```



### example

可以添加example 做输出说明

``` go
var removeCmd = &cobra.Command{
	Use:   "remove",
        Aliases: []string{"rm"},
        Example: `
cli remove -n test
cli remove --name test
`,
```

out:

```
go run main.go app remove 

Usage:
  cli app remove [flags]

Examples:
cli remove -n test
cli remove --name test
```

