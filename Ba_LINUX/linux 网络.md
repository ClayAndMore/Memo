## linux 网络

### linux的网卡

网卡的名称是以网卡内核模块对应的设备名称来表示的。

默认网卡名称为eth0， 第二张网卡则为eth1, 以此类推。



网卡需要内核的支持，才能驱动它。

如果不兼容，要么重新编译内核，要么重新编译网卡的内核模块，当然，大家都不愿意这么干。





### iptables

`/etc/sysconfig/iptables`

```
# 查看防火墙状态
service iptables status
 
# 停止防火墙
service iptables stop
 
# 启动防火墙
service iptables start
 
# 重启防火墙
service iptables restart
 
# 永久关闭防火墙
chkconfig iptables off
 
# 永久关闭后重启
chkconfig iptables on
```



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



### 网络

- netstat 当前网络状态
- ping 
- ifconfig
- ssh
- ftp
- telnet

#### 查看端口

查看80端口的占用情况：

lsof -i:80  

或者：

netstat -apn | grep 80

上面的命令执行之后可以显示进程号，找到进程号以后，再使用以下命令查看详细信息：

ps -aux | grep <进程号>

### 