require 函数:

https://www.cnblogs.com/carterzhang/articles/7680689.html

https://segmentfault.com/q/1010000015690715?sort=created



map 函数：

`map` 用于将一个函数作用于列表的所有元素，然后得到一个作用后的列表结果。

假设我们有一个列表，我们需要对列表中的每一个元素做同样的操作，直观的方法就是遍历列表，然后依次应用这个函数到每个元素上，最后把作用后的结果返回。map 封装了这些步骤，让我们无需显示循环列表。

在这里我们希望将 `this.todos` 这个列表中每一个完成的 todo 标为已完成，因此我们做了：`this.todo.map(func)`，这个 func 就是每一个 todo 的操作，它的操作是这样的：

```js
function (todo) {
    if (!todo.completed) {
        todo.completed = true
    }
}
```

即把所有未完成的 todo 的 `todo.completed` 置为 `true`。

组合起来就完成了我们的需求。

> ES6 还有一种箭头函数写法：
>
> todo => todo.finished = true



filter 函数：

`filter` 和之前讲过的 `map` 函数是类似的，都是函数式编程的思想。`filter` 顾名思义，就是要根据某个检测函数去列表中筛选出符合检测要求的结果。通常这个函数只返回两个值，列表元素符合要求返回真，否则返回假。`filter` 会返回所有检测为真的元素组成的列表。

我们这里的检测函数是：`todo => !todo.completed`，等价于：

```js
function(todo){
    return !todo.completed
}
```

即如果 `todo.completed` 为假，即 todo 未完成，返回真，已完成返回假。所以我们就把未完成的 todo 筛选出来了。

箭头函数： todo => !todo.completed



箭头函数：

```
是相似于 lambda 的函数，这是一种匿名函数，可用于定义函数体非常简单的函数。比如 Python 的 `lambda x: x*x
```

这比写一个函数：

```
python def square(x): return x*x
```

便捷很多。