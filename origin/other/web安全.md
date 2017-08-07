---
title: jjj
date: 2017-06-29 17:55:09
categories:
header-img:
tags:
---



### MIME Type

浏览器中的内容有HTML，XML，GIF,Flash等，浏览器是如何区分的呢，是Mime type  是媒体类型。

媒体类型是通过HTTP协议，由服务器告知浏览器的，通过Content-Type 来表示的，如：

`Content-Type: text/HTML`

这样的text/HTML是由标准发布的。

如果是客户端自己定义的格式，一般只能以application/x- 开头。

有些浏览器会做默认处理，如和系统中的配置文件有关，操作系统中可以给文件配置Mime Type 信息，在windos下HKEY_LOCAL_MACHINESOFTWAREClassesMIMEDatabaseContent Type”主键，你可以看到所有 MIME Type 的配置信息。

