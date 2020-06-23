

Tags:[Unity]  date: 2016-06-08

### 写在前面
在Unity3D中提供了2D,3D,4D向量类Vector,这些类都提供了对向量的操作，如取模，向量单位化，点乘，叉乘等。还有几个预设变量属性：

* Vector3.zero    : [0,0,0]
* Vector3.up      : [0,1,0]   Y轴正方
* Vector3.forward : [0,0,1]   Z轴正方
* Vector3.right   : [1,0,0]   X轴正方
  这些变量表示的值是始终固定的。
  而Transform类中的transform.up,forward,right预设变量表示当前对象在世界坐标系中的朝向，会随着对象朝向的不同而改变。
* TransformDirection，会将局部坐标转换成世界坐标，保持对象坐标的一致。
  如： 把当前对象的正面朝向从局部坐转换到世界坐标下：

        _newForward = transform.TransformDirection ( Vector3.forward);

<!-- more -->

![](http://claymore.wang:5000/uploads/big/e46d0cb2cf36205a722537ac70e197e9.png)

### 向量减法
两个对象之间的向量：

    other.positon - ransform.position 
求向量的长度（模）的平方：

    var sqrLen = (Other.position - transform.position).sqrMagnitude;
向量的magnitude属性是模，需要开方运算。有时不开放可用向量的sqrMagnitude属性。

### 标量与向量相称
可改变大小和方向

### 向量之间的点乘
点乘反映了两个向量的相似程度，结果越大，两个向量就越相近。

| a · b | 夹角范围          | a和b方向关系   |
| ----- | ------------- | --------- |
| 大于0   | 0 =< 角度 < 90  | 方向基本相同    |
| = 0   | 90            | ab正交，互相垂直 |
| < 0   | 90 < 角度 < 180 |           |

向量中的Dot函数：

    public Transform TraOther ; //其他物体的方位
    private Vector3 _VecForward ; // 前方
    private Vector3 _vecToOther ; //其他方向
    
    void Update(){
        //使用TransformDirection把当前对象的正面朝向从局部坐标转换到世界坐标系下，使该向量与其他对象的位置向量在世界坐标下同一
        //Vector3.forward表示当前对象的正方向向量
        _VecForward = transform.TransformDirection(Vector3.forward);
        //向量减法获得其他对象到当前对象之间的向量
        _vecToOther = TraOther.position - transform.position;
        //使用点乘计算结果的符号来判断其他对象是否在当前对象后方
        if(Vector3.Dot(_VecForward,_vecToOther) < 0){
            print("其他对象在我后方")；
        }else{
            print("其他对象不在我后方");
        }
    }

### 向量间的叉乘
叉乘的结果是一个向量，这个向量垂直与原来的两个向量，在unity中一般去获得一个方向，它是Corss(Vector3 lhs,Vector3 rhs)函数。
#### 单位向量化
Nomalize(),多代指方向。

### 向量间的夹角
要知道两个向量之际的夹角，可以使用向量类中的Angle(Vector3 from,Vector3 to)函数。该函数会计算from向量与to向量之间的夹角并返回度数值（不是弧度）。

    public Transform TraTarget ; //目标
    private Vector3 _VectTargetDir; //本物体和目标之间的向量
    private Vector3 _VecForward ; // 前方
    private float _FloAngle  ; // 度数
    
    void Update(){
      
      _VectTargetDir = TraTarget.position - transform.position ;
      //当前对象的正前方向量
      _VecForward = transform.forward;
      //求夹角
      _FloAngle = Vector3.Angle(_VectTargetDir,_VecForward);
      if (_FloAngle < 5.0f)
      {
          print("视线靠近了")；
      }else{
          print("视线没有靠近")；
      }
    }

![](http://claymore.wang:5000/uploads/big/b2c5f7b4e9ac35a678b3ce801e4fb9c5.png)