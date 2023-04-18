```
初级 k8s 是玩 Deploy,  入门级别是玩 Ingress, 中级的玩 helm & pv, 中高级玩 Operator & CRD,  高级的玩网络&源码，给大家一个渐进学习的思路。
```

# 生成 yaml 原则

- 不要写 yaml , 去生成
- 使用 `--dry-run=client -o yaml > my.yaml`作为 `kubectl run` 的参数去生成

# 校验 yaml 工具

https://learnk8s.io/validating-kubernetes-yaml

TL;DR:

1、Kubeval
2、Kube-score
3、Config-lint
4、Copper
5、Conftest
6、Polaris
