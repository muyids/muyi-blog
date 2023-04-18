**Spring Cloud Gateway**

网关作为流量入口，具有路由转发，权限校验，限流等功能；

Spring Cloud Gateway 是 Spring cloud 官方推出的第二代网关框架，定位于取代 Netflix Zuul1.0;

Spring Cloud Gateway 是由**WebFlux+Netty+Reactor 实现的响应式的 API 网关**。**不能在传统的 servlet 容器中工作，不能构建成 war 包**

Spring Cloud Gateway 旨在为微服务架构提供简单有效的 API 路由管理方式，**基于 Filter 的方式**提供网关的基本功能，例如安全认证、监控、限流等等

**功能特征**

- 基于 Spring Framework 5、Project Reactor 和 Spring Boot 2.0 进行构建
- 动态路由：能够匹配任何请求属性
- 支持路径重写
- 集成 Spring Cloud 服务发现功能（Nacos，Eureka）
- 可集成流控降级功能（Sentinel、Hystrix)
- 可以对路由指定易于编写的 Predicate(断言)和 Filter(过滤器)
  **核心概念**

一、路由（route）

网关中最基础的部分；路由信息包括一个 ID，一个目的 URI，一组断言工厂，一组 Filter；

如果断言为真，说明请求的 URI 和配置的路由匹配

二、断言（predicates)

Java8 中的断言函数，Spring Cloud Gateway 中的断言函数类型是 Spring5.0 框架中的 ServerWebExchange。

断言函数允许开发者去定义匹配 Http request 中的任何信息，比如请求头和参数等；

三、过滤器（Filter）

Spring Cloud Gateway 中的 Filter 分为 Gateway Filter 和 Global Filter。Filter 可以对请求和响应进行处理。

**工作原理**

暂不介绍

**快速开始**

<1>引入依赖

```xml
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

<2>application.yml 配置

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
          uri: http://127.0.0.1:9001 # 转发到order服务
          predicates:
            - Path=/order-service/**
            # http://127.0.0.1:8080/order-service/order/add/byFeign?id=1 -> http://127.0.0.1:9001/order-service/order/add/byFeign?id=1
          filters:
            - StripPrefix=1 # 转发前去掉第一层路径
            # http://127.0.0.1:9001/order/add/byFeign?id=1
```
