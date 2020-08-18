---
title: "Rocksdb安装.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["Nosql"]
author: "Claymore"

---


环境： centos7

install make:

`apt-get build-essential`

` yum groupinstall "Development Tools"`  # 这个很重要，解决了各种gcc的问题。



install cmake :

https://cmake.org/install/

or： https://www.heliocastro.info/?p=238(没试）



### leveldb

https://github.com/google/leveldb

文档： https://leveldb.org.cn/index.html



**可以直接安装pip中的leveldb:**

`pip install leveldb`

Making a clean slate:

```
import leveldb   leveldb.DestroyDB('./db') db = leveldb.LevelDB('./db')
```

Hello world:

```
db.Put('hello', 'world') # persisted to disc print db.Get('hello')
```



### Rocksdb

github: https://github.com/facebook/rocksdb/

安装前提：https://github.com/facebook/rocksdb/blob/master/INSTALL.md

一个centos7的官方安装脚本：https://github.com/facebook/rocksdb/blob/master/java/crossbuild/build-linux-centos.sh

安装devtoolset 那里可以跳过。

rocks的编译安装：https://blog.csdn.net/weixin_38976558/article/details/91616093



```sh
[root@10.250.123.10 rocksdb]#make static_lib
$DEBUG_LEVEL is 0
  GEN      util/build_version.cc
$DEBUG_LEVEL is 0
  GEN      util/build_version.cc
  CC       util/build_version.o
  AR       librocksdb.a
ar: creating librocksdb.a
[root@10.250.123.10 rocksdb]#make install-static
$DEBUG_LEVEL is 0
  GEN      util/build_version.cc
install -d /usr/local/lib
for header_dir in `find "include/rocksdb" -type d`; do \
        install -d /usr/local/$header_dir; \
done
for header in `find "include/rocksdb" -type f -name *.h`; do \
        install -C -m 644 $header /usr/local/$header; \
done
install -C -m 755 librocksdb.a /usr/local/lib

# 动态 make shared_lib
ln -fs librocksdb.so.6.4.0 librocksdb.so
ln -fs librocksdb.so.6.4.0 librocksdb.so.6
ln -fs librocksdb.so.6.4.0 librocksdb.so.6.4


[root@10.250.123.10 rocksdb]#make install-shared
$DEBUG_LEVEL is 0
  GEN      util/build_version.cc
install -d /usr/local/lib
for header_dir in `find "include/rocksdb" -type d`; do \
        install -d /usr/local/$header_dir; \
done
for header in `find "include/rocksdb" -type f -name *.h`; do \
        install -C -m 644 $header /usr/local/$header; \
done
install -C -m 755 librocksdb.so.6.4.0 /usr/local/lib && \
        ln -fs librocksdb.so.6.4.0 /usr/local/lib/librocksdb.so.6.4 && \
        ln -fs librocksdb.so.6.4.0 /usr/local/lib/librocksdb.so.6 && \
        ln -fs librocksdb.so.6.4.0 /usr/local/lib/librocksdb.so

```

此时 /usr/local/lib 中已经有librocks.db.a

ll /usr/local/lib:

```
-rwxr-xr-x 1 root root 475874942 Aug 20 12:05 librocksdb.a
lrwxrwxrwx 1 root root        19 Aug 20 12:18 librocksdb.so -> librocksdb.so.6.4.0
lrwxrwxrwx 1 root root        19 Aug 20 12:18 librocksdb.so.6 -> librocksdb.so.6.4.0
lrwxrwxrwx 1 root root        19 Aug 20 12:18 librocksdb.so.6.4 -> librocksdb.so.6.4.0
-rwxr-xr-x 1 root root 145895920 Aug 20 12:18 librocksdb.so.6.4.0
```

注意这里是不是全的。

**重要：**

`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib`

source一下



### pyrocksdb

文档：https://pyrocksdb.readthedocs.io/en/latest/installation.html

```python
pyrocksdb安装：
sudo pip install "Cython>=0.20"
sudo pip install git+git://github.com/stephan-hof/pyrocksdb.git@v0.2.1

至些安装成功
进入pyrocksdb环境

jerry@hq:/u01/rocksdb$ python
Python 2.7.3 (default, Sep 26 2013, 20:03:06)
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import rocksdb
>>> db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
>>> db.put(b"key1", b"v1") 
>>> db.put(b"key2", b"v2")
>>> db.get(b"key1")
'v1'

```



### python-rocksdb

上面的库有很久没有更新，这个库是支持最新版本的rocksdb

https://github.com/twmht/python-rocksdb

pip install pyhton-rocksdb

**注意，只有安装了rocksdb，这个库才可以安装成功，因为它需要rocksdb产出的动静编译包。**

```python
>>> import rocksdb
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.7/site-packages/rocksdb/__init__.py", line 1, in <module>
    from ._rocksdb import *
ImportError: librocksdb.so.6.4: cannot open shared object file: No such file or directory
```

这就是没有执行上面导出环境变量的操作



导出后测试：

```python
>>> import rocksdb
>>> db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
>>> db.put(b'a', b'data')
>>> print db.get(b'a')
data
```

此时当前文件夹下多了个test.db