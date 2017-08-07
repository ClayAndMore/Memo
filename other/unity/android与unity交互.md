---
title: android与unity交互
date: 2016-07-01 09:25:02
categories: unity
tags: [unity,android]
---

有的功能unity方便实现，而有的功能android方便实现，经过两天苦经周折的查阅，终于将android项目的值传到了unity。

---
1. 首先用eclipse新建一个项目，现在用studio的比较多，但我还是更喜欢eclipse，它方便导出jar包。新建项目时，Minimum Required SDK最好选择4.0以上，Theme最好为none。

2. 找到unity的classes.jar文件，个人用的unity5.23,文件在目录：E:\unity\Editor\Data\PlaybackEngines\androidplayer\Variations\il2cpp\Development\Classes

3. 将classes.jar文件拖拽到android项目的libs目录：
   ![](http://7xs1eq.com1.z0.glb.clouddn.com/androidForUnityExplorer.png)

   <!-- more -->

   然后右键->Build Path->Add to Build Path,这时就能看见Referenced Libraries下有class.jar文件，如上图。

4. 打开MainActivity.java，修改代码，将MainActivity继承UnityPlayerActivity,这时eclipse会提示你导入import com.unity3d.player.UnityPlayerActivity; 点击导入即可。代码如下：
```
        import com.unity3d.player.UnityPlayerActivity;
        import android.os.Bundle;
        import android.view.Menu;
        import android.view.MenuItem;
        
        public class MainActivity extends UnityPlayerActivity {
            @Override
            protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                //setContentView(R.layout.activity_main);
            }
        
            public int Max(int a,int b){
            	if(a<b) return a;
            	return b;
            }
```
在这里，定义一个Max 函数 用于传值给unity
5. 导出jar包
   最好右键scr导出jar包
   ![](http://7xs1eq.com1.z0.glb.clouddn.com/androidUnityExp.png)

---

下面就进入unity中进行开发了。
1. 在Project中建立Plugins目录：
   test41是上面导出的jar包，注意目录里要删除android里导入的classes.jar文件，因为unity里已经存在了，AndroidMainfest是android项目的AndroidMainfest.xml文件，记得导过来。
   ![](http://7xs1eq.com1.z0.glb.clouddn.com/UnityAndroidProject.png)
2. 新建一个脚本，代码如下
```
        using UnityEngine;
        using System.Collections;
        using UnityEngine.UI;
  
        public class sencondTest : MonoBehaviour {
            public int intTest = 0;
            private AndroidJavaObject jo;
            public Text text;
            // Use this for initialization
            
            void Start () {
                AndroidJavaClass jc = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
                jo = jc.GetStatic<AndroidJavaObject>("currentActivity");
                intTest = jo.Call<int>("Max", new object[] { 10, 20 });
        	}
        
            void OnGUI()
            {
                text.fontSize = 20;
                text.text = "较大的数字是" + intTest.ToString();
                GUI.Label(new Rect(20, 20, 300, 20), "调用的Android方法：求出10和20中比较小的数字是" + intTest.ToString());
                
            }
```
说明AndroidJavaObject是一个java对象，这里获取的是java视图，然后调用自定义方法。 
（注：初步了解这里的参数之所以填”com.unity3d.player.UnityPlayer”和”currentActivity”，是因为在生成jar文件的时候，已经指定了MainActivityclass继承UnityPlayerActivity，也在XML指定了MainActivity是Main class） 
activity.Call<int>("","");这个调用的是有返回值的方法，int是返回类型，第一个参数是方法名，第二个参数是 object[] 参数。activity.Call("");调用的是没返回值没参数的方法 
3. 将脚本放到一个物体上。进行导出设置：
   ![](http://7xs1eq.com1.z0.glb.clouddn.com/unityAndroidPlayerSettings.png)
4. 记得androidSDK配置好，Edit->Preferences->Exteral Tools->android sdk
5. 最好在真机测试，不然很容易出错误 下面是最后成果：
   ![](http://ojynuthay.bkt.clouddn.com/androidForUnityLast.png)
   GUI的字比较小，可能看不到，目前，到这里就结束了，有问题欢迎交流哈。








