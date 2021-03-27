### 环境准备

**选择一个aws的服务器，这对编译和下载非常友好，不用配置各种源和代理，非常丝滑** 

我在aws付费了一个按需计费（每小时大约5毛钱的的 Debian GNU/Linux 10）

下载git 和 make 以及 rsync.

``` sh
apt update
apt install git make rsync
```

选择一个合适的分支clone, github 地址： https://github.com/kubernetes/kubernetes/tree/master

` git clone -b release-1.20 https://github.com/kubernetes/kubernetes.git` 

最好是在linux下载，而不是在window下载再传入linux,这样的话，一些连接文件，makefile文件会失效，比如makefile的tab不是能是4个空格的问题。



配置go环境，k8s的编译对go的版本有要求，可以看源码中的go mod 文件来下载相应的go 版本

```sh

curl -O -L https://golang.org/dl/go1.16.2.linux-amd64.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    75  100    75    0     0    480      0 --:--:-- --:--:-- --:--:--   480
100  123M  100  123M    0     0  63.9M      0  0:00:01  0:00:01 --:--:-- 85.0M
 
ls
go1.16.2.linux-amd64.tar.gz

tar -C /usr/local -xzf go1.16.2.linux-amd64.tar.gz

vim ~/.bashrc # 配置 export PATH=$PATH:/usr/local/go/bin

go version
go version go1.16.2 linux/amd64

```



### 编译 apiserver

``` sh
# make kube-apiserver
+++ [0323 02:45:43] Building go targets for linux/amd64:
    ./vendor/k8s.io/code-generator/cmd/prerelease-lifecycle-gen
find: ‘rsync’: No such file or directory
find: ‘rsync’: No such file or directory
./hack/run-in-gopath.sh: line 34: _output/bin/prerelease-lifecycle-gen: Permission denied
make[1]: *** [Makefile.generated_files:148: gen_prerelease_lifecycle] Error 1
make: *** [Makefile:546: generated_files] Error 2
```

这里我们需要额外执行一步：

`chmod a+x  _output/bin/prerelease-lifecycle-gen`

再次编译：

``` sh
# make kube-apiserver
+++ [0323 02:49:22] Building go targets for linux/amd64:
    ./vendor/k8s.io/code-generator/cmd/deepcopy-gen
+++ [0323 02:49:30] Building go targets for linux/amd64:
    ./vendor/k8s.io/code-generator/cmd/defaulter-gen
+++ [0323 02:49:40] Building go targets for linux/amd64:
    ./vendor/k8s.io/code-generator/cmd/conversion-gen
+++ [0323 02:49:59] Building go targets for linux/amd64:
    ./vendor/k8s.io/kube-openapi/cmd/openapi-gen
+++ [0323 02:50:13] Building go targets for linux/amd64:
    ./vendor/github.com/go-bindata/go-bindata/go-bindata
+++ [0323 02:50:15] Building go targets for linux/amd64:
    cmd/kube-apiserver

ls _output/bin/
conversion-gen  deepcopy-gen  defaulter-gen  go-bindata  go2make  kube-apiserver  openapi-gen  prerelease-lifecycle-gen
```

此时的apiserver 就可以用了



### 在windows 上调试

相应代码下载到windows平台, 将代码导入到 goland ide, 最好放到 gopath/src/k8s.io下 执行 go mod vendor，把一些包下好

然后尝试编译： ·go build -mod=vendor cmd/kube-apiserver/apiserver.go`

``` sh
E:\gitCompany\src\k8s.io\kubernetes>go build -mod=vendor cmd/kube-apiserver/apiserver.go
# k8s.io/kubernetes/cmd/kube-apiserver/app
cmd\kube-apiserver\app\server.go:448:70: undefined: "k8s.io/kubernetes/pkg/generated/openapi".GetOpenAPIDefinitions
```

我们把liinux编译好的 zz_generated.openapi.go 放到  kubernetes\pkg\generated\openapi\zz_generated.openapi.go。

``` sh
find ./ -name zz_generated.openapi.go
./pkg/generated/openapi/zz_generated.openapi.go # 拿这个
./staging/src/k8s.io/apiextensions-apiserver/pkg/generated/openapi/zz_generated.openapi.go
./staging/src/k8s.io/kube-aggregator/pkg/generated/openapi/zz_generated.openapi.go
./staging/src/k8s.io/sample-apiserver/pkg/generated/openapi/zz_generated.openapi.go
./staging/src/k8s.io/code-generator/_examples/apiserver/openapi/zz_generated.openapi.go
```

在次编译，成功后运行

``` sh
E:\gitCompany\src\k8s.io\kubernetes>apiserver.exe
W0323 11:34:37.892381   11496 services.go:37] No CIDR for service cluster IPs specified. Default value which was 10.0.0.0/24 is deprecated and will be removed in future releases. Please specify it using --service-cluster-ip-range on kube-apiserver.

I0323 11:34:37.918312   11496 server.go:629] external host was not specified, using 10.61.72.206
W0323 11:34:37.919310   11496 authentication.go:507] AnonymousAuth is not allowed with the AlwaysAllow authorizer. Resetting AnonymousAuth to false. You should use a different authorizer
Error: [--etcd-servers must be specified, service-account-issuer is a required flag, --service-account-signing-key-file and --service-account-issuer are required flags]
```

这里提示我们要连接etcd

下载 etcd windwos， https://github.com/etcd-io/etcd/releases， 运行 etcd.exe，默认监听2379端口。



1.20版本的k8s需要连接的东西很多，不只etcd

``` sh
s>apiserver.exe --etcd-servers=http://127.0.0.1:2379 --service-account-issuer=https://kubernetes.default.svc.cluster.local
W0323 14:02:56.078236   36776 services.go:37] No CIDR for service cluster IPs specified. Default value which was 10.0.0.0/24 is deprecated and will be removed in future releases. Please specify it using --service-cluster-ip-range on kube-apiserver.

I0323 14:02:56.104168   36776 server.go:629] external host was not specified, using 10.61.72.206
W0323 14:02:56.104168   36776 authentication.go:507] AnonymousAuth is not allowed with the AlwaysAllow authorizer. Resetting AnonymousAuth to false. You should use a different authorizer
Error: --service-account-signing-key-file, --service-account-issuer, and --api-audiences should be specified together

```



### 1.18 版本

由于1.20 需要连接的东西很多，我们换成1.18的

``` 
>apiserver.exe  --etcd-servers=http://127.0.0.1:2379
```

接下来就可以调试了



参考： 

https://www.daimajiaoliu.com/daima/4edeaa21e900400