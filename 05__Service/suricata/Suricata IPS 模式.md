
---
title: "Suricata IPS 模式.md"
date: 2020-06-22 14:45:42 +0800
lastmod: 2020-06-22 14:45:42 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "Suricata.md"
date: 2020-06-16 18:00:43 +0800
lastmod: 2020-06-16 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

### 确保  ips 可以使用 NFQ

1. 安装 netfilter 包：

   ```
   apt-get -y install libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0
   ```

2. configure suricata 时 带上 `--enable-nfqueue` option. （apt install suricat 时默认是开启此选项的，我们可以不用编译安装）

3. 编译安装


### 配置

配置 iptables

扫描桥接的数据包：`iptables -I FORWARD -j NFQUEUE`

标记的包才进nfq,(use `repeat` Suricata `NFQ` mode) 

`iptables -I FORWARD -m mark ! --mark $MARK/$MASK -j NFQUEUE`

在 suricata.yaml 中配置 NFQ mode:

``` yaml
##
## Netfilter integration
##

# When running in NFQ inline mode, it is possible to use a simulated
# non-terminal NFQUEUE verdict.
# This permit to do send all needed packet to Suricata via this a rule:
#        iptables -I FORWARD -m mark ! --mark $MARK/$MASK -j NFQUEUE
# And below, you can have your standard filtering ruleset. To activate
# this mode, you need to set mode to 'repeat'
# If you want packet to be sent to another queue after an ACCEPT decision
# set mode to 'route' and set next-queue value.
# On linux >= 3.1, you can set batchcount to a value > 1 to improve performance
# by processing several packets before sending a verdict (worker runmode only).
# On linux >= 3.6, you can set the fail-open option to yes to have the kernel
# accept the packet if Suricata is not able to keep pace.
# bypass mark and mask can be used to implement NFQ bypass. If bypass mark is
# set then the NFQ bypass is activated. Suricata will set the bypass mark/mask
# on packet of a flow that need to be bypassed. The Nefilter ruleset has to
# directly accept all packets of a flow once a packet has been marked.
nfq:
#  mode: accept    # nfq mode: accept, repeat, route
#  repeat-mark: 1  # used for repeat mode to mark a packet
#  repeat-mask: 1  # used for repeat mode to mark a packet
#  bypass-mark: 1
#  bypass-mask: 1
#  route-queue: 2  # for ‘route’ mode
#  batchcount: 20  # max length of a batching verdict cache
#  fail-open: yes  # a packet is accepted when queue is full
```

nfq 的几种模式：

``` sh
Accept
# 默认 NFQ mode, Suricata 生成一个决断: pass or drop. 包不会被其余的iptables规则审查。

Repeat
# Suricata 生成一个非最终决断并 mark the packets that will be reinjected again at the first rule of iptables. Add the following rule to iptables:
 iptables -I FORWARD -m mark ! --mark $MARK/$MASK -j NFQUEUE
Route
To send a packet to another queue after an ACCEPT decision, set mode to route and set route-queue value. Use a route mode to scan packets with multiple network scanners on the same VM.
```



##