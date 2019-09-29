
tags: [python] date: 2017-04-09


### 概述

Anaconda是一个用于科学计算的python发行版。

利用工具和命令conda来进行package和environment的安装和管理。这也是它的核心功能。

设计理念：

conda将几乎所有的工具，第三方包都当作package来对待，甚至包括python和conda自身。

优点：

* 不需要配置python环境变量
* 集成package
* 多环境管理，互不干扰，兼容性强


下载：

```
https://www.continuum.io/downloads
```

如果国外的网站下载不下来，可以用清华镜像下载:
[http://mirrors.tuna.tsinghua.edu.cn/help/anaconda/](http://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
其中anaconda2.xx是python2.xx版本的，其中anaconda3.xx是python3.xx版本。

安装：

安装时，安装程序会把bin目录加入PATH（Linux/Mac写入`~/.bashrc`，Windows添加到系统变量PATH）

可以通过`which conda`或`conda --version`命令检查是否正确。假如安装的是Python 2.7对应的版本，运行`python --version`或`python -V`可以得到Python 2.7.12 :: Anaconda 4.1.1 (64-bit)，也说明该发行版默认的环境是Python 2.7。



#### MiniConda

Miniconda 是一个 Anaconda 的轻量级替代，默认只包含了 python 和 conda，但是可以通过 pip 和 conda 来安装所需要的包。

Miniconda 安装包可以到 https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/ 下载。



### 安装（Linux）

当前目录安装。

ubuntu：`bash XXXX.sh`

注意这可能改变了默认的python版本，去环境变量看下。

如需要python2的默认版本，可以把anaconda3/bin/python 软链接删掉。



### 添加环境变量（Linux）

都会自动加，安装后要重启。可以去`vi ~/.bashrc`看。



### 虚拟环境

用法和不用anaconda的用法差不多：

* 创建环境：

  `conda create --name python35 python=3.5`

  创建一个名为python34的环境，指定Python版本是3.5（不用管是3.5.x，conda会为我们自动寻找3.5.x中的最新版本）


* 创建的环境会在 D:\ANACONDA\envs类似的文件夹中存在。

  日后下载的相关包虚拟环境都会在相关目录中

* 进入环境：使用activate激活某个环境

  ```
  activate python35        # for Windows
  source activate python35 # for Linux & Mac
  ```

* 退出环境

  ```
  deactivate python34 # for Windows
  source deactivate python34 # for Linux & Mac
  ```

* 删除一个已有的环境：

  `conda remove --name python34 --all`

* 列出所有的虚拟环境

  `conda info --envs`

  



### 包管理

包管理和pip类似如安装xxx,:

`conda install xxx`

查看已经安装的包：

`conda list0`

更新包：

`conda update -n xxx`

删除:

`conda remove -n xxx`



前面已经提到，conda将conda、python等都视为package，因此，完全可以使用conda来管理conda和python的版本，例如

```
# 更新conda，保持conda最新
conda update conda 
# 更新anacondaconda 
update anaconda 
# 更新python
conda update python
# 假设当前环境是python 3.4, conda会将python升级为3.4.x系列的当前最新版本

```



### 改为国内镜像源

运行下面两条命令改为清华的镜像源：

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
# 设置搜索时显示通道地址
conda config --set show_channel_urls yes
```



显示当前镜像源：`conda config --show channels`

移除添加的镜像源：`conda config --remove-key channels`



### pycharm中配置

settings-project-project-interpreter

可以选择你刚建立好的虚拟环境。



### 卸载

可以直接删目录。

`rm -rf anaconda`

清理环境变量：

`vi ~/.bashrc`

最后，最好关掉终端重启，不然还是有原来的文件。



### 自带包

ipython

numpy

scipy

matplotlib

pandas

scikit-learn

可在Anaconda\Lib\site-packages里查看