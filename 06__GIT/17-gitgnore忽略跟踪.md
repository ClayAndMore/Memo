

---
title: "git ignore 忽略跟踪.md"
date: 2020-08-12 19:01:02 +0800
lastmod: 2020-08-15 09:12:32 +0800
draft: false
tags: [""]
categories: ["git"]
author: "Claymore"

---



## 忽略跟踪



### 使用 update-index

   `$ git update-index  --assume-unchanged  /path/to/file`           #忽略跟踪
   `$ git update-index --no-assume-unchanged  /path/to/file `     #恢复跟踪



### .gitignore

最直接的方式是编辑 `.gitignore`  将自己要忽略的文件夹或文件添加进去

https://git-scm.com/docs/gitignore

**刚添加的.gitignore 不会马上被识别，我们需要清理一下cached:**

要停止跟踪文件,您需要将其从索引中删除.这可以通过此命令实现.

`git rm --cached <file>`

如果要删除整个文件夹,则需要以递归方式删除其中的所有文件.

`git rm -r --cached <folder>`

警告：虽然这不会从本地删除物理文件,但它会在下一个git pull中删除其他开发人员计算机上的文件.

或者直接清掉所有：

`git rm -r --cached . `



### 只忽略文件，不忽略文件夹

``` sh
*.user     # ignore all paths ending in '.user'
!*.user/   # but don't ignore these paths if they are directories.
```

ps: 如忽略项目上生成的二进制文件，如go项目编译后生成的 aaa, 在gitignore中添加aaa,

但是我们vendor中有名为aaa的文件夹，所以这个aaa的文件夹也被忽略了，所以我们gitignore中可以这样写：

``` sh
./aaa
```

