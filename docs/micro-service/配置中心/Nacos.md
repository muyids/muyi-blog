[Nacos 官方文档](https://nacos.io/zh-cn/docs/what-is-nacos.html)

# 安装&启动

# 服务注册&发现和配置管理

服务注册

    curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'

服务发现

    curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'

发布配置

    curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"

获取配置

    curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"

# 两种模式

一致性协议：AP 和 CP

- 服务发现 AP
- 配置中心 CP

# 参考

- [Nacos 官方文档](https://nacos.io/zh-cn/docs/what-is-nacos.html)
- https://juejin.im/post/5ef8a736e51d453dec116003?utm_source=gold_browser_extension
