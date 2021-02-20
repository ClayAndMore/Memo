---
title: "hugo.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## hugo

```
原意：
- 英: [ˈhju:ɡəu] 
- n.雨果；Victor Mavie Hugo 维克多雨果
- 网络雨果的秘密；雨果奖；雨果的冒险
```



https://gohugo.io/getting-started/quick-start/



参数说明：

https://www.gohugo.org/doc/commands/hugo/



一些科普：

### Sass

Sass 的终极目标是解决 CSS 的缺陷。如我们所知，CSS 并不是一个完美的语言。CSS 虽然简单易学，却也能迅速制造严重的混淆，尤其是在工程浩大的项目中。

这就是 Sass 出现的契机，作为一种元语言，通过提供额外的功能和工具可以改善 CSS 的语法。同时，保留了 CSS 的原有特性。

**Sass 存在的关键不是将 CSS 变成一种全功能编程语言，它只是想修复缺陷。**正因如此，学习 Sass 如同学习 CSS 一样简单：它只在 CSS 的基础上添加了几个[额外功能](http://sitepoint.com/sass-reference/)。

参考：https://sass-guidelin.es/zh/





### 安装

### mac

brew install hugo

hugo version



## 使用

创建一个项目：

hugo new site quickstart

添加一个主题：

```
cd quickstart
git init
git submodule add https://github.com/alex-shpak/hugo-book themes/book
cp -R themes/book/exampleSite/content .
hugo server --minify --theme book
```

去 https://themes.gohugo.io/ 里选一个主题。



### 启动

```
使用方法:  
hugo [command] [flags] 
节选的 command: 
new         为你的站点创建新的内容  
server      一个高性能的web服务器 

节选的 flags:  
-D, --buildDrafts                包括被标记为draft的文章  
-E, --buildExpired               包括已过期的文章  
-F, --buildFuture                包括将在未来发布的文章 

举几个栗子:  
hugo -D                          生成静态文件并包括draft为true的文章  
hugo new post/new-content.md     新建一篇文章  
hugo new site mysite             新建一个称为mysite的站点  
hugo server --buildExpired       启动服务器并包括已过期的文章
```

*PS: hugo server 会自动监听你的原始文稿，你在编辑原始`.md`文件时的变化都会实时的反映在网站上。如果你不希望启用这个功能你可以使用`hugo server --watch=false`命令。*

**使用 Hugo 命令本身 直接生成 public 下的内容，不包含草稿，不用加参数 -D**



### 目录结构

new site 后会得到一个包含以下文件的目录：

```
.
├── archetypes
├── config.toml
├── content
├── data
├── layouts
├── static
└── themes
```

- **archetypes**: 储存`.md`的模板文件，类似于`hexo`的`scaffolds`，该文件夹的优先级高于主题下的`/archetypes`文件夹

  ```markdown
  ---
  title: "{{ replace .Name "-" " " | title }}"
  date: {{ .Date }}
  draft: true
  ---
  ```

  

- **config.toml**: 配置文件

- **content**: 储存网站的所有内容，类似于`hexo`的`source`

- **data**: 储存数据文件供模板调用，类似于`hexo`的`source/_data`

- **layouts**: 储存`.html`模板，该文件夹的优先级高于主题下的`/layouts`文件夹

- **static**: 储存图片,css,js等静态文件，该目录下的文件会直接拷贝到`/public`，该文件夹的优先级高于主题下的`/static`文件夹

- **themes**: 储存主题

- **public**: 执行`hugo`命令后，储存生成的静态文件



### Netlify

本身是个具备 CI/CD 功能的 CDN 网站托管平台，同类还有 [`ZEIT Now`](https://zeit.co/)

来源：https://www.bmpi.dev/dev/guide-to-setup-blog-site-with-zero-cost-1/

https://app.netlify.com/



### 使用问题

跳转某些文章404， 查看它的URL，看下public 下的post名是否和其对上，有时候在post下生成的文件夹名为大写的时候会有这样的问题，一般是如下原因造成的：

* 包含了空文件
* 包含了非md文件