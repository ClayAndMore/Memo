## 准备环境

Anaconda 

创建一个专门的虚拟环境：

```sh
# conda create --name py38QT python=3.8

C:\Users\wy>conda env list
# conda environments:
#
base                  *  E:\Anaconda3
py38QT                   E:\Anaconda3\envs\py38QT
```

安装包:

``` sh
# 进入虚拟环境安装activate py38QT, (py38QT) C:\Users\wy>
# sip
pip install SIP
# PyQt5:
pip install PyQt5 -i https://pypi.douban.com/simple # 使用豆瓣源
# PyQt5-tools
# 安装完后添加系统变量：E:\Anaconda3\envs\py38QT\Lib\site-packages\pyqt5_tools
pip install PyQt5-tools -i https://pypi.douban.com/simple
# pyinstaller , 把python打包成一个可执行文件
pip install PyInstaller -i https://pypi.douban.com/simple

```

pycharm

## 实际步骤 

### 配置 designer

打开pycharm, 创建一个新项目，选择我们之前创建的conda虚拟环境。

打开 Setting，找到 Tools -> External Tools, 添加一个tool.

Name添加为QTDesignier, program 选择 为 Anaconda3\Library\bin\designer 的可执行文件。

Work 选择为该项目路径。



### 一个demo

添加好后，我们可以在ide的导航框  Tools 中选择 external Tool 找到 QTDesignier, 点开后，设计一个简单的界面，然后保存 untiltled.ui。

在ide的终端上使用 pyuic5 -o qttest.py untitled.ui，将刚才的ui转换为 python 代码。

新建一个 excute.py ：

``` python
# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from qttest import Ui_Form

if __name__ == "__main__":
    app = QApplication(sys.argv) # 每个pyqt程序必须创建一个application对象
    window = QMainWindow()

    ui = Ui_Form()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_()) # 程序主循环退出
```

运行该 excute.py 即可弹出之前的设计窗口。





### 事件与信号处理





### 布局

绝对布局，箱式布局。