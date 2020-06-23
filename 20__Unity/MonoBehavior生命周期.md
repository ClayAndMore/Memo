
---
title: "MonoBehavior生命周期.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "MonoBehavior生命周期.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["unity"]
author: "Claymore"

---
Tags:[Unity]  date: 2016-06-05



### Awake() 脚本唤醒
当游戏对象被创建的时候，游戏对象绑定的这个脚本会在该帧执行Awake()函数，无论脚本时候处于激活状态都会执行。



### Star() 脚本激活时执行
在Awake()之后，脚本激活才执行（就是脚本那个勾选上），MonoBehaviour.enable = false,这个函数是不会执行的。

* 需要注意的是Awake和Start在一个游戏物体的生命周期中只调用一次，但是OnEnable会在每次激活脚本的时候再次执行。

<!-- more -->

### Update() 脚本激活执行
在每一帧里调用该函数。

### LateUpdata() 延迟更行函数，脚本激活执行
每一帧在Update()执行之后执行该函数，通常用来调整代码的顺序。
比如玩家的角色需要一个摄像机来跟随，主角位置更新放在Update()里，摄像机的跟随放在LateUpdate()里，这样确保主角位置计算完毕后，在来调整相机。

### FixedUpdate() 固定更行
每一帧处理的时间是不固定的，固定间隔时间处理代码时就要用到此函数，导航栏-> Edit -> Project Settings —> Time. Inspector 视图里会出现时间管理器，Fixed Timestep 选项用于设置 FixedUpdate()的更新频率，默认频率是0.02s。常用于物体的移动，这样能使物体移动均匀。

### OnGUI() 绘制界面函数
有UGUI ,这个函数作为测试功能使用，如创建按钮等。
它的更新频率要比Update()快：

![](http://claymore.wang:5000/uploads/big/ca570d6ed6c01a7c2d6e2768b1b4607f.png)

既然说到这，我们来看一下OnGUI的用法，在该函数中实现UI脚本：
* 它一共有两种形式
  * GUI.xxx(): 手动填写处于屏幕的位置。
  * GUILayout.xxx()：自动为我们排版 
* 测试中我们用的少，只介绍三种：
* GUILayout.Lable(string str)  : 标签，显式文本。
* GUILayout.Button(string str) : 按钮，用于触发事件。参数为按钮显示的名字。
* GUILayout.TextField (str)    : 编辑框，输入文本，参数为显式的文本。用户可以接收参数的文本，就是你输入的文本：

  	string str = "";
    	  str = GUILayout.TextField(str);


### OnDestory()
脚本销毁时调用，我们在这里可以写删除时要处理的逻辑。

### OnEnable() 激活函数
当脚本被激活时调用.

### OnDisable() 
当脚本被禁用时调用。
所用继承MonoBehaviour的脚本都有一个为enable的bool值开关，enable的值对应脚本名称左侧的勾。如果脚本没有任何生命周期函数，没有勾。
当enable为true时，生命周期各个阶段对应的函数将会被调用，当变为true时执行OnEnable(),false执行OnDisable().



### unity3d从唤醒到销毁有一段生命周期，请列出系统自己调用的几个重要方法。
Awake –>OnEnable –> Start  –> Update –> FixedUpdate –> LateUpdate –> OnGUI –> Reset –> OnDisable –> OnDestroy