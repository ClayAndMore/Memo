tags: [c#] date: 2016-04-12 


### 七.语句
* swith语句，和c++不同，每一个swith段，包括可选的default段，必须以一个跳转语句结尾，除非在两个分支标签之间没有可执行代码；
  eg:

        swith(x){
         case 1:                        //如果x=1,2,3执行该代码。
         case 2:
         case 3:
         ...
         break;
         case 5: y=x+1;                 //因为没有break，所以不可接受。
         case 6: ...
  <!-- more -->

* *标签语句和goto语句**
  给语句添加一个标签允许从代码的其他部分转移到该语句。只能在块内使用。
  由一个标识符后面跟着一个冒号再跟着一条语句组成。
  Identifier：Statement

        bool thingFine；
        while(true){
         thingFine=GetNuclearReactorCondition();
         if(thingFine)
          Console.WriteLine("Things are Fine");
         else
          goto NotSoGood;
         }
         NotSoGood: Console.WriteLine("We have a problem.");  //转到标签
  goto语句在swith内部，把控制转到swith语句内部的相应分支标签
  `goto case ConstantExpression;`
  `goto default;` 

* **using语句**
  **非托管**对象可能限制或消耗系统资源，在代码使用后，using语句对其进行处理。减少了意外错误，整洁包装资源的使用，资源是一类或者代码。
  语法： using（resourceType Identifier=Expressoion/分配资源） statement/使用资源的代码
  eg:`using（ResType Resoure=new ResType(...) {Statement}`和if一样 当语句不止一条时有中括号。
  上面语句实际等于：
  ​      
  ​       {                      //整个结构被封闭在一个隐式的块中，当finally块退出时，资源失效并不会意外的被调用。
  ​          ResType Resoure=new ResType(...);
  ​          try{
  ​           statement
  ​          }
  ​          finally{
  ​           Dispose of resource  //释放资源，由using隐式提供
  ​          }
  ​      }
  编译器接受using语句的元素并产生隐式的try...finally对以处理潜在的异常。

* **其他语句**
  checked unchecked           控制溢出上下文
  foreach                     便利一个集合的每个成员
  try throw finally           处理异常
  yield                       用于迭代
  后续章节介绍。 

---

### 八.结构
* 结构是值类型，放在栈中
* 在结构中初始化字段是不允许的。

        struct Simple{
         public int x=0;// 编译错误
        }   
* 结构是密封，不能派生其他结构。
* 如同其他值类型数据，将一个结构实例作为引用类型对象，必须创建**装箱**的副本。装箱的过程就是制作值类型的引用类型副本。后续描述。

---

### 九.枚举
*    与结构一样，枚举也是值类型。
*    每个枚举类型都有一个底层整数类型，默认为int.
*    默认情况下，编译器把第一个成员赋值为0，并对后续成员赋的值比前一个多1；
*    可以把冒号和类型名放在枚举名之后，可以使用int以外的整数类型。
     ​               `enmu Tranfficilight:ulong{ }`
*    **位标志**
     ​               长期使用单个字的不同位作为一组开/关标志的紧凑方法。
     ​               确定需要多少个位标志，并选择一种有足够多的无符号类型来保存它。
     ​               确定每个位代表什么，并给它们一个名称。
     ​               使用按位或（OR）运算符设置保持该位标识的字中适当的位。
     ​               使用按位与（AND)运算符，或HasFlag方法揭开位标识，
     ​               经常使用十六进制表示位模式，
     ​               用[Flag]修饰枚举，实际上不是必要的，但可以有写额外的便利，后续。
     ​             
     ​                     [Flag]
     ​                     enum Settings : uint
     ​                     {
     ​                      SingleDeck    = 0x01,  //位0
     ​                      LargePictures = 0x02,  //位1
     ​                      FancyNumbers  = 0x04,  //位2
     ​                      Animation     = 0x08   //位3   注意：最后的变量没有逗号。
     ​                      }
     ​                      //创建一个带有适当的位标识的字，需要声明一个该枚举类型的变量，并使用按位或运算符设置需要的位
     ​                      Settings ops（标志字） = Settings.SingleDeck|Settings.FancyNumers|Settings.Animation;
     ​                      //判断标志字师傅偶含有特定的位标识集，可使用枚举类型中的HasFlag布尔方法。  如果使用了指定的位标识，返回true。
     ​                      bool useFancyNubers = osp.HasFlag(Settings.FancyNumbers);
     ​                谈flag特性，可通知编译器该枚举的成员不仅可以用作单独的值，还可以按位标识进行组合，它允许枚举的ToString方法为位标识的值提供更多格式化信息。
     ​                ToString方法以一个枚举值作为参数，将其与枚举的常量成员进行比较，如果与某个成员匹配，返回该成员的字符串名称。接上面例子：
     ​               ​      
     ​                     class Program{
     ​                     static void Main(){
     ​                      Setings ops;
     ​                   
     ​                      ops=Setings.FancyNumbers;
     ​                      Console.WriteLine(ops.ToString());  //输出：FancyNumbers
     ​                   
                           ops=Setings.FancyNumbers|Setings.Animation;
                           Console.WriteLine(ops.ToString());  //输出：12（没有Flag标识），输出：FancyNumbers,Animation(有Flag标识)
                          }
                          }
                    **关于枚举的补充**：
*    不能对成员使用修饰符，它们隐式的具有枚举相同的可访问性。
*    由于成员是常量，没有该枚举的变量也可以访问，使用枚举类型名，跟着一个点和成员名。
*    可以比较同一枚举的变量，**不可以比较不同枚举的变量**
*    .NET Enum类型（enum基于该类型），有一些有用的静态方法：
     * GetName方法，枚举类型对象和值为参数，返回响应的枚举成员的名称
     * GetNames方法以枚举类型对象为参数，返回该枚举中所有成员的全部名称。

             enum Color{
                 Green,
                 Yellow,
                  Red
             }       
               
             class Program{
               static void Main(){
                 Console.WriteLine("Second member of Color is {0}",Enum.GetName(typeof(Color),1)); //输出：Second member of Color is Yellow。
               
             foreach (var name in Enum.GetNames(typeof(Color)))
              Console.WriteLine(name); //输出：Green \n Yellow \n Red
                 }
                 }

    **注意**：这里用了typeof运算符来获取枚举类型对象。
---

###十.数组
看数组之前，我们先看图，看数组的类型
![](leanote://file/getImage?fileId=5742f551ab64413fd7019f12)
这里要注意 new int[4]返回的是一个地址，就是arr.

*   所有元素必须是相同类型
*   可以为任何整数的维度，数组的维度成为秩（rank)
*   每一个维度有个长度，就是这个方向的位置个数
*   所有维度元素总和成为数组的长度
*   一但创建，大小固定，C#不支持动态数组
*   矩形数组和交错数组，矩形数组 每个维度有相同长度的多维数组。，不管有多少维度，总是用一组方括号。
    ​          ` int x=myArray[4,6,1];`
    ​          交错数组都是独立的多维数组，子数组不同长度，为每个维度使用一对方括号。
    ​          ` jagArray1[2][7][4]`
*   **数组是引用类型**，但数组的元素可以是值类型或是引用类型
*   声明一维数组或者矩形数组，在类型名和变量名之间用一组方括号，括号内的逗号是秩说明符，没有逗号一维数组，一个逗号而为数组，以此类推。维度长度到数组实例化才能确定
    ​          ` int[,,] firstArray;// 三维整型数组`
    ​          `long[2,3,5] secondArray;//错误，声明时括号内不允许放维度长度。
*   实例化 用new运算符构成。
    ​          ` int[] arr2=new int[4] ;//四个元素`
    ​          `MyClass[] mcArr=new MyClass[4]; //四个元素，数组里放引用`
*   初始化
    ​          `int [] intArr=new int[] {10,20,30,40};  //一维数组`
    ​          `int [,] intArr2=new int[] {{10,1},{2,10},{11,9}}; //二维数组`
    ​          `int [,,] intArr3=new int[] { {{10,1},{5,2},{6,4}},{{2,3},{3,5},{2,6}} };`
*   实例化交错数组

                    int[][] Arr =new int[3][];          //实例化顶层数组
                    Arr[0]= new int[] {10,20,30};       //实例化子数组
                    Arr[1]= new int[] {10,20,30,40};
                    Arr[2]= new int[] {10,20,30,40,50};

*   在CIL中，一维数组有助于优化，有时候使用一维数组的交错数组比矩形数组更有效率。
*   **foreach语句**
    ​          可以连续访问数组中的每一个元素。
    * 迭代变量是临时的，类型和数组元素的相同
    * 声明：
      `foreach(Type/var Identifier/迭代变量 in ArrayName) statement/语句`

            int[] arr1={10,11,12,13};
            foreach(int item in arr1)
             Console.WriteLine("{0}",item);
      输出：10 11 12 13
    * 迭代变量不可改变，是只读的，如上 item++ 就错了。对于数值型数组和引用型数组都是这样，但是可以通过迭代变量改变引用类型的数据值：
      ​      
      ​      class MyClass{
      ​       public int MyField=0;
      ​      }
      ​    
      ​      class Program{
      ​       static void Main(){
      ​       MyClass[] mcArray=new MyClass[4];   //创建数组
      ​      for(int i=0;i<4;i++){
      ​        mcArray[i]=new MyClass();       //创建类型对象
      ​        mcArray[i].MyField=i;           //设置字段
      ​       }
      ​       foreach (MyClass item in mcArray) 
      ​       item.MyField+=10;                 //改变数据
      ​    
      ​       foreach (MyClass item in mcArray)
      ​       Console.WriteLine("{0}",item.MyField);
      ​      }
      ​      }
    * 对于多维数组，处理次序是最右边的索引号最先递增，到n-1时，开始递增左边的索引，右边的被置换成零。
*   **数组协变**
    ​          即使某个对象不是数组的基类型，我们可以把它赋值给数组元素。这种属性叫做数组协变。要求：
    * 数组是**引用类型**数组
    * 在赋值的对象类型和数组类型之间有隐式转换和显式转换，由于在**派生类**和基类之间有隐式转换，因此总是可以将一个派生类的对象赋值给**基类声明**的数组。

            class A{...}
            class B:A{...}
            class Program{
             static void Main(){
              A[] Array1=new A[3];
              A[] Array2=new A[3];
             //普通：将A类型的对象赋值给A类型的数组
              Array1[0]=new A();
              Array1[1]=new A();
              Array1[2]=new A();
            //协变：将B类型的对象赋值给A类型的数组
              Array2[0]=new B();
              Array2[1]=new B();
              Array2[2]=new B();
          }
        }
*   Clone方法
    ​           C#数组从Systerm.Array类继承。可以继承基类很多有用的属性和方法，Clone方法为数组进行浅复制。克隆值类型会产生两个独立数组。克隆引用类型数组会产生指向相同的对象的两个数组。
    ​           Clone方法返回object类型的引用，必须强制转换成数组类型。
    ​          `int[] intArr=(int[]) intArr.Clone();


### 十一.泛型

*  如果我们把类的行为提取或重构出来，使之不仅能应用到他们编码的数据类型上，而且还能应用到其他类型上，类会更有用，我们可以重构代码并且额外增加一个抽象层，数据不用硬编码了。这是专门为多段代码在不同的数据类型上执行相同指令情况专门设计的，泛型提供了一种优雅的方式，让多个类型共享一组代码。
   先看一示例：

          class MyStack<T>
        {
            int StackPointer=0;
            T [] StackArray;
        
            public void Push(T x){...}
        
            public T Pop(){...}
        }


上例中，类型占位符T（可以是任意字符），在类名后放置占位符和尖括号，每一个T在编译器中都会替换为实际类型。

*   **泛型类不是实际的类，而是类的模板**，所以我们必须先从他们构建实际的类类型，然后创建这个构建后的类类型的实例。声明和正常类一样，类后加尖括号，实现一般用var  
    `var mySc=new SomeClass<short,int>();`
*   泛型参数的约束
    ​          并不是所有的参数泛型都能接受，需要对泛型进行约束，这时使用了**where**子句。语法如下
    ​         where/关键字 TypeParam/参数类型：constraint，constraint,.../约束列表
    ​        
    ​              class MyClass<T1,T2,T3>
    ​                          where T2:Customer    //T2的约束
    ​                          where T3:IComparable //T3的约束
    ​                  {....}        
    ​        T1是未绑定的，对于T2，只有Customer类型或从Customer继承的类的类型才能作用于类型实参，对于T3，只用实习那IComparable接口的类餐能用于类型实参
    ​        有五种约束类型：
    * 类名:    只有这个类型的类或从它继承的类才能作用类型实参。
    * class：  任何引用类型，类，数组，委托和接口都可以作用类型实参。 
    * struct： 任何**值类型**都可以用作类型实参
    * 接口名：只用这个接口或实现这个接口的类型才能作用类型实参。
    * mew()：   任何带有无参公共构造函数的类型都可以作用类型实参，这叫做构造函数的约束。
*   **泛型方法**
    * 声明

            public void PrintDate<S,T> (S p,T t) where S;Person  //类型参数列表在方法名称后，在方法参数列表之前
            {...}
*   调用

                      MyMethod<short,int>();
                      MyMethod<int,long>();
                      //如果有参数传入方法，编译器可以推断类型    
                      MyMethod<int>(myInt);  简化成： MyMethod(myInt);
*   **扩展方法和泛型类**
    ​        扩展方法可以和泛型类结合使用，允许我们将类中的静态方法关联到不同的泛型类上，还允许我们像调用类构造实例的实例方法一样来调用方法。
    ​        和非泛型类一样，泛型类的扩展方法：
    * 必须声明为static
    * 必须是静态类的成员
    * 第一个参数类形中必须有关键字this，后面是扩展的泛型类的名字。

            static class ExtendHolder{
                public static void Print<T>(this.Holder<T> h){
                    T[] theVals=h.GetValues();
                    Console.WriteLine("{0},{1},{2}",theVals{0},theVals{1},theVals{2});
                }
            }
            
            class Holder<T> {
                T[] Vals=new T[3];
                public Holder(T v0,T v1,T v2){
                    Vals[0]=v0; Vals[1]=v1; Vals[2]=v2;
                }
            
                public T[] GetValues() {return Vals;}
            }
            
            class Program{
                static void Main(string[] args){
                    var intHolder   = new Holder<int>(3,5,7);
                    var stringHolder= new Holder<string("a1","b2","c3");
                    intHolder.Print();
                    stringHolder.Pring();
                }
            }
*   **泛型委托**
    ​        泛型委托和非泛型委托非常相似，不过类型参数决定了能接受什么样的方法。
    ​        如下有一个泛型委托的示例。在Main中，泛型委托MyDelegate使用string类型的实参实例化，并且使用PrintString方法初始化。
    ​        
    ​              delegate void MyDelegate<T>(T value);//泛型委托
    ​        
    ​              class Simple
    ​              {
    ​                  static public void PrintString(string s){
    ​                      Console.WriteLine(s);
    ​                  }
    ​              
                      static public void PrintUpperString(string s){
                          Console.WriteLine("{0}",s.ToUpper());
                      }
                  }
                  
                  class Program{
                      static void Main(){
                          var myDel=new MyDelegate<string>(Simple.PrintString);  //创建委托的实例
                          myDel+=Simple.PrintUpperString;   //添加方法
                  
                          myDel("Hi There");        //调用委托
                      }
                  }
*   **协变**
    ​        如果创建泛型类型的实例，编译器会接受泛型类型声明以及类型参数来创建构造类型。但是，大家通常会犯的一个错误就是将派生类型分配给基类型的变量。
    ​        每一个变量都有一种类型，可以将任何派生类对象的实例赋值给基类的变量，这为赋值兼容性。如下：
    ​        ​          
    ​              class Animal{
    ​                  public int NumberOfLegs=4;
    ​              }
    ​              class Dog:Animal{
    ​              
    ​              }
    ​              
    ​              class Program{
    ​                  static void Main(){
    ​                      Animal a1=new Animal();
    ​                      Animal a2=new Dog();
    ​              
                          Console.WrieLine("Number of dog legs：{0}",a2.NumberOfLegs);
                      }
                  }            
                  输出：Number of dog legs :4
            创建了一个Dog类型的对象，并将它赋值给Animal类型的变量a2。
            下面我们看一个更有意思的例子：
            
                  class Animal{   public int Legs=4;}
                  class Dog:Animal{}
                  
                  delegate T Factory<T>(); //委托
                  
                  class Program{
                      static Dog MakeDog(){
                          return new Dog();
                      }
                  
                      static void Main(){
                          Factory<Dog>      dogMaker=MakeDog; //创建委托对象
                          Factory<Animal> animalMake=dogMaker;//尝试赋值委托对象
                  
                          Console.WriteLine(animalMake().Legs.ToString());
                      }
                  }
            这时，main函数中的第二行会出现问题，看上去派生类构造的委托应该可以赋值给由基类构造的委托，那么编译器为什么会出现错误呢？问题在于尽管Dog是Animal的派生类，但是Factory<Dog>没有从Factory<Animal>派生。两个委托对象是同级的，他们都从delegate类型派生，两者没有相互之间的派生关系，因此赋值兼容性不适用。
            再仔细分析一下这种情况，如果参数类型（Animal等）只用作输出值，同样的情况也使用于任何委托，我们应该可以使用派生类创建的委托类型，这样能够正常工作，因为**代码总是期望得到一个基类的引用**，这也是正是它会得到的。
            **如果派生类这是用于输出值，那么这种结构化的委托有效性之间的常数关系叫做协变**
            为了让编译器知道我们的期望，我们要用out关键字标记委托声明中的类型参数。
            ` delegate T Factory<out T>();`
            这是可行的，尽管在调用委托的时候，调用代码接受Dog类型的对象，而不是期望的Animal类型的对象，但是调用代码完全可以像之前期望那样自由地操作对象的Animal部分。

*   **逆变**
    ​        现在已经了解了协变，我们来看一种相关状况，和之前的情况相似，默认情况下可以赋值两种不兼容的类型。
    ​        **在期望传入基类时，允许传入派生对象的特性叫做逆变**
    ​        
    ​              class Animal { public int NumberOfLegs=4;}
    ​              class Dog:Animal{}
    ​              
    ​              class Program{
    ​                  delegate void Action<in T>(T a);
    ​              
                      static void ActionOnAnimal(Animal a){
                          Console.WriteLine(a.NumberOfLegs);
                      }
                      static void Main(){
                          Action<Animal> act1=ActionOnAnimal;
                          Action<Dog>    dog1=act1;
                          dog1(new Dog());
                      }
                  }
            比较协变和逆变：
            ![](http://7xs1eq.com1.z0.glb.clouddn.com/nibanAndxiebian.jpg)
            协变：
    * 左边栈上的变量是F<out T> ()类型的委托，类型变量是叫做Base的类
    * 在右边实际构建的委托，使用Derived类的类型变量进行声明，这个类派生自Base类
    * 这样可以工作，因为在调用的时候，方法返回指向派生类的对象的引用，派生类型同样指向其基类，调用代码可以正常工作
      逆变：
    * 左边栈上的变量是F<int T> (T p)类型的委托，类型参数是Derived类。
    * 在右边实际构建委托的时候，使用Base类的类型变量进行声明，这个类是Derived类的基类
    * 这样可以工作，因为在调用的时候，调用代码传入了派生类型的变量，方法期望的只是其基类，方法完全可以像以前那样操作对象的基类部分。
*   **接口的协变和逆变**

                  class Animal{public string Name;}
                  class Dog:Animal{};
                  
                  interface IMyIfc<out T>
                  {
                      T GetFirst();
                  }
                  
                  class SimpleReturn<T>: IMyIfc<T>
                  {
                      public T[] items=new T[2];
                      public T GetFirst(){return items[0];
                  }
                  
                  class  Program
                  {
                      static void DoSometing (IMyIfc<Animal> returner){
                          Console.WriteLine(returner.GetFirst().Name);
                          
                          IMyIfc<Animal> animalReturner=dogReturner;
                          
                          DoSometing(dogReturner);
                      }
                  }
    * 代码使用类型参数T声明了泛型接口。out关键字指明了类型参数是协变的。
    * 泛型类SimpleReturn实现了泛型接口。
    * 方法DoSometing演示了方法如何接受一个接口作为参数，这个方法接受由Anima类型构建的泛型接口IMyIfc作为参数。
    * Main下面一行把这个对象赋值给一个栈上的变量，这个变量声明为构建的接口类型IMyIfc Animal,对于这个声明注意以下两点，赋值左边的类型是接口而不是类。尽管接口类型不完全匹配，但是编译器允许这种赋值，因为在接口声明中定义了out协变标识符。
