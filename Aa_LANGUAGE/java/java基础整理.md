---
title: java基础整理
date: 2016-07-10 08:51:37
categories: java
tags: java
---

## jvm

## 初入理解
* 每一个应用程序，都有一个JVM ，而不是 多个应用程序，共享一个jvm

* java源文件，首先通过编译器，把java语法的代码，编译成 jvm语法的字节码文件 这个过程，是**不涉及到jvm**的。然后，jvm通过类加载，把需要的类字节码文件，加载进内存中。

* jvm运行时内存分为两部分：线程共享内存和线程私有内存

    * 线程共享内存包括：堆、方法区（包含 运行时常量池） 
    * 线程非共享内存包括：java栈，本地方法栈，PC程序寄存器 

每个线程，都有一份独有的线程非共享内存。

具体结构：
![](http://7xs1eq.com1.z0.glb.clouddn.com/jvm%E5%86%85%E5%AD%98%E6%A8%A1%E5%9E%8B.png)

* pc程序寄存器:记录某个线程当前执行到哪条字节码
* 本地方法栈: 类似于java栈，但是是为了native方法准备的

* java栈:很重要。每个线程都有一个java栈，它是为java方法准备的。栈里面存储着一个个 栈帧，每一个栈帧可看做一个方法的调用

* java堆，存放对象实例，数组。

* 方法区:不是执行方法的。执行方法的内存，是在　ｊａｖａ栈中。 
  方法区是涉及到类加载的时候，加载进来的类的信息，常量，字段，方法代码等的信息,而运行时常量池是方法区的一部分。其中存储的是，字面常量，符号引用等。

* 栈帧包括：局部变量表，操作数栈，方法返回地址，其他信息。其中操作数栈，才是和cpu中的ＡＬＵ联系在一起的。是ｃｐｕ唯一指定的数据来源。　执行一条指令，其中涉及到的操作，就是在　（局部变量表和操作数栈中进行的）。


当加载的类很多的时候，方法去也会溢出。 
～～～～～～～～～～～～～～～～～～～～～～～～～～～～ 
线程私有内存：ｊａｖａ栈，本地方法栈，这些都和线程有关，和线程的生命周期相同，一旦线程结束，相应的内存也将释放，所以这部分内存不需要关心回收

我们的垃圾回收主要是针对　堆内存。不过，方法区的内存是永久区，一般也不需要考虑回收。

## java string
###  内部机制
* 字符串是常量；它们的值在创建之后不能更改。是对象的创建，一旦被赋值就不能被改变。注意：这里指的是字符串的内容，而引用是可以再次赋值的，所以字符串的拼接非常浪费内存


* String s = new String("hello") 和 String s = "hello" 是不一样的

  ![](http://7xs1eq.com1.z0.glb.clouddn.com/newString%E5%8C%BA%E5%88%AB.png)


判断两个String变量：

```java
string s1 = "hello";
String s2 = new String("hello");
Systerm.out.println(s1==s2); 
Systerm.out.println(s1.equals(s2));
```
s1,是编译期就放在常量池里，而s2是运行期才确定位置。
由图可见，s1,s2两个引用指向的不同。
第一个判断两个变量指向的地址是否相等，输出false。

第二个判断两个变量的内容是否相等，输出true。

* 如果字符串变量相加，先开空间，在相加储存

  如果**字符串常量相加，先加，在常量池里面找，如果有就返回常量池里的地址，否则就创建新的空间**。

  ```java
          String ss1 = "hello";
          String ss2 = "world";
          String ss3 = "helloworld";

          System.out.println(ss3.equals(ss1+ss2));

          System.out.println(ss3 == ss1 + ss2); //false ，变量
          System.out.println(ss3 == "hello"+"world");//true，常量
  ```
  ​

### intern()方法
String的intern()方法就是扩充常量池的一个 方法；当一个String实例str调用intern()方法时，Java查找常量池中是否有相同Unicode的字符串常量，如果有，则返回其的引用， 如果没有，则在常量池中增加一个Unicode等于str的字符串并返回它的引用；看例3就清楚了 
```
String s0= “kvill”; 
String s1=new String(”kvill”); 
String s2=new String(“kvill”); 
s1.intern(); 
s2=s2.intern(); //把常量池中“kvill”的引用赋给s2 
System.out.println( s0==s1);  // false,虽然s1调用了intern()，但是没有把结果赋值给s1.
System.out.println( s0==s1.intern() ); //true
System.out.println( s0==s2 ); //true
```

### 一些API
* 判断API

  equals()                     比较内容是否相等，区分大小写。

  equalsIgnoreCase() 比较内容是否相等，不区分大小写。

  contains ()                 判断字符串中是否包含指定的字符串 

  endsWith()                 判断字符串是否以指定字符结尾

​        isEmpty()                   判断字符串是否为空，如果为空返回true

* 输入

  Scanner sc = new Scanner(System.in);

  String username = sc.nextLine();

* 获取API

  ​int length()  获取字符串长度

  ​char charAt(int index) 获取字符串在指定索引出的字符,可用来遍历字符串

  ​int indexOf(int ch) 获取ch这个字符在该字符串中第一次出项的索引

  ​int indexOf(String str) 获取str 这个字符串在该字符串中第一次出现的索引

  ​int indexOf(int ch,int fromIndex) 获取ch这个字符在该字符串中从自定索引开始后第一次出现的索引。

  ​iint indexOf(String str,int fromIndex) 获取str这个字符在该字符串中从自定索引开始后第一次出现的索引。

  ​String substring(int start)  获取字串，截取，从start到末尾

  ​String substring(int start,int end) 获取字串，截取，从start到end

* 遍历字符串 

  区分大小写和数字 ：  s>='0' && s < ='9' 

  ​				      s>='a' && s<='z'

  ​				      s>='A' && s<='z'


* 字符串的转换API

  byte[] getBytes()  字符串转换成字节数组。

  char[] toCharArray() 字符串转换成字符数组

  String copyValueOf(char[] chs)  字符数组转换成字符串

  String valueOf (char[] chs)任意类型转换成字符串

  String valueOf(int i) int类型的数据转换成字符串

  String toLowerCase():字符串转成小写

  String toUpperCase(); 字符串转成大写

  String concat(String str);字符串的拼接，相当于 + 


* 链式编程 对象调方法还是对象，可以继续调方法

```
String result = line.substring(0,1).toUpperCase().concat(line.substring(1).toLowerCase());
```

* 替换API(替换所有)

  String replace(char old,char new)

  String replace(String old, char new)


* 去掉字符串两端的空格（中间不会）

  String trim()  //例如输入名称时，会不小心输入空格


* 比较两个字符串（依次比较，字符相减，所以相同的字符串函数值为零）

  ​int compareTo(String str)

  ​int compareToIgnoreCase(String str) //忽略大小写

## Java map和list
在学Java以前，一说到存放东西，第一个想到的就是使用数组，使用数组，在数据的存取方面的却也挺方便，其存储效率高访问快，但是它也受到了一些限制，比如说数组的长度以及数组的类型，当我需要一组string类型数据的同时还需要Integer类型的话，就需要定义两次，同时，数组长度也受到限制，即使是动态定义数组长度，但是长度依然需要固定在某一个范围内，不方便也不灵活。
       如果说我想要消除上面的这个限制和不方便应该怎么办呢？Java是否提供了相应的解决方法。答案是肯定的，这就是Java容器，java容器是javaAPI所提供的一系列类的实例，用于在程序中存放对象，主要位于Java.util包中，其长度不受限制，类型不受限制，你在存放String类的时候依然能够存放Integer类，两者不会冲突。

容器API类图结果如下所示：
 ![](http://img.blog.csdn.net/20140411154642250?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZGFuZGFuem1j/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

<hr>
### Collection接口
    Collection是最基本的集合接口，一个Collection代表一组Object，即Collection的元素。一些Collection允许相同的元素而另一些不行。一些能排序而另一些不行。Java SDK不提供直接继承自Collection的类，Java SDK提供的类都是继承自Collection的“子接口”如List和Set。

举例：

    import java.util.*;
    public class TestA{
    	public static void main(String[] args)
    	{
    		Collection<String> lstcoll=new ArrayList<String>();
      	lstcoll.add("China");
      	lstcoll.add(new String("ZD"));
      	
     		System.out.println("size="+lstcoll.size());
        System.out.println(lstcoll);
    	}
    }

结果：
size=2
[China, ZD]

#### List接口

      List是有序的Collection，使用此接口能够精确的控制每个元素插入的位置。用户能够使用索引（元素在List中的位置，类似于数组下标）来访问List中的元素，也就是说它是有顺序的，类似于Java的数组。和Set不同，List允许有相同的元素。J2SDK所提供的List容器类有ArrayList、LinkedList等。

实例：

    import java.util.*;
    public class TestB{
    
    public static void main(String[] args)
    {
    	List<String> l1=new LinkedList<String>();
    	for(int i=0;i<=5;i++){
    		l1.add("a"+i);
    	}
    	System.out.println(l1);
    	l1.add(3,"a100");
    	System.out.println(l1);
    	l1.set(6,"a200");
    	System.out.println(l1);
    	System.out.println((String)l1.get(2)+" ");
    	l1.remove(1);
    	System.out.println(l1);
    }
    }


运行结果：

#### **ArrayList**

     ArrayList其实就相当于顺式存储，它包装了一个数组 Object[]，当实例化一个ArrayList时，一个数组也被实例化，当向ArrayList中添加对象时，数组的大小也相应的改变。这样就带来以下有特点：  

       快速随即访问，你可以随即访问每个元素而不用考虑性能问题，通过调用get(i)方法来访问下标为i的数组元素。  

       向其中添加对象速度慢，当你创建数组时并不能确定其容量，所以当改变这个数组时就必须在内存中做很多事情。  

       操作其中对象的速度慢，当你要向数组中任意两个元素中间添加对象时，数组需要移动所有后面的对象。  



#### **LinkedList**

        LinkedList相当于链式存储，它是通过节点直接彼此连接来实现的。每一个节点都包含前一个节点的引用，后一个节点的引用和节点存储的值。当一个新节点插入时，只需要修改其中保持先后关系的节点的引用即可，当删除记录时也一样。这样就带来以下有特点：  

       操作其中对象的速度快，只需要改变连接，新的节点可以在内存中的任何地方。  

       不能随即访问，虽然存在get()方法，但是这个方法是通过遍历接点来定位的，所以速度慢。

Set接口

      Set是一种不包含重复的元素的Collection，即任意的两个元素e1和e2都有e1.equals(e2)=false，Set最多有一个null元素。  

      Set的构造函数有一个约束条件，传入的Collection参数不能包含重复的元素。  



  Set容器类主要有HashSet和TreeSet等。

HashSet

       此类实现 Set 接口，由哈希表（实际上是一个 HashMap 实例）支持。它不保证 set 的迭代顺序；特别是它不保证该顺序恒久不变。此类允许使用 null 元素。

举例：  

    import java.util.*;

    public class TestC{

    public static void main(String[] args)
    {
    	Set <String> s=new HashSet<String>();
    	s.add("Hello");
    
    //相同元素
    	s.add("Hello");
    
    	System.out.println(s);
    }
    }



结果：
[hello]

### Map接口

      值得注意的是Map没有继承Collection接口，Map接口是提供key到value的映射。一个Map中不能包含相同的key，每个key只能映射一个value。即是一一映射，Map接口提供3种集合的视图，Map的内容可以被当作一组key集合，一组value集合，或者一组key-value映射。  
      Map接口的实现类主要是包括HashMap和TreeMap等。
HashMap（线程不安全）、Hashtable（线程安全），所以不考虑同步问题的时候HashMap性能好些
       Hashtable不允许null，HashMap key-value 均允许null的存在
#### **HaspMap**

* 添加数据使用put(key, value)，取出数据使用get(key)
* HashMap是允许null，即null value和null key。
* Map里的key类似一个Set，甚至可以通过map.keySet()拿到key的Set集合(下面遍历第一个例子就是)。
* Map里的value类似一个List，只不过索引不再是数字，而是任意类型。
* 但是将HashMap视为Collection时（values()方法可返回Collection），其迭代子操作时间开销和HashMap的容量成比例。因此，如果迭代操作的性能相当重要的话，不要将HashMap的初始化容量设得过高，或者load factor过低。

举例：

    import java.util.*;
    public class TestD{
    public static void main(String[] args)
    {
        Map <String,String> M=new HashMap <String,String>();
        M.put("one",new String("1"));
        M.put("two",new String("2"));
        System.out.println(M);
    }
    }


结果：
{one=1, two=2}


### 选择

          Java容器实际上只有三种:Map , List, Set;但每种接口都有不同的实现版本.它们的区别可以归纳为由什么在背后支持它们.也就是说,你使用的接口是由什么样的数据结构实现的.  

List的选择:  

         比如:ArrayList和LinkedList都实现了List接口.因此无论选择哪一个,基本操作都一样.但ArrayList是由数组提供底层支持.而LinkedList是由双向链表实现的.所以,如果要经常向List里插入或删除数据,LinkedList会比较好.否则应该用速度更快的ArrayList。  

Set的选择  

         HashSet总是比TreeSet 性能要好.而后者存在的理由就是它可以维持元素的排序状态.所以,如果需要一个排好序的Set时,才应该用TreeSet。  

Map选择:         同上,尽量选择HashMap。  
<hr>
### Iterator接口
在Java中Iterator为一个接口，它只提供了迭代了基本规则，在JDK中他是这样定义的：对 **collection** 进行迭代的迭代器。
注意：HashMap不支持Iterator所以要通过其他的方式迭代Map中的key和value。
接口定义如下：
```
public interface Iterator {　　boolean hasNext();　　Object next();　　void remove();}
```
* boolean hasNext()：判断容器内是否还有可供访问的元素.
* Object next()：返回迭代器刚越过的元素的引用，返回值是Object，需要强制转换成自己需要的类型.
* void remove()：删除迭代器刚越过的元素

**迭代**：迭代其实我们可以简单地理解为遍历，是一个标准化遍历各类容器里面的所有对象的方法类，它是一个很典型的设计模式。Iterator模式是用于遍历集合类的标准访问方法。它可以把访问逻辑从不同类型的集合类中抽象出来，从而避免向客户端暴露集合的内部结构
<hr>
### 遍历map和set
#### Java遍历Map
**entry对象**：HashMap在存储过程中并没有将key，value分开来存储，而是当做一个整体key-value来处理的，这个整体就是Entry对象。同时value也只相当于key的附属而已。在存储的过程中，系统根据key的hashcode来决定Entry在table数组中的存储位置，在取的过程中同样根据key的hashcode取出相对应的Entry对象。
对于一个entry，可以getKey()和getValue()来得到键和值。
```
对于Map接口而言，JDK源码中将其分为三种视图，其实就是三种以某种集合存储值的表现形式。分别为Set<K> :用以存储Map的key；Collection<K> 用以存储Map的value;而Set<Map.Entry<K,V>>是存储key-value对(键-值对)。Set视图就是使用Set集合存储的View,Set集合特点就是不可重复。
```
```
public static void main(String[] args) {

  Map<String, String> map = new HashMap<String, String>();
  map.put("1", "value1");
  map.put("2", "value2");
  map.put("3", "value3");
  
  //第一种：普遍使用，二次取值
  //通过map.keySet()拿到key的Set集合
  System.out.println("通过Map.keySet遍历key和value：");
  for (String key : map.keySet()) {
   System.out.println("key= "+ key + " and value= " + map.get(key));
  }
  
  //第二种
  System.out.println("通过Map.entrySet使用iterator遍历key和value：");
  Iterator<Map.Entry<String, String>> it = map.entrySet().iterator();
  while (it.hasNext()) {
   Map.Entry<String, String> entry = it.next();
   System.out.println("key= " + entry.getKey() + " and value= " + entry.getValue());
  }
  
  //第三种：推荐，尤其是容量大时
  System.out.println("通过Map.entrySet遍历key和value");
  for (Map.Entry<String, String> entry : map.entrySet()) {
   System.out.println("key= " + entry.getKey() + " and value= " + entry.getValue());
  }

  //第四种 values()方法可返回Collection
  System.out.println("通过Map.values()遍历所有的value，但不能遍历key");
  for (String v : map.values()) {
   System.out.println("value= " + v);
  }
 }
```

#### Java遍历Set

对 set 的遍历  
1.迭代遍历：  
```
Set<String> set = new HashSet<String>();  
Iterator<String> it = set.iterator();  
while (it.hasNext()) {  
  String str = it.next();  
  System.out.println(str);  
}  
```
2.for循环遍历：  
```
for (String str : set) {  
      System.out.println(str);  
}  

优点还体现在泛型 假如 set中存放的是Object  
  
Set<Object> set = new HashSet<Object>();  
for循环遍历：  
for (Object obj: set) {  
      if(obj instanceof Integer){  
                int aa= (Integer)obj;  
             }else if(obj instanceof String){  
               String aa = (String)obj  
             }  
              ........  
}  
```
## Java的异常分类

### 基本概念

Throwable:
　　　|--Error 
　　　|--Exception 
　　　　　　|编译期异常　在编译期间就会有提示，必须解决（try catch 解决，就会没有提示，或者抛出）
　　　　　　|运行期异常 RuntimeExecption 代码逻辑问题

另：

* RuntimeException及其子类是运行时的异常，其他都是编译期的异常。
* Throwable 是所有异常的根，java.lang.Throwable
* Error 是错误 ，Exception是异常

<br/>

### Exception
一般分为Checked异常和Runtime异常，所有RuntimeException类及其子类的实例被称为Runtime异常，不属于该范畴的异常则被称为CheckedException。

#### Checked异常

只有java语言提供了Checked异常，Java认为Checked异常都是可以被处理的异常，所以Java程序必须显示处理Checked异常。如果程序没有处理Checked异常，该程序在编译时就会发生错误无法编译。这体现了Java的设计哲学：没有完善错误处理的代码根本没有机会被执行。对Checked异常处理方法有两种

1.当前方法知道如何处理该异常，则用try...catch块来处理该异常。

2.当前方法不知道如何处理，则在定义该方法是声明抛出该异常。

我们比较熟悉的Checked异常有

Java.lang.ClassNotFoundException

Java.lang.NoSuchMetodException

java.io.IOException

RuntimeException

Runtime如除数是0和数组下标越界等，其产生频繁，处理麻烦，若显示申明或者捕获将会对程序的可读性和运行效率影响很大。所以由系统自动检测并将它们交给缺省的异常处理程序。当然如果你有处理要求也可以显示捕获它们。

我们比较熟悉的RumtimeException类的子类有

Java.lang.ArithmeticException

Java.lang.ArrayStoreExcetpion

Java.lang.ClassCastException

Java.lang.IndexOutOfBoundsException

Java.lang.NullPointerException
### Error

当程序发生不可控的错误时，通常做法是通知用户并中止程序的执行。与异常不同的是Error及其子类的对象不应被抛出。

Error是throwable的子类，代表编译时间和系统错误，用于指示合理的应用程序不应该试图捕获的严重问题。 
例如内存溢出，不是我们程序应该考录的。

Error由Java虚拟机生成并抛出，包括动态链接失败，虚拟机错误等。程序对其不做处理。

### 处理方法
* try{}
  catch{}
  catch{}
  第一个catch捕获成功 其catch将不再进行，但是如果有Exception这样的父类，要放在最后。
* catch(异常一|异常二|异常三  e) JDK7新特性，但是提示不会提示特别明确
  注意这些异常必须是平级关系。
* e.getMessage(); 返回字符串消息。
* e.toString(); 返回异常的描述。
* e.printStackTrace(); 把异常的信息输出到控制台,这个现在是我们最常用的。
* 抛出异常 throws + 类名 是告诉你调用方法的时候要注意问题。
   throw是抛出实际的异常。如果异常是编译异常，调用方法加 throws加类名，如果是继承RuntimeException的异常，不用，直接抛出 

        throw new MyExecption("这个是我自己定义的异常");
        public class MyExecpiton extends RuntimeExecption{
        public MyExecption(Stirng message)
        super(message);
        }

## java中的反射

### 什么是反射
通过一个class 文件对象来使用该class文件中的成员。
class文件对象： 我们写了一个student.java文件，还有一个Techer.java，应该有这样的内容被加到内存：student.class,techer.class。把多个class文件用一个类来表述，这个类就是Class类
如何获取class对象？

* Object中的getClass(),同一类的class 文件只有一个。
    person p1 = new person();
    person p2 = new person();
    Class c1 = p1.getCass();
    Class c2 = p2.getCass();
    System.out.println(c == c2):
* 通过对数据类型的一个静态的class属性
    `Class c3 = Person.class;`
* 通过Class类的一个静态方法forName(); 开发中最常用，可动态改变，通过配置文件。
    Class c4 = Class.forName("com.test.person").//一定要加上包名
```java
Class c = Class.forname("com.test.person");
Object obj = c.newInstance(); //这里会掉用person的无参构造函数，如果没有将出错。
```
### 配置文件
.properties的后缀是配置文件
 先新建一个classes.properties配置文件

推荐文章http://www.tuicool.com/articles/fIVjQfU



## 对象序列化

具有表现多中形态的能能力和特征，多个实例实现不同的类
 不同的对象对同一行为做出不同的相应

条件：

```
1， 要有继承或者接口
2， 要有重写
3， 父类的引用指向子类的条件。
```

### 作用：

把对象的状态写入一个字节流中，

1. 内厝对象保存到文件中。
2. socket 在网络上传送该对象
3. 通过RMI船速

### 如何实现序列化？

实现一个接口 Serializable，引入java.io.Serializable 这个接口没有任何方法。可以将这个接口理解为一个标签。

### 序列ID

唯一标识对象，两种，一种固定1L，一种随机 long 型 不重复的，使用IDE生成,编译器会提示
默认使用第一种，
private statci final long serialVersionUID = 1L;
介绍关键字 transient 在网络传输时不会将ID传出，会传出一个这个类型的默认值，0。不会被序列化。  

### 其他

- 序列化会忽略静态类型，因为它是类的状态。序列化只序列对象的序列。
- 当父类实现序列化时，子类不用显式写实现接口（implement Serializable），自动实现序列化
- 对象的实例变量引用其他对象，其他对象也会被序列化。



## java中的多线程

### 写在前面

java是不能直接操作os的，它封装了c/c++的代码，来为我们实现多线程。jvm支持并发（同时地）执行多个线程。
开启多个线程本质上是为了提高CPU的使用率

### 创建新线程的方式
创建新线程有两种方式：

* 将类声明为Thread的子类，子类重写run()方法，因为run方法里面封装的代码此时可以被线程执行的。创建自定义类的对象，启动线程并使用。
* 实现Runnable的接口

### Thtread类的使用
这里我们先只说Thread类的使用,它在java.lang.包下，我们无需导入。

```java
public class MyThread extends Thread{
@Override
    publiv void run(){
        for(int i = 0; i<1000; i++){
        System.out.println(i);
        }
    }
}
public class MyDemo {
public static vod main(String[] args){
  MyThread mt = new MyThread();
  //这样不是多线程，因为只用一个线程对象。
  mt.run();
  mt.run();
  
  MyThread mt1 = new MyThread();
  //这样也不是多线程
  mt.run();
  mt1.run();
  //下面才能执行多线程
  mt.start();
  mt1.start();
}
}
```
**run()和start()的区别**
run(): 只是执行了被封装的线程方法。
start()： 让线程启动，并由jvm调用run()方法。（这句话好好理解）

getName()和setName()方法,获取名字和设置名字：
  MyThread mt1 = new MyThread(”线程一“);
  这里MyThread里需要带参构造 ：
  public void MyThread(String name){
  super(name);

### 第二种方式，实现Runnable
自定义类MyRunnable实现Runnable接口
重写run()方法。
创建自定义类的对象
创建Thread类对象，把MyRunnable类的对象作为构造参数传递

```java
public class MyRunnable implement Runnable{
for (int i = 0; i<100; i++){
System.out.println(i);
} 
}

public class MyDemo {
public static vod main(String[] args){
MyRunnable mr = new MyRunnable;
Thread t = new Thread(mr);
Thread t1 = new Thread(mr);
}
```

获得名字：
Thread.currentThread().getName();
设置名字：
Thread t = new Thread(mr,"111");
Thread t1 = new Thread(mr,"222");

**为什么有了第一种方式还要有第二种方式**
因为类只能单继承，一个子类想要实现多线程，此时只能实现接口的那种方式。

### 内存资源占用问题
每个run方法都有自己的栈区，而堆和静态区是共享的，如果有共享资源一定要放到静态区。加静态的声明周期过长，还有一种办法可以通过第二种方式实现，

```java
public class Ticket implement Runnable{
  private  int  ticketNum = 100;
  @Override
  public void Run(){
  for(int i = 1; i<=100; i++){
  System.out.println(Thread.currentThread.getName()+"售出了第"+i+"张票")
  }
  }
}

public class MyDemo {
public static vod main(String[] args){
MyRunnable mr = new MyRunnable;
Thread t = new Thread(mr,"窗口1");
Thread t1 = new Thread(mr,"窗口2");
t.start();
t1.start();
}

```
这样就可以让票数共享，而没有设置静态
但是我把延时，把run函数改成这样：
```java
private int ticket = 100;
public void Run(){
    while(true){
        if(ticket>0){
            try{
                 Thread.sleep(10);
                }catch(InterrupedException e){
            e.printStackTrace();}
            }
            System.out.println(Thread.currentThread().getName()+"正在出售第" + "(ticket--)+"张票");
        }
  }
```
这是就会出现原子操作的问题，什么是原子操作，我们把cpu每一次进行的操作称为原子操作，ticket-- 分为两个原子操作，第一步先 ticket-1 ，第二步 ticket = ticket -1.在第一步和第二部中间，经过sleep（10）唤醒的线程会使用第一步操作的值，而引起ticket票数的重复。比如 int a = 10; 也是两个原子操作

### 同步操作
格式：
synchronized(对象) {
需要被同步的代码
}

```java
private int ticket = 100;
private Object obj = new Object();
public void Run(){
    while(true){
    synchronized(obj){  
        if(ticket>0){
            try{
                 Thread.sleep(10);
                }catch(InterrupedException e){
            e.printStackTrace();}
            System.out.println(Thread.currentThread().getName()+"正在出售第" + "(ticket--)+"张票");
            }
            }
        }
  }
```
当一个线程进来时，synchronized将obj设置为锁的状态，其他线程进不来，当这个线程出去时，将锁的状态改为开。
**同步方法**
将synchronized关键字放到方法的签名
```java
public synchronized void show(){
        if(ticket>0){
            try{
                 Thread.sleep(10);
                }catch(InterrupedException e){
            e.printStackTrace();}
            System.out.println(Thread.currentThread().getName()+"正在出售第" + "(ticket--)+"张票");
            }
}
```

这个方法等价于 synchronized(this)

### JDK5的新特性
上面的同步方式是比较常见的方式，但是我们总要考虑他的锁对象，现有一种新方式：lock锁对象。
```java
private Lock lock = new ReentranLock(); //定义在方法外

//run 内
lock.lock();
 if(ticket>0){
            try{
                 Thread.sleep(10);
                }catch(InterrupedException e){
            e.printStackTrace();}
            System.out.println(Thread.currentThread().getName()+"正在出售第" + "(ticket--)+"张票");
lock.unlock();
```
### 等待和唤醒 
notify 和 wait



## java的单例模式

类在内存中的对象只有一个
举例:打印机 网站计数器
</br>
如何实现单例模式：

1. 让外界不能去创建对象，但是不能不给构造函数、
2. 把构造函数私有
3. 类本身要创建一个对象，但是这个对象是私有和静态的
4. 对外提供一个方法，获取该类的对象

```java
public class Student{
    private Student(){} //私有的构造函数，为了不让外界去创建对象
    private static Student s = new Student(); //静态只能访问静态，所以设置为静态，private是不让外界直接调用，比如 Student.s；
    public static student getStudent(){ //对外界提供获取对象的方法
        return s;     
    }
}
```

分类： 

* 饿汉式
  进来就创建对象，如上。开发中会用，比如JDK中有个Runtime就是饿汉式

```java
public class RuntimeDemo{
public static void main(String[] args){
Runtime r = Runtime.getRuntime;
    try{
    //path路径中配置过的文件、
        r.exec("notepad");
    }catch(IOException e){
        e.printStackTrace();
    }
}
}
```

* 懒汉式
  调用的时候才创建对象，静态方法是程序开始就存在的，但是存在并不等于执行。

```java
public class Techer{
private Teacher(){}
private static Teacher t = null;
public Techer getTecher(){
if(t == null){
t = new Teacher();
}
return t;
}

```
但是懒汉式会有线程安全问题，比如几个线程进来都是执行到if（t = null）时 会有四个线程进入当中，所以应该加个关键字synchronized,这个面试中会问
还有问题就是用的时候才加载，会有延迟加载思想。



## java面试题整理

### 线程
* 创建线程有几种不同的方式？你喜欢哪一种？为什么？

有三种方式可以用来创建线程：

继承Thread类

实现Runnable接口

应用程序可以使用Executor框架来创建线程池

实现Runnable接口这种方式更受欢迎，因为这不需要继承Thread类。在应用设计中已经继承了别的对象的情况下，这需要多继承（而Java不支持多继承），只能实现接口。同时，线程池也是非常高效的，很容易实现和使用。

* 概括的解释下线程的几种可用状态。

线程在执行过程中，可以处于下面几种状态：

就绪(Runnable):线程准备运行，不一定立马就能开始执行。

运行中(Running)：进程正在执行线程的代码。

等待中(Waiting):线程处于阻塞的状态，等待外部的处理结束。

睡眠中(Sleeping)：线程被强制睡眠。

I/O阻塞(Blocked on I/O)：等待I/O操作完成。

同步阻塞(Blocked on Synchronization)：等待获取锁。

死亡(Dead)：线程完成了执行。

* 同步方法和同步代码块的区别是什么？

在Java语言中，每一个对象有一把锁。线程可以使用synchronized关键字来获取对象上的锁。synchronized关键字可应用在方法级别(粗粒度锁)或者是代码块级别(细粒度锁)。

* 在监视器(Monitor)内部，是如何做线程同步的？程序应该做哪种级别的同步？

监视器和锁在Java虚拟机中是一块使用的。监视器监视一块同步代码块，确保一次只有一个线程执行同步代码块。每一个监视器都和一个对象引用相关联。线程在获取锁之前不允许执行同步代码。

* 什么是死锁(deadlock)？

两个进程都在等待对方执行完毕才能继续往下执行的时候就发生了死锁。结果就是两个进程都陷入了无限的等待中。

* 如何确保N个线程可以访问N个资源同时又不导致死锁？

使用多线程的时候，一种非常简单的避免死锁的方式就是：指定获取锁的顺序，并强制线程按照指定的顺序获取锁。因此，如果所有的线程都是以同样的顺序加锁和释放锁，就不会出现死锁了。


### java基础类型和占位字节
* long: 8 
* double: 8
* int:  4
* float:4
* short:2
* char: 2
* byte::1 
* boolean: 4 或 1bit
  `boolean a = true(4字节) `
  `boolean[] a = new boolean[10],每一位为1bit`

