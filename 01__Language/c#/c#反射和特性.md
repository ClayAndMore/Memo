---
title: "c#反射和特性.md"
date:  2016-05-02 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: [""]
categories: ["c#"]
author: "Claymore"

---


## 先看概念：

* 元数据：有关程序和程序类型的数据，它们保存在程序的程序 集中。不是数字，文本，图形。
* 反射：查看本身或其他程序的元数据这样的行为称为反射。要用反射，必须使用System.Reflection命名空间。


## Type类
BCL声明了一个叫做Type的抽象类，包含了类型信息。

* 对于程序中的用到的每一个类型，CLR都会创建这个类型信息的Type类型对象。
* 不管创建的类型有多少个实例，只有一个Type类型会关联到所有这些实例。



| 成员            | 成员类型 | 描述            |
| ------------- | ---- | ------------- |
| Name          | 属性   | 返回类型的名字       |
| Namespace     | 属性   | 返回包含类型声明的命名空间 |
| Assembly      | 属性   | 返回类型的程序集      |
| GetFields     | 方法   | 返回类型的字段列表     |
| GetProperties | 方法   | 返回类型的属性列表     |
| GetMethods    | 方法   | 返回类型的方法列表     |




## 获取Type类型对象
* Type t= myInstance.GetType();
* Type t= typeof(DerivedClass);

        using Systerm;
        using Systerm.Reflection;
        
        namespace SimpleReflection
        {
            class BaseClass{
                public int MyFieldBase;
            }
            
            class DerivedClass : BaseClass {
                public int MyFieldBase;
            }
        }
        class Program{
            static void Main(){
                Type tbc = typeof(DerivedClass);        //获取类型
                Console.WriteLine("Result is {0}",tbc.Name);
                
                Console.WriteLine("It has the following fields:");
                FieldInfo[] fi = tbc.GetFields();
                foreach (var f in fi)
                {
                    Console.WriteLine("{0}",f.Mame);
                } 
            }
        }
        
        //输出：Result is DerivedClass，
           //  It has the follwing fields:
           // MyFieldDerived
           // MyFieldBase

## 特性
特性 ： 一种允许我们向程序的程序集添加元数据的语言结构。它是用于保存程序结构信息特殊类型的类。 就是为一个类贴上标签。
使用方法：

* 在结构前放置特性片段你来应用特性
  ` [Serializable] `
* 特性片段被方括号包围，其中特性名和特性的参数列表。
  ` [MyAttribute("Simple class","Version 3.57")] `

先看一个栗子：

    namespace test
    {
        class Mytest
        {
            [Obsolete("这个函数已经过时，推荐使用sayHi")]
         public   void say()
            {
                Console.WriteLine("this is say");
            }
         public  void sayHi()
            {
                Console.WriteLine("this is sayHi");
            }
        }
        class Program
        { 
            static void Main(string[] args)
            {
                Mytest t = new Mytest();
                t.say();
            }
        }
    }
此时，在vs编译器里，t.say()出会标记绿线，提示 say()已过时，这个函数已经过时，推荐使用sayHi。
这个Obsolete特性是微软给我自带的，标记过时的函数，但是还可以使用。
为了更好理解，我们看一下官方说法：
它是公共语言运行时允许添加类似关键字的描述声明，叫做**Attributes**,它对程序中的元素进行标注，如类型、字段、方法和属性等。
这时，我们简单的总结为： Attribute，本质上市一个类，为目标元素提供关联的附加信息，并在运行期以反射的方式来获取附加信息。

### 自定义特性 Attribute
Attibute就是类，我们可以自己定义自己需要的特性，类名一般以Attribute结尾。注意继承Attribute

      //自定义特性
        public class FlyAttribute: Attribute
        {
    
        }
        [Fly] //或者[FlyAttribute]
        class Mytest
        {

带参数的自定义特性，参数是特性类构造函数的参数。

     public class FlyAttribute: Attribute
        {
            public string Name { get; set; }
            public FlyAttribute(string name)
            {
               this.Name = name;
            }
        }
        [Fly("heihei")] 
        class Mytest
        {

**由上[Fly("heihei")]时，new了一个FlyAttribute对象，并把这个对象给Mytest**












