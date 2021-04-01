---
title: "Helm3.md"
date: 2021-01-02 09:58:51 +0800
lastmod: 2021-01-02 09:58:51 +0800
draft: false
tags: [""]
categories: ["k8s"]
author: "Claymore"

---

## Helm 3

Helm 2 是 C/S 架构，主要分为客户端 helm 和服务端 Tiller; 与v2版本不同，v3移除了Tiller，只有 helm。

Tiller 主要用于在 Kubernetes 集群中管理各种应用发布的版本，**在 Helm 3 中移除了 Tiller**, 版本相关的数据直接存储在了 Kubernetes 中。

这样更简单安全。

简单来说， Helm 就是 Kubernetes 的应用程序包管理器， 类似于 Linux 系统之上的 yum 或 apt-get 等， 可用于实现帮助用户查找、 分享及使用 Kubernetes 应用程序，目前的版本 由 CNCF ( Microsoft、 Google、 Bitnami 和 Helm 社区）维护。 

它的核心打包功能组件称为 chart，可以帮助用户创建、安装及升级复杂应用。 Helm 将 Kubernetes 的资源（如 Deployments、 Servic巳s 或 ConfigMap 等） 打包到 一 个 Charts 中，制作并测试完成的各个 Charts 将保存到 Charts 仓库进行存储和分发。 另外，Helm 实现了可配置的发布，它支持应用配置的版本管理，简化了 Kubemetes 部署应用的版 本控制、打包、 发布 、 删除和更新等操作。

helm和yum一样也有源（repo）、包的概念：

- chart：类似于yum的rpm包，里面定义了部署资源以及一些依赖的信息（deployment，service等）。和rpm包作用上类似，我们需要部署那些服务，按照格式定义好就行了。
- repo：类似于yum源，helm也有自己的源，存放chart。
- Release：chart部署到k8s后自己的唯一标识.



部署还是一样，下载helm3的二进制文件，放到环境变量里，如/usr/local/bin/

``` sh
# tar xzf helm-v3.4.1-linux-amd64.tar.gz
# ls
helm-v3.4.1-linux-amd64.tar.gz  linux-amd64
# ls linux-amd64/
helm  LICENSE  README.md
# 命令补全： 在~/.bashrc追加
source <(helm completion bash)
```



### 初始化

当安装好了Helm之后，您可以添加一个chart 仓库。 一个常见的选择是添加Helm的官方仓库：

```sh
$ helm repo add stable https://charts.helm.sh/stable

# 其它常用仓库：
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com/
```



当添加完成，您将可以看到可以被您安装的charts列表：

helm search：可以用于搜索**两种不同类型的源。**

helm search hub：搜索 Helm Hub，该源包含来自许多不同仓库的Helm chart。

helm search repo：搜索已添加到本地头helm客户端（带有helm repo add）的仓库，该搜索是通过本地数据完成的，不需要连接公网。

```sh
helm search hub			#可搜索全部可用chart
helm search hub wordpress

# helm search repo stable
NAME                                    CHART VERSION   APP VERSION                     DESCRIPTION
stable/acs-engine-autoscaler            2.2.2           2.1.1                           DEPRECATED Scales worker nodes within agent pools
stable/aerospike                        0.2.8           v4.5.0.5                        A Helm chart for Aerospike in Kubernetes
stable/airflow                          4.1.0           1.10.4                          Airflow is a platform to programmatically autho...
stable/ambassador                       4.1.0           0.81.0                          A Helm chart for Datawire Ambassador
```



### repo

``` sh
# helm repo list
Error: no repositories to show

# 添加一个仓库
helm repo add falcosecurity https://falcosecurity.github.io/charts
"falcosecurity" has been added to your repositories
# helm repo list
NAME            URL
falcosecurity   https://falcosecurity.github.io/charts

# 更新repo的chart
# helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "falcosecurity" chart repository
Update Complete. ⎈Happy Helming!⎈

# helm search repo falcosecurity  添加后的搜索
NAME                            CHART VERSION   APP VERSION     DESCRIPTION
falcosecurity/falco             1.5.4           0.26.2          Falco
falcosecurity/falco-exporter    0.3.8           0.3.0           Prometheus Metrics Exporter for Falco output ev...
falcosecurity/falcosidekick     0.1.29          2.15.0          A simple daemon to help you with falco's outputs

# helm repo remove falcosecurity		#移除repo
```



### release

``` sh
# 安装
helm install stable/mysql --generate-name 

# 查看, ls=list
$ helm ls
NAME             VERSION   UPDATED                   STATUS    CHART
smiling-penguin  1         Wed Sep 28 12:59:46 2016  DEPLOYED  mysql-0.1.0

# 卸载 
helm uninstall smiling-penguin

# 状态
$ helm status smiling-penguin
Status: UNINSTALLED
```





## 模板文件

chart里一个很重要的概念就是模板（template）,它就是Go语言模板，它是里面加入了编程逻辑的k8s文件。这些模板文件在使用时都要先进行模板解析，把其中的程序逻辑转化成对应的编码，最终生成k8s配置文件。

### create

``` sh
# helm create k8s-demo
Creating k8s-demo

# tree k8s-demo/
k8s-demo/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml

3 directories, 10 files
```

其中“k8sdemo”是chart的名字，这个名字很重要，服务的名字和label都是由它产生的。

上就是Helm自动生成的chart目录结构，在Helm里每个项目叫一个chart，它由下面几个组成部分：

- **"Chart.yaml"**：存有这个chart的基本信息，
- **"values.yaml"**：定义模板中要用到的常量。
- **“template”目录**：里面存有全部的模板文件，
  - 其中最重要的是“deployment.yaml”和“service.yaml”，部署和服务文件. "helpers.tpl"用来定义变量
  - "ingress.yaml"和"serviceaccount.yaml"分别是对外接口和服务账户，这里暂时没用， “NOTES.txt”是注释文件。
- **“charts”目录**: 存有这个chart依赖的所有子chart。



### values.yaml

这个文件定义了常量，常量的值在其他模板中可以 引用。

create 后默认的 values.yaml 内容：

``` yaml
# Default values for k8s-demo.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths: []
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
```



比如其中的 replicaCount: 1， 我们看下 templates/deployment.yaml 中它的使用：

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "k8s-demo.fullname" . }}
  labels:
    {{- include "k8s-demo.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}  # 注意这里
  {{- end }}
  selector:
    matchLabels:
      {{- include "k8s-demo.selectorLabels" . | nindent 6 }}
```



### _helpers.tpl

``` 
{{- define "k8s-demo.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
```



## 实战

###  改编一个 mongo chart

``` sh
# 先创建模板
helm create tc-mongo
```

改 values.yaml:

``` yaml

replicaCount: 1

image:
  repository: docker-hub.cloud.top/vsp/dsec/tc-mongo
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion, 这里是镜像tag，不填默认为最新版本，注意不是latest
  tag: "latest"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # 注意这里，关闭了serviceAccount
  create: false
  annotations: {}
  name: ""

podAnnotations: {}
podSecurityContext: {}

securityContext: {}

service:
  type: NodePort
  port: 27017
  nodePort: 32017
```

改 vim templates/service.yaml：

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "tc-mongo.fullname" . }}
  labels:
    {{- include "tc-mongo.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      nodePort: {{ .Values.service.nodePort }}   # 加了这行
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "tc-mongo.selectorLabels" . | nindent 4 }}

```

尝试安装：

``` sh
# helm install ./tc-mongo/
Error: must either provide a name or specify --generate-name

# helm install ./tc-mongo/ --generate-name
NAME: tc-mongo-1617102253
LAST DEPLOYED: Tue Mar 30 19:04:21 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services topsec-mongo-1617102253)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT

# kubectl get pods -A
NAMESPACE        NAME                                       READY   STATUS             RESTARTS   AGE
default          tc-mongo-1617102253-7fbc8d8bf8-lgfkr   0/1     ErrImagePull       0          36s


# helm list
NAME                    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
tc-mongo-1617102253 default         1               2021-03-30 19:04:21.752675783 +0800 CST deployed        tc-mongo-0.1.0      1.16.0

#helm uninstall tc-mongo-1617102253
release "tc-mongo-1617102253" uninstalled
```

有几个问题：

1. --generate-name 和 name 的关系，和values.yaml 中的 nameOverride ，fullnameOverride 关系，
2. 指定名字空间
3. 指定运行的node, 别的node上有该mongo的镜像，无需拉取。



#### 名字空间的指定

在 Helm 3 中，则必须主动指定release名称：  --name-template，或者增加 `--generate-name` 的参数自动生成。 fullnameOverride 会声明 pods 的名称，nameOverride 没有看到相关作用。https://stackoverflow.com/questions/63838705/what-is-the-difference-between-fullnameoverride-and-nameoverride-in-helm

可以通过 --namespace 来制定安装的名字空间，通过 --create-namespace 创建新的名字空间

fullnameOverride 指定的是pod的名称，如果没有该名称，那么 pod 名称会是 version name + name 的组合：

``` sh
helm install tc-mongo/ --namespace=tc --name-template=mongo-version
# kubectl get pods -n topsec
NAME                                    READY   STATUS             RESTARTS   AGE
mongo-version-tc-mongo-fff7cc4b9-5z4z8   0/1     CrashLoopBackOff   286        19h
```





#### 指定该pod的运行位置

修改 values.ya

``` yaml
# tolerations: []
tolerations:
  - key: node-role.kubernetes.io/master
    effect: NoSchedule
```

这里我们允许了 该pod 可以在master node上运行，再次helm install，我们可以观察到 该pod确实跑到了master,

那我们如何指定节点运行呢？

在helm之前我们可以通过nodeName 来选择，

nodeName是节点选择约束的最简单形式，但是由于其限制，通常很少使用它。nodeName是PodSpec的领域。

pod.spec.nodeName将Pod直接调度到指定的Node节点上，会【跳过Scheduler的调度策略】，该匹配规则是【强制】匹配。可以越过Taints污点进行调度。

nodeName用于选择节点的一些限制是：

- 如果指定的节点不存在，则容器将不会运行，并且在某些情况下可能会自动删除。
- 如果指定的节点没有足够的资源来容纳该Pod，则该Pod将会失败，并且其原因将被指出，例如OutOfmemory或OutOfcpu。
- 云环境中的节点名称并非总是可预测或稳定的。



所以我们使用 nodeSelector 来决定 pod 的运行位置，使用nodeSelector我们需要先给node打label:

``` sh
kubectl label nodes node201 nodeN=201
node/node201 labeled
root@node200:~# kubectl get nodes --show-labels
NAME      STATUS   ROLES    AGE    VERSION   LABELS
node200   Ready    master   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node200,kubernetes.io/os=linux,node-role.kubernetes.io/master=
node201   Ready    <none>   134d   v1.17.4   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node201,kubernetes.io/os=linux,nodeN=201
```

node201被打上了 nodeN=201 的label. 我们在 values.yaml 使用它：

``` yaml
# nodeSelector: {}
nodeSelector:
  nodeN: "201"
```

此时 pod 也跑到了 node201 上:

``` sh
# kubectl get pods -n topsec -o wide
NAME                          READY  STATUS                         NODE      NOMINATED NODE   
mongo-version-tc-mongo-fff7cc4b9-5z4z8   0/1     CrashLoopBackOff   286        ode201   
```

