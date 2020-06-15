
---
title: "Unity_性能分析工具_Profiler_及项目优化.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Unity]  date: 2016-06-15

Profiler是一个辅助优化游戏性能的工具，在游戏运行时实时详细报告游戏各个部分每帧所耗费的时间。如图像渲染部分、动画系统或者脚本各耗费多少时间。
Window ->Profiler

### 界面
功能分为5个部分检测：

* CPU usage 中央处理器使用率
* Rendering 渲染
* Memory    内存
* Audio     音频
* Physics   物理

![](http://claymore.wang:5000/uploads/big/d712c48c62c1100b52ef1f9f196baa6e.png)

<!-- more -->

所有栏中波形图都是在最右侧最新的时间占用并向左移动
下方的Overview显式的是脚本各占用了多少时间。
看那条竖线，上面的数值可以找到相关栏目里的相关颜色，颜色代表在栏目左侧有说明。

### 连接设备
android为例，先打开Buid Settings 窗口，勾选Development Buid，再勾选Autoconnected Profiler，build 将打出的apk安装到设备，确保同一网络环境（wifi）下。
在手机上查看wifi的ip地址，在profiler窗口点击Active Profile按钮，下拉菜单中点击“enter Player IP ” 输入ip，connect。

### CPU优化
我们选中CPU Usage栏，可以看到有66ms(15fps),33ms(30fps),16ms(60fps)3条横向基准线，当波形位于线上就是该基准线的数值。 33ms代表这一帧CPU计算占用了33ms的时间，1s是1000ms,1000/33 = 30,也就是说30 fps 为30帧/秒。

### 预定义标签
预定义标签Script Dfine symbols,编译器会在编译的时候根据预定义标签来生成对应的二进制编码。
Edit -> Project -> Project Settings -> Player，在Inspector中找到 Script Define Symbols，在其中输入Test并回车。
新建项目，新建空物体，附加脚本：

    using UnityEngine;
    using System.Collections;
    using System.Collections.Generic;
    
    public class CodeExample : MonoBehaviour
    {
        public List<string> playerNames;
        void OnGUI()
        {
    #if Test
            if (GUILayout.Button("Print play name"))
            {
                for (int i = 0; i < playerNames.Count; i++)
                {
                    Debug.Log("player:" + playerNames[i]);
                }
            }
    #endif        
        }
    }
当Player Settings的Script Define Symbols 栏中存在定义标签 Test时， #if Test 和 #endif块中的代码才会被编译执行，不存在将变为灰色，不会被编译执行。

我们可以测试的时候保留标签，发布的时候去掉。
不光测试，对于不同版本或不同平台我们可以选择相应的保留相应代码：

    void DoSomething{
    #if Channel_1
        ...
    #if Channel_2
        ...
    #endif 
    }


### 渲染优化
渲染主要和显卡GPU有关，如果在Profiler的CPU栏下显式Gfx.WaitForPresent 那么表示GPU每帧渲染需要时间过长，CPU需要等待GPU.
和渲染重要的几个参数可以在Game窗口下查看，Game中点击“stats”：
![](http://claymore.wang:5000/uploads/big/f4d1d5b0b75ad2fca022f3883031e3d7.png)

* Trs: Trangle,三角形的数量，渲染的基础指标。图中为1.7k，也就是当前画面共渲染了17000个三角形。
* Verts: Vertices,模型定点的数量，渲染的基础指标。5.0k,也就是当前画面一共渲染了5000个顶点。
* SetPass calls: SetPass调用次数。
* Batches： 合并后的Drawcall次数。
* Save by batching： 被合并的Drawcall次数。
* shadow casters： 阴影投射图的数量。

**优化**

*   材质优化
    * 尽量小的可接受的贴图尺寸，通过代码操作材质的时候，尽量使用renderer.shardMaterial 或者 renderer.sharedMaterials. 而不用render.material 或者 render.materials,因为后两者每一次改动都会创建一个新的材质。
    * 少用Standard Shader，参数多，运算也多。
    * 一般可以不接受光照的物体就用不参与光照的shader，Unlit栏里的都是。
    * 对于不涉及颜色变化的物体，尽量使用没有颜色参数的Shader。

*   光照优化
    ​      尽量使用烘培好的lightmap。如果是移动开发平台，控制光的数量谨慎使用实时阴影。

*   **Draw Call合并**
    *   先说下Draw Call的概念
        unity（或者基本所有图形引擎）生成一帧的过程大致：引擎简单的可见性预测，确定摄像机看到的物体，把这些顶点、位置、索引等等等（很多）数据准备好通知图形API-或者简单看为GPU-开始绘制，GPU基于这些数据画出成千上万的三角形，最终构成一幅图像，在unity中，将引擎准备数据并通知GPU过程称为一次DrawCall,它是逐个物体进行的，每帧的DrawCall是非常重要的指标。
    *   Unity内置了DrawCall合并技术（Draw Call Batching），就是在一次DrawCall里批量处理多个物体。只要物体的变化和材质相同，GPU就完全可以按照相同的方式处理，把相同材质分为一个组（一个Batch），然后合成同一个物体（统一变换），这样就可以在一个DrawCall里处理多个物体了（实际上是组合后的一个物体）。
    *   unity两种渲染模型方式，Skinned Mesh Renderer（骨骼模型）和Mesh Filter 加 Mesh Rendere,DrawCall只针对后者。
    *   Draw Call 分为 Dynamic Batching动态合并和Static Batching静态合并。
        * 动态合并
          不需要任何操作，同一材质的物体都可被合并。
        * 静态合并
          运行后一组游戏对象多个网格合并成一个网格，会动态创建合并后的网格，增加内存。
          实现方法：
        1. MeshRenderer勾选Batching Static
        2. 代码中是哦那个UnityEngine.StaticBatchingUtility实现，创建一个空对象为根对象，将所有合并的静态物体（不需要勾选Batching Static)置于其下，然后使用StaticBatchingUtility合并到一个游戏对象下，合并后可以移动父节点游戏对象。
            **推荐使用StaticBatchingUtility+动态合并**。

### 其他优化经验
* 降低资源比重
  Build 后，Console界面，右上角下来菜单-> Open Editor Log 有整个包按大小排序的资源列表，显式了资源在安装包的比例。
* 释放内存中的资源
  AssetBundle.Unload  
  Resource.unload
  GC.Collect等
* 设置目标帧率 
  通过Application.targetFrameRate设定FPS上限，稳定帧率，减少高帧率和低帧率切换的不流畅，移动设备上推荐为30FPS.
* 音频格式
  较长的背景音乐等，用OGG或者MP3的压缩格式。
  短促的枪声等，建议WAV或者AIF未压缩格式。
* 摄像机 调整合适距离，防止不必要的物体进入摄像机。
* 碰撞 尽量使用立方体或圆柱体等基本碰撞模型。

### 优化总结
* Update() 每帧都会运行，不能Update()里的逻辑尽量不要放在Update() 中。
* Debug.Log 控制台日志非常占用CPU，生成的应用安装包在运行时依然会输出日志。发布的时候要去掉。
* 频繁的变量不要用临时变量，而是存储起来，组件的获取尽量放在Awake()中。
* 尽量少用GameObject.Find()等搜索函数，效率比较低，应直接指定公共变量。
* 少用SendMessage()函数，效率比较低，而应直接掉用方法，或者用C#的delegates或System.Action.
* 少用粒子系统，粒子运动是对CPU不小的负担。
* 将大资源拆成小的模块分批加载，分散CPU对硬盘的读写，降低峰值。
* 尽量降低场景里d模型面数和点数，因为CPU需要对其进行运算再传递给GPU。

