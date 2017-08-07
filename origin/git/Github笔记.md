---
title: Github笔记
date: 2016-08-19 12:45:34
categories:
tags: github
---

### 基本概述

先进入到流行的开源项目bootstrap为例
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/github1.png)
  从上往下看：
  地址栏是一个叫twbs的用户（组织）下的bootstrap项目

* **pull requests**: 拉请求，最初用来请求别人复查已经完成的工作，并将它符合到主分支。现在常用于一个流程的早期阶段，可以讨论可能的功能。

* **issues**：提出问题，可用来讨论功能，跟踪缺陷。

* **fork** 分叉，有时候不具备直接改变一个项目的许可，也许这是一个你不知道的人写的开源代码，如果想对这样一个项目提交修改，首先要在github上你的账户下复制这个项目，这个过程称为分叉存储库，然后可以克隆，修改，并使用拉请求将其提交回最初的项目。

* 有6139人一直关注这个库，期望每次有新的变化得到通知。94204人将其标上星号，表示这是他们最喜欢的项目之一。40597曾经分叉过这个库文件，在github上制作自己的副本，并通过github上传对项目的修改及与他人分享这些修改。

* **commit** 提交，无论何时你将一个或多个文件修改保存到git的历史纪录，都会创建一个新的提交，

* **branch**分支，存放在一侧的独立的系列提交，开一个用它来进行一个实验或者创建一个新的提交。

* **master commit** 创建一个新项目的时候，都会有一个默认的主分支，一旦准备发布，工作则完全停止。

* 这个项目有11729次提交，正在开发的有22个分支，36个版本已经供人使用，672人为其编码，做了贡献。

* 我们正在查看的是主分支，位于根目录bootstrap下，最近提交到主分支的是cvrebert两天前Port#19628 to ....

    ---

* README.md文件
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/gitReadme.png)
  如果在项目根目录下有个README.md的文件，该文件提供项目说明和其他额外信息，如如何安装软件，如何运行自动化测试等。

* 查看提交历史
  点击上面的11729commits，会看到别人的提交历史，及许多修改信息，原因等。
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/commits.jpg)
  查看拉请求，和查看问题也一样

* **通过一个分叉做出贡献**
  进入https://github.com/pragmaticlearning/github-example，点击fork，如果你是任何组织的成员，会看到你所参与的有组织的列表已经你的名字，会询问你在哪里进行分叉存储库，如果不是组织中的一员，你将被带入新项目页面。
  点击new file 可创建新的项目文件
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/newfile.png)

* **创建一个拉请求**
  在上图第二个标签页pull requests
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/pullRequest.png)
  可看到这是一个在pragmaticlearning/github和ClaymoreWY/github之间的请求，将一个分支的更改信息合并到另一分支的请求，你希望合并的修改所在的分支在右边，你希望合并的目标分支在左边。


### 从本地已有项目，推送到github

#### 客户端与github建立连接

先看下面的ssh与公钥。

进入家目录 cd ~

配置链接，用一个常用的邮箱：

`$ ssh-keygen -t rsa -C "your_email@youremail.com" `

接下来让你输入什么的 一直回车就好

- 到.ssh文件看下，会有两个文件，id_rsa和id_rsa.pub
- 将id_rsa.pub用vi打开，复制其内容到github里setting-ssh keys-key中。

#### ssh与公钥

* 先进入家目录看下有个.ssh文件（可能隐藏）,如果有，先删掉。如果没有跳到客户端与github建立连接。

* 新建.ssh文件：

  `mkdir .ssh`

* 到.ssh文件看下，会有两个文件，id_rsa和id_rsa.pub

* 将id_rsa.pub用vi打开，复制其内容到github里setting-ssh keys-key中。

* 由于本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以要在本地生成一个私钥和一个密钥,输入：

* `$ ssh-keygen -t rsa -C "youxiang@aliyun.com"`

  后面不用设置密码，直接一路回车。

* 将本地数据库与远程仓库连接：

  `ssh -T git@github.com`

  会可能出现：

  `ssh: connect to host github.com port 22: Connection timed out`

  解决方法：

  在存放公钥私钥(id_rsa和id_rsa.pub)的文件里，新建config文本，内容如下：

  ```
  Host github.com
  User YourEmail@163.com
  Hostname ssh.github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa
  Port 443123456123456
  ```

  其中User为登录github的账号名称。 
  再次执行`ssh -T git@github.com`时，会出现提示，回车”yes”即可。 

  ​



#### 初始化本地仓库，并提交内容

1. github创建一个新的空仓库

2. bash命令终端进入本地仓库，初始化本地仓库：

   `git init`

3. 添加全部文件，准备commit提交

   `git add .`

4. 将文件提交到本地仓库

   `git commit -m'提交说明'`

#### 连接到远程仓库，并将代码同步

* `git remote add origin 远程仓库地址`

  连接到远程仓库并为该仓库创建别名 , 别名为origin . 这个别名是自定义的，通常用origin ;仓库地址是github上的项目地址，如：

  https://github.com/ClayAndMore/flask-blog.git

* `git push -u origin master`

  创建一个 upStream （上传流），并将本地代码通过这个 upStream 推送到 别名为 origin 的仓库中的 master 分支上

  > -u ，就是创建 upStream 上传流，如果没有这个上传流就无法将代码推送到 github；同时，这个 upStream 只需要在初次推送代码的时候创建，以后就不用创建了

  另外，在初次 push 代码的时候，可能会因为网络等原因导致命令行终端上的内容一直没有变化，耐心等待一会就好。

  可能会出现;`error: failed to push some refs to....`的问题，这是因为github中的README.md文件不在本地代码目录中，通过如下命令进行代码合并：

  `git pull --rebase origin master`

#### 后期继续提交

* git add .

* git commit -m'提交说明'

* git pull # 如果有团队合作的话，先pull,再push

* git push 将代码推送到 github , 默认推送到 别名为 origin 的仓库中的 master 分支上。

  或`git push origin master`

* 注意事项：

```
如果有多个远程仓库 或者 多个分支， 并且需要将代码推送到指定仓库的指定分支上，那么在 pull 或者 push 的时候，就需要 按照下面的格式书写：
git pull 仓库别名 仓库分支名
git push 仓库别名 仓库分支名
```





### 从linux上传项目到github

本地安装git，有github账号是前提。
（1）先在github创建一个空的仓库，并复制链接地址。使用https，以.git结尾的那个地址。
（2）初始化本地仓库，并提交内容到本地
　　要先打开命令行终端，然后通过cd命令切换到需要添加到github的项目的目录下，然后依次执行如下命令，具体命令及其含义如下：
　　touch README.md　　--创建说明文档
　　git init　　--初始化本地仓库
　　git add .　　--添加当前命令下全部已经修改的文件，准备commit 提交，该命令效果等同于git add -A
　　git commit -m '提交说明'　　--将修改后的文件提交到本地仓库，如：git commit -m '增加README.md说明文档'
　　git remote add origin 远程仓库地址　　--远程仓库地址，就是你自己新建的那个仓库的地址
　　git push -u origin master　　--创建一个上传流，并将本地代码通过这个流推送到别名为origin的仓库中的master分支上
等待一段时间，需要输入密码，即你的github登录密码。第一次上传需要一段时间。
至此，本地项目已经上传到了github上。以后对于代码的修改提交，只需要进行下面几个操作：
　　git add .　　--添加全部修改的代码，准备提交
　　git commit -m ’提交说明’　　--将修改后的代码先提交到本地仓库
　　git pull　　--如果是多人协作开发，一定要先pull，将 github 最新的代码拉取到本地，避免冲突
　　git push　　--将代码推送到 github , 默认推送到 别名为 origin 的仓库中的 master 分支上。