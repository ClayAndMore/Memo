## jenkins

https://www.jenkins.io



### 下载 in docker

https://www.jenkins.io/doc/book/installing/#linux

下载地址：https://www.jenkins.io/zh/download/

### docker 

注意： https://github.com/jenkinsci/docker/issues/779

docker pull jenkins/jenkins:lts

安装过程：

``` sh
mkdir /var/jenkins_home
chown 1000 /var/jenkins_home
docker run -d --name my-jenkins -p 8080:8080 -p 50000:50000 -v /var/jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

jenkins 使用 用户 -uid 1000

将装载绑定到卷中，则可以随时备份该目录（即jenkins_home）。

强烈建议这样做。 像对待数据库一样对待jenkins_home目录-在Docker中，通常将数据库放在一个卷上。



### 配置 和 插件

然后访问8080端口， 第一次进来会有个默认密码，在 /var/jenkins_home/secrets/initialAdminPassword 可以找到

这时会检测是否连接外网，如果没有可以配置代理连接外网，然后选择“install suggested plugins” 安装建议的插件。

常用插件：

**Email Extension Plugin** 该插件用于替换 Jenkins 自带的邮件发送，更加的强大。

**Git Plugin** 该插件允许使用GIT作为一个构建SCM(源代码控制管理系统)。

**Post build task** 该插件允许用户依据构建日志的输出执行一个shell/批处理任务。

**Ruby Plugin** 该插件允许用户在构建脚本中使用 Ruby。

**Python Plugin** 添加执行 Python 脚本作为Hudson的构建步骤。

**Gradle Plugin** 该插件允许Hudson调用Gradle构建脚本作为主体构建的步骤。

**FTP-Publisher Plugin** 该插件能上传项目构件和整个目录到一个FTP服务器。

**Extended Choice Parameter plugin** 该插件可以扩展参数化构建过程

**Extended Choice Parameter Plug-In** 该插件可以扩展参数化构建过程

**Dynamic Extended Choice Parameter Plug-In** 该插件可以扩展参数化构建过程

**git parameter Plug-in** 该插件可以扩展参数化构建过程

在线的插件库：https://jenkins-plugin-hub.herokuapp.com/



## Get start

点击新建，在新建项目页面输入项目名称，选择“构建一个自由风格的软件项目”，然后进入配置页面

**丢弃旧的构建：** 服务器资源是有限的，有时候保存了太多的历史构建，会导致Jenkins速度变慢，并且服务器硬盘资源也会被占满。当然下方的"保持构建天数" 和 保持构建的最大个数是可以自定义的，需要根据实际情况确定一个合理的值。



### 源码管理

1. 在**源码管理**中 选择 Git ,填写仓库地址, 填写https的地址，不是ssh的
2. 添加一个 Credentail， 在 Username 和 Password 输入 Git 仓库的用户名和密码



### 构建触发器

构建触发器就是我们选择什么时候来触发构建任务

1. 触发远程构建, 就是通过url接口调用来触发构建

2. 其他工程构建后触发

3. 定时构建。  周期性的构建，很好理解，就是每隔一段时间进行构建。

4. Github hook trigger for  GITScm poling

   当有更改push到gitlab代码仓库，即触发构建。后面会有一个触发构建的地址，一般被称为webhooks。需要将这个地址配置到gitlab中

5. 轮询SCM

   该选项是配合上面这个选项使用的。当代码仓库发生改动，jenkins并不知道。需要配置这个选项，周期性的去检查代码仓库是否发生改动。



### 配置go

1. 安装 go 插件： 系统管理” -> “管理插件” -> “可选插件” -> 选择 “Go Plugin” -> 点击最下边 “直接安装”

2. 安装完毕后，我们进入到 “系统管理” -> “Global Tool Configuration” -> “Go” -> “新增 Go”，默认情况下，插件自动安装 “Install from [golang.org](http://golang.org/)”， 国内网络下载golang.org的东西很麻烦。

3. 我们可以选择非自动安装，直接在机器上安装 Go，然后在这里指定 Go 安装目录即可：

   `tar xf go1.14.6.linux-amd64.tar.gz -C /var/jenkins_home/`

4. 勾掉自动安装，选择安装目录。

配置完成后即可以在构建环境中选择  "Set up Go programming language tools"



### 配置 docker

配置一个builder 节点,可以让jenkins 连接，并可以在上面构建镜像。

安装 插件 docker build step plugin

系统管理 -> 系统设置 -> Docker builder

先将被执行的docker node暴露相关的端口：

``` sh
# 通过 systemctl status docker 看下docker的启动文件位置
vim /lib/systemd/system/docker.service
# 启动命令后追加 -H tcp://0.0.0.0:2375
ExecStart=/usr/bin/docker daemon  -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375
# 重启docker
systemctl daemon-reload
systemctl restart docker
```





## 问题

### 忽略git的证书认证 jenkins certificate verification failed. CAfile

添加git 仓库地址时，可能会提示：

``` sh
jenkins certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none
```

是因为git校验了我们git 仓库的自认证证书，我们可以这样忽略认证：

`docker exec -it my-jenkins git config --global http.sslverify "false"`



### 重置管理员密码

进到 jenkinds 容器，找到 它的admin/config.xml 文件：

``` sh
bash-4.2$ find / -name config.xml
/opt/openshift/configuration/users/admin/config.xml
/opt/openshift/configuration/jobs/OpenShift Sample/config.xml
/opt/openshift/configuration/config.xml
...
/var/lib/jenkins/users/admin/config.xml # 一般是在这个目录
/var/lib/jenkins/jobs/OpenShift Sample/config.xml
...
bash-4.2$ vi /var/lib/jenkins/users/admin/config.xml/var/lib/jenkins/users/admin/config.xml/var/lib/jenkins/users/admin/config.xml^C
bash-4.2$ vi /var/lib/jenkins/users/admin/config.xml # 修改
```

修改admin的加密密码为123456的加密密码 #jbcrypt:$2a$10$MiIVR0rr/UhQBqT.bBq0QehTiQVqgNpUGyWW2nJObaVAM/2xSQdSq

``` xml 
<hudson.security.HudsonPrivateSecurityRealm_-Details>
      <passwordHash>#jbcrypt:$2a$10$MiIVR0rr/UhQBqT.bBq0QehTiQVqgNpUGyWW2nJObaVAM/2xSQdSq</passwordHash>

</hudson.security.HudsonPrivateSecurityRealm_-Details>
```

