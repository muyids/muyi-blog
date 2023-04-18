上一节，我们完成了 gateway 的 api 转发，但是有一个问题：服务地址是写死的，无法满足微服务场景下服务地址的动态获取

我们需要一个服务发现组件，从注册中心来获取动态的服务地址

**集成 nacos**

<1>gateway 中引入依赖

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

<2>编写 yml 配置文件

uri 配置 loadbalance

```yaml
spring:
  application:
    name: api-gateway
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
    # 网关配置
    gateway:
      # 路由规则
      routes:
        - id: order_route
          uri: lb://order-service # lb指从nacos中按名称获取服务实例列表，并遵循负载均衡策略
          predicates:
            - Path=/order-service/**
            # http://127.0.0.1:8080/order-service/order/add/byFeign?id=1 -> http://127.0.0.1:9001/order-service/order/add/byFeign?id=1
          filters:
            - StripPrefix=1 # 转发前去掉第一层路径
            # http://127.0.0.1:9001/order/add/byFeign?id=1
```

另一种配置：去掉路由配置，自动寻找服务（约定大于配置）

```yaml
spring:
  application:
    name: api-gateway
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
    # 网关配置
    gateway:
      discovery:
        locator:
          enabled: true # 服务发现自动识别nacos
```
