### 手势解锁

使用canvas的锁：

参考： https://www.jb51.net/article/102236.htm

注意，真正在手机端运行起来会很卡

不使用canvas：

https://github.com/geminate/mini-gesture-lock



#### hover-class

https://www.jb51.net/article/156958.htm





#### openid 缓存放置

```
wx.setStorageSync('openid', res.data.data.openid),设置
var openid = wx.getStorageSync('openid')获取
```

