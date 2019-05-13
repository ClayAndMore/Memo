tags: [c#,Socket] date: 2016-05-30


### Socket编程
1.Socket类

* 位于System.Net.Sockets命名空间
* 构造函数定义：
    `Socket localSocket = new Socket(AddressFamily。InterNetwork,SocketType.Stream,ProtocolType.Tcp);` 
    上面是tcp面向连接的通信，后两位参数改成:
    `SocketType.Dgram,ProtocolType.UDP` 
    为无连接的udp通信
* 在Internet中，TCP/IP 使用一个网络地址和一个服务端口号来唯一标识设备。网络地址标识网络上的特定设备；端口号标识要连接到的该设备上的特定服务。网络地址和服务端口的组合称为终结点，在 .NET 框架中正是由**EndPoint** 类表示这个终结点，它提供表示网络资源或服务的抽象，用以标志网络地址等信息。.Net同时也为每个受支持的地址族定义了 EndPoint 的子代；对于 IP 地址族，该类为 IPEndPoint

<!-- more -->

* 对于服务器
    1. 实例化Socket对象，建立一个套接字
    2. 绑定本地IP端口作为服务器端。Bind方法绑定本地**终结点**。指定一个本地ip和本地端口，socket将在该终结点上监听传入的客户端连接。
    3. Listen方法开始监听客户端连接，监听网络上是否有人给自己发送东西，这里跳到客户端的1.
    4. Accept相关方法接受连接，返回与客户端通信的Socket实例。这个实例用于客户端通信，而不是上面用于监听的Socket。
    5. 通过Send和Receive方法进行收发数据。
    6. 通信结束后用Close关闭sSocket对象
* 对于客户端
    1. 调用connect方法进行连接，需要指定服务器的地址和端口（必须与服务器绑定监听的接口一致），对于UDP，可不用进行连接。
    2. Send和Receive方法收发数据。 对于未连接的socket对象(UDP)，用SendTo和ReceiveFrom。
    3. 通信结束关闭socket对象

![](http://7xs1eq.com1.z0.glb.clouddn.com/socket.png)

* 一个同步通信（UDP）的示例：两个VS项目，一个接受端，一个发送端
  发送端：

        using System;
        using System.Text;
        using System.Net;
        using System.Net.Sockets;
        
        namespace synSocketUDP1
        {
            class UDPSending
            {
                public void Display()
                {
                    //定义发送字节区
                    byte[] byteArray = new byte[100];
                    //定义网络地址
                    IPEndPoint iep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 1000);
                    Socket socket1 = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                    //发送数据
                    Console.WriteLine("请输入要发送的数据");
                    EndPoint ep = (IPEndPoint)iep;
                    while (true)
                    {
                        string strMsg = Console.ReadLine();
                        //字节转换
                        byteArray = Encoding.Default.GetBytes(strMsg);
                        socket1.SendTo(byteArray, ep);
                        if(strMsg=="exit")
                        {
                            break;
                        }
                    }
                    socket1.Shutdown(SocketShutdown.Both);
                    socket1.Close();
                }
        
                static void Main(string[] args)
                {
                    UDPSending obj = new UDPSending();
                    Console.WriteLine("---发送端----");
                    obj.Display();
                }
            }
        }
  接收端：

        using System;
        using System.Text;
        using System.Net;
        using System.Net.Sockets;
        
        namespace synSocketUDP2
        {
            class UDPReceiving
            {
                public void Display()
                {
                    //定义接受的数据
                    byte[] byteArray = new byte[100];
                    //定义网络地址
                    IPEndPoint iep = new IPEndPoint(IPAddress.Parse("127.0.0.1"),1000);
                    Socket socket2 = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                    socket2.Bind(iep);//绑定地址（服务器端）
                    //接受数据
                    EndPoint ep = (IPEndPoint)iep;
                    while (true)
                    {
                        int intReceiveLength = socket2.ReceiveFrom(byteArray, ref ep);
                        string strReceiveStr = Encoding.Default.GetString(byteArray, 0, intReceiveLength);
                        Console.WriteLine(strReceiveStr);
                    }
        
                }
        
                static void Main(string[] args)
                {
                    UDPReceiving obj = new UDPReceiving();
                    Console.WriteLine("接收端");
                    obj.Display();
                }
            }
        }
  ![](http://7xs1eq.com1.z0.glb.clouddn.com/SynUdpDisplay.png)

* 下面是一个异步通信的UDP实例：

        using System;
        using System.Text;
        using System.Net;
        using System.Net.Sockets;
        using System.Threading;
        
        namespace asynSocketUDP1
        {
            class asynUDPTalk
            {
                //定义状态
                bool boolSendingFlag = true;
                bool boolReceivingFlag = true;
        
                IPEndPoint iep = null;
                IPEndPoint iep_Receive = null;
                Socket socketSend = null;
                Socket socketReceive = null;
        
                byte[] byteSendArray = null;
                byte[] byteReceiveArray = null;
        
                static void Main(string[] args)
                {
                    asynUDPTalk obj = new asynUDPTalk();
        
                    Console.WriteLine("———————我是哈哈哈——————");
                    obj.Display();
        
                }
                public void Display()
                {
                    Thread SendThread = new Thread(SendData);
                    Thread ReceiveThread = new Thread(ReceiveDate);
        
                    SendThread.Start();
                    ReceiveThread.Start();
                }
                //发送线程方法
                public void SendData()
                {
                    Thread.Sleep(500);//休眠0.5秒，不知道这样有何用意
                    if (boolSendingFlag)
                    {
                        //定义发送字节
                        byteSendArray = new byte[100];
                        //定义网络地址
                        iep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 1001);
                        socketSend = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                        boolSendingFlag = false;
                    }
                    //发送数据
                    Console.WriteLine("请输入要发送的数据：");
                    EndPoint ep = (EndPoint)iep;
                    while (true)
                    {
                        string strMsg = Console.ReadLine();
                        //字节转换
                        byteSendArray = Encoding.Default.GetBytes(strMsg);
                        socketSend.SendTo(byteSendArray, ep);
                        if(strMsg=="exit")
                        {
                            break;
                        }
                    }
        
                    socketSend.Shutdown(SocketShutdown.Both);
                    socketSend.Close();
        
                }
                //接受线程方法
                public void ReceiveDate()
                {
                    if(boolReceivingFlag)
                    {
                        //定义接收数据区
                        byteReceiveArray = new byte[100];
                        //定义网络地址
                        iep_Receive = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 1002);
                        socketReceive = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                        socketReceive.Bind(iep_Receive);
                        boolReceivingFlag = false;
                    }
        
                    //接受数据
                    EndPoint ep = (EndPoint)iep_Receive;
                    while (true)
                    {
                        int intReceiveLength = socketReceive.ReceiveFrom(byteReceiveArray, ref ep);
                        string strReceive = Encoding.Default.GetString(byteReceiveArray, 0, intReceiveLength);
                        Console.WriteLine(strReceive);
        
                    }
                }
            }
        }
    另一个客户端跟上面代码一样，不过要把这个接受端的端口号和另一个发送端口号对应，这个的发送端也是一样。
    运行效果：
    ![](http://7xs1eq.com1.z0.glb.clouddn.com/asynSocketUdp.png)

---

###上面的是自己动手做的，下面的是网上的
*   示例（TCP)。在vs中新建一个解决方案，包含两个控制台应用项目，运行时在方案属性中可以调成多项目启动。
    1. 服务端

            using System;
            using System.Collections.Generic;
            using System.Linq;
            using System.Text;
            using System.Threading.Tasks;
            using System.Net;
            using System.Net.Sockets;
               
            namespace ServerApp
            {
                class Program
                {
                    static void Main(string[] args)
                    {
                        // 1、实例化Socket对象
                        Socket server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                        // 2、定义本地终结点
                        IPEndPoint endpoint = new IPEndPoint(IPAddress.Any, 1332);
                        // 3、绑定本地终结点
                        server.Bind(endpoint);
                        Console.WriteLine("已经绑定到本地终结点{0}。");
                        // 4、监听客户端连接
                        server.Listen(15);  //15为最大连接数
                        Console.WriteLine("等待客户端连接……");
                        // 5、接受客户端连接
                        server.BeginAccept(new AsyncCallback(AccpCallback), server);  //开启异步编程
                        Console.WriteLine("请按ESC键退出。");
                        while (Console.ReadKey().Key != ConsoleKey.Escape) ;
                        // 6、关闭Socket
                        server.Close();
                    }
            
                    private static void AccpCallback(IAsyncResult ar)
                    {
                        Socket server = (Socket)ar.AsyncState;
                        // 返回表示客户端连接的Socket
                        Socket client = server.EndAccept(ar);
                        Console.WriteLine("已接受客户端{0}的连接。", client.RemoteEndPoint.ToString());
                        // 向客户端发送一条消息
                        byte[] data = Encoding.UTF8.GetBytes("您好，服务器已经接受连接了。");
                        // 先发送内容的长度
                        int len = data.Length;
                        client.Send(BitConverter.GetBytes(len));
                        // 然后发送内容正文
                        client.Send(data);
                        // 关闭Socket
                        client.Close();
                        // 继续接受连接
                        server.BeginAccept(new AsyncCallback(AccpCallback), server);
                    }
                }
            }


    2. 客户端
    
            using System;
            using System.Collections.Generic;
            using System.Linq;
            using System.Text;
            using System.Threading.Tasks;
            
            using System.Net;
            using System.Net.Sockets;
            
            namespace ClientApp
            {
                class Program
                {
                    static void Main(string[] args)
                    {
                        // 1、实例化Socket对象
                        Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);  //参数先记下，最后一个参数可改tcp或udp
                        try
                        {
                            // 2、连接服务器
                            client.Connect("127.0.0.1", 1332);
                            Console.WriteLine("成功连接服务器{0}。", client.RemoteEndPoint.ToString());
                            // 3、接收服务器发来的消息
                            // 先读取4个字节，得到消息长度
                            byte[] buffer = new byte[4];
                            client.Receive(buffer);
                            int len = BitConverter.ToInt32(buffer, 0);
                            // 开始接收正文
                            buffer = new byte[len];
                            client.Receive(buffer);
                            string msg = Encoding.UTF8.GetString(buffer);
                            Console.WriteLine("从服务器接收到的消息：\n" + msg);
                        }
                        catch (SocketException ex)
                        {
                            Console.WriteLine(ex.Message);
                        }
                        Console.Read();
                    }
                }
            }
    3. 上例在发送消息时，将消息长度int转化为字节数组发送出去，然后才接受内容，接收的时候，先读出4个字节，转换为int值，再读取消息内容，这样做防止粘包问题。
* 实例（UDP)
    1.服务端

            using System;
            using System.Text;
            using System.Net;
            using System.Net.Sockets;
            namespace server
            {
                class AsyncUdpServer
                {
                    
                    private static Socket serverSocket; //服务器端Socket对象
                    
                    private static byte[] receiveData = new byte[1024]; //接收数据的字符数组
            
                    static string Smsg="hello";     //服务器要发送的消息
            
                    public static void Main(string[] args)
                    {
                        serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp); //实例化服务器端Socket对象
                        //服务器端的IP和端口，IPAddress.Any实际是：0.0.0.0，表示任意，基本上表示本机IP
                        IPEndPoint server = new IPEndPoint(IPAddress.Any, 11000);
                        
                        serverSocket.Bind(server);        //Socket对象跟服务器端的IP和端口绑定
                       
                        IPEndPoint clients = new IPEndPoint(IPAddress.Any, 0);   //客户端的IP和端口，端口 0 表示任意端口
                       
                        EndPoint epSender = (EndPoint)clients;          //实例化客户端 终点
            
                        //开始异步接收消息  接收后，epSender存储的是发送方的IP和端口
                        serverSocket.BeginReceiveFrom(receiveData, 0, receiveData.Length, SocketFlags.None,
                            ref epSender, new AsyncCallback(ReceiveData), epSender);
                        Console.WriteLine("Listening...");
                        while (true)
                        {
                            Smsg = Console.ReadLine();
                            if (Smsg == "exit") break;
                        }
                        
                    }
            
                    private static void ReceiveData(IAsyncResult iar)
                    {
            
                        IPEndPoint client = new IPEndPoint(IPAddress.Any, 0);   //客户端的IP和端口，端口 0 表示任意端口
            
                        EndPoint epSender = (EndPoint)client;           //实例化客户端 终点
            
                        int recv = serverSocket.EndReceiveFrom(iar, ref epSender);     //结束异步接收消息  recv 表示接收到的字符数


                        Console.WriteLine("Client:" + Encoding.ASCII.GetString(receiveData, 0, recv));//将接收到的数据打印出来，发送方采用什么编码方式，此处就采用什么编码方式 转换成字符串

  ​          
  ​          
​                        //定义要发送回客户端的消息，采用ASCII编码，如果要发送汉字或其他特殊符号，可以采用UTF-8    
​                        byte[] sendData = Encoding.ASCII.GetBytes(Smsg);
​                            //开始异步发送消息  epSender是上次接收消息时的客户端IP和端口信息
​                            serverSocket.BeginSendTo(sendData, 0, sendData.Length, SocketFlags.None,
​                                epSender, new AsyncCallback(SendData), epSender);
​            
                            receiveData = new byte[1024];  //重新实例化接收数据字节数组
            
                            //开始异步接收消息，此处的委托函数是这个函数本身，递归                               
                        serverSocket.BeginReceiveFrom(receiveData, 0, receiveData.Length, SocketFlags.None,
                                ref epSender, new AsyncCallback(ReceiveData), epSender);
                        }
                    
                    private static void SendData(IAsyncResult iar)
                    {
                        serverSocket.EndSend(iar);
                    }
                }
            }
    2.客户端
    
        using System;
        using System.Net.Sockets;
        using System.Net;
        using System.Text;
        
        namespace client
        {
            class Program
            {
                
                private static Socket clientSocket;         //客户端 Socket对象
                
                private static EndPoint epServer;           //服务器端 终点
                
                private static byte[] receiveData;          //接收数据的字符数组
                public static void Main(string[] args)
                {
                    clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);  //客户端Socket对象实例化
                   
                    IPEndPoint server = new IPEndPoint(IPAddress.Parse("172.24.15.42"), 11000);                 //设置服务器端IP地址和对应端口
                   
                    epServer = (EndPoint)server;             //实例化服务器端 终点
                    string msg;                              //要发送的消息
                    byte[] sendData;                         //要发送的字符串
                    while (true)
                    {
                        msg = Console.ReadLine();            //输入要发送的消息
                        if (msg == "exit") break;            //当输入“exit”时，退出客户端程序
                        //将消息通过ASCII编码转换为字符数组，
                        //如果要发送汉字或其他特殊符号，可以采用UTF-8 
                        sendData = Encoding.ASCII.GetBytes(msg);
                        //开始异步发送消息
                        //参数：sendData           要发送的数据
                        //参数：0：                 要发送数据的起始位置
                        //参数：sendData.Length：   要发送数据的字节数
                        //参数：SocketFlags.None：  按位组合方式
                        //参数：epServer：          接收方设备（包含IP和端口）
                        //参数：new AsyncCallback(SendData):   委托
                        //参数：null：          请求的状态信息
                        clientSocket.BeginSendTo(sendData, 0, sendData.Length, SocketFlags.None,
                            epServer, new AsyncCallback(SendData), null);
                        //实例化接收数据的字符数组
                        //若在声明时已经初始化，此处依然要进行重新初始化
                        //当上次接收的数据长度大于本次，则该数组里包含上次接收的残留数据
                        //比如：上次接收“你个小逗逼”。本次接收“开玩笑”。
                        //则数组中的数据为：“开玩笑逗逼”。
                        receiveData = new byte[1024];
                        //开始异步接收消息
                        //参数部分与异步发送部分对应，基本一致
                        clientSocket.BeginReceiveFrom(receiveData, 0, receiveData.Length, SocketFlags.None,
                            ref epServer, new AsyncCallback(ReceiveData), null);
                    }
                }
                
                private static void SendData(IAsyncResult iar)            //异步发送消息的委托函数
                {
                   
                    clientSocket.EndSend(iar);                            //完成异步发送
                }
               
                private static void ReceiveData(IAsyncResult iar)         //异步接收消息的委托函数
                {
                    
                    int recv = clientSocket.EndReceive(iar);              //完成异步接收  recv 表示接收到的字节数
                    
                    Console.WriteLine("Server: " + Encoding.ASCII.GetString(receiveData, 0, recv));    //将接收到的数据打印出来
                }
            }
        }



2.TcpListener类和TcpClient类
待补充
3.UdpClient类    