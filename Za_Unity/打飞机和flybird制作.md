
Tags:[Unity] date: 2016-06-30

## 飞机

![](http://7xs1eq.com1.z0.glb.clouddn.com/Fly.png)

这个项目中有两个需要整理的点：


### 获取方向位移

         transform.Translate(Input.GetAxis("Horizontal") * speed * Time.deltaTime, 0f, 0f);
         transform.Translate(0f, 0f, Input.GetAxis("Vertical") * speed * Time.deltaTime);

<!-- more -->

Horizontal:水平的 Vertical：垂直的，这两个是自带方向浮点型数据，通过方向键或w、a、s、d增加或减少相应方向的量，

如w键会使Vertical变为正数，s键变为负数。

### 将子弹和陨石Prefab生成实例

        public GameObject bullet; //子弹物体
        Instantiate(bullet, new Vector3(transform.position.x, transform.position.y + 2f, transform.position.z), Quaternion.identity);  //实例函数
Quaternion.identity是四元数，该四元数，相当于"无旋转"：这个物体完全对齐于世界或父轴。

        public class example : MonoBehaviour {
        public void Awake() {
    	transform.rotation = Quaternion.identity;
    	}
        }
## flybird

### 游戏状态控制
在类MonoBehaviour外声明一个公共枚举，控制游戏的状态
​        
​        public enum GameState { 
​         start,
​         plaing,
​         end
​         }
​        public class GameManager : MonoBehaviour{
​        public static GameState state=GameState.start;//声明静态变量，使所有类能够访问
在其他脚本文件中可直接改变游戏状态
`GameManager.state=GameState.end;`

### 背景板的连续存在
如图，背景板：
![](http://7xs1eq.com1.z0.glb.clouddn.com/bgChanging.png)
当鸟飞行时，左边的背景板会消失右边的会生成，以此循环。
单个背景：
![](http://7xs1eq.com1.z0.glb.clouddn.com/onlyBg.png)
设置两个背景position变量。一个是左侧背景firstBg，一个右侧currentBg,在currentBg中心放置一个空的触发器，当鸟触发时，改变背景板。这里通过currentBg+背景宽度（10）来新建立背景。


        public void OnTriggerEnter(Collider other)
        {
        
        if (other.tag=="Player")
        {
            Transform firstbg= GameManager._intance.fistBg;
            currenBg.transform.position = new Vector3(firstbg.position.x + 10, currenBg.position.y, currenBg.position.z);
    
            GameManager._intance.fistBg = currenBg;
    
            pipe1.RandomGeneratePosition();
            pipe2.RandomGeneratePosition();
        } } }
RandomGenerate函数是管子高度随机生成的函数，一个背景上有两个管子组合（一个组合中上管子和下管子），这是挂在管子组合上的脚本。

            public void RandomGeneratePosition()
             {
                 float posY = Random.Range(-0.156f,0.176f);
                 this.transform.localPosition = new Vector3(this.transform.localPosition.x, posY, this.transform.localPosition.z);
             }

### 鸟飞行时帧数的控制
鸟的飞行需要每帧换一个图片，使鸟的翅膀看起来在煽动， 涉及到材质问题，如图：
![](http://7xs1eq.com1.z0.glb.clouddn.com/bird1.png)
Tiling是显式整个的多少，如设置为0.3333显式整个图片的三分之一，也就是一个鸟，Offset为偏移，整个图片向相关轴的偏移，如在tillingX为0.3的情况下，偏移X为0.3就是第二个翅膀想上的图片，下面为update中的代码。
​        
​            if (GameManager.state == GameState.plaing)
​            {
​                if (Input.GetMouseButton(0))
​                {
​                    Rigi.useGravity = true;
​                    Rigi.velocity = new Vector3(3, 0, 0);//给定速度	
​                    audi.Play();
​                    Vector3 vel = Rigi.velocity;
​                    Rigi.velocity = new Vector3(vel.x, 5, vel.z);
​                }
​    
            timer += Time.deltaTime;         //timer为时间计数器，如果运行五秒，此时timer为5f;
            if (timer >= 1.0f / frameNumber)  //1除以每秒的帧数，获得一帧的时间，每秒帧数可以自定义。
            {
                frameCount++;               //帧数增加，初值为零。
                timer -= 1.0f / frameNumber;     
    
                int frameIndex = frameCount % 3; //获得偏移索引，0，1，2
                rend.material.SetTextureOffset("_MainTex", new Vector2(0.3333f * frameIndex, 0));  //"_MainTex"为主要贴图，固定参数
            }
    
        }
### PlayerPrefs持久化数据
这是unity提供的一种简单有效的数据持久化方案，适合小项目对少量数据的持久化储存
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

  ![](http://7xs1eq.com1.z0.glb.clouddn.com/score.png)      
