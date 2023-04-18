module.exports = [
  {
    title: "JUC",
    collapsable: true,
    sidebarDepth: 2,
    children: [
      ["/java/juc/01_JUC概览.md", "JUC概览"],
      ["/java/juc/03_JAVA线程锁机制.md", "JAVA线程锁机制"],
      ["/java/juc/04_谈谈你对AQS的理解.md", "谈谈你对AQS的理解"],
      ["/java/juc/05_AQS在并发工具类中的使用.md", "AQS在并发工具类中的使用"],
      ["/java/juc/06_JUC锁:ReentrantLock.md", "JUC锁:ReentrantLock"],
      [
        "/java/juc/07_JUC锁:ReentrantReadWriteLock.md",
        "JUC锁:ReentrantReadWriteLock",
      ],
      ["/java/juc/08_JUC工具类:CountDownLatch.md", "JUC工具类:CountDownLatch"],
      ["/java/juc/09_JUC工具类:CyclicBarrier.md", "JUC工具类:CyclicBarrier"],
      ["/java/juc/10_JUC工具类:Semaphore.md", "JUC工具类:Semaphore"],
    ],
  },
  {
    title: "JVM",
    collapsable: true,
    sidebarDepth: 2,
    children: [
      // [ '/java/jvm/01_类加载机制.md', '类加载机制'],
      ["/java/jvm/06_JVM调优.md", "JVM调优"],
    ],
  },
  {
    title: "Spring",
    collapsable: true,
    sidebarDepth: 2,
    children: [
      // [ '/java/spring/01_Bean的创建过程.md', 'Bean的创建过程'],
      ["/java/spring/02_自动装配原理.md", "自动装配原理"],
      // [ '/java/spring/03_actuator详解.md', 'actuator详解'],
    ],
  },
  {
    title: "Cloud V1.0",
    collapsable: true,
    sidebarDepth: 2,
    children: [
      ["/java/cloud1.0/00_分布式架构实战.md", "00_分布式架构实战"],
      ["/java/cloud1.0/01_父子项目的构建.md", "01_父子项目的构建"],
      [
        "/java/cloud1.0/02_springcloudalibaba引入.md",
        "02_springcloudalibaba引入",
      ],
      ["/java/cloud1.0/03_nacos服务发现.md", "03_nacos服务发现"],
      ["/java/cloud1.0/04_feign远程调用.md", "04_feign远程调用"],
      ["/java/cloud1.0/05_ribbon负载均衡.md", "05_ribbon负载均衡"],
      ["/java/cloud1.0/06_sentinel流量控制.md", "06_sentinel流量控制"],
      [
        "/java/cloud1.0/06-01_sentinel的三种模式.md",
        "06-01_sentinel的三种模式",
      ],
      ["/java/cloud1.0/07_seata分布式事务.md", "07_seata分布式事务"],
      ["/java/cloud1.0/07-01_AT模式.md", "07-01_AT模式"],
      ["/java/cloud1.0/07-02_TCC模式.md", "07-02_TCC模式"],
      [
        "/java/cloud1.0/07-03_可靠消息最终一致性方案.md",
        "07-03_可靠消息最终一致性方案",
      ],
      ["/java/cloud1.0/07-04_Seata的AT模式原理.md", "07-04_Seata的AT模式原理"],
      ["/java/cloud1.0/07-05_Seata服务搭建.md", "07-05_Seata服务搭建"],
      ["/java/cloud1.0/07-06_Seata客户端配置.md", "07-06_Seata客户端配置"],
      ["/java/cloud1.0/08_gateway网关.md", "08_gateway网关"],
      ["/java/cloud1.0/08-01_gateway入门.md", "08-01_gateway入门"],
      ["/java/cloud1.0/08-02_gateway集成nacos.md", "08-02_gateway集成nacos"],
      [
        "/java/cloud1.0/08-03_gateway内置路由断言工厂.md",
        "08-03_gateway内置路由断言工厂",
      ],
      [
        "/java/cloud1.0/08-04_gateway局部网关过滤器工厂.md",
        "08-04_gateway局部网关过滤器工厂",
      ],
      [
        "/java/cloud1.0/08-05_gateway全局网关过滤器.md",
        "08-05_gateway全局网关过滤器",
      ],
      [
        "/java/cloud1.0/08-06_gateway整合sentinel流控.md",
        "08-06_gateway整合sentinel流控",
      ],
      ["/java/cloud1.0/09_skywalking链路追踪.md", "09_skywalking链路追踪"],
      [
        "/java/cloud1.0/10_prometheus+grafana可视化监控系统搭建.md",
        "10_prometheus+grafana可视化监控系统搭建",
      ],
    ],
  },
  {
    title: "Cloud V2.0",
    collapsable: true,
    sidebarDepth: 2,
    children: [
      ["/java/cloud2.0/00_分布式id系统.md", "00_分布式id系统"],
      ["/java/cloud2.0/01_用户系统.md", "01_用户系统"],
      ["/java/cloud2.0/02_数据库分库分表.md", "02_数据库分库分表"],
      ["/java/cloud2.0/03_定时任务.md", "03_定时任务"],
    ],
  },
];
