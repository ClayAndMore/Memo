Tags:[linux]

## Linux 问题排查 

### strace 命令

可以看到命令的具体行为：

```sh
wichert@fog:~$ strace ls
execve("/bin/ls", ["ls"], [/* 16 vars */]) = 0
brk(0)                                  = 0x9fa8000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7f0a000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
```

看进程在干嘛：

```sh
wichert@fog:~$ strace -p 3761
Process 3761 attached - interrupt to quit
select(16, [5 7 8], NULL, [5 7 8], {0, 580000}) = 0 (Timeout)
alarm(0)                                = 62
rt_sigprocmask(SIG_BLOCK, [ALRM], [], 8) = 0
rt_sigaction(SIGALRM, {SIG_DFL}, {0x809a270, [], 0}, 8) ...
```





### No space left on device

* 一般是磁盘满了，导致无法创建新文件。

  各分区占用情况： 

  ```
  # df -h
  Filesystem Size Used Avail Use% Mounted on
  /dev/vda1 29G 29G 0 100% /
  udev  10M 0 10M 0% /dev
  tmpfs  101M 232K 100M 1% /run
  tmpfs  5.0M 0 5.0M 0% /run/lock
  tmpfs  405M 0 405M 0% /run/shm
  ```

  各目录占用情况：

  `du -sh /*`

* 可能由于小文件过多，使inode急剧增加，消耗完了inode区域的空间

  无法创建新的 inode 来存储文件的元信息，也就无法创建新文件。

  还是用df进行验证：

  ```
  # df -ih
  Filesystem Inodes IUsed IFree IUse% Mounted on
  /dev/vda1 1.9M 299K 1.6M 17% /
  udev  123K 299 123K 1% /dev
  tmpfs  126K 249 125K 1% /run
  tmpfs  126K 4 126K 1% /run/lock
  tmpfs  126K 2 126K 1% /run/shm
  ```

* 最后一种可能： 

  些文件删除时还被其它进程占用，此时文件并未真正删除，只是标记为 deleted，只有进程结束后才会将文件真正从磁盘中清除。

  **于是我通过 lsop 命令查看了被进程占用中的文件：**

  ```
  # lsof | grep deleted
  mysqld 1952 2982 mysql 5u REG  254,1  0 127 /tmp/ibzMEe4z (deleted)
  mysqld 1952 2982 mysql 6u REG  254,1  0 146 /tmp/ibq6ZFge (deleted)
  mysqld 1952 2982 mysql 10u REG  254,1  0 150 /tmp/ibyNHH8y (deleted)
  apache2 2869  root 9u REG  254,1  0 168 /tmp/.ZendSem.2w14iv (deleted)
  apache2 2869  root 10w REG  0,16  0 11077 /run/lock/apache2/rewrite-map.2869 (deleted)
  ...
  python 3102  root 1w REG  254,1 22412342132 264070 /var/log/nohup.out (deleted)
  ```



#### lsmod

显示已经加载到内核中模块的状态信息， 会列出已经载入系统中的模块。

```
Module                  Size  Used by
ipt_MASQUERADE         16384  3 
nf_nat_masquerade_ipv4    16384  1 ipt_MASQUERADE
iptable_mangle         16384  1 
iptable_nat            16384  1 
nf_nat_ipv4            16384  1 iptable_nat
nf_nat                 28672  2 nf_nat_masquerade_ipv4,nf_nat_ipv4
nf_conntrack_ipv4      16384  12 
nf_defrag_ipv4         16384  1 nf_conntrack_ipv4
```

- 第1列：表示模块的名称。
- 第2列：表示模块的大小。
- 第3列：表示依赖模块的个数。
- 第4列：表示依赖模块的内容。



#### 关闭selinux

`/etc/selinux/conf`



python:

```python
selinux_conf="""
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
"""
k=open('/etc/selinux/config','w')
k.write(selinux_conf)
k.close()
subprocess.call(['setenforce','0'])
```



### tab自动补全失灵

编辑etc/bash bashrc文件（管理员权限），找到以下几行：

```
# enable bash completion in interactive shells
# if{-f etc/bash_conmpletion} $$ ! shopt -oq posix:then
# ./etc/bash_completion
# fi
```

取消注释即可

**bashrc文件讲讲rc的含义**：run command ,一般rc后缀文件就是启动脚本文件





### 过多进程睡眠

当我们用ps找我们的进程发在S睡眠状态，eg:

```
root      3265  0.0  0.0   4224  1544 ?        S<   Mar01  14:59 /sbin/modprobe -b acpi:IPI0001:
root      3275  0.3  0.0  53264 30740 ?        Sl   Mar01  92:11 /usr/local/bin/gitlab-runner run --working-directory /home/gitlab-runner --config /etc/gitlab-runne
root      3286  0.0  0.0      0     0 ?        S<   Mar01   0:00 [kworker/11:1H]
```



我们可以用 `strace -p <pid>` 看他在干嘛，

* write(1, "foobar"..., 4096,  这是在写块

* futex(0x1fcc500, FUTEX_WAIT_PRIVATE, 0, NULL， 进程被挂起，可能是程序原因，可能是其他原因，比较复杂。