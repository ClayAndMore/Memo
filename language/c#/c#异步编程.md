---
title: c#异步编程
date: 2016-05-10 14:52:38
categories: "c#"
tags: [c#,异步编程]
---

### 写在前面
* 一旦进程建立，系统会在Main方法的第一行语句处开始线程的执行。
* 线程锁：由于线程抢占处理器时间片，多个线程访问某个资源时出现不一致的问题，C#提供了**lock**关键字，该关键字可以对过个线程都要访问的资源进行锁定，哪个线程首先占有就把该资源锁定，其他想要访问该资源的线程只能等待该线程访问完成并**解锁**后才能访问资源。

<!-- more -->

###  一，async/await
C#5.0引入的一个用来构建异步方法的新特性
先看一个例子：

    class{
        static void Main(){
            Task<int> value = DoAsync.SumSync(5,6); //调用方法
        }
    }
    
    static class async Task<int> SumSync(int i1,int i2){   //异步方法
        int sum = await TaskEx.Run()(() => GetSum(i1,i2)); 
        return sum;
    }

如果一个程序调用某个方法，等待其执行所有处理后才继续执行，我们称这样的方法是同步的。
如上所示，异步方法在完成其工作之前要回到调用方法，然后再调用方法继续执行的时候完成其工作。 

* 调用方法：上面Main()函数里的方法，调用异步方法（可能在同线程，或者不同线程）执行其任务的时候，它自己继续执行。
* 异步（async）方法： 异步执行其工作，然后立即返回到调用方法。

异步方法语法上有如下特点：  

*   方法头中包含async方法修饰符，在返回类型之前，它只是包含await表达式，本身没啥用，不能创建任何异步操作。
*   包含一个或多个await表达式，表示异步可以完成的任务
*   参数可以任意类型和数量，但是不能为out或ref参数
*   必须具备这三种返回类型：

    * void，仅仅执行异步方法，包含return语句也不会返回任何东西
    * Task，不返回值，但要检查异步方法的状态，这时可以返回一个Task类型的对象。即使出现了return语句，也不会返回任何东西。
      `Task someTask = DoStuff.CalculateSumAsync(5,6);`
      `someTask.wait()`
    * `Task<T>` 返回值，返回T类型的值。
      `Task<int> value = DoStuff.CalculateSumAsync(5,6);`
*   除了方法，lambda表达式和匿名方法一可以作为异步对象
                **awati表达式**
                await表达式指定了一个异步执行的任务，
                ` awati + 空闲对象`
                默认情况下它是在当前线程下运行的,这么说吧，这个空闲对象是一个awaitable类型的实例，但是我们并不需要构建，只需要他-Task，异步方法返回`Task<T>`，放到await表达式中，他们将在当前线程中异步执行。返回这个空对象（即Task）我们最简单的方式是用**Task.Run()**方法来创建一个Task，关于Task.Run(),有一点非常重要，**它是在不同线程上运行你的方法**。
                Task.Run有个签名如下：
                `Task.Run( Func<TReturn> func)` 
                `Func<TReturn>`是个预定义的委托，返回值的类型为TReturn(就是泛型嘛）。
                因此将你的方法传递给Task.Run，需要基于Func创建一个委托，有三种方式 如下：
                
                      class Myclass {
                          public int Get10(){  //Get10 与 Func<int> 委托兼容，因为它没有参数，返回类型TReturn
                              return 10;
                          }


          public async Task DoWorkAsync(){
              Func<int> ten = new Func<int>(Get10);
              int a = await Task.Run(ten);  //用Get10创建Func<int>的委托ten给Task.Run
              
              int b = await Task.Run(new Func<int>(Get10)); //在参数列表中创建Func委托
              
              int c = await Task.Runc(() => { return 10; }); //与Func兼容的lambda表达式
              
              Consolo.WriteLine("{0} {1} {2}",a,b,c);    //输出：10 10 10 
              }
          }
          class Program{
              static void Main(){
                  Task t = (new MyClass()).DoWorkAsync();
                  t.Wait();
              }
          }
    **取消一个异步操作**
    System.Threading.Tasks命名空间有两个类是为此目的而设计的：CancellationToken和CancellationTokenSource
*   CancellationToken对象检查它的令牌（Token）状态，如果对象的IsCancellationRequested属性为true，任务停止并返回。一旦这个属性被改变就不能改回来了哦，一次性的。
*   CancellationTokenSource对象会为人物分配CancellationToken对象。持有CancellationTokenSource的对象可以调用其Cancel方法，这回将上面的属性设置为true。

                      class　Program{
                          static void Main(){
                              CancellationTokenSource cts = new CancellationTokenSource();
                              CancellationToken token = cts.Token;
                              
                              MyClass mc = new MyClass ();
                              Task T = mc.RunAsync(token);
                              
                              //Thread.Sleep(3000); //等待3秒
                              //cts.Cancle();       //取消操作
                              
                              t.Wait();
                              Console.WriteLine("Was Cancelled :{0}",token.IsCancellationRequested);
                          }
                      }
                      
                      class MyClass{
                          public async Task RunAsync (CancellationToken ct){
                              if (ct.IsCancellationRequested)
                              {
                                  return;
                                  await Task.Run( ()=> CycleMethod(ct),ct);
                              }
                          }
                          
                          void CycleMethod( CancellationToken ct){
                              Console.WriteLine("Starting CycleMethod");
                              const int Max = 5;
                              for( int i = 0; i < max ; i++){
                                  if( ct.IsCancellationRequested )
                                      return ;
                                      Thread.Sleep(1000);
                                      Console.WriteLine(" {0} of {1} iteration completed",i+1,max);
                              }
                          }
                      }
                      
                      //不取消注释时 
                      //输出： 
                      // Starting CycleMethod 
                      // 1 0f 5 iteration completed 
                      // 2 0f 5 iteration completed 
                      // 3 0f 5 iteration completed 
                      // 4 0f 5 iteration completed 
                      // 5 0f 5 iteration completed 
                      // Was Cancelled : False 
                      //取消注释
                      //输出：
                      // 1 0f 5 iteration completed 
                      // 2 0f 5 iteration completed 
                      // 3 0f 5 iteration completed 
                      // Was Cancelled : True 

---

###二，使用Tread类进行异步编程

* Tread类位于System.Threading命名空间，调用Thread类的**构造函数**创建新的Thread实例时，需要通过**委托**将新线程与一个现有的方法进行绑定，当线程启动后，就会执行该方法。
* 传递给Thread构造函数的委托有两种：一种表示不带参数的方法的委托，一种表示带一个object类型的委托。
* 在实例化Thread对象后，调用**Start方法**就可以启动执行线程，调用**Abort方法**终止线程并引发ThreadStateException异常。
* `Thread th1 = new Thread(Thread1);` 
    // Thread1是定义的一个线程方法，th1是多线程的实例，注意thread1后面没有括号
  eg:

        using System;
        using System.Threading;
        
        namespace ThreadTest
        {
            class Program
            {
                static void Main(string[] args)
                {
                    Thread th1 = new Thread(Thread1);  //创建线程
                    Thread th2 = new Thread(Thread2);
                    Thread th3 = new Thread(Thread3);
        
                    th1.Start();                        //开始线程
                    th2.Start();
                    th3.Start();
                    
                    th1.Priority = ThreadPriority.Highest;  //定义th1的优先级最高
                    th2.Priority = ThreadPriority.Normal;
                    th3.Priority = ThreadPriority.Lowest;
                    
                    Console.ReadLine();
                }
        
                static void Thread1()
                {
                    for(int i = 0; i < 1000; i++)
                    {
                        Console.WriteLine("线程1"+ "现在执行的次数: " + i);
                    }          
                }
                static void Thread2()
                {
                    for (int i = 0; i < 1000; i++)
                    {
                        Console.WriteLine("线程2"+"现在执行的次数: " + i);
                    }
                }
                static void Thread3()
                {
                    for (int i = 0; i < 1000; i++)
                    {
                        Console.WriteLine("线程3"+ "现在执行的次数: " + i);
                    }
                }
        
            }
        
        }
  共分五个优先级：
* Highest：最高优先级
* AboveNormal： 在Highest级别之后，Normal级别之前
* Normal：默认情况
* BelowNormal： 在Normal之后，在Lowest之前
* Lowest： 最低优先级
  状态控制：
* Start(): 开始
* Abort(): 终止
* Join(): 阻塞
* Sleep(): 休眠
   如果多线程不能同时访问一个资源，所以引入“锁”的概念，如果一个线程读或者写资源的时候，其他线程就被锁住不能访问，当这个线程完成工作后就解开锁，允许其他线程进行读/写。这种机制C#称为线程的“同步“
  eg:

            using System;
            using System.Threading;
            
            namespace ThreadTest
            {
                class Program
                {
                    static void Main(string[] args)
                    {
                        TestThreadTestClas test = new TestThreadTestClas();
                        Thread A = new Thread(test.Add);
                        A.Name = "zheA";
                        A.Start();
            
                        Thread B = new Thread(new ThreadStart(test.Add)); //显式声明一个委托，注意Add没有括号
                        B.Name = "theB";
                        B.Start();
            
                        Console.ReadLine();
             
                    }
            
                    public class TestThreadTestClas
                    {
                        private object obj = new object();
                        private int num = 0;
            
                        public void Add()
                        {
                            while (true)
                            {
                                lock (obj)
                                {
                                    num++;
                                    Thread.Sleep(100);
                                    Console.WriteLine(Thread.CurrentThread.Name + ";" + num);
                                }
                            }
                        }
                    }
                }
            
            }
  定义了两个线程，累计打印变量num，num就是竞争性资源

---

###三，通过委托执行异步操作
如果委托对象在调用列表中只有一个方法，就可以异步执行这个方法。
委托类有两个方法：**BeginInvoke和EndInvoke**

*   当我们调用委托的BeginInvoke方法时，它开始在一个独立线程上执行引用方法，并且立即返回到原始线程。原始线程可以继续，二引用方法会在线程池的线程中**并行**执行。
*   当程序希望获得已完成的异步方法的结果时，可检查BeginInvoke返回的**IAsyncResult**（它表示线程的状态）的IsCompleted属性，或者调用委托的**EndInvoke**方法等待委托完成。这一过程有三种标准模式：
                ![](http://7xs1eq.com1.z0.glb.clouddn.com/aync.png)
    * 在等待一直到完成模式中，发起了异步方法后，原始线程就**中断**等待异步方法完成后再继续。
    * 轮询模式中，原始线程定期检查发起的线程是否完成，如果没有则可以做其他的事。
    * 回调模式中，原始线程**一直进行**,无需等待或检查发起的线程是否完成。

下面我们来研究一下BeginInvoke和EndInvoke,有关BeginInvoke的事项如下：

*   调用BeginInvoke时，参数列表世界参数数组如下：
    * 引用方法需要的参数
    * 两个额外的参数——callback和state
*   BeginInvoke从线程池中获取一个线程并且让引用方法在新的线程中开始。
*   返回给调用线程一个实现**IAsyncResult**接口的对象的引用。这个接口包含了线程池中运行的异步方法的**当前状态**。

                      delegate long MyDel(int first,int second); //声明委托
                      static long Sum(int x, int y){...}        //方法匹配委托
                      Mydel del=new MyDel(Sum);                 //创建委托对象
                      IAsyncResult/有关新线程的信息 ar=del.BeginInvoke/异步调用(3,5,null,null);  //3，5是委托参数，null，null是额外参数
                EndInvoke方法用来获取由异步方法调用返回的值，并释放线程使用的资源。
*   它接受一个由BeginInvoke发放返回的IAsynResult对象的引用，并找到相关联的线程。
*   如果线程池的线程已经退出，它会清理线程的状态并释放资源，它找到**引用方法返回的值**并且把它作为返回值。
*   如果当EndInvoke被调用时线程仍然运行，调用线程就会停止等待，知道清理完毕并返回值，确保对每一个BeginInvoke都调用EndInvoke
*   如果异步方法触发了异常，在调用EndInvoke时会抛出异常。
*   下面是调用EndInvoke并从异步方法获取值的示例。必须把IAsyncResult对象的引用作为参数。

                      long result=del.EndInvoke(ar);  //long 为异步方法的返回值
                      long result=del.EndInvoke(out soneInt,ai); //如果委托的引用方法有ref和out参数，也要包含在参数列表

下面我们来看第一种模式：等待一直到结束模式

        using Systerm;
        using Systerm.Threading;
    
        delegate long MyDel(int first,int second);
    
        class Program{
            static long Sum(int x,int y){
            Console.WriteLine("Inside Sum");
            Thread.Sleep(100);
    
            return x+y;
        }
    static void Main(){
        MyDel del=new MyDel(Sum);
    
        Console.WriteLine("Before BeginInvoke");
        IAsyncResult ar=del.BeginInvoke(3,5,null,null);//开始异步调用
        Console.WriteLine("After BeginInvoke");
    
        Console.WriteLine("doing stuff");
    
        long result=del.EndInvoke(ar);   //等待结束并获取结果
        Console.WriteLine("After EndInvoke:{0}",result);
        
        Console.WriteLine("doing stuff");
    }
    } 
    //输出：Before BeginInvoke
            After  BeginInvoke
            Doing stuff
            Inside sum
            After EndInvoke:8
            doing stuff            //从这里可以看出主线程在等待新线程完成

轮询模式
使用IAsyncResult对象的IsComplete属性来定期检查开启的线程是否完成，如果异步方法完成，原始线程就调用EndInvoke并继续。没完成，就做一些处理，一会再检查，下面的示例 ‘处理’是0数到10000000

        using System;
        using System.Threading;
    
        namespace beginInvoke
    {
    delegate long MyDel(int first, int second);
    
    class Program
    {
        static long Sum(int x, int y)
        {
            Console.WriteLine("Inside Sum");
            Thread.Sleep(100);
    
            return x + y;
        }
        static void Main()
        {
            MyDel del = new MyDel(Sum);
    
            Console.WriteLine("Before BeginInvoke");
            IAsyncResult ar = del.BeginInvoke(3, 5, null, null);//开始异步调用
            Console.WriteLine("After BeginInvoke");
    
            while (!ar.IsCompleted)
            {
                Console.WriteLine("not done");
                //继续处理
                for (long i= 0; i < 10000000; i++)
                    ;
            }
    
            Console.WriteLine("done");
    
            long result = del.EndInvoke(ar);   //等待结束并获取结果
            Console.WriteLine("After EndInvoke:{0}", result);
            Console.WriteLine("doing stuff");
        }
    }
    }
    输出：Before BeginInvoke
        After BeginInvoke
        not done
        Inside Sum
        not done
        not done
        not done
        done
        After EndInvoke:8
        doing stuff

回调模式
一旦初始线程发起异步方法，就自己管自己。在异步方法调用结束之后，系统会调用一个用户自定义的方法（回调方法）处理结果，并调用委托的**EndInvoke**方法。
1，在会回调方法中调用BenginInvoke，BenginInvoke的参数列表中最后两个额外参数由回调方法使用。

*   第一个参数callback，是回调方法的名字，这个参数是AsnycCallback类型的委托。
*   第二个参数state，可以是null或者要传入回调方法的一个对象的引用。我们可以通过IAsyncResult参数的AsyncState属性来获取这个对象，参数的类型是object。

                      IAsyncResult ar1=del.BeginInvoke(3,5,new AsnycCallback(CallWhenDone)/使用回调方法创建委托,null);
                      IAsyncResult ar2=del.BEginInvoke(3,5,CallWhenDone/直接使用回调方法的名字编译器自动为我们创建委托,null);
                2，在回调方法中调用EndInvoke
                此时，需要委托对象的引用，**但是它在初始线程内，而不在新的线程内。**如果不使用BeginInvoke的state参数做其他用途，我们可以给它发送委托的引用给回调方法
                ![](http://7xs1eq.com1.z0.glb.clouddn.com/asyncResult.png)
    * 给回调方法的参数只有一个就是刚结束异步方法的IAsyncResult接口的引用
    * IAsyncResult接口没有委托对象的引用，封装它的**AsyncResult**类对象有委托对象的引用AsyncDelegate.上图方法体第一行代码里通过转换接口引用为类类型来获取类对象的引用。
    * 有了类对象的引用，可以调用类对象的AsyncDelegate属性并且转换为何时的类型。这样就得到了委托引用，用它来调用EndInvoke.
      完整代码：

            using System;
            using System.Threading;
          
            namespace beginInvoke
            {
            delegate long MyDel(int first, int second);
          
            class Program
            {
            static long Sum(int x, int y)
            {
                Console.WriteLine("Inside Sum");
                Thread.Sleep(100);
          
                return x + y;
            }
            static void CallWhenDone(IAsyncResult iar){
            Console.WriteLine("Inside CallWhenDone");
            AsyncResult ar=(AsyncResult) iar;
            MyDel del=(MyDel)ar.AsyncDelegate;
            
            long result=del.iar.EndInvoke(ar);
            Console.WriteLine("After EndInvoke:{0}", result);
            }
            static void Main()
            {
                MyDel del = new MyDel(Sum);
            
            Console.WriteLine("Before BeginInvoke");
            IAsyncResult ar = del.BeginInvoke(3, 5, new  AsyncCallback(CallWhenDone), del);//开始异步调用 del换成null也可以。。
            Console.WriteLine("After BeginInvoke");
          
            Console.WriteLine("done more work in the main ");
            Thread.Sleep(500);
          
            Console.WriteLine("done with main ,exting");
                }
            }
            }
            输出：  Before BeginInvoke
                    After BeginInvoke
                    done more work in the main                      
                    Inside Sum
                    Inside CallWhenDone
                    After EndInvoke:8
                    done with main ,exting


---

**四，计数器**
计时器提供了一种定期重复运行异步方法的方式，这里接受的不是Timer类中的，而是 using System.Threading下的

* 每次时间到期之后调用回调方法，回调方法必须是TimerCallback委托形式的，结构如下，它接受了一个object类型为参数，并且返回类型void
  `void TimerCallback(object state)`
* Timer类有很多构造函数，最常用的形式如下：
  ` Timer(TimerCallback callback,object state,uint dueTime,unit period)`
  当计时器到期之后，系统会从线程池中的线程开启一个回调方法，提供state对象作为其参数
  dueTime是回调方法首次被调用之前的时间，如果被设置为Timeout,Infinite，则不会开始，如为0，回调函数立即被调用。
  period是两次成功调用回调函数之间的时间间隔，如果设置为Timeout.Infinite，首次被调用之后不会再被调用。

        Timer myTimer=new Timer(MyCallback/回调的名字,someObject/传给回调的对象,2000,1000);//在2000毫秒后第一次调用，每1000毫秒调用一次
* 一但TImer对象被创建，我们可以用Change方法来改变它的dueTime或者period方法。        

            using System;
            using System.Threading;
      
            namespace Timers
            {
            class Program
           {
            int TimesCalled = 0;
      
            void Display(object state)
            {
                Console.WriteLine("{0} {1}", (string)state, ++TimesCalled);
            }
        
            static void Main()
            {
                Program p = new Program();
        
                Timer myTimer = new Timer(p.Display, "Processing timer event", 2000, 1000);
        
                Console.WriteLine("timer start");
        
                Console.ReadLine();
            }
        }
          }
          输出：timer start
                Processing timer event 1
                Processing timer event 2
                Processing timer event 3
                Processing timer event 4
                Processing timer even  一直加。。










