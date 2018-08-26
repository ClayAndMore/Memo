### 类

```python
# 定义
class Bird(object):
    have_feather = True
    way_of_reproduction = 'egg'
    # 方法
    def move(self,dx,dy):
    position = [0,0]
    position[0] = position[0]+dx
    position[1] = position[1]+dy
    return position 
    
# 使用
summer = Bird()
print summer.way_of_reproduction

# 继承
class Chicken(Bird);
    way_of_move = 'walk'
```

方法中有个self，方便我们引用自身对象，无论用或不用，第一个参数必须是self.传参可以不传.这个相当与其他语言中的this，代表这个实例，可以在方法中用本类的属性

#### 访问限制

如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线`__`，在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问，所以，我们把Student类改一改：

```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
```

改完后，对于外部代码来说，没什么变动，但是已经无法从外部访问`实例变量.__name`和`实例变量.__score`了，子类也不能访问，只有自己能访问。

`_abc`单下划线是保护变量，子类能访问。外部不能访问。更多看作用域。

#### `__slots__`

只允许对Student实例添加`name`和`age`属性。

为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的`__slots__`变量，来限制该class实例能添加的属性：

```
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称


```

然后，我们试试：

```python
>>> s = Student() # 创建新的实例
>>> s.name = 'Michael' # 绑定属性'name'
>>> s.age = 25 # 绑定属性'age'
>>> s.score = 99 # 绑定属性'score'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'score'
```

由于`'score'`没有被放到`__slots__`中，所以不能绑定`score`属性，试图绑定`score`将得到`AttributeError`的错误。

使用`__slots__`要注意，`__slots__`定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：

```
>>> class GraduateStudent(Student):
...     pass
...
>>> g = GraduateStudent()
>>> g.score = 9999


```

除非在子类中也定义`__slots__`，这样，子类实例允许定义的属性就是自身的`__slots__`加上父类的`__slots__`。

#### super()方法

http://python.jobbole.com/87291/



#### `__init__()方法`

python中有一些特殊方法，特殊方法的特点是名字前后有两个下划线
如果在类中定义了init这个方法，python会自动调用这个方法，这个过程也叫初始化

#### `__new__()`方法

`__new__` 这个方法负责创建类实例，而 `__init__` 负责初始化类实例 。 `__new__` 函数可以用来自定义对象的创建，它的第一个参数是这个类的引用，然后是一些构造参数；返回值通常是对象实例的引用。

通常用来判断有没有这个类的实例。





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

#### 使用特殊方法_getattr_

我们可以用__getattr__(self, name)来查询即时生成的属性。当我们查询一个属性时，如果通过__dict__方法无法找到该属性，那么Python会调用对象的__getattr__方法，来即时生成该属性。比如:

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

#### 静态方法@staticmethod和@classmethod

类中有三个方法，实例方法，静态方法，和类方法。

```python
 
class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)
 
    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)
 
    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x
 
a=A()
```

第一个实例方法，self需要为self传递一个实例，调用时是a.foo(x)。不能A.foo(x)。这里self指的是a.

第二个类方法，cls指的是一个类，不是非得要实例，A.class_foo(x)或a.class_foo(x)。这里的cls指得是A

第三个是静态方法，不需要对谁绑定，a.static_foo(x),A.static_foo(x)都可以。



#### 鸭子类型

当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”

我们并不关心对象是什么类型，到底是不是鸭子，只关心行为。

如果有个飞机类，行为函数fly()。飞。 鸟类，也有个fly().

```python
class Airplane(object):
    def fly(self):
        print('i can fly,i am a airplane')

class Bird(object):
    def fly(self):
        print('i can fly,i am a bird')

def who(object):
    object.fly()

a=Airplane()
b=Bird()
who(a) #i can fly,i am a airplane
who(b) #i can fly,i am a bird
```



### 特殊方法

python是多范式语言，既可以面向对象，也可以函数式，依赖于python的对象中的特殊方法。
格式：`_特殊方法名_()`
运算符（如+）、内置函数（如len()）、表元素（如list[3]），有特殊方法的函数可以被认为对象等。

这些方法不光是类有，函数也有，这可能是废话。

#### `__len__`

如下，对应内置函数len

另： 如果x是一个**内置类型**的实例，那么len(x)的速度会非常快，原因是CPython会从一个C结构体里读取对象的长度。



#### `__dict__`

用它存储用户属性，对于方法dir()，可以列出所有其属性。



#### `__getitem__`

```python
class Weekday:
    day = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Satur', 'Sun']

    def __init__(self):
        self._day = self.day
    def __len__(self):
        print '__len__'
        return len(self._day)
    def __getitem__(self, position):
        print '__getitem__'
        return self._day[position]

w = Weekday()

print len(w)

print w[2]

out:
__len__
7
__getitem__
Wed
```

**[] 会触发getitem方法，** 所以这个类还支持切片，迭代等。





#### `__contains__`

In 方法



#### `__repr__`

对应内置函数repr,  字符串描述对象。

```python
    def __repr__(self):
        return 'Weekday : %s'%self._day
    
    print w
    out:
        Weekday : ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Satur', 'Sun']
```

这个功能与eval也可以对应。打印出的结果直接放到eval里，通常可以获得原来的对象。
比如：
t1=datetime.datetime.now()
print repr(t1)
结果是
datetime.datetime(2014, 9, 9, 6, 34, 29, 756000)



#### `__str__`

对于内置函数str().

print 先找str,后repr



#### `__bool__`

bool(x)的背后是调用`x.__bool__()` 的结果，如果不存在`__bool__` 方法，

那么bool(x)会尝试`x.__len()` 方法， 若返回0，则False, 否则则True.



#### `__call__`

如果类定义了这个方法，那么它的实例可以作为函数调用。

对应是`callable(obj)` 函数，检查对象是否可以调用。

```python
class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items) # 让一个list内部随机排列
    def pick(self):
        try:
            return self._items.pop()
     	except IndexError:
            raise LookupError('pick from empty BingoCage')
            
    def __call__(self):
        return self.pick()
    
bingo = BingoCage(range(3))
bingo.pick()
1
bingo()
0
callable(bingo)
True   
```



#### `__defaults__`

它的值是一个元组，里面保存着定位参数和关键字参数等默认值。

#### `__kwdefaults__`

仅限关键字的默认值在这里。

#### `__code__`

参数名称在这里。





#### 如何使用特殊方法

通常你的代码无需直接使用特殊方法，除非有大量等元编程存在。

通过内置等函数（len, iter, str,）等来使用特殊方法是最好的选择。