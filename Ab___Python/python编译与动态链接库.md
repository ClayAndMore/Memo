## python编译 和 动态链接库



#### pyc, pyo, pyd

* pyc  是 py文件经过python 的 编译器 得到的 字节码(bytecode),  pyc文件通过python的解释器变成机器代码,去执行.

* pyo文件,是python编译优化后的字节码文件, 这个优化没有多大作用,只是移除了断言。

  生成方式: `python -O -m py_compile xxxx.py `

* pyd 是动态链接库文件, 在windows上为dll,  linux下为so.  

  一般是其他语言写的python库, 多为c/c++综合而成的D语言. 比如select库.



pyc 和 pyo 对比py的速度比较:

```

```

其实运行速度是不会改变的,只是加载速度会变快一点, import的时候会先找pyc





#### 动态链接库

