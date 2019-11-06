​	Tags:[python]

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

Python 3 可以使用直接使用 `super().xxx` 代替 `super(Class, self).xxx` :

```python
# 默认，Python 3
class B(A):
    def add(self, x):
        super().add(x)

# Python 2
class B(A):
    def add(self, x):
        super(B, self).add(x)
```

**super()**方法设计目的是用来解决多重继承时父类的查找问题，所以在单重继承中用不用 super 都没关系；但是，**使用 super() 是一个好的习惯**。一般我们在子类中需要调用父类的方法时才会这么用。

**super()**的好处**就是可以避免直接使用父类的名字.主要用于多重继承**

```python
# 明确指定 ：
class  C(P):
     def __init__(self):
             P.__init__(self)
             print 'calling Cs construtor'
# 使用super()方法 ：
class  C(P):
    def __init__(self):
            super(C,self).__init__()     #这种好处是当父类变名字时，不用改P的名字
            print 'calling Cs construtor'
 
c=C()
```



多继承时super的用法：http://python.jobbole.com/87291/

看文章时的补充：*MRO*就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。Method Resolution Order。



#### `__init__()方法`

如果在类中定义了init这个方法，python会自动调用这个方法，这个过程也叫初始化

`__init__`不能有返回值



#### `__new__()`方法

`__new__` 这个方法负责创建类实例，而 `__init__` 负责初始化类实例 。 `__new__` 函数可以用来自定义对象的创建，它的第一个参数是这个类的引用，然后是一些构造参数；返回值通常是对象实例的引用。

通常用来判断有没有这个类的实例。



#### init 和 new 的区别

`__new__`所接收的第一个参数是`cls`，而`__init__`所接收的第一个参数是`self`。

**这是因为当我们调用`__new__`的时候，该类的实例还并不存在（也就是`self`所引用的对象还不存在），所以需要接收一个类作为参数，从而产生一个实例。**

而当我们调用`__init__`的时候，实例已经存在，因此`__init__`接受`self`作为第一个参数并对该实例进行必要的初始化操作。**这也意味着`__init__`是在`__new__`之后被调用的。**



先不讨论python的旧式类，因为它已经过时了。具体看后面的新式类和旧式类。

Python的新式类允许用户重载`__new__`和`__init__`方法，且这两个方法具有不同的作用。

**`__new__`作为构造器，起创建一个类实例的作用。**

**`__init__`作为初始化器，起初始化一个已被创建的实例的作用。**

```python
class newStyleClass(object): 
    # In Python2, we need to specify the object as the base.
    # In Python3 it's default.

    def __new__(cls):
        print("__new__ is called")
        return super(newStyleClass, cls).__new__(cls) # 调用了 object 的 new 方法。

    def __init__(self):
        print("__init__ is called")
        print("self is: ", self)

newStyleClass()

# __new__ is called
# __init__ is called
# ('self is: ', <__main__.newStyleClass object at 0x108ac0b10>)
```

`__init__`函数在`__new__`函数返回一个实例的时候被调用，并且这个实例作为`self`参数被传入了`__init__`函数。



**这里需要注意的是，如果`__new__`函数返回一个已经存在的实例（不论是哪个类的），`__init__`不会被调用**

```python
obj = 12 
# obj can be an object from any class, even object.__new__(object)

class returnExistedObj(object):
    def __new__(cls):
        print("__new__ is called")
        return obj

    def __init__(self):
        print("__init__ is called")

print(returnExistedObj())

# __new__ is called
# 12
```



**如果我们在`__new__`函数中不返回任何对象，则`__init__`函数也不会被调用。**

```python
class notReturnObj(object):
    def __new__(cls):
        print("__new__ is called")

    def __init__(self):
        print("__init__ is called")

print(notReturnObj())

# __new__ is called
# None
```





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

第二个类方法，cls指的是一个类，不是非得要实例，A.class_foo(x)或a.class_foo(x), 这里的cls指得是A

第三个是静态方法，不需要对谁绑定，a.static_foo(x),A.static_foo(x)都可以。

这里可以看出类方法和静态方法是非实例化类调用而存在的。

类方法和静态方法具体区别：

@staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
@classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，**避免硬编码**（如直接调用cls,而不是类的名字.）。

一个例子可以看出它们的用途

```python
class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year) #注意这里已经返回了实例。
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string('11-09-2012')
is_date = Date.is_date_valid('11-09-2012')

```

一般一个init函数可以初始化：如Date(11,09,2012), 但是有传入(11-09-2012)这样的需求，我们可以通过类方法来预处理类的初始化。

静态方法和普通方法一样，这里可以看出式一些参数的判断。



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



#### 单例模式

`__new__`版本

```python
class Singleton(object):
    _instance=None #保存实例的引用

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._instance

one=Singleton()
two=Singleton()

print(one is two)
```

在上面的代码中，我们将类的实例和一个类变量 `_instance` 关联起来，如果 `cls._instance` 为 None 则创建实例，否则直接返回 `cls._instance`。

import版本

 mysingle.py

```python
class My_Single(object):
	def foo(self):
		pass
my_single=My_Single()

from mysingle import my_single

my_single.foo()
```

装饰器版本：

```python
def single(cls):
	instances={}
	def getinstance(*args,**kwargs):
		if cls not in instances:
			instances[cls]=cls(*args,**kwargs)
		return instances[cls]
	return getinstance

@single
class MyClass(object):
    a=1

a=MyClass()
b=MyClass()
print(a is b)
```



### 新式类和经典类

**Python 2.x中默认都是经典类，只有显式继承了object才是新式类**

```python
class A:  # A是旧式类，因为没有显示继承object
    pass

class B(A):  # B是旧式类，因为B的基类A是旧式类
    pass
```

**Python 3.x中默认都是新式类，不必显式的继承object**

```python
class A(object):  # A是新式类，因为显式继承object
    pass

class B(A):  # B是新式类，因为B的基类A是新式类
    pass
```



#### `__class__`

`__class__ `只有实例可以调用，表明实例属于哪个类，内容包括了__module__的信息

**对新式类的实例执行a.class与type(a)的结果是一致的，对于旧式类来说就不一样了。**

```python
class A:
    pass

class B(A):
    pass

a=A()
b=B()                  # python2          python3
print(type(a))         <type 'instance'>  <class '__main__.A'>
print(a.__class__)		 __main__.A				  <class '__main__.A'>
print(type(A))         <type 'classobj'>  <class 'type'>
print(type(b))			   <type 'instance'>  <class '__main__.B'>
print(b.__class__)     __main__.B         <class '__main__.B'>
print(type(B))         <type 'classobj'>  <class 'type'>
```

Class 和 type 对任何对象返回的结果都应该是一样的，但再python2中对类显得很不和谐，所以在python中所有都同一了。

#### 继承搜索的顺序

MRO(Method Resolution Order， 方法解析顺序)

经典类多继承属性搜索顺序: 先深入继承树左侧，再返回，开始找右侧; **深度优先**

新式类多继承属性搜索顺序: 先水平搜索，然后再向上移动, **广度优先**

```python
class A():
    def name(self):
        return 'A'
 
class B(A):
    pass
 
class C(A):
    def name(self):
        return 'C'
 
class D(B, C):
    pass
 
if __name__ == '__main__':
	print D().name()
  # 经典类输出： A ,  D->B->A->C
  # 心式类输出：C,    D->B->C->A
```



#### `__slots__`

新式类增加了`__slots__`内置属性, 可以把实例属性的种类锁定到`__slots__`规定的范围之中。

比如只允许对A实例添加name和age属性:

```python
# -*- coding:utf-8 -*-  

class A(object):  
    __slots__ = ('name', 'age') 

class A1():  
    __slots__ = ('name', 'age') 
	
a = A()
a1 = A1()

a.name1 = "a"
a1.name1 = "a1"
```

A是新式类添加了__slots__ 属性,所以只允许添加 name age,`__slots__ = ('name', 'age') `加一句这个可以只允许定义这两个属性，无法在实例中添加，这条命令只对当前类起作用，**对子类无效**

A1经典类__slots__ 属性没用：

```
Traceback (most recent call last):
  File "t.py", line 13, in <module>
    a.name1 = "a"
AttributeError: 'A' object has no attribute 'name1'
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

可看闭包中对其的使用。



#### 如何使用特殊方法

通常你的代码无需直接使用特殊方法，除非有大量等元编程存在。

通过内置等函数（len, iter, str,）等来使用特殊方法是最好的选择。



### Mixin

Mixin编程是一种开发模式，是一种**将多个类中的功能单元的进行组合的利用的方式**。

像继承，但和继承不同。

通常**mixin并不作为任何类的基类**，也不关心与什么类一起使用，而是**在运行时动态的同其他零散的类一起组合使用**。
使用mixin机制有如下好处：

* 可以在不修改任何源代码的情况下，对已有类进行扩展；

* 可以保证组件的划分；

* 可以根据需要，使用已有的功能进行组合，来实现“新”类；

* 很好的避免了类继承的局限性，因为新的业务需要可能就需要创建新的子类。

在举例子之前，我们需要先熟悉几个关键字：

#### `__bases__`

返回一个元组，该元组元素是类的基类

```python
class t0(object):
    pass

class t1(t0):
    pass

print t0.__bases__   # (<type 'object'>,)
print t1.__bases__   # (<class '__main__.t0'>,)
```



#### `___mro__`

返回一个元祖， 元素是该类的依次继承的类

```python
class t0(object):
    pass

class t1(t0):
    pass

print t0.__mro__  # (<class '__main__.t0'>, <type 'object'>)
print t1.__mro__  # (<class '__main__.t1'>, <class '__main__.t0'>, <type 'object'>)
```



#### eg

```python
def mixin(pyclass, pyMixinClass, b=1):
    if b:
        pyclass.__bases__ += (pyMixinClass,)
    elif pyMixinClass not in pyclass.__bases__:
        pyclass.__bases__ = (pyMixinClass,) + pyclass.__bases__
    else:
        pass

class MinxinClass:
    def p(self):
        print 'i am mixin p'

class t0(object):
    def p(self):
        print 'i am p1'

class t1(t0):
    pass

class t2(t0):
    pass

if __name__ == '__main__':
    t_1 = t1()
    t_1.p()
    mixin(t1, MinxinClass, b=0)
    t_1 = t1()
    t_1.p()

    mixin(t2, MinxinClass)
    t_2 = t2()
    t_2.p()
    
out:
i am p1
i am mixin p
i am p1
```

会有些输出bases中左边的类的方法， 注意：

```
>>> a=('s','ss')
>>> ('sss',)+a
('sss', 's', 'ss')

>>> a+=('sss',)
>>> a
('s', 'ss', 'sss')
```

所以注意pyMixin加的顺序。



**mixin 类的继承：**

```python
class t3(MixinClass, t0):
    pass

class t4(t0, MixinClass):
    pass
   
class t5(t0, MixinClass):
     def p(self):
        print 'i am p5'
    
if __name__ == '__main__':
    t_3 = t3()
    t_3.p()    # i am mixin p
    t_4 = t4()
    t_4.p()    #  i am p1
    t_5 = t5()
    t_5.p()    # i am p5
```

原理上和bases及mro属性是一样的。