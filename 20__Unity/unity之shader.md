
---
title: "unity之shader.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "unity之shader.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["unity"]
author: "Claymore"

---
Tags:[Unity]  date: 2016-06-27 

### 基本概念
*   shader：着色器，负责unity所有的渲染工作，实际上就是一小段程序，将Mesh（网格）指定的方式和输入的贴图或者颜色一起作用，然后输出。
*   将shader和输入参数打包储存在一起就是一个Material（材质），将材质赋予合适的renderer(渲染器)来进行渲染（输出）。

      Shader总体上可以分为两类：


    * Surface Shader ：表面着色器，简单技巧可以实现不错的效果。
    * Fragment Shader：底层上进行更复杂的开发。
      我们主要研究surface shader 

*   UV mapping的作用是将一个2D贴图上的点按照一定规则映射到3D模型上，是3D渲染中最常见的一种顶点处理手段

### Shader程序的基本结构
![](http://7xs1eq.com1.z0.glb.clouddn.com/shader%E7%BB%93%E6%9E%84.png)

<!-- more -->

1. 首先是一些属性定义，用来指定这段代码将有哪些输入。
2. 接下来是一个或者多个的子着色器，在实际运行中，哪一个子着色器被使用是由运行的平台所决定的。子着色器是代码的主体，每一个子着色器中包含一个或者多个的Pass。
3. 在计算着色时，平台先选择最优先可以使用的着色器，然后依次运行其中的Pass，然后得到输出的结果。最后指定一个回滚，用来处理所有Subshader都不能运行的情况（比如目标设备实在太老，所有Subshader中都有其不支持的特性）。
4. 需要提前说明的是，在实际进行表面着色器的开发时，**我们将直接在Subshader这个层次上写代码**，系统将把我们的代码编译成若干个合适的Pass。



### Hello Shader
在unity工程项目Project处新建一个shader（右键新建），我将其命名为firstShader.打开，下面为初始代码，我们一点一点来说。

    Shader "Custom/firstShader" {                        //指定了名字，可以在材质中找到这个shader，见下图
    	Properties {                                     //这里定义了着色器属性，将被输入给子着色器
    		_Color ("Color", Color) = (1,1,1,1)          //颜色RGBA（红绿蓝透明度），0～1定义的rgba颜色，比如(1,1,1,1)；
    		_MainTex ("Albedo (RGB)", 2D) = "white" {}   /2D/Rect/Cube - 对于贴图来说，默认值可以为一个代表默认tint颜色的字符串，可以是空字符串或者”white”,”black”,”gray”,”bump”中的一个 一张2阶数大小（256，512）之类的贴图。这张贴图将在采样后被转为对应基于模型UV的每个像素的颜色，最终被显示出来；
    		_Glossiness ("Smoothness", Range(0,1)) = 0.5  //Range(min, max) - 一个介于最小值和最大值之间的浮点数，一般用来当作调整Shader某些特性的参数（比如透明度渲染的截止值可以是从0至1的值等
    		_Metallic ("Metallic", Range(0,1)) = 0.0
    	}
    	SubShader {
    		Tags { "RenderType"="Opaque" } 
    		//表面着色器可以被若干的标签（tags）所修饰，而硬件将通过判定这些标签来决定什么时候调用该着色器。
    		//比如我们的例子中SubShader的第一句Tags { "RenderType"="Opaque" }告诉了系统应该在渲染非透明物体时调用我们，看下面后续。
    		
    		LOD 200  //下面有补充
    		
    		CGPROGRAM  //开始标记，表明这是一段CG程序，最后一行ENDCG与之对应，表明结束


    		// Physically based Standard lighting model, and enable shadows on all light types
    		#pragma surface surf Standard fullforwardshadows //它声明了我们要写一个表面Shader，并指定了光照模型。它的写法是这样的
            //语法：   #pragma surface surfaceFunction lightModel [optionalparams]
            //    surface - 声明的是一个表面着色器
            //   surfaceFunction - 着色器代码的方法的名字
            //   lightModel - 使用的光照模型。


​    
​    		// Use shader model 3.0 target, to get nicer looking lighting
​    		#pragma target 3.0
​    
​    		sampler2D _MainTex;  //sampler2D简单理解的话，所谓加载以后的texture（贴图）,后有补充
​    
​    		struct Input {
​    			float2 uv_MainTex;   //float和vec都可以在之后加入一个2到4的数字，来表示被打包在一起的2到4个同类型数
​    			//声明了一个叫做uv_MainTex的包含两个浮点数的变量。
​    			//在CG程序中，我们有这样的约定，在一个贴图变量（在我们例子中是_MainTex）之前加上uv两个字母，就代表提取它的uv值（其实就是两个代表贴图上点的二维坐标 ）。
​    			//我们之后就可以在surf程序中直接通过访问uv_MainTex来取得这张贴图当前需要计算的点的坐标值了。
​    		};
​    
​    		half _Glossiness;   //这里的half和我们常见float与double类似，都表示浮点数，只不过精度不一样。也许你很熟悉单精度浮点数（float或者single）和双精度浮点数（double），这里的half指的是半精度浮点数，精度最低，运算性能相对比高精度浮点数高一些，因此被大量使用。
​    		half _Metallic;
​    		fixed4 _Color;
​    
    		void surf (Input IN, inout SurfaceOutputStandard o) {   //这段代码是我们的着色器的工作核心。我们已经说过不止一次，着色器就是给定了输入，然后给出输出进行着色的代码。
    		//CG规定了声明为表面着色器的方法（就是我们这里的surf）的参数类型和名字，因此我们没有权利决定surf的输入输出参数的类型，只能按照规定写。
    		//这个规定就是第一个参数是一个Input结构，第二个参数是一个inout的SurfaceOutputStandard结构。后补。
    			// Albedo comes from a texture tinted by color
    			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;  //这里用到了一个tex2d函数，这是CG程序中用来在一张贴图中对一个点进行采样的方法，返回一个float4。
    			o.Albedo = c.rgb;
    			// Metallic and smoothness come from slider variables
    			o.Metallic = _Metallic;
    			o.Smoothness = _Glossiness;
    			o.Alpha = c.a;
    		}
    		ENDCG
    	} 
    	FallBack "Diffuse"
    }
###对上面代码的补充

*   在材质中找到shader的实例，custom有定制的意思，我的弱渣英语。
    ![](http://7xs1eq.com1.z0.glb.clouddn.com/%E6%9D%90%E8%B4%A8%E4%B8%8A%E9%80%89%E6%8B%A9shader.png)
*   对Tags的补充：
    ​      Unity定义了一些列这样的渲染过程，与RenderType是Opaque相对应的显而易见的是"RenderType" = "Transparent"，表示渲染含有**透明效果的物体**时调用。在这里Tags其实暗示了你的Shader输出的是什么，如果输出中都是非透明物体，那写在Opaque里；如果想渲染透明或者半透明的像素，那应该写在Transparent中。
    ​      另外比较有用的标签还有"IgnoreProjector"="True"（不被Projectors影响），"ForceNoShadowCasting"="True"（从不产生阴影）以及"Queue"="xxx"（指定渲染顺序队列）。这里想要着重说一下的是Queue这个标签，如果你使用Unity做过一些透明和不透明物体的混合的话，很可能已经遇到过不透明物体无法呈现在透明物体之后的情况。这种情况很可能是由于Shader的渲染顺序不正确导致的。Queue指定了物体的渲染顺序，预定义的Queue有：
    * Background - 最早被调用的渲染，用来渲染天空盒或者背景
    * Geometry - 这是默认值，用来渲染非透明物体（普通情况下，场景中的绝大多数物体应该是非透明的）
    * AlphaTest - 用来渲染经过Alpha Test的像素，单独为AlphaTest设定一个Queue是出于对效率的考虑
    * Transparent - 以从后往前的顺序渲染透明物体
    * Overlay - 用来渲染叠加的效果，是渲染的最后阶段（比如镜头光晕等特效）

    这些预定义的值本质上是一组定义整数，Background = 1000， Geometry = 2000, AlphaTest = 2450， Transparent = 3000，最后Overlay = 4000。在我们实际设置Queue值时，不仅能使用上面的几个预定义值，我们也可以指定自己的Queue值，写成类似这样："Queue"="Transparent+100"，表示一个在Transparent之后100的Queue上进行调用。通过调整Queue值，我们可以确保某些物体一定在另一些物体之前或者之后渲染，这个技巧有时候很有用处。
*   LOD 
    ​        LOD很简单，它是Level of Detail的缩写，在这里例子里我们指定了其为200（其实这是Unity的内建Diffuse着色器的设定值）。这个数值决定了我们能用什么样的Shader。在Unity的Quality Settings中我们可以设定允许的最大LOD，当设定的LOD小于SubShader所指定的LOD时，这个SubShader将不可用。Unity内建Shader定义了一组LOD的数值，我们在实现自己的Shader的时候可以将其作为参考来设定自己的LOD数值，这样在之后调整根据设备图形性能来调整画质时可以进行比较精确的控制。

                VertexLit及其系列 = 100
                Decal, Reflective VertexLit = 150
                Diffuse = 200
                Diffuse Detail, Reflective Bumped Unlit, Reflective Bumped VertexLit = 250
                Bumped, Specular = 300
                Bumped Specular = 400
                Parallax = 500
                Parallax Specular = 600
*   解释通了sampler2D是什么之后，还需要解释下为什么在这里需要一句对_MainTex的声明，之前我们不是已经在Properties里声明过它是贴图了么。答案是我们用来实例的这个shader其实是由两个相对独立的块组成的，外层的属性声明，回滚等等是Unity可以直接使用和编译的ShaderLab；而现在我们是在CGPROGRAM...ENDCG这样一个代码块中，这是一段CG程序。对于这段CG程序，要想访问在Properties中所定义的变量的话，**必须使用和之前变量相同的名字进行声明**。于是其实sampler2D _MainTex;做的事情就是再次声明并链接了_MainTex，使得接下来的CG程序能够使用这个变量。    
*   SurfaceOutputStandard结构

                struct SurfaceOutputStandard
                {
                    fixed3 Albedo;      // base (diffuse or specular) color
                    fixed3 Normal;      // tangent space normal, if written
                    half3 Emission;
                    half Metallic;      // 0=non-metal, 1=metal  金属的，含金属的
                    half Smoothness;    // 0=rough, 1=smooth    平滑
                    half Occlusion;     // occlusion (default 1)
                    fixed Alpha;        // alpha for transparencies
                };     

---

本笔记摘抄整理于http://www.360doc.com/content/13/0923/15/12282510_316492286.shtml
更多部分以及进阶在http://www.360doc.com/content/2015/0207/10/6432946_446860748.shtml
​     
​        