---

title: "04-Job.md"
date: 2020-03-28 18:45:29 +0800
lastmod: 2020-03-28 18:45:29 +0800
draft: false
tags: ["k8s配置文件"]
categories: ["k8s"]
author: "Claymore"

---



## Job

**Job对象通常用于运行那些仅需要执行一次的任务（例如数据库迁移，批处理脚本等等）**。

Job的本质是确保一个或多个Pod健康地运行直至运行完毕, 它强调的是运行完毕。



### 创建

``` yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

这个Job对象会启动一个Pod，用于计算π到小数点后2000位.



```csharp
$ kubectl create -f ./job.yaml
job "pi" created
[node1 ~]$ kubectl get pods
NAME       READY     STATUS    RESTARTS   AGE
pi-sgklk   1/1       Running   0          6s
```

如果返回No resources found，则表明这个计算π的Pod已经运行结束了，`get pods`命令只能返回当前正在运行的Pod，加上`-a`参数能够返回所有Pod以及对应的status。

参考：https://www.jianshu.com/p/bd6cd1b4e076
