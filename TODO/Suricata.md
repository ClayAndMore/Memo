 [https://www.maliciouskr.cc/2019/06/22/%E4%BD%BF%E7%94%A8Suricata%E6%9E%84%E5%BB%BA%E7%BD%91%E7%BB%9C%E5%B1%82%E5%85%A5%E4%BE%B5%E6%A3%80%E6%B5%8B/](https://www.maliciouskr.cc/2019/06/22/使用Suricata构建网络层入侵检测/) 



## 安装

官方安装文档：https://redmine.openinfosecfoundation.org/projects/suricata/wiki/suricata_installation

### 源码：

https://www.openinfosecfoundation.org/download/

```sh
# 下载
wget https://www.openinfosecfoundation.org/download/suricata-5.0.3.tar.gz

```



### 依赖

ubuntu:

```sh
apt -y install libpcre3 libpcre3-dbg libpcre3-dev build-essential autoconf \
automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev \
libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev libjansson4 pkg-config
```

默认是ids, 如果你需要ips的功能，还需要安装：

```
apt -y install libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0
```



centos:

```sh
yum install epel-release # epel 源
yum -y install gcc libpcap-devel pcre-devel libyaml-devel file-devel \
zlib-devel jansson-devel nss-devel libcap-ng-devel libnet-devel tar make \
libnetfilter_queue-devel lua-devel
```



### 解压和安装

下载好源码后，我们解压安装

``` sh
tar -xvzf suricata-4.1.3.tar.gz
cd  suricata-4.1.3

# 如果这步出错，基本上是因为少安装了包，根据提示搜索安装即可
./configure  --prefix=/usr --sysconfdir=/etc --localstatedir=/var  --enable-nfqueue 

make 
make install-conf # 将执行常规的“make install”，然后它将为你自动创建/设置所有必要的目录和suricata.yaml
make install 

ldconfig
```

常见的配置选项说明:

* --prefix=/usr/  ： 将Suricata二进制文件安装到/usr/bin/中,默认/usr/local/
* --sysconfdir=/etc ： 将Suricata配置文件安装到/etc/ Suricata /中。默认/usr/local/etc/
* --localstatedir=/var：将Suricata日志记录到/var/log/ Suricata /中。默认/usr/local/var/log/suricata
* --enable-lua ： 启用Lua支持检测和输出。
* --enable-geopip：启用对检测的GeoIP支持。
* --disable-rust：禁用Rust支持。如果rustc/cargo可用，则默认启用Rust支持
* --disable-gccmarch-native: 不要为构建二进制文件的硬件优化二进制文件。如果二进制文件是可移植的，或者Suricata要在VM中使用，则添加此标志
* --enable-nfqueue : 如果开启ips能力，需要开启此项



## 配置文件

默认的配置文件在：/etc/suricata/suricata.yaml

相关字段解释： https://www.osgeo.cn/suricata/output/eve/eve-json-output.html#eve-json-output，

英文原版： https://suricata.readthedocs.io/en/latest/configuration/suricata-yaml.html#event-output

自己翻译：

### default-log-dir

``` yaml
default-log-dir: /var/log/suricata # 所有suricata的输出都会在这个文件夹下。
# 该参数可以被命令行重写：
suricata -c suricata.yaml -i eth0 -l /var/log/suricata-logs/

# 所有日志文件
# ls /var/log/suricata/
certs  eve.json  fast.log  files  stats.log  suricata.log
```

### stats

引擎统计数据(如包计数器、内存使用计数器等)可以以多种方式记录。默认情况下，将启用单独的文本日志stats.log

``` yaml
stats:
  enabled: yes
  # The interval field (in seconds) controls at what interval
  # the loggers are invoked.
  interval: 8
  # Add decode events as stats.
  #decoder-events: true
  # Decoder event prefix in stats. Has been 'decoder' before, but that leads
  # to missing events in the eve.stats records. See issue #2225.
  #decoder-events-prefix: "decoder.event"
  # Add stream events as stats.
  #stream-events: false
```

enabled 是否启用

interval, 统计数据按时间间隔转储，将这个时间设置在3或4秒以下是没有用的，因为线程是在内部同步的。 



### outputs









## 问题



###  error while loading shared libraries: libhtp.so.2: cannot open shared object file: No such file or directory

``` sh
suricata -c /etc/suricata/suricata.yaml -i ens192 --init-errors-fatal

suricata: error while loading shared libraries: libhtp.so.2: cannot open shared object file: No such file or directory
```

安装完后忘记运行：

ldconfig