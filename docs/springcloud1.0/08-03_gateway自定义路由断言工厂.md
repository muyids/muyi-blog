实际开发中，可能存在内置路由断言工厂无法满足的场景，需要我们来自定义自己的路由断言工厂

**自定义路由断言工厂**

<1>配置 yaml

```yaml
# 网关配置
gateway:
  # 路由规则
  routes:
    - id: order_route
      uri: lb://order-service # lb指从nacos中按名称获取服务实例列表，并遵循负载均衡策略
      predicates:
        - Path=/order-service/**
        # http://127.0.0.1:8080/order-service/order/add/byFeign?id=1 -> http://127.0.0.1:9001/order-service/order/add/byFeign?id=1
        - CheckAuth=muyids
      filters:
        - StripPrefix=1 # 转发前去掉第一层路径
        # http://127.0.0.1:9001/order/add/byFeign?id=1CheckAuth=muyids
```

增加断言` - CheckAuth=muyids`检查

<2>断言工厂类编写

idea 中连续两次按 shift 键，搜索 QueryRoutePredicateFactory，观察其实现

自定义路由断言工厂需要继承 AbstractRoutePredicateFactory，重写 apply 方法的逻辑；

在 apply 方法中，可以通过 exchange.getRwquest()拿到 ServerHttpRequest 对象，从而获取到请求的参数、请求方式、请求头等信息。

1.必须是 spring 组件 bean

2.必须加上 RoutePredicateFactory 作为后缀

3.必须继承继承 AbstractRoutePredicateFactory

4.必须实现静态内部配置类，声明属性来接收配置文件信息，需要结合 shortcutFieldOrder()

```java
@Component
public class CheckAuthRoutePredicateFactory extends AbstractRoutePredicateFactory<CheckAuthRoutePredicateFactory.Config> {

    public CheckAuthRoutePredicateFactory() {
        super(CheckAuthRoutePredicateFactory.Config.class);
    }

    @Override
    public List<String> shortcutFieldOrder() {
        return Arrays.asList("name");
    }
    @Override
    public Predicate<ServerWebExchange> apply(CheckAuthRoutePredicateFactory.Config config) {
        return new GatewayPredicate() {
            @Override
            public boolean test(ServerWebExchange exchange) {
                if (StringUtils.isEmpty(config.getName())) {
                    return false;
                }
                if (StringUtils.isEmpty(exchange.getAttribute(config.getName()))) {
                    return false;
                }
                return true;
            }
            @Override
            public String toString() {
                return String.format("CheckAuth: name=%s", config.getName());
            }
        };
    }

    @Validated
    public static class Config {
        @NotEmpty
        private String name;
        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }
    }
}
```
