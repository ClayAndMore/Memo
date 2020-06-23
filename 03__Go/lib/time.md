
---
title: "time.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "time.md"
date: 2020-03-17 15:10:43 +0800
lastmod: 2020-06-12 19:01:02 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---
## time

go中时间的操作是在`time`包中



### time.Now()

``` go
	now := time.Now()      
fmt.Println(now)             // 2020-03-07 21:57:45.866411 +0800 CST m=+0.000560285
	fmt.Println(now.Year())    // 2020
	month := now.Month()
	fmt.Println(month)         // March
	fmt.Println(int(month))    // 3, 强制转为int,则会输出数字月份
	fmt.Println(now.Day())     // 7
	fmt.Println(now.Hour())    // 21
	fmt.Println(now.Minute())  // 57
	fmt.Println(now.Second())  // 45
	fmt.Println(now.Unix())    // 1583589465 , 时间戳
	fmt.Println(now.UnixNano()) // 1583589465356406000, 时间戳 带毫秒
```



### 时区 Zone

`Zone`方法可以获得变量的时区和时区与UTC的偏移秒数

``` go
	name, offset := t.Zone()
	name1, offset1 := t.Local().Zone()
	fmt.Printf("name: %v, offset: %v, name1: %v, offset1: %v \n", name, offset, name1, offset1)
    // name: UTC, offset: 0, name1: CST, offset1: 28800
```



#### 创建时区

``` go
zone1, err := time.LoadLocation("Asia/Shanghai")
fmt.Println(zone1, err)
zone2, err := time.LoadLocation("Asia/Beijing")
fmt.Println(zone2, err)
// out:
// Asia/Shanghai <nil>
// UTC unknown time zone Asia/Beijing
```

`time.LoadLocation`可以根据时区名创建时区`Location`，所有的时区名字可以在`$GOROOT/lib/time/zoneinfo.zip`文件中找到，解压`zoneinfo.zip`可以得到一堆目录和文件，我们只需要目录和文件的名字，时区名是目录名+文件名，比如**"Asia/Shanghai"**。

中国时区名只有**"Asia/Shanghai"**和**"Asia/Chongqing"**，而没有**"Asia/Beijing"**。



#### 设置时区

``` go
localTime = time.Now()
t1 := localTime.In(time.UTC)
fmt.Println(t1)
shangHai, _ := time.LoadLocation("Asia/Shanghai")
t2 := localTime.In(shangHai)
fmt.Println(t2)
// 2020-06-05 08:14:57.4730777 +0000 UTC
// 2020-06-05 16:14:57.4730777 +0800 CST
```

使用 ln 设置来设置时区，生成一个新的时间类型。





### 格式化 time.Fomat

这种方式可以理解成**时间转换成字符串**

``` go
	now := time.Now() 
	timeFmt := "2000-01-01 15:04:05"  // 随便设置一个时间，确定它的时间格式。
	fmt.Println(now.Format(time.RFC822)) // 07 Mar 20 22:06 CST
	fmt.Println(now.Format(timeFmt))     // 2020-03-07 22:06:02
```

在time包里其他规定好的时间格式：

``` go
const (
	ANSIC       = "Mon Jan _2 15:04:05 2006"
	UnixDate    = "Mon Jan _2 15:04:05 MST 2006"
	RubyDate    = "Mon Jan 02 15:04:05 -0700 2006"
	RFC822      = "02 Jan 06 15:04 MST"
	RFC822Z     = "02 Jan 06 15:04 -0700" // RFC822 with numeric zone
	RFC850      = "Monday, 02-Jan-06 15:04:05 MST"
	RFC1123     = "Mon, 02 Jan 2006 15:04:05 MST"
	RFC1123Z    = "Mon, 02 Jan 2006 15:04:05 -0700" // RFC1123 with numeric zone
	RFC3339     = "2006-01-02T15:04:05Z07:00"
	RFC3339Nano = "2006-01-02T15:04:05.999999999Z07:00"
	Kitchen     = "3:04PM"
	// Handy time stamps.
	Stamp      = "Jan _2 15:04:05"
	StampMilli = "Jan _2 15:04:05.000"
	StampMicro = "Jan _2 15:04:05.000000"
	StampNano  = "Jan _2 15:04:05.000000000"
)
```



### parse()

**字符串类型转成时间类型**

``` go
	str4 := "2014-11-12T11:45:26.371Z"
	t, err := time.Parse(time.RFC3339, str4)  // RFC3339 = "2006-01-02T15:04:05Z07:00"
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(t) // 2014-11-12 11:45:26.371 +0000 UTC
```

如fomat里，我们设置第一个参数的格式对应我们现在的字符串时间格式来转换成时间类型。但默认转换的是UTC时间，



还有一个常用的场景转换，now默认输出的字符串转成时间

``` go
const TIME_LAYOUT = "2006-01-02 15:04:05"
func main() {
	fmt.Println("0. now: ", time.Now())  // "Asia/Shanghai"
	str :=  time.Now().String()
	str = str[:strings.LastIndex(str, " ")] // 去掉 m=+..
	fmt.Println("1. str: ", str )           // 2020-06-05 14:53:19.7923121 +0800 CST
	t, _ := time.Parse("2006-01-02 15:04:05.999999999 -0700 MST", str) // 这个时间格式很重要
	fmt.Println("2. Parse time: ", t)  // 2020-06-05 14:53:19.7923121 +0800 CST, 成功转成时间类型
	tStr := t.Format(TIME_LAYOUT)  
    fmt.Println("3. Format time str: ", tStr)  // 2020-06-05 14:53:19
}
```





### time.sleep()

```
time.Sleep(time.Second * 3)
```





### 时间间隔

``` go
	startTime := time.Now()             
	time.Sleep(time.Second * 3)
	endTime := time.Now()
	duration := endTime.Sub(startTime)
	fmt.Println(duration)                // 3.002430609s
	fmt.Println(duration.Seconds())      // 3.002430609
	fmt.Println(duration.Nanoseconds())  // 3002430609
	fmt.Println(duration.String())       // 3.002430609s

```



#### time.Since

``` go
	beginTime :=time.Now()
	time.Sleep(time.Second*2)
	durtime:= time.Since(beginTime)
	fmt.Println("离开始时间过去了：",durtime) // 	time.Sleep(time.Second*2)
```

#### time.After

``` go

```





### 时区

