Tags:[Git]

## gitlab-ci

gitlab-ci全称是gitlab continuous integration的意思，也就是持续集成。中心思想是当每一次push到gitlab的时候，都会触发一次脚本执行，然后脚本的内容包括了测试，编译，部署等一系列自定义的内容



### GitLab-CI

这个是一套配合GitLab使用的持续集成系统，是GitLab自带的，也就是你装GitLab的那台服务器上就带有的。无需多考虑。.gitlab-ci.yml的脚本解析就由它来负责。



### GitLab-Runner

这个是脚本执行的承载者，.gitlab-ci.yml的script部分的运行就是由runner来负责的。GitLab-CI浏览过项目里的.gitlab-ci.yml文件之后，根据里面的规则，分配到各个Runner来运行相应的脚本script。这些脚本有的是测试项目用的，有的是部署用的。

#### 安装

官网： `https://docs.gitlab.com/runner/install/`

1. 下载

    ```
     # Linux x86-64
     sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
    ```

2. 执行权限：

   ` sudo chmod +x /usr/local/bin/gitlab-runner`

3. 创建ci用户：

   `useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash`

4. 注册Runner， runner需要向服务端注册

   ```
   $ gitlab-runner register
   #引导会让你输入gitlab的url，输入自己的url，例如http://gitlab.example.com/
   #引导会让你输入token，去相应的项目下找到token，例如ase12c235qazd32
   #引导会让你输入tag，一个项目可能有多个runner，是根据tag来区别runner的，输入若干个就好了，比如web,hook,deploy
   #引导会让你输入executor，这个是要用什么方式来执行脚本，图方便输入shell就好了。
   ```

5. 安装和运行

   ` sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner`

   ` gitlab-runner start`



#### 遇到的问题

```
x509: cannot validate certificate for 10.250.123.12 because it doesn't contain any IP SANs
PANIC: Failed to register this runner. Perhaps you are having network problems
```

这个是GItlab server启用了证书认证，我们需要去它页面上下载证书，上传到runner的: /etc/gitlab-runner/certs/, 没有目录要建立。

URL最好填写和证书里一样的域名，否则影响验证。如果有域名，记得配hosts.

```sh
# gitlab-runner register --tls-ca-file=/etc/gitlab-runner/certs/-_**_center.crt
Runtime platform                                    arch=amd64 os=linux pid=20825 revision=1564076b version=12.4.0
Running in system-mode.

Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
https://*.**.center:10443/
Please enter the gitlab-ci token for this runner:
eoRR-JTk2Jaz6uR17yR_
Please enter the gitlab-ci description for this runner:
[bogon]: host58
Please enter the gitlab-ci tags for this runner (comma separated):
58host
Registering runner... succeeded                     runner=eoRR-JTk
Please enter the executor: custom, shell, docker+machine, docker, docker-ssh, parallels, ssh, virtualbox, docker-ssh+machine, kubernetes:
shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
```

其他参考链接： https://stackoverflow.com/questions/44458410/gitlab-ci-runner-ignore-self-signed-certificate 



`x509: certificate has expired or is not yet valid`

证书过期，如果证书没有过期，runner同步一下server的时间

ntpdate ntp.sjtu.edu.cn



创建后，gitlab server 可能会显示该节点的状态：

`New runner. Has not connected yet`

运行一下  `gitlab-runner verify`  试试



ci/cd 时，又有如下问题：

` Peer certificate cannot be authenticated with known CA certificates `

```sh
# vi /etc/sudoers
gitlab-runner ALL=(ALL)     ALL
# chmod -R 755 /home/gitlab-runner/
# vim /home/gitlab-runner/.bashrc
export GIT_SSL_NO_VERIFY=1
# source /home/gitlab-runner/.bashrc
```







#### docker 版

todo

https://docs.gitlab.com/runner/install/docker.html，



### 一些概念

### Pipeline

一次 Pipeline 其实相当于一次构建任务，里面可以包含多个流程，如安装依赖、运行测试、编译、部署测试服务器、部署生产服务器等流程。

任何提交或者 Merge Request 的合并都可以触发 Pipeline，如下图所示：

```
+------------------+           +----------------+
|                  |  trigger  |                |
|   Commit / MR    +---------->+    Pipeline    |
|                  |           |                |
+------------------+           +----------------+
```



### Stages

Stages 表示构建阶段，说白了就是上面提到的流程。我们可以在一次 Pipeline 中定义多个 Stages，这些 Stages 会有以下特点：

- 所有 Stages 会按照顺序运行，即当一个 Stage 完成后，下一个 Stage 才会开始
- 只有当所有 Stages 完成后，该构建任务 (Pipeline) 才会成功
- 如果任何一个 Stage 失败，那么后面的 Stages 不会执行，该构建任务 (Pipeline) 失败

因此，Stages 和 Pipeline 的关系就是：

```
+--------------------------------------------------------+
|                                                        |
|  Pipeline                                              |
|                                                        |
|  +-----------+     +------------+      +------------+  |
|  |  Stage 1  |---->|   Stage 2  |----->|   Stage 3  |  |
|  +-----------+     +------------+      +------------+  |
|                                                        |
+--------------------------------------------------------+
```



### Jobs

Jobs 表示构建工作，表示某个 Stage 里面执行的工作。我们可以在 Stages 里面定义多个 Jobs，这些 Jobs 会有以下特点：

- 相同 Stage 中的 Jobs 会并行执行
- 相同 Stage 中的 Jobs 都执行成功时，该 Stage 才会成功
- 如果任何一个 Job 失败，那么该 Stage 失败，即该构建任务 (Pipeline) 失败

所以，Jobs 和 Stage 的关系图就是：

```
+------------------------------------------+
|                                          |
|  Stage 1                                 |
|                                          |
|  +---------+  +---------+  +---------+   |
|  |  Job 1  |  |  Job 2  |  |  Job 3  |   |
|  +---------+  +---------+  +---------+   |
|                                          |
```



job 是一组具有约束的作业，可以指定无限数量的 job 。

job 被定义为具有任意名称的顶级元素，并且始终必须至少包含该 script 子句。

job 必须具有唯一的名称，下面是一些保留的关键字不可以作为 job 的名称。

```
image
services
stages
types
before_script
after_script
variables
cache
```



### .gitlab-ci.yml

这个是在git项目的根目录下的一个文件，记录了一系列的阶段和执行规则。GitLab-CI在push后会解析它，根据里面的内容调用runner来运行。

具体写法和入门：https://docs.gitlab.com/ce/ci/quick_start/README.html

更多： https://docs.gitlab.com/ee/ci/yaml/#doc-nav

```yaml
before_script:
  - apt-get update -qq && apt-get install -y -qq sqlite3 libsqlite3-dev nodejs
  - ruby -v
  - which ruby
  - gem install bundler --no-document
  - bundle install --jobs $(nproc)  "${FLAGS[@]}"

rspec:
  script:
    - bundle exec rspec

rubocop:
  script:
    - bundle exec rubocop
```

rspec 和 rubocop 指的是两个job,  是自己取的名，在before_script之后执行。

rspec 和 rubocop中的script指的是运行的脚本



#### 基本写法

```yaml
# 定义 stages
stages:
  - build
  - test

# 定义 job
job1:
  stage: test
  script:
    - echo "I am job1"
    - echo "I am in test stage"

# 定义 job
job2:
  stage: build
  script:
    - echo "I am job2"
    - echo "I am in build stage"
```

每个 job 中可以可以再用 `stage` 关键字来指定该 job 对应哪个 stage.

这里先执行build, 然后再test.



#### 例子

```yaml
stages:
  - test
  - deploy

# 变量
variables:
  DEV_RSYNC_PATH: "/data/deploy/xunlei.com/misc.xl9.xunlei.com/d/"

# 所有 stage 之前的操作
before_script:
  - npm set registry http://xnpm.sz.xunlei.cn
  - npm install

# 代码检查
lint:
  stage: test
  script: npm run lint

# 单元测试
unit:
  stage: test
  script: npm run unit

# 部署测试服务器
deploy_dev:
  stage: deploy
  tags:
    - 10.10.34.91-dev
  only:
    - develop
  script:
    - rsync -av --delete-after --exclude-from=/data/shell/home.xl9.xunlei_exclude.list . $DEV_RSYNC_PATH
    - chmod -R 755 $DEV_RSYNC_PATH
    - chown -R nobody:nobody $DEV_RSYNC_PATH
    - find $DEV_RSYNC_PATH -type f -exec chmod 644 {} \;
    - cd $DEV_RSYNC_PATH
    - npm install
```



* before_script  定义stages/jobs之前都会执行的命令。
* after_script    定义任何 stages/Jobs 运行完后都会执行的命令。 要求 GitLab 8.7+ 和 GitLab Runner 1.2+
* variables: 除了用户定义的变量，还有由Runner本身设置的变量。一个例子是`CI_COMMIT_REF_NAME`具有构建项目的分支或标签名称的值。

* tags   被用于选择具体runner 去跑这个项目
* only  指定分支提交的时候才会触发相关的jobs