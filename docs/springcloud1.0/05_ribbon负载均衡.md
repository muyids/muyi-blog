#### **负载均衡**

负载均衡分为**服务端负载均衡**和**客户端负载均衡**

服务端负载均衡如 nginx，需要单独的服务器

我们这里说的 Ribbon 属于 客户端负载均衡

应用层的负载均衡：gateway，kong

#### Ribbon

Ribbon 已经被 Feign 继承，所以当我们引入 feign 以后，使用 ribbon 不需要再引入其他依赖

**ribbon 支持的负载均衡策略**

- 随机策略 Random
- 轮训策略 RoundRobin
- 重试策略 Retry
- 最小并发策略
- 可用过滤策略
- 响应时间加权重策略
- 区域权重策略

- 自定义（通过）

![img](https://muyids.oss-cn-beijing.aliyuncs.com/1090617-20210414202554498-384351902-20211012153949225.jpg)

**默认负载均衡策略**

① 启动两个 stock-service 实例，StockApplication9002 和 StockApplication9003

② 服务调用时返回节点端口

```java
@GetMapping("/reduce")
public String reduce(HttpServletRequest request, @RequestParam(name = "id") Long id) {
    String res = "减库存,商品id:" + id + ";当前节点端口：" + request.getServerPort();
    System.out.println(res);
    return res;
}
```

调用后，我们发现，9002 和 9003 以轮训的方式返回，所以可以推测默认负载均衡策略是 RoundRobin

**自定义负载均衡策略**

我们可以通过自定义`IRule`规则指定负载均衡策略；

```java
@Bean
public IRule loadBalancer(){
//        return new RandomRule();
        return new WeightedResponseTimeRule();
}
```
