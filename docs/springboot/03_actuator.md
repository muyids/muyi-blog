#### Spring Boot Actuator

本文主要来自官网阅读加自己理解：

https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html

一、增加 actuator 的 starter 依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

二、端点

Actuator 端点让你可以监控应用或与应用交互；

Springboot 包含一些内置的端点，比如 health 端点提供基础的应用健康信息；

你也可以增加你自己的端点；

每一个单独的端点都可以通过 HTTP 或 JMX 进行启用（禁用）和对外暴露，当端点被设置为启用和对外暴露时，可以视为是有效的。

通过 HTTP 对外暴露的端点，可以通过路由 `/actuator/${ID}`进行访问，比如 health 端点的路由为`/actuator/health`。

<1>启用端点

通过`management.endpoint.<id>.enabled` 配置

比如

```
management:
  endpoint:
    info:
      enabled: true
```

<2>暴露端点

```xml
management:
  endpoints:
    web:
      exposure:
        include: "*"
        exclude:
    jmx:
      exposure:
        include: "*"
        exclude:
```
