#### csv







### ast





### hashlib

使用python求字符串或文件的MD5 

```python

```





求文件md5

```python

```



较大文件处理：

```python
import hashlib
import os

def get_md5_02(file_path):
  f = open(file_path,'rb')  
  md5_obj = hashlib.md5()
  while True:
    d = f.read(8096)
    if not d:
      break
    md5_obj.update(d)
  hash_code = md5_obj.hexdigest()
  f.close()
  md5 = str(hash_code).lower()
  return md5

if __name__ == "__main__":
  file_path = r'D:\test\test.jar'
  md5_02 = get_md5_02(file_path)
  print(md5_02)
```

