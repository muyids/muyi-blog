**作用**

请求 gateway 的时候，使用断言对请求进行匹配，如果匹配成功，进行路由转发，如果匹配失败，返回 404

类型：

- 内置
- 自定义

#### 内置断言工厂举例

gateway 提供了多种类型的内置断言工厂，可以与 Http 请求的不同属性匹配，具体如下：

**Datetime 类型的断言工厂**

支持时间前、后、之间三种匹配

```yaml
predicates:
  - After=2017-01-20T17:42:47.789-07:00[America/Denver]
  - Before=2017-01-20T17:42:47.789-07:00[America/Denver]
  - Between=2017-01-20T17:42:47.789-07:00[America/Denver], 2017-01-21T17:42:47.789-07:00[America/Denver]
```

**Cookie 断言工厂**

匹配具有给定名称的 cookie 且其值与正则表达式匹配的请求

```yaml
predicates:
  - Cookie=chocolate, ch.p
```

**请求头断言工厂**

匹配具有给定名称的 =header 且其值与正则表达式匹配 的请求

```yaml
predicates:
  - Header=X-Request-Id, \d+
```

**Host 断言工厂**

```yaml
predicates:
  - Host=**.somehost.org,**.anotherhost.org
```

**请求方法断言工厂**

```yaml
predicates:
  - Method=GET,POST
```

**Path 断言工厂**

```yaml
predicates:
  - Path=/red/{segment},/blue/{segment}
```

**查询参数断言工厂**

不指定值

```yaml
predicates:
  - Query=green
```

指定值

```
predicates:
- Query=red, gree.
```

**权重断言工厂**

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: weight_high
          uri: https://weighthigh.org
          predicates:
            - Weight=group1, 8
        - id: weight_low
          uri: https://weightlow.org
          predicates:
            - Weight=group1, 2
```
