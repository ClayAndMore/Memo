## 文本

### text-align 

`text-align: justify;` 两端对齐， 除了最后一行

`text-align: center;` 居中

`text-align: right;` 右侧 对齐

And `text-align: left;` (默认值) 左侧对齐

eg:

``` html
<h1 style="text-align:center">This is a heading</h1>
<p>The heading above is aligned to the center of this page.</p>
```



### hr

可以使用hr标记在包含元素的宽度上添加一条水平线。这可以用于定义主题的更改，或用于可视地分离内容组。



### 阴影

box-shadow属性为一个元素应用一个或多个阴影。

| 值         | 描述                                   |
| :--------- | :------------------------------------- |
| *h-shadow* | 必需。水平阴影的位置。允许负值。       |
| *v-shadow* | 必需。垂直阴影的位置。允许负值。       |
| *blur*     | 可选。模糊距离。                       |
| *spread*   | 可选。阴影的尺寸。                     |
| *color*    | 可选。阴影的颜色。请参阅 CSS 颜色值。  |
| inset      | 可选。将外部阴影 (outset) 改为内部阴影 |

eg:

``` css
/* 一个灰色的阴影，使元素立体起来 */
box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23); 
/* 向内阴影 */ 
box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23) inset; 
```

图解：

![](https://www.html.cn/newimg88/2018/07/box-shadow-diagram.png)



## 颜色

### 互补色

色彩理论以及设计色彩学很复杂，这里将只涉及很基础的部分。在网站设计里，颜色能让内容更醒目，能调动情绪，从而创造舒适的视觉体验。不同的颜色组合对网站的视觉效果影响很大，精妙的设计都需要适宜的颜色来美化页面内容。

一半是科学，一半是艺术，色环是我们认识颜色关系的好工具 - 它是一个近色相邻异色相离的圆环。当两个颜色恰好在色环的两端时，这两个颜色叫做补色。绘画中两只补色在混合后会变成灰色。补色搭配能形成强列的对比效果，传达出活力、能量、兴奋等意义。

下面是一些十六进制码（hex code）补色的例子：

> 红色（#FF0000）和蓝绿色 (#00FFFF)
> 绿色（#00FF00）和品红色（#FF00FF）
> 蓝色（#0000FF）和黄色（#FFFF00）

现在很多的在线选色工具都有寻找补色的功能。



### 三原色

电脑显示器和手机屏幕是一种加色模型，将红（R）、绿（G）、蓝（B）三原色的色光以不同的比例相加，以产生多种多样的色光。

**两种原色相加产生二次色：蓝绿（G+B）、品红（R+B）和黄色（R+G）**。

这些二次色恰好是在合成它们时未使用的原色的补色（FF0000+00FF00 = 0000FF 的补色），即在色环中位于两端。例如，品红色是红色和蓝色相加产生，它是绿色的补色。

三次色是由原色和二次色相加产生的颜色，例如红色（原色）和黄色（二次色）相加产生橙色。将这六种颜色中相邻的颜色相加，便产生了十二色色环。

![](https://img-blog.csdnimg.cn/2019062222441059.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Z3aGR6aA==,size_16,color_FFFFFF,t_70)

设计里面有很多种颜色搭配方法。涉及到三次色的一种配色方法是分裂补色搭配法。选定主色之后，在色环上选择与它的补色相邻的两种颜色与之搭配。此种搭配既有对比，又不失和谐。

下面是使用分裂补色搭配法创建的三个颜色：

| 颜色   | HEX 颜色码 |
| :----- | :--------- |
| 橙色   | #FF7D00    |
| 蓝绿色 | #00FFFF    |
| 树莓红 | #FF007D    |



们知道了补色搭配能形成强列的对比效果，让内容更富生机。但是如果使用不当效果会适得其反，比如如果文字背景色和文字颜色互为补色，文字会很难看清。通常的做法是，一种颜色做为主要颜色，其补色用来装点页面。

eg:

``` html
<style>
  body {
    background-color: white;
  }
  header {
    background-color: #09A7A1;
    color: white;
    padding: 0.25em;
  }
  h2 {
    color: #09A7A1;
  }  
  button {
    background-color: #FF790E;
  }
  footer {
    background-color: #09A7A1;
    color: white;
    padding: 0.5em;
  }
</style>
<header>
  <h1>FCC 中国</h1>
</header>
<main>
  <article>
    <h2>FCC 成都社区</h2>
    <p>【FCC成都社区】是一个非营利性的公益性技术社区，由一群编程技术爱好者，利用业余时间搭建的一个友好的交流、学习、互助的平台，帮助开发者、技术爱好者提升个人技术能力，同时帮助企业解决人才问题。</p>
    <button><a href="https://freecodecamp-chengdu.github.io/" target="_blank">更多</a></button>
  </article>
  <article>
    <h2>FCC 深圳社区</h2>
    <p>【FCC 深圳社区】全称 freeCodeCamp 深圳社区，面向深圳所有有意学习编程、热爱编程、甚至想要通过编程找到一份好工作的学生和社会群众，传承 freeCodeCamp 中文社区的主旨思想，倡导人人皆可编程。</p>
    <button><a href="https://freecodecamp-shenzhen.github.io/" target="_blank">更多</a></button>
  </article>
</main>
<br>
<footer>&copy;2018 FCC 中国</footer>
```

使用深青色（`#09A7A1`）做为页面主色，用其补色橙色（`#FF790E`）来装饰登录按钮。



### 色相

HSL 色彩空间模型是一种将 RGB 色彩模型中的点放在圆柱坐标系中的表示法，描述了色相（hue）、饱和度（saturation）、亮度（lightness）。CSS3 引入了对应的`hsl()`属性做为对应的颜色描述方式。

**色相**是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。以颜色光谱为例，光谱左边从红色开始，移动到中间的绿色，一直到右边的蓝色，色相值就是沿着这条线的取值。在`hsl()`里面，色相用色环来代替光谱，色相值就是色环里面的颜色对应的从 0 到 360 度的角度值。

**饱和度**是指色彩的纯度，也就是颜色里灰色的占比，越高色彩越纯，低则逐渐变灰，取0-100%的数值。

**亮度**决定颜色的明暗程度，也就是颜色里白色或者黑色的占比，100% 亮度是白色， 0% 亮度是黑色，而 50% 亮度是“一般的”。

下面是一些使用`hsl()`描述颜色的例子，颜色都为满饱和度，中等亮度:

| 颜色 | HSL                 |
| :--- | :------------------ |
| 红   | hsl(0, 100%, 50%)   |
| 黄   | hsl(60, 100%, 50%)  |
| 绿   | hsl(120, 100%, 50%) |
| 蓝绿 | hsl(180, 100%, 50%) |
| 蓝   | hsl(240, 100%, 50%) |
| 品红 | hsl(300, 100%, 50%) |



### 色调

`hsl()`使 CSS 更改色调更方便。给纯色添加白色可以创造更浅的色调，添加黑色可以创造更深的色调。另外，还可以通过给纯色添加灰色来同时改变颜色的深浅和明暗。回忆下`hsl()`里面的‘s’和‘l’分辨代表饱和度和亮度。饱和度代表灰色的占比，亮度代表白色和黑色的占比。这在当你有了一个基色调却需要微调时非常有用。



### 线性渐变

HTML 元素的背景色并不局限于单色。CSS 还提供了颜色过渡，也就是渐变。可以通过`background`里面的`linear-gradient()`来实现线性渐变，下面是它的语法：

```
background: linear-gradient(gradient_direction, 颜色 1, 颜色 2, 颜色 3, ...);
```

第一个参数指定了颜色过渡的方向 - 它的值是角度，90deg 代表垂直渐变，45deg 的渐变角度和反斜杠方向差不多。剩下的参数指定了渐变颜色的顺序：

例子：

```
background: linear-gradient(90deg, red, yellow, rgb(204, 204, 255));
```

eg:

``` html
<style>

  div{ 
    border-radius: 20px;
    width: 70%;
    height: 400px;
    margin: 50px auto;
    background: linear-gradient(35deg, #CCFFFF, #FFCCCC)
  }

</style>

<div></div>
```

颜色很好看。

还可以使用渐变创建条纹，

`repeating-linear-gradient()`函数和`linear-gradient()`很像，主要区别是`repeating-linear-gradient()`重复指定的渐变。 

``` css
    background: repeating-linear-gradient(
      90deg,
      yellow 0px,
      blue 40px,
      green 40px,
      red 80px
    );
```

90 deg 指的是渐变角度， 45deg是斜条纹，90则是竖直条纹。

起止渐变颜色值代表渐变颜色及其宽度值，由颜色值和起止位置组成，起止位置用百分比或者像素值表示。

所以理解上方例子是如何过渡的：

`0px [黄色 -- 过渡 -- 蓝色] 40px [绿色 -- 过渡 -- 红色] 80px`

eg：一个黑黄条纹的例子：

``` html
<style>

  div{ 
    border-radius: 20px;
    width: 70%;
    height: 400px;
    margin:  50 auto;
    background: repeating-linear-gradient(
      45deg,
      yellow 0px,
      yellow 40px,
      black 40px,
      black 80px
    );
  }

</style>

<div></div>
```

