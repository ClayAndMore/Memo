---
title: "viper.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: ["go lib","go 日志命令解析和配置"]
categories: ["go"]
author: "Claymore"

---
Viper

https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fspf13%2Fviper

是国外大神 **spf13** 编写的开源配置解决方案，具有如下特性:

- 设置默认值
- 可以读取如下格式的配置文件：JSON、TOML、YAML、HCL
- 监控配置文件改动，并热加载配置文件
- 从环境变量读取配置
- 从远程配置中心读取配置（etcd/consul），并监控变动
- 从命令行 flag 读取配置
- 从缓存中读取配置
- 支持直接设置配置项的值

Viper 配置读取顺序：

- `viper.Set()` 所设置的值
- 命令行 flag
- 环境变量
- 配置文件
- 配置中心：etcd/consul
- 默认值



### demo

config.yaml:

```yaml
port: 10666
mysql:
  url: "(127.0.0.1:3306)/test"
  username: root
  password: 123456
```

读取：

```go
package main

import (
    "fmt"
    "github.com/spf13/viper"
)

// 定义配置文件解析后的结构
type MySQLConfig struct {
    URL      string
    Username string
    Password string
}

type Config struct {
    Port  int
    MySQL MySQLConfig
}

func main() {
    var config Config
    viper.SetConfigName("config")   // 设置配置文件名 (不带后缀),所以换格式也不用担心
    viper.AddConfigPath(".")        // 第一个搜索路径，
    err := viper.ReadInConfig()     // 读取配置数据
    if err != nil {
        panic(fmt.Errorf("Fatal error config file: %s \n", err))
    }
    viper.Unmarshal(&config)        // 将配置信息绑定到结构体上
    fmt.Println(config)         // {10666 {(127.0.0.1:3306)/test root 123456}}
    fmt.Printf("%+v", config)   // {Port:10666 MySQL:{URL:(127.0.0.1:3306)/test Username:root Password:123456}}
}

```

Viper 可以搜索多个路径，但目前单个 Viper 实例仅支持单个配置文件，Viper默认不搜索任何路径。

**注意：** `viper.SetConfigName("config")` 这里可以不写后缀，但是我们的配置文件一定要有后缀，不然会报找不到的错误，有配置文件名相同，后缀不同的话，优先使用`json`格式，其次是`toml`。

我们修改一下配置文件：

``` GO 
  USERNAME: root
  password1: 123456
```

再看输出：

```
{Port:10666 MySQL:{URL:(127.0.0.1:3306)/test Username:root Password:}}
```

可见 viper 是**忽略配置文件中的大小写的，大小写都没匹配到是没有值的**



### 时间的配置

我们为上述配置文件 加一个连接时间：

``` go
type MySQLConfig struct {
	URL      string
	Username string
	Password string
	TimeWait time.Duration // time对于秒，分，时，只有 Duration 类型来表示。
}
```

config.yaml:

``` yaml
mysql:
  url: "(127.0.0.1:3306)/test"
  USERNAME: root
  password: 123456
  timewait: 10 # 10s, 10m, 10min, 10min5s
```

我们分别该 timewait的值，观察下读到配置文件里的值：

```
timewait     TimeWait
10            10ns
10s           10s 
10m           10m0s
10min         0s
10m50s        10m50s
10m70s        11m10s
10h           10h0m0s
```

再尝试下 `fmt.Println(config.MySQL.TimeWait.Seconds())`

10s - 10,  10m - 600



### 设置值

#### 默认值

默认值不是必须的，如果配置文件、环境变量、远程配置系统、命令行参数、Set 函数都没有指定时，默认值将起作用

```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```

如果某个键通过`viper.Set`设置了值，那么这个值的优先级最高。

```
viper.Set("redis.port", 5381)
```



#### 监听配置变化

Viper 支持在程序运行时动态加载配置，只需要调用 viper 实例的 `WatchConfig` 函数，你也可以指定一个回调函数来获得变动的通知。

```go [guo]
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) {
    fmt.Println("配置发生变更：", e.Name)
})
```



####  获取值

在Viper中，有一些根据值的类型获取值的方法，存在以下方法：

- `Get(key string) : interface{}`
- `GetBool(key string) : bool`
- `GetFloat64(key string) : float64`
- `GetInt(key string) : int`
- `GetString(key string) : string`
- `GetStringMap(key string) : map[string]interface{}`
- `GetStringMapString(key string) : map[string]string`
- `GetStringSlice(key string) : []string`
- `GetTime(key string) : time.Time`
- `GetDuration(key string) : time.Duration`
- `IsSet(key string) : bool`

如果 `Get` 函数未找到值，则返回对应类型的一个零值。可以通过 `IsSet()` 方法来检测一个健是否存在。

```go
viper.GetString("logfile") // Setting & Getting 不区分大小写
if viper.GetBool("verbose") {
    fmt.Println("verbose enabled")
}
```

对应的修改配置

```
viper.Set("Verbose", true)
viper.Set("LogFile", LogFile)
```



#### 访问嵌套 key

访问方法也支持嵌套的键，如直接读取我们前面的 YAML 配置中的 MySQL 用户名

```
GetString("mysql.username") // root
```

eg:

```
common:
  database:
    name: test
    host: 127.0.0.1
```

如果要读取 host 配置，执行 `viper.GetString("common.database.host")` 即可。



#### 获取子级配置

当配置层级关系较多的时候，有时候我们需要直接获取某个子级的所有配置，可以这样操作：

```
app:
  cache1:
    max-items: 100
    item-size: 64
  cache2:
    max-items: 200
    item-size: 80
subv := viper.Sub("app.cache1")
```

subv 就代表：

```
max-items: 100
item-size: 64
```



#### 解析配置

可以将配置绑定到某个结构体、map上，有两个方法可以做到这一点：

- `Unmarshal(rawVal interface{}) : error`
- `UnmarshalKey(key string, rawVal interface{}) : error`

```go
var config Config
var mysql MySQL

err := Unmarshal(&config)            // 将配置解析到 config 变量
if err != nil {
    t.Fatalf("unable to decode into struct, %v", err)
}

err := UnmarshalKey("mysql", &mysql) // 将配置解析到 mysql 变量
if err != nil {
    t.Fatalf("unable to decode into struct, %v", err)
}
```



#### 设置别名



我们可以为 key 设置别名，当别名的值被重置后，原 key 对应的值也会发生变化。别名可以实现多个 key 引用单个值。

```
viper.RegisterAlias("loud", "Verbose")

viper.Set("verbose", true) 
viper.Set("loud", true)     // 这两句设置的都是同一个值

viper.GetBool("loud")       // true
viper.GetBool("verbose")    // true
```



### 读取

#### 从 `io.Reader` 中读取配置

Viper 预先定义了许多配置源，例如文件、环境变量、命令行参数和远程K / V存储系统，但您并未受其约束。 您也可以实现自己的配置源，并提供给 viper。

```
viper.SetConfigType("yaml") // 这里不区分大小写

var yamlExample = []byte(`
Hacker: true
name: steve
hobbies:
- skateboarding
- snowboarding
- go
clothing:
  jacket: leather
  trousers: denim
age: 35
eyes : brown
beard: true
`)

viper.ReadConfig(bytes.NewBuffer(yamlExample))

viper.Get("name") // 返回 "steve"
```

#### 从环境变量中读取

Viper 支持环境变量，使得我们可以开箱即用，很多时候环境参数是从命令行传入的。有四个和环境变量有关的方法：

- `AutomaticEnv()`
- `BindEnv(string...) error`
- `SetEnvPrefix(string)`
- `SetEnvKeyReplacer(string...) *strings.Replacer`

> 注意，环境变量时区分大小写的。

Viper 提供了一种机制来确保 `Env` 变量是唯一的。通过设置环境变量前缀 `SetEnvPrefix`，在从环境变量读取时会添加设置的前缀。`BindEnv` 和 `AutomaticEnv` 函数都会使用到这个前缀。

`BindEnv` 需要一个或两个参数。第一个参数是键名，第二个参数是环境变量的名称。环境变量的名称区分大小写。如果没有提供 ENV 的变量名，Viper 会自动假定该键名称与 ENV 变量名称匹配，并且 ENV 变量为全部大写。当你显式提供 ENV 变量名称时，它不会自动添加前缀。

使用 ENV 变量时要注意，当关联后，每次访问时都会读取该 ENV 值。Viper 在 `BindEnv` 调用时不读取 ENV 值。

`AutomaticEnv` 与 `SetEnvPrefix` 结合将会特别有用。当 `AutomaticEnv` 被调用时，任何 `viper.Get` 请求都会去获取环境变量。环境变量名为 `SetEnvPrefix` 设置的前缀，加上对应名称的大写。

`SetEnvKeyReplacer` 允许你使用一个 `strings.Replacer` 对象来将配置名重写为 Env 名。如果你想在`Get()` 中使用包含-的配置名 ，但希望对应的环境变量名包含 `_` 分隔符，就可以使用该方法。使用它的一个例子可以在项目中 `viper_test.go` 文件里找到。

```
SetEnvPrefix("spf")       // 将会自动转为大写
BindEnv("id")             // 必须要绑定后才能获取

BindEnv("loglevel", "LOG_LEVEL"); //直接指定了loglevel所对应的环境变量，则不会去补全前缀

os.Setenv("SPF_ID", "13") // 通常通过系统环境变量来设置
id := Get("id")           // 13
```

#### 读取远程 Key/Value

启用该功能，需要导入 `viper/remot` 包：

```
import _ "github.com/spf13/viper/remote"
```

Viper 可以从如 `etcd`、`Consul` 的远程 `Key/Value` 存储系统的一个路径上，读取一个配置字符串（JSON, TOML, YAML 或 HCL格式）。

这些值会优于默认值，但会被从磁盘文件、命令行 flag、环境变量的配置所覆盖。

Viper 使用 [crypt](https://github.com/xordataexchange/crypt) 从 `K/V` 存储系统里读取配置，意味着你可以加密储存你的配置信息，并且可以自动解密配置信息，加密是可选项。

你可以将远程配置与本地配置结合使用，也可以独立使用。

`crypt` 有一个命令行工具可以帮助你存储配置信息到 K/V 存储系统，`crypt` 在 [http://127.0.0.1:4001](http://127.0.0.1:4001/) 上默认使用 etcd。

```
$ go get github.com/xordataexchange/crypt/bin/crypt
$ crypt set -plaintext /config/biezhi.json /Users/biezhi/settings/config.json
```

确认你的值被设置：

```
$ crypt get -plaintext /config/biezhi.json
```

有关 `crypt` 如何设置加密值或如何使用 Consul 的示例，请参考文档。

**远程 Key/Value 存储例子 - 未加密的**

```
viper.AddRemoteProvider("etcd", "http://127.0.0.1:4001", "/config/biezhi.json")
viper.SetConfigType("json") // 因为不知道格式，所以需要指定
err := viper.ReadRemoteConfig()
```

**远程 Key/Value 存储例子 - 加密的**

```
viper.AddSecureRemoteProvider("etcd", "http://127.0.0.1:4001",
"/config/biezhi.json","/etc/secrets/mykeyring.gpg")

viper.SetConfigType("json") // 因为不知道格式，所以需要指定
err := viper.ReadRemoteConfig()
```





### pflag

https://github.com/spf13/pflag

https://o-my-chenjian.com/2017/09/20/Using-Flag-And-Pflag-With-Golang/