#### Feign 支持

<1>加入 `spring-cloud-starter-openfeign` 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

<2>`FeignClient` 的简单使用示例：

```java
@FeignClient(
        name = "stock-service",
        fallback = StockServiceFallback.class,
        configuration = FeignConfiguration.class
)
public interface StockService {
    @GetMapping(value = "/stock/reduce")
    // 需要添加@RequestParam("id")，用于纠正参数映射，不然会报405
    String reduce(@RequestParam("id") Long id);
}

@Configuration
public class FeignConfiguration {
    @Bean
    public StockServiceFallback stockServiceFallback(){
        return new StockServiceFallback();
    }
}

public class StockServiceFallback implements StockService {
    @Override
    public String reduce(Long id) {
        return "远程调用stock service失败";
    }
}
```

`StockService` 接口中方法 `reduce` 对应的资源名为 `GET:http://service-provider/stock/reduce?id=xx`

<3>调用 FeignClient

```java
@Autowired
StockService stockService;

@GetMapping("/add/byFeign")
public String addWithFeign(Long id) {
    System.out.println("下单,商品id:" + id);
    String res = stockService.reduce(id);
    System.out.println("扣减库存,商品id:" + id);
    return LocalDateTime.now().format(DateTimeFormatter.ISO_DATE) + ":" + res;
}
```
