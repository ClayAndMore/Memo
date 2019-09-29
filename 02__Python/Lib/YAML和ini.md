Tags:[python, py_lib]

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

**NI文件**是一个无固定标准格式的[配置文件]。

它以简单的文字与简单的结构组成，常常使用在[Windows操作系统])，或是其他操作系统上。

INI文件的命名来源，是取自英文“初始（Initial）”的首字缩写，正与它的用途——初始化程序相应。有时候，INI文件也会以不同的扩展名，如“.CFG”、“.CONF”、或是“.TXT”代替。

它能够读取ini格式的文件：

```ini
[database]
db_host=localhost
db_port=27017
db_name=bulkscan
[smb]
name=bulkscan_smb
mount_root=%(root)s/var/mointpoints/bulkscan/smb
collection=smb_scan
[sftp]
name=bulkscan_sftp
mount_root=%(root)s/var/mointpoints/bulkscan/sftp
collection=sftp_scan
[cloud2]
url=http://127.0.0.1:80/api
[misc]
enabled=true
scan_period=10
max_conn=1
```



### read and write

```python
>>> import ConfigParser
>>> conf=ConfigParser.ConfigParser()
>>> conf.read('bulk_scan.cfg')         #该文件不在该目录，或没有找到会返回空
[]
>>> conf.read('/conf/bulk_scan.cfg')
['/conf/bulk_scan.cfg']
>>> a=conf.read('/ng8w/conf/bulk_scan.cfg')
>>> a
['/conf/bulk_scan.cfg']

>>> conf.get('smb', 'name')                 #得到某个节点名的某属性， 返回为str
'bulkscan_smb'
>>> conf.getint(section,option)             #得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。
>>> conf.set('Section1', 'name', 'jack')    #添加某个节点的某值

>>> conf.options('smb') 					#获得某个节点的所有属性
['name', 'mount_root', 'collection', 'pass']

>>> conf.sections()                         #得到所有节点
['database', 'smb', 'sftp', 'cloud2', 'misc']
 
>>> conf.items('misc')                      # 得到该section的所有键值对
[('enabled', 'true'), ('scan_period', '60'), ('max_conn', '1')]

>>> remove_option(section, option)
# 从指定section中删除指定option，如果section不存在，抛出NoSectionError异常；如果option存在，则删除，并返回True；否则返回false

>>> remove_section(section)
# 从配置文件中删除指定的section，如果section确实存在，返回true，否则返回false。

>>> conf.add_section('Section2')   			# 添加conf节点

>>> with open('test.cfg', 'w') as fw:       # 写文件
...  conf.write(fw)
... 

```



### RawConfigParser

ConfigParser类继承了RawconfigParse, 可以视这两个类一样

```python
config = RawConfigParser()
if not config.read(filepath):
    raise ValueError("No valid config file found!")
return config
```

