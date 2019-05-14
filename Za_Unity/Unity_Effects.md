tags:[Unity] date: 2016-06-20 

### 写在前面
这篇文章主要介绍unity的高级功能，Effects和Image Effect相关的功能。
unity 自带的Effect资源包邮不少资源，点击导航菜单栏->Assets->Import Package->Effects 导入Effects包。
Effects功能可以建空对象再添加相关组件实现，组件位于 导航菜单栏->Component->Effects

### 尾径渲染器
![](http://claymore.wang:5000/uploads/big/d87a97be840c4aa2793456da464e760f.png)
它可以实现刀剑挥舞的残影，喷气尾焰等效果。下面就来实践：
新建场景，新建一个胶囊体，拉成条状，建立空物体为剑的底部，设置为子物体。

<!-- more -->

建空物体名为 top ,是剑的上端，设置为子物体。添加**Trail Renderer**。配置如下：
![](http://claymore.wang:5000/uploads/big/0b8423aa325618b3d30810ad10dfd404.png)
有几点待补充，

* Materials里是带拖尾贴图的材质球
* Time 是拖尾贴图消失的时间
* start width 是 挥动时头部的宽度。
* end width 是挥动末尾小尾巴的宽度。
* color 就是光影的颜色了 ，可以调成渐变的比较好
* Autodestruct 是自动销毁，挥动完可以销毁。

为圆柱体添加代码：

    using UnityEngine;
    using System.Collections;
    
    public class Sword : MonoBehaviour {
        public Transform bot;
        public float timeMax = 0.2f;
        public float speed = 100f;
        private float time = 0;
        private Vector3 startPos;
        private Vector3 starAngles;
    
        void Awake()
        {
            startPos = transform.position;
            starAngles = transform.eulerAngles;
        }
    
        void OnGUI()
        {
           //按下按钮开始挥剑
           if(GUILayout.Button("挥剑"))
            {
                time = timeMax;
                transform.position = startPos;
                transform.eulerAngles = starAngles;
            }
        }
    	
    	// Update is called once per frame
    	void Update () {
            if (time > 0)
            {
                time -= Time.deltaTime;
                Swing(); 
            }
    	}
    //更新剑的旋转
        void Swing()
        {
            transform.RotateAround(bot.position, Vector3.forward, speed * Time.deltaTime);
        }
    }



### 线段渲染器
Line Renderer 
一组3D点，在每个点之间用材质绘制一条线。比如闪电。
如果闪电用一张普通的贴图，用面片也能显示，但是形状是固定的，劈下来的过程也是固定的，二使用Line Renderer，这闪电可以不同的形状路径劈下来。

### 镜头光晕
镜头光晕（Lens Flare) 是模拟摄像机镜头内折射光线的效果，用来表现真正的光源（太阳）
空物体 添加 Lens Flare组件：
![](http://claymore.wang:5000/uploads/big/ca7b8bdcb3eabf8009ce446577f3f115.png)

### 光晕
Halo　光晕是光源周围的光线区域，常用来表现光线照射空气中细小灰尘颗粒产生的效果，也可以表现一些自发光物体，如萤火虫，新建物体添加 Halo

![](http://claymore.wang:5000/uploads/big/666b7a41da4b84757db48766365078e1.png)

### 投影仪
Projector
Effects包中包含Projector文件夹，包含一些常用的资源。
#### 原理
将一个Material投影到所设定平截头体内的物体上，通常包含两张贴图Cookie 和 Falloff。
Cookie 是要投射的图案，Falloff是根据距离来决定投影的明暗（Alpha）。
#### 下面我们来为一个人物添加阴影
虽然说unity的实时光照很好，但是有的旧设备不支持，所以有那种地面上就一个圆的阴影，我们来个例子，也好熟悉其功能。
![](http://claymore.wang:5000/uploads/big/0eb6212ff6f65003c61efb482fa42656.png)

* 导入effects包
* 关闭平行光和点光源的shadow type 设置为 no shadow。
* 为主角添加一个空物体，作为子物体，名为projector，添加projector组件。
* 新建一个Material，shader类型选择为 Projector/Multiply （如果不导入包这里是没有的）。
* 将Cookie贴图设置为shadow贴图，falloff贴图设置为falloff贴图，包里自带。
* 将此Material给空物体，调整空物体的位置，放到人物头部上方，调整角度，z轴，使阴影向下。
* 这时会发现，人物因为阴影而变黑，设置人物的Layers，比如为Player。在Projector组件中的Ignore Layers设置成Player就可以了。

#### 人物选择光圈
在3D游戏开发中，经常选取人物脚下的旋转光圈。用投影做，光圈不会被障碍物挡住。

![](http://claymore.wang:5000/uploads/big/e358366d47e020afb096dc397c968afd.png)

* 前面和上面一样，把Cookie贴图换成 一个光环（图片导入设置中Warp Mode设置为Clamp），给自物体添加脚本，让其自己旋转。
* 为人物添加碰撞，用于射线检测
* 建空物体Manager,建立CharacterSelector脚本：

        using UnityEngine;
        using System.Collections;
        
        public class CharacterSeletcor : MonoBehaviour {
            //摄像机
            public Camera cam;
            private GameObject lastSelectedChar; //上次选择的角色
        
        	void Update () {
                if (Input.GetMouseButtonDown(0))
                {
                    Ray ray = cam.ScreenPointToRay(Input.mousePosition); //从相机发射射线到屏幕点击的位置
                    RaycastHit hitInfo;
                    if(Physics.Raycast(ray,out hitInfo))
                    {
                        //如果射线碰到了碰撞体，并且碰撞体对象的层为Girl
                        if (hitInfo.collider != null && hitInfo.collider.gameObject.layer == LayerMask.NameToLayer("Girl"))
                        {
                            //如果有上次选取角色且不是将要选取的角色，则取消选择
                            if(lastSelectedChar!=null&&lastSelectedChar.GetInstanceID()!= hitInfo.collider.gameObject.GetInstanceID())
                            {
                                lastSelectedChar.transform.FindChild("Projector").GetComponent<Projector>().enabled = false;
                            }                            hitInfo.collider.transform.FindChild("Projector").GetComponent<Projector>().enabled = true;
                            //记录选取的角色
                            lastSelectedChar = hitInfo.collider.gameObject;
                        }
                    }
                }
        	}
        }

#### image Effects 
导入effects包后，image effects效果可以通过 Component > iamge effects 添加。

##### Sun Shaft 太阳光束
![](http://7xs1eq.com1.z0.glb.clouddn.com/sun%20shaft.png)
就是太阳光被挡住后又散射的部分。

* 添加草地和立方体，添加带lens flares的组件的空物体。
* 调整直射光和lens flares同一个方向。
* 为摄像机添加组件 sun shafts shafts caster 为刚才的空物体，组件的threshold color可调光的强弱。
##### Twirl 旋转 
图像扭曲，为摄像机添加自带Twirl脚本：
![](http://claymore.wang:5000/uploads/big/96e36a77a98ca79f79ff6036533eb4a3.png)

#### Vortex 漩涡
和旋转相似，区别是Twirl是围绕一个点，二漩涡是围绕一个区域

##### Depth of Field 景深
景深是一种常见的后期处理效果，可模拟摄像机的属性，在关键地方明亮，在其他地方模糊，突出距离感和写实。
![](http://claymore.wang:5000/uploads/big/4cbc8f1f94ae8d2a2b5defbab8cd3da9.png)
在相机添加 Depth of Field(Lens Bur、Scatter、DX11)组件，Focus On transform 为此立方体。
![](http://claymore.wang:5000/uploads/big/7ad2adf1b99b6715bbcd0837db522781.png)

##### Tilt Shift 移轴特效
它是景深的一种特殊版本，可以使失焦区域和聚焦区域的过渡更加光滑。不容易造成图像瑕疵，但是它依赖纹理查找，造成更高的处理开销。

##### Blur 模糊 
使全部图像模糊，比如游戏暂停时。
同样，也是为相机添加Blur组件。

##### Motion Blur 动态模糊
大多数模拟摄像机系统的光随时间基类，快速摄像机或对象移动造成动态模糊的情况。

##### Bloom 泛光 
强光源看起来影响到了周围物体，是一种高校的独特效果，可以烘托出梦幻的环境。
新建材质，将Emission自发光栏强度设置为一，摄像机添加Bloom，这样，用这个材质的物体会发出泛光。

##### Noise And　Scratches　噪点和刮痕
模拟电视机信号差的图像
![](http://7xs1eq.com1.z0.glb.clouddn.com/Noise%20And%20Scratches.png)

##### Noise And Grains 噪点和颗粒
模拟噪波和胶片颗粒，电影和摄影常出现的经典效果。
![](http://7xs1eq.com1.z0.glb.clouddn.com/Noise%20And%20Grain.png)

#### 抗锯齿
首先，锯齿的产生原因是最终显示到显示器的像素点数量是有限的。某像素点对应的真实图像也许是混合的颜色，而像素点只能采集单一颜色并显示，在两种颜色相邻的边缘，沿着边缘一排像素点取到的是一种颜色，而到了某一点，取到的颜色变成了零一种，因此有了锯齿。

 抗锯齿(Anti-aliasing)就是解决这个问题，大部分抗锯齿的思路是，将锯齿相关的像素点取几个临近像素，把这些采样混合成最终像素，这样具有了临近像素的特征。
Unity抗锯齿分为两大类：

* 硬件抗锯齿：多重采样MSAA（MultiSampling Anti-Aliasing）。
  实现方法：Edit->Project Settings -> Quality,在Inspector窗口中Anti Aliasing栏中选择一种，倍数越高效果也好，但是占用显卡的性能也会越多。
* 软件抗锯齿：后期处理，包括SSAA,NFAA,DLAA,FXAA。
  实现方法： 导入effects包后，选中摄像机，Component->Image effects -> Other ->Antialiasing,在Technique栏采取所要的技术即可，相对较快的是SSAA，效果最好的是FXAA3console，FXAA Preset A 和 FXAA Preset B。
  **推荐使用MSAA硬件采样（尤其是移动平台），效率高而且所有平台都支持**

#### ToonShading 卡通渲染
基本原理是在角色外侧绘制一圈黑色的轮廓，并且让受到光照的颜色亮度离散化，明的地方更亮，暗的地方更。
![](http://claymore.wang:5000/uploads/big/f39367d69263427bf50384f3e721700f.png)
将一个模型的shader改为Toon/Lit OutLine。
Base(rbg)是它本身的贴图，Toon Ramp是effects包里带的UnilToonGradient贴图。