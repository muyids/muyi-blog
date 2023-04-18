---
title: 分布式ID系统设计
date: 2019-2-13T00:00:00+08:00
categories: [后端]
tags: [后端]
draft: true
---

## 思维导图

![分布式ID系统设计-思维导图](https://processon.com/chart_image/5ed85e2ce0b34d4139fc4c57.png)

[源文件地址](https://www.processon.com/view/link/5ed905426376891862180c6d)

## 业务场景

业务系统对于 ID 的要求有哪些？

- 全局唯一性：不能出现重复的 ID 号，既然是唯一标识，这是最基本的要求。
- 趋势递增：在`MySQL InnoDB`引擎中使用的是 **聚集索引**，由于多数`RDBMS`使用`B-tree`的数据结构来存储索引数据，在主键的选择上面我们应该尽量使用**有序的主键**保证写入性能。
- 单调递增：保证下一个 ID 一定大于上一个 ID，例如事务版本号、IM 增量消息、排序等特殊需求。
- 信息安全：如果 ID 是连续的，恶意用户的扒取工作就非常容易做了，直接按照顺序下载指定 URL 即可；如果是订单号就更危险了，竞对可以直接知道我们一天的单量。所以在一些应用场景下，会需要 ID 无规则、不规则。

## 性能要求

如果 ID 生成系统瘫痪，整个系统的无法获取新生成 ID 号，业务系统会面临崩溃

因此 ID 系统在保证 **ID 号码满足自身的要求** 同时，还需要满足以下性能要求

1. 平均延迟和 TP999 延迟都要尽可能低
2. 可用性 5 个 9
3. 高 QPS

## 业内方案

9 种分布式 ID 解决方案：

1. 数据库自增 ID
   - 读写瓶颈
   - 单点故障风险大
2. UUID 随机数
   - 长度过长
   - 无序性
3. 雪花算法（SnowFlake）
   - 时钟回拨问题
   - workId 相同造成 id 冲突
4. 数据库多主模式
   - 集群的扩展问题
   - 未从根本上解决高并发的性能问题
5. 号段模式
   - 通过预分配号段的方式，减小了 DB 的压力，解决了并发场景的性能问题
   - 采用版本号乐观锁的方式更新，保证了并发场景下数据的准确性
6. Redis
   - 通过 incr 命令实现 ID 的原子性自增
   - redis 持久化问题
     - RDB：持久化不及时，重启后出现 ID 重复
     - AOF：重启恢复数据时间过长
7. 滴滴出品（TinyID）
   - 基于号段模式
8. 百度 （Uidgenerator）
   - 支持自定义时间戳、工作机器 ID 和序列号等各部分的位数
   - 支持用户自定义 workId 的生成策略，应用每次启动消费一个 workId
9. 美团（Leaf）
   - 同时支持号段模式和 snowflake 算法模式
   - snowflake 模式依赖 ZooKeeper 解决了时钟回拨问题
     我们主要讲下前三种，以及外研基于`号段模式` + Redis 实现的分布式 ID 系统

## 数据库自增 ID

以 MySQL 举例，利用给字段设置`auto_increment_increment`和`auto_increment_offset`来保证 ID 自增。

### 优点

- 非常简单，利用现有数据库系统的功能实现，成本小，有 DBA 专业维护。
- ID 号单调自增，可以实现一些对 ID 有特殊要求的业务。

### 缺点

- 强依赖 DB，当 DB 异常时整个系统不可用，属于致命问题。
  - 配置主从复制可以尽可能的增加可用性，但是数据一致性在特殊情况下难以保证。
  - 主从切换时的不一致可能会导致重复发号。
- ID 发号性能瓶颈限制在单台 MySQL 的读写性能。
  对于 MySQL 性能问题，可用如下方案解决：

在分布式系统中我们可以多部署几台机器，每台机器设置不同的初始值，且步长和机器数相等。
比如有两台机器，设置步长 step 为 2，TicketServer1 的初始值为 1（1，3，5，7，9，11…）、TicketServer2 的初始值为 2（2，4，6，8，10…）

## UUID

`UUID(Universally Unique Identifier)`的标准型式包含 32 个 16 进制数字，以连字号分为五段，形式为 8-4-4-4-12 的 36 个字符

示例：`550e8400-e29b-41d4-a716-446655440000`

优点：

- 性能非常高：本地生成，没有网络消耗。

缺点：

- 不易于存储：UUID 太长，16 字节 128 位，通常以 36 长度的字符串表示，很多场景不适用。
- 信息不安全：基于 MAC 地址生成 UUID 的算法可能会造成 MAC 地址泄露，这个漏洞曾被用于寻找梅丽莎病毒的制作者位置。
- ID 作为主键时在特定的环境会存在一些问题，比如做 DB 主键的场景下，UUID 就非常不适用：

**MySQL 官方有明确的建议主键要尽量越短越好，36 个字符长度的 UUID 不符合要求。**

### 优点

- 性能非常高：本地生成，没有网络消耗。

### 缺点

- 不易于存储：UUID 太长，16 字节 128 位，通常以 36 长度的字符串表示，很多场景不适用。
- 信息不安全：基于 MAC 地址生成 UUID 的算法可能会造成 MAC 地址泄露，这个漏洞曾被用于寻找梅丽莎病毒的制作者位置。
- ID 作为主键时在特定的环境会存在一些问题，比如做 DB 主键的场景下，UUID 就非常不适用：

## 雪花算法

自然界中并不存在两片完全一样的雪花

![自然界中并不存在两片完全一样的雪花](https://muyids.oss-cn-beijing.aliyuncs.com/snow-flake-bc.jpg)

`雪花算法`正如其名字，表示生成的 ID 如雪花般独一无二

### 工作原理

是一种以划分命名空间（UUID 也算，由于比较常见，所以单独分析）来生成 ID 的一种算法

以`Twitter Snowflake`为例，生成的数据为 64bit 的 long 型数据，在数据库中应该用大于等于 64bit 的数字类型的字段来保存该值，比如在 MySQL 中应该使用 BIGINT。

### Snowflake-ID 结构

`Twitter Snowflake`的`64-bit`结构

- E1-bit reserved，1bit，置为 0；
- E41-bit timestamp，41bit，表示从系统初始时间到现在的毫秒数, 可以用大概 69 年；`2 ^ 41 / 365 / 24 / 3600 / 1000 = 69.73`；
- E10-bit machine id，10bit，这个机器 id 每个业务要唯一; [机器 id 获取的策略后面会详述](#机器id获取的策略);
- E12-bit sequence，12bit，每台机器每毫秒最多产生 4096 个 id，超过这个数的话会等到下一毫秒
  ![雪花算法](https://muyids.oss-cn-beijing.aliyuncs.com/snow-flake-64-bit.jpg)

### 优势

- 毫秒数在高位，自增序列在低位，整个 ID 都是趋势递增的。
- 不依赖数据库等第三方系统，以服务的方式部署，稳定性更高，生成 ID 的性能也是非常高的。
- 可以根据自身业务特性分配 bit 位，非常灵活。

### 弊端

- **依赖机器时钟**，如果机器 **时钟回拨** ，会导致发号重复或者服务会处于不可用状态。（严重缺陷）
- 不能在一台服务器上部署多个分布式 ID 服务；(算不上缺陷，可以避免)

### 应用举例

- [MongoDB 官方文档 ObjectID](https://docs.mongodb.com/manual/reference/method/ObjectId/#description)
  - 24 长度的十六进制字符：**时间+机器码+pid+inc**（4+3+2+3）共 12 个字节
- [shardingsphere-jdbc](https://github.com/apache/shardingsphere#shardingsphere-jdbc)
  - 基于雪花算法实现，未解决`时钟回拨`问题
- [百度自研 uid-generator](https://github.com/baidu/uid-generator)
- [美团自研 Leaf](https://github.com/Meituan-Dianping/Leaf)

### 实际业务场景案例

**雪花算法二次改造案例**，引自`58沈剑《架构师之路》系列`

假设某公司 ID 生成器服务的需求如下：

1. 单机高峰并发量小于 1W，预计未来 5 年单机高峰并发量小于 10W
2. 有两个机房，预计未来 5 年机房数量小于 4 个
3. 每个机房机器数小于 100 台
4. 目前有 5 个业务线有 ID 生成需求，预计未来业务线数量小于 10 个
5. 。。。

分析过程如下：

- 高位取从**系统 ID 生成器服务上线**到现在的毫秒数，假设系统至少运行 10 年，那至少需要 10 年*365 天*24 小时*3600 秒*1000 毫秒=320\*10^9，差不多预留 39bit 给毫秒数
- 每秒的单机高峰并发量小于 10W，即平均每毫秒的单机高峰并发量小于 100，差不多预留 7bit 给每毫秒内序列号
- 5 年内机房数小于 4 个，预留 2bit 给机房标识
- 每个机房小于 100 台机器，预留 7bit 给每个机房内的服务器标识
- 业务线小于 10 个，预留 4bit 给业务线标识

这样设计的 64bit 标识，可以保证：

- 每个业务线、每个机房、每个机器生成的 ID 都是不同的
- 同一个机器，每个毫秒内生成的 ID 都是不同的
- 同一个机器，同一个毫秒内，以序列号区区分保证生成的 ID 是不同的
- 将毫秒数放在最高位，保证生成的 ID 是趋势递增的

## 外研分布式 ID 服务

### 思维导图

![外研分布式ID服务-思维导图](https://muyids.oss-cn-beijing.aliyuncs.com/fltrp-id-service.png)

### 场景

对外提供全局独立唯一 ID

- 支持单个、批量不同数量的 ID 获取
- 支持单调递增、趋势递增不同特性的 ID 获取

### 业务流程

![业务流程图](https://muyids.oss-cn-beijing.aliyuncs.com/id-only_flowchart.png)

### 核心服务

1. id 发号器
2. id 池定时轮询器

### 存储设计

应用配置存储（支持高性能查询）+ 缓存 id 池（支持高性能读取、写入）

#### 应用配置存储设计

mysql 存储 + redis 缓存优化读取性能，注意 数据一致性

#### 缓存 id 池设计

id 池要实现高性能读取和写入，我们选择了 redis 作为底层数据存储

对于数据结构选择，redis 常用容器类型有 hash、list、set、zset，选择哪一个更为合适呢

考虑到要支持**单调递增模式**，严格要求顺序性，list 和 zset 都能实现顺序性，究竟该选择哪一个？

我们知道 zset 可以根据权值实现顺序性，但是其底层实现为跳表，其查询、插入、删除的时间复杂度为 O(logn)，不满足我们对高性能的要求，故选择 list

##### 发号策略

list 中维护了从小到大的预生成 ID 队列，遵循`FIFO`规则，不管是单个还是批量，直接从队头获取

##### 更新策略

我们使用**号段模式**作为 id 的生成方式，每次从 currentOffset 算法生成 满足 单调递增 or 趋势递增的 ID 序列，执行入队操作

- 单调递增：不定增率，有序入队
- 趋势递增：增率为 1，shuffle 后入队
  入队操作完成后，同步更新缓存配置，再异步更新 db 配置

##### 问题思考

**分布式场景下，缓存 id 池的写入操作，会不会造成重复发号、id 池溢出等问题？**

必须配置**分布式锁机制**，保证全局串行化，即某一时刻，只允许一个 ID 生成器的 worker 在工作

**批量获取数量大于缓存池大小（缓存池被过度消费），如何处理？**

1. 理论上不会出现这种情况
   1. 系统预留 1 分钟的最大秒并发数（目前默认 5000），
   2. 定时任务每隔 100ms 扫描，低于最大池的 80%，进行补充
2. 如果异常发生，返回空；同时应触发**报警机制**

### web 层

[接口文档](http://wiki.ai.fltrp.im/id-only/API%E6%96%87%E6%A1%A3.html)

### 数据层

[表结构设计](http://wiki.ai.fltrp.im/id-only/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%AE%BE%E8%AE%A1.html)

#### 应用表示

- appKey：应用的唯一 key
- appSecret：应用秘钥
- appName：应用名称

#### ID 的增长方式

- 趋势递增 trend
- 严格递增(单调递增) monotony

#### ID 的分配范围配置

- startOffset 初始化的 id 起始位置
- step 每次向 id 池子增加的数量
- currentOffset id 的当前位置

#### 缓存 ID 池配置

- maxSizePerTimes 一次最大获取 id 量(默认 1000)
- maxSizePerSecond 1s 最大获取量(秒级并发 QPS，默认 5000)
- minSizePercent 触发添加的百分比上限（默认 80%）
- interval 循环添加间隔时间 10ms（不可修改)
- maxPoolSize id 池的最大 id 存量（系统默认是`maxSizePerSecond`的`60`倍，为了保证`1分钟`不断供）

### 我们做到了

- 一致性，服务端保证不会获取到重复的 ID
- 两种递增方式支持，趋势递增+严格递增
- 高可用，短 ID 服务允许部署多套完全独立的环境，每个环境产生的 ID 都不一样，client 可以 failover 到任何环境
- 高性能，每秒钟可以获取百万级的 ID，并且不会出现阻塞
- 基于时间的大致有序，基本上获取到的 ID 会越来越大，无法保证严格有序，比如一小时前获取的 ID 应该会比一小时后的小

### 我们不支持

- 没有实现严格自增长 ID
- 无法保证每个 ID 都不浪费

## 参考文档

- [snowflake](https://github.com/twitter-archive/snowflake)
- [A Universally Unique IDentifier (UUID) URN Namespace](https://www.ietf.org/rfc/rfc4122.txt)
- [Ticket Servers: Distributed Unique Primary Keys on the Cheap](http://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/)
- [Leaf](https://github.com/Meituan-Dianping/Leaf)
