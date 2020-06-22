---
title: "Android_Studio项目迁移到Eclipse.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["unity"]
author: "Claymore"

---
tags: [unity] date: 2016-06-30


1. studio中app->src->main->java 改名为src，也就是eclipse中的src.
2. 然后将main里面的内容（不包括main）拷贝到一个新的以你项目名称命名的文件夹中
3. 然后用eclipse导入就可以了

<!-- more -->

---
一般来讲一个项目如果没有什么新系统的特征，直接转换成eclipse的目录结构然后eclipse import进去就ok了，但是现在很多项目往往使用了Material Design中的一些东西，比如ToolBar，RecyclerView以及appcompat的主题等，这种依赖关系就比较复杂。

---

如生成apk的时候有 Installation error: INSTALL_FAILED_VERSION_DOWNGRADE等错误 ，提高 AndroidManifest.xml中的manifest的android:versionCode的版本 ，一般原本是1，提到到二即可