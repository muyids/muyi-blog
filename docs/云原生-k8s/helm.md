# Helm 安装 mysql

## Helm search: 查找 Charts

- `helm search hub` 从 [Artifact Hub](https://artifacthub.io/) 中查找并列出 helm charts。 Artifact Hub 中存放了大量不同的仓库。
- `helm search repo` 从你添加（使用 `helm repo add`）到本地 helm 客户端中的仓库中进行查找。该命令基于本地数据进行搜索，无需连接互联网。

```
 helm search repo mysql
```

​

## 'helm install'：安装一个 helm 包

```
 helm install dw-mysql bitnami/mysql
```

### _安装前自定义 chart_

helm show values 查看 chart 可配置选项

输出到 yaml 文件中

```
 helm show values bitnami/mysql --debug > mysql.yaml
```

修改 mysql.yaml，使用自定义配置 安装

```

 helm install -f mysql.yaml dw-mysql bitnami/mysql
```

安装过程中有两种方式传递配置数据：

- `--values` (或 `-f`)：使用 YAML 文件覆盖配置。可以指定多次，优先使用最右边的文件。
- `--set`：通过命令行的方式对指定项进行覆盖。

### 更新

```
helm upgrade -f bitnami/mysql/values.yaml dw-mysql bitnami/mysql
```

### 更多安装方法

`helm install` 命令可以从多个来源进行安装：

- chart 的仓库（如上所述）
- 本地 chart 压缩包（`helm install foo foo-0.1.1.tgz`）
- 解压后的 chart 目录（`helm install foo path/to/foo`）
- 完整的 URL（`helm install foo https://example.com/charts/foo-1.2.3.tgz`）

### Helm rollback 回滚 release 版本

每当发生了一次安装、升级或回滚操作，revision 的值就会加 1。第一次 revision 的值永远是 1。

回滚到 最初版本：

```
helm rollback dw-mysql 1
```

### helm history 查看历史版本

```
helm history dw-mysql
```

## helm status 查看 release 状态

```
helm status dw-mysql
```

## 'helm uninstall'：卸载 release

```
helm uninstall dw-mysql
```

`helm list` 命令看到当前部署的所有 release

`helm list --all` 会展示 Helm 保留的所有 release 记录，包括失败或删除的条目（指定了 `--keep-history`）

# 创建自己的 charts

## helm create 初始化模板项目

```
$ helm create deis-workflow
Creating deis-workflow
```

### `helm lint`

在编辑 chart 时，可以通过 `helm lint` 验证格式是否正确。

### `helm package`

当准备将 chart 打包分发时，你可以运行 `helm package` 命令：

### helm install

```
helm install deis-workflow ./deis-workflow-0.1.0.tgz
```

# 二次开发 已有的 charts

## helm pull 拉取已有 charts 到本地

从仓库下载并（可选）在本地目录解压

```
helm pull bitnami/mysql --untar
```

## 修改 values.yaml 文件

## Helm template 编译成 k8s-all.yaml

```
helm template bitnami/mysql > target/mysql-all.yaml
```

​

## kubectl-slice 分解 k8s-all.yaml

```
kubectl-slice -f target/mysql-all.yaml -o target/mysql
```

## kubectl apply 部署调试

按照 helm 的部署顺序手动部署 分解出来的 k8s 组件

[Helm 按照以下顺序安装资源：](https://helm.sh/zh/docs/intro/using_helm/)

- Namespace
- NetworkPolicy
- ResourceQuota
- LimitRange
- PodSecurityPolicy
- PodDisruptionBudget
- ServiceAccount
- Secret
- SecretList
- ConfigMap
- StorageClass
- PersistentVolume
- PersistentVolumeClaim
- CustomResourceDefinition
- ClusterRole
- ClusterRoleList
- ClusterRoleBinding
- ClusterRoleBindingList
- Role
- RoleList
- RoleBinding
- RoleBindingList
- Service
- DaemonSet
- Pod
- ReplicationController
- ReplicaSet
- Deployment
- HorizontalPodAutoscaler
- StatefulSet
- Job
- CronJob
- Ingress
- APIService
