---
title: "go-zap.md"
date: 2020-04-17 08:38:29 +0800
lastmod: 2020-04-17 19:54:27 +0800
draft: false
tags: ["go lib", "go 日志命令解析和配置"]
categories: ["go"]
author: "Claymore"

---
Uber 推出的go 日志记录库

Github: https://github.com/uber-go/zap

安装: `go get -u go.uber.org/zap`



### 日志记录器

Zap提供了两种类型的日志记录器—`Sugared Logger`和`Logger`。

在性能很好但不是很关键的上下文中，使用`SugaredLogger`。它比其他结构化日志记录包快4-10倍，并且支持结构化和printf风格的日志记录。

``` go
logger, _ := zap.NewProduction()
defer logger.Sync() // flushes buffer, if any, 刷新buffer, 如果有的话
sugar := logger.Sugar()
sugar.Infow("failed to fetch URL",
  // Structured context as loosely typed key-value pairs.
  // 宽松的 k-v 对儿 结构 
  "url", url,
  "attempt", 3,
  "backoff", time.Second,
)
sugar.Infof("Failed to fetch URL: %s", url)
```

在每一微秒和每一次内存分配都很重要的上下文中，

**使用`Logger`它甚至比`SugaredLogger`更快，内存分配次数也更少，但它只支持强类型的结构化日志记录。**

``` go
logger, _ := zap.NewProduction()
defer logger.Sync()
logger.Info("failed to fetch URL",
  // Structured context as strongly typed Field values.
  // 强类型的 k-v 对儿
  zap.String("url", url),
  zap.Int("attempt", 3),
  zap.Duration("backoff", time.Second),
)
```



### filed

由于 fmt.Printf 之类的方法大量使用 interface{} 和反射，会有性能损失。zap为了提高性能，减少内存的分配次数，没有使用反射，默认的logger只支持强类型的，结构化的日志。

zap.Type, Type 为 `bool/int/uint/float64/complex64/time.Time/time.Duration/error` 等。

zap.Typep 以p结尾的表示指针字段，以s结尾表示该类型的切片字段：

``` go
zap.Bool(key string, val bool) Field: bool 
zap.BoolP(key string, val bool) Field: bool 指针字段
zap.Bools(key string, val []bool) Field: bool 切片字段

// 一些特殊类型的字段：
zap.Any(key string, value interface{}) Field  任意类型的字段
zap.Binary(key string, val []byte) Field  二进制串的字段
```





### logger 

通过调用`zap.NewProduction()`/`zap.NewDevelopment()`或者`zap.Example()`创建一个Logger。唯一的区别在于它将记录的信息不同.

#### NewProduction()

json化输出

``` go
package main

import (
	"go.uber.org/zap"
	"net/http"
)

var logger *zap.Logger

func InitLogger() {
	logger, _ = zap.NewProduction()
}

func simpleHttpGet(url string) {
	resp, err := http.Get(url)
	if err != nil {
		logger.Error("Error fetching url..", zap.String("url", url), zap.Error(err))
	} else {
		logger.Info("Success..", zap.String("statusCode", resp.Status), zap.String("url", url))
		resp.Body.Close()
	}
}

func main() {
	InitLogger()
	defer logger.Sync()
	simpleHttpGet("www.qq.com")
	simpleHttpGet("http://www.qq.com")
}
```

输出：

``` json
{"level":"error","ts":1587006509.9558568,"caller":"gotest/main.go:17","msg":"Error fetching url..","url":"www.qq.com","error":"Get www.qq.com: unsupported protocol scheme \"\"","stacktrace":"main.simpleHttpGet\n\t/Users/claymore/Documents/go/src/gotest/main.go:17\nmain.main\n\t/Users/claymore/Documents/go/src/gotest/main.go:27\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:203"}
{"level":"info","ts":1587006510.2426739,"caller":"gotest/main.go:19","msg":"Success..","statusCode":"200 OK","url":"http://www.qq.com"}
```

可以看到输出等级，时间，调用行号等。

logger.XXX, 可以是Info / Error/ Debug / Panic等。每个方法都接受一个消息字符串和任意数量的`zapcore.Field` 参数。

每个`zapcore.Field`其实就是一组键值对参数。



#### NewDevelopment()

格式化输出

``` go
package main

import (
	"go.uber.org/zap"
	"time"
)

func main() {
	// zap.NewProduction json序列化输出
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()
	logger.Info("无法获取网址",
		zap.String("url", "http://www.google.com"),
		zap.Int("attempt", 3),
		zap.Duration("backoff", time.Second),
	)
}
```

输出：

```
2020-04-16T11:19:52.642+0800    INFO    zapTest/simple.go:12    无法获取网址    {"url": "http://www.google.com", "attempt": 3, "backoff": "1s"}
```



### 定制logger

使用`zap.New(…)`方法来手动传递所有配置，而不是使用像`zap.NewProduction()`这样的预置方法来创建logger

`func New(core zapcore.Core, options ...Option) *Logger`

其中 zapcore.Core`需要三个配置——`Encoder`，`WriteSyncer`，`LogLevel

* .**Encoder**:编码器(如何写入日志)。我们将使用开箱即用的`NewJSONEncoder()`，并使用预先设置的`ProductionEncoderConfig()`

  ```
  zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
  ```

* **WriterSyncer** ：指定日志将写到哪里去。我们使用`zapcore.AddSync()`函数并且将打开的文件句柄传进去。

  ```go
   file, _ := os.Create("./test.log")
   writeSyncer := zapcore.AddSync(file)
  ```

* **Log Level**：哪种级别的日志将被写入。



#### 日志写入文件

``` go
package main

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"os"
	"time"
)

var logger *zap.Logger

func InitLogger() {
	writeSyncer := getLogWriter()
	encoder := getEncoder()
	core := zapcore.NewCore(encoder, writeSyncer, zapcore.DebugLevel)
	logger = zap.New(core)
  // sugarLogger = logger.Sugar()
}

func getEncoder() zapcore.Encoder {
	return zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
  // 如果不想以json形式输出，可以改成普通的Encoder:
  //return zapcore.NewConsoleEncoder(zap.NewProductionEncoderConfig())
}

func getLogWriter() zapcore.WriteSyncer {
	file, _ := os.Create("./test.log")
	return zapcore.AddSync(file)
}

func main() {
	InitLogger()
	defer logger.Sync()
	logger.Info("无法获取网址",
		zap.String("url", "http://www.google.com"),
		zap.Int("attempt", 3),
		zap.Duration("backoff", time.Second),
	)
}
```

控制台没有输出，查看下文件：

```sh
~ cat test.log 
{"level":"info","ts":1587009900.752939,"msg":"无法获取网址","url":"http://www.google.com","attempt":3,"backoff":1}
```

注意，再次输出时会清空上次日志内容



#### 更改输出信息

使用一般形式输出如下：

```
1.572161052068744e+09	info	Success! statusCode = 200 OK for URL http://www.google.com
```

我们要做的更改：

* 时间是时间戳，人类不可读，
* 没有调用信息
* 大写日志级别

修改：

``` go
func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder // 时间
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder // 大写
	return zapcore.NewConsoleEncoder(encoderConfig)
}

logger := zap.New(core, zap.AddCaller()) // 调用者
```

输出：

```
2020-04-16T12:23:53.519+0800    INFO    zapTest/CustomLogger.go:37      无法获取网址    {"url": "http://www.google.com", "attempt": 3, "backoff": 1}
```



#### AddCallerSkip

有时我们稍微封装了一下记录日志的方法，但是我们希望输出的文件名和行号是调用封装函数的位置。这时可以使用`zap.AddCallerSkip(skip int)`向上跳 1 层：

``` go
func Output(msg string, fields ...zap.Field) {
  zap.L().Info(msg, fields...)
}

func main() {
  logger, _ := zap.NewProduction(zap.AddCaller(), zap.AddCallerSkip(1))
  defer logger.Sync()

  zap.ReplaceGlobals(logger)

  Output("hello world")
}
// out:

{"level":"info","ts":1587740501.5592482,"caller":"skip/main.go:15","msg":"hello world"}
```

输出在`main`函数中调用`Output()`的位置。如果不指定`zap.AddCallerSkip(1)`，将输出`"caller":"skip/main.go:6"`，这是在`Output()`函数中调用`zap.Info()`的位置。因为这个`Output()`函数可能在很多地方被调用，所以这个位置参考意义并不大



### zap config

NewProduction 和 NewDevelopment 是封装好的生成日志配置。我们可以通过更细致的config来配置

``` go 
package main

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"fmt"
	"time"
)

func main() {
	// 生成格式的一些配置
	encoderConfig := zapcore.EncoderConfig{
		TimeKey:        "time",							// 输出时间的key名 ， 基本上是json输出中的key
		LevelKey:       "level",						// 输出日志级别的key名
		NameKey:        "logger",
		CallerKey:      "caller",
		MessageKey:     "msg",                          // 输入信息的key名
		StacktraceKey:  "stacktrace",
		LineEnding:     zapcore.DefaultLineEnding,      // 每行的分隔符。基本zapcore.DefaultLineEnding 即"\n"
		EncodeLevel:    zapcore.LowercaseLevelEncoder,  // 将日志级别字符串转化为小写
		EncodeTime:     zapcore.ISO8601TimeEncoder,     // ISO8601 UTC 时间格式
		EncodeDuration: zapcore.SecondsDurationEncoder, // zapcore.SecondsDurationEncoder,执行消耗的时间转化成浮点型的秒
		EncodeCaller:   zapcore.FullCallerEncoder,      // 一般用zapcore.ShortCallerEncoder，以包/文件:行号 格式化调用堆栈
	}


	config := zap.Config{
		Level:            zap.NewAtomicLevelAt(zap.DebugLevel),                                                // 日志级别
		Development:      true,                                                // 是否是开发环境。如果是开发模式，对DPanicLevel进行堆栈跟踪
		Encoding:         "json",                                              // 输出格式 console 或 json
		EncoderConfig:    encoderConfig,                                       // 编码器配置
		InitialFields:    map[string]interface{}{"serviceName": "spikeProxy"}, // 初始化字段，如：添加一个服务器名称
		OutputPaths:      []string{"stdout", "./stdout.log"},         // 输出到指定文件 或 stdout（标准输出，正常颜色） stderr（错误输出，红色）
		ErrorOutputPaths: []string{"stderr", "./stderr.log"},         // 错误输出
	}
	/*
	其他字段：
	DisableCaller：bool 禁止使用调用函数的文件名和行号来注释日志。默认进行注释日志
	DisableStacktrace：bool 是否禁用堆栈跟踪捕获。默认对Warn级别以上和生产error级别以上的进行堆栈跟踪。
	当然了，如果想控制台输出，OutputPaths和ErrorOutputPaths不能配置为文件地址，而应该改为stdout。
	 */

	// 构建日志
	logger, err := config.Build()
	if err != nil {
		panic(fmt.Sprintf("log 初始化失败: %v", err))
	}
	logger.Info("log 初始化成功")

	logger.Info("无法获取网址",
		zap.String("url", "http://www.google.com"),
		zap.Int("attempt", 3),
		zap.Duration("backoff", time.Second),
	)
}
```

个人觉得这种方式定制性高，但是写起来太麻烦。



### 动态调整日志级别

通过 http 请求动态调整当前日志的级别。

``` go
package main

import (
    "fmt"
    "go.uber.org/zap"
    "net/http"
    "time"
)

func main() {
    alevel := zap.NewAtomicLevel()
    http.HandleFunc("/handle/level", alevel.ServeHTTP)
    go func() {
        if err := http.ListenAndServe(":9090", nil); err != nil {
            panic(err)
        }
    }()
    // 默认是Info级别
    logcfg := zap.NewProductionConfig()
    logcfg.Level = alevel

    logger, err := logcfg.Build()
    if err != nil {
        fmt.Println("err", err)
    }

    defer logger.Sync()
    for i := 0; i < 1000; i++ {
        time.Sleep(1 * time.Second)
        logger.Debug("debug log", zap.String("level", alevel.String()))
        logger.Info("Info log", zap.String("level", alevel.String()))
    }
}
```

查看日志级别

```
curl http://localhost:9090/handle/level
```

输出

```
{"level":"info"}
```

调整日志级别(可选值 “debug” “info” “warn” “error” 等)

```
curl -XPUT --data '{"level":"debug"}' http://localhost:9090/handle/level
```

输出

```
{"level":"debug"}
```





## 日志归档和切割 lumberjack

https://github.com/natefinch/lumberjack

有两种安装方式：go get -u github.com/natefinch/lumberjack

和 go get gopkg.in/natefinch/lumberjack.v2， 第二种用的人多点，到现在我也没有下载出来

要在zap中加入Lumberjack支持:

```go
func getLogWriter() zapcore.WriteSyncer {
    lumberJackLogger := &lumberjack.Logger{
        Filename:   "./test.log",
        MaxSize:    10,
        MaxBackups: 5,
        MaxAge:     30,
        Compress:   false,
    }
    return zapcore.AddSync(lumberJackLogger)
}
```

Lumberjack Logger采用以下属性作为输入:

- Filename: 日志文件的位置
- MaxSize：在进行切割之前，日志文件的最大大小（以MB为单位）
- MaxBackups：保留旧文件的最大个数
- MaxAges：保留旧文件的最大天数
- Compress：是否压缩/归档旧文件



## 一个全局的logger 配置

目录：

```
gotest/
	logger/
		log.go
	main.go
```



log.go:

``` go 
package logger

import (
	"git.cloud.top/DSec/apiserver/utils"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"github.com/natefinch/lumberjack"
	"io"
	"os"
)

var Logger *zap.Logger

func init() {

	// 两种判断日志等级的interface
	infoLevel := zap.LevelEnablerFunc(func(level zapcore.Level) bool {
		return level < zapcore.WarnLevel
	})

	warnLevel := zap.LevelEnablerFunc(func(level zapcore.Level) bool {
		return level >= zapcore.WarnLevel
	})

	allLevel := zap.LevelEnablerFunc(func(lvl zapcore.Level) bool {
		return lvl >= zapcore.DebugLevel
	})

	consoleDebugging := zapcore.Lock(os.Stdout)
	encoder := getEncoder()
	consoleEncoder := zapcore.NewConsoleEncoder(zap.NewDevelopmentEncoderConfig())

	infoHook := getLogWriter("debug.log")
	warnHook := getLogWriter("err.log")

	core := zapcore.NewTee(
		// 打印到 调试输出文件
		zapcore.NewCore(encoder, zapcore.AddSync(infoHook), infoLevel),
		// 打印到 错误输出文件
		zapcore.NewCore(encoder, zapcore.AddSync(warnHook), warnLevel),
		// 打印到控制台
		zapcore.NewCore(consoleEncoder, consoleDebugging, allLevel),
	)
	Logger = zap.New(core, zap.AddCaller())
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	//  zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder // 时间格式
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder // 大写级别
	return zapcore.NewConsoleEncoder(encoderConfig)

}

func getLogWriter(filename string ) io.Writer {
	hook := lumberjack.Logger{
		Filename:   utils.LOG_SAVE_DIR + filename, // 日志文件路径
		MaxSize:    utils.LOG_MAX_SIZE, // megabytes
		MaxBackups: utils.LOG_BACKUPS,    // 最多保留3个备份
		MaxAge:     utils.LOG_MAX_AGE,    //days
		Compress:   utils.LOG_COMPRESS, // 是否压缩 disabled by default
	}
	return &hook
}
```



main.go:

``` go
package main

import (
	//"go.uber.org/zap"
	"gotest/logger"
)

func main() {
	logger.Logger.Info("i'am info ")
	logger.Logger.Debug("i'am debug")
	logger.Logger.Error("i'am error")
	logger.Logger.Warn("i'am warn")
}
```

输出：

``` sh
~/Documents/go/src/gotest cat log/err.log
2020-04-16T16:15:28.780+0800    ERROR   gotest/main.go:11       i'am error
2020-04-16T16:15:28.780+0800    WARN    gotest/main.go:12       i'am warn

~/Documents/go/src/gotest cat log/debug.log                           
2020-04-16T16:15:28.779+0800    INFO    gotest/main.go:9        i'am info 
2020-04-16T16:15:28.780+0800    DEBUG   gotest/main.go:10       i'am debug
```



## 使用zap提供的全局配置

为了方便使用，`zap`提供了两个全局的`Logger`，一个是`*zap.Logger`，可调用`zap.L()`获得；另一个是`*zap.SugaredLogger`，可调用`zap.S()`获得。需要注意的是，全局的`Logger`默认并不会记录日志

可以使用`ReplaceGlobals(logger *Logger) func()`将`logger`设置为全局的`Logger`，该函数返回一个无参函数，用于恢复全局`Logger`设置：

``` go
func main() {
  zap.L().Info("global Logger before")
  zap.S().Info("global SugaredLogger before")

  logger := zap.NewExample()
  defer logger.Sync()

  zap.ReplaceGlobals(logger)
  zap.L().Info("global Logger after")
  zap.S().Info("global SugaredLogger after")
}

// out:
{"level":"info","msg":"global Logger after"}
{"level":"info","msg":"global SugaredLogger after"}

// 在调用 ReplaceGlobals 之前记录的日志并没有输出。
```

