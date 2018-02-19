---
title: LINQ
date: 2016-04-25 14:47:35
categories: "c#"
tags: [c#]
---

### 什么是LINQ
在数据库系统中，数据可以放在规划很好的表中，用SQL查询。但是在程序中，保存在类对象或结构中的数据差异很大。这时，使用LINQ可以轻松的查询对象集合。

* LINQ（发音为link），语言集成查询（Language Interated Query)
* 它是.NET框架的扩展，允许我们用SQL语句来查询
* 可以从数据库，程序对象的集合以及XML文档中查询数据
  <!-- more -->

### 匿名类型
在介绍LINQ的细节之前，我们先学习一个允许我们创建无名类类型的特性-匿名类型，它常用于LINQ查询的结果之中。
创建匿名类型的变量使用使用初始化类示例相同的形式，但是没有类名和构造函数，

    new {初始化语句}

下面实例：

    static void Main(){
        var student = new {Name="Mary",Age=19,Major="History"};  //必须使用var
        Console.WriteLine("{0},Age{1},Major{2}",student.Name,student.Age,student.Major);
        }  //在输出语句中，可以像访问具名类类型的成员那样访问实例成员

* 匿名类型只能和局部变量配合使用，不能用于类成员
* 必须使用var作为变量类型
* 不能设置匿名类型对象的属性。编辑器为其创建的属性是只读的
### 方法语法和查询语法
* 方法语法：使用标准的方法调用
* 查询语法：看上去和SQL语句很相似，使用查询表达式形式书写。
* 微软推荐查询语法，它更易读，更清晰的表达意图，但是有些运算符必须使用方法语法。

        static void Main(){
           int[] numbers = {2,5,28,31};
           var numsQuery = from in numbers           //查询语法
                           where n<20
                           select n;
                           
           var numsMethod = numbers.where(x => x < 20); //方法语法，这里使用了lambda表达式
           
           int numCount = (from n in numbers          //两种形式的组合
                           where n<20
                           select n).Count();
        }

LINQ查询可以返回两种类型的结果，枚举，或者一个单一值

       int[] numbers = {2,5,28,31};

       IEnumerable<int> lowNums = from n in numbers  //返回枚举数
                                  where n < 20 
                                  select n;
                             
       int numsCount            = (from n in numbers //返回一个数
                                  where n < 20
                                  select n).Count(); 

 由上，尽管显式定义了查询变量的类型IEnumerabel<T>和int，我们还是可以用var来让编译器自行推断

###查询表达式的结构
*   from子句  
        ` form Type Item in Ttems `
    * 它指定了要作为数据源使用的数据集合，还引入了迭代变量。
    * type是集合中元素的类型，这是可选的，编译器可以推断
    * Item是迭代变量的名字
    * Items是要查询的集合的名字，集合必须是可枚举的。 
*   join子句



