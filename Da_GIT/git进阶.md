Tags:[Git] date: 2017-08-31 





![](http://ovolonhm1.bkt.clouddn.com/git%E5%B7%A5%E4%BD%9C%E6%96%B9%E5%BC%8F.png)



### origin

在clone完成之后，Git 会自动为你将此远程仓库命名为origin

origin只相当于一个别名，运行git remote –v或者查看.git/config可以看到origin的含义



### remote

查看源：`git remote -v`

增加源： `git remote add <origin/upstream> url`

重命名源： `git remote rename old_name new_name`

删掉源： `git remote remove xxx`



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

    ​

  *  删掉本地仓库的所有分支：

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

    ​




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
* 切换分支

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



### git log

`git log --graph`命令可以看到分支合并图。



### git stash

git stash将当前工作区缓存起来，这样切换到其他分支工作区的内容就不会影响，当在其他分支建立新分支时，比如修复bug，我们当前的工作并不会影响，当提交bug分支后，我们再将缓存内容提取出来。

* git stash list 当前stash 列表
* git stash apply , 然后用git stash drop 删除缓存
* git stash pop , 会同时删除缓存内容。
* 可加具体stash:` $ git stash apply stash@{0}`

如果 你在a分支缓存了 到b分支又拿回来了，一般会又冲突，我们要解决冲突. 如果是误操作，需要：

`get reset --hard HEAD`



### 解决冲突

如果有冲突会提示，你只需要找到那个文件，文件中会标记冲突的地方，用编辑器打开，然后把冲突编辑掉，重新提交就好了 。看后文问题




### 版本回溯

`git log`   查看历史版本，如果嫌输出信息太多可以试试加上`--pretty=oneline`参数：

`git reset --hard HEAD^`   回到上一个版本，HEAD^^回到上两个版本。。HEAD~100回到上一百个版本。

在Git中，用`HEAD`表示当前版本。

Git提供了一个命令`git reflog`用来记录你的每一次命令，这样就可以回到未来。

回滚后需要强行提交：

`git add .`  

`git commit -'roll-back'`

`git push -f origin master`   加入-f参数，强制提交



### 本地撤销和版本回退

* 撤销没有add的，也就是所有本地修改。

  git checkout .  (所有)

  git checkout 文件名（具体文件）

* 撤销add 的， `git reset HEAD filename` ,  回到上面的状态。

  如果新建的文件，已add，删掉的话用`git rm -f filename`


* 只撤销上次的commit ,并没有push:

  `	git reset --hard HEAD^`

* 更改已经提交过的注释 :`git commit --amend`

* 撤销MERGING状态： `git reset --hard HEAD`




本地git操作版本回退

git reflog 可以看到本地的git操作

`git reset --hard Obfafd`

后面为操作记录id

然后可以强制推至远程分支`git push -f`



### 忽略跟踪

   `$ git update-index  --assume-unchanged  /path/to/file`           #忽略跟踪
   `$ git update-index --no-assume-unchanged  /path/to/file `     #恢复跟踪

最直接的方式是编辑 `.gitignore`  将自己要忽略的文件夹或文件添加进去






### 提交请求流程

1. fork 源仓库 到自己仓库，
2. 克隆自己仓库的相关分支
3. 基于刚才的分支新建开发分支
4. 更改开发分支并`git push origin 远程分支的名`
5. 请求merge



### 出部署包流程

1. 到更改的submodel 中提交请求合并
2. 合并后克隆主仓库到目录中，先不用递归克隆。
3. 进入主仓库，到相关submodel中(比如src),`git checkout -b 分支名 origin/远程分支名` 
4. git log 看是否是之前submodel的新提交。
5. 到顶层目录，进入刚才的分支，`git diff`看是否有内容改变 
6. 如果有，add . ,commit ,push




自己分支出包测试

` git submodule foreach git checkout master`

`git submodule foreach git pull origin master`

`git status`

`git add --`

`git commit -m -`

`git push origin 自己的分支名`



### 一些问题

#### windows更改文件权限

`git update-index --chmod=+x path/to/the/file`



#### windows git status乱码

```
git config --global core.quotepath false 
```



#### 一个分支的修改同步到另一个分支

branch A（01版本），在branch A（01版本）上开了分支branch B（01版本），这个时候我修改了branch A（01->02版本），请问我如何将修改的结果带到branch B？

```
git checkout B
git merge A
```



#### 文件从 Git 仓库中移除，但任希望保留在当前工作目录中

`git rm --cached file-you-want-to-remove`



#### 查看当前git分支是基于哪个分支建立的

`git reflog --date=local | grep <branchname>`



#### github设置密钥后push仍然需要密码：

原因是当时克隆用的https的方式

如果你已经用https方式克隆了仓库，就不必删除仓库重新克隆，只需将 .git/config文件中的 
url = <https://github.com/Name/project.git> 
一行改为 
url = git@github.com:Name/project.git 
即可。

#### 

#### Changes not staged for commit ,

网上查说是没有git add .,但是我add过了，下面的命令解决了这个问题：

`git` 这里有点特殊。要先加入到 staging area 的改动才会被 `git commit` 提交。同一个文件也可以 `add` 多次。不想`add`可以：

```
git commit -m 'msg' <file>
```

或者

```
git commit -m 'msg' -a
```


增加文件又删除也容易出现这个问题，这时我们要保持status的干净，可以用`git rm` , status里有说明



#### fatal: unable to access

 `'https://github.com/VundleVim/Vundle.vim.git/'`: GnuTLS recv error (-54): Error in the pull function.

  需要取消git的代理： `git config --global --unset http.proxy`



#### Git checkout: updating paths is incompatible with switching branches

I believe this occurs when you are trying to checkout a remote branch that your local git repo is not aware of yet. Try:

```
git remote show origin
```

If the remote branch you want to checkout is under "New remote branches" and not "Tracked remote branches" then you need to fetch them first:

```
git remote update
git fetch
```

Now it should work:

```
git checkout -b local-name origin/remote-name
```



### 注意

文件名在使用中文名时容易提交不上。