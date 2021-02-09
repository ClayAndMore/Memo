### transtorm

`transform`属性有很多函数，可以对元素进行调整大小、移动、旋转、翻转等操作

#### scale 

CSS 属性transform里面的scale()函数，可以用来改变元素的显示比例。下面的例子把页面的段落元素放大了 2 倍：

``` css
p {
  transform:scale(2);
}
```

当使用伪类描述元素的指定状态如`:hover`时，`transform`属性可以方便的给元素添加交互。

下面是当用户悬停段落元素时，段落大小缩放到原始大小 2.1 倍的例子：

``` css
p:hover {
 transform: scale(2.1);
}
```

eg:

``` html
<style>
  div { 
    width: 70%;
    height: 100px;
    margin:  50px auto;
    background: linear-gradient(
      53deg,
      #ccfffc,
      #ffcccf
    );
  }

  div:hover {
    transform: scale(1.1);
  }
  
</style>

<div></div>
```



#### skewX 旋转

接下来要介绍的`transform`属性是`skewX`，`skewX`使选择的元素沿着 X 轴（横向）翻转指定的角度。

下面的代码沿着 X 轴翻转段落元素 -32 度。

``` css
p {
 transform: skewX(-32deg);
}
```

同理`skewX`函数使指定元素沿 X 轴翻转指定的角度，想必你已经猜到了，`skewY`属性使指定元素沿 Y 轴（垂直方向）翻转指定角度。





### 使用 box-shadow 创建新月

```html
<style>
.center
{
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100px;
  height: 100px;
  
  background-color: transparent;
  border-radius: 50%;
  box-shadow: 25px 10px 0 0 blue; 
}

</style>
<div class="center"></div>
```



### 心形

``` html
<style>
.heart {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: pink;
  height: 50px;
  width: 50px;
  transform: rotate(-45deg);
}
.heart:after {
  background-color: pink;
  content: "";
  border-radius: 50%;
  position: absolute;
  width: 50px;
  height: 50px;
  top: 0px;
  left: 25px;
}
.heart:before {
  content: "";
  background-color: pink;
  border-radius: 50%;
  position: absolute;
  width: 50px;
  height: 50px;
  top: -25px;
  left: 0px;
}
</style>
<div class = "heart"></div>
```

`:before`和`:after`必须配合`content`来使用。这个属性通常用来给元素添加内容诸如图片或者文字。当`:before`和`:after`伪类用来添加某些形状而不是图片或文字时，`content`属性仍然是必需的，但是它的值可以是空字符串。