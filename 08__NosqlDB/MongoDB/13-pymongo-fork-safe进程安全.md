---
title: "13-pymongo-fork-safe进程安全.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: true
tags: ["Mongo"]
categories: ["Nosql"]
author: "Claymore"

---
https://api.mongodb.com/python/current/faq.html#is-pymongo-fork-safe



### pymongo 是线程安全的么

pymongo 是线程安全的，提供线程应用的内建连接池



### pymongo 是进程安全的么？ fork-safe?

它不是进程安全的。尤其注意MongoClient()（用fork())的情况。

特别的是，MongoClient 实例一定不是从父进程copy出来的子进程， 而是父进程子进程都有自己的MongoClient实例

