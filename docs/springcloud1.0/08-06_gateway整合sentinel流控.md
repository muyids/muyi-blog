网关作为内部系统外的一层屏障，对内起到一定的保护作用，限流便是其中之一；

<1>添加依赖

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-alibaba-sentinel-gateway</artifactId>
</dependency>
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>
```

<2>添加配置

```yaml
spring:
  application:
    name: api-gateway
  cloud:
    # 网关配置
    gateway:
      # 路由规则
      routes:
        - id: order_route
          uri: lb://order-service
    sentinel:
      transport:
        dashboard: 127.0.0.1:8080
```

<3>sentinel 控制台配置限流规则

**根据 Route 进行限流**

应用 api-gateway 》请求链路 》order_route 增加流控规则

![2021-10-14 pm4.18.33](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-14%20pm4.18.33.png)

**根据 API 分组进行限流**

应用 api-gateway 》API 管理 》新增 API 分组
