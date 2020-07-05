---
title: "question.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[linux]

#### rm后的文件恢复

`grep -a -B 50 -A 60 'some string in the file' /dev/sda1 > results.txt`

说明：

- 关于grep的-a意为–binary-files=text，也就是把二进制文件当作文本文件。
- -B和-A的选项就是这段字符串之前几行和之后几行。
- /dev/sda1，就是硬盘设备，
- \> results.txt，就是把结果重定向到results.txt文件中。



#### cannot remove Read-only file system 后尝试修复磁盘

先尝试看下目录权限：

` *cat /proc/mounts`

给与写权限：

` mount -o remount rw /disk`



文件系统扫描工具有fsck、fsck.ext2、fsck.ext3、fsck.ext4、fsck.msdos、fsck.cramfs、fsck.ext4dev、fsck.vfat。最好是根据不同的文件系统来调用不同的扫描工具，比如ext3的文件系统使用fsck.ext3，ext4文件系统使用fsck.ext4等。

```
[root@node44 ~]# fsck -y /dev/sdb1
fsck from util-linux-ng 2.17.2
e2fsck 1.41.12 (17-May-2010)
/dev/sdb1 is mounted.
e2fsck: Cannot continue, aborting.
```

umount掉 /dev/sdb的挂载盘，提示buzy, 查看那个使用该挂载目录的进程：

```
[root@node44 ~]# lsof | grep /disk
udp_knock  2363      root    1w      REG               8,17          0   57409571 /disk/ng8w/var/log/shell_udp_knock.log (deleted)
[root@node44 ~]# kill -9 2363
[root@node44 ~]# umount /dev/sdb1
```

 再次修复：

```
[root@node44 ~]# fsck -y /dev/sdb1
fsck from util-linux-ng 2.17.2
e2fsck 1.41.12 (17-May-2010)
fsck.ext4: Attempt to read block from filesystem resulted in short read while trying to open /dev/sdb1
Could this be a zero-length partition?
```

及一次文件系统损坏的修复： https://blog.csdn.net/xiefp/article/details/50290891



### 待补充

```
/proc/pid/cmdline
```



rsync