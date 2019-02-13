### Linux Cgroups

上面说的是隔离，但是怎么限制每个每个隔离的空间大小，保证他们之间不会互相争抢呢。

Linu x Cgroups(Control Groups)  ， 可以方便的限制某个进程的资源占用，并且可以实时的监控进程和统计信息。

#### Cgroups 中的三个组件：

- cgroup 

  是进程分组管理的一种机制，一个cgroup包含一组**进程**，并且可以在其增加linux subsystem 的各种参数配置。

- subsystem 

  是对一组进程资源控制的模块，一般包含：

  - 对设置（如硬盘）的输入输出访问控制
  - cpu的调度策略，占用，尺寸
  - 进程挂起，恢复，网络流量， 优先级，监控

- hierarchy

  把一组cgroup变成一个树状的结构，可以让其拥有继承功能。

三个组件的关系：

 一个hierarchy 可以有很多subsystem, 一个subsystem只能附加到一个hierarchy上。

一个进程可以作为多个cgroup的成员，但是这些cgroup必须在不同的hierarchy上。

一个进程fork出子进程时，子进程是和父进程在同一个cgroup中的，也可以移动到其他cgroups。

![](https://github.com/ClayAndMore/MyImage/blob/master/docker/cgroup.png?raw=true)

 整体一个cgroup, 红色的是两个subsystem(资源管理器)，蓝色框里是一个hierarchy.



#### kernel 接口

Kernel 怎样才能配置Cgroups?

1. 创建一个hierarchy(cgroup树)， 如下：

   ```
   mkdir cgroup-test # 创建一个hierarchy挂载点
   c # 挂载一个hierarchy
   ls ./cgroup-test/
   cgroup.clone_children  cgroup.procs          notify_on_release  tasks
   cgroup.event_control   cgroup.sane_behavior  release_agent
   
   ```

   这些文件就是这个hierarchy中cgroup根节点的配置项：

   - Cgroup.clone_children, cpuset 的 subsystem 会读取这个配置文件，如果其值为1（默认0），子cgroup才会继承父 cgroup 的 cpuset 的配置
   - Cgroup.procs 树当前节点 cgroup 中的进程组ID, 现在的位置是在根节点，这个文件中会有现在系统中所有进程组的ID
   - Notify_on_release 和 release_agent会一起使用， notify_on_release 标识当这个cgroup最后一个进程退出的时候是否执行类release_agent.
   - Release_agent 则是一个路径，通常用作进程退出之后自动清理掉不再使用的cgroup.
   - Tasks 标识该 cgroup 下面的进程ID, 如果吧一个进程ID写到tasks文件中， 便会将相应的进程加入到这个cgroup中。

2. 创建子文件

   ```
   cd cgroup-test
   mkdir cgroup-1 # 创建子cgroup 
   mkdir cgroup-2 # 创建子cgroup
   [root@claymore cgroup-test]# tree
   .
   |-- cgroup-1
   |   |-- cgroup.clone_children
   |   |-- cgroup.event_control
   |   |-- cgroup.procs
   |   |-- notify_on_release
   |   `-- tasks
   |-- cgroup-2
   |   |-- cgroup.clone_children
   |   |-- cgroup.event_control
   |   |-- cgroup.procs
   |   |-- notify_on_release
   |   `-- tasks
   |-- cgroup.clone_children
   |-- cgroup.event_control
   |-- cgroup.procs
   |-- cgroup.sane_behavior
   |-- notify_on_release
   |-- release_agent
   `-- tasks
   ```

   在一个cgroup的目录下创建文件夹时， Kernel会把文件夹标记为这个cgroup的子crgroup, 并继承父的属性。

3. 添加和移动进程

   系统所有的进程都会默认在根节点上存在， 可以将进程移动到其他cgroup节点，只需要将进程ID写到tasks文件即可。

   ```shell
   [root@claymore cgroup-test]# cd cgroup-1
   [root@claymore cgroup-1]# echo $$
   21303
   [root@claymore cgroup-1]# cat tasks
   [root@claymore cgroup-1]# sh -c "echo $$ >> tasks"
   [root@claymore cgroup-1]# cat tasks
   21303
   21527   #估计是进程
   [root@claymore cgroup-1]# cat /proc/21303/cgroup
   12:name=cgroup-test:/cgroup-1 #可以看到当前的进程被添加到这里了
   11:memory:/
   10:freezer:/
   9:blkio:/
   8:hugetlb:/
   7:cpuset:/
   6:devices:/
   5:net_prio,net_cls:/
   4:perf_event:/
   3:pids:/
   2:cpuacct,cpu:/
   1:name=systemd:/user.slice/user-0.slice/session-260327.scope
   ```

4. 通过subsystem 限制cgroup中进程的资源。

   上面创建的hierarchy没有关联到任何的subsystem。

   系统默认已经为每个 subsystem 创建了一个默认的 hierarchy ，比如 memory 的 hierarchy:

   ```shell
   [root@claymore cgroup-1]# mount | grep memory
   cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
   ```

   进行如下操作：

   ```shell
   cd /sys/fs/cgroup/memory
   # 开启一个占用200M内存的stress进程，没有可yum install stress
   stress --vm-bytes 200m --vm-keep -m 1 &
   top 看内存。
   [root@claymore memory]# mkdir test-limit-memory
   [root@claymore memory]# cd test-limit-memory/
   # 设置最大cgroup的在最大内存占用为100MB
   [root@claymore test-limit-memory]# sh -c "echo "100m" > memory.limit_in_bytes"
   [root@claymore test-limit-memory]# cat memory.limit_in_bytes
   104857600
   [root@claymore test-limit-memory]# sh -c "echo $$ > tasks"
   [root@claymore test-limit-memory]# cat tasks
   21303
   24884
   [root@claymore test-limit-memory]# stress --vm-bytes 200m --vm-keep -m 1 &
   [1] 24902
   ```

   发现再次使用200m起不来，用99M可以起来。



   内存：

   共2G，

```shell
   限制前： 2*10.9 = 200M
     PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
   23743 root      20   0  212112 204932    124 R 99.7 10.9   1:12.12 stress
       1 root      20   0  125484   3052   1724 S  0.0  0.2  38:19.25 systemd
       
   限制后： 2*5.4 = 100M
    PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
   25589 root      20   0  108688 101448    124 R 97.0  5.4   0:22.88 stress
    7900 mongod    20   0  985036  35232   2388 S  0.7  1.9 110:42.32 mongod
```









#### Docker 如何使用Cgroups

```
cd /sys/fs/cgroup/memory/docker/<id> 
cat memory.limit_in_bytes  # 看cgroup的内存限制
cat memory.usage_in_bytes  # 查看cgroup中进程所使用的内存大小
```

可以看到， Docker通过为每个容器创建cgroup配置资源限制和资源控制。



#### Go实现对cgroup限制容器的资源





