## Linux 



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





#### iptables

`/etc/sysconfig/iptables`

* service iptables start

* service iptablse save

  ```
  保存规则：shell>iptables-save > /etc/iptables-script

  恢复规则：shell>iptables-restore > /etc/iptables-script

  保存和恢复的位置只要是两者一致就可以了，如果iptables-script没有则需要创建。
  ```



`/etc/security/limits.conf`

/etc/security/limits.conf 是 Linux 资源使用配置文件，用来限制用户对系统资源的使用

语法：<domain>  <type>  <item>  <value>

```
[root@localhost ~]# cat /etc/security/limits.conf
* soft nproc 65535      # 警告设定所有用户最大打开进程数为65535
* hard nproc 65535      # 严格设定所有用户最大打开进程数为65535
* soft nofile 65535     # 警告设定所有用户最大打开文件数为65535
* hard nofile 65535     # 严格设定所有用户最大打开文件数为65535
```



```
<domain> 表示要限制的用户，可以是：

         ① 用户名
         ② 组名（组名前面加'@'以区别用户名）
         ③ *（表示所有用户）

<type> 有两个值：

         ① soft 表示警告的设定，可以超过这个设定值，但是超过会有警告信息
         ② hard 表示严格的设定，必定不能超过这个设定的值

<item> 表示可选的资源，如下：

         ① core：限制内核文件的大小
         ② data：最大数据大小
         ③ fsize：最大文件大小
         ④ memlock：最大锁定内存地址空间
         ⑤ nofile：打开文件的最大数目
         ⑥ rss：最大持久设置大小
         ⑦ stack：最大栈大小
         ⑧ cpu：以分钟为单位的最多CPU时间
         ⑨ nproc：进程的最大数目
         ⑩ as：地址空间限制

<value> 表示要限制的值
```





### 网卡配置

网卡配置文件：`/etc/sysconfig/network-scripts`

查看所有网卡： ifconfig -a .



##### 查看某网卡的口是否有线连接： 

1. `ethtool eth1` 

   最后一行： Link detected: yes为正常no为失败 

2. 或 `mii-tool` 用的少，有的驱动不支持。

3. ```
   /mnt/wifi$ cat /proc/net/dev

   Inter-|  Receive                                                | Transmit

   face |bytes  packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carriercompressed

   lo:      0      0    0  0    0    0        0        0        0      0    0    0  0    0      0        0

   eth0:    3439    15  0  0    0    0        0        0        0      0    0    0  0    0      0          0

   在开发板上/proc/net目录下，还有很多关于网络的信息的文件，我试了不少，觉得这个还算准确，但并非100%哦，如果启动开发板后，eth0中bytes、packets 不为0，那它一定插了网线，但此种方法只适合开机启动时判断，之后的话，就很麻烦了。
   ```

   ​

确定某网卡的具体物理口， 用：

`ethtool -p eth2`  时，对应网卡会闪烁， 注意此时是未插网线。



关闭 / 开启 / 重启 某块网卡：

`ifdown eth0 && ifup eth0       # 一定要连在一起使用！！切记啊  `

重启所有网卡服务：

`/etc/init.d/network restart`





##### 创建虚拟网卡

```
cd /etc/sysconfig/network-scripts
mv 
```

