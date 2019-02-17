Tags:[python, spider]

### Appium的安装

GIthub: https://github.com/appium/apppium

官网： http://appium.io

官方文档： http://appium.io/introductionhtml

Python Client: https://github.com/appium/python-client



Appium 负责驱动移动端，

对于ios使用UIAutomation来实现驱动

对于Android来说，使用UIAutomator和Selendroid实现驱动。



两种方式安装，Appium Desktop 和 Node,js

桌面版从Github的Release里面就可找到， Node.js适合linux。



### Charles

Charles是一个抓包工具，可以获取app和pc的所有网络请求。

官网下载：https://www.charlesproxy.com/download/latest-release/

破解： 网盘有



charles运行在自己pc上，默认会在8888开启一个代理服务

手机可以和pc在同一个局域网内通过互相认证证书来获取流量。



抓取时，出现unknow，注意几个点：

* 手机：通用->关于本机->证书信任设置->CA勾选

* 开Charles, 点击Help->SSL Proxying->Install Charles Root Certificate

  然后输入密码进行安装，安装完成之后就要信任这个证书，刚开始我以为下载下来就没事了，其实不是。

  在钥匙串里双击这个证书，然后永久信任。

* Proxy -> SSL Proxying Settings 

  add host: * port:443