
---
title: "11-gitbook的使用.md"
date: 2020-01-12 16:27:12 +0800
lastmod: 2020-01-12 16:27:12 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## 安装和使用

### 安装

运行下面的命令进行安装

```bash
npm install gitbook-cli -g
```

其中`gitbook-cli`是gitbook的一个命令行工具, 通过它可以在电脑上安装和管理gitbook的多个版本.

```
~/Documents/git_space sudo npm install gitbook-cli -g
Password:
/usr/local/bin/gitbook -> /usr/local/lib/node_modules/gitbook-cli/bin/gitbook.js
+ gitbook-cli@2.3.2
added 578 packages from 672 contributors in 24.321s


   ╭────────────────────────────────────────────────────────────────╮
   │                                                                │
   │       New minor version of npm available! 6.4.1 → 6.13.4       │
   │   Changelog: https://github.com/npm/cli/releases/tag/v6.13.4   │
   │               Run npm install -g npm to update!                │
   │                                                                │
   ╰────────────────────────────────────────────────────────────────╯
```

验证：

```
~/Documents/git_space gitbook -V
CLI version: 2.3.2
GitBook version: 3.2.3
```



### 初始化

```
~/Documents/git_space(master ✗) gitbook init ./gitbook_test
warn: no summary file in this book
info: create README.md
info: create SUMMARY.md
info: initialization is finished
```





### 构建

使用下面的命令，**会在项目的目录下生成一个 `_book` 目录，里面的内容为静态站点的资源文件**：

```text
$ gitbook buil
```

Eg:

```
~/Documents/git_space(master ✗) ls gitbook_test
README.md  SUMMARY.md
~/Documents/git_space(master ✗) cd gitbook_test
~/Documents/git_space/gitbook_test(master ✗) gitbook build
info: 7 plugins are installed
info: 6 explicitly listed
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 1 pages
info: found 0 asset files
info: >> generation finished with success in 1.8s !
```



### 服务

使用下列命令会运行一个服务器, 通过`http://localhost:4000/`可以预览书籍

```
~/Documents/git_space/gitbook_test(master ✗) gitbook serve
Live reload server started on port: 35729
Press CTRL+C to quit ...

info: 7 plugins are installed
info: loading plugin "livereload"... OK
info: loading plugin "highlight"... OK
info: loading plugin "search"... OK
info: loading plugin "lunr"... OK
info: loading plugin "sharing"... OK
info: loading plugin "fontsettings"... OK
info: loading plugin "theme-default"... OK
info: found 1 pages
info: found 0 asset files
info: >> generation finished with success in 0.8s !

Starting server ...
Serving book on http://localhost:4000
```

看下默认文件里的内容：

```
~/Documents/git_space/gitbook_test(master ✗) cat README.md
# Introduction

~/Documents/git_space/gitbook_test(master ✗) cat  SUMMARY.md
# Summary

* [Introduction](README.md)
```

在网页浏览下现在的gitbook：

![](http://claymore.wang:5000/uploads/big/8a2347f35d82cfe271b80a42ea844b7b.png)



### 其他命令

这里主要介绍一下 GitBook 的命令行工具 `gitbook-cli` 的一些命令, 首先说明两点:

- `gitbook-cli` 和 `gitbook` 是两个软件
- `gitbook-cli` 会将下载的 gitbook 的不同版本放到 `~/.gitbook`中, 可以通过设置`GITBOOK_DIR`环境变量来指定另外的文件夹

**列出 gitbook 所有的命令**

```text
gitbook help
```

**输出** **`gitbook-cli`** **的帮助信息**

```text
gitbook --help
```

**生成静态网页**

```text
gitbook build
```

**生成静态网页并运行服务器**

```text
gitbook serve
```

**生成时指定gitbook的版本, 本地没有会先下载**

```text
gitbook build --gitbook=2.0.1
```

**列出本地所有的gitbook版本**

```text
gitbook ls
```

**列出远程可用的gitbook版本**

```text
gitbook ls-remote
```

**安装对应的gitbook版本**

```text
gitbook fetch 标签/版本号
```

**更新到gitbook的最新版本**

```text
gitbook update
```

**卸载对应的gitbook版本**

```text
gitbook uninstall 2.0.1
```

**指定log的级别**

```text
gitbook build --log=debug
```

**输出错误信息**

```text
gitbook builid --debug
```



## 目录结构

一个基本的 GitBook 电子书结构通常如下：

```text
.
├── book.json
├── README.md
├── SUMMARY.md
├── chapter-1/
|   ├── README.md
|   └── something.md
└── chapter-2/
    ├── README.md
    └── something.md
```

`SUMMARY.md` 文件，中列出的所有 Markdown / Asciidoc 文件将被转换为 HTML。

gitbook 中特殊文件的功能：

```
book.json 配置数据
README.md 电子书的前言或者简介
SUMMARY.md 电子书目录
GLOSSARY.md 词汇/注释术语列表
```

静态文件是在 `SUMMARY.md` 中未列出的文件。除非被忽略，否则所有静态文件都将复制到输出路径。



### 子项目和子项目集成

对于软件项目，您可以使用子目录（如 `docs/` ）来存储项目文档的图书。您可以配置根选项来指示 GitBook 可以找到该图书文件的文件夹：

```text
.
├── book.json
└── docs/
    ├── README.md
    └── SUMMARY.md
```

在 `book.json` 中配置以下内容：

```text
{
    "root": "./docs"
}
```



### 忽略文件或者文件夹

GitBook将读取 `.gitignore`，`.bookignore` 和 `.ignore` 文件，以获取要过滤的文件和文件夹。这些文件中的格式遵循 `.gitignore` 的规则：

```text
# This is a comment

# Ignore the file test.md
test.md

# Ignore everything in the directory "bin"
bin/*
```





## 其他

### 插件

Gitbook默认自带有5个插件：

> highlight： 代码高亮
> search： 导航栏查询功能（不支持中文）
> sharing：右上角分享功能
> font-settings：字体设置（最上方的"A"符号）
> livereload：为GitBook实时重新加载





```json
{
    "plugins": [
        "hide-element",
        "back-to-top-button",
        "chapter-fold",
        "code",
        "splitter",
        "-lunr", "-search", "search-pro"
    ],
    "pluginsConfig": {
        "hide-element": {
            "elements": [".gitbook-link"]
        }
    }
}
```



chapter-fold: 支持多层目录，点击导航栏的标题名就可以实现折叠扩展。

splitter 侧边栏宽度可调节.

search-pro: 支持中文搜索，在使用此插件之前，需要将默认的search和lunr 插件去掉。其中"-search"中的`-`符号代表去除默认自带的插件。