Tag: [Go]

### 包管理工具go get

类似于python 的pip， 可以获得远程包并管理包目录。

go语言有一个获取远程包的工具就是`go get`，目前go get支持多数开源社区(例如：github、googlecode、bitbucket、Launchpad), eg:

```
go get github.com/astaxie/beedb
```

参数介绍：

- `-d` 只下载不安装
- `-f` 只有在你包含了`-u`参数的时候才有效，不让`-u`去验证import中的每一个都已经获取了，这对于本地fork的包特别有用
- `-fix` 在获取源码之后先运行fix，然后再去做其他的事情
- `-t` 同时也下载需要为运行测试所需要的包
- `-u` 强制使用网络去更新包和它的依赖包,自动获取该包依赖的其他第三方包
- `-v` 显示执行的命令



通过这个命令可以获取相应的源码，对应的开源平台采用不同的源码控制工具，例如github采用git、googlecode采用hg，

**注意**：所以要想获取这些源码，必须先安装相应的源码控制工具,并同时把这些命令加入你的PATH中

通过上面获取的代码在我们本地的源码相应的代码结构如下

```
$GOPATH
  src
   |--github.com
		  |-astaxie
			  |-beedb
   pkg
	|--相应平台
		 |-github.com
			   |--astaxie
					|beedb.a
```

go get本质上可以理解为首先第一步是通过源码工具clone代码到src下面，然后执行`go install`

在代码中如何使用远程包，很简单的就是和使用本地包一样，只要在开头import相应的路径就可以

```
import "github.com/astaxie/beedb"
```



#### 设置代理

```
export http_proxy='http://name:password@x.x.x.x:xx' export https_proxy=$http_proxy
```

其他绕墙方式：https://tianshimanbu.com/basic/go-get-timeout.html





#### golang.org/x/net

go get 墙的问题,因为国内对google的政策， 我们需要从github上clone下来，搞成go可以识别的包，我们构造目录：

```
$mkdir -p $GOPATH/src/golang.org/x/
$cd $GOPATH/src/golang.org/x/
$git clone https://github.com/golang/net.git net 
$go install net 
```

具体操作：

```
root@VM:~/go_workspace# tree -d -L 3 $GOPATH
/root/go_workspace
├── bin
└── src
    ├── gin_test
    ├── github.com
    │   ├── gin-contrib
    │   ├── gin-gonic
    │   ├── golang
    │   ├── kardianos
    │   ├── mattn
    │   ├── opencontainers
    │   └── ugorji
    └── gopkg.in
        ├── go-playground
        └── yaml.v2

14 directories

root@VM:~/go_workspace# mkdir -p $GOPATH/src/golang.org/x/
root@VM:~/go_workspace# cd $GOPATH/src/golang.org/x/
root@VM:~/go_workspace/src/golang.org/x# git clone https://github.com/golang/net.git net
...

root@VM:~/go_workspace/src/golang.org/x# go install net
root@VM:~/go_workspace/src/golang.org/x# tree -d -L 3 $GOPATH
/root/go_workspace
├── bin
└── src
    ├── gin_test
    ├── github.com
    │   ├── gin-contrib
    │   ├── gin-gonic
    │   ├── golang
    │   ├── kardianos
    │   ├── mattn
    │   ├── opencontainers
    │   └── ugorji
    ├── golang.org
    │   └── x
    └── gopkg.in
        ├── go-playground
        └── yaml.v2

16 directories

```



#### get 中仍timeout

下载gin为例：

```bash
root@VM~/go_workspace/src/golang.org/x# go get -u -v github.com/gin-gonic/gin
github.com/gin-gonic/gin (download)
github.com/gin-contrib/sse (download)
github.com/golang/protobuf (download)
github.com/ugorji/go (download)
Fetching https://gopkg.in/go-playground/validator.v8?go-get=1
Parsing meta tags from https://gopkg.in/go-playground/validator.v8?go-get=1 (status code 200)
get "gopkg.in/go-playground/validator.v8": found meta tag get.metaImport{Prefix:"gopkg.in/go-playground/validator.v8", VCS:"git", RepoRoot:"                        https://gopkg.in/go-playground/validator.v8"} at https://gopkg.in/go-playground/validator.v8?go-get=1
gopkg.in/go-playground/validator.v8 (download)
Fetching https://gopkg.in/yaml.v2?go-get=1
Parsing meta tags from https://gopkg.in/yaml.v2?go-get=1 (status code 200)
get "gopkg.in/yaml.v2": found meta tag get.metaImport{Prefix:"gopkg.in/yaml.v2", VCS:"git", RepoRoot:"https://gopkg.in/yaml.v2"} at https://                        gopkg.in/yaml.v2?go-get=1
gopkg.in/yaml.v2 (download)
github.com/mattn/go-isatty (download)
Fetching https://golang.org/x/sys/unix?go-get=1
https fetch failed: Get https://golang.org/x/sys/unix?go-get=1: dial tcp 216.239.37.1:443: i/o timeout
package golang.org/x/sys/unix: unrecognized import path "golang.org/x/sys/unix" (https fetch: Get https://golang.org/x/sys/unix?go-get=1: di                        al tcp 216.239.37.1:443: i/o timeout)

root@VM:~/go_workspace/src/golang.org/x# git clone https://github.com/golang/sys.git
Cloning into 'sys'...
remote: Enumerating objects: 190, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (124/124), done.
remote: Total 7091 (delta 125), reused 105 (delta 65), pack-reused 6901
Receiving objects: 100% (7091/7091), 5.46 MiB | 103.00 KiB/s, done.
Resolving deltas: 100% (6057/6057), done.
Checking connectivity... done.

root@VM:~/go_workspace/src/golang.org/x# go get -u -v github.com/gin-gonic/gin
github.com/gin-gonic/gin (download)
github.com/gin-contrib/sse (download)
github.com/golang/protobuf (download)
github.com/ugorji/go (download)
Fetching https://gopkg.in/go-playground/validator.v8?go-get=1
Parsing meta tags from https://gopkg.in/go-playground/validator.v8?go-get=1 (status code 200)
get "gopkg.in/go-playground/validator.v8": found meta tag get.metaImport{Prefix:"gopkg.in/go-playground/validator.v8", VCS:"git", RepoRoot:"https://gopkg.in/go-playground/validator.v8"} at https://gopkg.in/go-playground/validator.v8?go-get=1
gopkg.in/go-playground/validator.v8 (download)
Fetching https://gopkg.in/yaml.v2?go-get=1
Parsing meta tags from https://gopkg.in/yaml.v2?go-get=1 (status code 200)
get "gopkg.in/yaml.v2": found meta tag get.metaImport{Prefix:"gopkg.in/yaml.v2", VCS:"git", RepoRoot:"https://gopkg.in/yaml.v2"} at https://gopkg.in/yaml.v2?go-get=1
gopkg.in/yaml.v2 (download)
github.com/mattn/go-isatty (download)
Fetching https://golang.org/x/sys/unix?go-get=1
https fetch failed: Get https://golang.org/x/sys/unix?go-get=1: dial tcp 216.239.37.1:443: i/o timeout
golang.org/x/sys (download)
github.com/gin-contrib/sse
github.com/gin-gonic/gin/internal/json
github.com/golang/protobuf/proto
github.com/ugorji/go/codec
gopkg.in/go-playground/validator.v8
gopkg.in/yaml.v2
github.com/gin-gonic/gin/binding
github.com/gin-gonic/gin/render
golang.org/x/sys/unix
github.com/mattn/go-isatty
github.com/gin-gonic/gin
```





### 包管理 govendor

安装：`go get -u github.com/kardianos/govendor`

```shell
root@VM:~/go_workspace/src/gin_test# tree -d -L 4 $GOPATH
/root/go_workspace
└── src
    ├── gin_test
    └── github.com
        └── opencontainers
            └── runc

5 directories
root@VM~/go_workspace/src/gin_test# cd $GOPATH
root@VM:~/go_workspace# tree -d -L 4 $GOPATH
/root/go_workspace
└── src
    ├── gin_test
    └── github.com
        └── opencontainers
            └── runc

5 directories
root@VM:~/go_workspace# go get -u github.com/kardianos/govendor
root@VM:~/go_workspace# tree -d -L 4 $GOPATH
/root/go_workspace
├── bin
└── src
    ├── gin_test
    └── github.com
        ├── kardianos
        │   └── govendor
        └── opencontainers
            └── runc

# 添加到已在PATH变量中的go/bin，这样可直接运行
root@VM:~/go_workspace# ls bin
govendor
root@VM:~/go_workspace# ls /root/go/bin/
go  godoc  gofmt
root@VM:~/go_workspace# cp bin/govendor /root/go/bin/
root@VM:~/go_workspace# ls /root/go/bin/
go  godoc  gofmt  govendor

root@VMtu:~/go_workspace# govendor -version
v1.0.9
```

