图灵-白起

ElasticSearch 从 0 到集群高可用实战

1、ElasticSearch 快速入门
2、ElasticSearch 底层原理深度剖析
3、ElasticSearch 数据管理详解
4、ElasticSearch 集群高可用环境快速实战
5、ElasticSearch 集群脑裂问题如何解决
6、ElasticSearch 集群架构读写原理剖析
7、IK 分词器源码升级改造实现自定义词库热更新
8、ElasticSearch 文档算分原理解密
9、千万数据查询时间毫秒级你会怎么设计
10、京东等大型电商系统搜索实战带你手写实现
11、大厂面试 ElasticSearch 都问了什么

---

## ElasticSearch 集群脑裂问题如何解决

- 集群节点部署成奇数
  - 过半选举机制
  - 2\*n + 1 , 过半数正常集群可用，容忍 n 台不可用
  - 2\*n + 2 台，同样是容忍 n 台不可用，没必要多部署一台，部署奇数台能节省资源
- 脑裂场景说明
  - 现象：一个集群中出现两个 master
  - 发生原因：
    - **假死：**由于心跳超时（网络原因导致的）认为 Leader 死了，但其实 leader 还存活着；
    - **脑裂：**由于假死会发起新的 Leader 选举，选举出一个新的 Leader，但旧的 Leader 网络又通了，导致出现了两个 Leader ，有的客户端连接到老的 Leader，而有的客户端则连接到新的 leader。
  - 解决方法：
    - Quorums (法定人数) 方式: zookeeper 的过半选举机制
    - **Redundant communications (冗余通信)方式：**集群中采用多种通信方式，防止一种通信方式失效导致集群中的节点无法通信。
    - **Fencing (共享资源) 方式：**比如能看到共享资源就表示在集群中，能够获得共享资源的锁的就是 Leader，看不到共享资源的，就不在集群中。
    - 仲裁机制方式
    - 启动磁盘锁定方式

## Elasticsearch 选举原理之 Bully 算法

选举时间点

- 某个新节点加入了集群或者某个节点从宕机中恢复
- 集群中的某个节点检测到 leader 崩溃
  选举流程

1. 节点 node 向所有比自己大的节点发送选举消息(选举为 election 消息)

2. 如果节点 node 得不到任何回复(回复为 alive 消息)，那么节点 node 成为 master，并向所有的其它节点宣布自己是 master(宣布为 Victory 消息)

3. 如果 node 得到了任何回复，node 节点就一定不是 master，同时等待 Victory 消息，如果等待 Victory 超时那么重新发起选举

https://www.cs.colostate.edu/~cs551/CourseNotes/Synchronization/BullyExample.html

Bully 算法缺陷

- master 假死
- 脑裂问题
