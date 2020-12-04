## Helm 3

Helm 2 是 C/S 架构，主要分为客户端 helm 和服务端 Tiller; 与v2版本不同，v3移除了Tiller，只有 helm。

Tiller 主要用于在 Kubernetes 集群中管理各种应用发布的版本，**在 Helm 3 中移除了 Tiller**, 版本相关的数据直接存储在了 Kubernetes 中。

这样更简单安全。

简单来说， Helm 就是 Kubernetes 的应用程序包管理器， 类似于 Linux 系统之上的 yum 或 apt-get 等， 可用于实现帮助用户查找、 分享及使用 Kubernetes 应用程序，目前的版本 由 CNCF ( Microsoft、 Google、 Bitnami 和 Helm 社区）维护。 

它的核心打包功能组件称为 chart，可以帮助用户创建、安装及升级复杂应用。 Helm 将 Kubernetes 的资源（如 Deployments、 Servic巳s 或 ConfigMap 等） 打包到 一 个 Charts 中，制作并测试完成的各个 Charts 将保存到 Charts 仓库进行存储和分发。 另外，Helm 实现了可配置的发布，它支持应用配置的版本管理，简化了 Kubemetes 部署应用的版 本控制、打包、 发布 、 删除和更新等操作。



部署还是一样，下载helm3的二进制文件，放到环境变量里，如/usr/local/bin/

``` sh
# tar xzf helm-v3.4.1-linux-amd64.tar.gz
# ls
helm-v3.4.1-linux-amd64.tar.gz  linux-amd64
# ls linux-amd64/
helm  LICENSE  README.md
```



### 初始化

当安装好了Helm之后，您可以添加一个chart 仓库。 一个常见的选择是添加Helm的官方仓库：

```fallback
$ helm repo add stable https://charts.helm.sh/stable
```



当添加完成，您将可以看到可以被您安装的charts列表：

helm search：可以用于搜索**两种不同类型的源。**

helm search hub：搜索 Helm Hub，该源包含来自许多不同仓库的Helm chart。

helm search repo：搜索已添加到本地头helm客户端（带有helm repo add）的仓库，该搜索是通过本地数据完成的，不需要连接公网。

```sh
helm search hub			#可搜索全部可用chart
helm search hub wordpress
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





## 实战

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



#### values.yaml

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



