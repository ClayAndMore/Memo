都是在centos7上实验的



install make:

`apt-get build-essential`

` yum groupinstall "Development Tools"`





install cmake :

https://cmake.org/install/

or： https://www.heliocastro.info/?p=238(没试）





leveldb:

https://github.com/google/leveldb

文档： https://leveldb.org.cn/index.html



**可以直接安装pip中的leveldb:**

```
`pip install leveldb`
```

Making a clean slate:

```
`import leveldb   leveldb.DestroyDB('./db') db = leveldb.LevelDB('./db')`
```

Hello world:

```
`db.Put('hello', 'world') # persisted to disc print db.Get('hello')`
```



### Rocksdb

github: https://github.com/facebook/rocksdb/

安装前提：https://github.com/facebook/rocksdb/blob/master/INSTALL.md

rocks的编译安装：http://hysky.cc/2018/10/14/rocksdb%E7%9A%84%E7%BC%96%E8%AF%91%E5%AE%89%E8%A3%85/



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

