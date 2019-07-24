tags:[python, py_lib] 

### json

python和json类型转换：
```
| Python           | JSON   |  | JSON          | Python    |
| ---------------- | ------ |  | ------------- | --------- |
| dict             | object |  | object        | dict      |
| list, tuple      | array  |  | array         | list      |
| str, unicode     | string |  | string        | unicode   |
| int, long, float | number |  | number (int)  | int, long |
| True             | true   |  | number (real) | float     |
| False            | false  |  | true          | True      |
| None             | null   |  | null          | None      |
```

注意： json的str转会python变成了unicode而不是str

### dumps

json.dumps 用于将 Python 对象编码成 JSON 字符串。

```python
In [1]: import json
In [2]: data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]
In [3]: json = json.dumps(data)
In [4]: print json
[{"a": 1, "c": 3, "b": 2, "e": 5, "d": 4}]
```

注： 会将中文编译成unicode，并其他字段也会变成unicode,

如果想将中文变成ascii 的str， 可使用 `encode('utf-8')`

一些参数：

#### ensure_asci

ensure_ascii：默认值True，只做两件事：

1. 如果有非ASII的字符， 用utf-8解码。
2. 确保dumps后的数据为 str 字符数组。
3. 如果dict内含有non-ASCII的字符，则会解码成utf-8的数据，去掉了u, 双斜杠转义单斜杠

e.g:

```python
>>> a={"aa": 123, "bb":"BBB", "cc":"中文"}
>>> a
{'aa': 123, 'cc': '\xe4\xb8\xad\xe6\x96\x87', 'bb': 'BBB'}
>>> json.dumps(a)
'{"aa": 123, "cc": "\\u4e2d\\u6587", "bb": "BBB"}'  # 第一点
>>> type(json.dumps(a))
<type 'str'>    # 第二点

>>> a={"aa": 123, "bb":"BBB", "cc":u"中文"}
>>> a
{'aa': 123, 'cc': u'\u4e2d\u6587', 'bb': 'BBB'} # 第三点，和上方json.dumps后的结果做比较。
```

设置成False后，

```python
  >>> a={'a':'aa', 'b':'彻底'}
  >>> json.dumps(a)
  '{"a": "aa", "b": "\\u5f7b\\u5e95"}'
  >>> '彻底'.decode('utf-8')
  u'\u5f7b\u5e95
  >>> '彻底'
  '\xe5\xbd\xbb\xe5\xba\x95'
  >>> json.dumps(a, ensure_ascii=False)
  '{"a": "aa", "b": "\xe5\xbd\xbb\xe5\xba\x95"}'
```

  ​

#### indent

indent：是一个非负的整型，如果是0，或者为空，则一行显示数据，否则会换行且按照indent的数量显示前面的空白，这样打印出来的json数据也叫pretty-printed json



#### encoding

*encoding*：默认是UTF-8，设置json数据的编码方式。

```python

```





### loads

json.loads 解码 JSON 数据。该函数返回 Python 字段的数据类型。

```python
import json
jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
text = json.loads(jsonData)
print text
{u'a': 1, u'c': 3, u'b': 2, u'e': 5, u'd': 4}
```

注意： json的str转会python变成了unicode而不是str

**如果里面用单引号，外面用双引号也会解析失败**，**规定里面只能用双引号**，如果想loads里面是单引号的数据：

```python
>>> import ast
>>> s = "{'username':'dfdsfdsf'}"
>>> ast.literal_eval(s)
{'username': 'dfdsfdsf'}
>>> type(s)
<dict>
```



### dump

dump(f), 

```python
>>> with open('test.conf', 'w') as f:
...  json.dump({'b':'bb','c':'cc'},f)
```

生成文件流​



### load

json.load(f),

f为从文件读取出来的文件流，**注意该文件内的josn格式 只能用双引号：**

```
{
    "a": "aaaa",
    "b": "bbbbbbb"
}
```



### Python对象的转换

对python对象的转换： 

```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
print(json.dumps(s))
```

这样会毫不留情的得到一个TypeError.可选参数`default`就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为`Student`专门写一个转换函数，再把函数传进去即可：

```python
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

print(json.dumps(s, default=student2dict))
```



现在我们可以偷个懒，把任意`class`的实例变为`dict`：

```
print(json.dumps(s, default=lambda obj: obj.__dict__))
```



同样的道理，如果我们要把JSON反序列化为一个`Student`对象实例，`loads()`方法首先转换出一个`dict`对象，然后，可选参数object_hook`函数负责把`dict`转换为`Student实例：

```python
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))

<__main__.Student object at 0x10cd3c190>
打印出的是反序列化的Student实例对象。
```


