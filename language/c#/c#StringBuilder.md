---
title: c#StringBuiler
date: 2016-04-30 16:39:40
categories: c#
tags: [c#,string]
---

### 写在前面

　　String 对象是不可改变的。每次使用 System.String 类中的方法之一时，都要在内存中创建一个新的字符串对象，这就需要为该新对象分配新的空间。在需要对字符串执行重复修改的情况下，与创建新的 String 对象相关的系统开销可能会非常昂贵。如果要修改字符串而不创建新的对象，则可以使用 System.Text.StringBuilder 类。例如，当在一个循环中将许多字符串连接在一起时，使用 StringBuilder 类可以提升性能。
通过用一个重载的构造函数方法初始化变量，可以创建 StringBuilder 类的新实例，正如以下示例中所阐释的那样。
`StringBuilder MyStringBuilder = new StringBuilder("Hello World!");`

<!-- more -->

### 设置容量和长度

　　虽然 StringBuilder对象是动态对象，允许扩充它所封装的字符串中字符的数量，但是您可以为它可容纳的最大字符数指定一个值。此值称为该对象的容量，不应将它与当前 StringBuilder 对象容纳的字符串长度混淆在一起。例如，可以创建 StringBuilder 类的带有字符串“Hello”（长度为 5）的一个新实例，同时可以指定该对象的最大容量为 25。当修改 StringBuilder 时，在达到容量之前，它不会为其自己重新分配空间。当达到容量时，将自动分配新的空间且容量**翻倍**。可以使用重载的构造函数之一来指定 StringBuilder 类的容量。以下代码示例指定可以将 MyStringBuilder 对象扩充到最大 25 个空白。
`StringBuilder MyStringBuilder = new StringBuilder("Hello World!", 25);`
另外，可以使用读/写 Capacity 属性来设置对象的最大长度。以下代码示例使用 Capacity 属性来定义对象的最大长度。
MyStringBuilder.Capacity = 25;

### 下面列出了此类的几个常用方法：
* Append 方法可用来将文本或对象的字符串表示形式添加到由当前 StringBuilder 对象表示的字符串的结尾处。以下示例将一个 StringBuilder 对象初始化为“Hello World”，然后将一些文本追加到该对象的结尾处。将根据需要自动分配空间。

        StringBuilder MyStringBuilder = new StringBuilder("Hello World!");
        MyStringBuilder.Append(" What a beautiful day.");
        Console.WriteLine(MyStringBuilder);
  此示例将 Hello World! What a beautiful day. 显示到控制台。
* AppendFormat 方法将文本添加到 StringBuilder 的结尾处，而且实现了 IFormattable 接口，因此可接受格式化部分中描述的标准格式字符串。可以使用此方法来自定义变量的格式并将这些值追加到 StringBuilder 的后面。以下示例使用 AppendFormat 方法将一个设置为货币值格式的整数值放置到 StringBuilder 的结尾。

        int MyInt = 25; 
        StringBuilder MyStringBuilder = new StringBuilder("Your total is ");
        MyStringBuilder.AppendFormat("{0:C} ", MyInt);
        Console.WriteLine(MyStringBuilder);
  此示例将 Your total is $25.00 显示到控制台。
* Insert 方法将字符串或对象添加到当前 StringBuilder 中的指定位置。以下示例使用此方法将一个单词插入到 StringBuilder 的第六个位置。

        StringBuilder MyStringBuilder = new StringBuilder("Hello World!");
        MyStringBuilder.Insert(6,"Beautiful ");
        Console.WriteLine(MyStringBuilder);
  此示例将 Hello Beautiful World! 显示到控制台。
* 可以使用 Remove 方法从当前 StringBuilder 中移除指定数量的字符，移除过程从指定的从零开始的索引处开始。以下示例使用 Remove 方法缩短 StringBuilder。

        StringBuilder MyStringBuilder = new StringBuilder("Hello World!");
        MyStringBuilder.Remove(5,7);
        Console.WriteLine(MyStringBuilder);
  此示例将 Hello 显示到控制台。
* 使用 Replace 方法，可以用另一个指定的字符来替换 StringBuilder 对象内的字符。以下示例使用 Replace 方法来搜索 StringBuilder 对象，查找所有的感叹号字符 (!)，并用问号字符 (?) 来替换它们。

        StringBuilder MyStringBuilder = new StringBuilder("Hello World!");
        MyStringBuilder.Replace('!', '?');
        Console.WriteLine(MyStringBuilder);
  此示例将 Hello World? 显示到控制台