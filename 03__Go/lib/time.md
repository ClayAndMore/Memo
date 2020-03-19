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
	fmt.Println(now.UnixNano()) // 1583589465356406000
```



### 格式化 time.Fomat

这种方式可以理解成时间转换成字符串

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



