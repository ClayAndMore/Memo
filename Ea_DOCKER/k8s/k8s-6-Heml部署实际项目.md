### Heml Chart

上节我们解释过 `chart` 的含义，现在我们要将项目使用 Helm 部署，那么首先，我们需要创建一个 `chart`。

#### Chart 结构

在我们项目的根目录下，通过以下命令创建一个 `chart`。

```
[root@192.168.18.196 helm_test]#helm create saythx
Creating saythx
[root@192.168.18.196 helm_test]#tree -a saythx/
saythx/
├── charts
├── Chart.yaml
├── .helmignore
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   └── service.yaml
└── values.yaml

2 directories, 8 files
```



* Chart.yaml

    ```
    [root@192.168.18.196 helm_test]#cat saythx/Chart.yaml 
    apiVersion: v1
    appVersion: "1.0"
    description: A Helm chart for Kubernetes
    name: saythx
    version: 0.1.0
    ```
    
    这个文件是每个 `chart` 必不可少的一个文件，其中包含着几个重要的属性，如：

    - `apiVersion`：目前版本都为 `v1`
    - `appVersion`：这是应用的版本号，需要与 `apiVersion`， `version` 等字段注意区分
    - `name`: 通常要求 `chart` 的名字必须和它所在目录保持一致，且此字段必须
    - `version`：表明当前 `chart` 的版本号，会直接影响 `Release` 的记录，且此字段必须
    - `description`：描述

* charts

  `charts` 文件夹是用于存放依赖的 `chart` 的。当有依赖需要管理时，可添加 `requirements.yaml` 文件，可用于管理项目内或者外部的依赖。

* .helmignore

    `.helmignore` 类似于 `.gitignore` 和 `.dockerignore` 之类的，用于忽略掉一些不想包含在 `chart` 内的文件。

* templates

    `templates` 文件夹内存放着 `chart` 所使用的模板文件，也是 `chart` 的实际执行内容。在使用 `chart`进行安装的时候，会将 下面介绍的 `values.yaml` 中的配置项与 `templates` 中的模板进行组装，生成最终要执行的配置文件。

    `templates` 中，推荐命名应该清晰，如 `xx-deployment.yaml`，中间使用 `-` 进行分割，避免使用驼峰式命名。

    `Notes.txt` 文件在 `helm install` 完成后，会进行回显，可用于解释说明如何访问服务等。

* values.yaml

    `values.yaml` 存放着项目的一些可配置项，如镜像的名称或者 tag 之类的。作用就是用于和模板进行组装。



#### 编写chart

Chart.yaml

```yaml
apiVersion: v1
appVersion: "1.0"
description: A Helm chart SayThx
name: saythx
version: 0.1.0
maintainers:
    -name: Claymore
```

添加 `maintainers` 字段，表示维护者。

values.yaml

```yaml
# Default values for saythx.

# backend is the values for backend
backend:
  image: claymore94/saythx-be
  tag: "lastest"
  pullPolicy: IfNotPresent
  replicas: 1

# frontend is the values for frontend
frontend:
  image: claymore94/saythx-fe
  tag: "lastest"  # tag: "1.0"
  pullPolicy: IfNotPresent
  replicas: 1

# work is the values for work
work:
  image: claymore94/saythx-work
  tag: "lastest"
  pullPolicy: IfNotPresent
  replicas: 1

# redis is the values for redis
redis:
  image: redis
  tag: 5
  pullPolicy: IfNotPresent
  replicas: 1

# namespace is the values for deploy namespace
namespace: work_helm

# service.type is the values for service type
service:
  type: NodePort
```

定义了我们预期哪些东西是可配置的，比如 `namespace` 以及镜像名称 tag 等



#### 模板化

之前写的各种deployment.yaml 和 service.yaml 模板化：

backend-deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: backend
  name: saythx-backend
  namespace: {{ .Values.namespace }}
spec:
  selector:
    matchLabels:
      app: backend
  replicas: 1
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - env:
        - name: REDIS_HOST
          value: saythx-redis
        image: {{ .Values.backend.image }}:{{ .Values.backend.tag }}
        name: backend
        ports:
        - containerPort: 8080
```



backend-service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: backend
  name: saythx-backend
  namespace: {{ .Values.namespace }}
spec:
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
  selector:
    app: backend
  type: {{ .Values.service.type }}
```



namespace.yaml:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {{ .Values.namespace }}
```



tree saythx/templates:

```
saythx/templates/
├── backend-deployment.yaml
├── backend-service.yaml
├── frontend-deployment.yaml
├── frontend-service.yaml
├── _helpers.tpl
├── namespace.yaml
├── NOTES.txt
├── redis-deployment.yaml
├── redis-service.yaml
└── work-deployment.yaml
```



NOTES.txt:

```
1. Get the application URL by running these commands:
{{- if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Values.namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services saythx-frontend)
  export NODE_IP=$(kubectl get nodes --namespace {{ .Values.namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "ClusterIP" .Values.service.type }}
  export POD_NAME=$(kubectl get pods --namespace {{ .Values.namespace }} -l "app=frontend" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Values.namespace }} port-forward $POD_NAME 8080:80
{{- end }}
```

上面这是 `NOTES.txt` 文件内的内容。 这些内容会在 `helm install` 执行成功后显示在终端，用于说明服务如何访问或者其他注意事项等。





### 直接部署

```
[root@192.168.18.196 helm_test]#helm install --set name=mycharts ./saythx/
NAME:   manageable-umbrellabird
LAST DEPLOYED: Mon Apr 15 11:25:03 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME             READY  UP-TO-DATE  AVAILABLE  AGE
saythx-backend   0/1    1           0          0s
saythx-frontend  0/1    1           0          0s
saythx-redis     0/1    1           0          0s
saythx-work      0/1    1           0          0s

==> v1/Namespace
NAME       STATUS  AGE
work-helm  Active  0s

==> v1/Pod(related)
NAME                              READY  STATUS             RESTARTS  AGE
saythx-backend-7cf4f96c7d-r77dz   0/1    ContainerCreating  0         0s
saythx-frontend-5c96646685-dtm2b  0/1    ContainerCreating  0         0s
saythx-redis-75f8d49554-j6mdc     0/1    ContainerCreating  0         0s
saythx-work-57bd4f85b6-pn47m      0/1    ContainerCreating  0         0s

==> v1/Service
NAME             TYPE      CLUSTER-IP      EXTERNAL-IP  PORT(S)         AGE
saythx-backend   NodePort  10.100.215.148  <none>       8080:31904/TCP  0s
saythx-frontend  NodePort  10.110.166.49   <none>       80:31552/TCP    0s
saythx-redis     NodePort  10.103.183.93   <none>       6379:30921/TCP  0s


NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace work-helm -o jsonpath="{.spec.ports[0].nodePort}" services saythx-frontend)
  export NODE_IP=$(kubectl get nodes --namespace work-helm -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```



### 访问服务

前面在部署完成后，有一些返回信息，我们来按照其内容访问我们的服务：

```
➜  saythx export NODE_PORT=$(kubectl get --namespace work -o jsonpath="{.spec.ports[0].nodePort}" services saythx-frontend)
➜  saythx export NODE_IP=$(kubectl get nodes --namespace work -o jsonpath="{.items[0].status.addresses[0].address}")
➜  saythx echo http://$NODE_IP:$NODE_PORT
http://172.17.0.5:30300
➜  saythx curl http://172.17.0.5:30300
```

服务可以正常访问。



