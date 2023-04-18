#### **双写一致**

1、Cache-aside pattern

读： 先读缓存，没有，读数据库再写缓存

写：写数据库，删缓存 （+ 延时删除）

2、延时双删

为什么需要延时双删，多线程并发请求的情况，存在 t1 从库中读了老数据，t2 去写新数据并且删了缓存，t1 把老数据又写到了缓存里，发生数据不一致

解决方案：

1、Canel 订阅 binlog 去异步删缓存

#### 持久化机制

rdb+aof

Rdb：全量备份，快照，

aof：增量日志追加备份

#### Redis 缓存系统是如何部署的

两种方式

主从+sentinel

cluster 模式

## 1.在你的项目中，哪些数据是数据库和 redis 缓存双写的？如何保证双写一致性？

## 2.系统上线，redis 缓存系统是如何部署的

## 3.系统上线，redis 缓存给了多大的总内存？命中率多高？抗住了多少 QPS？数据流回源会有多少 QPS?

## 4.热 key 大 Value 问题，某个 key 出现了热点缓存导致缓存集群中的某个机器负载过高？如何发现并解决？

## 5.超大 value 打满网卡的问题如何避免这样的问题

- 获取用户 Post 过来的数据，对 Key，Value 长度进行限制，避免产生超大的 Key,Value，打满网卡
- 可以将超大 value 的数据拆分成几个 Key-value,用 MGET（同时获取多个 key 的值）取值,降低 IO 消耗.

## 6.以往的工作经历中，是否出现过缓存集群事故？说说细节并说说高可用保障的方案？

## 7.平时如何监控缓存集群的 QPS 和容量

## 8.缓存集群如何扩容？

## 9.说一下 redis 的集群原理和选举机制

## 10.Key 寻址算法都有哪些？

## 11.Redis 线程模型现场画个图说说

## 12.Redis 内存模型现场画个图说说

## 13.redis 的底层数据结构了解多少

## 14.redis 的单线程特性有什么优缺点

## 15.如何解决缓存击穿的问题

---

## 1、在项目中缓存是如何使用的？为什么要用缓存？缓存使用不当会造成什么后果？

为什么要用缓存？

用缓存，主要有两个用途：高性能、高并发。

高性能：

比如 外研社这边 K12 优学 业务中有一个地区树查询接口，要拉取全国省-市-地区三级地区树的结构，从数据库中查询三级结构，至少要有三个 in 查询，查询后的结构后面也基本不怎么变了，这种查询结果 我们就把他扔到缓存里，一次查询走 db，后面的查询直接命中缓存返回

高并发：

我在天脉的时候，做的一些秒杀类似的业务（比如游戏抽奖，每天签到奖励这类的业务），先参与的人往往会获得更高的奖励，在某一时间点会产生大量的流量，如果这些大流量 的操作直接到了数据库，数据库肯定扛不住；
一方面，我们会把高并发会涉及到的业务数据写入缓存，比如用户签到，我们会在 redis 中用 hashTable 保存用户的连签信息，bonus 信息（比如生日）等
另一方面，还有会用 redis 实现分布式锁，起到限流的效果，限制用户在 10s 内只能触发一次签到操作

id-only 服务：

用 list 做 id 池，用 hash 保存 application 的信息（currentOffset 等属性）

## 2、redis 和 memcached 有什么区别？redis 的线程模型是什么？为什么 redis 单线程却能支撑高并发

- redis 支持复杂的数据结构
- redis 原生支持集群模式
- redis 大 key 没有 memcache 快

线程模型：

单线程的模型。它采用 IO 多路复用机制同时监听多个 socket，将产生事件的 socket 压入内存队列中，事件分派器根据 socket 上的事件类型来选择对应的事件处理器进行处理。

为什么 redis 单线程却能支撑高并发：

- 纯内存操作
- 非阻塞的 IO 多路复用机制
- 避免了多线程的频繁上下文切换问题

## 3、redis 都有哪些数据类型？分别在哪些场景下使用比较合适？redis 的底层数据结构了解多少

字符串 String、列表 List、字典 Hash、集合 Set、有序集合 SortedSet

string：简单动态字符串 SDS

hash ：底层实现：压缩列表，哈希表

存放的是结构化的对象

场景：我在做单点登录的时候，就是用这种数据结构存储单条用户信息，以 `CookieId` 作为 Key，设置 30 分钟为缓存过期时间，能很好的模拟出类似 `Session` 的效果。

List：底层实现：压缩列表，链表

使用 List 的数据结构，可以做简单的消息队列的功能。`rpush+blpop`实现先进先出；
另外还有一个就是，可以利用 `lrange` 命令，做基于 Redis 的分页功能，性能极佳，用户体验好，类似粉丝列表、文章的评论列表之类，微博那种下拉不断分页的东西。
set ： 底层实现：hash 表(不带 value)

- 全局去重的功能;因为 Set 堆放的是一堆不重复值的集合。所以可以做全局去重的功能
- 利用交集、并集、差集等操作，可以计算共同喜好，全部的喜好，自己独有的喜好等功能。
  ZSet ：底层实现：跳表

- `Sorted Set`多了一个权重参数 Score，集合中的元素能够按 Score 进行排列。
- 可以做排行榜应用，取 `TOP N` 操作。
- `Sorted Set` 可以用来做延时任务。最后一个应用就是可以做范围查找。

其他一些数据结构

HyperLogLog、Geo、Pub/Sub

Redis Module

BloomFilter，RedisSearch，Redis-ML

## 4、redis 的过期策略都有哪些？内存淘汰机制都有哪些？手写一下 LRU 代码实现？

过期策略

**定期删除+惰性删除**

定期删除，redis 默认是每隔 100ms 就随机抽取一些设置了过期时间的 key，检查其是否过期，如果过期就删除。

惰性删除，获取某个 Key 的时候，Redis 会检查一下，这个 Key 如果设置了过期时间，如果过期了此时就会删除。

内存淘汰机制：

如果没有过期的 Key 被**定期删除 或 惰性删除**，内存不断增长，怎么办？内存不够用了怎么办？

在 redis.conf 中有一行配置：

```shell
# maxmemory-policy volatile-lru
```

六种内存淘汰策略：

- noeviction：当内存不足以容纳新写入数据时，新写入操作会报错。应该没人用吧。
- **allkeys-lru**：当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的 Key。推荐使用，目前项目在用这种。
- allkeys-random：当内存不足以容纳新写入数据时，在键空间中，随机移除某个 Key。应该也没人用吧，你不删最少使用 Key，去随机删。
- volatile-lru：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，移除最近最少使用的 Key。这种情况一般是把 Redis 既当缓存，又做持久化存储的时候才用。不推荐。
- volatile-random：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，随机移除某个 Key。依然不推荐。
- volatile-ttl：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，有更早过期时间的 Key 优先移除。不推荐。
  推荐使用：allkeys-lru

手写下 LRU 代码实现：

```java
class LRUCache {
    class Node {
        int key;
        int val;
        Node pre;
        Node next;

        public Node(int key, int val) {
            this.key = key;
            this.val = val;
            this.pre = this.next = null;
        }
    }
    public void removeNode(Node node) {
        node.pre.next = node.next;
        node.next.pre = node.pre;
    }
    public void addNodeToTail(Node node) {
        node.pre = tail.pre;
        node.next = tail;
        node.pre.next = node;
        tail.pre = node;
    }
    int capacity;
    Map<Integer, Node> hash = new HashMap<>();
    Node head = new Node(-1, -1);
    Node tail = new Node(-1, -1);
    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.pre = head;
    }

    public int get(int key) {
        if (!hash.containsKey(key)) {
            return -1;
        }
        removeNode(hash.get(key));
        addNodeToTail(hash.get(key));
        return hash.get(key).val;
    }
    public void put(int key, int value) {
        while (!hash.containsKey(key) && hash.size() >= capacity) {
            hash.remove(head.next.key);
            removeNode(head.next);
        }
        if (hash.containsKey(key)) {
            removeNode(hash.get(key));
        }
        Node node = new Node(key, value);
        hash.put(key, node);
        addNodeToTail(node);
    }
}
```

## 5.如何保证 redis 的高并发和高可用？redis 的主从复制原理能介绍一下么？redis 的哨兵原理能介绍一下么？

redis 主从架构

redis 基于哨兵实现高可用 redis 实现高并发主要依靠主从架构，一主多从，一般来说，很多项目其实就足够了，单主用来写入数据，单机几万 QPS，多从用来查询数据，多个从实例可以提供每秒 10w 的 QPS。

如果想要在实现高并发的同时，容纳大量的数据，那么就需要 redis 集群，使用 redis 集群之后，可以提供每秒几十万的读写并发。

redis 高可用，如果是做主从架构部署，那么加上哨兵就可以了，就可以实现，任何一个实例宕机，可以进行主备切换。

## 6、redis 的持久化有哪几种方式？不同的持久化机制都有什么 优缺点？持久化机制具体底层是如何实现的？

问题背景：

如果 redis 的数据都在内存里，一旦宕机重启，内存数据丢失。造成缓存雪崩，数据库挂掉

所以，我们必须使用 redis 的持久化机制，将数据写入内存，在重启的时候尽量少丢数据

A:

redis 持久化的两种方式

- RDB：RDB 持久化机制，是对 redis 中的数据执行周期性的持久化。
- AOF：AOF 机制对每条写入命令作为日志，以 append-only 的模式写入一个日志文件中，在 redis 重启的时候，可以通过回放 AOF 日志中的写入指令来重新构建整个数据集。
  两种方式结合使用：

- RDB：备份周期长，会丢失更多数据；但恢复快
- AOF：恢复时间长，时间间隔一秒，丢失数据少
