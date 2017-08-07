---
title: hexo搭建
date: 2017-01-21 21:53:44
header-img: "postBack.jpg"
tags: hexo
---

### 前期准备

- 下载安装nodejs

- 安装git 

  尽量从这里下，https://git-for-windows.github.io/

- github账户，注意开启github page

- 创建账户同名仓库 如：username.github.io

- 何为rss

```
RSS就是一种用来分发和汇集网页内容的XML格式,
1.订阅BLOG(BLOG上，你可以订阅你工作中所需的技术文章；也可以订阅与你有共同爱好的作者的日志，总之，BLOG上你对什么感兴趣你就可以订什么) 
2.订阅新闻(无论是奇闻怪事、明星消息、体坛风云，只要你想知道的，都可以订阅) 
你再也不用一个网站一个网站，一个网页一个网页去逛了。只要这将你需要的内容订阅在一个RSS阅读器中，这些内容就会自动出现你的阅读器里，你也不必为了一个急切想知道的消息而不断的刷新网页，因为一旦有了更新，RSS阅读器就会自己通知你！ 
```

### 本地部署hexo

- 新建一个存放博客目录的文件夹，例如：blog

- 进入到blog文件夹

- 执行如下命令安装Hexo：

  `sudo npm install -g hexo`

- 初始化hexo, `hexo init ` ,博客安装完毕，这个命令需要翻墙

- `hexo s` 启动博客

- 打开浏览器 [http://127.0.0.1](http://127.0.0.1):4000/ 即可访问

### 部署到github

配置blog目录下的_config.yml文件，修改deploy参数，其中repo换成刚刚新建项目的git地址，这里用的https，也可以用git形式

```
deploy:
  type: git
  repository: http://github.com/ClayAndMore/ClayAndMore.github.io
  branch: master
```

- 在blog目录下，用gitbash执行`hexo g` `hexo d`命令即可，中途会提示输入用户名和密码
- 在浏览器中输入 [http://mousycoder.github.io](http://mousycoder.github.io) 即可看到。

### 一些命令

- 克隆主题

  `git clone https://github.com/wuchong/jacman.git themes/jacman`

  记得将文件目录下的`_config.yml`中的theme属性，将其设置为jacman。

- `hexo s` =hexo server本地启动服务预览

- `hexo g`=hexo generate 生成静态页面到public目录,可理解为编译

- `hexo d`=hexo deploy 部署到github

- `hexo new "psotname"` 新建文章，可去掉引号

- `hexo new page "pageName"` 新建页面，添加分类:

在命令行里面输入：

```
hexo new page "about"
```

然后你会发现`source`里面多了个目录`about`，里面有个`index.md`。其实你也可以手动建立。页面的格式和文章一样。

接着把链接加上，`themes//_config.yml`里面的`menu`一项，添加一行`About: /about`。

- `hexo clean` 清除缓存，会删除 public 文件夹中的内容。

### 一些规则

- 建立多标签：`[标签一，标签二，标签三]`

### 出现的错误

- 执行hexo d后出现error deployer not found:github的错误

`npm install hexo-deployer-git --save`

重新 deploy 即可

- 错误提示那个单词后有问题时，大部分是yml文件属性后没打空格，这个格式很严格：

  `theme:test`-改成：`theme: test`

- 提示命令没有找到时，如`hexo command not found`

  环境变量丢失，将`C:\Users\你的用户名\AppData\Roaming\npm\node_modules\hexo\bin`添加到path

