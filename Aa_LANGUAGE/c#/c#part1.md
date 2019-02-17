
tags: [c#] date: 2016-04-08


## 写在前面

### c#可以做什么

* windows桌面应用程序 （.NET3.0后的WPF(Windows Presentation Foundation)）
* web应用程序(ASP.NET)
* web服务（WCF(Windows Communicatino Foundation)).

<!-- more -->

### .NET Framework
是c#的运行环境

###  面向对象的基本特征
继承，封装，多态

## 进入基础

注：参考教程：Cshap图解教程（第4版）

### 一..net框架
![](http://7xs1eq.com1.z0.glb.clouddn.com/netFrame1.jpg)
![](http://7xs1eq.com1.z0.glb.clouddn.com/netFrame2.jpg)
---


### 二.基础概述
```cs
 using System;  --命名空间
 
 namespace simple --声明一个命名空间
 {
  class program  --一个类program类中包含Main方法，系统自动生成，
  {
  static void main(){
    Console.WriteLine("hello"); --和Console.Write()方法一样，writeline()多\n
    }
  }
 }
```
* **代替标记 格式字符串**

  ```c#
  Console.WriteLine("Two simple integers are {0} and {1}",3,6);  
  --Two simple integers are 3 and 6;

  Console.WriteLine("Three simple integers are {1} {0} and {1}",3,6);  
  --Three simple integers are 6,3and6;
   
  ```

 {index，alignment：format}
 index:指定某一项
 alignment:指定字段宽度，正直右对齐，负值左对齐。
 format:货币C，c，定点F，f等

 `eg:Console.WriteLine({0,-10:F4},12.345678);--12.3456`

* **C#就是一组类型声明**
  这里说明下，在cshap中，万物皆对象，就连int，他也是个对象 对应 微软库中的Int32,bool 对应 boolean ,只是我们在编程中简略的书写罢了。

* **值类型和引用类型**
   1，值类型 

  数值类型直接将数据存储在栈里变量的空间
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/cshapType.png)
   2，数据放在堆里，引用放在栈里 
   ![](http://7xs1eq.com1.z0.glb.clouddn.com/yinyong.jpg)
   另：总结起来，每种类型的默认值都是0，bool型是false，引用类型为null;


  3.装箱和拆箱

  将数值类型的变量变成引用类型的过程叫做装箱，将引用类型的数据变成数值类型的过程叫做拆箱。
  装箱和拆箱都需要复制数据，会浪费性能，最好要避免装箱和拆箱的操作

* **类型转换**
    满足两个条件可以类型转换：

* 数据类型要兼容 比如你double的肯定能转成 int 的啦，都是数，还有 string类型的"123"，也能转成数，它里面也是数啊
    ` int i = int.Parse(str);`
    或：
    ` int i = Convert.ToIn32(str);`
    这时，就要多说一句了，一道面试题，string str = '123' 转成int类型，用上面两种方法有什么区别？
    可以查库的api，convert就是调用的parse方法，不过在前判断了str=null的情况，如果为空，那么convert返回零，而parse会抛出异常。
* 还有一点就是 目标类型要大于源类型 比如 int 转成 byte 是不行的，但是可以强制转换，`byte a = (byte) by;`

- string 
  string是Systerm.String类型的别名，表示由零个或多个unicode字符组成的不可变序列，可用“[]”运算符访问string中的每个字符。
  `string a = "hello"`
  a存放在栈里，而“hello”存放在堆里，a中存的是地址。
- 枚举类型
  枚举属于值类型，默认每个枚举中是int类型，可以使用冒号制定类型：

```
enum Gender:byte
{
    Female,
    Male
}
```

默认为第一个元素设置为0,其他递增，如Gender.Female=0,Gender.Male=1.

- 数组类型
  数组类型是一种引用类型，语法：`type[] array=new type[index]`
  type可以是任意类型。

###三.**类**

- 和c++不同，c#在类型的外部不能声明全局变量，所有的字段都属于类型，而且必须在类型声明内部。不能声明同名的变量，不管嵌套级别如何；
- 可在内部直接初始化字段。

        class MyClass{
          int f1;
          string f2="abc";
            }

**声明类类型的变量所分配的内存是用来保存引用的，不是保存对象实例实际数据的，为实际数据分配内存，需要用new运算符。**
使用对象创建表达式初始化变量：
`Dealer theDealer=new Dealer();`

* **var关键字**

        int total =15;
        var total=15;
        MyClass mec=new MyClass();
        var mec=new MyClass();
    编译器可通过右边的类型推断左端的显示声明，避免冗余，可以用var关键字，它不是特定的类型符号，只是语法上的速记，表示任何可以初始化语句右边推断出的类型；
    但只能用于**本地变量**，只能在声明变量初期包含初始化使用；
* **本地常量**
  在类型前加关键字**const**,声明后**不能改变**(不能赋值)，在方法体或者代码块里，随着块结束地方结束生命，编译期决定。**在方法或者类里声明**
* **静态成员**
   静态成员是类内被**static**修饰的成员，它是属于类的，只能通过类名来访问，类名.成员。
   没有被static修饰的是实例成员，它是属于对象的，同过类的实例来访问。

        class Common{
            public static int num = 0;
            public int num1 = 1;
        }
        
        Common c = new Common();
        int numc = Common.num;
        int num1c = c.num1;
   ![](http://ojynuthay.bkt.clouddn.com/cshap%E9%9D%99%E6%80%81%E5%8C%BA.png)
   **看图说话，静态成员不是在堆里已不是在栈里，它是在专门的静态存储区里，在类第一次声明时创建，并只创建一次，程序结束才会垃圾回收，而类是用完就回收。**

另外，静态成员的意义是被共享，或多次利用。
还有，在静态方法中不能调用实例成员，this和base(父类)也不能在静态方法中使用，不确定实例是否存在，看图会懂的。
在实例方法中可以调用静态成员，因为此时静态成员肯定存在。

*   **静态字段** 和静态成员一样
    * 能被类的所有实例**共享**。所有实例都访问同一内存位置`static int menu2;`
    * 类没有实例，也存在静态成员，并且可以访问。、
    * 它是可以赋值的，作用范围是整个类，相当于全局变量。
* **静态类**    
    * 被static修饰的类是静态类
    * 静态类中只能有静态成员
    * 静态类中不能有实例构造函数
    * 静态类不能被初始化，不能被继承。
    * 本质就是一个抽象类的密封类，所以不能被继承也不能被实例化
    * 如果一个类的下面所有成员被共享，那么可以把这个类定义为静态类。
      这些有过之前的静态成员都好理解
* **静态构造函数**
    * 非静态类也可以有静态构造函数
    * 第一次访问类的成员 **之前**就会调用静态构造函数，记住普通构造函数也是类的成员
      ` common c = new common();` 这就是访问普通构造函数。
    * 静态构造函数只执行一次。
* **属性**
     ​    特征与字段相似，但是不为数据储存分配内存，重点是属性可以保护字段，防止外部瞎赋值：

               class Program{
                   class people{
                       private int age = 18;
                   
                       public int Age{  
                           get { return age;}
                    }  
                   }
                   
                 static void Main(){
                     people p1 = new people();
                     int age = p1.Age;
                 }
               }
         这样就能保护类内部的数据了，还能让外界访问，但是修改不了，nice。
         这里注意，属性和方法的语法很像，但是**属性没有括号**哦。
         再看一个：
         
               private string gender;
               private bool isMan;
               
               public int Gender{  
                   get{
                       string strGender =  isMan == true ? "man":"woman";
                       return strGender; 
                      }
                   set { return value == "man"?false}
            }  

set访问器为属性赋值，get访问器从属性获值。
eg:声明一个int型的属性语法。

        int MyValue{
        set{a=value;}  //拥有一个单独的，隐式的值参，value，与属性的类型相同，返回类型void
        get{return a;}  //没有参数，拥有与属性类型相同的返回类型。
        }
        MyValue=5; //赋值：隐式调用set方法
        z=Myvalue; //表达式：隐式调用get方法 
    注：两个访问器不能显式调用，只能隐式调用；
    只声明set访问器为只写属性，只声明get访问器的称为只读属性；
    不成文约定：属性用Pascal命名法，字段用Camel命名法；

*   **构造函数**
     可以带参数，可以被重载，没有返回值
     静态构造函数，使用static修饰，只有一个，不能有访问修饰符。
* **readonly修饰符**
     ​    作用类似于const，而readonly字段的值可以在运行时决定，只可以在构造函数中初始化。这种自有性允许在不同的环境不同的构造函数中设置不同的值。可以是实例字段，可以是静态字段，在内存中有储存位置。
* **this关键字**
     ​    是对当前实例的引用。
* **is关键字**
     ​    判断变量是否是指定的类型

              Person p = new Person();
              bool b = p is Person();  // b 为 true

* **as关键字**
     ​    类型转寒关键字 如果转换失败不报异常,返回null

             student s2 = (student) p; //可能会报异常
             student s3 = p as Student;

* **虚拟成员**
     ​    被关键字“virtual”修饰的成员，其实虚拟成员并不虚拟，它可以包含实质性的代码，完成一定的功能，只是虚拟成员可以方便的被重载而已，继承者可以根据需要不重载这些虚拟方法。

               public class MyClass{
                   public virtual int Sum(int a,int b){
                       return a+b;
                   }
               }
* **抽象成员**
     ​    被关键字“abstract”修饰的类型成员，抽象成员只能是属性，方法和索引器。
     ​    `public abstract int Sum(int a, int b);`
     ​    抽象成员必须出项在抽象类中，而且在从抽象类派生新类型时，所有的抽象方法必须重写以填充方法体。
     ​    **注：** 抽象成员和虚拟成员是有区别的：
* **抽象成员成员不能定义任何实质的功能，必须被重载。**

    * 虚拟成员必须包含完整的代码结构，可以包含实际功能，可以不被重载。
* **索引器**
     ​    索引器允许类或结构的实例像数组一样进行索引，类似一个带有参数的属性。
     ​    索引器，是一组get和set访问器 ，总是实例成员，不能声明为static。
     ​    
                //声明格式
                return this [type param1]{
                get{}
                set{}
               }
               emp[0]="Doe"; //自动调用set访问器
               string NewName=enp[0];//自动调用get访问器
               eg:
               class Employee{
               public string LastName;
               public string FirstName;
               public string CityBorth;
               
               public string this[int index]{
                set{swith (index){
                 case 0:LastName=value;  break;
                 case 1:FirstName=value; break;
                 case 2:CityBorth=value;  break;
                 default:
                throw new ArgumentOutOfRangeException("index");}}//抛出异常
                
                get{
                 switch(index){
                  case 0:return LastName;
                  case 1:return FirstName;
                  case 2:return CityBorth;
                  default:
                throw new ArgumentOutOfRangeException("index");}}//抛出异常
                }
                
                static void main(){
                Employee emp1= new Employee();
                emp1[0]="Doe";
                emp1[1]="Jane";
                emp1[2]="Dallas";
                Console.WriteLine("{0}",emp1[0]);
                Console.WriteLine("{0}",emp1[1]);
                Console.WriteLine("{0}",emp1[2]);}
* **部分类**
     ​    类的声明可以分割成几个分部类的声明。可以在同一文件，也可以在不同文件。
     ​    每个局部声明必须被标为**partial class**，
     ​    
               partial class MyClass{           
                partial void PrintSum(int x,int y);  //定义部分方法，返回类型必须为void，要有上下文关键字partial，不能包含访问修饰符，这使部分方法是隐式私有的。
                public void Add(int x,int y)
                {
                 PrintSum(x,y);}
                 }
                 
                 partial class MyClass{             
                  partial void PrintSum(int x,int y){         //实现部分方法
                   Console.WriteLine("Sum is {0}",x+y); }
               }
               
               class program{
                static void main(){
                 var mc=new MyClass();
                 mc.Add(5,6);    //分部方法是隐式私有的，PrintSum不能从类的外部调用，方法Add是调用printSum的共有方法。
                 }
                }



* **类和结构体的区别**
  关键字不同，结构体的为struct。
  结构体中不能对声明字段进行初始化，但是类可以。
  类是引用类型，结构体是值类型。

###四.方法
**只有 void 类型的方法，可以用return中断；**
1，**值参数**
2，**引用参数**
- 使用引用参数前，必须在方法的**声明**和**调用**中都使用**ref**修饰符
- 实参必须是**变量**，在做实参前必须被赋值，如果是引用变量，可以赋值为一个引用或null;
    eg: 
```
void MyMethod(ref int val){...}
int y=1;
Mymethod(ref y);  //正确
MyMethod(ref 3+5); //错误，必须使用变量
```
就是用ref 修饰的参数 必须传递变量，不能是常量。**也就是说传递了变量的地址**，请看：

    int i = 12;
    Test(ref i);
    Console.WriteLine(i);
    
    static void Test(ref int i){
        i++;
    }
    
    //输出 i = 13
    //就是说外部i的地址进入方法

3，**输出参数**
- 在**声明**和**调用**中都使用 **out** 修饰符。
- 和引用参数相似，实参必须是**变量**。
- 在方法内部，输出参数必须在被读取之前被赋值。
- 如果方法中有任何执行路径试图在输出参数被方法赋值之前读取她，编译器就会产生错误
  eg:

    public void add(out int outVaulue){
    int var1=outVaulue+2; //错误，在方法赋值之前使用参数。 
    }
  也就是说 在方法内，必须为它赋值，**也是传递了变量的地址**，它侧重于输出，而ref侧重于修改。    

4，**参数数组**
- 一个参数列表只能有一个参数数组，切它必须是列表中最后一个，就是放在参数的最后面啦。
- 数组里必须居然有相同的类型。
- 在数据类型前必须使用**params**修饰符。
- 在数据类型后放置一组空的**方括号**。
- 数组为一个引用类型，所有数据项都保存在堆中。
- **在声明中需要修饰符，在调用中不允许有修饰符**。
  eg:

    void ListInst(params int[] inVals){...}//声明
    //调用
    ListInst(10,20,30);  //第一种方法
    int[] intArray={1,2,3};//第二种方法
    ListInst(intArray);
  也就是说被Params修饰的数组参数，调用方法时候可以直接传数字，它会自动生成一维数组。
  5.**命名参数**
- 显式指定参数的名字，就可以任意顺序调出实参。
  `c.Calc(c:2,a:4,b:3);`
  6,**可选参数**
- 为了表明某个参数是可选的，需要在方法声明的时候为参数提供默认值。
  `public in Calc(int a,int b=3);//b为可选参数`

###五.类和继承
*   类OtherClass继承Someclass的类：
     `class OtherClass：SomeClass{};`
* 除了特殊的类object,所有的类都是派生类，么有基类规格说的类隐式的直接派生自object。
* 可以用与基类成员相同的名称来屏蔽基类成员，要用new修饰符，告诉编译器故意屏蔽成员.

         class SomeClass{
          public stirng Field1;
          public void Method(string value){};
          }
          class OtherClass:SomeClass{
          new public string Field1;
          new public void Method(string value){};
          }
     如果想访问隐藏的基类成员：
     `Console.WriteLine("{0}",base.Field);`
* **里氏替换原则LSP**
     ​    子类可以替换父类的位置，并且程序不受影响，就是子类有的功能，父类肯定有的，继承肯定没问题的
* **运行时绑定**
     ​    student继承person
     ​    ![](leanote://file/getImage?fileId=5744433cab64413fd701bedf)

* **类型转换**
     ​    `Person p1 = new Student();`
     ​    `Student s1 = (Student)p1`
     ​    必须有继承关系才可以使用强制转换

* **使用基类的引用**：派生类的实例由基类的实例和派生类新增的成员组成，派生类的引用指向整个类，包括基类，基类的引用只对自己可以见。

         class BaseClass{
          public void print(){ Console.WriteLine("base");}
          
         class MyDerivedClass:BaseClass{
          new public void print(){Consle.WriteLine("Drive");}
          
         class Program{
          static void Main(){
          MyDerivedClass derived=new MyDerivedClass();
          BaseClass mb=(BaseClass)derived; //转换成基类 （）转换运算符

* **虚方法和覆写方法**
     ​    虚方法可使基类的引用调用派生类的方法。要求：
* 基类和派生类的方法有相同的签名和返回类型。
    * 基类的方法用virtual标注。派生类的方法用override标注。
    * 覆写和被覆写必须有相同的访问性。

            class BaseClass{
            virtual public void Print(){...}
            }
            class DerivedClass:BaseClass{
            override public void Print(){...}
            }

    * 覆写可以在继承的任何层次出现，当使用对象的基类引用调用一个覆写方法时，在**最高**派生类里执行(情况一)
    * 如果在派生类里有该方法的其他声明，但没有标记为override，那么他们不会被调用。（情况二）
    * 不只是方法，在属性和所引器上也是一样的。

            class BaseClass{
            virtual public void Print(){Console.WriteLine("baseclass");}
            }
            class DerivedClass:BaseClass{
            override public void Print(){Console.WriteLine("derivedclass");}
            }
            //下面有两种情况，一种是用override标记，一种是用new标记
            class SecondDerived:DerivedClass{
            override public void Print(){Console.WriteLine("SecondDerived");}
            }
            class Program{
             static void main(){
              SencondDerived derived=new SencondDerived();
              BaseClass mybc=(BaseClass)derived;
               derived.Print();             //输出SencondDeriver
               mybc.Print(); }}             //输出SencondDeriver
              
            //第二种情况
            class SecondDerived:DerivedClass{
            new public void Print(){Console.WriteLine("SecondDerived");}
            }
            class Program{
             static void main(){
              SencondDerived derived=new SencondDerived();
              BaseClass mybc=(BaseClass)derived;
               derived.Print();              //输出SencondDeriver
               mybc.Print(); }}               //输出derivedclass

* 继承层次链中的每个类在执行他自己的构造函数体之前，先执行他的**基类构造函数**。
     ​    默认隐式调用基类的无参构造函数，但构造函数可以重载，基类可以有一个以上的构造函数，如果想调用一个**指定**的基类构造函数，必须在派生类的构造函数初始化语句中指定它。
     ​    两种方式构造函数初始化：
     ​    **1.**关键字base指定具体的基类构造函数
     ​    `public DerivedClass(int x,string s):base(s,x){...}`//base中两个参数要和基类构造函数的参数列表匹配。//这里没有定义基类，强调顺序。
     ​    **2.**关键字this并指明应该使用**当前类**的哪一个构造函数。
     ​    `public MyClass(int x):this(x,"Using Default String"){...}`
     ​    这种方法很好，一个类有好几个构造函数，并且他们都需要，在对象构造的时候执行一些公共代码，可以把公共代码提取出来做为一个构造函数，可以完全把它设置为public的构造函数。但如果不能完全初始化一个对象，此时，必须禁止从类的外部调用构造函数，那样的话只会初始化一部分，可以把构造函数声明为private，只让其他构造函数使用它：
     ​    
                class MyClass{
                 readonly int firstVar;
                 readonly double secondVar;
             
                 public string UserName;
                 public int UserIdNumer;
             
                 private MyClass(){          //私有构造函数执行其他构造
                  firstVar=10;                //函数公用的初始化
                  secondVar=0.1;
                 }
             
                 public MyClass(string firstName):this(){   //使用构造函数初始化语句
                  UserName=firstName;
                  UserIdNumer=1;
                }
             
                 public MyClass(int idNumer):this(){    //使用构造函数初始化语句
                  UserName="Alay";
                  UserIdNumer=idNumer;
                 }
               }
* 类的访问修饰符
     ​    public：被系统内的任何程序集访问到。using namespace；
     ​    internal：只能被自己的程序集内的类看到，默认的访问级别。即使成员访问级别为public，外界也不可见。
* 成员访问修饰符：
     ​    private：只在类的内部可见。
     ​    internal：对该程序集内所有的类可以访问。
     ​    protected：所有继承该类的类可以访问。
     ​    internal:所有继承该类或在该程序集内部声明的类可以访问。
     ​    public：对任何类可见。
* **抽象成员**：被覆写的函数成员，必为**函数**成员，用abstract修饰符。
     ​    **抽象类**：被继承的类。只能用作其他类的基类。不能创建实例。用abstract修饰符。
     ​    可包含普通函数和抽象成员，也可派生抽象类。派生自派生类的类，用override实现该类的抽象成员。
     ​    
                abstract class AbClass{                          //抽象类
                 public void IDBase(){ Console.WriteLine("AbClass")}   //普通方法
                 abstract public void IDDerived(){};               //抽象方法
                }
             
                class DerivedClass:AbClass{                     //派生类
                 override public void IDDerived(){
                 Console.WriteLine("DerivedClass");
                 };
                 }
             
                class Program{
                 static void Main(){
                   //AbClass a=new AbClass();    //错误，抽象类不能创建实例。
                   //a.IDDerived();
             
                    DerivedClass b=new DerivedClass();
                    b.IDBase();
                    b.IDDerived();
                    }
                     } 

* **虚方法和抽象方法的区别**
     ​    简单点说,抽象方法是需要子类去实现的.虚方法,是已经实现了,子类可以去覆盖,也可以不覆盖取决于需求. 

虚方法和抽象方法都可以供派生类重写，它们之间有什么区别呢？
1. 虚方法必须有实现部分，抽象方法没有提供实现部分，抽象方法是一种强制派生类覆盖的方法，否则派生类将不能被实例化。
2. 抽象方法只能在抽象类中声明，虚方法不是。其实如果类包含抽象方法，那么该类也是抽象的，也必须声明为抽象的。
3. 抽象方法必须在派生类中重写，这一点跟接口类似，虚方法不必。


* **密封类**：和抽象类相反，它不能被用来做基类，是独立的类。用sealed修饰符。
  `sealed class MyClass{}`
  有些时候，并不希望所编写的类被继承，如果所有的类都可以被继承，则类的层次结构将会变得十分复杂，从而加重理解类的困难。此时，可以用“sealed”来定义密封类。这样的话，可以防止被其他类继承。
* **密封方法** 
  密封方法：是为了防止方法在类的派生类中对该方法进行重载。不是类的每个成员都可以作为密封方法，密封方法必须对基类的虚方法进行重载。所以，sealed总是与override修饰符同时使用。
  当应用于方法或属性时，sealed 修饰符必须始终与override 一起使用。

        using System;
        class A
        {
            public virtual void F()
            {
                Console.WriteLine("A.F");
            }
            public virtual void G()
            {
                Console.WriteLine("A.G");
            }
        }
        class B:A
        {
            public sealed override void F()
            {
                Console.WriteLine("B.F");
            }
            public override void G()
            {
                Console.WriteLine("B.G");
            }
        }
        class C:B
        {
            public override void G()
            {
                Console.WriteLine("C.G");
            }
        }
        class Test
        {
            static void Main()
            {
            }
        }
  在类C中，不能再对B中的void F()进行重写了。

* **静态类**：用于存放不受实例数据影响的数据和函数。常见用途可能就是一个包含一组数学方法的数学库。
  1.本身必须标记为**static**。该类所有成员都是静态的。
  2.可以有一个静态函数，不能有实例构造函数，不能创建该类的实例。
  3.静态类是隐式封闭的，不能继承静态类。
```c#
static public class MyMath{
    public static float PI=3.14f;           //所有成员必须是静态的
    public static bool IsOdd(int x){
        return x%2 ==1;
    }
    public static int Times2(int x){
        return 2*x;
    }
}

class Program{
    static void Main(){
        int val=3;
        Console.WriteLine("{0} is odd {1}",MyMath.IsOdd(val));  //像正常类那样使用
        Console.WriteLine("{0} *2= {1}",MyMath.Times2(val));
    }
}
```
* **扩展方法**
  已有一个不能访问其代码的类，或者密封类，若要更改其中的方法，需要写一个类来实现。如现在有这样一个求三个数的和的类：
```
sealed class MyData{
    private double D1,D2,D3;
    public MyData(double d1,double d2,double d3){
        D1=d1;D2=d2;D3=d3;
    }
    public double Sum(){return D1+D2+D3;}
}
```

我们要写一个类来求三个数的平均值：

      static class ExtendMyData{
        public static double Average(MyData md){
        return md.Sum()/3;
       }
     }
    
      class Program{
        static void Main(){
        MyData md=new MyData(3,4,5);
        Console.WriteLine("Average:{0}",ExtendMyData(md));  
     }
    }

这是一个好的解决方案，但是我们想从MyData自身的实例来求平均值，而不是创建另外一个类的实例，可以md.Average();那么就用到了扩展方法。
这时，需要在方法Average上做改动，

      static class ExtendMyData{          //必须是一个静态类
        public static double Average(this MyData md){    //必须是共有的和静态的，和this关键字
        return md.Sum()/3;
       }
     }
    
      class Program{
        static void Main(){
        MyData md=new MyData(3,4,5);
        Console.WriteLine("Sum:{0}",md.Sum()};       //调用自身的方法
        Console.WriteLine("Average:{0}",md.Average());   //调用类ExtendMyData的方法
     }
    }
这样看来就为密封类加了一个方法。

###六.表达式
* **字面量**：代码中键入的数字或者字符串，如下中的整形字面量2014    
  `Console.WriteLile("{0}",2014);`
  令：注意浮点和双精度字面量的区别。
  `Console.WriteLile("{0}",3.1415);` //双精度字面量
  `Console.WriteLile("{0}",3.1415f);` //浮点字面量
* 字符串字面量
  分为两种：
  常规字面量：`string rst="Value 1\t5,Val2\t10";`  输出：Value 1   5,Val2    10           
  逐字字面量：`@string vst="Value 1\t5,Val2\t10";` 输出Value 1\t5,Val2\t10
  逐字字面量中转义字符串**不会被求值**，但相邻的双引号被解释为单个双引号：
  `string str="It started,\"Four score and seven...\"";`
  `string vtr=@"It started,""Four score and seven...""";`
  都输出为：It started,"Four score and seven..."
* 在C#中不像C和C++，数字不具有布尔意义，

        int x=5;
         if(x){}// 错误，x不是布尔类型
         if(x==5){}//正确

* 一元运算符：设置数字值的符号，当+，-做加减运算时它是二元运算符。
  其他的一元运算符：！，~，++，--，true，false,typeof
  `int x=+10;  int y=-x;  int z=-y;` x=10,y=10,z=10.
* 条件运算符（三元运算符）
  Condition？Expression1：Expression2
  eg:
  `if(x<y) x=5; else =10;`  => `x<y?5:10;`
* **用户自定义的类型转换**
  可为自己的类或者结构定义隐式转化和显式转换。
  定义语法：

        public static(必须) implicit(隐式)/explicit(显式) operator TargeType/目标类型 (Source Identifier/源数据)
        {
         return ObjectOfTargetType;
        }
  eg:

        class LimitedInt{
        const int MaxValue=100;
        const int MinValue=0;
      
         public static implicit operator int(LimitedInt li)  //显式将implicit换成explicit
         {
            return li.TheValue;
         }        
         public static implicit operator LimitedInt(int x) //显式将implicit换成explicit
         {
            LimitedInt li=new LimitedInt();
            li.TheValue=x;
            return li;
         }
         private int _theValue=0;
         public int TheValue{
            get{return _theValue;}
            set{
                if(value<MinValue) _theValue=0;
                else _theValue = value>MaxValue?MaxValue:value;
            }
         }
        }
        class Program{
            static void Main(){
                LimitedInt li=500;  //显式 LimitedInt li=(LimitedInt)500;
                int value=li;       //显式 int value=(int) li;
                Console.WriteLine("li:{0},value:{1}",li.TheValue,value);
            }
        }
  输出：li:100,value:100
* **运算符重载**
  运算符重载允许你定义C#运算符应该如何操作自定义类型的操作数。
  1，运算符重载只能用于类和结构。
  2，为类或结构重载一个运算符x，可以声明一个名称为operator x的方法并实现它的行为（eg:operator +)
  3,一元运算符的重载方法带一个单独的class或struct类型的参数。
  4，二元运算符的重载方法带两个参数，至少有一个必须是class或者struct类型.
  5，声明必须同时使用struct和public修饰符。
  6，运算符必须是要操作的类或结构的成员。
  7，说明：重载运算符应该符合运算符的直观意义。

        class LimitedInt{
            const int MaxValue=100；
            const int MinValue=0;
            public static LimitedInt operator -(LimitedInt x)
            {
                //在这个奇怪的类中，取一个值的负数等于0
                LimitedInt li=new LimitedInt();
                li.TheValue=0;
                return li;
            }
            public static LimitedInt operator -(LimitedInt x,LimitedInt y){
                LimitedInt li=new LimitedInt();
                li.TheValue=x.TheValue-y.TheValue;
                return li;
            }
            public static LimitedInt operator +(LimitedInt x,double y ){
                LimitedInt li=new  LimitedInt();
                li.TheValue=x.TheValue+(int)y;
                return li;
            }
        
            private int _theValue=0;
            public int TheValue;
            {
                get{return _theValue;}
            set{
                if(value<MinValue) _theValue=0;
                else _theValue = value>MaxValue?MaxValue:value;
            }
        }
        }
        class Program{
            static void Main(){
                LimitedInt li1=new LimitedInt();
                LimitedInt li2=new LimitedInt();
                LimitedInt li3=new LimitedInt();
        
                li1.TheValue=10; li2.TheValue=26;
                Console.WriteLine("li1:{0},li2:{1}",li1.TheValue,li2.TheValue);//输出:li1:10,li2:26
        
                li3=-li1;
                Console.WriteLine("-{0}={1}",li1.TheValue,li3.TheValue);//输出：-10=0
        
                li3=li2-li1;
                Console.WriteLine("{0}-{1}={2}",li1.TheValue,li2.TheValue,li3.TheValue);//输出：26-10=16
        
                li3=li1-li2;
                Console.WriteLine("{0}-{1}={2}",li1.TheValue,li2.TheValue,li3.TheValue);//输出：10-26=0
        
            }
        }

* **运算符typeof**
  typeof是一元运算符，返回已知类型的Systerm.Type对象（对任何已知类型，只有一个Systerm.Type对象。Type是System中的一个类。语法示例；
  Tpye t=typeof(SomeClass)
  下面代码使用typeof运算符获取SomeClass类的信息，并打印公有字段和方法的名称：

        using Systerm.Reflection;//使用反射命名空间来全面利用检测类型信息的功能
        class SomeClass{
            public int Field1;
            public int Field2;
            public void Method1(){}
            public int Method2(){return 1;}
        }
        class Program{
            static void Main(){
                type t=typeof(SomeClass);
                FieldInfo[] fi=t.GetFields();
                FieldInfo[] mi=t.GetMethods();
        
                foreach (FieldInfo f in fi)  Console.WriteLine("Field:{0}",f.Name);
                foreach (FieldInfo m in mi)  Console.WriteLine("Method:{0}",m.Name);
            }
        }

输出：
Field：Field1
Field：Field2
Method：Method1
Method：Method2
Method：ToString
Method：Equals
Method：GetHashCode
Method：GetType


