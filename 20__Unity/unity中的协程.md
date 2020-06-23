
---
title: "unity中的协程.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "unity中的协程.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["unity"]
author: "Claymore"

---
Tags:[Unity]  date: 2016-06-10 

### 协程
协程并非真正的多线程。协程其实是等某个操作完成之后再执行后面的代码，或者说是控制代码在特定的时机执行。协程只是部分执行，并假定在适当的条件得到满足，在未来的某一时刻将被恢复，直到它的工作完成。
或者说，协同程序，在主程序运时开启另一段逻辑处理，协同当前程序的执行。而多线程在Unity渲染和复杂逻辑运算时可以高效的使用多核CPU，帮助程序可以更高效的运行。

先看一个示例，点击按钮让cube旋转30°，过三秒后再旋转30°
![](http://ojynuthay.bkt.clouddn.com/unity%E5%8D%8F%E7%A8%8B.png)
代码：

<!-- more -->    

        using UnityEngine;
        using System.Collections;
        
        public class IEnumeratorTest : MonoBehaviour {
            public void BtnClick()
            {
                StartCoroutine(Test());
            }
        
            IEnumerator Test()
            {
                this.transform.Rotate(Vector3.up * 30);
                yield return new WaitForSeconds(3); //等待三秒
                this.transform.Rotate(Vector3.forward * 30);
            }
        }

* 协程不会阻塞主线程
* 协程在游戏中用于AI，降低它的资源利用，不让它总是每帧检测，而是像上面等几秒检测一次。


### 调用函数
调用函数是协程的简化写法，分为：

* Invoke 调用函数： 隔多长时间执行**一次**某方法。

        public void Invoke(string methodName,float time);

* InvokeRepeating 重复调用函数： 指定时间、指定间隔时间重复调用。

        public void InvokeRepeating(string methodName, float time, float repeatRate)
    eg:

    	void Start () {
		
    	    Invoke("test", 5f);   //5秒后调用一次text
		
    	    InvokeRepeating("test1", 1f, 1f);  //重复调用，1s时开始，1s间隔重复调用。
    	}
    	
    	void test()
    	{
    	    Debug.Log("this is test");
    	}
    	
    	void test1()
    	{
    	    Debug.Log("this is test1");
    	}

### 协程和调用函数的区别

* 调用函数是协程的简化写法。
* 调用函数语法简单，但是不灵活，协程注重“非固定时间间隔”。

---

### 多线程
Unity3D编程时，总有个主线程执行你的代码，也可以创建额外的线程和主线程同时运行。而Unity中，你仅能从主线程中访问Unity3D的组件，对象和Unity3D系统调用。任何企图访问这些项目的第二个线程都将失败并引发错误，这是一个要重视的一个限制。

先记住一句结论：
 **分线程可以做 基本类型的计算， 以及非Unity(包括.Net及SDK)的API** 
使用多线程注意：

* 变量都是共享的(都能指向相同的内存地址)
* UnityEngine的API不能在分线程运行
* UnityEngine定义的基本结构(int,float,Struct定义的数据类型)可以在分线程计算，如 Vector3(Struct)可以 ， 但Texture2d(class,根父类为Object)不可以。
* UnityEngine定义的基本类型的函数可以在分线程运行
* tread类等多线程一般不用于unity里，它会和 unity的api起冲突，一般socket类用多线程。

---

### Loom
Unity的函数执行机制是帧序列调用，甚至连Unity的协程Coroutine的执行机制都是确定的，如果可以使用多线程访问UnityEngine的对象和api就得考虑同步问题了，也就是说Unity其实根本没有多线程的机制，协程只是达到一个延时或者是当指定条件满足是才继续执行的机制。这时我们发现了Loom.
我们只需要关系两个函数：RunAsync(Action)和QueueOnMainThread(Action, [optional] float time) 就可以轻松实现一个函数的两段代码在C#线程和Unity的主线程中交叉运行。原理也很简单：用线程池去运行RunAsync(Action)的函数，在Update中运行QueueOnMainThread(Acition, [optional] float time)传入的函数。
更多请看，[点击这里](http://blog.csdn.net/sgnyyy/article/details/41779451)