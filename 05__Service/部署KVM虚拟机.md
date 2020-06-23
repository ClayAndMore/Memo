
---
title: "部署KVM虚拟机.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "部署KVM虚拟机.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
环境： [CentOS] 版本：64位 7.2  1511 

### 安装KVM

验证CPU是否支持KVM, 输出结果中有vmx(intel) 或svm(AMD)字样，就说明CPU的支持的。

```shell
[root@192.168.18.198 ~]#egrep '(vmx|svm)' /proc/cpuinfo
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch epb cat_l3 cdp_l3 intel_pt tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm rdt_a rdseed adx smap xsaveopt cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts
```



关闭SELinux 

把 /etc/sysconfig/selinux 中改为： `SELinux=disabled `

一些必要的包：`yum install epel-release net-tools vim unzip zip wget ftp -y`



安装KVM及其依赖项

`yum install qemu-kvm libvirt virt-install bridge-utils -y`

验证：

`lsmod | grep kvm`

 开启kvm服务，并且设置其开机自动启动:

`systemctl start libvirtd`

`systemctl enable libvirtd`

验证： `systemctl status libvirtd`

网桥模式(卡住):

https://www.chenyudong.com/archives/libvirt-kvm-bridge-network.html

<https://www.linuxidc.com/Linux/2017-01/140007.htm>

<https://blog.csdn.net/hzhsan/article/details/44098537/>



安装brctl

`apt-get install bridge-utils`

`yum install bridge-utils`

