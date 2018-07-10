### python2.7以前的字典推导

```python
>>> a = ['a', 'b', 'c']
>>> dict((x,y) for x, y in enumerate(a))
{0: 'a', 1: 'b', 2: 'c'}
>>> dict((x,y) for x, y in enumerate(a) if x < 2)
{0: 'a', 1: 'b'}
```

