module.exports = [
  ["/计算机网络", "计算机网络"],
  ["/数据结构", "数据结构"],
  ["/操作系统", "操作系统"],
  {
    title: "Mysql",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      // A4.集群架构和相关原理.md
      // A6.MySQL优化.md
      // A9.大表增加一列.md
      // B1.奈学教育《3天挑战架构师级MySQL海量数据设计与实践》在线专栏课.md
      // B2.图灵-诸葛老师《Mysql高并发底层原理分析》.md
      // C1.一次mysql模拟面试.md
      // zz.名词解释.md
      // zz规范.md
      // zz基本SQL操作.md
      // [ '/mysql/A1.架构原理和存储机制.md', '架构原理和存储机制' ],
      // [ '/mysql/2.索引存储机制和工作原理.md', '索引存储机制和工作原理' ],
      // [ '/mysql/A3.事务和锁工作原理.md', '事务和锁工作原理' ],
      // [ '/mysql/4.集群架构和相关原理.md', '集群架构和相关原理' ],
      // [ '/mysql/6.MySQL优化.md', 'MySQL优化' ],
      // [ '/mysql/9.大表增加一列.md', '大表DDL操作' ],
      // [ '/mysql/10.面试必刷.md', '基础' ],
      // [ '/mysql/奈学教育《3天挑战架构师级MySQL海量数据设计与实践》在线专栏课.md', '进阶' ],
      // [ '/mysql/基本SQL操作.md', '常用DML语句' ],
    ],
  },
  {
    title: "Redis",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      // [ '/redis/1.为什么用redis.md', '为什么用redis' ],
      // [ '/redis/2.redis的使用场景.md', 'redis的使用场景' ],
      // [ '/redis/3.redis的数据类型、应用及底层实现.md', 'redis的数据类型、应用及底层实现' ],
      // [ '/redis/4.redis实现分布式锁.md', 'redis实现分布式锁' ],
      // {
      //   title: 'Redis线上常见问题',
      //   collapsable: false,
      //   sidebarDepth: 2,
      //   children: [
      //     [ '/redis/5.双写一致性问题.md', '双写一致性问题' ],
      //     [ '/redis/6.缓存穿透和缓存雪崩问题.md', '缓存穿透和缓存雪崩问题' ],
      //     [ '/redis/7.并发竞争Key问题.md', '并发竞争Key问题' ],
      //   ]
      // },
      // [ '/redis/8.redis的集群方案.md', 'redis的集群方案' ],
      // [ '/redis/9.redis主从模式.md', 'redis主从模式' ],
      // [ '/redis/redis的哨兵机制.md', 'redis的哨兵机制' ],
      // [ '/redis/redis的cluster集群模式.md', 'redis的cluster集群模式' ],
      // [ '/redis/redis持久化和主从复制原理.md', 'redis持久化和主从复制原理' ],
      // [ '/redis/redis的过期策略以及内存淘汰机制.md', 'redis的过期策略以及内存淘汰机制' ],
    ],
  },
  {
    title: "MongoDB",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      // [ '/mongodb/mongodb.md', 'Mongodb' ],
      // [ '/mongodb/mongodb调优.md', 'Mongodb调优' ],
    ],
  },
  {
    title: "Zookeeper",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      ["/zookeeper/00_环境搭建.md", "00_环境搭建"],
      ["/zookeeper/01_zookeerper知识点.md", "01_zookeerper知识点"],
      ["/zookeeper/02_客户端操作.md", "02_客户端操作"],
    ],
  },
  {
    title: "Kafka",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      ["/kafka/1.内部kafka环境.md", "内部kafka环境介绍"],
      ["/kafka/2.概念介绍.md", "概念介绍"],
      ["/kafka/3.基础架构.md", "基础架构"],
      ["/kafka/4.集群部署.md", "集群部署"],
      ["/kafka/5.命令行基本操作.md", "命令行基本操作"],
      ["/kafka/6.工作流程和数据存储机制.md", "工作流程和数据存储机制"],
      {
        title: "生产者",
        collapsable: false,
        sidebarDepth: 2,
        children: [
          ["/kafka/生产者/分区策略.md", "分区策略"],
          ["/kafka/生产者/数据可靠性保证.md", "数据可靠性保证"],
          ["/kafka/生产者/Exactly-Once语义.md", "Exactly Once语义"],
        ],
      },
      {
        title: "消费者",
        collapsable: false,
        sidebarDepth: 2,
        children: [
          ["/kafka/消费者/消费方式.md", "消费方式"],
          ["/kafka/消费者/分区分配策略.md", "分区分配策略"],
          ["/kafka/消费者/offset的维护.md", "offset的维护"],
        ],
      },
      ["/kafka/zookeeper的作用.md", "zookeeper的作用"],
      ["/kafka/java客户端实战.md", "java客户端实现"],
      {
        title: "运维监控",
        collapsable: false,
        sidebarDepth: 2,
        children: [
          ["/kafka/运维/运维工具对比.md", "运维工具对比"],
          ["/kafka/运维/CMak.md", "CMak"],
        ],
      },
    ],
  },
  {
    title: "ELK Stack",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      ["/elastic/1.ElasticStack简介.md", "Elastic Stack简介"],
      ["/elastic/2.Elasticsearch的介绍与安装.md", "Elasticsearch的介绍与安装"],
      ["/elastic/3.Elasticsearch的快速入门.md", "Elasticsearch的快速入门"],
      ["/elastic/4.Elasticsearch的核心讲解.md", "Elasticsearch的核心讲解"],
      ["/elastic/5.中文分词.md", "中文分词"],
      ["/elastic/6.全文搜索.md", "全文搜索"],
      ["/elastic/7.Elasticsearch集群.md", "Elasticsearch集群"],
    ],
  },
  {
    title: "工具",
    collapsable: false,
    sidebarDepth: 2,
    children: [
      ["/tools/git.md", "Git"],
      ["/tools/shell.md", "Shell"],
      ["/tools/vim.md", "Vim"],
      ["/tools/latex.md", "Latex"],
      ["/tools/ssh-keygen.md", "ssh-keygen"],
      ["/tools/supervisor.md", "supervisor"],
    ],
  },

  {
    title: "协议规范",
    collapsable: false,
    sidebarDepth: 2,
    children: [["/protocol/restful.md", "Restful"]],
  },
];
