什么是 nacos?

一个更易于构建云原生应用的动态服务发现，服务配置的服务管理平台

注册中心+配置中心+服务管理；

关键特性：

- 服务发现和服务健康检测
- 动态配置服务
- 动态 DNS 服务
- 服务及其元数据管理

#### **注册中心的演变和设计思想**

注册中心：管理微服务，解决微服务间调用关系错综复杂，难以维护的问题

架构设计：

![2021-09-17 pm10.08.54](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-17%20pm10.08.54-4008118.png)

思考：

1. 每次请求都要去注册中心拉取服务列表吗？注册中心宕机了怎么办？
2. 注册中心应设计为 CP 还是 AP？
3. 如果注册表中的服务对应的机器宕机了怎么办？

#### **nacos 环境搭建**

**本地安装和启动**

本地安装路径 ： /usr/local/nacos

启动 ：`sh /usr/local/nacos/bin/startup.sh -m standalone`

**docker 启动**

```shell
docker run -d -p 8848:8848 --env MODE=standalone  --name nacos  nacos/nacos-server
```

**访问**

http://127.0.0.1:8848/nacos/

默认用户名密码`nacos/nacos`登录

#### **服务发现配置**

<1>Pom.xml 的配置

```xml
<dependency>
  <groupId>com.alibaba.cloud</groupId>
  <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

<2>yml 文件配置

```yaml
spring:
  application:
    name: stock-service
```

启动项目后发现服务列表中已存在对应的 web 服务

#### 服务调用

还记得我们之前使用 RestTemplate 进行服务间接口调用吗？

```java
    @Autowired
    RestTemplate restTemplate;

    @GetMapping("/add")
    public String add(Long id) {
        System.out.println("下单,商品id:" + id);
        String url = "http://localhost:9002/stock/reduce";
        String res = restTemplate.getForObject(url, String.class);
        return LocalDateTime.now().format(DateTimeFormatter.ISO_DATE) +":"+ res;
    }
```
