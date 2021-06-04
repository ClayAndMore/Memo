---
title: "04-css动画.md"
date: 2016-07-27  17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["css"]
categories: ["前端"]
author: "Claymore"

---



## 使用动画

如果要给元素添加动画，你需要了解`animation`属性以及`@keyframes`规则。

`animation`属性控制动画的外观，`@keyframes`规则控制动画中各阶段的变化。总共有 8 个`animation`属性。为了便于理解，暂时只涉及到两个最常用的属性。

`animation-name`设置动画的名称， 也就是要绑定的选择器的`@keyframes`的名称。

`animation-duration`设置动画所花费的时间。

**`@keyframes`能够创建动画。 创建动画的原理是将一套 CSS 样式逐渐变化为另一套样式。**

具体是通过设置动画期间对应的“frames”的 CSS 的属性，以百分比来规定改变的时间，或者通过关键词“from”和“to”，等价于 0% 和 100%。打个比方，CSS 里面的 0% 属性就像是电影里面的开场镜头。CSS 里面的 100% 属性就是元素最后的样子，相当于电影里的演职员表或者鸣谢镜头。CSS 在对应的时间内给元素过渡添加效果。下面举例说明`@keyframes`和动画属性的用法：

> \#anim {
>  animation-name: colorful;
>  animation-duration: 3s;
> }
> @keyframes colorful {
>  0% {
>   background-color: blue;
>  }
>  100% {
>   background-color: yellow;
>  }
> }

id 为`anim`的元素，代码设置`animation-name`为`colorful`，设置`animation-duration`为 3 秒。然后把`@keyframes`引用到名为`colorful`的动画属性上。`colorful`在动画开始时（0%）设置颜色为蓝色，在动画结束时（100%）设置颜色为黄色。注意不是只有开始和结束的过渡可以设置，0% 到 100% 间的任意百分比你都可以设置。

eg：

``` html
<style>
  div {
    height: 40px;
    width: 70%;
    background: black;
    margin: 50px auto;
    border-radius: 5px;
  }

  #rect {
    animation-name: rainbow;
    animation-duration: 4s;
  }
  @keyframes rainbow {
    0% {
      background-color: blue;
    }
    50% {
      background-color: green;
    }
    100% {
      background-color: yellow;
    }
  }
  
</style>
<div id="rect"></div>
```

### 使用动画改变按钮悬停状态

你可以在按钮悬停时使用`@keyframes`改变按钮的颜色。

下面是在图片悬停时改变图片宽度的例子：

``` html
<style>
  img:hover {
    animation-name: width;
    animation-duration: 500ms;
  }

  @keyframes width {
    100% {
      width: 40px;
    }
  }
</style>

<img src="https://bit.ly/smallgooglelogo" alt="Google's Logo" />
```

改变按钮背景颜色：

``` html
<style>
  button {
    border-radius: 5px;
    color: white;
    background-color: #0F5897;
    padding: 5px 10px 8px 10px;
  }
  
  button:hover {
    animation-name: background-color;
    animation-duration: 500ms;
    /*   animation-fill-mode: forwards; */
  }

  @keyframes background-color {
    100% {
      background-color: #4791d0;
    }
  }
  
  
</style>
  
<button>注册</button>
```

当鼠标悬停500ms后，按钮恢复之前的颜色，我们可以设置   animation-fill-mode: forwards; 让它始终高亮；

`animation-fill-mode`指定了在动画结束时元素的样式



### 使用动画创建运动

当元素的`position`被指定，如`fixed`或者`relative`时，CSS 偏移属性`right`、`left`、`top`和`bottom`可以用在动画规则里创建动作。

就像下面的例子展示的那样，你可以在`50%`keyframe 处设置`top`属性为 50px， 在开始（0%）和最后（100%）keframe 处设置为 0px，以产生项目向下运动，然后返回的动作效果。

``` css
@keyframes rainbow {
  0% {
    background-color: blue;
    top: 0px;
  }
  50% {
    background-color: green;
    top: 50px;
  }
  100% {
    background-color: yellow;
    top: 0px;
  }
```



### 淡出

改变动画元素的`opacity`，使其在到达屏幕右侧时渐隐。

``` html
<style>

  #ball {
    width: 70px;
    height: 70px;
    margin: 50px auto;
    position: fixed;
    left: 20%;
    border-radius: 50%;
    background: linear-gradient(
      35deg,
      #ccffff,
      #ffcccc
    );
    animation-name: fade;
    animation-duration: 3s;
  }

  @keyframes fade {
    50% {
      left: 60%;
      opacity: 0.1;
    }
  }

</style>

<div id="ball"></div>
```



### 动画计数

一个常用的动画属性是`animation-iteration-count`，这个属性允许你控制动画循环的次数。下面是一个例子：

``` html
<style>

  #ball {
    width: 100px;
    height: 100px;
    margin: 50px auto;
    position: relative;
    border-radius: 50%;
    background: linear-gradient(
      35deg,
      #ccffff,
      #ffcccc
    );
    animation-name: bounce;
    animation-duration: 1s;
    animation-iteration-count: 3;
  }

  @keyframes bounce{
    0% {
      top: 0px;
    }
    50% {
      top: 249px;
      width: 130px;
      height: 70px;
    }
    100% {
      top: 0px;
    }
  }
</style>
<div id="ball"></div>
```

在这里动画会在运行 3 次后停止，如果想让动画一直运行，可以把值设置成 infinite。



### 运动加速度

`animation-timing-function`规定动画的速度曲线

* 默认的值是`ease`，动画以低速开始，然后加快，在结束前变慢。
* 其它常用的值包括`ease-out`，动画以高速开始，以低速结束;
* `ease-in`，动画以低速开始，以高速结束；
* `linear`，动画从头到尾的速度是相同的。

除了上面几个值，还可以使用赛尔曲线来定义： 通俗的讲，将一条直线放在范围只有 1 的坐标轴中，并从中间拿`p1`和`p2`两个点来拉扯（X 轴的取值区间是 [0, 1]，Y 轴任意），最后形成的曲线就是动画的贝塞尔速度曲线。下面是贝塞尔曲线模仿 ease-out 预定义值的例子：

```
animation-timing-function: cubic-bezier(0, 0, 0.58, 1);
```