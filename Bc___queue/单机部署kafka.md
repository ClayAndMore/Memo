### 下载和配置java

去官网下载 https://www.java.com/zh_CN/download/manual.jsp

mkdir -p /opt/module

tar xvfz dk-8u211-linux-x64.tar.gz -C /opt/module



添加环境变量：

```shell
vim /etc/profile
export JAVA_HOME=/opt/module/jdk1.8.0_211
export PATH=$PATH:$JAVA_HOME/bin

# 使环境变量生效
source /etc/profile

# 验证：
[root@node101 ~]# java -version
java version "1.8.0_211"
Java(TM) SE Runtime Environment (build 1.8.0_211-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.211-b12, mixed mode)
```

   