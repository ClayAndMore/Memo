# Ab___Python
## bottle.md
## Bottle
### 启动
### 关于请求
### 动态路由
### 静态文件
### 错误页面
### URL转向
### 为客户端返回不同的数据类型
### header
### cookie
### 添加cookie
### 加密cookie
### 中文cookie
### 文件上传
### 内建模版引擎
## 传递html代码
### 部署
### 实践出真知
### 问题
### Broken pip
## csv.md
### to be a dict
### read a single line
## logging.md
### 简单demo
### 几个概念
###  Logger记录器
### Handler处理器
### Filter过滤器
### 基础配置
### 配置方式
### 继承方式
### logging的继承
## main.py
## coding=utf-8
## util.py
### logger的继承
### 配置输出流
### 进阶
### 格式输出：
### 异常处理
### 输出到控制台并输出到文件
## coding=utf-8
## 第一步，创建一个logger
## 第二步，创建一个handler，用于写入日志文件
## 第三步，再创建一个handler，用于输出到控制台
## 第四步，定义handler的输出格式
## 第五步，将logger添加到handler里面
## 日志
## pandas.md
## PyPy.md
## PyPy
### 安装
## origin to know
### 编译型 or 解释型
### 动态 or 静态
### 强类型 or 弱类型
### JIT
## pyqt尝试.md
## pyqt尝试
### 前期准备
### 开始
### 图形编辑
### 代码
### 一个倒计时工具
## python case.md
### append 问题
## python magic.md
### python2.7以前的字典推导
## Python 测试.md
## Python 测试
### 测试代码的必要性
###  assert：断言
### 内置测试模块
### unittest
### doctest
### 三方测试工具
### py.test
### TestCase
### TestSuite
### doctest
### 自动化测试
### Robot Framework
## python2和3及pip等安装问题.md
### python2和python3区别
### 字符
### xrange
### 触发异常
### for循环变量与全局命名空间泄漏
### input输入
### 返回可迭代对象，而不是列表
### python 系统自带2.7升级到最新2.7.x
### python2.7安装pip
### python2和python3共存
### ubuntu
### 同一文件
##! python2
## -*- coding: utf-8 -*-12
##! python3
## -*- coding: utf-8 -*-12
### 分别安装pip
### 分别使用pip
### centos
### pip共存
### 各个安装组件的关系
### distutils（setup.py 相关）
### setuptools（easy_install相关) 和 distribute
## easy_install --version
### pip
### wheel
###　离线安装
### 安装python
### 指定安装目录，脱离系统环境
### 安装setuptools
### 指定python版本
### 安装pip
### 总结
### pip
## python内建.md
### 内建模块
### `__builtin__`
### 向内建函数中添加函数
### `__builtins__`
### 内置字段
### ` __doc__`
### `__name__`
### `__file__`
### `__dict__`
### `__future__`
### `__all__`
### `__call__`
### 内置函数
### vars
### locals() 获得函数参数k-v
### globals()
### eval() 和 exec()
### getattr()
### setattr()
### dir()
### help()
### property()
### `@property`
### python 自带命令解析
### -c
### -m
### 路径问题
### 其他
### 获取某函数的print到变量
## python内置库.md
## 内置
### sys
### os
### 系统操作
### 路径操作
###　文件操作
### 判断目标
### `os.path`
### `os.environ `
### json
### traceback
### collections
### defaultdict
### OderedDict
##输出：OrderedDict([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
### namedtuple 具名元组
## 接受两个参数，类名，和各个字段的名字，可以是由数个字符串组成的可迭代对象，或者像下面这样由空格组成的可迭代对象
### deque类
### pprint
### subprocess
### Queue
### singnal
## Define signal handler function
## register signal.SIGTSTP's handler
## Define signal handler function
## register signal.SIGALRM's handler
### socketserver
### shutil
### shlex
### timeit
### ConfigParser
### binascii
### shutil
### StringIO 和 cStringIO
## 生成一个StringIO对象，当前缓冲区内容为ABCDEF
## 从开头写入，将会覆盖ABC
## 每次使用read()读取前，必须seek()
## 定位到开头
## 将输出abcDEF
## 定位到第三个字符c
## 从当前位置一直读取到结束，将输出cDEF
## 从第三个位置读取两个字符，将输出DE
## 从指定位置写入
## 将输出abcDEFGH
## 如果读取所有内容，可以直接使用getvalue()
## 将输出abcDEFGH
### webbrowser
### 常用内建模块
### datetime
##转为字符串
##字符串转为时间类型
### time
### collections
## 创建namedtuple
## 初始化
## 使用下标访问
## 使用名字访问
## 使用getattr()访问
## 创建namedtuple
## 初始化
## 获得字段名
## 更改值
## namedtuple转为OrderedDict
## 使用list构造namedtuple
## 使用dict构造namedtuple
### base64
## 标准Base64:
## 自动去掉=:
### struct
###
### itertools
### contextlib
### XML
### HTMLParser
### urllib
### urllib2
## python内置库2.md
### bisect
## 根据成绩来判断成绩评级
### inspect
### signatrue
### csv
### ast
### functools
### 偏函数partial
## coding:utf-8
##par_func(0,2,3)
### 默认参数
## 可变参数和关键字参数
### wraps
##Calling decorated function
##Called example function
##'example', 去掉@wraps, 则是wrapper
##'Docstring', 去掉@wraps, 为None,也就是wrapper的doc
### hashlib
### asyncore
## python性能监控
## 性能监控
### 时间装饰器
## 时间统计
### Profile / cProfile + pastas
### line_profiler
### gprof2dot
### vprof
### pprofile
### Kcachegrind
### qcachegrind
## 系统监控
### glances
## python爬虫.md
### requests库
### BeautifulSoup库
### tag
### 提取标签的名字：
### 提取标签的属性：
### scrapy
### XPath
## python的字符编码.md
### 搞清字符编码问题：
### 了解编程环境编码
### python2和python3的编码区别
### python2
### python3
### 编辑页面的编码
##-*-coding: utf-8-*-
### 读入文件编码
### 一些问题
## python编译与链接库.md
## python编译 和 链接库
### pyc, pyo, pyd
### gcc 和 g++
### 链接库
### 静态链接库
### 动态链接库
### python调用c的so库
##include <stdio.h>
### 查看依赖库的共享库：
### 总结
## python非内置库.md
## 非内置
### rsa
### 生成秘钥
### 导入秘钥
### 加密和解密
### 签证和确认
### psutil
### chardet
##可根据需要，选择不同的数据
##创建一个检测对象
##关闭检测对象
##输出检测结果
## YAML.md
## YAML
### 语法
### python 读取
### load
### dump
## 问题
### 中文
### True | False
## 使用anaconda.md
### 概述
### MiniConda
### 安装（Linux）
### 添加环境变量（Linux）
### 虚拟环境
### 包管理
## 更新conda，保持conda最新
## 更新anacondaconda
## 更新python
## 假设当前环境是python 3.4, conda会将python升级为3.4.x系列的当前最新版本
### 改为国内镜像源
## 设置搜索时显示通道地址
### pycharm中配置
### 卸载
### 自带包
## 命令行解析.md
## 命令行解析
### argparse
### 默认配置， 配置说明
### 带固定参数(位置参数)
### 带可选参数
### add_argument
### **action:**
### nargs
### const
### dest
### default
### require
### type
### choices
### metavar
### docopt
## 字符集.md
### 问题起源
### ASCII编码
### GBK编码
### Unicode编码
### **UTF-8**
## 正则表达式.md
### 写在前面
### 规则
### 样例
### 单个字符
### 重复
### 特殊
### python中的正则
## 对应的正则表达式字符串变成：
## 'ABC\-001'
## 对应的正则表达式字符串不变：
## 'ABC\-001'
### match
### search
### 分组
### 贪婪匹配
### 编译
## 编译:
## 使用：
### findall
### 练习
### 一些实例
### ip
### 域名
## 域名正则， 匹配ntp服务器，可能形式：
## utcnist.colorado.edu
## time-a.timefreq.bldrdoc.gov
### 中文
## 用pdb调试python代码.md
### 写在前面
### 基本用法
### 打印变量
### 看当前代码所调试在的位置
### 进入函数
### 调试中改变变量的值
## 设计模式.md
## 写在前面
## UML类图
## 原则
### 1.单一职责原则
### 2.开放-封闭原则
### 3.里氏替换原则（LSP）
### 4.依赖倒转原则
## 模式
### 1.简单工厂模式
### 2.策略模式
### 3.后续
### 4.
# Ab___Python/Grammer
## Class.md
### 类
## 定义
## 使用
## 继承
### 访问限制
### `__slots__`
### super()方法
### `__init__()方法`
### `__new__()`方法
### 对象的属性
### 属性的`_dict_`系统
### 特性(property)
### 使用特殊方法_getattr_
### 静态方法@staticmethod和@classmethod
### 鸭子类型
### 特殊方法
### `__len__`
### `__dict__`
### `__getitem__`
### `__contains__`
### `__repr__`
### `__str__`
### `__bool__`
### `__call__`
### `__defaults__`
### `__kwdefaults__`
### `__code__`
### 如何使用特殊方法
## Function.md
### 函数
### 函数参数
### 函数的参数为引用时
### 可变类型作为参数默认值
### 包裹传递
##<type 'tuple'>
##(5, 6, 7, 1, 2, 3)
## <type 'dict'>
## {'c': 11, 'm': 2, 'n': 1}
## 相应的：
### lambda表达
### 内置函数
### map()
### filter()(根据条件判断)
### reduce()(累积传参）
### zip()
## cluster
## decompose
### dir()
### help()
### 运算和逻辑
### 计算
### sorted
### isinstance()
## 确认是声明的类
## 多选
### type()
### 函数式编程
## python(1).md
### 解释器
### 输出和输入
### 格式化
### format
### 条件判断
## python 写法
### 真值判断
### 相等比较
## True
## False
### 三目运算符
### 运算符是特殊方法
### 文件操作
### 作用域
### 非公开
### 作用域规则
### 模块和模块包
### 模块
### 模块包
### 导入
### 导入上级模块
## 现在直接可以导入上级的包了
### 查看导入包的路径
### 导入其他目录的包
### 错误和异常
### 抛异常
### 注意
## python(2).md
### 上下文管理器
## without context manager
## with context manager
## out:
## 把a+='1'注释打开：
### 内存管理
## True
## True
## False
## False
### del
### 垃圾回收
### 循环引用
## -*- coding:utf-8 -*-
## -*- coding:utf-8 -*-
### 弱引用和weakref
### 分代回收
### 浅拷贝和深拷贝
### python自省
### getattr()
### hasattr(object, name)
### python 面试题
### 参数传递
### 单例模式
### read,readline,readlines
## python进程线程.md
## 线程进程
### 多线程
### threading
### lock
### Event
### 队列
### local
### GIL锁
### 多进程
## Only works on Unix/Linux/Mac:
### Pool
### multiprocessing
## 为进程起名字，方便管理
## 得到目前进程名
## 该进程是否在进行
## 停止进程
### 进程间传递消息
## 写数据进程执行的代码:
## 读数据进程执行的代码:
## 协程和异步.md
### python中的异步
### 理解yield
### `next()`
### **yield是表达式**
### send(msg)
### send(msg) 与 next()的返回值
### 中断Generator
## Other exceptions are not caught
### 协程
### yield
### 一个简单的协程
##coding:utf8
### 协程的状态
### 终止协程和异常处理
##coding:utf8
##from inspect import getgeneratorstate
##print getgeneratorstate(coro)
##print getgeneratorstate(coro)
##print getgeneratorstate(coro)
### 那和多线程比，协程有何优势？
### 生产者消费者模型
### asynico
### async/await
## 循环迭代生成.md
### 迭代
### range
### enumerator
### dict.items()
### 迭代字符串
### else
### 占位符
### 生成式
### 列表生成式
### 内存泄露问题
### 生成器
### 生成器表达式：
### 迭代器
### next
## 类型和变量.md
### 变量
### 序列
### 元组
### 切片
### 关于序列的内置函数
## x为元素值，i为下标(元素在序列中的位置)
## l为一个表, l2为另一个表
##str为一个字符串，sub为str的一个子字符串。s为一个序列，它的元素都是字符串。width为一个整数，用于说明新生成字符串的宽度。
### 不可变对象
### 词典（字典dict）
## ============== 创建 =========
## ============== 删除 =======
### 字典中的散列表
### 集合set
### array
### memoryview
## 闭包和装饰器.md
### kwu闭包
### 闭包与并行计算
### 为什么要闭包？
### 自由变量
### global and nonlocal
### 闭包中的陷阱
### 装饰器
## get square sum
## get square diff
## get square sum
## get square diff
### 含参的装饰器
## a new wrapper layer
## get square sum
## get square diff
### 装饰类
### 几个simple demo 深刻理解
# Ac___Go
## Go(2)_ 语言基础.md
## Go(2)_ 语言基础
### 关键字
### 启动
### 定义变量
### 初始化
### 常量
### 分组声明
### 内置类型
### Boolean
### 数值类型
### 字符串
### 错误类型
### iota枚举
### array
### slice
### map
### 默认零值
### struct
### Go内置的一些规则
## Go(3)_流程和函数.md
## 流程和函数
### 流程控制
### if
### goto
### for
### 函数
## GO.md
## Go
### 安装
### 前提
### 配置
### 多版本管理gvm
### 目录结构
### 编译包
### 调用包和编译应用
### 安装应用
### 包管理工具go get
### go 命令
### go build
### go clean
### go fmt
### go get
### go install
### go test
### go tool
### go generate
### godoc
### 其它命令
### main 包
# Ba_LINUX
## Linux 硬件信息和命令.md
## Linux 硬件信息和命令
### 磁盘
### 查看磁盘容量-df
### 查看目录容量 du
### 分区
### fdisk
### 格式化（创建文件系统）
### 挂载
### 卸载
### RAID
### 软硬件RAID
### 内存
### free
### /proc/meminfo
### 硬件信息
### CPU
### lscpu
### /proc/cpuinfo
### 网卡
### ifconfig
### ip link show
### 查看某网卡的口是否有线连接：
### 创建虚拟网卡
## linux 网络.md
## linux 网络
### linux的网卡
### iptables
## 查看防火墙状态
## 停止防火墙
## 启动防火墙
## 重启防火墙
## 永久关闭防火墙
## 永久关闭后重启
### 网络
### 查看端口
###
### nc/netcat
### 端口扫描
### Chat Server
### 文件传输
### 目录传输
## Linux 问题排查.md
## Linux 问题排查
### No space left on device
### lsmod
### 关闭selinux
## This file controls the state of SELinux on the system.
## SELINUX= can take one of these three values:
##     enforcing - SELinux security policy is enforced.
##     permissive - SELinux prints warnings instead of enforcing.
##     disabled - No SELinux policy is loaded.
## SELINUXTYPE= can take one of these two values:
##     targeted - Targeted processes are protected,
##     mls - Multi Level Security protection.
### tab自动补全失灵
## enable bash completion in interactive shells
## if{-f etc/bash_conmpletion} $$ ! shopt -oq posix:then
## ./etc/bash_completion
## fi
## linux与终端传输.md
### virtual box虚拟机连接网络的方式
### 第一种 NAT模式 
### 第二种 Bridged Adapter模式 
### 第三种 Internal模式 
### 第四种 Host-only Adapter模式 
### xshell连接ubuntu虚拟机
###  lrzsz
### ftp
### scp
## question.md
### rm后的文件恢复
## 磁盘与文件系统.md
### 物理磁盘
### IDE接口
### SATA接口
### 接口和设备文件名的关系
### 磁盘结构
### 分区
### 挂载
### 光盘
### 文件系统
### Ext2 文件系统
### 目录
### 日志文件系统
### 其他文件系统与VFS
# Bb___Command
## bash脚本的编写.md
### 开始
### 输入输出
### 变量
### 字符串
### 注释
### 数组
### 参数传递
### 运算
##!/bin/bash
### 测试命令
### test命令条件测试
### 流程控制 if
### 循环 for
### case
### 函数
### 输入输出重定向
### 文件包含
##!/bin/bash
##!/bin/bash
## 使用以下包含文件代码
## source ./test1.sh
### 调试和检错 set
### 通过脚本学习到的linux命令
### shift
### shopt——set
### extglob  模糊匹配
### readlink
### dirname ： 会获得文件的目录路径：
### exec
### 其他或问题
### declare
### unexpected end of file
### linux命令执行返回值
## Linux proc.md
## ls /proc
## linux(1).md
### linux启动流程
### shell
### 文件系统
### SSH
### 版本分类
### 关机
### 用户切换
### 用户符号
### su,su-与sudo
### 当前用户更改root密码
### 用户和用户组
## User privilege specification
### 用户组(groups命令)
### 目录结构
### 目录颜色
### 目录和文件操作
### 新建目录（mkdir）
### 新建文件（touch)
### 复制(cp)
## \cp -f sourcefile targetdir
## vi ~/.bashrc
### 删除（rm)
### 移动/重命名（mv)
### 查看文件
### 软链接和硬链接
### 文件权限
### 查看文件权限
### 修改文件权限
### 一些技巧
### Tap补全命令
### history
### 通配符*
### man命令
### top
### who 命令
### whereis
### ~目录
### source和.
### 小技巧
## linux(2).md
### 比较合并
### 环境变量
### 修改环境变量
### 内存
### Swap
### buffer和cache
### 进程
### 进程的分类
### fork和exec()
### 僵尸进程和孤儿进程
### init 进程
### 进程组和Session
### kill
##kill的使用格式如下
##signal从1-64个信号值可以选择，可以这样查看
### 查看进程
### top
##查看物理CPU的个数
##cat /proc/cpuinfo |grep "physical id"|sort |uniq|wc -l
##每个cpu的核心数
### ps
###
### Mount
## linux(3).md
### Watchdog 看门狗
### 计划任务crontab
### 深入
### 一句话执行命令
### 管道
### `|`
### cut
## 前五个（包含第五个）
## 前五个之后的（包含第五个）
## 第五个
## 2到5之间的（包含第五个）
### grep
### wc
### sort
### uniq
### 数据流重定向
### tee
### 日志系统
### 神器 lsof
### find 查找文件
### 删除符合条件的文件
### 查找文件中的字符串
### Suprise Get
### state
### date
### w
### bg
## 字符操作.md
## linux 字符操作
### xargs
### cut
### sed
# Bc___Package
## CURL.md
## CURL
### post
### https
### 一些参数
### 添加请求头
### 添加User Agent
### 添加cookie
### 问题：
## NG
## OK
## Linux 软件和包.md
### 软件源码
### 可执行文件
### 函数库
### make 和 configure
### 解压文件
### 压缩格式
### gzip
### tar
### 安装软件的方式
### （1）下载源文件编译，安装：
### （2）软件包（安装包）
### （2）软件包的管理工具
### (3)apt(常用在线只能管理工具集)
### 软件源
### 卸载软件
## vim.md
### 基本操作
### 普通模式下
### 移动光标
### 行内跳转
### 当前光标处进入插入模式：
### 删除文本信息
### 复制和粘贴文本
### 替换和撤销
### 全部替换
### 缩进
### 调整文本位置
### 查找
### 命令模式
### 退出vim
### 多文件编辑
### 进入vim后打开新文件
### 视图操作
### 多窗口
### 在vim中执行外部命令
### 文件加密
### 恢复文件
### 其他
### 多行注释
### 多行tab
### 撤销
### 断行
### 4空格替换tab
### 设置unix格式
### 去掉M
## vim2.md
### 打开其他文件
### gf命令
### 缓冲区
### 窗口分屏
### 分屏同步移动
### 保存会话
## vim插件和配置.md
### Tmux
### 会话（session）
### 窗口（wind）
### 安装和配置git
### VIM
### vundle
### NEATree
### TagList
### python-mode
## 找代码定义
### YouCompleteMe
### 补充：
# Bd___Service
## beanstalkd.md
## beanstalkd
### 写在前面
### 下载
### beanstalkc
### 状态机
### tubes
### Statistics
## 查看job状态
## 查看某队列状态
## 查看客户端状态
### 遇到的问题
### 不是线程安全的
## kafka.md
### 写在前面
### 几个术语
### topics
### broker（经济人）
### producer
### consumer
### zookeeper
### ZAB 协议
### 广播
### 恢复
### AMQP
### 使用场景
### Quick Start
### Question
### 安装java
### `bogon: bogon: Name or service not known`
## nginx.md
## nginx
### 常用操作
### 配置文件
### 全局配置
### 其他
### 跨域
## ntp服务器.md
## NTP 服务器
### 时间标准
### GMT
### UTC
### linux 时钟管理
### 时间修改
### NTP 通信协议
### 客户端 ntpdate
### 服务端 ntpd
## ssl证书.md
### SSL证书
### 查看
### nginx 配置
### 自行颁发不受浏览器信任的SSL证书
## 生成一个RSA密钥
## 拷贝一个不需要输入密码的密钥文件
## 生成一个证书请求
## 自己签发证书
### 受信任的证书
## Syslog.md
### 登录档
### Syslog
MODULES　####
LOBAL DIRECTIVES####
RULES ####
### syslog 服务器
### 登录档的安全性
### logrotate
## see "man logrotate" for details
## rotate log files weekly
## keep 4 weeks worth of backlogs
## create new (empty) log files after rotating old ones
## use date as a suffix of the rotated file
## uncomment this if you want your log files compressed
#compress # 被更劢的登录档是否需要压缩？如果登录档太大则可考虑此参
## RPM packages drop log rotation information into this directory
## 将 /etc/logrotate.d/ 这个目录中的所有档案都读迚来执行 rotate 的工作！
## no packages own wtmp and btmp -- we'll rotate them here
## system-specific logs may be also be configured here.
## 远程联机服务器.md
### 远程联机服务器
### 可提供登入的类型
### SSH 服务器
### 服务启动
### 客户端联机
### 免密码登陆
## PubkeyAuthentication yes
## 是否允许用户自行使用成对的密钥系统进行登入行为，仅针对 version 2。
## AuthorizedKeysFile .ssh/authorized_keys
## 至于自制的公钥数据就放置于用户家目录下的 .ssh/authorized_keys 内
### sftp , scp
# Bottle源码阅读
## 1.md
### 流程
### bottle.py
### ServerAdapter
### WSGIRefServer
### wsgiref.simple_server.py
### WSGIServer
### WSGIRequestHandler
### ServerHandler
### wsgiref.handlers.py
### SimpleHander
### BaseHandler
### BaseHTTPServer.py
### HTTPServer
### BaseHTTPRequestHandler
### SocketServer.py
### TCPServer
### BaseServer
### StreamRequestHandler
### BaseRequestHandler
### Handle
## bottle源码阅读.md
###  流程
### bottle.py
##: A dict to map HTTP status codes (e.g. 404) to phrases (e.g. 'Not Found')
### BaseRequest(object)
### BaseResponse(object)
##: A thread-safe namespace. Not used by Bottle.
## 一个线程安全空间， bottle并没有用上
### Bottle()
### Router()
### Server
### handle
### `Bottle.__call__ ,__handle, __cast, wsgi`
### router.match(environ)
### handlers.py BaseHandler.start_response
###  装饰器路由的初始化
## bottle 文件中
## 最后：
## 走的route(), 基本所有方法都会走route()
## 那是不是直接用route会快那么一点点。。
### route()
### Route
### Router.add
### other get
## FixedHandler_all.py
## ======== bottle.py =============
## ========= wsgiref/simple_server.py  =========
## ========== wsgiref/handlers.py =======
## ==========  BaseHTTPServer.py ===========
## ============ SocketServer.py ===========
## select.select.md
## socket.md
### 写在前面
### TCP socket 实现
### 客户端
## 导入socket库:
## 创建一个socket:
## 建立连接:
## 发送数据:
## 接收数据:
## 关闭连接:
### 服务器
## 监听端口:
## 建立连接:
## 接收欢迎消息:
### UDP socket 实现
### 客户端
### 服务端
## 绑定端口:
### socket对象 其他API
### accpet()
### setblocking()
### fileno()
### makefile([mode[, bufsize]])
### shutdown(how)
## WSGIServer_all.py
##  =========== wsgiref/simple_server.py ===========
##  =========== BaseHTTPServer.py HTTPServer =========
## ============ SocketServer.py TCPServer =============
## =========== SocketServer.py BaseServer ======================
## 用socket实现http服务器_.md
### TCP socket
## 地址
##socket.socket()创建一个socket对象，并说明socket使用的是IPv4(AF_INET，IP version 4)和TCP协议(SOCK_STREAM)。
## 绑定ip和端口
## 被动监听，连接队列中最大有三个连接数
## 接受连接，并建立链接
## 接受消息
##发送消息
## Written by Vamei
## Client side
## Address,没有两台计算机，用本地ip
## configure socket
## send message
## receive message
## close connection
### 基于TCP socket的http服务器
## Address
## Prepare HTTP response
## Read picture, put into HTTP format
## s=f.read()
## print(chardet.detect(s))
## Configure socket
## infinite loop, server forever
### response
### request
# Cb___Sql
## linux下python与mysql.md
### 安装mysql
### mysql和python的中间件
### 进入mysql
### 数据库基本使用
### 创建用户和创建数据库
## mysql与mongodb的安装与配置.md
## MySql
### 配置（免安装版）
## 默认字符集
## mysql 安装路径
## mysql 数据文件夹路径，不要怕，我们现在确实还没有创建这个 data 文件夹
## mysql 服务器监听的 TCP/IP 端口号
### 命令操作
## NoSql
### 键值数据库
### 文档数据库
### 列式数据库和基于图的数据库
## MongoDB
### 可视化工具Robomongo
## MySQL安装.md
## 解压安装
## 配置环境变量
## 编辑配置文件
## 默认字符集
## mysql 安装路径
## mysql 数据文件夹路径，不要怕，我们现在确实还没有创建这个 data 文件夹
## mysql 服务器监听的 TCP/IP 端口号
## 安装 mysql 服务
## 初始化 data 文件夹
## 启动 MySQL 服务
## 修改 MySQL 初始密码
## Mysql 一些命令
## ubuntu下安装
## navicat远程连接Linux中的mysql
## 修改mysql字符集
### 修改默认编码集
## windows 导出数据库到 linux
### Django 连接Mysql
## slite.md
## 数据库与SQL.md
## 数据库范式
### 概念
### 范式
## SQL语言
### SQL集成工具集
### 查询语句
### 新增数据
### 修改数据库
### 删除数据
### 函数
## SQL扩展
### 修改表：
### select的修改
### 一些关键字
### 嵌套
### 聚集函数
### 左连接与右连接
### 多表查询
### 笛卡尔积
### 多表连接
### 经典题
### 三表联合查询
# Cc___Nosql
## Celery与消息队列.md
### Celery
### 何为Celery
### 特点
### RabbitMQ
### 下载与安装
### windows
## Elasticsearch.md
### 写在前面
### 下载和安装
### 确保Java 8环境
##!/bin/bash
### elasticsearch安装
### 概念说明
### 索引
### 文档
### 文档元数据
### 操作
### PUT
### 创建：
### 更新：
### 只是创建
### POST
### GET
### `_source`
### `_search`
### 使用查询表达式
### 全文搜索
### 查询情况和过滤情况
### 验证查询
### 分页
### HEAD
### DELETE
### 其他
### 高亮
### 显示所有索引
### 进阶
## MongoDB(1).md
### 写在前面
### 安装和配置
### 离线安装
### 后台运行
### 使用和命令
### 创建
### 删除
### 插入
##  插入单条数据
##  插入多条数据
### 改
### 查看
### 条件
### $type操作符
### 集合
### 常用类型
### 方法
### limit
### skip
### sort
### 索引
### 副本集（复制）
### 分片
## mongodb(2).md
### 关系
### 嵌入式
### 引用式
### aggregate（聚合）
### aa
### 聚合方式
### Aggregation Pipelines
### Map-Reduce
### Single Purpose Aggregation Operations
## mongo状态检查和问题记录.md
## Mongo 检查和问题记录
### 0
### 内存
### 硬盘
### 1
### mongostat
### mongotop
### 1.5 mongo存储结构
### 基础
### Data files
### Extents
### db.stats()之前
### 2
### stats()
### serverStatus()
### 当前库使用的内存
### stack
### currentOp()
### 3导入导出
### 4其他
### 建索引
###getMongo
### MongoDB释放内存的命令
### com.mongodb.MongoException: Lock not granted. Try restarting the transaction
## Mongo集群.md
### 分片
### 分割数据
### 分配数据
### 建立集群
### 使用集群
## pymongo.md
## pymongo
### 建立连接
### 访问数据库
### 访问集合
### 操作文档
### 插入
### 更新
### 查询
### Cursor
### 删除
### sort,skip, limit
### 索引
### 技巧
### cursor conver to json
### ObjectId to str
### find时只返回特定字段
### 只匹配一个字段中数组的数
### 在不存在时才更新
## pymongo2.md
### db.command
### 聚合
### statistics
## print collection statistics
## print database statistics
# Da_GIT
## CI 持续集成.md
## CI 持续集成
### 一些概念
### Pipeline
### Gitlab-CI
### GItlab-runner
## git 进阶2.md
## git 进阶2
###  some details
### git rebase
### 标签管理
### 标签操作
### submodoule
### 克隆带子模块的版本库
### linux 下的配置
### 终端显示git 当前所在分支
### linux git自动补全
### git的命令行的颜色配置
## Github笔记.md
### 基本概述
## git基本验证和操作.md
### 从本地已有项目，推送到github
### ssh与公钥
### 客户端与github建立连接
### 初始化本地仓库，并提交内容
### 连接到远程仓库，并将代码同步
### 后期继续提交
### 从linux上传项目到github
## git多账户管理.md
### 多账户链接
## 配置github.com
## 配置gitlab
## 局域网
### 测试配置是否成功
### 添加到ssh-agent
### 配置局部用户和邮箱
### test
## git进阶.md
### origin
### remote
### 分支
### fork
### checkout
### fetch
### merge
### git log
### git stash
### 解决冲突
### 版本回溯
### 本地撤销和版本回退
### 忽略跟踪
### 提交请求流程
### 出部署包流程
### 一些问题
### windows更改文件权限
### 一个分支的修改同步到另一个分支
### 查看当前git分支是基于哪个分支建立的
### github设置密钥后push仍然需要密码：
###
### Changes not staged for commit ,
### fatal: unable to access
### Git checkout: updating paths is incompatible with switching branches
### 注意
# Ea_DOCKER
## Docker .md
##Docker
### 初识容器和Docker
### 三大核心概念
### 安装
### 配置
### 命令
### 三大概念的操作
### 使用Docker镜像
### 容器操作
### 访问Docker仓库
### 使用Dockerfile创建镜像
### 命令说明
## first dockerfile demo
## 设置该dockerfile的作者和联系邮箱
## 开始配置环境, 下载apt-get,生成index.html的文件
## 暴露server的port
### 运行
## 一个一个的赋值
## 另外,还可以一起赋值
## 修改环境变量
### Docker 容器数据管理
### 数据卷
### 数据卷容器
### 端口映射与容器互联
## 实战
### 用Docker安装操作系统
## 遇到的问题
## yun.md
## 自己动手写docker(2).md
### 构造容器
### 实现run命令
## 自己动手写Docker.md
## 自己动手写Docker
### Linux Namespace
### UTS Namespace
###  IPC Namespace
### PID Namespace
### Mount Namespace
### User Namespace
### Network Namespace
### Linux Cgroups
### Cgroups 中的三个组件：
###  kernel 接口
###  Docker 如何使用Cgroups
### Go实现对cgroup限制容器的资源
### Union File System
## 目录结构
## 创建一个mount目录
## 把水果目录和蔬菜目录union mount到 ./mnt目录中
##  查看./mnt目录
### 删除文件
## tree
## mkdir mnt
## mount -t aufs -o dirs=./test=rw:./fruits=ro:./vegetables=ro none ./mnt
# # ls ./mnt/
## touch ./test/.wh.apple
## ls ./mnt
### 作用
### 分支
##ls /sys/fs/aufs/si_b71b209f85ff8e75/
## cat /sys/fs/aufs/si_b71b209f85ff8e75/*
### Docker如何使用AUFS的
### layer目录
### diff目录
### mnt目录
### container layer 和 AUFS
# Fa_WebFramework
## IO模型.md
### 异步IO
### 何为异步
### 在理解并发和并行
### 阻塞和非阻塞
### 总结
### Linux下的五种IO模型
### 三种I/O复用的实现方式
## JWT.md
### 结构
### 优点特性
## SSE.md
### 本质
### 特点
### 服务端实现
### data 字段
### id 字段
### event 字段
### retry 字段
### python 实现
## WebSocket.md
## 从web服务方式到nginx.md
### 常见web服务方式
### 一个web请求的处理过程
### linux I/O 模型
### Apache Http的工作模式
### 提高web服务器的并发连接处理能力
### Nginx优异之处
### 工作原理
### 为什么选择Nginx
### 正向代理与反向代理
## 网络协议.md
### http协议
### 浏览器向服务器的请求request:
### 服务器的响应消息 response
### 状态码
### tcp/ip协议
### 三次握手，四次挥手
### 问题
### 打开一个url发生了什么
### DNS 解析
### DNS负载均衡
### HTTPS协议
### 环回地址
## 跨域.md
# Fb___Django
## Django(一).md
### 概述
### 安装
##python
### 目录
### 建立项目
### 建立应用
### Migrate
### 开始
### settings 配置
### 启动
### 模型类
# -*- coding: utf-8 -*-    #最好在有中文的代码中加上这句话，声明文件用utf-8编码
### 字段
### Model元数据meta
### 导入导出数据
### 生成数据移植文件
### 重置
### 删除一张表后，重新建立
### 将多个迁移文件变为一个
###  添加新的字段
### 管理器
### 基本查询
### 关系模型
### 一对多，一对一
### 多对多
### 对模型的api操作
### 增：
##方法一：
##方法二：
##方法三
##一对多或多对多的增，先把相关对象查询出来。
### 查：
##方法一，获取一个对象
##方法二
##方法三
## 找出名称含有abc, 但是排除年龄是23岁的
## 1. 使用 reverse() 解决
## 2. 使用 order_by，在栏目名（column name）前加一个负号
## 合并到一起
## 去重方法
### 用select_related和prefetch_related优化关系查询
### defer和only
### 语句集合
### 其他:
### 改
### 删
### 性能优化
## Django(三）.md
### 上传文件
### 基本形式
### 文件限制
## Django在Ubuntu下的部署.md
### Nginx
### 配置转发
### 静态文件的处理
### 防火墙的开启
### 开启安全组
### django
### uwsgi
### 遇到的坑
## Django缓存.md
## django部署企业微信应用.md
### 写在前面
### 可信域名
### 接受消息（回调校验）
## -*- coding:utf-8 -*-
## from django.shortcuts import render_to_response
## logger = logging.getLogger("EngEye")
### 自定义菜单
## Django（二）.md
### Request 和 Response
### URL映射
### 带参的url
### 分布式URL映射
### 反向解析
### 表单
### 绑定状态
### 数据验证
### cleaned_data
### 自定义逻辑验证
### 检查变更字段
### save()，获取表单值并修改。
### 模版文件
### 视图
### 创建视图
### 例子
### Admin
### 创建管理员
##输入登录名
##输入email
##输入两次密码，八位，字母和数字。
## Framework.md
### RestFramework
### 建立一个数据模型
### 序列化
### 写在前面
### 保存实例和save()方法：
## .save() will create a new instance.
## .save() will update the existing `comment` instance.
## 也可添加另外的参数
### 检验器 Validation
## False
## {'email': [u'Enter a valid e-mail address.'], 'created': [u'This field is required.']}
### framwork中的序列化
### 一对多关系的处理
### 多对多的处理
### 序列化关系模型
### Requests和Responses
### 为URL添加可选的数据格式后缀
### 状态码
### 视图
### 1. 基于视图函数的@api_view
### 2. 基于类视图的APIView
### minxins:
### 通用类视图：
### 权限和认证
### 修改模型
### 修改seralizers
### 添加permissions.py
### 修改views.
### 修改URL
### Relationships和Hyperlinked
### 分页
### ViewSets和Routers
### 权衡Views和Viewsets
# Fc___Flask
## flask+gunicorn+supervisorn+nginx项目部署.md
### 虚拟环境
### 创建项目
### gunicorn
### gunicorn的设计
### gunicorn+Nginx
### uWSGI
### 安装
### 启动
### supervisor
### 命令
### 配置开机就启动我们的项目
### 出现的问题
### 开启防火墙端口
### Nginx
### 进程模型
### 多进程时间模型：异步非阻塞
### 配置
### 记得开启安全组
## flask开发前的准备.md
### vagrant 和 docker
### wsgi和werkzeug
### openid和OAuth 
### PyPI
### 钩子
###  一些docker命令
### 下载镜像
### 查看镜像列表
### 启动容器
### 退出容器
### 重新进入一个存在的容器
## Flask整理(一).md
### 使用FlaskScipt
### config.py文件
### manage.py文件
## import Flask Script object
## Init manager object via app object
## Create a new commands: server
## This command will be run the Flask development_env server
##可以运行命令：python manage.py server 来运行整个项目
### main.py文件
## Get the config from object of DecConfig
### 程序和请求上下文
### SQLAlchemy
##MySql
##Oracle
##sqlite不用
### 创建uri来链接数据库
##mysql
##sqlite
##Oracle
### 创建数据模型
## 直接调用对象实际上是隐式的调用了 User.__repr__(user)
## __repr__() 其定义了类实例化对象的可打印字符串表达式
### 在数据库中根据模型创建表
### SQLAlchemy的CRUD
## 返回表中的第一条记录
## 其中 User.query 返回的是 flask_sqlalchemy.BaseQuery object
## flask_sqlalchemy.BaseQuery object 拥有对数据库操作的所有抽像方法
## or
## 返回表中指定主键的一条记录
## or
## 返回符合过滤条件的第一条记录
## 其中 db.session.query(User).filter_by(id='49f86ede-f1e5-410e-b564-27a97e12560c') 返回的是一个 sqlalchemy.orm.query.Query object 对象
## sqlalchemy.orm.query.Query.first() 才是一个 User 对象
## 获取多条记录
## 返回符合过滤条件的所有记录, 将所有 username == fanguiju 的记录都获取
## 获取全部数据
## or
## 获取数量限制数据，这个返回特征常与数据的分页功能结合使用.
## 排序返回的记录
## 正向排序
## 反向排序
## 链式调用，一条读取语句的链式操作都是一个 first() 或 all() 函数结束的. 它们会终止链式调用并返回结果.
## paginate() 与 first()/all() 不同, 后者返回的是一个 models 对象或 models 对象列表, 而前者返回的是一个 pagination 对象. 而且 pagination 对象还包含了几个特有的属性:
## 获取这一页所包含的数据对象
## 获取这一页的页码
## 获取总共的页数
## 是否有上一页
## 如果有上一页的话, 获取上一页的 pagination 对象
## 是否有下一页
## 如果有下一页的话, 获取下一个的 pagination 对象
### model间的关系
## 实例化一个 User 的对象
## 写入一条 users 记录
## 现在因为还没有添加 posts 的记录所以为空，这个posts是posts=db.relationship中的posts
## 实例化一个 Post 的对象
## 主键值是非空的，必须指定一个，否则会报错
## =============重点================
## 指定该 post 是属于哪一个 user 的
## 获取一个已经存在数据库中的记录 user
## 实例化一个 Post 的对象 post_second
## 必须为其设置主键值
## 现在该 post_second 对象是没有关联到任何 user 的
## =============重点================
## 为 post_second 指定一个 user 对象，users为表名
## 将 post_second 写入数据库
## 写入完成之后，user 才能够通过关系来访问到属于其下的 posts
## 实例化 3 个 Tag 的对象
## 将 Tag 的实例化对象赋值给 Post 实例化对象的 tags 属性
## 即指定 Tag 和 Post 之间的关联状态
## post_one 对应一个 tag
## post_two 对应三个 tags
## tag_one/tag_three 对应一个 post
## tag_two 对象两个 posts
##==============重点=================
##================重点=========================
##在上面说过了 many to many 的 backref 是一个 List 对象，所以我们还可以反过来为 tags 添加一个 posts 对象(引用)。
## 因为修改了 tag_one 的 posts 属性(添加了 post_one 的引用)，所以需要重新提交 tag_one 才会被写入到数据库。
### 数据库迁移
##Flask-Migrate提供MigrateCommand类来连接Flask-Script的manager对象。
### 补充
### WTForm
### 基础
### 支持的html字段
### 表单验证函数
### 自定义检验器
### 视图函数中处理表单
### 模板接收表单
### 重定向和用户会话session
### flush消息
### CSRF保护
## Flask整理（三）.md
### Itsdangerous
### Flask_Mail
##下面是SMTP服务器配置，可以在相关邮件代理查到，比如我这个用的就是腾讯的。
### Flask_Security
### Flask_Admin
### BaseView: 基础视图
### ModelView: 模型视图
### FileAdmin: 本地文件系统管理
##初始化
### Flask_Uploads
### PIL
## Flask整理（二）.md
### 使用BootStrap
### 使用蓝图创建控制器（controller）
### 请求构建和销毁，和全局变量
### 自定义错误页面
### 使用类描述视图
### 方法视图
### 蓝图
### 工厂模式生成应用对象
## Get the ENV from os_environ
## Create thr app instance via Factory Method
### 目录结构
### 需求文件
### Bcrypt密文存储账户信息
## Create the Flask-Bcrypt's instance
### reCAPTCHA实现验证码
### Flask Login保护登陆安全
## Setup the configuration for login manager.
##     1. Set the login page.
##     2. Set the more stronger auth-protection.
##     3. Show the information when you are logging.
##     4. Set the Login Messages type as `information`.
##检验 User 的实例化对象是否登录了.
##检验用户是否通过某些验证
##检验用户是否为匿名用户
### 构建RESTful Flaks API
### 为什么要构建restful api
### 使用ajax
# Ga__Tornado
## tornado.md
### 基本结构
### 路由解析
### RequestHandler
### Entry Point 接入点函数
### 输入捕获
### 获得URL查询参数和POST提交参数集合
### 获得cookie
### 输出响应函数
### 设置状态和跳转：
### 设置header和cookie
### 写入body值
### 清空
### 异步化及协程化
### 异步化
### 协程化
## 异步.md
##!/bin/env python
## 这个并发库在python3自带;在python2需要安装sudo pip install futures
# Ra_RPC
## 1.md
### 什么是RPC
### Nginx 和 RPC
### Hadoop 与RPC
### 再谈HTTP调用，它是一种特殊的RPC
### 交互流程
### 协议设计
### 消息的结构
### 消息压缩
###
## 协议实例.md
###  Redis 文本协议结构
### RESP
###  发送指令
### Protebuf 二进制协议结构
### 协议格式
### 消息边界
### Redis 客户端的缺陷
###  请求缺陷
### 请求唯一ID
## 构造RPC客户端.md
### 设计要点
### 多线程
### 安全锁
### 惰性连接
### 健康检查
### 超时策略
### 性能追踪
### 多路复用
### 单项请求
### 心跳
## 模型.md
## 单线程同步模型
### client
## coding: utf-8
## client.py
### server
## coding: utf8
## blocking_single.py
## 多线程同步模型
## 多进程同步模型
## PreForking 同步模型
# Sa_Security
## Burp Suite.md
## Burp Suite 使用
### 运行
### Proxy
### Spider
### Scanner
### intruder
## web安全.md
### SQL注入
### 前端攻击
### 跨站脚本攻击xss
### 存储型
### 反射型
### 跨站请求伪造csrf
### DOS 攻击
### MIME Type
### C&C服务器（C2）
# Ya_ShortcutKey
## win10优盘重装系统.md
### 写在前面
### 准备工作
### 开始装机
## win10激活.md
## windows一些快捷键和命令.md
### 查看自己DirectX版本的方法是：
### 新建文件夹快捷键 
### 启动服务 
### 注册表 regedit
### 当面目录直接进入cmd
### 开机启动
### 画图
### MD5
### 批量重命名
### 刷新dns
### 屏幕控制
## 一些快捷键.md
### idea快捷键
### 这里简单记一下我需要的Vimium命令
### 下面是chrome自带的快捷键
### markdown表格
