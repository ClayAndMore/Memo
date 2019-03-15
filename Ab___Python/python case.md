

### append 问题

```
>>> l=[]
>>> print l.append(2)
None
```

所以这样写是不可以的：`l = l.append(2)`

应该这样`l.append(2)`



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



### python2.7以前的字典推导

```python
>>> a = ['a', 'b', 'c']
>>> dict((x,y) for x, y in enumerate(a))
{0: 'a', 1: 'b', 2: 'c'}
>>> dict((x,y) for x, y in enumerate(a) if x < 2)
{0: 'a', 1: 'b'}
```

