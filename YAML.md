## YAML

### 语法



### python 读取

#### load

从配置文件中读取，类似与json的loads，将某一格式换成python理解的格式

```python
import yaml,os

with open('chinese_yaml.conf') as f:
    y = yaml.load(f)
print str(y), type(y)
```

此时y 是个dict。



#### dump

```python
# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import yaml

s = 'I have an apple'
print yaml.dump(s)

lists = ['zhangsan', 'lisi', 'wangwu', 'zhaoliu']
print yaml.dump(lists)

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person('zhangsan', 19)
p2 = Person('lisi', 20)
p3 = Person('wangwu', 21)

persons = [p1, p2, p3]

print yaml.dump(persons)
```

运行结果：

```
I have an apple
...

[zhangsan, lisi, wangwu, zhaoliu]

- !!python/object:__main__.Person {age: 19, name: zhangsan}
- !!python/object:__main__.Person {age: 20, name: lisi}
- !!python/object:__main__.Person {age: 21, name: wangwu}
```





## 问题

### 中文

在配置文件中有中的时候