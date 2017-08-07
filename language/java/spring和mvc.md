---
title: spring和mvc
date: 2016-08-10 12:22:33
categories: java
tags: [java,spring]
---

### Spring和Spring mvc 
spring开源框架，威力解决企业应用的程序开发，简单来说，就它是一个轻量级的ioc和aop的容器框架。

* 容器：管理和应用bean的生命周期。
* 框架：典型的是对象被声明式的组合放在一个xml文件中。事物管理，提供了持久化框架等功能。

spring mvc就是一个MVC框架。

### 谈谈MVC
model+view+controller(数据模型+视图+控制器)
### 三层架构
 通常意义上的三层架构就是将整个业务应用划分为：
 表现层（UI）、业务逻辑层（BLL）、数据访问层（DAL）。
区分层次的目的即为了**“高内聚，低耦合”**的思想。

* 表现层（UI）：通俗讲就是展现给用户的界面，即用户在使用一个系统的时候他的所见所得。   
* 业务逻辑层（BLL）：针对具体问题的操作，也可以说是对数据层的操作，对数据业务逻辑处理。   
* 数据访问层（DAL）：该层所做事务直接操作数据库，针对数据的增添、删除、修改、更新、查找等。 

有个很好的例子：
![](http://7xs1eq.com1.z0.glb.clouddn.com/%E4%B8%89%E5%B1%82%E6%9E%B6%E6%9E%84.png)

### 关系
其实上面的mvc和三层架构间并没有太多关联，实际上**mvc只存在三层架构的展现层**，
m是包含数据的对象，在spring MVC有一个专门的类model，用来和V之间的数据交互传值。
v指得是视图页面，包含jsp等。
c当然就是控制器（Spring MVC的注解@Controller的类）。
也就是说，MVC把三层架构中的UI层再度进行了分化，分成了实体、视图、控制器三个部分，控制器完成页面逻辑，通过实体来与界面层完成通话；而C层直接与三层中的业务逻辑层BLL进行对话。

### 总结
mvc可以是三层中的一个表现层框架，属于表现层。三层和mvc可以共存。
三层是基于业务逻辑来分的，而mvc是基于页面来分的。

### 常用注解
* @Controller
  注解在类上，表明这个类是SpringMVC里的Controller，并将其声明为一个Bean,servlet会自动扫描注解了此注解的类，并将web请求映射到了注解@RequestMapping的方法上。

* @RequestMapping
  映射web请求（访问路径和参数），处理类和方法。可以注解在类或方法上，注解在方法上的路径会继承注解在类上的路径，支持Servlet的request和response作为参数

* RequestBody 
  @RequestBody 允许request的参数在request体中，而不是直接链接在地址后面。此注解放置在参数前。

* @ResponseBody
  @RequestBody支持返回值放在response体内。**而不是返回一个页面**,很多基于Ajax程序的时候，可以以此注解返回数据而不是页面，注解放置在返回值前或者方法上。

* @RestController 
  @Controller和@ResponseBody的组合注解，意味着只开发一个和页面交互控制的时候，需要使用此注解。没有此注解，就加上面两个注解。

### springboot一些注解

* @SpringBootApplication: 申明让springboot自动给程序进行必要的配置，等价于以默认属性使用 @Configuration，@EnableAutoConfiguration和@ComponentScan

* @RestControlle:我们在编写接口的时候，时常会有需求返回json数据，那么在spring boot应该怎么操作呢？主要是在class中加入注解@RestController,。

* 在一个项目中的异常我们我们都会统一进行处理的，那么如何进行统一进行处理呢？
  新建一个类GlobalDefaultExceptionHandler，
  在class注解上@ControllerAdvice,
  在方法上注解上@ExceptionHandler(value = Exception.class)

* 1)如果只是使用**@RestController**注解Controller，则Controller中的方法无法返回jsp页面，配置的视图解析器InternalResourceViewResolver不起作用，返回的内容就是Return 里的内容。
  例如：本来应该到success.jsp页面的，则其显示success.
  2)如果需要返回到指定页面，则需要用 **@Controller**配合视图解析器InternalResourceViewResolver才行。
  3)如果需要返回JSON，XML或自定义mediaType内容到页面，则需要在对应的方法上加上**@ResponseBody**注解。