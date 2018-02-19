## Go

Go 语言又称Golang, 是谷歌开发的一种 **静态类型， 编译型、并发型 具有垃圾回收** 的编程语言。





### 开始

* 安装，去官网下载对应平台的安装包：https://golang.org/

* 创建目录： `tar -C /usr/local -xzf go1.9.2.linux-amd64.tar.gz`

* 环境变量： `vi ~/.bashrc` 

  添加`export PATH=$PATH:/usr/local/go/bin`

  执行`source ~/.bashrc` 使环境变量生效

* 查看： `go version`



代码路径： 

GO寻找依赖包时会根据`$GOPATH` 来寻找， `$GOPATH` 的目录约定有三个子目录：

* src存放源代码
* pkg存放编译后的生成文件
* bin存放编译后的可执行文件。 

编辑`~/.bashrc`  添加 ： `export GOPATH=/home/go`   执行`source ~/.bashrc`,

`go env` ,  就能看到刚才配置的GOPATH路径了。





