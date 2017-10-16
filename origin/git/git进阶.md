date: 2017-08-31 

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

  `git checkout -b b rigin/a`    检出远程的分支a到本地b

* 删除分支

  `git branch -b branchname `   删除本地分支

  `git branch -r -d origin/branch-name`    删除远程分支

* 重命名分支

  `git brach -m oldname newname`




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

   ​

### 版本回溯

`git log`   查看历史版本，如果嫌输出信息太多可以试试加上`--pretty=oneline`参数：

`git reset --hard HEAD^`   回到上一个版本，HEAD^^回到上两个版本。。HEAD~100回到上一百个版本。

在Git中，用`HEAD`表示当前版本。

Git提供了一个命令`git reflog`用来记录你的每一次命令，这样就可以回到未来。

回滚后需要强行提交：

`git add .`  

`git commit -'roll-back'`

`git push -f origin master`   加入-f参数，强制提交





### 一些问题

* github设置密钥后push仍然需要密码：

  原因是当时克隆用的https的方式

  如果你已经用https方式克隆了仓库，就不必删除仓库重新克隆，只需将 .git/config文件中的 
  url = <https://github.com/Name/project.git> 
  一行改为 
  url = git@github.com:Name/project.git 
  即可。

* 文件名在使用中文名时容易提交不上注意。