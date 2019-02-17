Tags:[Git]

## git 进阶2



###  some details

* `git  blame [file] `   

  显示指定文件是什么人在什么时间修改过

* 显示某个文件的版本历史，包括文件改名

  `$ git log --follow [file]`
  `$ git whatchanged [file]`

* `git status`  查看当前仓库状态

* `git diff`    可看我们哪里对什么做了修改

  ​

  ​

### git rebase

git rebase 也是分支的合并，它会把本地修改接到最新的后面，而不像merge那样在历史记录里看上去是平行的。



### 标签管理

版本确定了，要发版了就为某次提交打个tag, 它和commit的区别是它是不可更改的，

为什么有了commit还要tag，因为让管理更便捷，不能说是去取某个id为6e3dadf的commit，直接说tag就好了。

其实tag就是commit的一个指针，它是一个容易让人记住的名字，跟某个commit捆绑在一起。



#### 标签操作

* 创建标签

  * 切到某个分支：

    `git tag <tag_name>`

  * 如果对以前的提交打标签：

    `git tag <tag_name> <commit_id>`

    eg: `$ git tag v0.9 6224937`

  * 还可以创建带有说明的标签，用`-a`指定标签名，`-m`指定说明文字：

    ```
    $ git tag -a v0.1 -m "version 0.1 released" 3628164
    ```

  * 还可以用GPG来加密某次git 标签，防止被在传输过程中被篡改。

  注： 创建的标签只会存在本地，不会推送到远程。

* 查看所有标签

  `git tag`

* 查看标签信息

  `git show v0.9`

* 删除标签

  删除本地

  `git tag -d <tag_name>`1

  删除远程：

  先删除本地，再删除远程：

  `git push origin :refs/tags/<tagname>`

* 推送tag标签

  `git  push origin tag_name`

  ​


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





### linux 下的配置

#### 终端显示git 当前所在分支

vi .bashrc:

```bash
function git_branch {
  branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
  if [ "${branch}" != "" ];then
      if [ "${branch}" = "(no branch)" ];then
          branch="(`git rev-parse --short HEAD`...)"
      fi
      echo " ($branch)"
  fi
}

export PS1='\u@\h \[\033[01;36m\]\W\[\033[01;32m\]$(git_branch)\[\033[00m\] \$ '
```

添加到文件中。

`source ./.bashrc`



#### linux git自动补全

`https://github.com/git/git/blob/master/contrib/completion/git-completion.bash `

将上方git官网库中的bash脚本放到~.bashrc 同级， 在~.bashrc中加入：

`source ~/git-completion.bash`



一个插件： yum install bash-completion  



#### git的命令行的颜色配置

```
git config --global color.status auto 
git config --global color.diff auto 
git config --global color.branch auto 
git config --global color.interactive auto
```

