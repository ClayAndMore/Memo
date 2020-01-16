## Go mod

Golang从诞生之初就一直有个被诟病的问题：缺少一个行之有效的“官方”包依赖管理工具。其原因是在Google内部，所有人都是在一个代码库上进行开发的，因此并不是非常需要。但Golang变成一个社区化的工程语言之后，这个问题被放大了。

1. GOPATH不符合一般开发者习惯，大部分人更习惯maven、node modules之类的方式
2. GOPATH无法有效的管理版本依赖，没有一个地方能够表明依赖包的具体版本号，无法形成有效的版本配套关系

在Golang 1.5发布了vendor特性之后，社区在vendor基础上开发了很多包管理工具，例如glide, dep(这个最悲催，已经半官方了，结果横刀杀出来一个go mod)

同样的库，同样的版本，就因为在不同的工程里用了，就要在vendor里单独搞一份，不浪费吗？所以这些基于vendor的包管理工具，都会有这个问题。

相比之下maven这种本地缓存库的管理方式就好很多。

Golang 1.11 版本引入的 go mod ，其思想类似maven：摒弃vendor和GOPATH，拥抱本地库。

考虑向前兼容，目前仍然可以用go get，但最终这个命令是会消失的。



### 所有命令

命令 说明  

 download download modules to local cache(下载依赖包)  edit edit go.mod from tools or scripts（编辑go.mod  graph print module requirement graph (打印模块依赖图)  init initialize new module in current directory（在当前目录初始化mod）  tidy add missing and remove unused modules(拉取缺少的模块，移除不用的模块)  vendor make vendored copy of dependencies(将依赖复制到vendor下)  verify verify dependencies have expected content (验证依赖是否正确）  why explain why packages or modules are needed(解释为什么需要依赖)





### init

使用go mod 管理项目，就不需要非得把项目放到GOPATH指定目录下，你可以在你磁盘的任何位置新建一个项目，比如：E:\gitCompany\goEchoPractice> （注意，该路径并不在GOPATH里），

使用 go.mod:

```
E:\gitCompany\goEchoPractice>go mod init goEchoPractice
go: creating new go.mod: module goEchoPractice
```

init goEchoPractice， init 后面的名称可以称之为 声明现在这个包的名字，可以随意写，不一定要和你的文件夹相同。

会在当前目录下生成一个 go.mod 文件.

在里新建一个 go源码文件： main.go:

```go
package main

import (
	"net/http"

	"github.com/labstack/echo"
)

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})
	e.Logger.Fatal(e.Start(":1323"))
}
```

运行 go build main.go:

```
go: downloading github.com/labstack/echo v3.3.10+incompatible
go: extracting github.com/labstack/echo v3.3.10+incompatible
go: finding golang.org/x/crypto latest
....
```

它会自己去下载最新的包，go命令(‘go build’, ‘go test’, ‘go get’, 'go run'甚至 ‘go list’)执行时，会自己去修改go.mod文件。

**go modules 下载的包在 `GOPATH/pkg/`**



### go.mod

go.mod中记录了依赖包及其版本号。 默认的go.mod:

```
module goEchoPractice

go 1.13
```

首行为当前的模块名称，接下来是 go 的使用版本。



go.mod 提供了`module`, `require`、`replace`和`exclude` 四个命令

- `module` 语句指定包的名字（路径）
- `require` 语句指定的依赖项模块
- `replace` 语句可以替换依赖项模块
- `exclude` 语句可以忽略依赖项模块



go module 安装 package 的原則是先拉最新的 release tag，若无tag则拉最新的commit，go 会自动生成一个 go.sum 文件来记录 dependency tree.

使用 replace  替换无法直接获取的 package
由于某些已知的原因，并不是所有的package都能成功下载，比如：`golang.org`下的包。
modules 可以通过在 go.mod 文件中使用 replace 指令替换成github上对应的库，比如：

```
replace (
	golang.org/x/crypto v0.0.0-20190313024323-a1f597ede03a => github.com/golang/crypto v0.0.0-20190313024323-a1f597ede03a
)

或：
replace golang.org/x/crypto v0.0.0-20190313024323-a1f597ede03a => github.com/golang/crypto v0.0.0-20190313024323-a1f597ede03a
```



### GO111MODULE

如果想更好的控制，可以修改 `GO111MODULE` 临时环境变量。

`GO111MODULE` 有三个值：`off`, `on`和`auto（默认值）`。

- `GO111MODULE=off`，go命令行将不会支持module功能，寻找依赖包的方式将会沿用旧版本那种通过vendor目录或者GOPATH模式来查找。

- `GO111MODULE=on`，go命令行会使用modules，而一点也不会去GOPATH目录下查找。

- `GO111MODULE=auto`

  ，默认值，go命令行将会根据当前目录来决定是否启用module功能，如果当前目录不在$GOPATH **并且** 当前目录（或者父目录）下有go.mod文件，则使用 `GO111MODULE`， 否则仍旧使用 GOPATH mode。


> 当modules 功能启用时，依赖包的存放位置变更为`$GOPATH/pkg`，允许同一个package多个版本并存，且多个项目可以共享缓存的 module。



### go get

当然我们平常都不会直接先写代码，写上引入的依赖名称和路径，然后在 build 的时候再下载。

**如果要想先下载依赖，那么可以直接像以前那样 `go get` 即可**

运行 go get -u 将会升级到最新的次要版本或者修订版本

运行 go get -u=patch 将会升级到最新的修订版本

运行 go get package@version 将会升级到指定的版本号version， 

* 可以跟语义化版本号，比如 `go get foo@v1.2.3`
* 也可以跟 git 的分支或 tag, 如`go get foo@master`
* 也可以跟 git 提交哈希,如 `go get foo@e3702bed2`

**如果使用 `go get foo@master`，下次在下载只会和第一次的一样，无论 master 分支是否更新了代码**

运行go get如果有版本的更改，那么go.mod文件也会更改

**如果下载所有依赖可以使用 `go mod download` 命令。**



### go list

查看依赖包：

```sh
$ go list -m all
github.com/adesight/test
golang.org/x/crypto v0.0.0-20190313024323-a1f597ede03a
golang.org/x/sys v0.0.0-20190215142949-d0b11bdaac8a
golang.org/x/text v0.3.0
rsc.io/quote v1.5.2
rsc.io/sampler v1.99.99
$ go list -m -json all # json 格式输出
{
        "Path": "golang.org/x/text",
        "Version": "v0.3.0",
        "Time": "2017-12-14T13:08:43Z",
        "Indirect": true,
        "Dir": "/Users/lishude/go/pkg/mod/golang.org/x/text@v0.3.0",
        "GoMod": "/Users/lishude/go/pkg/mod/cache/download/golang.org/x/text/@v/v0.3.0.mod"
}
{
        "Path": "rsc.io/quote",
        "Version": "v1.5.2",
        "Time": "2018-02-14T15:44:20Z",
        "Dir": "/Users/lishude/go/pkg/mod/rsc.io/quote@v1.5.2",
        "GoMod": "/Users/lishude/go/pkg/mod/cache/download/rsc.io/quote/@v/v1.5.2.mod"
}
```





### 移除包

当前代码中不需要了某些包，删除相关代码片段后并没有在 `go.mod` 文件中自动移出。

运行下面命令可以移出所有代码中不需要的包：

```text
go mod tidy
```

如果仅仅修改 `go.mod` 配置文件的内容，那么可以运行 `go mod edit --droprequire=path`，比如要移出 `golang.org/x/crypto` 包

```text
go mod edit --droprequire=golang.org/x/crypto
```