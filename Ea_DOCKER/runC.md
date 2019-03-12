### 由来

过去几年内，linux 增加了 Cgroups,Namespace, Seccomp 等一些功能， Docker 严重依赖这些特性。

实际上容器技术是一系列晦涩难懂的 系统特性集合， 因此， Docker 公司将这些底层的技术合并在一起，开源出一个项目runC.

实际上， runC 是由 Docker 公司 libcontainer 项目发展而来的， 托管于OCI组织。



#### OCI 组织

Linux 基金会在2015年6月份成立了 OCI (open Container Initiative), ps: Initiative(倡议),  

**旨在围绕容器格式定义和运行时配置定制一个开放的工业化标准。**

`github: https://github.com/opencontainers/`



runC 是一个轻量级的容器运行引擎，包括所有Docker 使用和容器相关的系统调用代码。

可以这样立即，runC 的目标就是构造到处可以运行的标准容器。

单的说，OCI有两个规范:

* 一个是容器运行时规范`runtime-spec`
* 一个是镜像格式规范`image-spec`。

一个镜像，简单来说就是一个打包好的符合OCI规范的`filesystem bundule`。

而bundile的话，包含一个配置文件`config.json`和一个rootfs目录。



### OCI 标准包（bundle）

一个标准的容器运行时需要文件系统， 也就是镜像。

OCI 是怎样定义一个基本的容器运行包的呢？

这个容器标准包的定义仅仅考虑如何把容器和它的配置数据存储到磁盘上以便运行时读取。

一般包含两个模块：

* config.json 包括容器的配置数据，这个文件必须在容器的root文件系统内。

* 一个文件夹，代表容器的root文件系统。

  这个文件夹的名字理论上是可以随意的，但是按照一般命名规则，叫 rootfs 比较合适。

  当然这个文件夹内必须包含上面提到的config.json.



#### config.json

```json
ociVersion  // OCI 容器版本号
"root":{    // 配置容器的root文件系统
    "path": "rootfs",  // 指定root文件系统路径，可以是/开头的绝对路径，也可以是相对路径
    “readonly”: true // 如为true, root文件系统在容器内就是只读的，默认是false.
},
“mounts”:[  // 配置额外的挂载点
    {
        "destination": "/tmp",  //挂载点在容器内的目标位置，必须是绝对路径 。
        "type": "tmpfs", // 需要挂载的文件系统类型
        "source":  "tmpfs", // 设备名或文件名
        "options": [ "nosuid", "strictatime", "mode=755", "size=65536k"] //额外信息
    }，
    {
    	"destination":"/data",
    	"type": "bind",
    	"source": "/volumes/testing",
    	"options":["rbind","rw"]
    ｝
],
```

process 配置容器进程信息：

```json
"process": {
    "terminal": true, //是否需要连接一个终端到此进程，默认false
    "consoleSize": {  // 在terminal 连接时，指定控制台大小，包含下面两个属性。
        "height": 25,
        "width": 80
    },
    "user": {   //指定容器内运行进程的用户信息
        "uid": 1,
        "gid": 1,
        "additionalGids": [5, 6] //附加的 groups ID
    },
    "env": [  // 需要传递给进程的环境变量，变量格式必须是KEY=value的格式。
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "TERM=xterm"
    ],
    "cwd": "/root",  //可执行文件的工作目录，必须是绝对路径。
    "args": [   // 转递给可执行文件的参数
        "sh"
    ],
    "apparmorProfile": "acme_secure_profile",
    "selinuxLabel": "system_u:system_r:svirt_lxc_net_t:s0:c124,c675",
    "noNewPrivileges": true,
    "capabilities": {
        "bounding": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
       "permitted": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
       "inheritable": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL",
            "CAP_NET_BIND_SERVICE"
        ],
        "effective": [
            "CAP_AUDIT_WRITE",
            "CAP_KILL"
        ],
        "ambient": [
            "CAP_NET_BIND_SERVICE"
        ]
    },
    "rlimits": [     // 限制容器内执行的进程资源使用量。
        {
            "type": "RLIMIT_NOFILE",
            "hard": 1024,
            "soft": 1024
        }
    ]
}
```

 钩子 hook：

配置文件提供了钩子的特性，它可以让开发者扩展容器运行的动作， 在容器运行前后执行一些命令。

```json
"hooks": {
        "prestart": [ //容器创建后，用户没有开始前触发执行。
            		 // 在linux 上 它是在Namespace 创建成功后触发的，它能提供一个配置容器初始化环境的机会。
            {
                "path": "/usr/bin/fix-mounts",
                "args": ["fix-mounts", "arg1", "arg2"],
                "env":  [ "key1=value1"]
            },
            {
                "path": "/usr/bin/setup-network"
            }
        ],
        "poststart": [  // 在用户进程启动后执行，可以用来告诉用户进程以及启动。
            {
                "path": "/usr/bin/notify-start",
                "timeout": 5
            }
        ],
        "poststop": [  // 容器停止后执行，可以用来清理容器运行中的垃圾。
            {
                "path": "/usr/sbin/cleanup.sh",
                "args": ["cleanup.sh", "-f"]
            }
        ]
    }
```

path 是需要执行脚本的路径。 args 和 env 都是可选参数， timeout 是执行脚本的超时时间。



### todo

https://segmentfault.com/a/1190000017543294#articleHeader2

https://segmentfault.com/a/1190000016366810

https://www.jianshu.com/p/62ede45cfb2e