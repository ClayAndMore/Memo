Tags:[k8s]

官方提供了 CLI 工具 `kubectl` 用于完成大多数集群管理相关的功能。当然凡是你可以通过 `kubectl`完成的与集群交互的功能，都可以直接通过 API 完成。

一般的用法 `kubectl [flags] [options]` 



在我们的用户家目录，可以看到一个名为 `.kube/config` 的配置文件，主要包含

- K8S 集群的 API 地址
- 用于认证的证书地址



### get

kubectl get nodes, 可以获得集群信息

如果我们想要看到更详细的信息呢？可以通过传递 `-o` 参数以得到不同格式的输出。

```
➜  ~ kubectl get nodes -o wide 
NAME       STATUS    ROLES     AGE       VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE            KERNEL-VERSION   CONTAINER-RUNTIME
minikube   Ready     master    2d        v1.11.3   10.0.2.15     <none>        Buildroot 2018.05   4.15.0           docker://17.12.1-ce
```

当然也可以传递 `-o yaml` 或者 `-o json` 得到更加详尽的信息。

使用 `-o json` 将内容以 JSON 格式输出时，可以配合 [`jq`](https://link.juejin.im/?target=https%3A%2F%2Fstedolan.github.io%2Fjq%2F) 进行内容提取。例如：

```
➜  ~ kubectl get nodes -o json | jq ".items[] | {name: .metadata.name} + .status.nodeInfo"
{
  "name": "minikube",
  "architecture": "amd64",
  "bootID": "d675d75b-e58e-40db-8910-6e5dda9e7cf9",
  "containerRuntimeVersion": "docker://17.12.1-ce",
  "kernelVersion": "4.15.0",
  "kubeProxyVersion": "v1.11.3",
  "kubeletVersion": "v1.11.3",
  "machineID": "078e2d22629747178397e29cf1c96cc7",
  "operatingSystem": "linux",
  "osImage": "Buildroot 2018.05",
  "systemUUID": "4073906D-69A1-46EE-A08C-0252D9F79893"
}
```



### run

```
Usage:
  kubectl run NAME --image=image [--env="key=value"] [--port=port] [--replicas=replicas] [--dry-run=bool] [--overrides=inline-json] [--command] -- [COMMAND] [args...] [options]
```

`NAME` 和 `--image` 是必需项。分别代表此次部署的名字及所使用的镜像，其余部分之后进行解释。当然，在我们实际使用时，推荐编写配置文件并通过 `kubectl create` 进行部署。

eg:  部署redis 实例
