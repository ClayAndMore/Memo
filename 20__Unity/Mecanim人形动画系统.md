Tags:[Unity]  date: 2016-06-29

### 模型准备
![](http://claymore.wang:5000/uploads/big/2dcf19a358a5f31fae80ca0a907cb257.png)
确保type是人形骨骼，在configure里查看骨骼与名称是否对应的上，并创建自己的替身Avatar,并且要有丰富的动作包
![](http://claymore.wang:5000/uploads/big/09fb265fc086f3cf020d677416ea7f30.png)

<!-- more -->

### 基础动画

![](http://claymore.wang:5000/uploads/big/bb688332504250107e2d6447b3ec103f.png)
添加两个变量float类型speed和bool类型IsRun，通过脚本控制变量，从而控制状态机
![](http://claymore.wang:5000/uploads/big/68d2f1840dbcf0dfdb8a027a382443af.png)   ![](http://claymore.wang:5000/uploads/big/b0abd8ea0bee377f8088605f55719a5d.png)
这里是状态的过渡，这里有个**小细节**：注意上面的has exit time,如果这个勾选上，意味着完成一个动作进度才能进行下一个，如果让人物流畅切换状态，那么不用勾选。
下面是控制代码：        
        
         void Update() {
        if (Input.GetKey(KeyCode.W)) {
​            if (Input.GetKey(KeyCode.LeftShift)) //通过按shift控制是走还是跑
​            {
​                girlAnimator.SetBool("IsRun", true); //girlAnimator为Animator组件的变量
​                girlAnimator.SetFloat("Speed", 0);
​                this.transform.Translate(Vector3.forward * floWalkingSpeed);
​            }
​            else
​            {
​                girlAnimator.SetBool("IsRun", false);
​                girlAnimator.SetFloat("Speed", 1f);
​            }
​            this.transform.Translate(Vector3.forward * floWalkingSpeed);
​        }
​    
​        else if (Input.GetKey(KeyCode.S))
​        {
​            this.transform.Translate(Vector3.back * floWalkingSpeed);
​        }
​        else
​        {
​            girlAnimator.SetBool("IsRun", false);
​            girlAnimator.SetFloat("Speed", 0f);
​        }
​    
​        if (Input.GetKey(KeyCode.A)) //注意这里控制角度，而不是直接控制左右方向位移
​        {
​            this.transform.Rotate(Vector3.down * floRotatSpeed);
​        } else if(Input.GetKey(KeyCode.D)){
​            this.transform.Rotate(Vector3.up * floRotatSpeed);
​        }  } 

### 状态树（融合技术）
通过将动画集合到一个状态树中，能更好的过渡动画，使动画流畅。
![](http://claymore.wang:5000/uploads/big/49560efb7fe5cc3804d0cb21f7d174fa.png)
先new 一个混合树Motion,和初始standing状态,建立两个float变量，Speed和Direction,两个状态靠speed参数转换。
下面是我们具体的融合树了：
![](http://claymore.wang:5000/uploads/big/cda06561770c1b1f6bca7d43611d7474.png)
speed控制走还是跑，direction控制左右转弯，当direction为正时，偏向向right的动画，负数时偏向向左的动画。

        void FixedUpdate () {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        anim.SetFloat("Speed", v);
        anim.SetFloat("Direction", h);
        anim.speed = animSpeed;  //animSpedd定义的是动画播放的速度
        velocity = new Vector3(0, 0, v);
        velocity = transform.TransformDirection(velocity);
        //确定前进与后退的速度
        if (v > 0.1f)
        {
            velocity *= floSpeed;
        }
        else if (v < -0.1f)
        {
            velocity *= backSpeed;
        }
        transform.localPosition += velocity * Time.fixedDeltaTime;
        transform.Rotate(0, h * rotateSpeed, 0);  //控制人物方向的旋转。
        }
### Mask屏蔽人物肢体动画
在人物走的状态下，加入一个跑步举手的动画层（注意有个权重，后面会说）：
![](http://claymore.wang:5000/uploads/big/a2f5db34a15fe4955e689970c6a1263e.png)
在Mask加入MaskBody(右键在project处可创建)遮罩，遮住要禁止运动的部分
![](http://claymore.wang:5000/uploads/big/0dd084f1c11fce0c2747e37b3b2f461c.png)
这里禁止了腿部动作，也就是说这个动画层只有腿部以外的动画有效。
        
        void Start () {
        anim = GetComponent<Animator>();
        if (anim.layerCount >= 2) //图层数量大于等于2
​        {
​            anim.SetLayerWeight(1, 1);//第一个数字为图层索引，1表示第二个图层，
​        }
​            }
​    
​            // Update is called once per frame
​            void Update () {
​              if (anim)
​             {
​            if (Input.GetButtonDown("Fire1"))
​            {
​                anim.SetBool("IsRaise", true);
​            }
​            if (Input.GetButtonUp("Fire1"))
​            {
​                anim.SetBool("IsRaise", false);
​            }
​            }
​            }    
如果状态机有两个动画层，设置第二个图层的权重为1，图层序号从零开始计算，**权重1表示没有被身体蒙版所蒙蔽的部分将由该图层的骨骼动画控制**，权重为零便是不受该层的影响    
walking:![](http://claymore.wang:5000/uploads/big/13e64f3bca09fb7ee133e73906d87f42.png)
walking下执行run的举手：![](http://claymore.wang:5000/uploads/big/161791a6659e2d67ab93ffa7c00b51ba.png),腿部仍为walking状态

* **状态机的复用**
  将设置好的状态机和脚本添加到其他人形模型中，任然可以实现原先的动作
  ![](http://claymore.wang:5000/uploads/big/e672b0e9f34eb55ae32a43cfa44d7e34.png)
        