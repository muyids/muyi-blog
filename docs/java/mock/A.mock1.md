[来源 IT 老哥;面试自学 Java 的大佬，看看这水平值不值 30K](https://www.bilibili.com/video/BV1Gf4y1t7X3)

---

多线程

### Java 多线程有几种实现方式？

- 集成 thread 类
- 实现 runnable 接口
- 实现 callable 接口通过 futuretask 包装器来创建 thread 线程
- 通过线程池创建；使用线程池接口 ExecutorService 结合 Callable、Future 实现有返回结果的多线程

```
        ExecutorService threadPool = Executors.newFixedThreadPool(3); // 一池三个线程
//        ExecutorService threadPool = Executors.newSingleThreadExecutor(); // 一池1个线程
//        ExecutorService threadPool = Executors.newCachedThreadPool(); // 一池N个线程
```

```
ExecutorService threadPool = new ThreadPoolExecutor(
        2,
        5,
        60L,
        TimeUnit.SECONDS,
        new LinkedBlockingQueue<>(3),
        Executors.defaultThreadFactory(),
        new ThreadPoolExecutor.DiscardPolicy()
);
```

### 禁止直接使用 Executors 创建线程池的原因

1. 让我们更加明确线程池的运行规则
2. 规避资源耗尽的风险

```
        /**
         * 线程池不允许使用Executors去创建，而是通过ThreadPoolExecutor的方式，这样的处理方式的好处：
         * 1. 让我们更加明确线程池的运行规则
         * 2. 规避资源耗尽的风险
         *
         * 说明：Executors返回的线程池对象的弊端如下：
         *
         * 1）FixedThreadPool和SingleThreadPool:
         *   允许的请求队列底层为LinkedBlockingQueue<Runnable>(), 长度为Integer.MAX_VALUE，可能会堆积大量的请求，从而导致OOM。
         * 2）CachedThreadPool和newScheduledThreadPool:
         *   允许的创建线程数量为Integer.MAX_VALUE，可能会创建大量的线程，从而导致OOM。
         */
//        ExecutorService threadPool = Executors.newFixedThreadPool(3); // 一池三个线程
//        ExecutorService threadPool = Executors.newSingleThreadExecutor(); // 一池1个线程
//        ExecutorService threadPool = Executors.newCachedThreadPool(); // 一池N个线程
        ExecutorService threadPool = Executors.newScheduledThreadPool(1);
        for (int i = 0; i < 10; i++) {
            threadPool.execute(()->{
                System.out.println(Thread.currentThread().getName()+ "\t来办理业务");
            });
        }
```

### 能说一下线程池的参数吗

7 大参数

### 线程池工作原理

先核心，核心满了进阻塞队列，阻塞队列满了，开启最大线程数，最大和队列都满了，拒绝策略；

当一个线程空闲超过 keepAliveTime 且当前运行线程数大于 corePoolSize，这个线程被停掉；

### 拒绝策略

-

- 自定义；实现 RejectedExecutionHandler 接口

---

锁

### 先说一下 AQS

![2021-07-20 pm2.59.14](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm2.59.14.png)

抽象队列同步器： Abstract Queue Synchr

Volatile + 双向链表

![2021-07-20 pm3.03.34](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm3.03.34.png)

### AQS 用了什么设计模式

模板模式

### 读写锁是怎么实现的

readLock 和 WriteLock

### AQS 尾分叉

![2021-07-20 pm3.12.36](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm3.12.36.png)

### 说一下 synchronized

无锁 -> 偏向锁 -> 轻量级锁 -> 重量级锁

### 为什么引入适应性自旋锁

为了节约 cpu

---

集合

### ConcurrentHashMap

jdk1.7

![2021-07-20 pm3.18.26](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm3.18.26.png)

jdk8

![2021-07-20 pm3.19.45](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm3.19.45.png)

![2021-07-20 pm3.24.44](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm3.24.44.png)

### 说一下 CAS

- Compare and swap
- 乐观锁
- CPU 并发原语

cas 存在的问题

- ABA 问题
- 自旋操作对 CPU 有一定消耗
  ABA 问题的解决方案：

- 加版本号

### 什么是 LongAdder

**在低竞争的并发环境下 `AtomicInteger` 的性能是要比 `LongAdder` 的性能好，而高竞争环境下 `LongAdder` 的性能比 `AtomicInteger` 好**

因为 `AtomicInteger` 在高并发环境下会有多个线程去竞争一个原子变量，而始终只有一个线程能竞争成功，而其他线程会一直通过 CAS 自旋尝试获取此原子变量，因此会有一定的性能消耗；而 `LongAdder` 会将这个原子变量分离成一个 Cell 数组，每个线程通过 Hash 获取到自己数组，这样就减少了乐观锁的重试次数，从而在高竞争下获得优势；而在低竞争下表现的又不是很好，可能是因为自己本身机制的执行时间大于了锁竞争的自旋时间，因此在低竞争下表现性能不如 `AtomicInteger`。

阿里为什么推荐使用 LongAdder，而不是 volatile？https://zhuanlan.zhihu.com/p/197903344

### HashMap 加载因子为什么是 0.75

![2021-07-20 pm4.35.52](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm4.35.52.png)

### HashMap 多线程操作导致死循环问题

![2021-07-20 pm4.39.29](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm4.39.29.png)

### 快速失败（fail-fast）和安全失败

---

Spring

---

Spring Cloud

---

### 说一下 zookeeper

### zk 的 watch 机制

### zk 实现分布式锁的机制

两种方式：

1. 临时节点 + watch
2. 顺序节点，公平的
   临时节点+watch: 一个线程创建节点，别的线程 watch，删除后抢占

存在性能问题：当节点很多的时候，羊群（惊群）现象

### zk 的选举机制

服务启动 + 崩溃选举

### zk 选举过程中节点的几种状态

- looking
- leading
- following

### zab 协议

### zk 一个节点能存多大的数据

### zk 集群有哪些角色

![2021-07-21 am8.30.28](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 am8.30.28.png)

### 分布式集群中 Master 节点的作用

![2021-07-21 am8.31.27](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 am8.31.27.png)

---

tcp/ip

### 粘包 ，拆包怎么解决？

![2021-07-21 am8.33.30](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 am8.33.30.png)

### netty 底层是怎么实现的

nio

---

jvm

### 说一下 jvm 有哪几部分组成

![2021-07-21 am8.37.58](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 am8.37.58.png)

### 一个对象创建到创建完成

### 常见的垃圾回收算法

- 引用计数
- 复制
- 标记清除
- 标记整理

### 列举下垃圾回收器

### CMS 用的什么垃圾回收算法

---

kafka

### kafka 如何实现高性能

- 顺序写
- 预读
- 零拷贝

### 存储原理

### 丢数据和数据重复的情况

---

redis

### 缓存雪崩，穿透，击穿的问题

雪崩：大面积 key 失效

穿透：黑客攻击，故意请求不存在的 key

击穿：热点 key 失效

如何解决

### redis 字符串的底层数据结构

简单动态字符串 SDS

### list 的底层数据结构

- Ziplist: 列表对象所有字符串元素长度都小于 64 字节；元素数量小于 512
- 双向链表：

### hash 的底层数据结构

- ziplist
- 哈希表

### set 的底层数据结构

- inset
- 哈希表

### zset

- ziplist
- 跳表

---

elasticsearch

### 路由算法

### TF/IDF 算法

![2021-07-21 pm1.48.38](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 pm1.48.38.png)

---
