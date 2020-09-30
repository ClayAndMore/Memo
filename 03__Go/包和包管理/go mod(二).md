

## Go Modules v2 及更高版本

模块在 Go 中确定了一个重要的原则，即 “[导入兼容性规则](https://research.swtch.com/vgo-import)”

> 如果旧包和新包的导入路径相同，新包必须向后兼容旧的包

根据这条原则，一个软件包新的主版本没有向后兼容以前的版本。这意味着这个软件包新的主版本必须使用和之前版本不同的模块路径。

**从 `v2` 开始，主版本号必须出现在模块路径的结尾**（在 go.mod 文件的 `module` 语句中声明）。例如，当模块 `github.com/googleapis/gax-go` 的开发者们开发完 `v2` ，他们用了新的模块路径 `github.com/googleapis/gax-go/v2` 。想要使用 `v2` 的用户必须把他们的包导入和模块要求更改为 `github.com/googleapis/gax-go/v2`



### 项目如何升级到 v2

假设你的项目已经支持 go module 了。

1. 修改 go.mod 第一行，在`module`那行最后加上`/v2`。`module github.com/mnhkahn/aaa/v2`。
2. 对于不兼容的改动（除了 v0 和 v1），都必须显示得修改 import 的路径。所以我们的引用需要改成 `import "github.com/mnhkahn/aaa/v2/config"`。在所有的地方都需要修改，包括自己的包内和调用方包。
3. 底层包的更新有个小工具可以帮助快速实现[mod](https://github.com/marwan-at-work/mod)。`GO111MODULE=on go get github.com/marwan-at-work/mod/cmd/mod` `mod upgrade`。
4. 代码提交之后需要打新 tag，v2.0.0。
5. 调用方修改引用代码，需要加`v2`，和第二步提到的一样。
6. `go get github.com/mnhkahn/aaa/v2`。



### incompatible

有时候你能在 go.mod 文件中发现不兼容的标记，`v3.2.1+incompatible`，这是因为这个依赖包没有使用 go module，并且它通过 git 打了 tag。



### 问题

####  tag 删除了重建为什么没效果

困扰了我很久的一个问题。有一个 tag v2.0.0 的代码有问题，我删除了这个 tag，新建了一个好的版本，但是`go get`依然报错，困扰了很久，一直以为是 v2 的版本号写错了。后来才发现是 go 有本地缓存，缓存在 $GOPATH/pkg/mod/cache 下面，把里面的内容清掉，重新获取即可