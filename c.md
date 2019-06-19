环境 vs 2017



### dll程序

新建项目，Visual c++-windows 桌面 - 动态链接库(Dll)，命名为CreateDllDemo

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



### 加载dll

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



### 内部函数

