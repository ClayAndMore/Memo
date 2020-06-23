

Tags:[Unity]  date: 2016-06-25 

### 写在前面
UnityEngin.Network是实现网络功能的核心，提供了基本的功能接口，例如建立服务器和加入服务器等。
虽然Unity自己有一个NetWork用于网络通讯，但不得不承认，最通用的网络编程还是Socket。毕竟Unity network只是为了方便，还是会存在许许多多的限制。
NetWork比较适合短连接的游戏，也就是说他和网络不是实时连接通信的，用于局域网联机的话效果十分不错，但是如果上升到了MMO游戏，则不太适宜。
Socket则具备着相当高的自由度，主流游戏均采用它。但是它比较反，需要写数据类型转化，数据->字节流->数据，稍有错误就会崩盘...
<!-- more -->
### 接口介绍
先了解下面三个基本接口：

* Network.InitializeServer(int connections,int port,bool useNat); 初始化服务器。
  * connections是最大连接数。
  * port服务监听的端口号。
  * useNat表示是否使用Nat穿透。
  * 返回枚举类型NetworkConnectionError.---NetworkConnectionError.NoError表示创建服务器成功，没有错误。
* Network.Connect(string IP,int Port); 连接服务器。
  * IP就是服务器的IP地址啦，port端口号了.
  * 返回枚举类型NetworkConnectionError.---NetworkConnectionError.NoError表示创建服务器成功，没有错误。
* Network.Disconnect();用于断开网络连接。如果是服务器的话，则是断开网络连接并关闭服务器。
  <br>
### 开始实战
建立一个空物体，命名为 Manager ，添加脚本：

    using UnityEngine;
    using System.Collections;
    
    public enum STATE
    {
        idel,
        server,
        client
    }
    
    public class Server : MonoBehaviour {
        private STATE state = STATE.idel;
        private string ip = "127,0,0,1";
        private int port = 1000;
    
        void OnGUI()
        {
            switch (state)
            {
                case STATE.idel:
                    OnIdel();   break;
                case STATE.server:
                    OnServer(); break;
                case STATE.client:
                    OnClient(); break;
            }
    
        }
    
        //idle状态，可以连接或创建服务器
        void OnIdel()
        {
            if (GUILayout.Button("建立服务器"))
            {
                NetworkConnectionError error = Network.InitializeServer(3, port, false);
                if (error == NetworkConnectionError.NoError)
                {state = STATE.server;}
            }
            GUILayout.Label("===========================");
            GUILayout.BeginHorizontal();
            GUILayout.Label("服务器ip地址");
            ip = GUILayout.TextField(ip);
            GUILayout.EndHorizontal();
            if(GUILayout.Button("连接服务器"))
            {
                NetworkConnectionError error = Network.Connect(ip, port);
                if(error == NetworkConnectionError.NoError)
                { state = STATE.client; }
            }
        }
        //server状态，显式客户端连接信息
        void OnServer()
        {
            GUILayout.Label("当前连接数量："+ Network.connections.Length);
            if(GUILayout.Button("断开服务器"))
            {
                Network.Disconnect();
                state = STATE.idel;
            }
        }
        //Client状态
        void OnClient()
        {
            GUILayout.Label("已连接至服务器");
            if(GUILayout.Button("断开"))
            {
                Network.Disconnect();
                state = STATE.idel;
            }
        }
    }

![](http://ojynuthay.bkt.clouddn.com/unityNetWork.png)



### 在unity 脚本中获取客户端的IP地址

需要using System.Net.NetworkInformation;
原理就是获取网卡的信息。

//下面这段代码是我在百度贴吧找来的，经检验是正确的

    string userIp = "";
    NetworkInterface[] adapters = NetworkInterface.GetAllNetworkInterfaces(); ;
    foreach (NetworkInterface adapter in adapters)
    {
    　　if (adapter.Supports(NetworkInterfaceComponent.IPv4))
    　　{
    　　　　UnicastIPAddressInformationCollection uniCast = adapter.GetIPProperties().UnicastAddresses;
    　　　　if (uniCast.Count > 0)
    　　　　{
    　　　　　　foreach (UnicastIPAddressInformation uni in uniCast)
    　　　　　　{
    　　　　　　　　//得到IPv4的地址。 AddressFamily.InterNetwork指的是IPv4
    　　　　　　　　if (uni.Address.AddressFamily == AddressFamily.InterNetwork)
    　　　　　　　　{
    　　　　　　　　　　userIp =uni.Address.ToString();
    　　　　　　　　}
    　　　　　　}
    　　　　}
    　　}
    }


### unity Unet 多人联机游戏

整理自 siki 的视屏教程 http://pan.baidu.com/s/1o8283xg 密码：y86u

#### Player的设置和网络初始
创建一个空物体命名为NetWorkManager 为其添加同名脚本，这是unet的核心组件 然后添加NetWork Manager HUD 这是一个ui和network交互 有客户端 和 服务端 方便开发。
![](http://ojynuthay.bkt.clouddn.com/unet%E5%A4%9A%E4%BA%BA%E8%81%94%E6%9C%BA%E6%B8%B8%E6%88%8F1.png)
用自带3D物体创建一个player存成预设，放到networkManager的 Player Prefab里。这意味着每次创建客户端或者服务端自动创建。
![](http://ojynuthay.bkt.clouddn.com/unet%E5%A4%9A%E4%BA%BA%E8%81%94%E6%9C%BA%E6%B8%B8%E6%88%8F2.png)
为player写移动脚本，添加到预设
为player添加Network Identity，意味着在网络生成，这里有两个属性，一个Server Only，是只在服务端，一个是LocalPlayerAuthority在每个客户端生成。
![](http://ojynuthay.bkt.clouddn.com/unet%E5%A4%9A%E4%BA%BA%E8%81%94%E6%9C%BA%E6%B8%B8%E6%88%8F3.png)
为player添加network Transform组件 ，实现不同端的同步，这个同步是单向的，由localPlayer同步到其他客户端

#### 子弹的设置
创建子弹预设，这里注意，要把子弹添加Network Identity，注册到networkManager，只有添加了才能注册到networkManager（在网络中生成需要注册），还要为子弹添加Network Transform 同步子弹的运动。
![](http://ojynuthay.bkt.clouddn.com/unet%E5%A4%9A%E4%BA%BA%E8%81%94%E6%9C%BA%E6%B8%B8%E6%88%8F3.png)
#### 血条
为player新建一个slider，并修改成如图：
![](http://ojynuthay.bkt.clouddn.com/unet%E5%A4%9A%E4%BA%BA%E8%81%94%E6%9C%BA%E6%B8%B8%E6%88%8F5.png)
设置颜色，然后添加脚本：

        using UnityEngine;
        using System.Collections;
        
        public class HealLookAtScreen : MonoBehaviour {
        	void Update () {
                transform.LookAt(Camera.main.transform); //让血条一直对着屏幕
        	}
        }