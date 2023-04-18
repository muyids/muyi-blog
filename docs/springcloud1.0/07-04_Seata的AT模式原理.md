### **Seata 的三大角色**

**TC (Transaction Coordinator) - 事务协调者**

维护全局和分支事务的状态，驱动全局事务提交或回滚。

**TM (Transaction Manager) - 事务管理器**

定义全局事务的范围：开始全局事务、提交或回滚全局事务。

**RM (Resource Manager) - 资源管理器**

管理分支事务处理的资源，与 TC 交谈以注册分支事务和报告分支事务的状态，并驱动分支事务提交或回滚。

_其中，TC 为单独部署的 Server 服务器，TM 和 RM 是嵌入到应用中的 Client 客户端_

**三大角色交互模型**

![68747470733a2f2f63646e2e6e6c6](https://muyids.oss-cn-beijing.aliyuncs.com/68747470733a2f2f63646e2e6e6c6.png)

**Seata 托管分布式事务的典型生命周期**

1. TM 要求 TC 开始一个新的全局事务。TC 生成代表全局事务的 XID。
2. XID 通过微服务的调用链传播。
3. RM 将本地事务作为 XID 对应的全局事务的一个分支注册到 TC。
4. TM 请求 TC 提交或回滚 XID 对应的全局事务。
