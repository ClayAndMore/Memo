

### append 问题

```
>>> l=[]
>>> print l.append(2)
None
```

所以这样写是不可以的：`l = l.append(2)`

应该这样`l.append(2)`



### 默认参数为可变类型

```python
>>> def func(numbers=[], num=1):
...     numbers.append(num)
...     return numbers

>>> func()
[1]
>>> func()
[1, 1]
>>> func()
[1, 1, 1]
```

numbers 第一次生成时在内存中地址不变，后期调用实际在改变的是地址的值。

**在使用默认参数为可变类型时一定要注意。**

这样也可以用做缓存：

```python
def factorial(num, cache={}):
    if num == 0:
        return 1
    if num not in cache:
        print('xxx')
        cache[num] = factorial(num - 1) * num
    return cache[num]


print(factorial(4))
print("-------")
print(factorial(4))

---第一次调用---
xxx
xxx
xxx
xxx
24
---第二次调用---
24
```

