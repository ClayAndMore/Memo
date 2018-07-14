### csv



### ast





### functools

python2.5 引进

#### 偏函数partial

和数学中的偏函数不一样，说白了它可以帮你用一个已知函数固定其中参数的值生成一个参数少传一些的函数：

用法： new_func = partial(func, 固定参数)

```python
# coding:utf-8
from functools import partial
def func(a, b, c):
    print a, '@', b, '@', c

par_func = partial(func, 1)
print '指定一个参数'
par_func(2,3)
#par_func(0,2,3)

print '指定两个参数'
par_func = partial(func, 1, 2)
par_func(3)

print '指定三个参数'
par_func = partial(func, 1,2,3)
par_func()

### 默认参数

def default(a, b='bb',c='cc'):
    print a, b,c

par_default = partial(default, 1)
print '默认参数'
par_default(3)

## 可变参数和关键字参数
def alterable(*args, **kwargs):
    print args
    print kwargs

print '可变参数和关键字参数'
par_alterable = partial(alterable, 1,2, a='aa')
par_alterable(3,4,5,b='bb',c='cc')
```

输出：

```
指定一个参数
1 @ 2 @ 3
指定两个参数
1 @ 2 @ 3
指定三个参数
1 @ 2 @ 3
默认参数
1 3 cc
可变参数和关键字参数
(1, 2, 3, 4, 5)
{'a': 'aa', 'c': 'cc', 'b': 'bb'}
```



#### wraps

让被装饰的函数不改变func.name 和doc

```python
from functools import wraps
def my_decorator(f):
    #@wraps(f)
    def wrapper(*args, **kwds):
        print 'Calling decorated function'
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print 'Called example function'

example()
#Calling decorated function
#Called example function
print example.__name__
#'example', 去掉@wraps, 则是wrapper
print example.__doc__
#'Docstring', 去掉@wraps, 为None,也就是wrapper的doc
```

这样的目的是使其看起来更像被包裹（wrapped）的函数； 





### hashlib

使用python求字符串或文件的MD5 

字符串md5:

```python
>>> import hashlib
>>> hashlib.md5("filename.exe").hexdigest()
'2a53375ff139d9837e93a38a279d63e5'
```



求文件md5

```python
>>> import hashlib
>>> hashlib.md5(open('filename.exe','rb').read()).hexdigest()
'd41d8cd98f00b204e9800998ecf8427e'

def _get_md5(filepath):
    md5 = ''
    with open(filepath) as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        return md5

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

