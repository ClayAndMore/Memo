## systemd

从 CentOS 7.x 以后，Red Hat 系列的 distribution 放弃沿用多年的 System V 开机启动服务的
流程，就是 init 启动脚本的方法, 改用 systemd 这个启动服务管理机制



### systemd的好处

#### 平行处理所有服务

加速开机流程： 旧的 init 启动脚本是“一项一项任务依序启动”的模式，因此不相依的服务也是得要一个一个的等待。但目前我们的硬件主机系统与操作系统几乎都支持多核心架构了， 没道理未相依的服务不能同时启动啊！systemd 就是可以让所有的服务同时启动，因此你会发现到，系统启动的速度变快了！



#### 一经要求就回应的 on-demand 启动方式

 systemd 全部就是仅有一只 systemd 服务搭配 systemctl 指令来处理，无须其他额外的指令来支持。不像 systemV 还要 init,chkconfig, service... 等等指令。 此外， systemd 由于常驻内存，因此任何要求 （ondemand） 都可以立即处理后续的 daemon 启动的任务。



#### 服务相依性的自我检查

由于 systemd 可以自订服务相依性的检查，因此如果 B 服务是架构在 A 服务上面启动的，那当你在没有启动 A 服务的情况下仅手动启动 B 服务时，systemd 会自动帮你启动 A 服务喔！这样就可以免去管理员得要一项一项服务去分析的麻烦～（如果读者不是新手，应该会有印象，当你没有启动网络， 但却启动 NIS/NFS时，那个开机时的 timeout 甚至可达到 10~30 分钟...）



#### 依 daemon 功能分类

systemd 旗下管理的服务非常多，包山包海啦～为了理清所有服务的功能，因此，首先 systemd 先定义所有的服务为一个服务单位 （unit），并将该unit 归类到不同的服务类型 （type） 去。 旧的 init 仅分为 stand alone 与 super daemon实在不够看，systemd 将服务单位 （unit） 区分为 service, socket, target, path, snapshot, timer 等多种不同的类型（type）， 方便管理员的分类与记忆



#### 将多个 daemons 集合成为一个群组

如同 systemV 的 init 里头有个 runlevel 的特色，systemd 亦将许多的功能集合成为一个所谓的 target 项目，这个项目主要在设计操作环境的创建， 所以是集合了许多的 daemons，亦即是执行某个 target 就是执行好多个
daemon 的意思！



#### 向下相容旧有的 init 服务脚本 

基本上， systemd 是可以相容于 init 的启动脚本的，因此，旧的 init 启动脚本也能够通过 systemd 来管理，只是更进阶的 systemd 功能就没有
办法支持就是了。



### 没有取代的点

在 runlevel 的对应上，大概仅有 runlevel 1, 3, 5 有对应到 systemd 的某些 target 类型而已，没有全部对应；

全部的 systemd 都用 systemctl 这个管理程序管理，而 systemctl 支持的语法有限制，不像 /etc/init.d/daemon 就是纯脚本可以自订参数，systemctl 不可自订参数。；

如果某个服务启动是管理员自己手动执行启动，而不是使用 systemctl 去启动的 （例如
你自己手动输入 crond 以启动 crond 服务），**那么 systemd 将无法侦测到该服务，而无**
**法进一步管理。**
systemd 启动过程中，无法与管理员通过 standard input 传入讯息！因此，自行撰写
systemd 的启动设置时，务必要取消互动机制～（连通过启动时传进的标准输入讯息也
要避免！）



### systemd 的配置文件目录

/usr/lib/systemd/system/：每个服务最主要的启动脚本设置，有点类似以前的 /etc/init.d下面的文件；
/run/systemd/system/：系统执行过程中所产生的服务脚本，这些脚本的优先序要比/usr/lib/systemd/system/ 高！
/etc/systemd/system/：管理员依据主机系统的需求所创建的执行脚本，其实这个目录有点像以前 /etc/rc.d/rc5.d/Sxx 之类的功能！执行优先序又比 /run/systemd/system/ 高.

```sh
[root@10.250.123.10 ~]#ls /usr/lib/systemd/system/ | grep crond # 太多 没有都打出来
crond.service

[root@10.250.123.10 ~]#ls /run/systemd/system/ # 这个目录感觉不是很重要
session-225428.scope    session-225838.scope.d  session-225869.scope    user-0.slice.d
session-225428.scope.d  session-225862.scope    session-225869.scope.d
session-225838.scope    session-225862.scope.d  user-0.slice

[root@10.250.123.10 ~]#ls /etc/systemd/system
basic.target.wants                           network-online.target.wants
dbus-org.freedesktop.NetworkManager.service  redis-sentinel.service.d
dbus-org.freedesktop.nm-dispatcher.service   redis.service.d
default.target                               remote-fs.target.wants
default.target.wants                         sockets.target.wants
getty.target.wants                           sysinit.target.wants
local-fs.target.wants                        system-update.target.wants
multi-user.target.wants                      timers.target.wants

[root@10.250.123.10 ~]#ll /etc/systemd/system/basic.target.wants/
total 0
lrwxrwxrwx. 1 root root 41 Feb 27  2020 microcode.service -> /usr/lib/systemd/system/microcode.service
lrwxrwxrwx. 1 root root 42 Feb 27  2020 rhel-dmesg.service -> /usr/lib/systemd/system/rhel-dmesg.service
```

也就是说，到底系统开机会不会执行某些服务其实是看 /etc/systemd/system/ 下面的设置,所以该目录下面就是一大堆链接文件。

而实际执行的 systemd 启动脚本配置文件， 其实都是放置在 /usr/lib/systemd/system/ 下面的喔！

**因此如果你想要修改某个服务启动的设置，应该要去 /usr/lib/systemd/system/ 下面修改**！ /etc/systemd/system/ 仅是链接到正确的执行脚本配置文件而已。所以想要看执行脚本设置，应该就得要到 /usr/lib/systemd/system/ 下面去
查阅才对！

运行相关过程的目录：

```
/etc/sysconfig/*： 几乎所有的服务都会将初始化的一些选项设置写入到这个目录下，举
例来说，mandb 所要更新的 man page 索引中，需要加入的参数就写入到此目录下的
man-db 当中喔！而网络的设置则写在 /etc/sysconfig/network-scripts/ 这个目录内。所
以，这个目录内的文件也是挺重要的；
/var/lib/： 一些会产生数据的服务都会将他的数据写入到 /var/lib/ 目录中。举例来说，数
据库管理系统 Mariadb 的数据库默认就是写入 /var/lib/mysql/ 这个目录下啦！
/run/： 放置了好多 daemon 的暂存盘，包括 lock file 以及 PID file 等等。
```



### systemd 的 unit 类型

基本上， systemd 将过去所谓的 daemon 执行脚本通通称为一个服务单位 （unit），而每种服务单位依据功能来区分时，就分类为不同的类型 （type）。 

基本的类型有包括系统服务、数据监听与交换的插槽档服务 （socket）、储存系统状态的快照类型、提供不同类似执行等级分类的操作环境 （target） 等等。

| 扩展名                 | 主要服务功能                                                 |
| ---------------------- | ------------------------------------------------------------ |
| .service               | 一般服务类型 （service unit）：主要是系统服务，包括服务器本身所需要的本机服务以及网络服务都是！比较经常被使用到的服务大多是这种类型！ 所以，这也是最常见的类型了！ |
| .socket                | 内部程序数据交换的插槽服务 （socket unit）：主要是 IPC （Interprocess communication） 的传输讯息插槽档 （socket file） 功能。 这种类型的服务通常在监控讯息传递的插槽档，当有通过此插槽档传递讯息来说要链接服务时，就依据当时的状态将该用户的要求传送到对应的daemon， 若 daemon 尚未启动，则启动该 daemon 后再传送用户的要求。使用 socket 类型的服务一般是比较不会被用到的服务，因此在开机时通常会稍微延迟启动的时间 （因为比较没有这么常用嘛！）。一般用于本机服务比较多，例如我们的图形界面很多的软件都是通过 socket 来进行本机程序数据交换的行为。 （这与早期的 xinetd 这个 super daemon 有部份的相似喔！） |
| .target                | 执行环境类型 （target unit）：其实是一群 unit 的集合，也就是说， 选择执行**.target 就是执行一堆其他 .service 或/及 .socket 之类的服务就是了！ |
| .mount<br />.automount | 文件系统挂载相关的服务 （automount unit / mount unit）：例如来自网络<br/>的自动挂载、NFS 文件系统挂载等与文件系统相关性较高的程序管理。 |
| .path                  | 侦测特定文件或目录类型 （path unit）：某些服务需要侦测某些特定的目录来提供伫列服务，例如最常见的打印服务，就是通过侦测打印伫列目录来启动打印功能！ 这时就得要 .path 的服务类型支持了！ |
| .timer                 | 循环执行的服务 （timer unit）：这个东西有点类似 anacrontab 喔！不过是由 systemd 主动提供的，比 anacrontab 更加有弹性！ |



## systemctl 管理服务

systemd 这个启动服务的机制，主要是通过一只名为 systemctl 的指令来处理的！
跟以前 systemV 需要 service / chkconfig / setup / init 等指令来协助不同， systemd 就是仅有systemctl 这个指令来处理.

### 启动/开机启动/状态观察

命令格式： `systemctl [command] [unit]`

command: 

> start ：立刻启动后面接的 unit
> stop ：立刻关闭后面接的 unit
> restart ：立刻关闭后启动后面接的 unit，亦即执行 stop 再 start 的意思
> reload ：不关闭后面接的 unit 的情况下，重新载入配置文件，让设置生效
> enable ：设置下次开机时，后面接的 unit 会被启动
> disable ：设置下次开机时，后面接的 unit 不会被启动
> status ：目前后面接的这个 unit 的状态，会列出有没有正在执行、开机默认执行否、登录等信息等！
> is-active ：目前有没有正在运行中
> is-enable ：开机时有没有默认要启用这个 unit

eg:

```sh
[root@10.250.123.10 ~]#systemctl status sshd
● sshd.service - OpenSSH server daemon
   Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2020-08-04 14:32:35 CST; 11 months 13 days left
     Docs: man:sshd(8)
           man:sshd_config(5)
 Main PID: 25352 (sshd)
    Tasks: 1
   CGroup: /system.slice/sshd.service
           └─25352 /usr/sbin/sshd -D

Aug 21 15:23:18 10.250.123.10 sshd[1741]: pam_unix(sshd:account): account root has pas...re
Aug 22 17:40:03 10.250.123.10 sshd[38770]: Accepted password for root from 10.250.72.1...h2
Hint: Some lines were ellipsized, use -l to show in full.
[root@10.250.123.10 ~]#systemctl status sshd.service # 一样的加个后缀.service
```
Loaded：这行在说明，开机的时候这个 unit 会不会启动，enabled 为开机启动，disabled 开机不会启动
除了这两种状态还有：

> static：这个 daemon 不可以自己启动 （enable 不可），不过可能会被其他的 enabled
> 的服务来唤醒 （相依属性的服务）
> mask：这个 daemon 无论如何都无法被启动！因为已经被强制注销 （非删除）。可通过
> systemctl unmask 方式改回原本状态



Active：现在这个 unit 的状态是正在执行 （running） 或没有执行 （dead）

另1： active （exited）：仅执行一次就正常结束的服务，目前并没有任何程序在系统中执行。

> 举例来说，开机或者是挂载时才会进行一次的 quotaon 功能，就是这种模式！ quotaon
> 不须一直执行～只须执行一次之后，就交给文件系统去自行处理啰！通常用 bash shell
> 写的小型服务，大多是属于这种类型 （无须常驻内存）

另2： active （waiting）：正在执行当中，不过还再等待其他的事件才能继续处理。

> 举例来说，打印的伫列相关服务就是这种状态！ 虽然正在启动中，不过，也需要真的有伫列进
> 来 （打印工作） 这样他才会继续唤醒打印机服务来进行下一步打印的功能。



所以 关闭一个正常的进程在这里不可以用kill的方式，否则systemclt无法继续监控



### 观察系统上的所有服务

```
systemctl [command] [--type=TYPE] [--all]
command:
list-units ：依据 unit 列出目前有启动的 unit。若加上 --all 才会列出没启动的。
list-unit-files ：依据 /usr/lib/systemd/system/ 内的文件，将所有文件列表说明。
--type=TYPE：就是之前提到的 unit type，主要有 service, socket, target 等
```

socket 服务：

```
 # systemctl list-sockets
LISTEN                          UNIT                         ACTIVATES
/dev/log                        systemd-journald.socket      systemd-journald.service
/run/dbus/system_bus_socket     dbus.socket                  dbus.service
/run/dmeventd-client            dm-event.socket              dm-event.service
/run/dmeventd-server            dm-event.socket              dm-event.service
/run/lvm/lvmetad.socket         lvm2-lvmetad.socket          lvm2-lvmetad.service
/run/lvm/lvmpolld.socket        lvm2-lvmpolld.socket         lvm2-lvmpolld.service
/run/systemd/initctl/fifo       systemd-initctl.socket       systemd-initctl.service
/run/systemd/journal/socket     systemd-journald.socket      systemd-journald.service
/run/systemd/journal/stdout     systemd-journald.socket      systemd-journald.service
/run/systemd/shutdownd          systemd-shutdownd.socket     systemd-shutdownd.service
/run/udev/control               systemd-udevd-control.socket systemd-udevd.service
/var/run/libvirt/virtlockd-sock virtlockd.socket             virtlockd.service
/var/run/libvirt/virtlogd-sock  virtlogd.socket              virtlogd.service
/var/run/rpcbind.sock           rpcbind.socket               rpcbind.service
0.0.0.0:111                     rpcbind.socket               rpcbind.service
0.0.0.0:111                     rpcbind.socket               rpcbind.service
@ISCSIADM_ABSTRACT_NAMESPACE    iscsid.socket                iscsid.service
@ISCSID_UIP_ABSTRACT_NAMESPACE  iscsiuio.socket              iscsiuio.service
[::]:111                        rpcbind.socket               rpcbind.service
[::]:111                        rpcbind.socket               rpcbind.service
kobject-uevent 1                systemd-udevd-kernel.socket  systemd-udevd.service
```

这样能够知道监听本机服务需求的 socket file 所在的文件名位置

上面是了解了使用网络的服务，下面了解服务使用的端口号：

```
[root@study ~]# cat /etc/services
....（前面省略）....
ftp 21/tcp
ftp 21/udp fsp fspd
ssh 22/tcp # The Secure Shell （SSH） Protocol
ssh 22/udp # The Secure Shell （SSH） Protocol
....（中间省略）....
http 80/tcp www www-http # WorldWideWeb HTTP
http 80/udp www www-http # HyperText Transfer Protocol
```





### 各服务直接的相依性

```sh
#  列出目前的 target 环境下，用到什么特别的 unit
systemctl get-default

# 相依列表
systemctl list-dependencies [unit] [--reverse]
选项与参数：
--reverse ：反向追踪谁使用这个 unit 的意思！
```

eg:

```sh
[root@study ~]# systemctl get-default
multi-user.target
[root@study ~]# systemctl list-dependencies
default.target
├─abrt-ccpp.service
├─abrt-oops.service
├─vsftpd.service
├─basic.target
│ ├─alsa-restore.service
│ ├─alsa-state.service
.....（中间省略）.....
│ ├─sockets.target
│ │ ├─avahi-daemon.socket
│ │ ├─dbus.socket
.....（中间省略）.....
│ ├─sysinit.target
│ │ ├─dev-hugepages.mount
│ │ ├─dev-mqueue.mount
.....（中间省略）.....
│ └─timers.target
│ └─systemd-tmpfiles-clean.timer
├─getty.target
│ └─getty@tty1.service
└─remote-fs.target
# 那么如果要查出谁会用到 multi-user.target 呢
[root@study ~]# systemctl list-dependencies --reverse
default.target
└─graphical.target
```



## systemctl 针对 service 类型的配置文件

systemd  的配置文件大部分放置于 /usr/lib/systemd/system/ ， 这里是默认的配置， 如果要修改修的位置应为/etc/systemd/system

```sh
# ll  /usr/lib/systemd/system/redis.service
-rw-r--r--. 1 root root 372 Oct 26  2018 /usr/lib/systemd/system/redis.service

# ll  /etc/systemd/system/redis.service.d/
total 4
-rw-r--r--. 1 root root 217 Oct 26  2018 limit.conf
```

在 /etc/systemd/system 下面创建与配置文件相同文件名的目录，但是要加上 .d 的扩展名。

然后在该目录下创建配置文件即可。

另外，配置文件最好附文件名取名为 .conf 较佳！ 在这个目录下的文件会“累加其他
设置”进入 /usr/lib/systemd/system/redis.service 

另外：

* /etc/systemd/system/***.service.wants/*：此目录内的文件为链接文件，设置相依服务的链接。意思是启动了 vsftpd.service 之后，最好再加上这目录下面建议的服务。
* /etc/systemd/system/vsftpd.service.requires/*：此目录内的文件为链接文件，设置相依
服务的链接。意思是在启动 vsftpd.service 之前，需要事先启动哪些服务的意思。



### 配置文件本身

```ini
[root@10.250.123.10 ~]#cat /usr/lib/systemd/system/sshd.service
[Unit]
Description=OpenSSH server daemon
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target sshd-keygen.service
Wants=sshd-keygen.service

[Service]
Type=notify
EnvironmentFile=/etc/sysconfig/sshd
ExecStart=/usr/sbin/sshd -D $OPTIONS
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target 
```

[Unit]： unit 本身的说明，以及与其他相依 daemon 的设置，包括在什么服务之后才启动此 unit 之类的设置值；
[Service], [Socket], [Timer], [Mount], [Path]..：不同的 unit type 就得要使用相对应的设置项目。
我们拿的是 sshd.service 来当范本，所以这边就使用 [Service] 来设置。 
这个项目内主要在规范服务启动的脚本、环境配置文件文件名、重新启动的方式等等。

[Install]：这个项目就是将此 unit 安装到哪个 target 里面去的意思！

细项：

#### [Unit]

| 设置参数      | 参数说明                                                     |
| ------------- | ------------------------------------------------------------ |
| Description   | 使用 systemctl list-units 时，会输出给管理员看的简易说明！当然，使用 systemctl status 输出的此服务的说明，也是这个项目 |
| Documentation | 这个项目在提供管理员能够进行进一步的文件查询的功能！提供的文件可以是如下的数据： Documentation=http://www....<br/>Documentation=man:sshd（8）<br/>Documentation=file:/etc/ssh/sshd_config |
| After         | 说明此 unit 是在哪个 daemon 启动之后才启动的意思！基本上仅是说明服务启动的顺序而已，并没有强制要求里头的服务一定要启动后此unit 才能启动。<br/>以 sshd.service 的内容为例，该文件提到 After 后面有 network.target 以及 sshd-keygen.service，但是若这两个 unit 没有启动而强制启动 sshd.service 的话， 那么 sshd.service 应该还是能够启动的！这与 Requires 的设置是有差异的喔！ |
| Before        | 与 After 的意义相反，是在什么服务启动前最好启动这个服务的意思。<br/>不过这仅是规范服务启动的顺序，并非强制要求的意思。 |
| Requires      | 明确的定义此 unit 需要在哪个 daemon 启动后才能够启动！就是设置相依服务啦！如果在此项设置的前导服务没有启动，那么此 unit 就不会被启动！ |
| Wants         | 与 Requires 刚好相反，规范的是这个 unit 之后最好还要启动什么服务比较好的意思！不过，并没有明确的规范就是了！主要的目的是希望创建让使用者比较好操作的环境。 因此，这个 Wants 后面接的服务如果没有启动，其实不会影响到这个 unit 本身！ |
| Conflicts     | 代表冲突的服务！亦即这个项目后面接的服务如果有启动，那么我们这个 unit 本身就不能启动！我们 unit 有启动，则此项目后的服务就不能启动！ 反正就是冲突性的检查啦！ |



#### [Service]
Type    ：明此 daemon 启动的方式，会影响到 ExecStart 。一般来说，有下面几种类型：
* simple：默认值，这个 daemon 主要由 ExecStart 接的指令串来启动，启动后常驻于内存中。
* notify：类似于simple，启动结束后会发出通知信号，然后 Systemd 再启动其他服务
* forking：由 ExecStart 启动的程序通过 spawns 延伸出其他子程序来作为此 daemon 的主要服务。原生的 父程序在启动结束后就会终止运行。 传统的 unit 服务大多属于这种项目，例如 httpd 这个 WWW 服务，当  httpd 的程序因为运行过久因此即将终结了，则 systemd 会再重新生出另一个子程序持续运行后， 再将父程序删除。据说这样的性能比较好！！
* oneshot：与 simple 类似，不过这个程序在工作完毕后就结束了，不会常驻在内存中。
* dbus：与 simple 类似，但这个 daemon 必须要在取得一个D-Bus 的名称后，才会继续运行！因此设置这个项目时，通常也要设置 BusName= 才行！
* idle：与 simple 类似，意思是，要执行这个daemon 必须要所有的工作都顺利执行完毕后才会执行。这类的daemon 通常是开机到最后才执行即可的服务！比较重要的项目大概是 simple, forking 与 oneshot 了！毕竟很多服务需要子程序（forking），而有更多的动作只需要在开机的时候执行一次（oneshot），例如文件系统的检查与挂载啊等等的。 

EnvironmentFile ：可以指定启动脚本的环境配置文件！例如 sshd.service 的配置文件写入到 /etc/sysconfig/sshd 当中！你也可以使用 Environment= 后面接多个不同的 Shell 变量来给予设置！ 所有的启动设置之前，都可以加上一个连词号（-），表示"抑制错误"，即发生错误的时候，不影响其他命令的执行。比如`EnvironmentFile=-/etc/sysconfig/sshd`（注意等号后面的那个连词号），就表示即使`/etc/sysconfig/sshd`文件不存在，也不会抛出错误。

Environment ：用来设置环境变量，可以使用多次：

```
[Service]
# Client Env Vars
Environment=ETCD_CA_FILE=/path/to/CA.pem
Environment=ETCD_CERT_FILE=/path/to/server.crt
```

ExecStart ：  就是实际执行此 daemon 的指令或脚本程序。你也可以使用ExecStartPre （之前） 以及 ExecStartPost （之后） 两个设置项目来在实际启动服务前，进行额外的指令行为。 但是你得要特别注意的是，指令串仅接受“指令 参数 参数...”的格式，不能接受 <, >, >>, |, &等特殊字符，很多的 bash 语法也不支持喔！ 所以，要使用这些特殊的字符时，最好直接写入到指令脚本里面去！不过，上述的语法也不是完全不能用，亦即，若要支持比较完整的 bash 语法，那你得要使用 Type=oneshot 才行喔！ 其他的 Type 才不能支持这些字符。

ExecStop：与 systemctl stop 的执行有关，关闭此服务时所进行的指令。

ExecReload ：与 systemctl reload 有关的指令行为

Restart：  当设置 Restart=1 时，则当此 daemon 服务终止后，会再次的启动此服务。举例来说，如果你在 tty2 使用文字界面登陆，操作完毕后登出，基本上，这个时候 tty2 就已经结束服务了。 但是你会看到屏幕又立刻产生一个新的 tty2 的登陆画面等待你的登陆！那就是 Restart的功能！除非使用 systemctl 强制将此服务关闭，否则这个服务会源
源不绝的一直重复产生！

RemainAfterExit：当设置为 RemainAfterExit=1 时，则当这个 daemon 所属的所有程序都终止之后，此服务会再尝试启动。这对于 Type=oneshot 的服务很有帮助！

TimeoutSec：若这个服务在启动或者是关闭时，因为某些缘故导致无法顺利“正常启动或正常结束”的情况下，则我们要等多久才进入“强制结束”的状态！

KillMode：可以是 process, control-group, none 的其中一种，如果是 process则 daemon 终止时，只会终止主要的程序 （ExecStart 接的后面那串指令），如果是 control-group 时， 则由此 daemon 所产生的其他control-group 的程序，也都会被关闭。如果是 none 的话，则没有程序会被关闭喔！mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号

- control-group（默认值）：当前控制组里面的所有子进程，都会被杀掉
- process：只杀主进程
- mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号
- none：没有进程会被杀掉，只是执行服务的 stop 命令。

RestartSec：与 Restart 有点相关性，如果这个服务被关闭，然后需要重新启动时，大概要 sleep 多少时间再重新启动的意思。默认是 100ms （毫秒）。

- no（默认值）：退出后不会重启
- on-success：只有正常退出时（退出状态码为0），才会重启
- on-failure：非正常退出时（退出状态码非0），包括被信号终止和超时，才会重启
- on-abnormal：只有被信号终止和超时，才会重启
- on-abort：只有在收到没有捕捉到的信号终止时，才会重启
- on-watchdog：超时退出，才会重启
- always：不管是什么退出原因，总是重启

PIDFile: 守护进程的PID文件，必须是绝对路径。 强烈建议在 `Type=forking` 的情况下明确设置此选项。 systemd 将会在此服务启动后从此文件中读取主守护进程的PID 。 systemd 不会写入此文件， 但会在此服务停止后删除它(若存在)。

WorkingDirectory=/home， 设置工作路径， 但是各种选项里仍然要写全路径

PrivateTmp=True       # 是否分配独立的临时空间（缺省） 

StandardOutput=syslog+console
StandardError=syslog+console

日志输出，其实这也是默认值




#### [Install]

WantedBy:  这个设置后面接的大部分是 *.target unit ！意思是，这个 unit 本身是附挂在哪一个 target unit 下面的！一般来说，大多的服务性质的 unit 都是附挂在multi-user.target 下面！
Also:  当目前这个 unit 本身被 enable 时，Also 后面接的 unit 也请 enable 的意思！也就是具有相依性的服务可以写在这里呢！
Alias : 进行一个链接的别名的意思！当 systemctl enable 相关的服务时，则此服务会进行链接文件的创建！以 multi-user.target 为例，这个家伙是用来作为默认操作环境 default.target 的规划， 因此当你设置用成 default.target时，这个 /etc/systemd/system/default.target 就会链接到/usr/lib/systemd/system/multi-user.target 啰！



ps: http://www.jinbuguo.com/systemd/systemd.directives.html, 一位老哥翻译的各种参数，厉害。



#### 自定义服务配置

尝试了下自己定义mongo的启动：

/etc/systemd/system/test.mongod.service:

```ini
[Unit]
Description=MongoDB Database Server
Documentation=https://docs.mongodb.org/manual
After=network.target

[Service]
User=mongod
Group=mongod
Environment="OPTIONS=-f /**/opt/mongodb/mongod.conf"
EnvironmentFile=-/etc/sysconfig/mongod
ExecStart=/***/opt/mongodb/bin/mongod $OPTIONS

ExecStartPre=/usr/bin/mkdir -p /***/opt/mongodb/data /***/opt/mongodb/log
ExecStartPre=/usr/bin/chown -R mongod:mongod /***/opt/mongodb/data /***/opt/mongodb/log
ExecStartPre=/usr/bin/chmod -R 0755 /***w/opt/mongodb/


PermissionsStartOnly=true  #  这里目前还不知什么意思
PIDFile=/***/opt/mongodb/mongod.pid

Type=forking

# file size
LimitFSIZE=infinity
# cpu time
LimitCPU=infinity
# virtual memory size
LimitAS=infinity
# open files
LimitNOFILE=64000
# processes/threads
LimitNPROC=64000
# locked memory
LimitMEMLOCK=infinity
# total threads (user+kernel)
TasksMax=infinity
TasksAccounting=false
# Recommended limits for for mongod as specified in
# http://docs.mongodb.org/manual/reference/ulimit/#recommended-settings

[Install]
WantedBy=multi-user.target
```



#### 注意事项

1. systemctl 配置文件修改后要记得： systemctl daemon-reload ， 重新载入配置文件

2. 配置文件里不能通过变量名获取一些变量：`Environment="PATH=/local/bin:$PATH"`

   但是可以这样： `ExecStart=/bin/bash -c 'PATH=/new/path:$PATH exec /bin/mycmd arg1 arg2'`

   或者这样：`Environment=PATH=/home:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`


