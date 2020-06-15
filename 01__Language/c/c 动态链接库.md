
---
title: "c 动态链接库.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
Tags: [c]

环境 vs 2017

### 动态链接库

dll, 是能够被其他动态链接库所加载的程序。

windows 官方：

user32.dll

FindWindow function

kernel32.dll

```
  4GB内存空间
+---------------------+
|                     |
|系统内核              |
|                     |
|                     |
+---------------------+
|                     |
|                     |
|                     |
|                     |
+---------------------+
```

同一份dll只会在内存中存在一份，被更改后，所有使用dll的都会改变。



#### dll程序

新建项目，Visual c++-windows 桌面 - 动态链接库(Dll)，命名为CreateDllDemo

(Vs 2015 -> Visual c++ - win32项目)

视图-解决方案资源管理器

找到源文件dllmain.cpp,这里便是dll的入口函数：

```c
// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "stdafx.h"

BOOL APIENTRY DllMain( HMODULE hModule,       // 模块句柄
                       DWORD  ul_reason_for_call,  //调用原因
                       LPVOID lpReserved     // 保留参数
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:   // 被其他程序加载
    case DLL_THREAD_ATTACH:    // 当其他程序启动了一个线程的时候
    case DLL_THREAD_DETACH:    // 当其他程序某个线程终止运行的时候
    case DLL_PROCESS_DETACH:   // 被其他程序卸载的时候
        break;
    }
    return TRUE;
}
```

调用原因有四个，如上注释。



#### 加载dll

在解决方案管理器中右键添加项目，Visual C++ - windows 桌面 - windows桌面向导 - 只勾选预编译

项目命名为loadDllDemo.

找到loadDllDemo.cpp:

```c
#include "pch.h"
#include <iostream>
#include "windows.h" // #include <windows.h>

int main()
{
	::LoadLibrary(L"CreateDllDemo.dll");
    std::cout << "Hello World!\n"; 
}
```

改成如上。

回到dllmain.cpp，改成：

```c
  case DLL_PROCESS_ATTACH:
		MessageBox(NULL, L"Dll 被加载! Process Attach", L"i love mark", MB_OK);
		break;
    case DLL_THREAD_ATTACH:
		MessageBox(NULL, L"Dll 被加载! THREAD Attach", L"i love mark", MB_OK);
		break;
    case DLL_THREAD_DETACH:
		MessageBox(NULL, L"Dll 被加载! THREAD Detach", L"i love mark", MB_OK);
		break;
    case DLL_PROCESS_DETACH:
		MessageBox(NULL, L"Dll 被加载! Process Attach", L"i love mark", MB_OK);
        break;
```

在createDllDemo上右键生成，会生成一个dll.

在loaddllDemo项目上右键调试-生成新实例：

![]()



改进下，如果找不到dll会提示：

```c
HMODULE hModule = ::LoadLibrary(L"CreateDllDemo.dll");
	//查找路径： 先在当前文件夹，如果当前的文件夹没有，去c盘syste32 然后是64
	if (hModule == NULL) {
		MessageBox(NULL, L"加载DLL失败", L"I Love Mark", MB_OK);
	}
```



试想一下，如果在我的本地文件夹里建立一个假的user32.dll, 它是不是先加载我这个假的dll.

其实这种方式原先用的很多，叫dll劫持。



### 导出函数

dll作为一个模块，一个导出函数是可以被其他程序使用的，如MessageBox, 如CreateProcess.

如何做一个导出函数呢？ 

两种方式：

#### 动态

在解决方案右键，添加新项目 DllExportDemo-> Visual c++ -> win32项目(dll) -> 导出符号

进入可以看到：

DllExportDemo.cpp, DllExportDemo.h 会和我们建的第一个项目不一样。

DllExportDemo.cpp:

```c
#include "stdafx.h"
#include "DllExportDemo.h"

// 这是导出变量的一个示例
DLLEXPORTDEMO_API int nDllExportDemo=0;

// 这是导出函数的一个示例。
DLLEXPORTDEMO_API int fnDllExportDemo(void)
{
    return 42;
}

// 这是已导出类的构造函数。
// 有关类定义的信息，请参阅 DllExportDemo.h
CDllExportDemo::CDllExportDemo()
{
    return;
}
```



改下LoadDllDemo.cpp：

```c
#include "stdafx.h"
#include <windows.h>

typedef int(*FUNC)(void); //这是一个函数类型
int main()
{
	HMODULE hModule = ::LoadLibrary(L"DllExportDemo.dll");
	if (hModule == NULL) {
		MessageBox(NULL, L"加载DLL失败", L"I Love Mark", MB_OK);
	}

	FUNC dllFunc = (FUNC)::GetProcAddress(hModule, "fnDllExportDemo");
	printf("%d", dllFunc());

    return 0;
}
```

DLLExportDemo.h:

```c
// 此类是从 DllExportDemo.dll 导出的
class DLLEXPORTDEMO_API CDllExportDemo {
public:
	CDllExportDemo(void);
	// TODO:  在此添加您的方法。
};

extern DLLEXPORTDEMO_API int nDllExportDemo;  //这里有我们的导出函数

//当前使用的是c++ 编译出来的，有命名粉碎机制, 起名和用名都不一样。
//c++ 支持重载，将你所有的函数名称都粉碎, 所以我们这里改为用c执行
// DLLEXPORTDEMO_API int fnDllExportDemo(void);
extern "C" DLLEXPORTDEMO_API int fnDllExportDemo(void);
```



生成dll,  在printf那里打断点， F5调试，在按下F10，可以看到输出终端为42。

#### 静态

```
C:\Users..\Projects\CreateDllDemo\loadDllDemo
将C:\Users..\Projects\CreateDllDemo\DllExportDemo\DLLExportDemo.h 拷贝放入上方目录
将C:\Users..\Projects\CreateDllDemo\Debug\CreateDllDemo\Debug\DllExportDemo.lib 也拷贝放入最上方目录
```

LoadDllDemo.cpp:

```c
#include "stdafx.h"
#include <windows.h>

#include"DllExportDemo.h"
#pragma comment(lib, "DllExportDemo.lib")

typedef int(*FUNC)(void); //这是一个函数类型


int main()
{
	printf("%d", fnDllExportDemo());
}
```



### 内部函数





### 伪造消息

窗口

sky++

一系列窗口操作函数

新建项目，win32 控制台应用程序，项目名：Fkqq,  不要选空项目，预编译，安全。

Fkqq.cpp:

```c
#include "stdafx.h"
#include <windows.h>


int main()
{	
	POINT pos = { 0 }; //鼠标坐标结构体，x,y
	RECT wndRect = { 0 }; //窗口坐标结构体，left，right,top, bottom,下面有解释
	while (true) {
		HWND hqq = FindWindow(L"IXGuiFoundation", L"QQ"); //获取句柄，sky++中的类名和标题名
		GetWindowRect(hqq, &wndRect); // 获取句柄的Rect给winRect
		GetCursorPos(&pos); //获取鼠标位置给pos
		if (wndRect.left < pos.x && pos.x < wndRect.right)
		{
			if (wndRect.top < pos.y && pos.y < wndRect.bottom)
			{
        // 0.1s忽闪忽灭
				ShowWindow(hqq, SW_HIDE);
				Sleep(100);
				ShowWindow(hqq, SW_SHOW);
		
        // 永远跟着鼠标走，位置调
				MoveWindow(hqq, pos.x, pos.y+100, 600, 600, true);

				
			}
		}
	}
	// MoveWindow((HWND)0x1111, 200, 200, 400, 500, true); 这里句柄是直接填的sky++中的16进制数
    return 0;
}
```



Rect坐标说明：

```
x:left            x:right
y:top             y:top
+---------------------+
|                     |
|                     |
|                     |
|                     |
|                     |
|                     |
+---------------------+
x:left            x:right
y:bottom          y:bottome
```

