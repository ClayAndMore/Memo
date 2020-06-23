---
title: "08-git log & relog.md"
date: 2017-09-09 17:53:13 +0800
lastmod: 2020-04-03 19:50:52 +0800
draft: false
tags: [""]
categories: ["git"]
author: "Claymore"

---


### git log

`git log -p`   ,   -p 是 `--patch` 的缩写，通过 `-p` 参数，你可以看到具体每个 `commit` 的改动细节

`git log --stat`,  查看简要统计，只想大致看一下改动内容，但并不想深入每一行的细节

`git log --graph`命令可以看到分支合并图。

`git log`   查看历史版本，如果嫌输出信息太多可以试试加上`--pretty=oneline`参数

`git log --pretty="format:%ci" filename`   修改时间记录

其他：

- `git  blame [file] `   

  显示指定文件是什么人在什么时间修改过

- 显示某个文件的版本历史，包括文件改名

  `$ git log --follow [file]`
  `$ git whatchanged [file]`



### git show 和 diff

1. 查看具体某个commit：

   ```
   show
   ```

   1. 要看最新 `commit` ，直接输入 `git show` ；要看指定 `commit` ，输入 `git show commit的引用或SHA-1`
   2. 如果还要指定文件，在 `git show` 的最后加上文件名

2. 查看未提交的内容：

   ```
   diff
   ```

   1. 查看暂存区和上一条 `commit` 的区别：`git diff --staged`（或 `--cached`）
   2. 查看工作目录和暂存区的区别：`git diff` 不加选项参数
   3. 查看工作目录和上一条 `commit` 的区别：`git diff HEAD`







### relog

`reflog` 是 "reference log" 的缩写，使用它可以查看 Git 仓库中的引用的移动记录。如果不指定引用，它会显示 `HEAD` 的移动记录。

#### 找回删除的branch

假如你误删了 `branch1` 这个 `branch`，那么你可以查看一下 `HEAD` 的移动历史：

```bash
660aa81 (HEAD -> master) HEAD{0}: checkout: moving from branch1 to master
c08de9a HEAD@{1}: checkout:moving from master to branch1
660aa81 (HEAD -> master) HEAD{2}: checkout: moving from branch1 to master
c08de9a HEAD@{3}: reset: moving to HEAD
```

从中可以看出，`HEAD` 的最后一次移动行为是「从 `branch1` 移动到 `master`」。而在这之后，`branch1` 就被删除了。所以它之前的那个 `commit` 就是 `branch1` 被删除之前的位置了，也就是第二行的 `c08de9a`。

所以现在就可以切换回 `c08de9a`，然后重新创建 `branch1` ：

```
git checkout c08de9a
git checkout -b branch1
```

这样，你刚删除的 `branch1` 就找回来了。

> 注意：不再被引用直接或间接指向的 `commit`s 会在一定时间后被 Git 回收，所以使用 `reflog` 来找回删除的 `branch` 的操作一定要及时，不然有可能会由于 `commit` 被回收而再也找不回来。



#### 查看其他引用的 reflog

`reflog` 默认查看 `HEAD` 的移动历史，除此之外，也可以手动加上名称来查看其他引用的移动历史，例如某个 `branch`：

```
git reflog master
```



