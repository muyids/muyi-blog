本文参考[在生产环境中使用 Sentinel](https://github.com/alibaba/Sentinel/wiki/%E5%9C%A8%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E4%B8%AD%E4%BD%BF%E7%94%A8-Sentinel)

**规则推送的三种模式**

##### 一、原始模式

- API 将规则推送至客户端并直接更新到内存中
- 扩展写数据源（[`WritableDataSource`](https://github.com/alibaba/Sentinel/wiki/动态规则扩展)）
- 重启消失

##### 二、Pull 模式

- 客户端主动向某个规则管理中心定期轮询拉取规则，这个规则中心可以是 RDBMS、文件 等
- 扩展写数据源（[`WritableDataSource`](https://github.com/alibaba/Sentinel/wiki/动态规则扩展)）
- 规则持久化，不保证一致性，不保证高可用

##### 三、Push 模式

- **规则中心统一推送**，客户端通过注册监听器的方式时刻监听变化，比如使用 Nacos、Zookeeper 等配置中心
- 扩展读数据源（[`ReadableDataSource`](https://github.com/alibaba/Sentinel/wiki/动态规则扩展)）
- **生产环境下一般采用 push 模式的数据源**

**配置 Nacos 动态数据源**

application.yml

```yaml
spring:
  application:
    name: stock-service
sentinel:
  transport:
    port: 8719
    dashboard: localhost:8080
  datasource:
    ds:
      nacos:
        server-addr: localhost:8848
        dataId: ${spring.application.name}-sentinel
        groupId: DEFAULT_GROUP
        rule-type: flow
```

nacos 控制台增加配置 dataId: stock-service-sentinel，groupId: DEFAULT_GROUP；配置格式选 json

```json
[
  {
    "resource": "StockReduce",
    "limitApp": "default",
    "grade": 1,
    "count": 2,
    "stategy": 0,
    "controlBehavior": 0,
    "clusterMode": false
  }
]
```

配置规则是一个数组类型，数组中的每个对象是针对每一个保护资源的配置对象，每个对象中的属性解释如下：

- resource：资源名，即限流规则的作用对象
- limitApp：流控针对的调用来源，若为 default 则不区分调用来源
- grade：限流阈值类型（QPS 或并发线程数）；`0`代表根据并发数量来限流，`1`代表根据 QPS 来进行流量控制
- count：限流阈值
- strategy：调用关系限流策略
- controlBehavior：流量控制效果（直接拒绝、Warm Up、匀速排队）
- clusterMode：是否为集群模式

启动应用后，请求流控资源的访问 url，正常的话可以在 sentinel 控制台中的流控规则中找到配置的流控规则

需要注意的是当前版本的 Sentinel 控制台不具备同步修改 Nacos 配置的能力，而 Nacos 由于可以通过在客户端中使用 Listener 来实现自动更新。所以，在整合了 Nacos 做规则存储之后，需要知道在下面两个地方修改存在不同的效果：

- Sentinel 控制台中修改规则：仅存在于服务的内存中，不会修改 Nacos 中的配置值，重启后恢复原来的值。
- Nacos 控制台中修改规则：服务的内存中规则会更新，Nacos 中持久化规则也会更新，重启后依然存在。
