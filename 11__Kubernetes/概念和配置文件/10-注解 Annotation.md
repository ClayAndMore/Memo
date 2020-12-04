## Annotaion 注解

Annotation，顾名思义，就是注解。Annotation可以将Kubernetes资源对象关联到任意的非标识性元数据。

在元数据标签时有个例子：

``` yaml
metadata:       #必选，元数据
  name: string       #必选，Pod名称
  namespace: string    #必选，Pod所属的命名空间
  labels:      #自定义标签
    - name: string     #自定义标签名字
  annotations:       #自定义注释列表
    - name: string
```

Annotation与Label类似，也使用key/value键值对的形式进行定义。不同的Label具有严格的命名规则，它定义的是Kubernetes对象的元数据（Metadata），并且用于Label Selector。而Annotation则是用户任意定义的“附加”信息，以便于外部工具进行查找，很多时候，Kubernetes的模块自身会通过Annotation的方式标记资源对象的特殊信息。

Label和Annotation都可以将元数据关联到Kubernetes资源对象。Label主要用于选择对象，可以挑选出满足特定条件的对象。相比之下，annotation 不能用于标识及选择对象。annotation中的元数据可多可少，可以是结构化的或非结构化的，也可以包含label中不允许出现的字符。annotation和label一样都是key/value键值对映射结构

通常来说，用Annotation来记录的信息如下。

- build信息、release信息、Docker镜像信息等，例如时间戳、release id号、PR号、镜像hash值、docker registry地址等。
- 日志库、监控库、分析库等资源库的地址信息。
- 程序调试工具信息，例如工具、版本号等。
- 团队等联系信息，例如电话号码、负责人名称、网址等

相关命令：kubectl annotate -h