
---
title: "python 图像识别.md"
date: 2019-10-12 17:45:41 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "python 图像识别.md"
date: 2019-10-12 17:45:41 +0800
lastmod: 2019-10-21 09:53:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
https://juejin.im/post/5aa8b7706fb9a028b54794ba



https://zhuanlan.zhihu.com/p/29868652

https://www.cnblogs.com/dcb3688/p/4610660.html



tesseract 

安装：https://zhuanlan.zhihu.com/p/35687577





游戏测试：

https://testerhome.com/topics/12537



网易 ATX:

https://testerhome.com/topics/6218



cv2 对比：

https://blog.csdn.net/firemicrocosm/article/details/48374979

https://testerhome.com/topics/12537



带ui的：

https://blog.csdn.net/zydarChen/article/details/77587985



## cv2

说明：

### 安装

```python
# pip install cv2  
Collecting cv2
  Could not find a version that satisfies the requirement cv2 (from versions: )
No matching distribution found for cv2

# pip install opencv-python 
Collecting opencv-python
  Downloading https://files.pythonhosted.org/packages/34/9f/c0f259ce0869959b802fd1dfff5861fa9c0e72b1cfdd60867476bc70a310/opencv_python-4.1.1.26-cp35-cp35m-win_amd64.whl (39.0MB)
    100% |████████████████████████████████| 39.0MB 396kB/s
Requirement already satisfied: numpy>=1.11.1 in f:\anaconda\envs\py35_draw\lib\site-packages (from opencv-python)
Installing collected packages: opencv-python
Successfully installed opencv-python-4.1.1.26

# python
>>> import cv2
>>>
```

cv2 为 32位的系统安装方式， opencv-python 为 64位的安装方式

详情请看： https://pypi.org/project/opencv-python/



### 读取并显示图像

```python
import cv2

img = cv2.imread("F:\\test.jpg") 
#采用默认方式读取图像，支持 bmp、jpg、png、tiff 等常用格式
#采用黑白方式读取图片
# img2 = cv.imread("C:\\Users\\tt.jpg",0)

#创建窗口
cv2.namedWindow("Image") 

#第二个参数是cv.WINDOW_NORMAL时可以调节窗口大小，默认不可调的(cv.WINDOW_AUTOSIZE)
#cv.namedWindow("Image",cv.WINDOW_NORMAL)

cv2.imshow("Image", img)

cv2.waitKey(0) #延迟，在delay<=0时会无限制等待按钮事件
cv2.destroyAllWindows()  #破坏所有创建的窗口，释放窗口
#若要销毁特定窗口可以用 cv.destroyWindow()

print (img.size)  3261360
print (img.shape) (1070, 1016, 3)
print (img.dtype)  uint8
```

图片属性：

* img.size 计算图片、数组和矩阵所有数据的个数 
* iimg.shape 获得图片每个维度的大小 ，第一个元素表示矩阵行数，第二个元组表示矩阵列数，第三个元素是3，表示像素值由光的三原色组成。
* img.dtype  获得数据类型

图像保存：

```python
cv.imwrite('savejpg.jpg', img2, [int(cv.IMWRITE_JPEG_QUALITY),5])
#第一个参数是保存的路径，第二个是图像矩阵名
#第三个参数对JPEG而言，其表示的是图像的质量，用0-100的整数表示，默认为95, 这里设置成了5。 
#注意，cv2.IMWRITE_JPEG_QUALITY类型为Long，必须转换成int。

#对png图片而言，第三个参数表示的是压缩级别。从0到9,压缩级别越高，图像尺寸越小。默认级别为3
# cv2.imwrite("./cat2.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9]) 
```



### 创建/复制 图像

创建图像，需要使用numpy的函数（现在使用OpenCV-Python绑定，numpy是必装的）。如下：

```
emptyImage = np.zeros(img.shape, np.uint8) 
```

在新的OpenCV-Python绑定中，图像使用NumPy数组的属性来表示图像的尺寸和通道信息。

如果输出img.shape，将得到(500, 375, 3)，这里是以OpenCV自带的cat.jpg为示例。最后的3表示这是一个RGB图像。

也可以复制原有的图像来获得一副新图像。

```
emptyImage2 = img.copy(); 
```

如果不怕麻烦，还可以用cvtColor获得原图像的副本。

```
emptyImage3=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
#emptyImage3[...]=0 
```

后面的emptyImage3[...]=0是将其转成空白的黑色图像



### 图像匹配

cv2.matchTemplate(image, templ, method[, result]) → result

`image`是源图像，`templ`是模板图像，`method`是匹配算法

```python
import cv2
import numpy as np

img = cv2.imread("F:\\test.jpg")
template = cv2.imread("F:\\temp.jpg")

method = cv2.TM_CCOEFF
res = cv2.matchTemplate(img,template,method)
print(res)
min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
print(min_val,max_val,min_loc,max_loc) # (-21885944.0, 23648630.0, (538, 826), (193, 865))
#依次是:最小匹配度，最大匹配度，最小匹配位置，最大匹配位置

# === 
res:
 [[  236153.2      54322.766  -116610.81  ...   179690.34   -900482.1
  -1188530.1  ]
 [  352865.78    165767.44    -15731.851 ...   162352.23   -884955.56
  -1169717.1  ]
 [  428780.6     236834.       43013.016 ...    72161.41   -939501.4
  -1216983.9  ]
 ...
 [ -393566.38    140648.2     570055.6   ...   -24419.078   -23685.664
    -22954.25 ]
 [ -401979.66    134937.7     577151.1   ...   -32436.314   -31855.584
    -31222.852]
 [ -418450.88    115301.2     569662.4   ...   -41304.65    -41089.28
    -40806.918]]
```



最大匹配位置（193，865）是最相近的位置，我们标记出来：

首先我们需要先获取模板图像的尺寸

```python
find_img  = cv2.imread("temp.jpg")
find_height, find_width, find_channel = find_img.shape[::]
```

根据max_loc结果计算出中间位置

```python
pointUpLeft  = max_loc
pointLowRight = (max_loc[0]+find_width, max_loc[1]+find_height)
pointCentre   = (max_loc[0]+(find_width/2), max_loc[1]+(find_height/2))
```

为了更直观些，我们把坐标在源图中点出来并显示出图片

```python
cv2.circle(img, pointUpLeft, 2, (0, 255, 255), -1)
cv2.circle(img, pointCentre, 2, (0, 255, 255), -1)
cv2.circle(img, pointLowRight, 2, (0, 255, 255), -1)
cv2.namedWindow("Image")
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```



## ImageGrab

ImageGrab模块用于将当前屏幕的内容或者剪贴板上的内容拷贝到PIL图像内存。

### grab

ImageGrab.grab(bbox) ⇒ image, 抓取当前屏幕的快照，返回一个模式为“RGB”的图像。参数边界框用于限制只拷贝当前屏幕的一部分区域。

```python
from PIL import ImageGrab
im =ImageGrab.grab() # 抓取整个屏幕
print(im.size)  # (1920, 1080)
print(im.mode)  # RGB

im.show()
im0 = ImageGrab.grab((300, 100, 1400, 600))
im0.show()
 
print(im0.size) # (1100, 500)
print(im0.mode) # RGB
```



ImageGrab.grabclipboard() ⇒ image or list of strings or None

含义：（New in 1.1.4）抓取当前剪贴板的快照，返回一个模式为“RGB”的图像或者文件名称的列表。如果剪贴板不包括图像数据，这个函数返回空。

用户可以使用函数isinstance()来检查该函数返回的是一个有效图像对象或者其他数据。
