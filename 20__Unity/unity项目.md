

Tags:[Unity]  date: 2016-07-03

## 省赛项目-科二模拟

### 说明
这个项目是我在大学的大创项目，也是参加计算机科技省赛的项目就现在的进度做一下总结。
它主要是模拟汽车在考试中的流程，让学员掌握场地，后来会考虑结合VR进行体验上的改良。

<!-- more -->

---

### 作品截图
![](http://claymore.wang:5000/uploads/big/6d5b0399a10fc691d3e2691fb4c4dc7d.png)
![](http://claymore.wang:5000/uploads/big/928b281277e2dc988d73a5fe307b3f3a.png)
![](http://claymore.wang:5000/uploads/big/5a123047f23c62f9f00a0de98e536cfa.png)
![](http://claymore.wang:5000/uploads/big/457192d76715c2e238a9e39bf566bf99.png)
![](http://claymore.wang:5000/uploads/big/72690a6a2e5c11cce200babb1fa24da0.png)

---

### 要点说明
* 离合和刹车的控制
    因为考试时，没有油门，考虑按键不宜过多，也就没做。刹车和离合通过UGUI slider的值来控制，值的增量用按键来控制，没有按键触发时，值会自动消减。
* 档位的设计
    档位的设计是在2D平面上，方向键控制加了collider 2D的小球来到达相应档位的trigger区域，从而给予汽车不同的速度。
* 汽车的驱动力
    开始时，汽车的驱动力，用轮子的wheel Collier 来添加，但这样会造成汽车的颠簸，影响体验。后来使用rigidbody AddForce使汽车到达稳定。
* 上坡起时的处理
    坡起时，根据真实驾驶，需要踩下离合。这里，在上坡开始处，设计了一个触发器，通过触发，使汽车在上坡时按下离合可以加速。
* 视角的变换
    可以变换第一人称和第三人称的视角，在车内和车外分别添加两个相机，跟随车的移动，通过按键控制不同相机的开关。
* 地形的创建
    地形完全用unity自带地形系统Terrain制作，公路是添加的 box，更改其材质看起来更接近公路，当然黄色的公路线也是。




## VR项目-走钢丝

### 说明
    现在网上有关htc vive 开发的demo很少，相关内容都是初始摸索出来的。
    这个项目就是在这样的环境下，开发主角坐上电梯到达二层，走钢丝，到达对面电梯，上三层，就这样一直到五层，天空中障碍物会使你坠落，当然走钢丝，头部位置偏了也会掉的，坠入感很刺激哦。途中会有飞机和空中电车干扰。
    工作室有台htc vivo，就这样我们就具备了走在前面的优势。

---

### 项目截图
* 这是主角在地下仰头的视角，里面的手柄是写实的
  ![](http://claymore.wang:5000/uploads/big/87cce9f5a04934aec7b111d4a4a5bc72.png)
* 这是相机位置和一层电梯的位置（红色那个）
  ![](http://claymore.wang:5000/uploads/big/df718f46b982f7271eaa4461d53361a1.png)
* 上电梯要开门时触发的按钮，这里会涉及到触发了。
  ![](http://claymore.wang:5000/uploads/big/7b39407fcecdc30710a0823c6979483a.png)
* 在高层走钢丝，（红色电梯，有开关门动画）
  ![](http://claymore.wang:5000/uploads/big/ad6229619c8f565ce6c6f5fb253c3ceb.png)
  ![](http://claymore.wang:5000/uploads/big/7f8b42cad626fd66aff9da5690e08287.png)
* 主角在高层时的飞机
  ![](http://claymore.wang:5000/uploads/big/e76209ab10839453819c88e0ada6f710.png)
* 全图鸟瞰
  ![](http://claymore.wang:5000/uploads/big/0159ab5273c8477a2a4c622f9d151a69.png)

---

### 要点
* 整体CameraRig 的放置，重力的取消与选定
* 相机随电梯的上升，人物的视角跟随
* 钢丝和人物的碰撞接触
* 门开关动画的控制
* 手柄对按钮的识别和触发
* 人物掉下的坠落感