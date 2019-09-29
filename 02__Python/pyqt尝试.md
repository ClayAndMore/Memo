Tags:[python]

## pyqt尝试

### 前期准备

- Anaconda 
- Qt Designer , 其是你不需要下载，它在 `*\Anaconda3\Library\bin\designer-qt4.exe.*`
- 建个虚拟环境 安装pyqt4 : 
  - 去` https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4` 下载相应版本的whl 到本地。
  - 在有刚才下载的文件目录中`pip install PyQt4-4.11.4-cp35-none-win_amd64.whl`

我们打算做一个小demo，类似于一个输入框输入数字作为收入，根据另一个组件的值来计算税值:

![](http://claymore.wang:5000/uploads/big/d4b432ce080da6949511a87afd042ba3.png)

### 开始

#### 图形编辑

1. 打开qt Designer, 选择Main Window,  它将创立一个空的窗口画布。
2. 在左侧选择一个Text Edit拖到右侧画布。
3. 点击Text Edit 右侧属性栏中objectName 为这个text edit对象的名字，最好更改，后来我们在python文件中将会用到。
4. 可以为上方Text Edit 前加个TextLabel,
5. 左侧找到一个spin box, 右侧我们可以输入限制值， 我们可以在它前加个TextLabel。
6. 从左侧拖拽一个PushButton和一个Text Edit作为输出。
7. 保存，到工作目录， 其实打开它，可以看到是一个xml格式的文件。

#### 代码

main.py,

```python
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMessageBox

qtCreatorFile = "untitled.ui" # 这里是我们上方画的ui模版文件，这里是同级陌路.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.CalculateTax) # pushButton是我们按钮对象的名字
        
     def CalculateTax(self):
        price = int(self.text_edit1.toPlainText())   #text_edit1 是第一个输入框的名字
        tax = (self.spinBox.value())                # spinBox 同样的
        total_price = price  + ((tax / 100) * price)
        total_price_string = "The total price with tax is: " + str(total_price)
        self.textEdit.setText(total_price_string)  # textEdit 展示端框的名字
        
 if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

```



到这里我们的代码就写完了， pyqt是封装好的一套ui api调用，如果我们工作中不太需要，不需要花太多经理在上面，这里只是尝试一下。

做一个弹窗：

在MyApp类中添加函数：

```python
def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
            
        retval = msg.exec_()
        print("value of pressed message box button:", retval)
```



`__init__` 函数中添加一个按钮事件触发：

`self.pushButton1.clicked.connect(self.showdialog)`





### 一个倒计时工具

用了组件： lcdNumber

计算到20190607 高考时间的倒计时

```python
import sys
import time
import datetime
from threading import Thread
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QLCDNumber

qtCreatorFile = "countdown.ui" 
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
END_TIME_DAY =  datetime.datetime(2019, 6, 7) #2019.6.7 00:00

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        t = Thread(target=self._countdown)
        t.start()
    
    def _countdown(self):
        while True:
            today = datetime.datetime.now()
            del_datetime = END_TIME_DAY - today
            days = del_datetime.days
            seconds = del_datetime.seconds

            remain_perc = '%.2f'%(1-seconds/86400) # 3600*24
            show_str = str(days) + remain_perc[1:]
            self.lcdNumber.display(show_str)

            time.sleep(600)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
```

