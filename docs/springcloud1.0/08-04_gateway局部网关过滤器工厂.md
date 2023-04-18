#### 官方提供的内置网关过滤器工厂

参考文档

https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/index.html#gatewayfilter-factories

路由过滤器允许以某种方式修改传入的 HTTP 请求或传出的 HTTP 响应。路由过滤器的范围是特定的路由。Spring Cloud Gateway 包括许多内置的 GatewayFilter 工厂。

**AddRequestHeaderGatewayFilterFactory**

```yaml
filters:
  - AddRequestHeader=X-Request-red, blue
```

将`X-Request-red:blue`标头添加到所有匹配请求的下游请求标头中。

**AddRequestParameter 网关过滤器工厂**

```yaml
filters:
  - AddRequestParameter=red, blue
```

添加`red=blue`到所有匹配请求的下游请求的查询字符串中。

**重定向网关过滤器工厂**

```yaml
filters:
  - RedirectTo=302, https://acme.org
```

https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/index.html#the-redis-ratelimiter

#### 自定义网关过滤器工厂

跟自定义路由断言工厂类似，

自定义网关过滤器工厂需要继承 AbstractNameValueGatewayFilterFactory，类名以 GatewayFilterFactory 结尾并交给 Spring 管理

<1>yml 配置

```
filters:
- CheckAuth=muyids,yourpassword
```

<2>过滤器工厂类

```java
@Component
public class CheckAuthGatewayFilterFactory extends AbstractNameValueGatewayFilterFactory {
    @Override
    public GatewayFilter apply(NameValueConfig config) {
        return new GatewayFilter() {
            @Override
            public Mono<Void> filter(ServerWebExchange exchange,
                                     GatewayFilterChain chain) {
                String log = String.format("调用CheckAuthGatewayFilterFactory;%s:%s", config.getName(), config.getValue());
                System.out.println(log);
                return chain.filter(exchange);
            }
        };
    }
}
```
