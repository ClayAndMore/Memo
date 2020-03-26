Docker网络模式介绍

  Docker在创建容器时有四种网络模式：bridge/host/container/none，bridge为默认不需要用--net去指定，其他三种模式需要在创建容器时使用--net去指定

 

  **1.bridge****模式(****默认模式)**

   docker run时使用--net=bridge，这种模式会为每个容器分配一个独立的Network Namespace,

   同一个宿主机上的所有容器会在同一个网段下，相互之间是可以通信的

 

   注1：bridge为默认模式，不需要使用参数--net去指定，使用了--net参数反而无效

   注2：bridge模式无法指定容器IP(但非绝对

 

  **2.host****模式**

   docker run时使用--net=host，容器将不会虚拟出IP/端口，而是使用宿主机的IP和端口

 

   docker run -itd --net=host 961769676411

 

   注1：host模式不能使用端口映射和自定义路由规则，这些都与主机一致，-p 与-icc 参数是无效的

 

**外部访问docker****容器**

  **1.bridge****模式**

   docker run -itd -p 7101:7101 镜像ID

   \## -p参数可以出现多次，     

   docker run -itd -p 8080:8080 -p 8088:8088 镜像ID

实例：docker run -di --name mytomcat -p 8081:8080 镜像ID

  http:192.168.198.146：8081

 

  **2.host****模式**

   docker run -itd --net=host 镜像ID

实例：docker run -di --name mytomcat03 --net=host 镜像ID

 http:192.168.198.146：8080

   注1：不需要添加-p参数，因为它使用的就是主机的IP和端口，添加-p参数后，反而会出现以下警告：

​     WARNING: Published ports are discarded when using host network mode

   注2：宿主机的ip路由转发功能一定要打开，否则所创建的容器无法联网！

​     echo 1 > /proc/sys/net/ipv4/ip_forward





1.host模式下是怎么占领端口的？
host模式端口占用模式是你的容器占用你主机上当前所监听的端口(官网描述为publish)，比如我们都知道tomcat占用8080端口，那么当我们用host模式启动的时候，主机上的8080端口会被tomcat占用，这个时候其他的容器就不能指定我们的8080端口了，但是可以指定其他端口，所以说一台主机上可以运行多个host模式的容器，只要彼此监听的端口不一样就行。

2.host模式下使用-p或者-P会出现WARNING: Published ports are discarded when using host network mode
当你是host模式的时候，主机会自动把他上面的端口分配给容器，这个时候使用-p或者-P是无用的。但是还是可以在Dockerfile中声明EXPOSE端口
