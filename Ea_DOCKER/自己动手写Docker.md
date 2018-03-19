## 自己动手写Docker



我们经常听到docker是一个使用了Linux Namespace 和 Cgroups 的虚拟化工具。

### Linux Namespace

* 一个Kernel 的功能
* 将资源隔离， 资源包括进程树， 网络接口，挂载点等。
* linux 一共 有六种不同类型的Namespace.


#### User Namespace

可以做到UID级别的隔离，也就是说，可以以UID为n的用户虚拟化出来一个Namespace,在这个Namespace里面，用户是有root权限的，但在真实的物理机上，他还是以为那个以UID为n的用户。



#### PID Namespace 

每个被虚拟的空间，都有自己pid为1的init进程，这个init进程在父空间（也就是真实机器）中有对应的id.



#### UTS Namespace



#### IPC Namespace



#### Mount Namespace



#### Network Namespace





### Linux Cgroups



