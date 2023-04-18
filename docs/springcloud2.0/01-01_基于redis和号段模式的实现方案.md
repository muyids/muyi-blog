## 基于 Redis 和号段模式的分布式 id 实现方案

利用 redis 原子性和号段模式的高性能实现的分布式 id 方案

### 思维导图

![外研ID服务](https://muyids.oss-cn-beijing.aliyuncs.com/外研ID服务.png)

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

### 数据库设计

```sql
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime NOT NULL COMMENT '修改时间',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `deleted_at` bigint(16) DEFAULT '0' COMMENT '删除时间（0:有效）',
  `entity_key` varchar(64) NOT NULL COMMENT '实体标识的唯一key',
  `entity_name` varchar(64) NOT NULL COMMENT '实体名称描述',
  `increasing_type` int(2) NOT NULL DEFAULT 1 COMMENT '递增类型(1:单调递增;2:严格递增) 默认为:1',
  `start_offset` bigint(16) DEFAULT '0' COMMENT '初始化的id起始位置',
  `step` int(11) DEFAULT '1000' COMMENT '每次向id池子增加的数量',
  `current_offset` bigint(16) DEFAULT '0' COMMENT 'id的当前位置',
  `max_size_per_times` int(11) DEFAULT '0' COMMENT '一次最大获取id量',
  `max_size_per_second` int(11) DEFAULT '0' COMMENT '1s最大获取量(秒级并发QPS)',
  `min_size_percent` int(11) DEFAULT '0' COMMENT '触发添加的百分比上限',
  `interval` int(11) DEFAULT '0' COMMENT '循环添加间隔时间ms（不可修改)',
  `max_pool_size` int(11) DEFAULT '0' COMMENT 'id池的最大id存量（系统默认是maxSizePerSecond的300倍，为了保证5分钟不断供）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `entity_key` (`entity_key`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
```

初始化实体

比如 user 实体

start_offset : 100000 // id 从 100000 开始
step : 1000 // 每次向 id 池子增加 1000 个
current_offset : // id 的当前位置
max_size_per_times : // 一次最大获取 id 量 : 防止 id 获取
max_size_per_second : // 1s 最大获取量(秒级并发 QPS)；防止恶意请求

当前 id 池中 id 的库存数量 少于 max_pool_size \* min_size_percent / 100 时，向 id 池中增加 step 个 id

max_pool_size \* (1-min_size_percent / 100) 应满足 大于等于 step

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
