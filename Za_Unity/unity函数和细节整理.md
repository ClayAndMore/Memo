---
title: unity函数和细节整理
date: 2016-06-03 09:15:02
categories: unity
tags: unity
---

## 基础函数

### 移动、旋转和缩放对象
*   移动
    对象在**原有的位置**上继续移动：

          transform.Translate ( Vector3 offset);

      相当于:

          transform.position = transform.position + offset;
    <!-- more -->

*   缩放游戏对象

                      transform.localScale = new Vector3( x, y, z);
                      transform.lacalScale *= 1.2f ; //对整体进行缩放

*   旋转游戏对象 
                  旋转有两种，一种是自转：
                ​      
                      transform.Rotate( new Vector3(0,10,0));  // 围绕Y轴转10°。
                
                  一种是围绕一个点或者一个对象来旋转：
                
                      this.transform.RotateAround(sphere.position, Vector3.up, 180);  //围绕球的位置对Y轴旋转180。

    * Vector.up : 　   Y 轴正向
    * Vector.right：   X 轴正向
    * Vector.forward : Z 轴正向

*   四元数 

                      transform.rotation = Quaternion.Euler(0f,100f, 0f);
                括号内是一个vector3的变量，这个函数将它变成四元数，我在测试的时候发现，上述代码会使物体的rotation 变成一百，是个固定的赋值，而不是旋转100°。  
                <br>
### 克隆生成实例

    public GameObject prefab；
    void OnGUI(){
        if(GUILayout.Button("克隆"){
            GameObject obj = Instantiate(prefab) as GameObject;
            obj.position = this.position;
            }
        }
<br>
### 发送广播与消息
* 发送者

        public GameObject reciever； //定义接受消息的对象
        void OnGUI(){
            if(GUILayout.Button("发送消息"){
               reciever.SendMessage("Show",100,SendMessageOptions.DontRequireReceiver);
                }
            }
  说明：第一个参数是接受的函数名称，100是传的参数，后面是是否必须有接受方法，一般可不填。
* 接收者 

        //消息接收函数，消息发送后被调用，就是接收一次调用一次
            void Show(int num)
            {
                Debug.Log("收到的数字是" + num);
            }
  <br>
### 时间类 Time
* Time.time : 从游戏开始计时，暂停不增加，运行游戏的时间。
* Time.timeScale : 时间流逝速度，1f和现实流逝速度一样，0.5f时间变慢，真实时间一秒，游戏时间过了0.5秒
* Time.deltaTime : 上一帧所消耗的时间。
* Time.fixedTime : 固定更新时间，Edit->Project Settings Time ->Time 可设置。
* Time.fixedDeltaTime : 固定更新上一帧所消耗的时间。
* TIme.realtimeSinceStarup : 从游戏开始计时，截至到目前共运行的真实时间，不受time.scale影响，游戏暂停该时间仍然增加。
  <br>
### 数字类 
*   随机数   

          int i   = Random.Range(0,10);
          float f = Random.Range(0f,10f);
*   Mathf.Abs(a): a的绝对值，a为整数或者浮点数。
*   Mathf.Clamp(a,min,max) : a限制在min和max之间，参数为整数或者浮点数。
*   Mathf.Lerp (from,to,t) : 
    * 插入值，基于浮点数t返回a到b之间的插值，t限制在**0～1**之间。当t = 0返回from，当t = 1 返回to。当t = 0.5 返回from和to的平均值。
    * 在一秒内从minimum渐变到maximum

            var minimum = 10.0; var maximum = 20.0;
            function Update () {
            transform.position = Vector3(Mathf.Lerp(minimum, maximum, Time.time), 0, 0);
            }
*   Mathf.Min (a,b,c) : 返回两个或n个数的最小值，参数为整数或者浮点数。
*   Mathf.Max (a,b,c) : 返回两个或n个数的最大值，参数为整数或者浮点数。
                <br>
### 射线
* 新建射线

        private Vector3 direction = new Vector3 (1,0,0); //定义射线的方向
        Ray ray = new Ray (transform.position,direction)

* 射线撞击状态的信息

        RaycastHit info; 
* 发射射线，函数返回bool值，如果射到了什么返回true

        Physics.Raycast(ray,out info,distance); //dis 为射线的距离，可以不填，没有距离
* 常用这样的语句判断

        if（ Physics.Raycast(ray,out info,distance)){
            if(info.collider.gameObject.tag=="NPC"){
                ...
            }
        }
* 显示射线

        Debug.DrawLine(ray.origin,ray.origin+direction*distance);
        Debug.DrawLine(ray.origin,info.point);


​      

### 脚本的单例模式

```
public static scriptName _instance;

void Awake(){_instance=this }

```



### 加载另外一个scene

`Application.loadlevel(场景的index或者string); `

eg:

```
public void StartButton(string sceneName)

{

Application.LoadLevel(sceneName);

}

或：Application.LoadLevel("runView");

```

### 隐藏物体和组件失效

隐藏物体 setActive()

组件失效 enable=

### 一个脚本开启另个脚本

`GameObject.Find("物体名称").GetComponent<你想要开启或关闭的脚本名称>().enabled = true`  
​        

## unity持久化
### PlayerPrefs
简单有效的持久化方案，适合小项目
存储数据：
PlayerPrefs.SetString("查询键”，“存储的数值”）；//存储字符串类型数据
PlayerPrefs.SetInt("查询键”，“存储的数值”）;//存储整型数据
PlayerPref.SetFloat("查询键”，“存储的数值”）; //存储 浮点型数据
输出数据：
PlayerPrefs.GetString("查询键“）；//返回字符串类型数据
PlayerPrefs.GetInt("查询键”）； //返回整形数据
PlayerPrefs.GetFlaot("查询键“）；//返回浮点型数据

  另：PlayerPrefs.Haskey("查询键”） //返回bool型 是否有这个键值。

  这个项目中需要设置当前分数和最高分数      


        public class gameMune : MonoBehaviour {

        public UILabel nowScore;    
        public UILabel highScore;
        public static gameMune _instan;
    
        void Awake()
        {
            _instan = this;
            this.gameObject.SetActive(false);  //开始时不显示分数面板
        }
    
        public void muneShow(float NScore)
        {
            float HScore = PlayerPrefs.GetFloat("score", 0); //声明得到一个键值score为零
    
        if (NScore>HScore)
        {
            HScore = NScore;
        }
    
        PlayerPrefs.SetFloat("score", HScore);  //将最高分赋值
    
        nowScore.text = NScore+"";  //+“”转换成string类型
        highScore.text = HScore + "";
         }

### XML持久化技术
XML严格易读，多用于没有网络环境下的存储介质
XML可以对对象序列化和反序列化

* 序列化： 将数据结构或对象转换成二进制串的过程
* 反序列化：将在序列化过程中所生成的二进制串转换成数据结构或者对象的过程


















## 细节总结

### 获得UGUI的slide的value值

先在脚本开头using UnityEngine.UI 就可以有专门的slider，其他控件也可以；

### 加碰撞器之前先加刚体

两collier相碰，至少有一个物体具有rigibody才会触发Trigger函数

### collider 和 collision的区别 

collider 是用做OnTriggerEnter 这类触发检测函数的参数。 
collision是用做OnCollisionEnter这类碰撞检测函数的参数，携带碰撞检测结果信息，比如碰撞的是哪个collider，碰撞的接触点等，碰撞后返回的数据存储在这个collision中。

### gameObject和Gameobject的区别

### 单位

mass的单位是1kg

坐标的单位是1m

### 用ugui时，空格键会触碰按钮

![](http://ojynuthay.bkt.clouddn.com/ugui%E8%A7%A6%E5%8F%91%E7%A9%BA%E6%A0%BC.png)

### mono

mono是.net的一个开源跨平台工具，就类似java虚拟机，java本身不是跨平台语言，但运行在虚拟机上就能够实现了跨平台。.net只能在windows下运行，mono可以实现跨平台跑， 可以运行于linux，Unix，Mac OS等。



### 判断状态机的是否在切换状态 

`if(anim.IsIntransition(0)){}`0指的是状态机的层数，默认一个状态机都为零层。该为如果在切换。（就播放声音啊，其他功能之类的）

### 相机追随主角移动 射线判断是否有物体挡在摄像机前 

```
RaycastHit hitinfo; 

if(Physics.Raycast(posArray[i],player.position-posArray[i],out hitinfo)){} 

Raycast发送射线 参数一：起始位置，参数二：方向 参数三：碰撞信息
```



## 错误解决

### UnityEngine.UI.dll’ is in timestamps but is not known in guidmapper...

 错误重新导入项目就好 
Assets->Reimport All.