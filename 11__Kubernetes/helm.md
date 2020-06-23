---
title: "helm.md"
date: 2020-03-24 09:58:51 +0800
lastmod: 2020-03-24 09:58:51 +0800
draft: true
tags: [""]
categories: ["k8s"]
author: "Claymore"

---
Tags:[k8s]

helm list -a

删除记得用purge

helm del --purge xyz



删除所有release

helm ls --all --short | xargs -L1 helm delete --purge





### 问题



#### Helm reports that tiller is already installed in the cluster, but it's not deployed

<https://github.com/helm/helm/issues/3996>

