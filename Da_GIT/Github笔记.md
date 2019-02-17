
Tags:[Git] date: 2016-08-19

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

