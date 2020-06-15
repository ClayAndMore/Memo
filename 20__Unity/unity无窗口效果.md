
---
title: "unity无窗口效果.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags:[Unity]  date: 2016-07-01

本笔记参照蛮牛案例而作
http://www.manew.com/thread-43230-1-1.html
下面是最后成品：觉得好酷炫，哈哈，谢谢大神的教程
![](http://claymore.wang:5000/uploads/big/e0faae31a17d90f81ca7e2f6936c3cfa.png)

<!-- more -->

首先新建项目，在项目中新建一个shader，shader代码如下：（可直接复制）

```
    Shader "Custom/ChromakeyTransparent" {
    Properties {
    _MainTex ("Base (RGB)", 2D) = "white" {}
    _TransparentColourKey ("Transparent Colour Key", Color) = (0,0,0,1)
    _TransparencyTolerance ("Transparency Tolerance", Float) = 0.01
    }
    SubShader {
    Pass { 
    Tags { "RenderType" = "Opaque" } 
    LOD 200 
    CGPROGRAM 
    #pragma vertex vert 
    #pragma fragment frag
    #include "UnityCG.cginc"
     
    struct a2v  
    {  
    float4 pos : POSITION; 
    float2 uv : TEXCOORD0; 
    }; 
    
    struct v2f 
    { 
    float4 pos : SV_POSITION;
    float2 uv : TEXCOORD0; 
    };
     
    v2f vert(a2v input) 
    {
    v2f output;  
    output.pos = mul (UNITY_MATRIX_MVP, input.pos);
    output.uv = input.uv;
    return output;
    }
  
    sampler2D _MainTex;
    float3 _TransparentColourKey;
    float _TransparencyTolerance;
    float4 frag(v2f input) : SV_Target
     
    {
    // What is the colour that *would* be rendered here?
    float4 colour = tex2D(_MainTex, input.uv);
    // Calculate the different in each component from the chosen transparency colour
    float deltaR = abs(colour.r - _TransparentColourKey.r);
    float deltaG = abs(colour.g - _TransparentColourKey.g);
    float deltaB = abs(colour.b - _TransparentColourKey.b);
    // If colour is within tolerance, write a transparent pixel
     
    if (deltaR < _TransparencyTolerance && deltaG < _TransparencyTolerance && deltaB < _TransparencyTolerance)
    {
    return float4(0.0f, 0.0f, 0.0f, 0.0f);
    } 
    // Otherwise, return the regular colour 
    return colour;  
    } 
    ENDCG
    }
    }
    }
```

输入一张纹理，一个关键颜色值以及相应的阈值，用于将指定的范围变透明（也就是大家所熟知的“抠图”）。
这个等我过后再学习shader回来再看。

---

接下来新建一个材质并使用上面的Shader，选定你想要替换的关键颜色值（必要时也可改变阈值）。注意这里不用手动指定纹理，我们会将摄像机的输出应用到该纹理，也就是下一步要做的事情。

新建一个脚本赋给主摄像机，代码如下：

```
    using System;
    using System.Runtime.InteropServices;
    using UnityEngine;
   
    public class NoFragment : MonoBehaviour
    {
        [SerializeField]
        private Material m_Material;
        private struct MARGINS
        {
            public int cxLeftWidth;
            public int cxRightWidth;
            public int cyTopHeight;
            public int cyBottomHeight;
        }
   
        // Define function signatures to import from Windows APIs
        [DllImport("user32.dll")]
        private static extern IntPtr GetActiveWindow();
        [DllImport("user32.dll")]
        private static extern int SetWindowLong(IntPtr hWnd, int nIndex, uint dwNewLong);
        [DllImport("Dwmapi.dll")]
        private static extern uint DwmExtendFrameIntoClientArea(IntPtr hWnd, ref MARGINS margins);
    
        // Definitions of window styles
        const int GWL_STYLE = -16;
        const uint WS_POPUP = 0x80000000;
        const uint WS_VISIBLE = 0x10000000;
        void Start()
        {
    #if !UNITY_EDITOR  
    var margins = new MARGINS() { cxLeftWidth = -1 };
     
    // Get a handle to the window
    var hwnd = GetActiveWindow();
     
    // Set properties of the window
    // See: [url]https://msdn.microsoft.com/en-us/library/windows/desktop/ms633591%28v=vs.85%29.aspx[/url]
     
    SetWindowLong(hwnd, GWL_STYLE, WS_POPUP | WS_VISIBLE);
     
    // Extend the window into the client area
    //See: [url]https://msdn.microsoft.com/en-us/library/windows/desktop/aa969512%28v=vs.85%29.aspx[/url]
     
    DwmExtendFrameIntoClientArea(hwnd, ref margins);
     
    #endif
        }
        // Pass the output of the camera to the custom material
        // for chroma replacement

        void OnRenderImage(RenderTexture from, RenderTexture to)
        {
            Graphics.Blit(from, to, m_Material);
        }
    }
    
```
这个代码复制博主的有一个地方没有注释掉，会显示错误，我更改过来了。

---

上面的代码用到了InterOpServices命名空间，以便调用一些Windows底层API从而改变Unity应用在运行时的窗口属性。然后使用OnRenderImage事件将摄像机的输出应用到RenderTexture。将使用了上面自定义Shader的材质赋给脚本种的m_Material字段，这样我们就可以开始抠图了。

---

下面重点来了，就是将天空盒去掉，这里原博文没有说，将摄像机的背景颜色改为与透明材质（就是之前新建的那个材质）中_TransparentColourKey属性一样。

---

最后就是build and run 啦。。














