---
title: "kvm-网络模式.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---




### 创建  NAT 网络模式

确认 ip forwarding 打开：t.

```sh
# this needs to be "1"
cat /proc/sys/net/ipv4/ip_forward
# 没有打开的话：
sudo sysctl -w net.ipv4.ip_forward=1
# 永久设置：
vim /etc/sysctl.conf
net.ipv4.ip_forward=1
```

https://fabianlee.org/2019/05/26/kvm-creating-a-guest-vm-on-a-nat-network/