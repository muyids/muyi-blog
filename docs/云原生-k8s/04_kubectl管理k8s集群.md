# Kubectl 本地连接 k8s 集群

## 安装 kubectl

macOS 下直接使用 homebrew 管理工具进行安装：

> $ brew install kubernetes-cli

确认是否安装成功：

> $ kubectl version

## 配置

通过`kubectl config xxx`指令配置三部分内容。

### 设置集群信息

```
# 配置集群名称与服务地址
kubectl config --kubeconfig=${HOME}/.kube/config set-cluster cluster-name --server=https://xxx/k8s/clusters/c-f22sq --insecure-skip-tls-verify
```

### 设置用户信息,用户连接集群

```
# 设置一个管理 标识为 k8s-cluster ，并设置访问凭证。此处使用 用户名-密码 的验证方式
kubectl config --kubeconfig=${HOME}/.kube/config set-credentials k8s-cluster --username=ml --password=CiKB3gzcfC0LkoSPEP&Ty

kubectl config --kubeconfig=${HOME}/.kube/config set-credentials k8s-cluster --client-certificate=fake-cert-file --client-key=fake-key-seefile

```

### 设置 context 信息, 用于建立用户和集群的关系.

```
# 设置一个名为 k8s-cluster 的配置，使用 cluster-name 集群与 k8s-cluster 用户的上下文
kubectl config --kubeconfig=${HOME}/.kube/config set-context k8s-cluster --cluster=ali-yinli-k8s --namespace=ml --user=ml
```

### 切换默认的 context

```
# 启用 k8s-cluster  为默认上下文
kubectl config --kubeconfig=${HOME}/.kube/config use-context k8s-cluster
```

### 删除信息相关操作

```
要删除用户，可以运行 kubectl --kubeconfig=${HOME}/.kube/config config unset users.<name>
要删除集群，可以运行 kubectl --kubeconfig=${HOME}/.kube/config config unset clusters.<name>
要删除上下文，可以运行 kubectl --kubeconfig=${HOME}/.kube/config config unset contexts.<name>
```

## 配置文件地址(可以直接修改)

```
${USER_HOME}/.kube/config
```
