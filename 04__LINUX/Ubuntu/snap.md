---
title: "snap.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: true
tags: [""]
categories: ["linux"]
author: "Claymore"

---
### 问题



#### /dev/loop , /snap 目录占用满了

大致情况如下：

``` sh
root@node200:~/# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           798M  1.4M  797M   1% /run
/dev/sda1        63G   19G   41G  32% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
/dev/loop0       13M   13M     0 100% /snap/gnome-characters/103
/dev/loop5       15M   15M     0 100% /snap/gnome-logs/37
/dev/loop3      141M  141M     0 100% /snap/gnome-3-26-1604/70
/dev/loop6      2.4M  2.4M     0 100% /snap/gnome-calculator/180
/dev/loop1      3.8M  3.8M     0 100% /snap/gnome-system-monitor/51
/dev/loop2       35M   35M     0 100% /snap/gtk-common-themes/319
/dev/loop4       87M   87M     0 100% /snap/core/4917
tmpfs           798M   28K  798M   1% /run/user/121
tmpfs           798M     0  798M   0% /run/user/0
```

需要下载清理工具：

```
sudo apt purge snapd ubuntu-core-launcher squashfs-tools
```

下载后：

```
root@node200:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           798M  1.4M  797M   1% /run
/dev/sda1        63G   19G   42G  32% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
tmpfs           798M   28K  798M   1% /run/user/121
tmpfs           798M     0  798M   0% /run/user/0
```



参考：https://askubuntu.com/questions/990013/system-mounts-dev-loop0-on-snap-core-3604-and-its-100-full-where-is-it-comi