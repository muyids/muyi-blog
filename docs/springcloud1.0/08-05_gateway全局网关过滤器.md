全局过滤器和局部过滤器的区别：

- 局部过滤器主要是针对某一个路由进行过滤，全局过滤器针对所有路由请求进行过滤
- 全局过滤器不需要在配置文件中进行配置，一旦定义就会投入使用
  列举全局过滤器

![2021-10-14 pm2.29.11](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-14%20pm2.29.11.png)

这些全局过滤器已经在 gateway 源码中实现，可以直接使用，了解其原理需要查看相关源码；

全局过滤器 LoadBalancerClientFilter 功能：会检查 exchange 中的 URI 属性，如果 uri 的 scheme 是 lb，如 lb://myservice，则使用 SpringCloud 中的 LoadBalancerClient 将 myservice 解析成 host:port

**自定义全局过滤器**

```java
@Component
public class LogFilter implements GlobalFilter {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        Logger logger = LoggerFactory.getLogger(this.getClass());
        logger.info("请求path:{}", exchange.getRequest().getPath().value());
        return chain.filter(exchange);
    }
}
```
