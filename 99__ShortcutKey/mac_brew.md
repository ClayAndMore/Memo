
---
title: "mac_brew.md"
date: 2019-09-29 19:29:06 +0800
lastmod: 2019-09-29 19:29:06 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Mac]

## home-brew

brew ， 也叫homebrew,是 Mac 下的一个包管理工具，类似于 centos 下的 yum，可以很方便地进行安装/卸载/更新各种软件包

brew 官网：<https://brew.sh/>



### 安装

官方安装方式：

`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

国内镜像源安装方式：

```
用国内的镜像安装的过程如下：
1.将安装brew的文件下载到本地

cd ~ && curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install >> brew_install
2.修改安装文件内的镜像源（BREW_REPO和CORE_TAP_REPO）
#!/System/Library/Frameworks/Ruby.framework/Versions/Current/usr/bin/ruby
# This script installs to /usr/local only. To install elsewhere you can just
# untar https://github.com/Homebrew/brew/tarball/master anywhere you like or
# change the value of HOMEBREW_PREFIX.
HOMEBREW_PREFIX = "/usr/local".freeze
HOMEBREW_REPOSITORY = "/usr/local/Homebrew".freeze
HOMEBREW_CACHE = "#{ENV["HOME"]}/Library/Caches/Homebrew".freeze
HOMEBREW_OLD_CACHE = "/Library/Caches/Homebrew".freeze
 
#BREW_REPO = "https://github.com/Homebrew/brew".freeze
BREW_REPO = "git://mirrors.ustc.edu.cn/brew.git".freeze
 
#CORE_TAP_REPO = "https://github.com/Homebrew/homebrew-core".freeze
CORE_TAP_REPO = "git://mirrors.ustc.edu.cn/homebrew-core.git".freeze
3.执行安装
/usr/bin/ruby ~/brew_install
4.添加执行路径
sudo vim /etc/profile
添加/etc/local/bin到PATH
source /etc/profile
5.验证是否安装成功
brew doctor

如果未提示command not found，则表示安装成功
```



### 使用

nodejs 为例：

```sh
# 安装，更新，卸载
brew install nodejs
brew upgrade nodejs
brew remove nodejs

rew list                    # 列出当前安装的软件
brew search nodejs          # 查询与 nodejs 相关的可用软件
brew info nodejs            # 查询 nodejs 的安装信息
brew deps  nodejs                # 显示包依赖

#brew search 查看有没有需要的版本，在 @ 后面指定版本号，例如 
brew install thrift@0.9
```



### brew services

`brew services` 是一个非常强大的工具，可以用来管理各种服务的启停，有点像 linux 里面的 services，非常方便，以 elasticsearch 为例

```shell
brew install elasticsearch          # 安装 elasticsearch
brew services start elasticsearch   # 启动 elasticsearch
brew services stop elasticsearch    # 停止 elasticsearch
brew services restart elasticsearch # 重启 elasticsearch
brew services list 					# 列出当前的状态
```

brew services 服务相关配置以及日志路径

- 配置路径：`/usr/local/etc/`
- 日志路径：`/usr/local/var/log`



### 安装位置

1、通过brew install安装应用最先是放在/usr/local/Cellar/目录下。
 2、有些应用会自动创建软链接放在/usr/bin或者/usr/sbin，同时也会将整个文件夹放在/usr/local
 3、可以使用 **brew list 软件名** (比如 brew list oclint)确定安装位置。

brew list oclint

```
/usr/local/Cellar/oclint/0.13/bin/oclint
/usr/local/Cellar/oclint/0.13/bin/oclint-0.13
/usr/local/Cellar/oclint/0.13/bin/oclint-json-compilation-database
/usr/local/Cellar/oclint/0.13/bin/oclint-xcodebuild
/usr/local/Cellar/oclint/0.13/include/c++/ (151 files)
/usr/local/Cellar/oclint/0.13/lib/clang/ (141 files)
/usr/local/Cellar/oclint/0.13/lib/oclint/ (75 files)
```

