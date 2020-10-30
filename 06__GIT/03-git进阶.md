---
title: "03-git进阶.md"
date: 2017-08-31 17:53:13 +0800
lastmod: 2019-10-11 14:17:56 +0800
draft: false
tags: [""]
categories: ["git"]
author: "Claymore"

---


![](https://cdn.jsdelivr.net/gh/ClayAndMore/image/git/git_work_mode.png)



### origin

在clone完成之后，Git 会自动为你将此远程仓库命名为origin

origin只相当于一个别名，运行git remote –v或者查看.git/config可以看到origin的含义



### remote

查看源：`git remote -v`

增加源： `git remote add <origin/upstream> url`

重命名源： `git remote rename old_name new_name`

删掉源： `git remote remove xxx`

修改源地址： `git remote set-url origin new_url`

eg: git 库迁移，附带提交记录：

``` sh
# 如果有未提交的，先commit 
git commit -m "change repo."
# 删除原来的git源
git remote remove origin
# 将新源地址写入
git remote add origin [new url]
# 提交所有代码
git push -u origin master
```





### clone

`git clone url [文件夹名]`

只克隆某个分支：

`git clone -b opencv-2.4 --single-branch https://github.com/Itseez/opencv.git`

克隆部分文件，稀疏克隆：

``` sh
# 如果本地还没有建版本库，要用这个功能，先进入要放版本库的目录，在命令行执行几条命令：
$ git init <project>
$ cd <project>
$ git remote add origin ssh://<user>@<repository's url>
$ git config core.sparsecheckout true # 打开sparse checkout功能。
# 加路径到checkout的列表。路径是版本库下的相对路径
$ echo "path1/" >> .git/info/sparse-checkout
$ echo "path2/www/app" >> .git/info/sparse-checkout
$ git pull origin master
```

如果只拉取最近一次的变更，忽略以前的变更记录，在拉取时可以加参数depth，

如`git pull --depth=1 origin master` （浅克隆）



#### sparse-checkout

子目录的匹配
在 sparse-checkout 文件中，如果目录名称前带斜杠，如`/docs/`，将只匹配项目根目录下的docs目录，如果目录名称前不带斜杠，如`docs/`，其他目录下如果也有这个名称的目录，如`test/docs/`也能被匹配。
而如果写了多级目录，如`docs/05/`，则不管前面是否带有斜杠，都只匹配项目根目录下的目录，如`test/docs/05/`不能被匹配。

通配符 “*“ (星号)
在 sparse-checkout 文件中，支持通配符 “*“，如可以写成以下格式：

```
*docs/
index.*
*.gif
```



排除项 “!” (感叹号)
在 sparse-checkout 文件中，也支持排除项 “!”，如只想排除排除项目下的 “docs” 目录，可以按如下格式写：

```
/*
!/docs/
```



要注意一点：如果要关闭sparsecheckout功能，全取整个项目库，可以写一个”*“号，但如果有排除项，必须写”/*“，同时排除项要写在通配符后面。




### branch

* 查看分支

  `git branch`  查看当前本分支和地分支

  `git branch -r ` 查看远程分支

  `git branch -a ` 查看所有分支


* 建立分支

  `git branch 分支名`

  `git checkout -b branch2_based_on_b1 branch1 `  基于该分支创建子分支

* 切换分支

  `git checkout branchname`

  `git checkout -b branchname`    //创建并切换到分支branchname

* 克隆分支

  ` git clone -b <branch name> [remote repository address] "filename"`

  -b 代表克隆分支，filename为你已经存在的文件夹名，或者不存在它会自己创立。

* 推送和拉取分支

  `git push origin a:b`          本地a分支推送到远程分支b

  `git checkout -b b origin/a`    检出远程的分支a到本地b

* 删除分支

  `git branch -d branchname `   删除本地分支

  `git branch -r -d origin/branch-name`    删除远程分支

  `git push <remote_name> --delete <branch_name>`  也是删除远程分支

* 重命名分支

  `git brach -m oldname newname`

* 批量删分支

  * 删掉本地除master之外的所有分支：

    ```bash
    AT@DESKTOP-4FSTEEM MINGW64 /f/git_company/wy_ng8wbuild_master (master)
    $ git branch | grep -v master
      add_bin_pypy_devWY
      release-3.6.17-送检
      wy_dev_build
      wy_release-3.6.16
    
    AT@DESKTOP-4FSTEEM MINGW64 /f/git_company/wy_ng8wbuild_master (master)
    $ git branch | grep -v master | xargs git branch -D
    Deleted branch add_bin_pypy_devWY (was 56bd947).
    Deleted branch release-3.6.17-送检 (was 98bc3d4).
    Deleted branch wy_dev_build (was 1910c98).
    Deleted branch wy_release-3.6.16 (was 98bc3d4).
    
    ```

  * 删掉本地仓库的所有分支：

    ```bash
    AT@DESKTOP-4FSTEEM MINGW64 /f/git_company/wy_ng8w_dist_master (master)
    $ git branch -a | grep origin
      remotes/origin/add_tag_info
      remotes/origin/add_user_email_com
      remotes/origin/add_users_email_com
      remotes/origin/del_audit_cron
      remotes/origin/master
      remotes/origin/modify_api_run
      remotes/origin/repair_web_security
    
    $ git branch -a | grep origin |grep -v "master"
      remotes/origin/add_tag_info
      remotes/origin/add_user_email_com
      remotes/origin/add_users_email_com
      remotes/origin/del_audit_cron
      remotes/origin/modify_api_run
      remotes/origin/repair_web_security
      
      # 切掉remotes
     $ git branch -a | grep origin |grep -v "master" | cut -d / -f 2-3 
       origin/add_tag_info
       origin/add_user_email_com
       origin/add_users_email_com
       origin/del_audit_cron
       origin/modify_api_run
       origin/repair_web_security
    
    $ git branch -a | grep origin |grep -v "master" | cut -d / -f 2-3 | xargs git branch -r -D
        Deleted remote-tracking branch origin/add_tag_info (was 3762763e).
        Deleted remote-tracking branch origin/add_user_email_com (was c7255e52).
        Deleted remote-tracking branch origin/add_users_email_com (was a3913bd8).
        Deleted remote-tracking branch origin/del_audit_cron (was 9b698d9e).
        Deleted remote-tracking branch origin/modify_api_run (was 68fbbb77).
        Deleted remote-tracking branch origin/repair_web_security (was 7650ea5e).
    
    ```





### fork

情形： 从别人的库里fork为自己的库，但是别人的库更新了，自己如何更新？

1. 首先要先确定一下是否建立了主repo的远程源：

   ```
   git remote -v
   ```

2. 如果里面只能看到你自己的两个源(fetch 和 push)，那就需要添加主repo的源：

   ```
   git remote add upstream 主源URL
   git remote -v
   ```

   然后你就能看到upstream了。

3. 如果想与主repo合并：

   ```
   git fetch upstream / 拉取了远端所有的分支到本地
   git merge upstream/分支 自己的分支
   ```

4. pull （和三步骤一样，只执行这两个中的一步）

   ```
   git pull <远程仓库名> <远程分支名>
   ```




### checkout

checkout的作用就是将本地远程代码版本替换你工作区里的版本，不论你的工作区是做了如何更改，比如删除等。

所以用它有两种所用：

* 撤销你的更改，还未提交。
* 切换分支 和 切换到某次提交

将远端代码检出到本地：

`git checkout upstream/dev-3.7.0`

此时你所在分支会变成一个未命名的分支：

```
AT@DESKTOP-4FSTEEM MINGW64 /f/git_company/upstream_dist_xxx ((dailybuild))
$ git branch
* (HEAD detached at upstream/dev-3.7.0)
  master
```

将其命名： `git checkout -b new_branch `

切换到某个提交：

git checkout 2d1e23qr..

某个文件切换到指定版本：

git checkout 2d1ed0 main.js



### fetch

从远端取回本地的操作为fetch, 比如远端库有了更新：

`git branch -r `, 查看远程分支

我们拉回到本地，就用到了 `git fetch`

默认取回所有分支的更新，如果执行取回特定的分支如：

`git fetch origin master`

取回分支后我们一般用`git checkout -b newBranch origin/master` 

基于刚才新拉取的分支新建分支。

或者用`git merge` 或`git rebase`   在本地分支上合并远程分支。



### merge

git 合并远端master分支：

```git
git checkout slef_branch
-- 保持无更改 --
git merge master

```



通常，合并分支时，如果可能，Git会用`Fast forward`模式，但这种模式下，删除分支后，会丢掉分支信息。

准备合并`dev`分支，请注意`--no-ff`参数，表示禁用`Fast forward`：

```
$ git merge --no-ff -m "merge with no-ff" dev
Merge made by the 'recursive' strategy.
 readme.txt |    1 +
 1 file changed, 1 insertion(+)

```

因为本次合并要创建一个新的commit，所以加上`-m`参数，把commit描述写进去。

和不加参数的区别：

合并后的历史有分支，能看出来曾经做过合并，而`fast forward`合并就看不出来曾经做过合并。

合并后是一次新的提交，所有-m参数。

eg:  master 的 新分支 dev， dev做了修改并commit , 得到一个commit id A，此时合并dev, git merge dev, master的分支id也是A, 这是没有加参数的时候，如果加了参数，git master会有一个新的commit ，一个新的id，

这样容易分辨merge.



**取消此次merge:**

`git merge —-abort`



**合并指定分支文件**

`git checkout source_branch <path>...`

eg:

```
$ git branch
  * A  
    B
    
$ git checkout B message.html message.css message.js other.js
```

使用与新增文件或新增修改的场景，因为这样会强制覆盖A上的文件，如果a中相关文件有修改，建议不这么做。看下面：



**智能合并**

基于A建立一个临时分支A_temp, 将B合并到A_temp

```
$ git checkout -b A_temp
Switched to a new branch 'A_temp'

$ git merge B
Updating 1f73596..04627b5
Fast-forward
 message.css                     | 0
 message.html                    | 0
 message.js                      | 0
 other.js                        | 1 +
 4 files changed, 1 insertion(+)
 create mode 100644 message.css
 create mode 100644 message.html
 create mode 100644 message.js

```

切换到A分支，并使用git checkout 将A_temp分支上新增的内容合到A:

```
$ git checkout A
Switched to branch 'A'

$ git checkout A_temp message.html message.css message.js other.js

$ git status
# On branch A
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#    new file:   message.css
#    new file:   message.html
#    new file:   message.js
#    modified:   other.js
```



### stash

git stash将当前工作区缓存起来，这样切换到其他分支工作区的内容就不会影响，当在其他分支建立新分支时，比如修复bug，我们当前的工作并不会影响，当提交bug分支后，我们再将缓存内容提取出来。

* git stash list 当前stash 列表
* git stash apply , 然后用git stash drop 删除缓存
* git stash pop , 会同时删除缓存内容。
* 可加具体stash:` $ git stash apply stash@{0}`

如果 你在a分支缓存了 到b分支又拿回来了，一般会又冲突，我们要解决冲突. 如果是误操作，需要：

`get reset --hard HEAD`



> 注意：没有被 track 的文件（即从来没有被 add 过的文件不会被 stash 起来，因为 Git 会忽略它们。如果想把这些文件也一起 stash，可以加上 `-u` 参数，它是 `--include-untracked` 的简写。就像这样：

```
git stash -u
```



### clean

git clean命令用来从你的工作目录中删除所有没有tracked过的文件

git clean经常和git reset --hard一起结合使用. 记住reset只影响被track过的文件, 所以需要clean来删除没有track过的文件. 

用法 : 

* `git clean -n`

  是一次clean的演习, 告诉你哪些文件会被删除. 记住他不会真正的删除文件, 只是一个提醒

* `git clean -f`

  删除当前目录下所有没有track过的文件. 

* git clean -f <path>

  删除指定路径下的没有被track过的文件

* git clean -df

  删除当前目录下没有被track过的文件和文件夹

* git clean -xf

  删除当前目录下所有没有track过的文件. 不管他是否是.gitignore文件里面指定的文件夹和文件


git reset --hard和git clean -f是一对好基友. 结合使用他们能让你的工作目录完全回退到最近一次commit的时候



### 解决冲突

如果有冲突会提示，你只需要找到那个文件，文件中会标记冲突的地方，用编辑器打开，然后把冲突编辑掉，重新提交就好了 。看后文问题




