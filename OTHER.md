递归遍历目录：

**一.递归方法**

```python
 #coding:utf-8
 import os
 allfile=[]
 def getallfile(path):
  allfilelist=os.listdir(path)
  for file in allfilelist:
   filepath=os.path.join(path,file)
   #判断是不是文件夹
   if os.path.isdir(filepath):
    getallfile(filepath)
   allfile.append(filepath)
  return allfile

 if __name__ == '__main__':

  path="C:\Users\zs\PycharmProjects\demo"
  allfiles=getallfile(path)

  for item in allfiles:
   print item
```