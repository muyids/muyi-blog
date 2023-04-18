[Sentinel](https://github.com/alibaba/Sentinel) 以流量为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。

**控制台安装启动**

<1>获取控制台

从 [release 页面](https://github.com/alibaba/Sentinel/releases) 下载最新版本的控制台 jar 包

<2>启动控制台

```shell
java -Dserver.port=8080 -Dcsp.sentinel.dashboard.server=localhost:8080 -Dproject.name=sentinel-dashboard -jar /usr/local/sentinel-dashboard-1.8.2.jar
```

<3>配置控制台

application.yml

```
spring:
  cloud:
    sentinel:
      transport:
        port: 8719
        dashboard: localhost:8080
```

这里的 `spring.cloud.sentinel.transport.port` 端口配置会在应用对应的机器上启动一个 Http Server，该 Server 会与 Sentinel 控制台做交互。比如 Sentinel 控制台添加了一个限流规则，会把规则数据 push 给这个 Http Server 接收，Http Server 再将规则注册到 Sentinel 中。

**增加 Sentinel 资源**

```java
@Service
public class StockService {

    @SentinelResource(value = "StockReduce")
    public String reduce(Long id){
        String res = "减库存,商品id:" + id;
        System.out.println(res);
        return res;
    }
}

```

使用注解`@SentinelResource(value = "StockReduce")`增加 Sentinel 资源

**流量规则的配置**
