
tags: [java] date: 2016-07-30 


## idea创建servlet项目

### 下载并配置tomcat
* 前提安装了javaJDK ,cmd- > java -version 和 java 
* 从官网下载tomcat，解压
* 配置环境变量
    * 在变量名中填写“CATALINA_HOME”变量值:D:\Tomcat\apache-tomcat-9.0.0.M1-windows-x64\apache-tomcat-9.0.0.M1
      <br>
    * 系统变量Path，双击打开Path变量，在“变量值”的最后面添加%CATALINA_HOME%\bin（后面没有分号）然后点击“确定”
      <br>
    * 系统变量CLASSPath变量，变量值的最后面添加%CATALINA_HOME%\lib\servlet-api.jar（后面没有分号)
* cmd输入service install Tomcat9，或者点击tomcat/bin/tomcat9w.exe启动，在浏览器localhost:8080可看到tomcat页面

### 新建工程
![](http://7xs1eq.com1.z0.glb.clouddn.com/s1.png)
此时启动会进到http://localhost:8080，看到jsp文件中设置的文件。

### 创建servlet
src工程下 新建包名，创建一个servlet类：
```
package com.claymore;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;


public class Servlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
      
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        //使用GBK设置中文正常显示
        response.setCharacterEncoding("GBK");
        response.getWriter().write("HelloWord");
    }
}
```
同时 在web.xml中配置这个类：
```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <servlet>
        <!--类名-->
        <servlet-name>Servlet</servlet-name>
        <!--路径名-->
        <servlet-class>com.claymore.Servlet</servlet-class>
    </servlet>

    <!--访问的地址-->
    <servlet-mapping>
        <servlet-name>Servlet</servlet-name>
        <url-pattern>/HelloServlet</url-pattern>
    </servlet-mapping>
    
</web-app>
```
有图有真相：
![](http://7xs1eq.com1.z0.glb.clouddn.com/s2.png)
启动项目，就能在http://localhost:8080/HelloServlet中看到helloword了

## idea创建Springboot项目

### idea下创建项目
新建 spring intitializr
![](http://7xs1eq.com1.z0.glb.clouddn.com/1.png)
写下组织名和项目名
![](http://7xs1eq.com1.z0.glb.clouddn.com/2.png)
选择web
![](http://7xs1eq.com1.z0.glb.clouddn.com/3.png)
工程目录
![](http://7xs1eq.com1.z0.glb.clouddn.com/4.png)
这里有个.mvn,没查到具体意思，知道的教教我。。。
sbAndTestApplication中添加如下代码：(添加的后面有注释)
```
    package com.sbPackage;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController          //这个是spring中的注解，
@SpringBootApplication   //这个注解是springboot的核心注解，开启自动配置
public class SbAndTestApplication {

	@RequestMapping("/")    //spring中的注解
	String index(){
		return "xixixixixixixi";
	}

	public static void main(String[] args) {     
		SpringApplication.run(SbAndTestApplication.class, args);
	}
}

```
### 运行结果
启动项目，访问127.0.0.1：8080
![](http://7xs1eq.com1.z0.glb.clouddn.com/5.png)

### springboot注解
* @SpringBootApplication
  组合了@Configuration，@EnableAutoConfiguration（jar包依赖为当前项目自动配置），@ComponentScan；

### 定制Banner
默认启动时会有个默认图标：
![](http://7xs1eq.com1.z0.glb.clouddn.com/6.png)
我们在src/main/resources 下新建一个banner.txt
访问http://patorjk.com/software/taag，可将字母转成汉字
新springboot1.4.0有个新特性，可将图片转成字符，在resources下放如命名为spanner的图片。会自动转：
![](http://7xs1eq.com1.z0.glb.clouddn.com/7.png)

### 配置文件
SpringBoot使用一个全局的配置文件 application.properties 或 application.yml,不仅支持常规的properties配置文件，还支持yaml语言的配置文件。yaml是以数据为中心的语言，在配置数据的时候有面向对象的特征。

### 命令行参数配置
Spring boot 基于jar包运行的的，打成jar包的程序可以直接通过下面命令：
`java -jar xx.jar`
通过一下命令修改tomcat端口号：
`java -jar xx.jar --server.port = 9090`

### 示例
改变tomcat的默认端口号8080，并将默认路径/改为/helloboot，在application.properties添加：
```
server.port = 9090
server.context-path=/hello
```
或在application.yml 中添加：
```
server:
    port:9090
    contextpath:/hello
```
![](http://7xs1eq.com1.z0.glb.clouddn.com/8.png)

### 取得配置文件中的值
在配置文件.properties中加：
```
book.author=claymore
```
然后：
![](http://7xs1eq.com1.z0.glb.clouddn.com/9.png)
这样就能取到配置文件中的值了，如果有多个值，可以为其建一个类，eg:
```
@Component
@Data            //自动生成属性的set和get方法，需要在pom配置依赖，和idea下载lombok插件
@ConfigurationProperties(prefix = "test",locations = {"classpath:resources/application.properties"})
public class propertiesEntity {
    private String name;
    private int age;
    private String adress;
}
```
在SbAndTestApplication中：
```
//获取配置文件
	@Autowired
	private propertiesEntity proEntity;

	@RequestMapping("/")
	String index(){
		return proEntity.getName()+proEntity.getAge()+proEntity.getAdress();
	}
```

### starter pom
Starter POMs就是maven配置文件pom.xml中的配置关联。是可以包含到应用中的一个方便的依赖关系描述符集合,我们应用了所需的starter pom ,相关的技术配置就会消除，得到spring boot 为我们提供的自动配置的Bean。
如 `spring-boot-starter`是springboot 核心starter，包含自动配置，日志，yaml等配置文件的支持。

### 日志配置
SpringBoot支持Java Util Logging,Log4J,Log4J2和Logback作为日志框架，无论使用哪种日志框架，都已做好配置。
SpringBoot 默认使用Logback作为日志框架。

### profile配置
profile是spring用来针对不同的环境对不同的配置提供支持的。在.properties中配置。
全局profile：application.properties-{profile}.properties
如：spring.profiles.active=prod
eg:
新建springboot项目，再建两个配置文件（一个开发，一个生产）：
`application-dev.properties` 和 `appication-prov.properties`
分别配置两个启动端口：sever.port=6060/7070
在原本的配置文件application中:
`spring.profiles.active=prod`这样就用7070端口来启动；=dev时则用6060。
