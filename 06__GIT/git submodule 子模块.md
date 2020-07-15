## submodoule

工作上会遇到**在一个Git仓库 中添加 其他 Git 仓库的场景**

使用 Git 的 `git submodule` 命令为一个 `git 项目` 添加 `子git项目`。



### 创建子模块

已知有两个项目 MainProject 和 SubProject

``` sh
git clone https://github.com/xxx/MainProject.git
cd MainProject/
# 在MainProject中添加SubProject
git submodule add https://github.com/xxx/SubProject.git # SubProjectDirName
```

当然后面添加目录名可以指定要添加的目录。

此时`.gitmodules`:

```
[submodule "SubProject"]
	path = SubProjectDirName
	url = https://github.com/xxx/SubProject.git
```

**.gitmodules文件**：保存项目 URL 与已经拉取的本地目录之间的映射，有多个子模块则含有多条记录，会随着版本控制一起被拉去和推送的。

最后别忘记add添加,

``` sh
git add SubProject
git commit -m""
git push 
```



### 更新子模块

进入子模块目录更新，和正常使用git 更新操作一样

``` sh
cd SubProject/
git fetch
git merge origin/master
```



### 删除子模块

使用 git rm --cached liba 将liba 从版本控制中删除（本地仍保留有），若不需要可不带 --cached进行完全删除。
使用 vim .gitmodules 可打开vim编辑,删除对应的内容:

``` sh
 [submodule "liba"]
          path = liba
          url = https://github.com/imtianx/liba.git
          branch = dev
```

使用 vim .git/config 可打开vim编辑,删除对应的内容

```
[submodule "liba"]
         url = https://github.com/imtianx/liba.git
         active = true
```

使用 rm -rf .git/modules/liba, 删除.git下的缓存模块，最后提交项目。





### 克隆带子模块的版本库

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



### 使用 git submodoule foreach

foreach 可以作用于当下所有子模块

```sh
$ ls
build/  dyanalysis/  dist/  src/
do_build.sh*  MAKETAG      prepare.sh*   

# 所有子模块fetch centos7-py3分支
$ git submodule foreach git fetch origin centos7-py3
Entering 'build'
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
From ssh://git.pta.center:10022/888/888-build-3.6.5
 * branch              centos7-py3 -> FETCH_HEAD
   2cf5fa13..549a735f  centos7-py3 -> origin/centos7-py3
Entering 'dist'
remote: Enumerating objects: 14, done.
remote: Counting objects: 100% (14/14), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 14 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (14/14), done.
From ssh://git.pta.center:10022/888/888_dist_3.6.5
 * branch                centos7-py3 -> FETCH_HEAD
   bbd0a0d3a..07d152bf2  centos7-py3 -> origin/centos7-py3
Entering 'dyanalysis'
From ssh://git.pta.center:10022/888/dynamic_analysis
 * branch            centos7-py3 -> FETCH_HEAD
 * [new branch]      centos7-py3 -> origin/centos7-py3
Entering 'src'
remote: Enumerating objects: 13, done.
remote: Counting objects: 100% (13/13), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 13 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (13/13), done.
From ssh://git.pta.center:10022/888/888_3.6.5
 * branch            centos7-py3 -> FETCH_HEAD
   82c66ca..5191cfc  centos7-py3 -> origin/centos7-py3

# 上面可以看到有四个子模块fetch了最新状态
# 所有子模块checkout 
$ git submodule foreach git checkout origin/centos7-py3
Entering 'build'
Previous HEAD position was f4033c50... Merge branch 'release3618' into 'release-3.6.18'
HEAD is now at 549a735f...  编译到bin2/bin3
Entering 'dist'
Checking out files: 100% (17863/17863), done.
Previous HEAD position was 1e1243175... Merge branch 'fix-3618bug' into 'release-3.6.18'
HEAD is now at 07d152bf2... 增加了/bin/bin3, bin/bin2, 更改了mongo 的 data 和 log的存放
Entering 'dyanalysis'
Previous HEAD position was 885139e... Merge branch 'dev-3.7.0' into 'release-3.6.18'
HEAD is now at b6c74d5... Merge branch 'dev-370' into 'dev-3.7.0'
Entering 'src'
Previous HEAD position was 5edd54b... Merge branch '3618' into 'release-3.6.18'
HEAD is now at 5191cfc... 改目录，python3的bin移动到python3/bin
```





