---
title: Unity遮挡剔除和LOD
date: 2016-06-18 10:40:04
categories: unity
tags: unity
---

### 遮挡剔除
简单点说，就是对相机视野内的物体进行渲染，看不到的不进行渲染。
来看实践：

* 新建场景，一个plane和一堆cube，模仿高楼。

  ![](http://7xs1eq.com1.z0.glb.clouddn.com/occulsion1.png)

<!-- more -->

* 选中所有的高楼（cube）,右上角static -> Occluder Static 和 Occludee Static 
* window -> Occlusion Culling  Bake烘培
* 右侧窗口的Visualizatior,开始运行
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/occlusion2.png)
  如图所示，没有被相机检测的物体没有渲染。

#### 层消隐距离
比较小的物体，在大的地图中隐藏掉，当距离近的时候可以看到。
将小的物体放到一个层（Layer），用Camera.main.layerCullDistances函数设置距离。

    void Start(){
        float[] distances = new float[32];
        //这里定义数组下标“8” ，表示第八层
        distances[8] = 10; //十米之内小物体可见
        Camera.main.layerCullDistances = distances;
    }

### LOD 层级细节
Level of Detail ,当一个物体离摄像机较远的时候使用复杂度低的模型，较进的时候使用复杂度较高的模型。
一般在第三方软件制作各个层级（不同复杂程度）的模型，并按照复杂程度的高低命名为 “模型名称_LOD0” ，“模型名称_LOD1” ，“模型名称_LOD2”等，数字越高表示复杂程度越低，这样的命名会使Unity自动添加LOD组(LODGroup).
自带的环境包里就有：
![](http://7xs1eq.com1.z0.glb.clouddn.com/LOD1.png)

实例：

* 新建场景添加三个基础物体,建立空物体名为_LOD，并将三个物体放置其下，摄像机在右边：
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/LOD2.png)
* 空物体添加组件：LODGroup，三个物体在空物体下reset，位置归零，重合到一起。
* 这里我将cube拖拽到组件的LOD0中，sphere拖拽到LOD1中，capsule拖拽到LOD2。
* 可以测试了，在将相机从右到左移动中，先显式capsule，然后shpere,最后cube.
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/LOD3.png)

