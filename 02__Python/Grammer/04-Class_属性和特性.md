Tags:[python]

### python自省

这个也是python彪悍的特性.

自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.简单一句就是运行时能够获得对象的类型.比如type(),dir(),getattr(),hasattr(),isinstance().

#### getattr()

Class 文档里有说明

#### hasattr(object, name)

说明：判断对象object是否包含名为name的特性（hasattr是通过调用getattr(ojbect, name)是否抛出异常来实现的）。



### 对象的属性

Python一切皆对象(object)，每个对象都可能有多个属性(attribute)。Python的属性有一套统一的管理方案。

#### 属性的`_dict_`系统

对象的属性储存在对象的`__dict__`属性中。`__dict__`为一个词典，键为属性名，对应的值为属性本身。

```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age

summer = chicken(2)

print(bird.__dict__)
print(chicken.__dict__)
print(summer.__dict__)
```

输出结果：

```
{'__dict__': <attribute '__dict__' of 'bird' objects>, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'bird' objects>, 'feather': True, '__doc__': None}


{'fly': False, '__module__': '__main__', '__doc__': None, '__init__': <function __init__ at 0x2b91db476d70>}


{'age': 2}
```

可以看到，Python中的属性是分层定义的，比如这里分为object/bird/chicken/summer这四层。当我们需要调用某个属性的时候，Python会一层层向上遍历，直到找到那个属性。(某个属性可能出现再不同的层被重复定义，Python向上的过程中，会选取先遇到的那一个，也就是比较低层的属性定义)。



#### `_getattr_`

我们可以用`__getattr__(self, name)`来查询即时生成的属性。当我们查询一个属性时，如果通过`__dict__`方法无法找到该属性，那么Python会调用对象的`__getattr__`方法，来即时生成该属性。比如:

```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age
    def __getattr__(self, name):
        if name == 'adult':
            if self.age > 1.0: return True
            else: return False
        else: raise AttributeError(name)

summer = chicken(2)

print(summer.adult)
summer.age = 0.5
print(summer.adult)

print(summer.male)
```

每个特性需要有自己的处理函数，而__getattr__可以将所有的即时生成属性放在同一个函数中处理。__getattr__可以根据函数名区别处理不同的属性。比如上面我们查询属性名male的时候，raise AttributeError。

(Python中还有一个__getattribute__特殊方法，用于查询任意属性。__getattr__只能用来查询不在__dict__系统中的属性)
__setattr__(self, name, value)和__delattr__(self, name)可用于修改和删除属性。它们的应用面更广，可用于任意属性。



#### 特性(property)

同一个对象的不同属性之间可能存在依赖关系。当某个属性被修改时，我们希望依赖于该属性的其他属性也同时变化。这时，我们不能通过`__dict__`的方式来静态的储存属性。Python提供了多种即时生成属性的方法。其中一种称为特性(property)。特性是特殊的属性。比如我们为chicken类增加一个特性adult。当对象的age超过1时，adult为True；否则为False：

```python
class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age
    def getAdult(self):
        if self.age > 1.0: return True
        else: return False
    adult = property(getAdult)   # property is built-in

summer = chicken(2)

print(summer.adult)
summer.age = 0.5
print(summer.adult)
```

特性使用内置函数property()来创建。property()最多可以加载四个参数。前三个参数为函数，分别用于处理查询特性、修改特性、删除特性。最后一个参数为特性的文档，可以为一个字符串，起说明作用。
进一步说明：

```
class num(object):
    def __init__(self, value):
        self.value = value
    def getNeg(self):
        return -self.value
    def setNeg(self, value):
        self.value = -value
    def delNeg(self):
        print("value also deleted")
        del self.value
    neg = property(getNeg, setNeg, delNeg, "I'm negative")

x = num(1.1)
print(x.neg)
x.neg = -22
print(x.value)
print(num.neg.__doc__)
del x.neg
```

上面的num为一个数字，而neg为一个特性，用来表示数字的负数。当一个数字确定的时候，它的负数总是确定的；而当我们修改一个数的负数时，它本身的值也应该变化。这两点由getNeg和setNeg来实现。而delNeg表示的是，如果删除特性neg，那么应该执行的操作是删除属性value。property()的最后一个参数("I'm negative")为特性negative的说明文档。

#### `@property`

内置的`@property`装饰器就是负责把一个方法变成属性调用的：

```python
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```

`@property`的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上`@property`就可以了，此时，`@property`本身又创建了另一个装饰器`@score.setter`，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：

```
>>> s = Student()
>>> s.score = 60 # OK，实际转化为s.set_score(60)
>>> s.score # OK，实际转化为s.get_score()
60
>>> s.score = 9999
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!


```

注意到这个神奇的`@property`，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。

还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性：

```
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth



```

上面的`birth`是可读写属性，而`age`就是一个**只读**属性，因为`age`可以根据`birth`和当前时间计算出来。



#### getattr()

```python
def getattr(object, name, default=None): # known special case of getattr
    """
    getattr(object, name[, default]) -> value
    
    Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    """
    pass
```

`getattr(x, y, z) = x.y`  如果y不存在则返回z, 没有z则抛出异常。



#### setattr()

```python
def setattr(p_object, name, value): # real signature unknown; restored from __doc__
    """
    setattr(object, name, value)
    
    Set a named attribute on an object; setattr(x, 'y', v) is equivalent to
    ``x.y = v''.
    """
    pass
```

嗯 说的很明白： `setattr(x, 'y', v) = x.y = v`

