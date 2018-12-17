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
import yaml

data = dict(
    A = 'a',
    B = dict(
        C = 'c',
        D = 'd',
        E = 'e',
    )
)

with open('data.yml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)
```

运行结果：

```yaml
A: a
B:
  C: c
  D: d
  E: e
```

default_flow_style 表示起新行表示结构.



## 问题

### 中文

在配置文件中有中文的时候，我们像打印出来，由于字符编码的问题是有异常的，下面这样的代码可以正常打印：

```python
f=open('data.yaml',)
data = yaml.load(f)
print data
print (repr(data).decode('unicode-escape'))
```



传输的时候不用decode，也没有问题。



### True | False

设置成： 字段值on 或 off 会识别为Ture 或 False



## ConfigParser

`ConfigParser`模块在python3中修改为`configparser`