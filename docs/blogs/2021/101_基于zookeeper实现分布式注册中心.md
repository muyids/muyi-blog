分布式服务框架-注册中心 : https://juejin.cn/post/6997940076986515492?utm_source=gold_browser_extension

zookeeper 之 ZkClient：https://link.juejin.cn/?target=https%3A%2F%2Fsegmentfault.com%2Fa%2F1190000021258723

命令行工具 zkCli.sh 的使用：http://wiki.ai.fltrp.im/%E4%B8%AD%E9%97%B4%E4%BB%B6/zookeeper/

- 客户端 zkCli.sh -timeout 5000 -server 129.0.4.32:2181

zk ui:

- 访问地址： http://127.0.0.1:9090/home

项目代码：

- 本地：/Users/dw/workspace/knowledge/simple-rpc
  github : https://github.com/MIracleCczs/simple-rpc
- 我自己的项目: /Users/dw/workspace/muyids/cloudAli/register-center

注册中心架构

nacos 架构设计 https://zhuanlan.zhihu.com/p/344572647

- service

  - Service 对象

    ```
    {
    	服务名
    	[] 服务实例对象列表: {
    		host+port
    	}
    }
    ```

  - 通知订阅者

  - 通知持久化

- controller

  - http 请求注册

- subscriber

  - 订阅者

图灵学院 》手写 zookeeper 分布式注册中心 https://www.bilibili.com/video/BV1ZE411i7uE

Dubbo 推荐使用 zookeeper 做注册中心

---

- 服务（持久节点） /zkRegister/${servicename}

  - 服务提供者 1（临时节点）/pid1 {ip:port,servicename,pid 等信息}
  - 服务提供者 2（临时节点）/pid2 {ip:port,servicename,pid 等信息}
  - 。。。
    功能：

- 注册服务
- 订阅服务
  模块抽象：

- 注册中心 IRegister

  负责注册服务，获取服务列表，服务下线等功能

  - 实现类 ZkRegister

- Client 层

  客户端接入

  - 注册服务
  - 订阅服务列表 - 调用别的服务

- Controller 层

  http/rpc 调用

  Netty

- 中间件

  - zk : zookeeper 的连接

服务注册：

1. Client 端通知 注册中心

   通知方式：

   接口调用 IRegister.register(HostInfo info)

2. 注册中心创建服务

   1. 创建持久化节点（已存在则不创建）
   2. 创建临时节点
      订阅功能实现：

基于 zookeeper 的 watch 机制

1. 获取 service 持久节点列表
2. 订阅 service 持久节点的子节点的变化
   获取服务列表：

- 注册中心 从 zookeeper 获取
- 本地维护一份
  心跳机制：

客户端一旦断开，服务端需要等 10s 才将客户端注册的临时节点删除

原理：

- 客户端每隔 1s 向服务端发送一次通知
- 注册中心维护每一个客户端的最近心跳时间
- 间隔 3s 未收到心跳，则断开客户端连接，并删除客户端的临时节点

知识点：

- 服务节点用持久节点的原因：临时节点不能创建子节点
- 服务提供者节点用临时节点原因：下线的时候临时节点自动删除

---
