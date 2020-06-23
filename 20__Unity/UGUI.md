
---
title: "UGUI.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2020-06-22 14:47:41 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
---
title: "UGUI.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: ["unity"]
author: "Claymore"

---
Tags:[Unity]  date: 2016-06-19

### slide和文字滚动
![](http://claymore.wang:5000/uploads/big/a9a8d82cc48c0d6a7881b98d3fb9fe73.png)
基本操作都是在文字的背景图片上添加组件
![](http://claymore.wang:5000/uploads/big/b72211ad8016a0b793a0c585c895bc9c.png)

<!-- more -->

背景是image图片    调整颜色的阿尔法值 （黑白亮度）使背景 变透明

然后拉伸文字控件的长度使全部文字显示出来

再添加一个和文字控件一样大小的image 
为image添加 ScrollRect,其content设置成此text（ 让此text可以滚动）
这里将滚动方向设为垂直

添加mask组件可将显示界面外的内容隐藏，滑动能显示
添加scrollbar 将image组件scrollrect里的scrollbart添加即可实现滑动条控制

### button控件函数传值
这里介绍通过UGUIbutton的Click函数加载另外场景的两种方式，也是函数传值的方式
![](http://claymore.wang:5000/uploads/big/4d790da1f37e5ba795ed82cde931799c.png)
    
​        public void buttonStarOtherSence(string SceneName) {

        Application.LoadLevel(SceneName);
        }
    
        public void buttonStarOtherScenceNum(int sceneNum) {
        Application.LoadLevel(sceneNum);
        }
数字传值需要在buid setting里将场景添加，正如数组，索引1是第二个场景。
### image type
有四种ImageType,Simple,Sliced,Tiled,Filled
simple 即正常缩放
右上为sliced可划分九宫格 在图片属性的sprite editor中可拖拽几个点，分割出边框，使图片在缩放时边框不会失真
左下为Tiled 平铺
右下为 filled 可显示部分 技能刷新时可用
![](http://claymore.wang:5000/uploads/big/e3b1660bdeacd72d8f90f69dfdc0a0b5.jpg)

#### 制作技能冷却图标
    技能释放时，图标以中心成扇形刷新，如上右下
![](http://claymore.wang:5000/uploads/big/90b4a36657a95fb003e39a7b0b981b3f.png)
需要脚本控制：

            using UnityEngine;
            using System.Collections;
            using UnityEngine.UI;    //注意这里，加入命名空间
        
            public class SkillItem : MonoBehaviour {
        
            public float coldtimer = 2f;   //技能冷却时间
            public KeyCode kecode;  //这里不太明白
            private float timer = 0;    //时间计时
        
            private Image fillImage;
        
            bool isStartTime = false;
        	// Use this for initialization
        	void Start () {
        	fillImage=transform.Find("FilledImage").GetComponent<Image>();
        	}   //找到图片对象，覆盖在技能图片外面的暗图片
        	
        	// Update is called once per frame
        	void Update () {
                if(Input.GetKeyDown(kecode)){
                    isStartTime = true;
                }
        
        	 if(isStartTime==true){
                 timer += Time.deltaTime;
                 fillImage.fillAmount = (coldtimer - timer) / coldtimer;
        
                 if(timer>=coldtimer){
                     fillImage.fillAmount = 0;
                     timer = 0;
                     isStartTime = false;
                 }
             }
        	}
        
            public void OnSkillClick() {
                isStartTime = true;
            }
              }
将image的Click方法给予OnSIllClick，点击技能即可实现。
### 标签页
![](http://claymore.wang:5000/uploads/big/753a53348eb40e346444c0230812c714.png)
创建三个空物体，目的是分别对应GameObject.SetAvtive()方法，物体下添加各自的内容，如文字，使得在点击不同标签页时显示不同内容，每个标签页(tap)都是image物体，添加了toggle组件，下都有个图片，比自己颜色深的图片，父物体（image4）添加了了toggle group组件，使三个tap下的group都设置为它 这样就可以只选择一个页面

### 滚动列表
![](http://claymore.wang:5000/uploads/big/40be1a7f595da8c3cf58bd089aab8aa7.png)
创建一个空的image（如图）作为显式范围，添加Scroll Rect脚本，contest为一个空的gameobject，将这个gameobject高度，左端和image对齐，右端延伸到很长，放你需要的图标，这个gameobject添加网格（component->Layout->Gird Layout Group），网格内放新建的空物体，空物体下放图标。



























