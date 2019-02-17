Tags:[Unity]  date: 2016-06-12

导航系统可以让人物在场景里面只能的移动，绕过障碍等。

### 建立场景
![](http://7xs1eq.com1.z0.glb.clouddn.com/navagation.png)

* 建立如图所示的物体，将正方体，两个特别长的长方体在inspector菜单右上角static设置成navigation static。
* Window -> Navigation 添加导航。

<!-- more -->

### 烘培
参数介绍：

* Object：物体参数面板
* Navigation Static：勾选后表示该对象参与导航网格的烘培。
* OffMeshLink Generation：勾选后可跳跃(Jump)导航网格和下落(Drop)。
* Bake：烘培参数面板
* Radius：具有代表性的物体半径，半径越小生成的网格面积越大。
* Height：具有代表性的物体的高度。
* Max Slope：斜坡的坡度。
* Ste Height：台阶高度。
* Drop Height：允许最大的下落距离。
* Jump Distance：允许最大的跳跃距离。
* Min Region Area：网格面积小于该值则不生成导航网格。
* Width Inaccuracy：允许最大宽度的误差。
* Height Inaccuracy：允许最大高度的误差。
* Height Mesh：勾选后会保存高度信息，同时会消耗一些性能和存储空间
  点击bake 烘培

### Nav Mesh Agent
为圆柱体添加Nav Meh Agent,可以理解它是主角行动的代理。
参数：

* Radius：物体的半径
* Speed：物体的行进最大速度
* Acceleration：物体的行进加速度
* Augular Speed：行进过程中转向时的角速度。
* Stopping Distance：离目标距离还有多远时停止。
* Auto Traverse Off Mesh Link：是否采用默认方式度过链接路径。
* Auto Repath：在行进某些原因中断后是否重新开始寻路。
* Height：物体的高度。
* Base Offset：碰撞模型和实体模型之间的垂直偏移量。
* Obstacle Avoidance Type：障碍躲避的的表现登记，None选项为不躲避障碍，另外等级越高，躲避效果越好，同时消耗的性能越多。
* Avoidance Priority：躲避优先级。
* NavMesh Walkable：该物体可以行进的网格层掩码。

为圆柱添加脚本MyAgent：

    public class MyAgent : MonoBehaviour {
        public GameObject destinationTarget;
        public NavMeshAgent navmesh;
    	void Start () {
    	//将目的地设置为球体的位置
            navmesh.destination = destinationTarget.transform.position;
    	}
    	}
destinationTarget为球体的位置，navmesh为自身。
运行即可看到效果。

### Nav Mesh Obstacle 障碍物
不可攀爬的Nav Mesh 会被视为障碍物，不需要烘培。
可为这样的物体添加 Nav Mesh Obstacle 脚本，有box 和 胶囊体 两种碰撞。
Carve 是指NavMesh生成的可通过区域是否会被Nav Mesh Obstacle 切割。
途中横着的两个小长方体就是我添加的障碍物。

### Off_Mesh Links 分离网格链接
可以将它理解为传送门。
![](http://7xs1eq.com1.z0.glb.clouddn.com/offMesh.png)

* 在右边新建一个场地，添加一个空物体，放到相应的位置。
* 左边相应位置也添加一个空物体，放到相应位置。
* 添加一个空物体，添加Off Mesh Links 组件，将start和end设置为上面两个空物体。
  参数：
* start：起点。
* end: 终点。
* Cost Overide : 重定义负担。当值小于0时，Cost 为Navigation Area栏中设定的Cost。
* Bi-Directionnal ： 是否双向链接，默认激活。
* Activated ： 是否激活，默认激活。
* Auto Update Position ： 激活： 每次调整Start 和 End 的位置后自动更新Off Mesh Link;
* Navigation Area : Off Mesh Link 的区域类型。
* 另：遇到典型错误信息：SetDestination can only be called on an active agent that has been placed on a NavMesh?
  你需要导航的游戏对象放置的位置不对，不是Y轴远离了“地面”，就是离开了烘培的“地面”。检查主角的Y轴位置。