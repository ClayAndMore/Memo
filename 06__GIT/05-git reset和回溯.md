
---
title: "05-git reset和回溯.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Git]

### 版本回溯

`git reset --hard HEAD^`   回到上一个版本，HEAD^^回到上两个版本。。HEAD~100回到上一百个版本。

```bash
说明：在 Git 中，有两个「偏移符号」： ^ 和 ~。

^ 的用法：在 commit 的后面加一个或多个 ^ 号，可以把 commit 往回偏移，偏移的数量是 ^ 的数量。例如：master^ 表示 master 指向的 commit 之前的那个 commit； HEAD^^ 表示 HEAD 所指向的 commit 往前数两个 commit。

~ 的用法：在 commit 的后面加上 ~ 号和一个数，可以把 commit 往回偏移，偏移的数量是 ~ 号后面的数。例如：HEAD~5 表示 HEAD 指向的 commit往前数 5 个 commit。

```



Git提供了一个命令`git reflog`用来记录你的每一次命令，这样就可以回到未来。

回滚后需要强行提交：

`git add .`  

`git commit -'roll-back'`

`git push -f origin master`   加入-f参数，强制提交



### 本地撤销和版本回退

- 撤销没有add的，也就是所有本地修改。

  git checkout .  (所有)

  git checkout 文件名（具体文件）

- 撤销add 的， `git reset HEAD filename` ,  回到上面的状态。

  如果新建的文件，已add，删掉的话用`git rm -f filename`

- 只撤销上次的commit ,并没有push:

  `	git reset --hard HEAD^`

- 更改已经提交过的注释 :`git commit --amend`, 也可用于代码写错再次提交时使用。

- 撤销MERGING状态： `git reset --hard HEAD`



本地git操作版本回退

git reflog 可以看到本地的git操作

`git reset --hard Obfafd`

后面为操作记录id

然后可以强制推至远程分支`git push -f`



### reset 的本质

实质上，`reset` 这个指令虽然可以用来撤销 `commit` ，但它的实质行为并不是撤销，而是移动 `HEAD`，并且「捎带」上 `HEAD` 所指向的 `branch`（如果有的话）。它是用来重置 `HEAD` 以及它所指向的 `branch` 的位置的。



`reset --hard HEAD^` 之所以起到了撤销 `commit` 的效果，是因为它把 `HEAD` 和它所指向的 `branch` 一起移动到了当前 `commit` 的父 `commit` 上，从而起到了「撤销」的效果

Git 的历史只能往回看，不能向未来看，所以把 `HEAD` 和 `branch` 往回移动，就能起到撤回 `commit` 的效果。

所以同理，`reset --hard` 不仅可以撤销提交，还可以用来把 `HEAD` 和 `branch` 移动到其他的任何地方。

```
git reset --hard branch2
```



`reset` 指令可以重置 `HEAD` 和 `branch` 的位置，不过在重置它们的同时，对工作目录可以选择不同的操作，而对工作目录的操作的不同，就是通过 `reset` 后面跟的参数来确定的。

暂存区：即staged的。

#### --hard

`--hard` 会在重置 `HEAD` 和 `branch` 的同时，重置工作目录里的内容。

你的工作目录里的内容会被完全重置为和 `HEAD` 的新位置相同的内容。换句话说，就是你的未提交的修改会被全部擦掉。当然已commit 的也会消失。



#### —soft

`reset --soft` 会在重置 `HEAD` 和 `branch` 时，保留工作目录和暂存区中的内容，并把重置 `HEAD`所带来的新的差异放进暂存区。



#### --mixed

`reset` 如果不加参数，那么默认使用 `--mixed` 参数。它的行为是：保留工作目录，并且清空暂存区。也就是说，工作目录的修改、暂存区的内容以及由 `reset` 所导致的新的文件差异，都会被放进工作目录。简而言之，就是「把所有差异都混合（mixed）放在工作目录中」。

工作目录的内容和 `--soft` 一样会被保留，但和 `--soft` 的区别在于，它会把暂存区清空。



### checkout 的本质

`checkout` 并不止可以切换 `branch`。`checkout` 本质上的功能其实是：签出（ checkout ）指定的 `commit`。

`git checkout branch名` 的本质，其实是把 `HEAD` 指向指定的 `branch`，然后签出这个 `branch` 所对应的 `commit` 的工作目录。所以同样的，`checkout` 的目标也可以不是 `branch`，而直接指定某个 `commit`：

```
git checkout HEAD^^
git checkout master~5
git checkout 78a4bc
git checkout 78a4bc^
```

这些都是可以的。



所以可以用 `checkout -- 文件名` 的格式，通过「签出」的方式来撤销指定文件的修改。

它和reset的不同：

checkout是带着 head 走，reset 是带着 head 和 branch 走.


