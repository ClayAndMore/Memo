### 多输出

``` go
package main

import (
    "io/ioutil"
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
    "gopkg.in/natefinch/lumberjack"
    "os"
)

func main(){
    // First, define our level-handling logic.
    // 仅打印Error级别以上的日志
    highPriority := zap.LevelEnablerFunc(func(lvl zapcore.Level) bool {
        return lvl >= zapcore.ErrorLevel
    })
    // 打印所有级别的日志
    lowPriority := zap.LevelEnablerFunc(func(lvl zapcore.Level) bool {
        return lvl >= zapcore.DebugLevel
    })

    hook := lumberjack.Logger{
        Filename:   "/tmp/abc.log",
        MaxSize:    1024, // megabytes
        MaxBackups: 3,
        MaxAge:     7,    //days
        Compress:   true, // disabled by default
    }


    topicErrors := zapcore.AddSync(ioutil.Discard)
    fileWriter := zapcore.AddSync(&hook)

    // High-priority output should also go to standard error, and low-priority
    // output should also go to standard out.
    consoleDebugging := zapcore.Lock(os.Stdout)

    // Optimize the Kafka output for machine consumption and the console output
    // for human operators.
    kafkaEncoder := zapcore.NewJSONEncoder(zap.NewProductionEncoderConfig())
    consoleEncoder := zapcore.NewConsoleEncoder(zap.NewDevelopmentEncoderConfig())

    // Join the outputs, encoders, and level-handling functions into
    // zapcore.Cores, then tee the four cores together.
    core := zapcore.NewTee(
        // 打印在kafka topic中（伪造的case）
        zapcore.NewCore(kafkaEncoder, topicErrors, highPriority),
        // 打印在控制台
        zapcore.NewCore(consoleEncoder, consoleDebugging, lowPriority),
        // 打印在文件中
        zapcore.NewCore(consoleEncoder, fileWriter, highPriority),
    )

    // From a zapcore.Core, it's easy to construct a Logger.
    logger := zap.New(core)
    defer logger.Sync()
    logger.Info("constructed a info logger", zap.Int("test", 1))
    logger.Error("constructed a error logger", zap.Int("test", 2))
}
```





### 日志时间归档

他原生不支持文件归档，如果要支持文件按大小或者时间归档，必须要使用第三方库, 根据官方资料参考资料，官方推荐的是 [natefinch/lumberjack](https://github.com/natefinch/lumberjack)

``` go
package main

import (
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
    "gopkg.in/natefinch/lumberjack.v2"
)
// logpath 日志文件路径
// loglevel 日志级别
func initLogger(logpath string, loglevel string) *zap.Logger {

    hook := lumberjack.Logger{
        Filename:   logpath, // 日志文件路径
        MaxSize:    1024, // megabytes
        MaxBackups: 3,    // 最多保留3个备份
        MaxAge:     7,    //days
        Compress:   true, // 是否压缩 disabled by default
    }
    w := zapcore.AddSync(&hook)

    var level zapcore.Level
    switch loglevel {
    case "debug":
        level = zap.DebugLevel
    case "info":
        level = zap.InfoLevel
    case "error":
        level = zap.ErrorLevel
    default:
        level = zap.InfoLevel
    }
    encoderConfig := zap.NewProductionEncoderConfig()
    encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
    core := zapcore.NewCore(
        zapcore.NewConsoleEncoder(encoderConfig),
        w,
        level,
    )

    logger := zap.New(core)
    logger.Info("DefaultLogger init success")

    return logger
}

func main() {
    logger := initLogger("/tmp/all.log", "info")
    logger.Info("test log", zap.Int("line", 47))

}
```





**注意** ， 使用了这个库之后就无法设置日志采样等原生的高级功能了



