---
title: "dashborad.md"
date: 2020-03-24 09:58:51 +0800
lastmod: 2020-03-24 09:58:51 +0800
draft: false
tags: [""]
categories: ["k8s"]
author: "Claymore"

---


### 安装

从github

```
git clone https://github.com/kubernetes/dashboard
cd dashboard/src/deploy/recommend
kubectl apply -f  kubernetes-dashboard.yaml
```

或直接`kubectl apply -f `

`https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml> `

需要翻墙。

网络原因可以使用如下连接：

`kubectl apply -f http://mirror.faasx.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml`

上面使用的yaml只是将 原github yaml中的 *k8s.gcr.io* 替换为了 *reg.qiniu.com/k8s*。



查看状态：

```查看
master $ kubectl -n kube-system get all  -l k8s-app=kubernetes-dashboard
NAME                                        READY     STATUS    RESTARTS   AGE
pod/kubernetes-dashboard-67896bc598-dhdpz   1/1       Running   0          3m

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/kubernetes-dashboard   ClusterIP   10.109.92.207   <none>        443/TCP   3m

NAME                                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kubernetes-dashboard   1         1         1            1           3m

NAME                                              DESIRED   CURRENT   READY     AGE
replicaset.apps/kubernetes-dashboard-67896bc598   1         1         1         3m
```



### 访问

#### localhsot

`Service` 使用了 `ClusterIP` 的类型，所以在集群外不能直接访问。我们先使用 `kubectl` 提供的 `port-forward` 功能进行访问。

```
master $ kubectl -n kube-system port-forward pod/kubernetes-dashboard-67896bc598-dhdpz 8443
Forwarding from 127.0.0.1:8443 -> 8443
Forwarding from [::1]:8443 -> 8443
```



#### 外部访问

需要生成证书：

```
[root@192.168.18.196 dashboard]#grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.crt
[root@192.168.18.196 dashboard]#ls
kubecfg.crt
[root@192.168.18.196 dashboard]#vim kubecfg.crt 
[root@192.168.18.196 dashboard]#grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.key
[root@192.168.18.196 dashboard]#
[root@192.168.18.196 dashboard]#ls
kubecfg.crt  kubecfg.key
[root@192.168.18.196 dashboard]#openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"
Enter Export Password:
Verifying - Enter Export Password:
[root@192.168.18.196 dashboard]#ls
kubecfg.crt  kubecfg.key  kubecfg.p12
[root@192.168.18.196 dashboard]#sz kubecfg.p12
```

把kubecfg.p12放到访问机上打开，重新打开浏览器

开启：

1. port-forward 方式

   `kubectl -n kube-system port-forward --address='0.0.0.0' pod/kubernetes-dashboard-576695b89b-mmkks 8443`

2. kubectl proxy

   启动代理只需执行如下命令：

   ```
   $ kubectl proxy
   Starting to serve on 127.0.0.1:8001
   ```

   我们也可以使用`--address`和`--accept-hosts`参数来允许外部访问：

   ```
   kubectl proxy --address='0.0.0.0'  --accept-hosts='^*$' 8443
   ```

3. Node port

   NodePort是将节点直接暴露在外网的一种方式，只建议在开发环境，单节点的安装方式中使用。

   

```
[root@192.168.18.196 saythx_k8s]#kubectl cluster-info
Kubernetes master is running at https://192.168.18.196:6443
Heapster is running at https://192.168.18.196:6443/api/v1/namespaces/kube-system/services/heapster/proxy
KubeDNS is running at https://192.168.18.196:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
monitoring-grafana is running at https://192.168.18.196:6443/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
monitoring-influxdb is running at https://192.168.18.196:6443/api/v1/namespaces/kube-system/services/monitoring-influxdb/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```





### token

浏览器能打开后，需要我慢输入token

```
[root@192.168.18.196 home]#kubectl -n kube-system get serviceaccount -l k8s-app=kubernetes-dashboard -o yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: ServiceAccount
  ...
  secrets:
  - name: kubernetes-dashboard-token-75mvt
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""
[root@192.168.18.196 home]#kubernetes-dashboard-token-75mvt kubernetes-dashboard-token-75mvt
-bash: kubernetes-dashboard-token-75mvt: command not found
[root@192.168.18.196 home]#kubectl -n kube-system describe secrets kubernetes-dashboard-token-75mvt
Name:         kubernetes-dashboard-token-75mvt
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: kubernetes-dashboard
              kubernetes.io/service-account.uid: aeb7678a-64de-11e9-8400-801844f349cc

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImt...
```

或一句：

```
[root@192.168.18.196 dashboard]#kubectl create -f admin-user-role-binding.yaml
clusterrolebinding.rbac.authorization.k8s.io/admin-user created
[root@192.168.18.196 dashboard]#kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
Name:         admin-user-token-4sbm7
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: admin-user
              kubernetes.io/service-account.uid: 250e5386-64ee-11e9-8400-801844f349cc

Type:  kubernetes.io/service-account-token

Data
====
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJu...
ca.crt:     1025 bytes
namespace:  11 bytes
```



### 跳过token

Dashboard 支持 Kubeconfig 和 Token 两种认证方式，为了简化配置，我们通过配置文件 dashboard-admin.yaml 为 Dashboard 默认用户赋予 admin 权限。

```
[root@ken ~]# cat dashboard-admin.yml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
  labels: 
     k8s-app: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard
  namespace: kube-system
```

执行kubectl apply使之生效

```
[root@ken ~]# kubectl apply -f dashboard-admin.yml
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
```

登录时点击跳过即可。



### 添加用户

进去后很多资源没有权限访问，我们需要添加一个账户。



**创建服务账号**

利用`vi admin-user.yaml`命令创建admin-user.yaml文件，输入以下内容,来创建admin-user的服务账号，放在kube-system名称空间下：

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
```

输入命令`kubectl create -f admin-user.yaml`来执行。

**绑定角色**

利用`vi admin-user-role-binding.yaml`命令创建admin-user-role-binding.yaml文件，输入以下内容,来进行绑定

```
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```



### 集成Heapster

eapster是容器集群监控和性能分析工具，天然的支持Kubernetes和CoreOS。

Heapster支持多种储存方式，本示例中使用`influxdb`，直接执行下列命令即可：

```
kubectl create -f http://mirror.faasx.com/kubernetes/heapster/deploy/kube-config/influxdb/influxdb.yaml
kubectl create -f http://mirror.faasx.com/kubernetes/heapster/deploy/kube-config/influxdb/grafana.yaml
kubectl create -f http://mirror.faasx.com/kubernetes/heapster/deploy/kube-config/influxdb/heapster.yaml
kubectl create -f http://mirror.faasx.com/kubernetes/heapster/deploy/kube-config/rbac/heapster-rbac.yaml
```

> 上面命令中用到的yaml是从 <https://github.com/kubernetes/heapster/tree/master/deploy/kube-config/influxdb> 复制的，并将`k8s.gcr.io`修改为国内镜像。

然后，查看一下Pod的状态：

```
raining@raining-ubuntu:~/k8s/heapster$ kubectl get pods --namespace=kube-system
NAME                                      READY     STATUS    RESTARTS   AGE
...
heapster-5869b599bd-kxltn                 1/1       Running   0          5m
monitoring-grafana-679f6b46cb-xxsr4       1/1       Running   0          5m
monitoring-influxdb-6f875dc468-7s4xz      1/1       Running   0          6m
...
```

等待状态变成`Running`，刷新一下浏览器