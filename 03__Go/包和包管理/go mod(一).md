---
title: "go mod（一）.md"
date: 2020-01-16 18:29:52 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---
## Go mod

Golang从诞生之初就一直有个被诟病的问题：缺少一个行之有效的“官方”包依赖管理工具。其原因是在Google内部，所有人都是在一个代码库上进行开发的，因此并不是非常需要。但Golang变成一个社区化的工程语言之后，这个问题被放大了。

1. GOPATH不符合一般开发者习惯，大部分人更习惯maven、node modules之类的方式
2. GOPATH无法有效的管理版本依赖，没有一个地方能够表明依赖包的具体版本号，无法形成有效的版本配套关系

在Golang 1.5发布了vendor特性之后，社区在vendor基础上开发了很多包管理工具，例如glide, dep(这个最悲催，已经半官方了，结果横刀杀出来一个go mod)

同样的库，同样的版本，就因为在不同的工程里用了，就要在vendor里单独搞一份，不浪费吗？所以这些基于vendor的包管理工具，都会有这个问题。

相比之下maven这种本地缓存库的管理方式就好很多。

Golang 1.11 版本引入的 go mod ，其思想类似maven：摒弃vendor和GOPATH，拥抱本地库。

考虑向前兼容，目前仍然可以用go get，但最终这个命令是会消失的。



## go.mod 文件

go.mod中记录了依赖包及其版本号。 默认的go.mod:

```
module goEchoPractice

go 1.13
```

首行为当前的模块名称，接下来是 go 的使用版本。



go.mod 提供了`module`, `require`、`replace`和`exclude` 四个模块：

- `module` 语句指定包的名字, 用于定义当前项目的模块路径。
- `require` 语句指定的依赖项模块, 用于设置一个特定的模块版本。
- `replace` 语句可以替换依赖项模块, 用于将一个模块版本替换为另外一个模块版本。
- `exclude` 语句可以忽略依赖项模块, 用于从使用中排除一个特定的模块版本。

```
module example.com/foobar

go 1.13

require (
    example.com/apple v0.1.2
    example.com/banana v1.2.3
    example.com/banana/v2 v2.3.4
    example.com/pineapple v0.0.0-20190924185754-1b0db40df49a
)

exclude example.com/banana v1.2.4
replace example.com/apple v0.1.2 => example.com/rda v0.1.0 
replace example.com/banana => example.com/hugebanana
```

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



## go mod 命令

### mod init

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



### get / mod download

当然我们平常都不会直接先写代码，写上引入的依赖名称和路径，然后在 build 的时候再下载。

**如果要想先下载依赖，那么可以直接像以前那样 `go get` 即可**, 使用go module之后，go get 拉取依赖的方式就发生了变化：

- 老的`go get`取包过程类似：`git clone` + `go install` , 开启`Go Module`功能后`go get`就只有 `git clone` 或者 `download`过程了。
- 新老实现还有一个不同是，两者存包的位置不同。前者，存放在`$GOPATH/src`目录下；后者，存放在`$GOPATH/pkg/mod`目录下。
- 老的`go get`取完主包后，会对其`repo`下的`submodule`进行循环拉取。新的`go get`不再支持`submodule`子模块拉取。

运行 go get -u 将会升级到最新的次要版本或者修订版本(只改bug的版本), 更新现有的依赖

eg ：`go get -u=patch github.com/gogf/gf`

运行 go get -u=patch 将会升级到最新的修订版本

运行 go get package@version 将会升级到指定的版本号version， 

* 可以跟语义化版本号，比如 `go get foo@v1.2.3`
* 也可以跟 git 的分支或 tag, 如`go get foo@master`
* 也可以跟 git 提交哈希,如 `go get foo@e3702bed2`

**如果使用 `go get foo@master`，下次在下载只会和第一次的一样，无论 master 分支是否更新了代码,?(存疑)**

运行go get如果有版本的更改，那么go.mod文件也会更改

**如果下载所有依赖可以使用 `go mod download` 命令。**

它是下载modules到本地cache， 目前所有模块版本数据均缓存在 `$GOPATH/pkg/mod`和 `$GOPATH/pkg/sum` 下

清除 moudle 缓存： `go clean -modcache`



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

查看可下载版本：

`go list -m -versions github.com/gogf/gf`



### mod tidy 移除包

当前代码中不需要了某些包，删除相关代码片段后并没有在 `go.mod` 文件中自动移出。

运行下面命令可以移出所有代码中不需要的包：

```text
go mod tidy
```



### mod edit 

如果仅仅修改 `go.mod` 配置文件的内容，那么可以运行 `go mod edit --droprequire=path`，比如要移出 `golang.org/x/crypto` 包

```text
go mod edit --droprequire=golang.org/x/crypto
```

编辑go.mod文件 选项有`-json`、`-require`和`-exclude`，可以使用帮助go help mod edit



### mod vendor

生成vendor目录， 这个选项比较重要。

其他：

验证依赖是否正确

```text
go mod verify
```

查找依赖

```text
go mod why
```



## 环境变量



### GO111MODULE

如果想更好的控制，可以修改 `GO111MODULE` 临时环境变量。

`GO111MODULE` 有三个值：`off`, `on`和`auto（默认值）`。

- `GO111MODULE=off`，go命令行将不会支持module功能，寻找依赖包的方式将会沿用旧版本那种通过vendor目录或者GOPATH模式来查找。

- `GO111MODULE=on`，go命令行会使用modules，而一点也不会去GOPATH目录下查找。

- `GO111MODULE=auto`

  ，默认值，go命令行将会根据当前目录来决定是否启用module功能，如果当前目录不在$GOPATH **并且** 当前目录（或者父目录）下有go.mod文件，则使用 `GO111MODULE`， 否则仍旧使用 GOPATH mode。


> 当modules 功能启用时，依赖包的存放位置变更为`$GOPATH/pkg`，允许同一个package多个版本并存，且多个项目可以共享缓存的 module。



### Chache

这个主要是针对 Go modules 的全局缓存数据说明，如下：

- 同一个模块版本的数据只缓存一份，所有其他模块共享使用。
- 目前所有模块版本数据均缓存在 `$GOPATH/pkg/mod`和 `$GOPATH/pkg/sum` 下，未来或将移至 `$GOCACHE/mod`和`$GOCACHE/sum` 下( 可能会在当 `$GOPATH` 被淘汰后)。
- 可以使用 `go clean -modcache` 清理所有已缓存的模块版本数据。

另外在 Go1.11 之后 GOCACHE 已经不允许设置为 off 了，我想着这也是为了模块数据缓存移动位置做准备，因此大家应该尽快做好适配。



### 辅助环境变量

5个辅助环境变量：

#### GOPROXY

这个环境变量主要是用于设置 Go 模块代理，主要如下：

- 它的值是一个以英文逗号 “,” 分割的 Go module proxy 列表（稍后讲解）
  - 作用：用于使 Go 在后续拉取模块版本时能够脱离传统的 VCS 方式从镜像站点快速拉取。它拥有一个默认：`https://proxy.golang.org,direct`，但很可惜 `proxy.golang.org` 在中国无法访问，故而建议使用 `goproxy.cn` 作为替代，
  - **可以执行语句：`go env -w GOPROXY=https://goproxy.cn,direct`**。
  - 设置为 “off” ：禁止 Go 在后续操作中使用任 何 Go module proxy。

刚刚在上面，我们可以发现值列表中有 “direct” ，它又有什么作用呢。其实值列表中的 “direct” 为特殊指示符，用于指示 Go 回源到模块版本的源地址去抓取(比如 GitHub 等)，当值列表中上一个 Go module proxy 返回 404 或 410 错误时，Go 自动尝试列表中的下一个，遇见 “direct” 时回源，遇见 EOF 时终止并抛出类似 “invalid version: unknown revision...” 的错误。

代理网站：https://goproxy.io/

如果还是timeout, 尝试单独访问代理网站，看是否通畅。



#### GOSUMDB

它的值是一个 Go checksum database，用于使 Go 在拉取模块版本时(无论是从源站拉取还是通过 Go module proxy 拉取)保证拉取到的模块版本数据未经篡改，也可以是“off”即禁止 Go 在后续操作中校验模块版本

- 格式 1：`+`。
- 格式 2：`+ `。
- 拥有默认值：`sum.golang.org` (之所以没有按照上面的格式是因为 Go 对默认值做了特殊处理)。
- 可被 Go module proxy 代理 (详见：Proxying a Checksum Database)。
- `sum.golang.org` 在中国无法访问，故而更加建议将 GOPROXY 设置为 `goproxy.cn`，因为 `goproxy.cn` 支持代理 `sum.golang.org`。

如有 Get https://sum.golang.org  的下载错误，是因为：1.13之后设置了默认的GOSUMDB=sum.golang.org，由于墙的原因无法访问，执行以下命令关闭即可：

`go env -w GOSUMDB=off`



#### GOPRIVATE/GONOPROXY/GONOSUMDB

这三个环境变量都是用在当前项目依赖了私有模块，也就是依赖了由 GOPROXY 指定的 Go module proxy 或由 GOSUMDB 指定 Go checksum database 无法访问到的模块时的场景,可以简单的理解为跳过代理的模块。

- 它们三个的值都是一个以英文逗号 “,” 分割的模块路径前缀，匹配规则同 path.Match。
- 其中 GOPRIVATE 较为特殊，它的值将作为 GONOPROXY 和 GONOSUMDB 的默认值，**所以建议的最佳姿势是只是用 GOPRIVATE。**

在使用上来讲，比如 `GOPRIVATE=*.corp.example.com` 表示所有模块路径以 `corp.example.com` 的下一级域名 (如 `team1.corp.example.com`) 为前缀的模块版本都将不经过 Go module proxy 和 Go checksum database，**需要注意的是不包括 `corp.example.com` 本身。**



#### GOINSECURE 

在Go 1.14中增加了新的环境变量，用于指定哪些域名下的仓库不去校验CA证书。

使用方式同 GOPRIVATE 类似 `go env -w GOINSECURE=private.repo.com `

如果在Go 1.14以下 可以使用 go get -insecure

这种方式不推荐，原因如下

1. 添加 -insecure 参数即表示更新依赖时可以不去校验CA证书，但是这会带来一个问题：范围无法界定(overkill)，所有与要更新依赖相关联的依赖，均不会去做校验，可能会意外更新到不安全的依赖。

2. -insecure 仅支持 go get 命令，不支持 go mod 命令，因此使用 go mod 命令时是无法更新不支持https协议的私有库的



### 交叉编译

待补充：https://juejin.im/post/5cac9b73e51d456e8c1d3bfc#heading-8



## 坑

### 管理 GO 的环境变量

在 Go 1.13 中， 建议 将所有有关 Go 相关的环境变量都由新出的 go env -w 来管理。

比如 go env -w GO111MODULE=on 就会在 `$HOME/.config/go/env ` 文件中追加一行：

`GO111MODULE=on`

**但go env -w 不会覆盖你的系统环境变量**



### unrecognized import path "golang.org/x/tools/go/packages"

有时候设置了proxy 还是会有这样的问题，可以尝试go env -w GO111MODULE=on(笑哭)



### x509: certificate

```sh
$ go list
go: downloading git.cloud.top/go/rest v0.0.0-20190325032036-dad58215d74f
go: downloading git.cloud.top/go/utility v0.0.0-20190717063107-2c329e490c02
...
go: finding github.com/coreos/pkg v0.0.0-20180928190104-399ea9e2e55f
go: finding golang.org/x/net v0.0.0-20191002035440-2ec189313ef0
build git.cloud.top/DSec/go-server: cannot load git.cloud.top/DSec/goanchore: unrecognized import path "git.cloud.top/DSec/goanchore" (https fetch: Get https://git.cloud.top/DSec/goanchore?go-get=1: x509: certificate signed by unknown authority)

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/DSec/Docker-Images/go-server (my_back_end)
$ go get -insecure it.cloud.top/DSec/goanchore


wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/DSec/Docker-Images/go-server (my_back_end)
$ go get -insecure git.cloud.top/DSec/goanchore
go: finding git.cloud.top/DSec/goanchore latest
go: downloading git.cloud.top/DSec/goanchore v0.0.0-20200107041953-ff0fdb8096b8
go: extracting git.cloud.top/DSec/goanchore v0.0.0-20200107041953-ff0fdb8096b8
go: downloading github.com/astaxie/beego v1.12.0
go: downloading github.com/kelseyhightower/envconfig v1.4.0
go: downloading github.com/lib/pq v1.2.0
go: extracting github.com/lib/pq v1.2.0
go: extracting github.com/kelseyhightower/envconfig v1.4.0
go: extracting github.com/astaxie/beego v1.12.0
```

原因是go get的执行过程需要https证书，检查server端证书是未知CA签署的并报错。

`go get -insecure xxx`,  或者拿到证书。





参考链接： https://juejin.im/post/5d8ee2db6fb9a04e0b0d9c8b





### 更新

```
wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ go  get -insecure git.cloud.top/DSec/gaia
go: downloading git.cloud.top/DSec/gaia v0.0.0-20200223100719-3106fd0eba0c
go: downloading gopkg.in/yaml.v2 v2.2.7
go: downloading go.aporeto.io/elemental v1.100.1-0.20200131212138-0acbf2761bf0
go: downloading github.com/mitchellh/reflectwalk v1.0.0
go: extracting git.cloud.top/DSec/gaia v0.0.0-20200223100719-3106fd0eba0c
go: extracting gopkg.in/yaml.v2 v2.2.7
go: extracting github.com/mitchellh/reflectwalk v1.0.0
go: extracting go.aporeto.io/elemental v1.100.1-0.20200131212138-0acbf2761bf0
go: finding git.cloud.top/DSec/gaia v0.0.0-20200223100719-3106fd0eba0c
go: finding go.aporeto.io/elemental v1.100.1-0.20200131212138-0acbf2761bf0
go: finding github.com/mitchellh/reflectwalk v1.0.0
go: finding gopkg.in/yaml.v2 v2.2.7


```

变化：

```
wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ git status
On branch wy
Your branch is ahead of 'origin/wy' by 29 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   go.mod
        modified:   go.sum

```

变化：

```

$ git diff go.mod
 require (
+       git.cloud.top/DSec/gaia v0.0.3 // indirect


$ git diff go.sum

+git.cloud.top/DSec/gaia v0.0.3 h1:JEKaotDiQ5H7u6gwOz5nX34fAo12tA6ucoH+o5KkGGU=
+git.cloud.top/DSec/gaia v0.0.3/go.mod h1:5vfBVISmuJGAxVSSeUia4LOvK2khrYGrcKbPCimP6RM=

```



mod vendor:

```sh
$ go mod vendor
go: downloading go.aporeto.io/manipulate v1.114.1-0.20200211161817-73d840c10110
go: downloading go.aporeto.io/bahamut v1.112.1-0.20191212212221-6a099a60d19a
go: downloading github.com/smartystreets/goconvey v0.0.0-20190731233626-505e41936337
go: downloading go.uber.org/zap v1.10.0

# 卡主，尝试取消代理

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ echo $HTTP_PROXY
http://192.168.59.241:8888/

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ unset HTTP_PROXY

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ echo $HTTP_PROXY

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ echo $HTTPS_PROXY
http://192.168.59.241:8888/

wy@DESKTOP-9OB8A7N MINGW64 /e/gitCompany/apiserver (wy)
$ unset HTTPS_PROXY

再次尝试即可。
```



### 待参考

https://www.gitdig.com/go-mod-enterprise-work-1/