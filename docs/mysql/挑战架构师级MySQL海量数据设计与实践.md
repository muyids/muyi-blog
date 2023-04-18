[我的已购](https://e.naixuejiaoyu.com/bought)

https://www.bilibili.com/video/BV1P64y167Fd?p=1

---

### mysql 的架构设计

![2021-07-16 am9.37.23](https://muyids.oss-cn-beijing.aliyuncs.com/20210716102259680.png)

- 客户端
- server
  - 连接器：查询缓存
  - 分析器
  - 查询优化器
  - 执行器：->binlog cache -> binlog file
- 存储引擎
  - innodb
    - Buffer pool -> page
    - Undo log
    - Redo log
  - myisam

### Mysql 存储引擎 innodb 存储原理

两类文件

- .frm 文件(framework)保存 表结构
- .ibd 文件保存 索引+数据
  数据页：

- 页（Pages）是 InnoDB 中管理数据的最小单元

- `.ibd`文件中的数据以页的形式保存；

- 页与页之间是通过**双向链表**连接起来，而存储在页中的一行一行的数据则是通过**单链表**连接起来

页的组成：Innodb 单页数据页的大小为 16KB，由以下七部分组成：

- 文件头：38 字节，包含页空间大小，页的位置，页的类型，上下页的地址（双链表），LSN
- 页头：56 字节；slot 数量，第一条记录指针，记录数量，最后一条被插入记录的指针，索引 ID（属于哪个索引），当前页在索引中的层级，标记为删除的记录所占字节数...
- 虚记录：最大虚记录和最小虚记录。
- 记录堆：行记录存储区，分为有效记录、自由空间链表（已删除记录链接的链表）。
- 未分配空间：页面未使用的存储空间。
- slot 区：辅助链表进行二分查找
- 页尾：页面最后部分，占 8 个字节，主要存储页面的校验信息

![20201123182104537](https://muyids.oss-cn-beijing.aliyuncs.com/20201123182104537-6850836.png)

页内记录维护（顺序保证、插入策略、页内查询）：

- 顺序保证：

        - 逻辑有序（单向链表）而不是物理有序
        - 插入效率高，链表查询效率怎么保证？

- 插入策略：

        - 自由空间链表 -- 优先

  - 未分配空间
    注意：删除操作频繁的话也会产生磁盘碎片，因为记录的长度不一定相等（varchar 之类），所以也要定期做**表碎片整理**

- 页内查询：

  - slot 辅助链表进行二分查找

### innodb 内存管理机制

> 全表扫描对内存有什么影响？如何避免热数据被淘汰？没有空闲页怎么办？

![2021-08-17 am9.10.19](https://muyids.oss-cn-beijing.aliyuncs.com/2021-08-17 am9.10.19.png)

内存：缓冲池 buffer pool -- 一片连续的内存空间

磁盘：页为单位

内存管理

- 缓冲池技术
  - free list : free page （空闲页）
  - flush list: 刷盘，dirty page（脏页）
  - lru list: clean page（数据页） + dirty page
- 页面管理
  - 空闲页
  - 数据页
  - 脏页
- 数据淘汰
  - LRU 算法
  - 新生代、老生代；midpoint， 5：3
  - 老生代停留时间窗口机制： **满足** “被访问” 并且 “在老生代停留时间” 大于 T，被移到新生代头部；
    页面装载：磁盘数据到内存

1. 先从 free list 取一个 free page，写入 page；然后写入 lru list 老生代
2. free list 没有空闲页怎么办？-> 从 lru list 中淘汰，如果 尾部被锁住怎么办？-> 从 flush list 取
   ![2021-07-19 pm8.51.43](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm8.51.43.png)

### [InnoDB 脏页刷新机制 Checkpoint](https://www.cnblogs.com/olinux/p/5196139.html)

- 脏页：InnoDB 采用 Write Ahead Log 策略来防止宕机数据丢失，即事务提交时，先写重做日志，再修改内存数据页，这样就产生了脏页
- 脏页刷新：redo log 不能无限大，宕机时重做全部日志恢复时间太长；buffer pool 也不能无限大；所以，脏页要刷入磁盘
- Checkpoint：当数据库宕机时，数据库不需要重做所有的日志，只需要执行上次刷入点之后的日志。这个点就叫做 Checkpoint
- 两种 Checkpoint
  - Sharp Checkpoint：关闭数据库时，将所有脏页刷回磁盘
  - Fuzzy Checkpoint：部分脏页的刷新
    - Master Thread Checkpoint ： Master Thread 以每秒或每十秒的速度从缓冲池的脏页列表中刷新一定比例的页回磁盘
    - FLUSH_LRU_LIST Checkpoint：InnoDB 要保证 LRU 列表中有 100 左右空闲页可使用
    - Async/Sync Flush Checkpoint ： 重做日志文件不可用时，需要强制将脏页列表中的一些页刷新回磁盘
    - Dirty Page too much Checkpoint：脏页数量太多

---

### 事务

### 事务的基本概念

事务特性 ACID

A：原子性 （undo log）

C：一致性；只要 AID 保证，C 就保证了

I：隔离性（mvcc）

D：持久性 (内存+redo log 刷盘)

并发问题：

- 脏读：读到了未提交的

- 不可重复读：两次读到的结果不同

- 幻读：

隔离级别：

- 读未提交：会读取到其他事务未提交的数据；脏读
- 读已提交：会读取到其他事务已提交的数据；不可重复读
- 可重复读：每次读取相同结果集，不管其他事务是否提交；幻读
- 串行化：

## 事务实现原理

- MVCC
  - 多版本并发控制
  - 解决读-写冲突
  - 隐藏列：trx_id, roll_ptr, 隐藏 id
  - 当前读，快照读
- undo log ：事务回滚
- redo log : 事务固化

### MVCC 是什么；MVCC 如何实现多版本控制？如何解决读写冲突？

https://zhuanlan.zhihu.com/p/52977862

- MVCC 多版本并发控制机制：实现读取数据不用加锁， 可以让读取数据同时修改。修改数据时同时可读取。
- 用于实现提交读（RC）和可重复读(RR)这两种隔离级别
- MVCC 是通过保存数据在某个时间点的快照来实现该机制，其在每行记录后面保存两个隐藏的列，分别保存这个行的创建版本号和删除版本号，然后 Innodb 的 MVCC 使用到的快照存储在 undo log 中，该日志通过回滚指针把一个数据行所有快照连接起来。

实现方式：

- 隐藏列：

  - trx_id: 事务版本号；自增长的事务 ID，判断事务的执行先后顺序。
  - db_roll_ptr: 上一版本数据在 undo log 里的位置指针
  - 隐藏 id：创建表没有合适索引作为聚集索引时，用该隐藏 ID 创建聚集索引

- Undo log ：记录数据被修改之前的日志

  ![2021-07-19 pm9.27.57](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.27.57.png)

- Read view：一致性视图

  ① 当事务第一次执行**查询 sql**时会生成一致性视图 read-view

  ②Read view 由 所有未提交事务 ID 数组(数组里最小的 ID 为 min_id)和已创建的最大事务 id(max_id)组成

  ③ 查询的数据结果需要跟 read-view 做比较从而得到快照结果

  ![img](/Users/dw/Documents/Pictures/blog/v2-fef7954f5e3c7713f48b35597e7f9fb8_1440w-20210717135039397.jpg)

  已提交读和可重复读的区别就在于它们生成 ReadView 的策略不同。

  ReadView 中主要就是有个列表来存储我们系统中当前活跃着的读写事务，也就是 begin 了还未提交的事务。通过这个列表来判断记录的某个版本是否对当前事务可见。其中最主要的与可见性相关的属性如下：

  **up_limit_id**：当前已经提交的事务号 + 1，事务号 < up_limit_id ，对于当前 Read View 都是可见的。理解起来就是创建 Read View 视图的时候，之前已经提交的事务对于该事务肯定是可见的。

  **low_limit_id**：当前最大的事务号 + 1，事务号 >= low_limit_id，对于当前 Read View 都是不可见的。理解起来就是在创建 Read View 视图之后创建的事务对于该事务肯定是不可见的。

  **trx_ids**：为活跃事务 id 列表，即 Read View 初始化时当前未提交的事务列表。所以当进行 RR 读的时候，trx_ids 中的事务对于本事务是不可见的（除了自身事务，自身事务对于表的修改对于自己当然是可见的）。理解起来就是创建 RV 时，将当前活跃事务 ID 记录下来，后续即使他们提交对于本事务也是不可见的。

  已提交读隔离级别下的事务在每次查询的开始都会生成一个独立的 ReadView，而可重复读隔离级别则在第一次读的时候生成一个 ReadView，之后的读都复用之前的 ReadView

总结：MVCC：通过版本链，实现多版本，可并发读-写，写-读。通过 ReadView 生成策略的不同实现不同的隔离级别。

https://zhuanlan.zhihu.com/p/66791480

https://zhuanlan.zhihu.com/p/340600156

### 回滚日志 undo log 如何实现多版本控制与保证事务原子性？

谈到 undo log 就不得不提 innodb 中数据行的隐藏列：tx_id, roll_pointer, 隐藏 id;

tx_id 表示事务序列号，自增; roll_pointer 是回滚指针，指向这条记录的上一个版本；

undo log 保存了所有修改记录的快照，根据 roll_pointer 以链表形式串联；

当有事务对数据进行操作时，首先将当前数据记录到 undo log，然后修改当前数据为最新，并将 roll_pointer 指向 undo log 中保存的上一版本数据；

### undo log 如何清理？为什么 InnoDB count(\*) 这么慢？

readview 重 最小事务 ID 的

![2021-07-19 pm9.29.31](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.29.31.png)

### 重做日志 redo log 如何实现事务持久性

![2021-07-19 pm9.31.12](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.31.12.png)

![2021-07-19 pm9.33.22](/Users/dw/Documents/Pictures/blog/2021-07-19%20pm9.33.22.png)

![2021-07-19 pm9.36.19](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.36.19.png)

redo log 记录了数据操作在物理层面的修改，mysql 中使用了大量缓存，缓存存在于内存中，修改操作时会直接修改内存，而不是立刻修改磁盘，当内存和磁盘的数据不一致时，称内存中的数据为脏页(dirty page)。为了保证数据的安全性，事务进行中时会不断的产生 redo log，在事务提交时进行一次 flush 操作，保存到磁盘中, redo log 是按照顺序写入的，磁盘的顺序读写的速度远大于随机读写。当数据库或主机失效重启时，会根据 redo log 进行数据的恢复，如果 redo log 中有事务提交，则进行事务提交修改数据。这样实现了事务的原子性、一致性和持久性。

### InnoDB 的锁机制和原理；锁种类、加锁过程，常见的锁有哪些？

![2021-07-19 pm9.39.52](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.39.52.png)

![2021-07-19 pm9.40.58](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.40.58.png)

![2021-07-19 pm9.47.55](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.47.55.png)

表级锁：

- 全表扫描 相当于”表锁“

![2021-07-19 pm9.51.28](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-19 pm9.51.28.png)

### innodb 中 行级锁，间隙锁，表级锁 是如何实现的

### innodb 是如何实现加锁过程的

![2021-07-19 pm9.52.47](/Users/dw/Documents/Pictures/blog/2021-07-19%20pm9.52.47.png)

### mysql 是如何查找数据的？

https://zhuanlan.zhihu.com/p/339183789

1.首先客户端通过 tcp/ip 发送一条 sql 语句到 server 层的 SQL interface
2.SQL interface 接到该请求后，先对该条语句进行解析，验证权限是否匹配 3.验证通过以后，分析器会对该语句分析,是否语法有错误等 4.接下来是优化器器生成相应的执行计划，选择最优的执行计划 5.之后会是执行器根据执行计划执行这条语句。在这一步会去 open table,如果该 table 上有 MDL，则等待。
如果没有，则加在该表上加短暂的 MDL(S)
(如果 opend_table 太大,表明 open_table_cache 太小。需要不停的去打开 frm 文件) 6.进入到引擎层，首先会去 innodb_buffer_pool 里的 data dictionary(元数据信息)得到表信息 7.通过元数据信息,去 lock info 里查出是否会有相关的锁信息，并把这条 update 语句需要的
锁信息写入到 lock info 里(锁这里还有待补充) 8.然后涉及到的老数据通过快照的方式存储到 innodb_buffer_pool 里的 undo page 里,并且记录 undo log 修改的 redo
(如果 data page 里有就直接载入到 undo page 里，如果没有，则需要去磁盘里取出相应 page 的数据，载入到 undo page 里) 9.在 innodb_buffer_pool 的 data page 做 update 操作。并把操作的物理数据页修改记录到 redo log buffer 里
由于 update 这个事务会涉及到多个页面的修改，所以 redo log buffer 里会记录多条页面的修改信息。
因为 group commit 的原因，这次事务所产生的 redo log buffer 可能会跟随其它事务一同 flush 并且 sync 到磁盘上 10.同时修改的信息，会按照 event 的格式,记录到 binlog_cache 中。(这里注意 binlog_cache_size 是 transaction 级别的,不是 session 级别的参数,
一旦 commit 之后，dump 线程会从 binlog_cache 里把 event 主动发送给 slave 的 I/O 线程) 11.之后把这条 sql,需要在二级索引上做的修改，写入到 change buffer page，等到下次有其他 sql 需要读取该二级索引时，再去与二级索引做 merge
(随机 I/O 变为顺序 I/O,但是由于现在的磁盘都是 SSD,所以对于寻址来说,随机 I/O 和顺序 I/O 差距不大) 12.此时 update 语句已经完成，需要 commit 或者 rollback。这里讨论 commit 的情况，并且双 1
13.commit 操作，由于存储引擎层与 server 层之间采用的是内部 XA(保证两个事务的一致性,这里主要保证 redo log 和 binlog 的原子性),
所以提交分为 prepare 阶段与 commit 阶段
14.prepare 阶段,将事务的 xid 写入，将 binlog_cache 里的进行 flush 以及 sync 操作(大事务的话这步非常耗时)
15.commit 阶段，由于之前该事务产生的 redo log 已经 sync 到磁盘了。所以这步只是在 redo log 里标记 commit 16.当 binlog 和 redo log 都已经落盘以后，如果触发了刷新脏页的操作，先把该脏页复制到 doublewrite buffer 里，把 doublewrite buffer 里的刷新到共享表空间，然后才是通过 page cleaner 线程把脏页写入到磁盘中

### binlog, redo log, undo log 都是啥

binlog：主从复制

redo log： 持久性；

undo log 的作用：1.事务回滚；2.MVCC 中的快照读

### RR 和 RC 隔离级别下的 InnoDB 快照读有什么区别

- RR 隔离级别下，当事务第一次进行快照读，仅此一次创建 read-view 视图，所以 read-view 中的未提交事务数组和最大事务 ID 始终保持不变，因此每次读取时只会读取事务之前的数据
- 而在 RC 隔离级别下，每次事务进行快照读时，都会生成 read-view 视图，导致在 RC 隔离级别下事务可以看到其他事务修改后的数据，这也是导致不可重复的原因
  总之在 RC 隔离级别下，是每个快照读都会生成并获取最新的 Read View；而在 RR 隔离级别下，则是同一个事务中的第一个快照读才会创建 Read View, 之后的快照读获取的都是同一个 Read View。

---

模块二：千亿级海量数据分库分表方法论

1. 在海量数据和高并发场景下如何进行主键设计

2. 聚簇索引、二级索引和联合索引 具备哪些特点？

   聚簇索引：叶子节点存储的是 主键索引+数据

   二级索引：叶子节点 存储的是 二级索引+主键

   联合索引：多列组合成索引，叶子存储 索引 + 主键

   ![2021-07-20 pm8.23.27](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm8.23.27.png)

3. 在进行索引优化时应注意哪些问题？

   ![2021-07-20 pm8.31.42](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm8.37.18.png)

主键选择：

- 自增主键，顺序写入，效率高
- 随机主键，节点分裂，数据移动 -- IO 开销大
  联合索引的使用：

- 按索引区分度排序
- 覆盖索引
- 索引下推

字符串索引：

- 设置合理长度
- 不支持%开头的模糊查询

### 什么情况下会导致索引失效？

索引失效问题分析：

- 隐式类型转换；where mobile="188xxxx1234"; where mobile=188xxxx1234;
  - 如何避免：跑个查询计划看一看，有没有命中索引
- 索引列查询包含计算
- 数据范围影响；索引区分度过低，条件超出索引范围，造成索引失效；
- A=xx or B=xx ； -- 5.1 开始，引入 Index Merge（索引合并）技术，对同一个表可以使用多个索引分别扫描

### mysql 如何进行优雅的库表设计？

- 联合索引： 优于多列独立索引
- 索引顺序：
  ![2021-07-20 pm9.15.15](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm9.15.15.png)

![2021-07-20 pm9.17.52](/Users/dw/Documents/Pictures/blog/2021-07-20%20pm9.17.52-6787338.png)

![2021-07-20 pm9.19.01](/Users/dw/Documents/Pictures/blog/2021-07-20%20pm9.19.01-6787348.png)

### 海量数据和高并发场景下如何实现优雅的分库分表方案？

![2021-07-20 pm9.24.03](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm9.24.03.png)

### 不同场景下的分库分表的落地方案有哪些？

- 用户库分表

  UID ，Phone(index) 用户 + 手机号
  一对一 ： 映射表

- 商品库分表

  UID，PID（index） 用户发布商品

  一对多 ： 基因法

![2021-07-20 pm9.38.52](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm9.38.52.png)

- 消息系统库分表
  - 时效性强
  - 冷热数据拆分

### 分库分表时，分表分少了怎么进行处理？

![2021-07-20 pm9.53.54](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-20 pm9.53.54.png)

---

模块三：真实案例实战篇

### 数据库扩展会带来哪些问题？

- 请求路由
  - 分表规则
  - 写入路由
  - 查询路由
- 分布式事务（业务规避！！）
  - 不管什么方案，最终都要人工介入对齐数据
    分页查询怎么办？（join 连接查询不考虑，业务上避免)

分库分表解决方案-请求路由

- Sharding JDBC - 客户端集成 - 去中心化 - 稳定性
- Sharding Proxy - 代理模式 - 中心化 - 方便运维
- 混合模式

### 如何实现千亿级电商商品数据与推送数据 水平拆分？

### 如何实现万亿级 微信消息垂直拆分？

### 企业级数据库 Sharding Sphere 是如何实现分库分表的？

### 分布式事务

- 强一致性

  - 一致性协议
    - 2PC ： 出错的概率很低，+人工介入，可以落地生产
    - 3PC ： 过程太漫长
  - 落地方案
    - XA 规范
      - 资源管理器 - 事务参与者
      - 事务管理器 - 事务协调者

- 柔性事务（最终一致性）

  - TCC（Try-Confirm-Cancel）
    - 尝试执行业务，预留资源
    - 确认执行业务，使用 Try 阶段资源
    - 取消执行业务，释放 Try 阶段预留的资源
  - SAGA 模型
    - 一个分布式事务拆分为多个本地事务
    - 本地事务都有相应的执行模块和补偿模块
    - 事务管理器负责在事务失败时调度执行补偿逻辑

- 事务消息

  - 简化了分布式事务模型
  - 对业务友好
    本质：两次 RPC 拆成了 一次 RPC+ 事务消息

2PC

![2021-07-21 pm8.18.22](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 pm8.18.22.png)

3PC

![2021-07-21 pm8.25.54](https://muyids.oss-cn-beijing.aliyuncs.com/2021-07-21 pm8.25.54.png)

### 强一致性协议落地方案有哪些？

### 最终一致性方案 TCC 与 SAGA 模型是如何处理的

### Seata 分布式事务的工作流程

### Seata 中 AT 模式的 核心设计与执行流程

- 一种无侵入的分布式事务解决方案，2PC 的广义实现
- 源于阿里云 GTS AT 模式的开源版
  一阶段：

- 拦截 业务 SQL
- 生成前镜像
- 生成后镜像
