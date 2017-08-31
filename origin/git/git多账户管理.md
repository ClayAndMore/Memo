在工作时，我们的个人git和公司git要合理的区分。

### 多账户链接

`$ ssh-keygen -t rsa -C "my_email@email.com" `

输入ssh-key的名字,个人。

`$ ssh-keygen -t rsa -C "company_email@email.com" `

输入ssh-key的名字，公司。

分别将连个rsa.pub公钥添加到主页（个人和公司）。

在.ssh文件下建立config文件：

```conf
# 配置github.com
Host github.com                 
    HostName github.com
    IdentityFile C:\\Users\\AT\\.ssh\\github_rsa
    PreferredAuthentications publickey
    User claymore

# 配置gitlab
Host git.pta.center
    HostName git.pta.center
    IdentityFile C:\\Users\\AT\\.ssh\\id_rsa
    Port 10022
    PreferredAuthentications publickey
    User wangyu
    
# 局域网
Host 192.168.1.222
    HostName 192.168.1.222
    User smallajax@foxmail.com
    PreferredAuthentications publickey
    IdentityFile /D/Workspace/ssh/id_rsa_oschina
```



Host后面的名字可以随便起，就是命名。

Hostname 是域名 或者ip ,第二个中是我在公司局域网的域名，已经在host文件中配置ip,

注意有个port参数，这个要看你git项目的链接参数才可知道这里要填的端口号，而不是网站服务器的端口号。

User  你的邮箱

PreferredAuthentications 验证方式，这里是公钥方式，还可以设置用密码等。

IdentifyFile 是私钥 的文件地址。



#### 测试配置是否成功

`ssh -T git@github.com `

这里的github.com 是上面的Host 的名称。接下来可以分别验证。



#### 添加到ssh-agent

`ssh-add 密钥文件路径`

如进到.ssh文件夹中，可以直接添加了 `ssh-add 密钥文件的名字`

如果执行`ssh-add ...`命令提示如下错误：

```
Could not open a connection to your authentication agent.
```

那么请执行`eval $(ssh-agent)`命令后再重试，如果还不行，请再执行`ssh-agent bash`命令后重试。 
如果还不行，请参考：[StackOverFlow·ssh-Could not open a…](http://stackoverflow.com/questions/17846529/could-not-open-a-connection-to-your-authentication-agent)



#### 配置局部用户和邮箱

进到项目目录，分别配置用户和邮箱。

`git config --local user.name "你的名字"`
`git config --local user.email "你的邮箱"`

