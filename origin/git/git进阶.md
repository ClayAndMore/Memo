date: 2017-08-31 





![](http://ovolonhm1.bkt.clouddn.com/git%E5%B7%A5%E4%BD%9C%E6%96%B9%E5%BC%8F.png)



### origin

在clone完成之后，Git 会自动为你将此远程仓库命名为origin

origin只相当于一个别名，运行git remote –v或者查看.git/config可以看到origin的含义



### submodoule

https://www.cnblogs.com/nicksheng/p/6201711.html

#### 克隆带子模块的版本库

方法一，先clone父项目，再初始化submodule，最后更新submodule，初始化只需要做一次，之后每次只需要直接update就可以了，需要注意submodule默认是不在任何分支上的，它指向父项目存储的submodule commit id。

```
git clone project.git project2
cd project2
git submodule init
git submodule update
cd ..
```

方法二，采用递归参数`--recursive`，需要注意同样submodule默认是不在任何分支上的，它指向父项目存储的submodule commit id。

```
git clone project.git project3 --recursive
```



git submodoule foreach



### 分支

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

* 重命名分支

  `git brach -m oldname newname`




一个分支的修改同步到另一个分支

branch A（01版本），在branch A（01版本）上开了分支branch B（01版本），这个时候我修改了branch A（01->02版本），请问我如何将修改的结果带到branch B？

```
git checkout B
git merge A
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
   git fetch upstream 
   git merge upstream/分支 自己的分支
   ```

4. pull （和三步骤一样，只执行这两个中的一步）

   ```
   git pull <远程仓库名> <远程分支名>
   ```


### 解决冲突

如果有冲突会提示，你只需要找到那个文件，文件中会标记冲突的地方，用编辑器打开，然后把冲突编辑掉，重新提交就好了 。


### 版本回溯

`git log`   查看历史版本，如果嫌输出信息太多可以试试加上`--pretty=oneline`参数：

`git reset --hard HEAD^`   回到上一个版本，HEAD^^回到上两个版本。。HEAD~100回到上一百个版本。

在Git中，用`HEAD`表示当前版本。

Git提供了一个命令`git reflog`用来记录你的每一次命令，这样就可以回到未来。

回滚后需要强行提交：

`git add .`  

`git commit -'roll-back'`

`git push -f origin master`   加入-f参数，强制提交





* 撤销没有add的，也就是所有本地修改。

  git checkout .  (所有)

  git checkout 文件名（具体文件）

* 撤销add 的， `git reset HEAD filename` ,  回到上面的状态。


* 只撤销上次的commit ,并没有push:

  `git reset --hard HEAD^`

* 更改已经提交过的注释 :`git commit --amend`



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

* github设置密钥后push仍然需要密码：

  原因是当时克隆用的https的方式

  如果你已经用https方式克隆了仓库，就不必删除仓库重新克隆，只需将 .git/config文件中的 
  url = <https://github.com/Name/project.git> 
  一行改为 
  url = git@github.com:Name/project.git 
  即可。

* 文件名在使用中文名时容易提交不上注意。

* Changes not staged for commit ,网上查说是没有git add .,但是我add过了，下面的命令解决了这个问题：

  `git` 这里有点特殊。要先加入到 staging area 的改动才会被 `git commit` 提交。同一个文件也可以 `add` 多次。不想`add`可以：

  ```
  git commit -m 'msg' <file>
  ```

  或者

  ```
  git commit -m 'msg' -a
  ```

* fatal: unable to access `'https://github.com/VundleVim/Vundle.vim.git/'`: GnuTLS recv error (-54): Error in the pull function.


  需要取消git的代理： `git config --global --unset http.proxy`

  ​