
---
title: "docker的导入导出.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "docker的导入导出.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


### save

```sh
#docker save --help
Usage:	docker save [OPTIONS] IMAGE [IMAGE...]
Save one or more images to a tar archive (streamed to STDOUT by default)

Options:
  -o, --output string   Write to a file, instead of STDOUT
```

eg:

`docker save -o nginx.tar nginx:latest` 
或 
`docker save > nginx.tar nginx:latest` 

其中-o和>表示输出到文件，`nginx.tar`为目标文件，`nginx:latest`是源镜像名（name:tag）



### load

```sh
#docker load --help
Usage:	docker load [OPTIONS]
Load an image from a tar archive or STDIN

Options:
  -i, --input string   Read from tar archive file, instead of STDIN
  -q, --quiet          Suppress the load output #阻止load时的输出
```

eg:

`docker load -i nginx.tar` 
或 
`docker load < nginx.tar` 
其中-i和<表示从文件输入。会成功导入镜像及相关元数据，包括tag信息



### export

```sh
#docker export --help
Usage:	docker export [OPTIONS] CONTAINER
Export a container's filesystem as a tar archive

Options:
  -o, --output string   Write to a file, instead of STDOUT
```

eg:
`docker export -o nginx-test.tar nginx-test` 
其中-o表示输出到文件，`nginx-test.tar`为目标文件，`nginx-test`是源容器名（name）



### import

```sh
#docker import --help

Usage:	docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]

Import the contents from a tarball to create a filesystem image

Options:
  -c, --change list      Apply Dockerfile instruction to the created image
  -m, --message string   Set commit message for imported image
```

eg:

`docker import nginx-test.tar nginx:imp` 
或 
`cat nginx-test.tar | docker import - nginx:imp`



### 区别

* export命令是从容器（container）中导出tar文件，而save命令则是从镜像（images）中导出

* export导出的文件再import回去时，无法保留镜像所有历史（即每一层layer信息，不熟悉的可以去看Dockerfile），不能进行回滚操作；

  而save是依据镜像来的，所以导入时可以完整保留下每一层layer信息。

  使用 docker history image 可看layer

* 所以， export命令导出的tar文件略小于save命令导出的

* 使用 export  **会把此时容器内的变化也导出**。



### 注意点

* save 和 export 导出时都**不会把挂载的目录内容也导出。**
* 可以依据具体使用场景来选择命令
  - 若是只想备份images，使用save、load即可
  - 若是在启动容器后，容器内容有变化，需要备份，则使用export、import



参考：https://blog.csdn.net/ncdx111/article/details/79878098