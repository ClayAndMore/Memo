## CI 持续集成



### 一些概念

#### Pipeline

一次 Pipeline 其实相当于一次构建任务，里面可以包含多个流程，如安装依赖、运行测试、编译、部署测试服务器、部署生产服务器等流程。

包含有多个阶段（[stages]），每个阶段包含有一个或多个工序（[jobs]），比如先购料、组装、测试、包装再上线销售，每一次push或者MR都要经过流水线之后才可以合格出厂。而`.gitlab-ci.yml`正是定义了这条流水线有哪些阶段，每个阶段要做什么事。



#### Gitlab-CI

[Gitlab-CI]是GitLab Continuous Integration（Gitlab持续集成）的简称。
从Gitlab的8.0版本开始，gitlab就全面集成了Gitlab-CI,并且对所有项目默认开启。
只要在项目仓库的根目录添加`.gitlab-ci.yml`文件，并且配置了Runner（运行器），那么每一次合并请求（MR）或者push都会触发CI [pipeline]。



#### GItlab-runner

[Gitlab-runner]是`.gitlab-ci.yml`脚本的运行器，Gitlab-runner是基于Gitlab-CI的API进行构建的相互隔离的机器（或虚拟机）。GitLab Runner 不需要和Gitlab安装在同一台机器上，但是考虑到GitLab Runner的资源消耗问题和安全问题，也不建议这两者安装在同一台机器上。



通过`gitlab-ci-multi-runner register`注册的Runner配置会存储在`/etc/gitlab-runner/config.toml`中，如果需要修改可直接编辑该文件。