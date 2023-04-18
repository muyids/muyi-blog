**大纲**

- 特性，为什么快

- 常用数据结构和使用场景

- 底层数据结构及原理

  - 跳表能具体说一下吗

- 双写、读写一致性问题

- 持久化机制是怎样的

- 过期策略和内存淘汰机制；LRU 算法实现

- 缓存雪崩、穿透、击穿

- 集群方案有哪些？主从、哨兵、集群

---

#### **特点，为什么快**

Redis 的特点

1. 速度快：单线程，内存操作，I/O 多路复用，数据结构优化，RESP 协议
1. 键值对的数据结构
1. 支持丰富数据类型：支持 string，list，set，sorted set，hash
1. 丰富的特性：可用于缓存，消息，按 key 设置过期时间，过期后将会自动删除
1. 简单稳定
1. 持久化
1. 主从复制
1. 高可用和分布式转移
1. 客户端语言多

Redis 为什么这么快

1. 单线程，避免了频繁的上下文切换
2. 内存操作
3. 采用了非阻塞 I/O；多路复用机制
4. 数据结构优化
5. RESP 协议

#### 常用数据结构和使用场景

常用数据结构：

- **五种基本数据类型**

  字符串 String、列表 List、字典 Hash、集合 Set、有序集合 SortedSet

  **string**

  简单动态字符串 SDS

  **hash**

  底层实现：压缩列表，哈希表

  存放的是结构化的对象

  场景：我在做单点登录的时候，就是用这种数据结构存储单条用户信息，以 `CookieId` 作为 Key，设置 30 分钟为缓存过期时间，能很好的模拟出类似 `Session` 的效果。

  **List**

  底层实现：压缩列表，链表

  使用 List 的数据结构，可以做简单的消息队列的功能。`rpush+blpop`实现先进先出；另外还有一个就是，可以利用 `lrange` 命令，做基于 Redis 的分页功能，性能极佳，用户体验好。

  **set**

  底层实现：hash 表(不带 value)

  - 全局去重的功能;因为 Set 堆放的是一堆不重复值的集合。所以可以做全局去重的功能
  - 利用交集、并集、差集等操作，可以计算共同喜好，全部的喜好，自己独有的喜好等功能。
    **ZSet**

  底层实现：跳表

  - `Sorted Set`多了一个权重参数 Score，集合中的元素能够按 Score 进行排列。
  - 可以做排行榜应用，取 `TOP N` 操作。
  - `Sorted Set` 可以用来做延时任务。最后一个应用就是可以做范围查找。

  **其他一些数据结构**

  HyperLogLog、Geo、Pub/Sub

  **Redis Module**

  BloomFilter，RedisSearch，Redis-ML

  **内部数据结构详解**

  - [dict](http://zhangtielei.com/posts/blog-redis-dict.html)
  - [sds](http://zhangtielei.com/posts/blog-redis-sds.html)
  - [robj](http://zhangtielei.com/posts/blog-redis-robj.html)
  - [ziplist](http://zhangtielei.com/posts/blog-redis-ziplist.html)
  - [quicklist](http://zhangtielei.com/posts/blog-redis-quicklist.html)
  - [skiplist](http://zhangtielei.com/posts/blog-redis-skiplist.html)
    链表：

  Quicklist -> ziplist,ziplist 大小的配置

  list-max-ziplist-size

常用的 几种场景如下：

- 会话缓存（Session Cache）
- 全页缓存（FPC）
- 队列 ： list, lpush+brpop 阻塞队列
- 分布式锁 ：setnx ex
- 排行榜 ：zset
- 计数器 ：hyperloglog
- 发布/订阅

**跳表**

推荐阅读：http://zhangtielei.com/posts/blog-redis-skiplist.html

**跳表的结构**

- 多层链表结构
- 节点：

  - 值
  - 指针数组：不同层链表的下一个结点指针
  - 层：节点位于多少层，可以由指针数组的大小定义

- 头节点：各层链表的头节点
- 尾节点：各层链表的尾节点，每一层最后一个节点的本层链表下一个节点为空，即到达尾部
  ![2021-09-16 am8.45.38](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-16 am8.45.38-1807564-1809225.png)

节点插入过程：

默认层数和随机层数算法：32 层，随机上升因子 1/4

#### 双写、读写一致性问题

一致性级别：

- 强一致性
- 弱一致性
- 最终一致性

手段

1. 延时双删策略
2. 设置缓存的过期时间
3. Binlog 异步同步

#### 持久化机制是怎样的

RDB、AOF、混合持久化

#### 过期策略和内存淘汰机制；LRU 算法实现

**过期策略**：**定期删除+惰性删除**

定期删除，redis 默认是每隔 100ms 就随机抽取一些设置了过期时间的 key，检查其是否过期，如果过期就删除。

惰性删除，获取某个 Key 的时候，Redis 会检查一下，这个 Key 如果设置了过期时间，如果过期了此时就会删除。

**内存淘汰机制**

如果没有过期的 Key 被**定期删除 或 惰性删除**，内存不断增长，怎么办？内存不够用了怎么办？

在 redis.conf 中有一行配置：

```shell
# maxmemory-policy volatile-lru
```

六种内存淘汰策略：

1. volatile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
2. volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
3. volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
4. allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
5. allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
6. no-enviction（驱逐）：禁止驱逐数据
   推荐使用：allkeys-lru

**LRU 算法实现**：双向链表+哈希表

#### **缓存雪崩、穿透、击穿**

**缓存雪崩** ：即缓存同一时间大面积的失效

发生原因：

- 缓存服务宕机
- 大量 key 同时过期
  解决方案：

- **高可用**：发生雪崩事前，主从+哨兵，redis cluster，避免服务崩溃
- **限流&降级**：发生雪崩事中：本地`ehcache`缓存 + `hystrix` ，避免 MySQL 被打死
- **数据预热**：将发生大并发访问前，预先访问一遍
- **随机失效时间**：平时开发，给缓存的失效时间，加上一个随机值，避免集体失效
  **缓存穿透**：即黑客故意去请求缓存中不存在的数据。

低频的缓存穿透是 正常的，高频的缓存穿透才会影响数据库

缓存穿透解决方案

1. 同样的请求 ID 的情况；
   - **分布式锁**，使用**互斥锁**更新，保证同一个进程中针对同一个数据不会并发请求到 DB，减小 DB 压力。
   - 把查询到的结果（正常查询结果、NULL 值等）写入到缓存中，可以过滤掉同样的请求
2. 每次都是 不同的 ID（最常见的攻击场景）；
