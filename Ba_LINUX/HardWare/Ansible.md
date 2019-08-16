### 写在前面

Ansible 默认通过ssh协议管理机器

一单Asible被安装， 它不会加数据库，不会有守护进程，只要安装再一个机器（比如你的便携笔记本），它就可以管理一整片集群。

英文文档：https://docs.ansible.com/

中文文档：https://ansible-tran.readthedocs.io/en/latest/index.html



### 要求

大于等于python2.7，pytthon3.5

被管理的节点，需要有个方式去通信，大多是用ssh。默认用sftp. 可以自己在ansible.cfg中替换成scp等。被管理的节点也需要python2.7 或 python3.5



### 安装

`yum install ansible`  

可以自己构建rpm：

```
$ git clone https://github.com/ansible/ansible.git
$ cd ./ansible
$ make rpm
$ sudo rpm -Uvh ./rpm-build/ansible-*.noarch.rpm
```



Ansible 1.3及之后的版本默认会在本地的 OpenSSH可用时会尝试用其进行远程通讯.这会启用ControlPersist(一个性能特性),Kerberos,和在~/.ssh/config中的配置选项如 Jump Host setup.然而,

当你使用Linux企业版6作为主控机(红帽企业版及其衍生版如CentOS),其OpenSSH版本可能过于老旧无法支持ControlPersist. 在这些操作系统中,Ansible将会退回并采用 paramiko (由Python实现的高质量OpenSSH库).

使用pip:

```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
(pip install paramiko )
pip install ansible
```

遇到的问题：

```sh

[root@10.250.123.10 python2.7]#bin/python2.7 bin/pip install ansible
Collecting ansible
Exception:
Traceback (most recent call last):...
    raise SSLError(e, request=request)
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)

# 参考： https://stackoverflow.com/questions/25981703/pip-install-fails-with-connection-error-ssl-certificate-verify-failed-certi

bin/python2.7 bin/pip  --trusted-host pypi.org --trusted-host files.pythonhosted.org  install  ansible
```

确认版本：

```sh
[root@10.250.123.10 python2.7]#bin/ansible --version
ansible 2.8.3
  config file = None
  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /ng8w/bin/python2.7/lib/python2.7/site-packages/ansible
  executable location = bin/ansible
  python version = 2.7.14 (default, Jan 30 2018, 12:09:57) [GCC 4.4.7 20120313 (Red Hat 4.4.7-18)]
```



### 第一条命令

编辑(或创建)/etc/ansible/hosts 并在其中加入一个或多个远程系统,你的public SSH key必须在这些系统的``authorized_keys``中.

```sh
[root@10.250.123.10 python2.7]#mkdir -p /etc/ansible
[root@10.250.123.10 python2.7]#vim /etc/ansible/hosts # 里面写入10.250.130.10.

[root@10.250.123.10 python2.7]#bin/ansible all -m ping
10.250.130.10 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}

[root@10.250.123.10 python2.7]#bin/ansible all -a "/bin/echo hello"  ## 执行了第一条命令
10.250.130.10 | CHANGED | rc=0 >>
hello
```

ping 所有节点，Ansible会像SSH那样试图用你的当前用户名来连接你的远程机器.要覆写远程用户名,只需使用’-u’参数. 如果你想访问 sudo模式,这里也有标识(flags)来实现:

```sh
# as bruce
$ ansible all -m ping -u bruce
# as bruce, sudoing to root
$ ansible all -m ping -u bruce --sudo
# as bruce, sudoing to batman
$ ansible all -m ping -u bruce --sudo --sudo-user batman
```



### 公钥认证

Ansible1.2.1及其之后的版本都会默认启用公钥认证.

如果有个主机重新安装并在“known_hosts”中有了不同的key,这会提示一个错误信息直到被纠正为止.在使用Ansible时,如果有个主机没有在“known_hosts”中被初始化将会导致在交互使用Ansible或定时执行Ansible时对key信息的确认提示.

如果你想禁用此项行为并明白其含义,你能够通过编辑 /etc/ansible/ansible.cfg or ~/.ansible.cfg来实现:

```
[defaults]
host_key_checking = False
```

或者你也可以通过设置环境变量来实现:

```
$ export ANSIBLE_HOST_KEY_CHECKING=False
```

同样注意在paramiko 模式中 公钥认证 相当的慢.因此,当使用这项特性时,切换至’SSH’是推荐做法.





### Inventory 文件

上面的/etc/ansible/hosts就是一个inventory文件，它声明了主机组和多台主机的关系以及联动配置信息。

文件的格式与windows的ini配置文件类似。

```ini
mail.example.com
badwolf.example.com:5309 #主机的SSH端口不是标准的22端口,可在主机名之后加上端口号,用冒号分隔

[webservers] # []中是组名, 对系统进行分类。
foo.example.com
bar.example.com

[dbservers] 
one.example.com
two.example.com
three.example.com
```

设置别名：

```ini
jumper ansible_ssh_port=5555 ansible_ssh_host=192.168.1.50 #
```

在这个例子中,通过 “jumper” 别名,会连接 192.168.1.50:5555，

范围：

```ini
[webservers]
www[01:50].example.com

[databases]
db-[a:f].example.com
```

连接类型和用户名：

```ini
[targets]

localhost              ansible_connection=local
other1.example.com     ansible_connection=ssh        ansible_ssh_user=mpdehaan
other2.example.com     ansible_connection=ssh        ansible_ssh_user=mdehaan
```



#### 组变量和组成员：

组变量： 

```ini
[atlanta]
host1
host2

[atlanta:vars] # vars代表组变量声明
ntp_server=ntp.atlanta.example.com
proxy=proxy.atlanta.example.com
```

把一个组当为另一个组的子成员

```ini
[atlanta]
host1
host2

[raleigh]
host2
host3

[southeast:children] # children 认为是声明组成员
atlanta
raleigh

[southeast:vars]
some_server=foo.southeast.example.com
halon_system_timeout=30
self_destruct_countdown=60
escape_pods=2

[usa:children]
southeast
northeast
southwest
northwest
```



#### 分文件定义

待补充



#### 参数说明

```sh
ansible_ssh_host # 将要连接的远程主机名.与你想要设定的主机的别名不同的话,可通过此变量设置.
ansible_ssh_port # ssh端口号.如果不是默认的端口号,通过此变量设置.
ansible_ssh_user # 默认的 ssh 用户名
ansible_ssh_pass # ssh 密码(这种方式并不安全,我们强烈建议使用 --ask-pass 或 SSH 密钥)
ansible_sudo_pass # sudo 密码(这种方式并不安全,我们强烈建议使用 --ask-sudo-pass)

ansible_sudo_exe (new in version 1.8) # sudo 命令路径(适用于1.8及以上版本)

ansible_connection
    # 主机的连接类型.比如:local, ssh 或者 paramiko. Ansible 1.2 以前默认使用 paramiko.1.2 以后默认使用 'smart','smart' 方式会根据是否支持 ControlPersist, 来判断'ssh' 方式是否可行.

ansible_ssh_private_key_file
   #  ssh 使用的私钥文件.适用于有多个密钥,而你不想使用 SSH 代理的情况.

ansible_shell_type
   # 目标系统的shell类型.默认情况下,命令的执行使用 'sh' 语法,可设置为 'csh' 或 'fish'.

ansible_python_interpreter
   #  目标主机的 python 路径.适用于的情况: 系统中有多个 Python, 或者命令路径不是"/usr/bin/python",比如  \*BSD, 或者 /usr/bin/python
   #  不是 2.X 版本的 Python.我们不使用 "/usr/bin/env" 机制,因为这要求远程用户的路径设置正确,且要求 "python" 可执行程序名不可为 python以外的名字(实际有可能名为python26).

  #   与 ansible_python_interpreter 的工作方式相同,可设定如 ruby 或 perl 的路径....
```

eg:

```
some_host         ansible_ssh_port=2222     ansible_ssh_user=manager
aws_host          ansible_ssh_private_key_file=/home/example/.ssh/aws.pem
freebsd_host      ansible_python_interpreter=/usr/local/bin/python
ruby_module_host  ansible_ruby_interpreter=/usr/bin/ruby.1.9.3
```







### PLAYBOOKS

它是一个用于构建应用环境的YAML格式的文件，人类和机器可读，描述事物状态。

其中有几个变量：

Inventories:  可以是静态或者动态的服务器ip列表，范围或其他。

```yaml
[web]
web-1.example.com
web-2.example.com
[db]
db-a.example.com
db-b.example.com
```

