
---
title: "02-git基础.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-14 15:42:19 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Git]



### Untrack 和 stage

文件的状态从 "untracked"（未跟踪）变成了 "staged"（已暂存），意思是这个文件中被改动的部分（也就是这整个文件啦）被记录进了 staging area（暂存区）。

> 解释一下 "stage" 这个词，这个词对我们中国人可能有一些理解难度。按我们英语课本上的内容来看，stage 是一个名词，它的意思是「舞台」。
>
> 可是不论从词性还是词义，「舞台」都不太能解释 "stage" 或 "staging area" 的意思。
>
> 实质上，Git 中的 stage 取自这个词的另一个意思：组织和准备某个事件。
>
> 而 "staging area" 的意思也并不是「舞台区域」，而是「用来汇集物品或材料以备使用的区域」的意思。
>
> 所以 stage 这个词在 Git 里，是「集中收集改动以待提交」的意思；而 staging area ，就是一个「汇集待提交的文件改动的地方」。简称「暂存」和「暂存区」。至于 staged 表示「已暂存」，就不用再解释了吧？

所谓的 staging area，是 `.git` 目录下一个叫做 `index` 的文件（嗯，它的文件名并不叫 `stage`）。你通过 `add` 指令暂存的内容，都会被写进这个文件里。



### 引用和HEAD

本质： HEAD：当前 commit 的引用

上一段里说到，图中括号里是指向这个 `commit` 的引用。其中这个括号里的 `HEAD` 是引用中最特殊的一个：它是**指向当前 commit 的引用**。它具有唯一性，每个仓库中只有一个 `HEAD`

所谓**当前 `commit`**这个概念很简单，它指的就是当前工作目录所对应的 `commit`。

当使用 `checkout`、`reset` 等指令手动指定改变当前 `commit` 的时候，`HEAD` 也会一起跟过去。

总之，当前 `commit` 在哪里，`HEAD` 就在哪里，这是一个永远自动指向当前 `commit` 的引用，所以你永远可以用 `HEAD` 来操作当前 `commit`。在每次提交时它都会自动向前移动到最新的 `commit` 。



### branch

`branch` 是一类引用。`HEAD` 除了直接指向 `commit`，也可以通过指向某个 `branch` 来间接指向 `commit`。

当 `HEAD` 指向一个 `branch` 时，`commit` 发生时，`HEAD` 会带着它所指向的 `branch` 一起移动。

branch有树枝的意思，但是不要进入两个误区，

1. 以前认为分支是单条线性的，读了才发现，branch 包含了从初始 commit 到它的所有路径，而不是一条路径。即包含树根到树枝，而不是树分叉的地方到树枝。
2. 由于 Git 中的 branch 只是一个引用，所以删除 branch 的操作也只会删掉这个引用，并不会删除任何的 commit。（不过如果没有任何一个 branch 可以回溯到这条 commit（游离 commit），那么在一定时间后，它会被 Git 的回收机制删除掉。



### push 的本质

1. `push` 是把当前的分支上传到远程仓库，并把这个 `branch` 的路径上的所有 `commit`s 也一并上传。
2. `push` 的时候，如果当前分支是一个本地创建的分支，需要指定远程仓库名和分支名，用 `git push origin branch_name` 的格式，而不能只用 `git push`
3. `push` 的时候之后上传当前分支，并不会上传 `HEAD`；远程仓库的 `HEAD` 是永远指向默认分支（即 `master`）的。

4. 获取远程代码修改后,想要push到远端与原来不同的新分支，可以使用下面的命令实现：
   `git push origin 本地分支:远端希望创建的分支`



### pull 的本质

git fetch + git merge

#### fetch

`git pull` 的「两步走」中的第一步——`git fetch` 下载远端仓库内容时，这两个镜像本地引用得到了更新，也就是本地的`origin/master` 和 `origin/HEAD` 移动到了它们最新的 `commit`。

`git fetch origin master`



#### merge

git pull 的 第二步：  `git merge origin/HEAD`

`merge` 的含义：从两个 `commit`「分叉」的位置起，把目标 `commit` 的内容应用到当前 `commit`（`HEAD` 所指向的 `commit`），并生成一个新的 `commit`；

两种特殊情况：

* 如果 `merge` 时的目标 `commit` 和 `HEAD` 处的 `commit` 并不存在分叉，而是 `HEAD` 领先于目标 `commit`：

  那么 `merge` 就没必要再创建一个新的 `commit` 来进行合并操作，因为并没有什么需要合并的。在这种情况下， Git 什么也不会做，`merge` 是一个空操作。

* 如果 `HEAD` 和目标 `commit` 依然是不存在分叉，但 `HEAD` 不是领先于目标 `commit`，而是落后于目标 `commit`：

  那么 Git 会直接把 `HEAD`（以及它所指向的 `branch`，如果有的话）移动到目标 `commit`

  这种操作有一个专有称谓，**叫做 "fast-forward"（快速前移)**



第二种情况非常常见， 比如你在开发master, 其他同事也在开发，并比你先提交了代码，你需要把你的HEAD移到最新的commit.

 

另：merge后会保留目标branch的历史commit，而且会与当前branch的commits一起根据时间排序



### git pull --rebase

git pull = git fetch + git merge
git pull --rebase = git fetch + git rebase

使用场景如下图：

``` 
A  <--+  B  <---+  C <---+ D
                    \
                      E
```

Origin 上有三次提交， 在C的时候我们切出来一个分支做了修改，并提交，此时是E, 而在提交之前，其他人也提交过，此时分支状态是D，（其实就是上文中的fast-forward状态），如果这个时候E提交到origin会有冲突， 此时有两种解决办法：

1. 用git pull命令把"origin"分支上的修改pull下来与本地提交合并（merge）成版本M，但这样会形成图中的菱形，让人很困惑。

   ``` 
   A  <--+  B  <---+  C <---+ D
                       \        \
                         E <----- M 
   ```

2. git rebase ，创建一个新的提交R，R的文件内容和上面M的一样，但我们将E提交废除

   ``` 
   A  <--+  B  <---+  C <---+ D
                               \
                                 R
   ```

   在rebase的过程中，有时也会有conflict，这时Git会停止rebase并让用户去解决冲突，解决完冲突后，**用git add命令去更新这些内容，然后不用执行git-commit,直接执行git rebase --continue,这样git会继续apply余下的补丁。**
   在任何时候，**都可以用git rebase --abort参数来终止rebase的行动**，并分支会回到rebase开始前的状态。



### Feture Branching 工作流

 Feature Branching 这种工作流。它的概念很简单：

1. 每个新功能都新建一个 `branch` 来写；
2. 写完以后，把代码分享给同事看；写的过程中，也可以分享给同事讨论。另外，借助 GitHub 等服务提供方的 Pull Request 功能，可以让代码分享变得更加方便；
3. 分支确定可以合并后，把分支合并到 `master` ，并删除分支。



 提交requset请求流程

1. fork 源仓库 到自己仓库，
2. 克隆自己仓库的相关分支
3. 基于刚才的分支新建开发分支
4. 更改开发分支并`git push origin 远程分支的名`
5. 请求merge