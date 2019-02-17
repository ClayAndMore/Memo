 tags: [c#] date: 2016-04-23 14:42:23



## 使用foreach语句

这个语句为我们依次取出数组中的每一个元素，例如下面代码声明了一个有四个元素的数组，然后使用foreach来循环打印这些项的值：

        int[] arr1={10.11.12.13};  //定义数组
        foreach ( int item in arr1) //枚举元素
          Console.WriteLine("item value:{0},item);
        //输出： Item value:10 Item value:11 Item value:12 Item value:13
为什么数组可以这么做？原因是数组可以按需提供一个叫做**枚举器**对象，它可以一次返回请求中的数组中的元素，并跟踪它在序列中的位置然后返回当前项。

* foreach结构设计用来和枚举类型一起使用，只要给它的对象是枚举类型，比如数组之类的，就会调用GetEnumerator方法获取对象的枚举器。

        foreach(Type VarName in EnumerableObject/可枚举的类型）{...}

<!-- more -->

## 枚举器和可枚举类型
*   枚举器有个IEnumerator接口，它有三个函数成员：Current.MoveNext以及Reset
    * Current 是返回序列中当前位置项的只读属性。返回object的引用，可以返回任何类型
    * MoveNest 把枚举器位置前进到集合下一项的方法，返回bool值，指示新位置是否到了尾部，新位置有效true，无效false（到达了尾部），如果枚举器的原始位置在序列中的第一项之前，MoveNext必须在第一次调用Current之前调用。
    * Reset是把位置重置为原始状态的方法。

             static void Main(){
                int[] MyArray = {10,11,12,13};
                
                IEnumerator ie= MyArray.GetEnumerator();//获取枚举器
                
                while (ie.MoveNext()){                 //移到下一项
                    int i=(int) ie.Current;            //获取当前项
                    Console.WriteLine("{0}",i); 
                }
                 }
*   **可枚举类是指实现了IEnumerable接口的类**，IEnumerable接口只用一个成员——GetEnumerator方法

                       class MyClass : IEnumerable{      //实现IEnumerable接口
                          public IEnumerator GetEnumerator{...}  //返回IEnumerator的对象
                      }           
            ![](http://7xs1eq.com1.z0.glb.clouddn.com/arrayIEnumerable.png)
*   目前描述的枚举接口都是非泛型的，而大多数用的是泛型的，因为非泛型返回object的引用，而必须转化为实际类型。而**泛型的返回实际类型的引用**。
    ​        ![](http://7xs1eq.com1.z0.glb.clouddn.com/IEnumeratorAndIEnumerable.jpg)

---

## 迭代器
虽然我们已经知道如何创建自己的可枚举类和枚举器，但从C#2.0后提供了更简单创建枚举器和可枚举类型的方式，实际是编译器为我们创建它们，这种结构叫**迭代器**。把手动编码的可枚举类型和枚举器替换为由迭代器生产那个的可枚举类型和枚举器。先来看一个简单的例子：

        public IEnumerator<string> BlackAndWhite(){  //返回泛型枚举器（返回字符串）
            yield return "black";                    //yield return 声明这是枚举中的下一项
            yield return "gray";
            yield return "white";
        }
**迭代器块**是一个或多个yield语句的代码块。其中的代码描述了如何枚举元素，

* yield return 语句指定了序列中返回的下一项
* yield return 语句指定在序列中没有其他项
  编译器在得到有关如何枚举项的描述后，使用它来创建包含所有需要的方法和属性实现的枚举器类。

        public IEnumerator<string> IteratorMethod(){  |  public IEnumerator<string> IteratorMethod(){ 
            yield return ....                         |      yield return .... 
        }                                             |  } 
         产生枚举器的迭代器                                 产生可枚举类型的迭代器     
### 使用迭代器来创建枚举器
    class Myclass{
        public IEnumerator<string> GetEnumerator(){
            return BlackAndWhite();
        }
        
        public IEnumerator<string> BlackAndWhite(){
            yield return "black";
            yield return "gray";
            yield return "white";
        }
    }
    
    class Program{
        static void Main(){
            Myclass mc=new Myclass();
            foreach (string shade in mc)
            {
                Console.WriteLine(shade);
            }
        }
    }
注意Main方法，由于MyClass类实现了GetEnumerator，是可枚举类型，我们在foreach语句中直接使用了类的实例。
###使用迭代器来创建可枚举类型
​    class Myclass{
​        public IEnumerator<string> GetEnumerator(){
​            IEnumerable<string> myEnumerable=BlackAndWhite(); //获取可枚举类型
​            return myEnumerable.GetEnumerator();              //获取枚举器
​        }
​        
​        public IEnumerator<string> BlackAndWhite(){
​            yield return "black";
​            yield return "gray";
​            yield return "white";
​        }
​    }
​    
​    class Program{
​        static void Main(){
​            Myclass mc=new Myclass();
​            
            foreach (string shade in mc)                      //使用类对象
            {
                Console.WriteLine(shade);
            }
            
            foreach (string shade in mc.BlackAndWhite())      //使用类枚举器方法
            {
                Console.WriteLine(shade);
            }
        }
    }
 注意，在main的foreach语句中，我们可以使用类的实例，也可以直接调用BlackAndwhite方法，因为它**返回**的是可枚举类型。        
 上面的两种做法都是让类实现可枚举，如果本身是可枚举类型就不用这么费劲了，比如数组，看下面。

 产生多个可枚举类型：

    using System;
    using System.Collections.Generic;
    
    class Test{
        string[] letter = {"a","b","c"};
        
        public IEnumerable<string> abc(){
            for(int i=0; i<letter.Length; i++)
               yield return colors[i];
        }
        
        public IEnumerable<string> cba(){
            for(int i=colors.Length-1; i>=0; i--)
               yield return colors[i];
        }
    }
    
    class Program{
        static void Main(){
            Test test = new Test();
            
            foreach(string letter in test.abc()) 
               Console.WriteLine("{0}",letter);
        }
            foreach(string letter in test.cba()) 
               Console.WriteLine("{0}",letter);
        }
    }
    //输出：a b c 
           c b a    
 注意，尽管它有两个方法可返回可枚举类型，但**类本身不是可枚举类型**，因为它没有实现GetEnumerator.            
​         
​         
​         