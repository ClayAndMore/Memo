---

title: "05-DaemonSet.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---
**一个DaemonSet对象能确保其创建的Pod在集群中的每一台（或指定）Node上都运行一个副本**。如果集群中动态加入了新的Node，DaemonSet中的Pod也会被添加在新加入Node上运行。删除一个DaemonSet也会级联删除所有其创建的Pod。下面是一些典型的DaemonSet的使用场景：

- 在每台节点上运行一个集群存储服务，例如运行glusterd，ceph。
- 在每台节点上运行一个日志收集服务，例如fluentd，logstash。
- 在每台节点上运行一个节点监控服务，例如[Prometheus Node Exporter], collectd, Datadog agent, New Relic agent, 或Ganglia gmond
- 如果新节点加入集群的时候，想要立刻感知到它，然后去部署一个 pod，帮助我们初始化一些东西
- 如果有节点退出的时候，希望对应的 pod 会被删除掉



### 创建

``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:    # .spec.template是.spec的必填字段。.spec.template用来定义Pod模板。
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

在Kubernetes 1.8之后，必须指定`.spec.selector`来确定这个DaemonSet对象管理的Pod，通常与`.spec.template.metadata.labels`中定义的Pod的label一致， 如果指定了*.spec.selector*，则必须匹配*.spec.template.metadata.labels*

一旦创建了DaemonSet，就不能对*.spec.selector进行修改，*改变Pod选择器可能会导致Pod成为孤儿。



### 仅在 某些节点运行pod

如果指定了 `.spec.template.spec.nodeSelector`，则DaemonSet控制器将在与该节点选择器匹配的Node节点上部署Pod 。

同样，如果指定了 `.spec.template.spec.affinity`，则DaemonSet控制器将在与该节点关联相匹配的Node节点上创建Pod 。

**如果您未指定上述两个字段，则DaemonSet控制器将会在所有的Node节点上创建Pod。**