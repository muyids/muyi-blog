# 系统架构图

![micro-service](https://muyids.oss-cn-beijing.aliyuncs.com/micro-service.jpeg)

# 组件

- [统一配置中心 Nacos](./配置中心/Nacos.md)

# 功能介绍

- 微服务平台
  - 统一认证功能
    - 网关统一认证 Spring Cloud Gateway
    - url 级权限控制 Spring Cloud Gateway
    - OSS 单点登录 Spring Security
      - 支持 OAuth2 的 4 种模式登陆
      - 用户名、密码登录
      - 手机号、验证码登录
  - 系统监控功能
    - 服务调用链监控 SkyWalking
    - 应用拓扑图 SkyWalking
    - 慢查询 SQL 监控 ELK
    - 应用吞吐量监控（qps、rt） Sentinel
    - 服务限流、降级、熔断监控 Sentinel
  - 分布式系统基础支撑
    - 服务降级与熔断 Sentinel
    - 服务限流（url/方法级别） Sentinel
    - 统一配置中心 Nacos
    - 统一日志中心 ELK
    - 统一搜索中心 ElasticSearch
  - 业务基础功能支撑
    - 分布式 ID 系统
    - 多租户（应用隔离）
    - 方法级幂等性支持
    - RBCA 权限管理，实现细粒度控制（url 级别）
    - 代码生成器，自定义脚手架开发
    - 网关聚合所有服务的 Swagger 接口文档
    - 统一跨域处理

# 知识阅读

- [zlt2000 企业级微服务框架项目](https://github.com/zlt2000/microservices-platform)
- https://processon.com/view/5c406df3e4b056ae29f3d544
