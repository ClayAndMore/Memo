---
title: "20-使用git中的一些问题.md"
date: 2019-09-09 17:53:13 +0800
lastmod: 2020-04-03 19:50:52 +0800
draft: false
tags: [""]
categories: ["git"]
author: "Claymore"

---



### 一些问题

#### warning: LF will be replaced by CRLF

如果你是 Windows 程序员，且正在开发仅运行在 Windows 上的项目，可以设置 false 取消此功能，把回车保留在版本库中：

```sh
#提交检出均不转换
$ git config --global core.autocrlf false
```

 **你也可以在文件提交时进行safecrlf检查**

```sh
#拒绝提交包含混合换行符的文件
git config --global core.safecrlf true   

#允许提交包含混合换行符的文件
git config --global core.safecrlf false   

#提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```

https://www.jianshu.com/p/450cd21b36a4



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



#### Connection timed out

```
git config --local -e
```

change entry of

```
 url = git@github.com:username/repo.git
```

to

```
url = https://github.com/username/repo.git
```

失败的原因似乎是有时候会被防火墙禁掉，而因为443是HTTPS的端口，不会被飞掉，所以在进行如上设置后，我们就可以强制与Github的连接都通过HTTPS。



### 注意

文件名在使用中文名时容易提交不上。





## 升级git

rpm 源 :  http://opensource.wandisco.com/centos/ 

eg: ` wget http://opensource.wandisco.com/centos/6/git/x86_64/wandisco-git-release-6-1.noarch.rpm && rpm -ivh wandisco-git-release-6-1.noarch.rpm `



`yum install git -y`

验证：

```
git --version
git version 2.14.1
```

