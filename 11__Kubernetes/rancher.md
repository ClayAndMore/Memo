---
title: "rancher.md"
date: 2020-05-15 18:43:09 +0800
lastmod: 2020-05-15 18:43:09 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
| **Protocol** | **Port range** | **Purpose**            |
| ------------ | -------------- | ---------------------- |
| tcp          | 22             | ssh server             |
| tcp          | 80             | Rancher Server/ingress |
| tcp          | 443            | Rancher Server/ingress |
| tcp          | 6443           | kubernetes api server  |
| tcp          | 2379-2380      | etcd server client api |
| tcp          | 10250-10256    | kubernetes components  |
| tcp          | 30000-32767    | nodeport services      |
| udp          | 8472           | canal                  |