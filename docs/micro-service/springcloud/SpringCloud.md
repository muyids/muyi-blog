# SpringCloud

项目地址：[http://gitlab.nse.cn/yangdw/cloud2020](http://gitlab.nse.cn/yangdw/cloud2020)

进度：

P102 Nacos 之命名空间分组。。。

## 文档

- [github 中文文档](https://github.com/alibaba/spring-cloud-alibaba/blob/master/README-zh.md)
- [spring-cloud-alibaba/wiki](https://github.com/alibaba/spring-cloud-alibaba/wiki)
- [Spring Cloud 中文网](https://www.springcloud.cc/)

## 组件

![组件](https://muyids.oss-cn-beijing.aliyuncs.com/spring-cloud-component.png)

SpringCloud 升级,部分组件停用:

1. Eureka 停用,可以使用`zk`作为服务注册中心
2. 服务调用,Ribbon 准备停更,代替为`LoadBalance`
3. Feign 改为`OpenFeign`
4. Hystrix 停更,改为`resilence4j`或者阿里巴巴的`sentienl`
5. Zuul 改为`gateway`
6. 服务配置 Config 改为`Nacos`
