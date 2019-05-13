Tags:[Git]

### git log

`git log -p`   ,   -p 是 `--patch` 的缩写，通过 `-p` 参数，你可以看到具体每个 `commit` 的改动细节

`git log --stat`,  查看简要统计，只想大致看一下改动内容，但并不想深入每一行的细节

`git log --graph`命令可以看到分支合并图。

`git log`   查看历史版本，如果嫌输出信息太多可以试试加上`--pretty=oneline`参数

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



### 一些问题

#### windows更改文件权限

查看：`git  ls-files --stage`

```bash
AT@DESKTOP-4FSTEEM MINGW64 (add_apicloud2)
$ git  ls-files --stage bin/api*
100644 8aae9d44084b31a11e8000e395e680c24da3db2e 0       bin/apicloud2
100755 b18a4f5a8031d3b5f513c91f8c34a536a46a2d63 0       bin/apiup

AT@DESKTOP-4FSTEEM MINGW64 (add_apicloud2)
$ git update-index --chmod=+x bin/apicloud2

AT@DESKTOP-4FSTEEM MINGW64  (add_apicloud2)
$ git  ls-files --stage bin/api*
100755 8aae9d44084b31a11e8000e395e680c24da3db2e 0       bin/apicloud2
100755 b18a4f5a8031d3b5f513c91f8c34a536a46a2d63 0       bin/apiup

AT@DESKTOP-4FSTEEM MINGW64 (add_apicloud2)
$ git status
On branch add_apicloud2
Your branch is ahead of 'upstream/dev-3.7.0' by 3 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   bin/apicloud2

```

更改：

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