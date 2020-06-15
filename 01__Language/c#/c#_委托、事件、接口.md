
---
title: "c#_委托、事件、接口.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
tags: [c#] date: 2016-04-20


### 委托

![](http://7xs1eq.com1.z0.glb.clouddn.com/%E5%A7%94%E6%89%98.png)

委托可以理解为为当事人辩护的律师。

<!-- more -->

* 委托格式上比方法多了个delegate,但是它可以理解成类，本质就是个类。
* 可以认为委托是持有一个或多个**方法**的对象
* 和类相似，声明委托，和方法声明类似，但是没有实现块。 使用该委托类型声明一个**委托变量**，创建委托类型的对象，把它赋值给委托变量。

* 可以为委托对象添加其他方法，这些方法必须与定义的委托类型有相同的签名和返回类型。
* 像调用方法一样调用委托，其包含的每一个方法都会被执行。
* 关键字delegate看作一个包含有序方法列表的对象
    ``` 
        delegate void MyDel(int x); //声明委托类型

        MyDel delVar; //声明委托变量

        delVar=new MyDel(myInstObj.MyM1);//括号内为实例方法,创建委托并保存引用，这个方法的结构和委托一样
        delVar=new MyDel(SClass.OtherrM2);//括号内为静态方法，创建委托并保存引用，这个方法的结构和委托一样。
        //快捷语法,因为在方法名称和其相应的委托类型之间存在隐式转换。
        delVar=myInstObj.MyM1;
        delVar=SClass.OtherrM2
    ```
      一个实例，更好的帮助理解：
 ```
 class Program{
    //1.使用delegate关键字来定义一个委托类型
    delegate void MyDelegate(int x,int y);
    
    static void Main(string[] args){
        //2.声明一个委托变量
        MyDelegate d ;
        //3.实例化委托变量（可以传静态方法，也可以是实例方法,注意不带括号)
        d=new MyDelegate(new Program().Add);
        //4.将委托作为参数给另一个方法。
        MyMethod(d);
    }
    
    void Add(int a,int b){
        int c = a+b;
        Console.WriteLine("两个数的和为:"+sum);
    }
    
    //方法的参数是委托类型，可以把这个方法理解成法官，法官先调用委托律师，律师陈述了当事人的情况（方法）
    private static void MyMethod(MyDelegate myDelegate){
    //在方法中调用委托。
        myDelegate(1.2);
    }
 }
 ```
* **组合委托** 一个委托由其他委托构成
  ​      
  ​      MyDel delA=myInstobj.MyM1;
  ​      MyDel delB=SClass.Other2;
  ​    

        MyDel delC=delA+delB; 
*   增加方法 ： `delVar+=SCL.m3;`
*   移除方法 ： `delVar-=SCL.m3;`
*   **语法糖**： 像上面这样加减是强大的Cshap编译器为我们做的工作，将原本很复杂的代码编译成简介的代码，我们管这样的结构叫做语法糖
*   **调用委托**
    ​                ![](http://7xs1eq.com1.z0.glb.clouddn.com/delegate.jpg)
    * 调用引用参数的委托

            delegate void MyDel(ref int x);
            
            class MyClass{
            public void add2(ref int x){x+=2;}
            public void add3(ref int x){x+=3;}
            static void Main(){
            MyClass mc=new MyClass();
              
            MyDel mDel=mc.add2;
            mDel+=mc.add3;
            mDel+=mc.add2;
              
            int x=5;
            mDel(ref x);
              
            Console.WriteLine("Value:{0}",x);
            }
            }  //输出  Value：12
*   **匿名方法**
    ​                如果方法只会被使用一次--用来初始化委托，这种情况没有必要创建独立的具名方法，可以用匿名方法

                            class Program                              |  class Program
                            {                                          |{
                                public static int Add20(int x){        | 
                                    return x+20;                       |
                                }                                      |
                            }                                          |}   
                                                                       |
                            delegate int OtherDel(int InParam);        | delegate int OtherDel(int InParam); 
                            static void Main(){                        | static void Main(){            
                                OtherDel del=Add20;                    |  OtherDel del =delegate(int x)  //关键字 （参数列表 ） {语句块}
                                                                       |   {
                                                                       |        return x+20;
                                                                       |   }       
                                Console.WriteLine("{0}",del(5));       |   Console.WriteLine("{0}",del(5)); 
                                Console.WriteLine("{0}",del(6));       |   Console.WriteLine("{0}",del(6));
                            }                                          |  }  
                    可以通过使圆括号为空或省略圆括号来简化匿名方法的参数列表，
    * 委托的参数列表不包含任何out参数；
    * 匿名方法不适用任何参数；

            delegate void SomeDel(int x);
            SomeDel SDel=delegate{
             PrintMessage();   //方法没有使用任何参数
             };
*   如果参数列表包含params参数，匿名方法的参数列表将忽略params关键字。
    ​                ​      
    ​                          delegate void SomeDel(int x,params int[] Y);
    ​                          SomeDel mDel=delegate(int x,int[] y){};  //省略了params关键字

在匿名方法内声明的变量，作用域仅在大括号内。外部变量，可在方法括号内使用（方法捕获）。

*   **Lambda（λ）表达式**
    ​    c#2.0引入的匿名方法，3.0引入的λ表达式，简化了匿名方法的语法
    * 删除了delegate关键字
    * 在参数裂变和主体之间放Lambda运算符=>，读作“goes to"
      `MyDel del=delegate(int x) {returen x+1;};`
      `Mydel del=        (int x)=>{return x+1;};`
      编译器可以从委托的声明中知道参数的类型最后lambda表达式可以简化成：
      `mMyDel del=            x=>         x+1;`
    * lambda表达式中参数列表中的参数必须在**参数数量、类型、和位置**上和委托相匹配。
    * 有ref.out参数必须注名参数列表中的参数类型。
    * **如果只用一个参数，并且是隐式类型的，圆括号可以省略，否则必须有括号**
### 事件
当一个特定的程序事件发生时，程序的其他部分可以得知该事件的发生
**发布者/订阅者模式**  发布者定义事件，其他类可以“注册”，以便事件发生时可以通知它们。

*   声明事件 
    * 声明事件在一个类中，他需要**委托类型的名称**
    * 注册的处理程序必须与委托类型的签名和返回类型匹配
    * 声明public，其他类和结构可以在它上面注册事件处理程序。

            class Incrementer{
             public event/关键字 EventHandler/委托类型 CountedADozen/事件名；
             public event EventHandler MyEvent1,MyEvent2,MyEvent3; //可连续声明多个事件。
             public static event EventHandler CouterADozen;//可以声明为静态
    * BCL声明了一个叫做**EventHandler**的委托，专门用于系统事件。
*   订阅事件(或注册)

                          Incrementer.CoutedADozen+=IncrementDozensCount;//实例方法
                          Incermenter.CouterADozen+=new EventHandler(CC.CounterHandlerC);//委托形式
                          Incermenter.CouterADozen+=()=>DozenCout++;//lambda表达式
                          Incermenter.CouterADozen+= delegate{DozensCount++;}; //匿名方法
*   事件触发
    ​                ` if(CouterAdozen!=null)//确认有方法可以执行 CountedADozen/事件名(source,args)/参数列表;` 
*   **标准的事件用法**，windowsGUI编程广泛的使用了事件，.NET提供了一个标准模式。System命名空间声明的EventHandler委托类型
    ​                ` public delegate void EventHandler(object sender,EventArgs e);`
    * 第一个参数用来保存触发事件的对象的引用，object可以匹配任何类的实例，可以理解成监视的对象。
    * 第二个参数用来保存状态信息，指明什么类型适用于该应用程序。它是EventArgs的对象，但它不用于传递数据，如果希望传递，需要声明一个派生EventArgs的类，可以理解为监视的数据。

            //发布者
            class Incrementer{
            public event EventHandler CAD;    //使用系统定义的委托。
              
            public void DoCount(){
                for(i=1,i<100,i++)
                 if(i%12==0&&CAD!=null)  
                  CAD(this,null);        //触发事件时使用EventHandler的参数
            }
            }
            //订阅者
            class Dozens{
            public int DozensCount{get;private set;}
              
            public Dozens(Incrementer incrementer){
             DozensCount=0;
             incrementer.CAD+=theWay;
            }
              
            void theWay(object source,EventArs e) //事件处理程序的签名必须与委托的签名匹配
             {
                DozensCount++；
            }
            }
              
            class Program{
             static void Main(){
               Incrementer incrementer=new Incrementer();
               Dozens d=new Dozens(incrementer);
               incrementer.DoCount();
               Console.WriteLine("Number of dozen={0}",d.DozensCount);
                }
            }

看一个更通俗的例子，新郎发请帖：
```
namespace eventTest
{
	//新郎官类
	class Bridegroom
	{
		//自定义委托
		public delegate void MarryHandler(string msg);

		//自定义事件,事件名为MarryEvent
		public event MarryHandler MarryEvent;

		//发出事件
		public void OnMarryComing(string msg){
			//判断是否绑定了事件处理方法
			if(MarryEvent != null){
				//触发事件
				MarryEvent(msg);
			}
		}
			
		public static void Main (string[] args)
		{
			Bridegroom birdegroom = new Bridegroom ();
			Friend f1 = new Friend ("张三");
			Friend f2= new Friend ("李四");
			Friend f3 = new Friend ("王五");

			//订阅事件
			birdegroom.MarryEvent+=new MarryHandler(f1.SendMessage);
			birdegroom.MarryEvent+=new MarryHandler(f2.SendMessage);
			//发出通知，只有订阅事件的对象才能接到通知
			birdegroom.OnMarryComing("朋友们，我结婚了，到时候准时参加婚礼");
			Console.WriteLine ("-------------------");
		}
	}

	//朋友类
	class Friend
	{
		public string Name;

		public Friend(string name){
			Name = name;
		}

		//事件处理函数
		public void SendMessage(string message){
			Console.WriteLine (message);
			Console.WriteLine (this.Name + "收到了，到时准时参加");
		}
	}
}
```

* 通过扩展EventArgs来传递数据
    我们需要声明一个派生自EventArgs的自定义类保存我们需要传入的数据。
    ​      
    ​        public class IncrenmentEventArgs:EventArgs{
    ​        public int IterationCount{get;set;}//存储整数}
* 要获得该类，用泛型版本的委托EventHandler<>(后续介绍泛型)，将自定义的类名称放在<>里
    `public event EventHandler<IncrenmentEventArgs> CountedADozen/事件名;`
* 移除事件处理程序 
  `p.SimpleEvent-=s.MethodB;`//移除使劲按处理程序MethodB
* 事件访问器 
  +=和-=是事件允许的位移运算符。看到这里我们应该知道，这些运算符有预定义的行为。这是高级主题我们不会深入研究
   有两个访问器：add和remove 和声明一个属性差不多。

        public event EventHandler CountedADozen{
         add{
          ...}
         remove{
         ...}
         }
### 接口
接口用于定义一组属性，方法和事件，但不能包含字段，接口的成员无需修饰，全部是公开的。
接口是指定一组函数成员而不实现他们的引用类型。所以只能类和结构实现接口，这么说比较抽象，先看一个例子：

    class CA{
        public string name;
        public int age;
    }
    class CB{
        public string Fisrt;
        public string Last;
        public double PersonsAge;
    }
    class Program{
        static void PrintInfo(CA item){
            Console.WriteLine("name:{0},age {1}",item,name,item.age);
        }
    
        static void Main(){
            CA a=new CA() {name="john",age=15};
            PrintInfo(a);
        }
    }

PrintInfo要传入的是CA类型，比如这个方法很用，如果想传入CB对象，这这时我们需要用到接口

    interface IInfo      //声明接口
    {
        string GetName();
        string GetAge();
    }
    
    class CA:IInfo      //声明实现接口的CA类
    {
        public string Name;
        public string Age;
        public string GetName(){return Name;}   //在CA类中实现两个接口方法
        public string GetAge(){return Age;}
    }
    
    class CB:IInfo      //声明实现接口的CB类
    {
        public string First;
        public string Last;
        public double PersonsAge;
        public string GetName(){return First+""+Last;} //在CB类中实现两个接口方法
        public string GetAge(){return PersonsAge.ToString();}
    }
    
    class Program
    {
        static void PrintInfo(IInfo item){    //传入接口的引用
            Console.WriteLine("Name:{0},Age{1}",item.GetName,item(),GetAge());
        }
        static void Main(){
            CA a=new CA(){Name="john doe",Age=35};
            CB b=new CB(){First="john",Last="doe",PersonsAge=33};
            PrintInfo(a);    //对象的引用能自动转换成它们实现的接口的引用
            PrintInfo(b);
        }
    }

* 声明接口
1. 不能包含**数据成员**和**静态成员**；
2. 函数成员不能包含任何实现代码，每个成员声明的主题后必须使用分号；
3. 惯例，接口名字必须从大写字母I开始（如：ISaveable);
4. 和类一样，接口声明还可以分割成部分接口声明。
5. 接口声明可有任何修饰符，而接口成员是**隐式public**,不允许有任何修饰符，包括public

            interface IMyInterface  //关键字+接口名称
            {
                int Dostuff(int nvar1,long lvar2); //分号代替了主体
                double Doothe(sting s,long x);     //分号代替了主体
            }
* 实现接口
1. 只有类和结构才能实现接口
2. 在基类列表中包含接口名称
3. 为接口每一个成员提供实现

            class MyClass:IMyInterface  //冒号 和 接口名
            {
                int Dostuff (int nvar1,long lvar2)
                {....} //实现代码 
                double Doothe(sting s,long x)
                {....} //实现代码 
            }

4. 若类从基类继承并实现了接口，基类在接口名前面，只能有一个基类，其他为接口名
   ` class Derived : MyBaseClass,IIfc1,IEnumerable,IComparaple{...}` //此处应实现多个接口。
5. 若派生类有:接口名，基类没有，但基类实现了接口的方法，那么，派生类即使是空的也能实现接口
6. 在类中显式实现接口,但这时，只能通过几口的引用来访问
    `void IIfc.PrinOut(string s) {...}` //显式实现接口
    `((Iifc)mc).PrintOut(""):`  //只能通过接口的引用来访问。
* 接口和as运算符
    * 接口不仅仅是类或结构要实现的成员列表，它是一个引用类型。
      我们可以把类对象引用强制转换为接口类型来获取指向接口的引用，然后可以用点号来调用接口方法。
      `IIfc1 ifc=(IIfc1) mc`
       IIfc1/接口  ifc/接口引用  = (IIfic1)/转换为接口   mc/类对象引用;
      `ifc.PrintOut();` //使用接口方法。
    * 但是另一更好的方式是使用**as运算符**，强制转换容易会抛出异常。
      `ILiveBirth b = a as ILiveBirth;`
      ILiveBirth/接口名，b/接口引用，a/类对象引用 
      `if(b!=null)  Console.WriteLine("baby is called:{0}",b.BabyCalled());`
      如果类实现了接口，表达式返回指向接口的引用，如果没有实现接口，表达式返回null而不是抛出异常。
    * 抽象类和接口
      相同点：
      (1) 都可以被继承
      (2) 都不能被实例化
      (3) 都可以包含方法声明
      (4) 派生类必须实现未实现的方法
      区 别：
      (1) 抽象基类可以定义字段、属性、方法实现。接口只能定义属性、索引器、事件、和方法声明，不能包含字段。
      (2) 抽象类是一个不完整的类，需要进一步细化，而接口是一个行为规范。微软的自定义接口总是后带able字段，证明其是表述一类“我能做。。。”
      (3) **接口可以被多重实现，抽象类只能被单一继承**
      (4) 抽象类更多的是定义在一系列紧密相关的类间，而接口大多数是关系疏松但都实现某一功能的类中
      (5) 抽象类是从一系列相关对象中抽象出来的概念， 因此反映的是事物的内部共性；接口是为了满足外部调用而定义的一个功能约定， 因此反映的是事物的外部特性
      (6) 接口基本上不具备继承的任何具体特点,它仅仅承诺了能够调用的方法    
      (7) 接口可以用于支持回调,而继承并不具备这个特点
      (8) 抽象类实现的具体方法默认为虚的，但实现接口的类中的接口方法却默认为非虚的，当然您也可以声明为虚的 
      (9) 如果抽象类实现接口，则可以把接口中方法映射到抽象类中作为抽象方法而不必实现，而在抽象类的子类中实现接口中方法













