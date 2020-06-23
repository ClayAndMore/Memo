
---
title: "06-git基本验证和操作.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "06-git基本验证和操作.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Git] date: 2017-08-19 12:45:34

### 从本地已有项目，推送到github

#### ssh与公钥

由于本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以要在本地生成一个私钥和一个密钥。

先进入家目录看下有个.ssh文件（可能隐藏），这里就是ssh公钥放置的地方。

如果没有跳到上一步，客户端与github建立连接。

到.ssh文件看下，会有两个文件，id_rsa（私钥）和id_rsa.pub（公钥）

#### 客户端与github建立连接

先看下面的ssh与公钥。

进入家目录 cd ~，一般是c盘用户文件。

配置链接，用一个常用的邮箱（这个邮箱是你的github账号，我的是wXXXX@outlook.com）：

`$ ssh-keygen -t rsa -C "your_email@youremail.com" `

接下来让你输入key的名字和密码（记住）。如果不输入直接按回车就好，多账号时这里要输入。

- 到.ssh文件看下，会有两个文件，id_rsa和id_rsa.pub

- 将id_rsa.pub用vi（或笔记本）打开，复制其内容到github里setting-ssh keys-key中。

- 将本地数据库与远程仓库连接（验证链接）：
  
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
  
  还有可能出现`Permission denied (publickey).` 的问题，这很可能是你更改了密钥的命名或者路径，可以用ssh-add 等命令来解决，最好我们用默认的位置。

#### 初始化本地仓库，并提交内容

1. github创建一个新的空仓库

2. bash命令终端进入本地仓库，初始化本地仓库：
   
   `git init`

3. 添加全部文件，准备commit提交
   
   `git add .`

4. 将文件提交到本地仓库
   
   `git commit -m'提交说明'`

设置username和email，因为github每次commit都会记录他们。 
gitconfig−−globaluser.name"yourname" git config –global user.email “your_email@youremail.com”

`git config --global user.name "你的名字"`
`git config --global user.email "你的邮箱"`

可去.gitconfig文件看。

#### 连接到远程仓库，并将代码同步

- `git remote add origin 远程仓库地址`
  
  连接到远程仓库并为该仓库创建别名 , 别名为origin . 这个别名是自定义的，通常用origin ;仓库地址是github上的项目地址，如：
  
  https://github.com/ClayAndMore/flask-blog.git

- `git push -u origin master`
  
  创建一个 upStream （上传流），并将本地代码通过这个 upStream 推送到 别名为 origin 的仓库中的 master 分支上
  
  > -u ，就是创建 upStream 上传流，如果没有这个上传流就无法将代码推送到 github；同时，这个 upStream 只需要在初次推送代码的时候创建，以后就不用创建了
  
  另外，在初次 push 代码的时候，可能会因为网络等原因导致命令行终端上的内容一直没有变化，耐心等待一会就好。
  
  可能会出现;`error: failed to push some refs to....`的问题，这是因为github中的README.md文件不在本地代码目录中，通过如下命令进行代码合并：
  
  `git pull --rebase origin master`

#### 后期继续提交

- git add .

- git commit -m'提交说明'

- git pull # 如果有团队合作的话，先pull,再push

- git push 将代码推送到 github , 默认推送到 别名为 origin 的仓库中的 master 分支上。
  
  或`git push origin master`

- 注意事项：

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

### 问题

#### Permission denied (publickey)

* 这很可能是你更改了密钥的命名或者路径，可以用ssh-add 等命令来解决，最好我们用默认的位置。

* ssh-agent
  
  * 开启
    
    ```shell
    # start the ssh-agent in the background
    eval $(ssh-agent -s)
    Agent pid 59566
    ```
  
  * 列表
    
    ```
    ssh-add -l
    ```
  
  * 添加
    
    `ssh add ~/.ssh/id_rsa`

* 目录权限
  
  ```
    sudo chmod 700 ~/.ssh/
    sudo chmod 600 ~/.ssh/*
    sudo chown -R User ~/.ssh/
    sudo chgrp -R User ~/.ssh/
  ```

* 万能：
  
  ```
    ssh -vT git@github.com
  ```
