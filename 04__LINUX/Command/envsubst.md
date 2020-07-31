---
title: "linux envsubst 命令的使用"
date: 2020-07-31 17:53:13 +0800
lastmod: 2020-07-31 17:53:13 +0800
draft: false
tags: [""]
categories: ["linux"]
author: "Claymore"

---

## envsubst

linux 中替换文件中的字符可以用sed，但是对个多个文件我们可以使用ensubst  假设我们需要将某个环境变量添加到脚本中，则我们只需要制作一个模板文件，然后只需要执行一行命令即可实现替换



### 安装

有些发行版没有自带

安装：

```
 Debian     apt-get install gettext-base
 Ubuntu     apt-get install gettext-base
 Alpine     apk add gettext
 Arch Linux pacman -S gettext
 Kali Linux apt-get install gettext-base
 CentOS     yum install gettext
 Fedora     dnf install gettext
 OS X       brew install gettext
 Raspbian   apt-get install gettext-base
 Docker     docker run cmd.cat/envsubst envsubst
```



### 使用

使用方法：
`envsubst < original_file > destination_file`

eg:

``` sh
# a.template 模板文件
vars:
  address-groups:
    HOME_NET: "${S_HOME_NET}"
# 执行 export S_HOME_NET=172.19.19.0/24
envsubst < a.template > a.yaml

# 此时生成新 a.yaml:
vars:
  address-groups:
    HOME_NET: "172.19.19.0/24"
```

这个工具可以替换掉`${}`包裹的环境变量





### 只替换需要替换的特定变量

上面的例子如果多加一个变量HOME_NET:

``` sh
vars:
  address-groups:
    HOME_NET: "${S_HOME_NET}"

    EXTERNAL_NET: "!$HOME_NET"
```

仍然安装上方的执行，HOME_NET也会被替换掉。

**虽然环境变量中没有HOME_NET, 会把模板中的该变量替换成空值**

所以需要声明需要替换的变量：

`envsubst '${VAR1} ${VAR3}' <infile > outfile`

例子里则是：`envsubst '${S_HOME_NET}' < a.template > a.yaml`

