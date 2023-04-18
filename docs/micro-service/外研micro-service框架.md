# 目前已有组件及功能

目前已有的组件其功能都比较简单，没有添加太多内容，需要大家共同讨论决定，以获取 best practice

- cloud 版本：H.SR5
- boot 版本：2.2.1

## commons

主要内容为：

- 常量定义
- 枚举
- 微服务间数据交互的实体定义,目前还是定义在公共的包中，其他服务
- 通用异常，如业务异常的基类放在该包中，其他服务异常继承自该基类

## web

服务类型为 web 的公共抽象，主要内容包括

- 统一的返回数据格式 code message data
- 默认值问题，后端尽量不返回 null 对象，但基于健壮性考量，前后端在使用数据前都需判断
- 异常拦截统一处理
- web 常用异常定义

## redis

- 看外研在线提供的框架中的 redis 相关模块是否可以复用
- value 的序列化处理方式，需要考虑异构的问题，GenericJackson2JsonRedisSerializer 可能不满足需求，考虑使用 Jackson2JsonRedisSerializer
- key 的序列化和反序列化默认为 string

## db

- 包含了数据库的分页功能，pageHelper 插件
- 定义了分页返回结果格式
- 定义了分页工具类

![数据库的分页功能](https://muyids.oss-cn-beijing.aliyuncs.com/CCmemtPsSvW32vIO.png)

# 约定：

## 通用业务异常

通用的业务异常目前是定义在 web 模块中，需移到 commons 包中

![img](https://muyids.oss-cn-beijing.aliyuncs.com/N92StSgwnQrf3sVa.png!thumbnail)

每个服务的错误码段`1001-1999、2001-2999...`

看原来的错误码定义，避免冲突

输出统一维护文档

## 关于事务注解@Transactional

注解加载具体的方法上，不要加在类上，也不要加载接口上

## Rest 接口命名及约定

对前端接口，严格遵循 rest 规范

- rest 规范

特殊的接口除外

login logout 等

后端 service dao 阿里建议：

![图片](https://muyids.oss-cn-beijing.aliyuncs.com/EttazcpD9XAjjHJ5.png!thumbnail)

- 对外服务、对前端服务，接口要有版本号 `/api/**v1****/**teacher`

## 2.4 项目包结构

代码：

    com.xxx.yyy.zzz.config

    com.xxx.yyy.zzz.mapper

    com.xxx.yyy.zzz.controller

    com.xxx.yyy.zzz.constant

    com.xxx.yyy.zzz.exception

    com.xxx.yyy.zzz.service

    com.xxx.yyy.zzz.service.impl

    com.xxx.yyy.zzz.utils

    com.xxx.yyy.zzz.entity.teacher.teacherDO

配置：

    resources/application.yml

    resources/application-dev.yml

    resources/application-test.yml

    resources/application-prod.yml

    resources/bootstrap.yml

    resources/bootstrap-dev.yml

    ....

可使用 maven profile 按环境打包，这样不同环境部署脚本或方式是一致的

静态资源：

    resources/static/

    resources/mapper/

## 日志

见阿里日志规约

## 数据库

### mysql:

- 时区，统一为东八区：

```plain
serverTimezone=Asia/Shanghai&allowMultiQueries=true&characterEncoding=UTF-8
```

- 数据库字符集: utf8mb4
- 排序规则: utf8mb4_general_ci
- 连接池 : druid

### redis

- redis 连接池：lettuce

## 微服务在服务注册于发现中的名称

    dera-homework

    dera-basedw

# 上线内容

微服务最近一个上线时间点是 8 月底的 新标准 0.8 需求，我们要上的内容

- 服务注册与发现---------------------- [nacos](./配置中心/Nacos.md)
- 微服务网关---------------------------- gateway
- 服务间调用---------------------------- openfeign

--------------------------待定-----------------------------------

- 配置中心---------------------------- nacos
- 熔断限流---------------------------- sentinel
- 链路追踪---------------------------- skywalking
- 消息系统---------------------------- kafka
