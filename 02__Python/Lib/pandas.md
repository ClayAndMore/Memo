文档： https://www.pypandas.cn

pip install  pandas



```python 
>>> import pandas as pd
>>> df = pd.DataFrame()
>>> df
Empty DataFrame
Columns: []
Index: []
```


数据结构：
| 维数 | 名称      | 描述                               |
| ---- | --------- | ---------------------------------- |
| 1    | Series    | 带标签的一维同构数组               |
| 2    | DataFrame | 带标签的，大小可变的，二维异构表格 |



```
>>> import numpy as np
>>> s=pd.Series([1, 3, 5, np.nan, 6, 8])
>>> s
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```



## DataFrame 数据帧
数据帧(DataFrame)是二维数据结构，即数据以行和列的表格方式排列。
数据帧(DataFrame)的功能特点：

- 潜在的列是不同的类型
- 大小可变
- 标记轴(行和列)
- 可以对行和列执行算术运算

数据帧的结构体：

```
    columns columns  columns
    +------+-------+---------+
row |      |       |         |
    +------------------------+
row |      |       |         |
    +------------------------+
row |      |       |         |
    +------+-------+---------+
```



### 函数结构

`pandas.DataFrame( data, index, columns, dtype, copy)` 

构造函数的参数如下: 

| 参数      | 描述                                                         |
| --------- | ------------------------------------------------------------ |
| `data`    | 数据采取各种形式，如:`ndarray`，`series`，`map`，`lists`，`dict`，`constant`和另一个`DataFrame`。 |
| `index`   | 对于行标签，要用于结果帧的索引是可选缺省值`np.arrange(n)`，如果没有传递索引值。 |
| `columns` | 对于列标签，可选的默认语法是 - `np.arange(n)`。 这只有在没有索引传递的情况下才是这样。 |
| `dtype`   | 每列的数据类型。                                             |
| `copy`    | 如果默认值为`False`，则此命令(或任何它)用于复制数据。        |



### 创建

从上方data中可以看到：

Pandas数据帧(*DataFrame*)可以使用各种输入创建，如 - 

- 列表
- 字典
- 系列
- Numpy ndarrays
- 另一个数据帧(*DataFrame*)



创建基本数据帧是空数据帧。

```python
import pandas as pd
df = pd.DataFrame()
print df

out:
Empty DataFrame
Columns: []
Index: []
```



#### 从列表创建

```python
import pandas as pd
data = [1,2,3,4]
df = pd.DataFrame(data)
print df
out：
     0
0    1
1    2
2    3
3    4

data = [['Alex',10],['Bob',12],['Clarke',13]]
df = pd.DataFrame(data,columns=['Name','Age'])
print df

      Name      Age
0     Alex      10
1     Bob       12
2     Clarke    13

data = [['Alex',10],['Bob',12],['Clarke',13]]
df = pd.DataFrame(data,columns=['Name','Age'],dtype=float) #指定数据类型
print df

      Name     Age
0     Alex     10.0
1     Bob      12.0
2     Clarke   13.0

# 某元素未对其的长度
data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
df = pd.DataFrame(data)
print df
  a    b      c
0   1   2     NaN
1   5   10   20.0

# 指定列
data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
df1 = pd.DataFrame(data, index=['first', 'second'], columns=['a', 'b'])
df2 = pd.DataFrame(data, index=['first', 'second'], columns=['a', 'b1'])
print df1
print df2

#df1 output
         a  b
first    1  2
second   5  10

#df2 output
         a  b1
first    1  NaN
second   5  NaN
```





#### 从字典创建



```python
import pandas as pd
data = {'Name':['Tom', 'Jack', 'Steve', 'Ricky'],'Age':[28,34,29,42]}
df = pd.DataFrame(data)
print df
      Age      Name
0     28        Tom
1     34       Jack
2     29      Steve
3     42      Ricky

# 指定索引
import pandas as pd
data = {'Name':['Tom', 'Jack', 'Steve', 'Ricky'],'Age':[28,34,29,42]}
df = pd.DataFrame(data, index=['rank1','rank2','rank3','rank4'])
print df

         Age    Name
rank1    28      Tom
rank2    34     Jack
rank3    29    Steve
rank4    42    Ricky

```



#### 从Series创建

```python
import pandas as pd

d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
      'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}

df = pd.DataFrame(d)
print df

      one    two
a     1.0    1
b     2.0    2
c     3.0    3
d     NaN    4

```



### 列添加和删除

```python
import pandas as pd

d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
      'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}

df = pd.DataFrame(d)

# 添加新列
df['three']=pd.Series([10,20,30],index=['a','b','c'])
print df

# 添加新列，通过已存在的列
df['four']=df['one']+df['three']

print df

out: 
     one   two   three
a    1.0    1    10.0
b    2.0    2    20.0
c    3.0    3    30.0
d    NaN    4    NaN

      one   two   three    four
a     1.0    1    10.0     11.0
b     2.0    2    20.0     22.0
c     3.0    3    30.0     33.0
d     NaN    4     NaN     NaN
```

删除：

```python
df.pop("two")
print(df)
del df["one"]
print(df)

   one  three  four
a  1.0   10.0  11.0
b  2.0   20.0  22.0
c  3.0   30.0  33.0
d  NaN    NaN   NaN
   three  four
a   10.0  11.0
b   20.0  22.0
c   30.0  33.0
d    NaN   NaN
```



### 行

#### 选择

```python
import pandas as pd

d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
     'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}
df = pd.DataFrame(d)

	 one  two
a  1.0    1
b  2.0    2
c  3.0    3
d  NaN    4

# 按标签索引选择：
print(df.loc['b'])
one    2.0
two    2.0
Name: b, dtype: float64
    
# 按位置选择
print(df.iloc[2])
one    3.0
two    3.0
Name: c, dtype: float64
    
# 行切片
print(df[2:4]
   one  two
c  3.0    3
d  NaN    4
```





#### 添加

`DataFrame.append(other, ignore_index=False, verify_integrity=False, sort=None)`

向dataframe对象中添加新的行，如果添加的列名不在dataframe对象中，将会被当作新的列进行添加
* other：DataFrame、series、dict、list这样的数据结构
* ignore_index：默认值为False，如果为True则不使用index标签
* verify_integrity ：默认值为False，如果为True当创建相同的index时会抛出ValueError的异常
* sort：boolean，默认是None，该属性在pandas的0.23.0的版本才存在。

```python
# 添加DataFrame
df = pd.DataFrame([[1, 2], [3, 4]], columns = ['a','b'])
df2 = pd.DataFrame([[5, 6], [7, 8]], columns = ['a','b'])

df = df.append(df2)
print df

   a  b
0  1  2
1  3  4
0  5  6
1  7  8

# 添加字典
# 如果不设置ignore_index, 会提示：
# TypeError: Can only append a Series if ignore_index=True or if the Series has a name
# 一般只能添加Series类型，设置后可以添加其他类型
data = pd.DataFrame()
a = {"x":1,"y":2}
data = data.append(a,ignore_index=True)
print(data)

     x    y
0  1.0  2.0

# 添加series
# 当dataframe使用append方法添加series的时候，必须要设置name，设置name名称将会作为index的name。
# 或者使用ignore_index参数不添加name.
series = pd.Series({"x":1,"y":2},name="a")
data = data.append(series)
print(data)
     x    y
a  1.0  2.0

# 添加list
data = pd.DataFrame()
a = [1,2,3]
data = data.append(a)
print(data)
   0
0  1
1  2
2  3

data = pd.DataFrame()
data = data.append([[1,2,3]])
print(data)
   0  1  2
0  1  2  3

data = pd.DataFrame()
data = data.append([[[1,2,3]]])
print(data)
           0
0  [1, 2, 3]

data = pd.DataFrame()
data = data.append([[1,2,3],[4,5,6]])
print(data)
   0  1  2
0  1  2  3
1  4  5  6

# 多次添加后的索引变化
>>> data = pd.DataFrame()
>>> data = data.append([[1,2,3],[4,5,6]])
>>> data = data.append([[7,8,9],[10,11,12]])
>>> data
    0   1   2
0   1   2   3
1   4   5   6
0   7   8   9
1  10  11  12

# 去掉重复索引
>>> data = pd.DataFrame()
>>> data = data.append([[1,2,3],[4,5,6]], ignore_index=True)
>>> data = data.append([[7,8,9],[10,11,12]], ignore_index=True)
>>> data
    0   1   2
0   1   2   3
1   4   5   6
2   7   8   9
3  10  11  12
```



**每次追加后要重新赋值给原pd, 不然是没有保存到当前的pd的：**

```
>>> data = pd.DataFrame()
>>> a = [[1,2,3],[4,5,6]]
>>> data.append(a)
   0  1  2
0  1  2  3
1  4  5  6
>>> data.append([[7,8,9],[10,11,12]])
    0   1   2
0   7   8   9
1  10  11  12
>>> data
Empty DataFrame
Columns: []
Index: []
```



#### 删除

```python
df = pd.DataFrame([[1, 2], [3, 4]], columns = ['a','b'])
df2 = pd.DataFrame([[5, 6], [7, 8]], columns = ['a','b']) #没有指定ignore_index，标签会重复

df = df.append(df2)

# Drop rows with label 0
df = df.drop(0)

print df
  a b
1 3 4
1 7 8
# 一共有两行被删除，因为这两行包含相同的标签0

# 删除指定index
>>> data = pd.DataFrame()
>>> data = data.append(pd.Series({"x":1,"y":2},name="a"))
>>> data = data.append(pd.Series({"x":3,"y":4},name="b"))
>>> data
     x    y
a  1.0  2.0
b  3.0  4.0
>>> data.drop('b')
     x    y
a  1.0  2.0
>>> data
     x    y
a  1.0  2.0
b  3.0  4.0
>>> data = data.drop('b')  #还是要重新赋值
>>> data
     x    y
a  1.0  2.0
```



