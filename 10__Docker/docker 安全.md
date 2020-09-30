---
title: "docker 安全.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
### gosu

gosu是个工具，用来提升指定账号的权限，作用与sudo命令类似，而docker中使用gosu的起源来自安全问题；

docker容器中运行的进程，如果以root身份运行的会有安全隐患，该进程拥有容器内的全部权限，更可怕的是如果有数据卷映射到宿主机，那么通过该容器就能操作宿主机的文件夹了，一旦该容器的进程有漏洞被外部利用后果是很严重的。
https://github.com/tianon/gosu 



## 容器逃逸

https://wohin.me/rong-qi-tao-yi-gong-fang-xi-lie-yi-tao-yi-ji-zhu-gai-lan/

### 检测容器环境

1. 检查`/.dockerenv`文件是否存在；
2. 检查`/proc/1/cgroup`内是否包含`"docker"`等字符串；
3. 检查是否存在`container`环境变量。



### 危险配置

 --privileged特权模式

默认带的白名单：

``` sh
func DefaultCapabilities() []string {
	return []string{
		"CAP_CHOWN",
		"CAP_DAC_OVERRIDE",
		"CAP_FSETID",
		"CAP_FOWNER",
		"CAP_MKNOD",
		"CAP_NET_RAW",
		"CAP_SETGID",
		"CAP_SETUID",
		"CAP_SETFCAP",
		"CAP_SETPCAP",
		"CAP_NET_BIND_SERVICE",
		"CAP_SYS_CHROOT",
		"CAP_KILL",
		"CAP_AUDIT_WRITE",
	}
}
```





### 危险挂载

* 挂载 docker sock 到容器内部，容器内安装docker客户端，导致可以操作主机的容器环境，建立一个特权容器然后挂载宿主机根目录，再chroot拿到权限

* 挂载procfs, /proc/sys/kernel/core_pattern

  



### 程序漏洞

runc : CVE-2019-5736



### 内核漏洞

脏牛， CVE-2016-5195





## Seccomp

https://docs.docker.com/engine/security/seccomp/



## docker安全基线

https://yangrz.github.io/blog/2018/04/13/docker/

https://github.com/Kutim/docker-security/blob/master/docker%E5%9F%BA%E7%BA%BF.md

https://github.com/aquasecurity/kube-bench

华为：https://support.huaweicloud.com/usermanual-cgs/cgs_01_0052.html