---
title: 数据库知识点总结
date: 2018-03-31T00:00:00+08:00
categories: [数据库]
tags: [数据库]
draft: true
---

- [B-Tree 和 B+Tree 的区别](#B-Tree和B+Tree的区别)
- [聚簇索引和非聚簇索引](#聚簇索引和非聚簇索引)
  数据库的隔离级别，MySQL 怎么解决幻读问题的？
  ？B+Tree 的优势
  B+ 树数据都存放在叶子节点，非叶子节点只存放索引，B+树更少得磁盘 IO

联合索引、最左匹配原则

你项目中数据库表是怎么设计的，数据库三范式知道吗？
介绍下数据库的锁，你在项目中是怎么用的？
索引有哪些实现方式？说说他们的优缺点
MySQL 一般用的什么索引？介绍下......为什么不用 Hash 索引？
B+ 树

十一、举出几个 你做过的分库分表的实例。
十二、你通常是如何优化 mysql 的查询？
十三、你们项目中用到了 redis 的那些方法，set 和 mset 的区别？
十四、Mysql 的索引是如何实现的。
十五、举例写出一个 Mysql 储存过程和一个事务。

---

## B-Tree 和 B+Tree 的区别

## 数据库

- [事务的四大特征 ACID](#事务的四大特征ACID)
- [CAS 算法](#CAS算法)

## CAS 算法

campare and set

CAS 有 3 个操作数，内存值 V，旧的预期值 A，要修改的新值 B。
当且仅当预期值 A 和内存值 V 相同时，将内存值 V 修改为 B，否则什么都不做。
这个过程是原子性的。

乐观锁用到的就是 CAS 算法

findAndUpdate 操作 就是 CAS 算法

update xxxx where xx = ? 就是 CAS 算法

---

乐观锁不能解决脏读

---

### 数据库

- 用过哪些数据库（MySQL、MongoDB、Redis）

- MySQL 查询优化、索引、索引的原理

- MySQL 库设计一个简单的论坛系统，画出用户表、帖子表、评论表的 er 图，

  当用户量很大时，如何优化，缓存最多存一万条数据时如何优化(使用 LRU 缓存)

- MySQL 的配置文件改过哪些参数

- MySQL 及 MongoDB 如何选择，选择的标准是什么

- MongoDB 的聚合函数，用到过哪些参数

- MongoDB 的几种索引，数据量特别大时的分片

- 数据库的灾备（MySQL、MongoDB）

## InnoDB 的隔离级别

## mongodb 和 mysql 的区别

### mysql

1. mysql 是关系型数据库
2. 在不同的引擎上有不同的存储方式。常用的是 InnoDB，支持事务
3. 查询语句是使用传统的 sql 语句，拥有较为成熟的体系，成熟度很高。
4. 开源数据库的份额在不断增加，mysql 的份额也在持续增长。
5. 缺点就是在海量数据处理的时候效率会显著变慢。

## mongodb

1. 非关系型数据库(nosql), 属于文档型数据库。可以存放 xml、json、bson 类型的数据
2. 这些数据具备自述性（self-describing），呈现分层的树状数据结构。数据结构由键值(key=>value)对组成。
3. 存储方式：虚拟内存+持久化。
4. 查询语句：是独特的 Mongodb 的查询方式。可以写 javascript 脚本查询
5. 适合场景：事件的记录，内容管理或者博客平台等等。
6. 架构特点：可以通过副本集，以及分片来实现高可用。
7. 数据处理：数据是存储在硬盘上的，只不过需要经常读取的数据会被加载到内存中，将数据存储在物理内存中，从而达到高速读写。
8. 成熟度与广泛度：新兴数据库，成熟度较低，Nosql 数据库中最为接近关系型数据库，比较完善的 DB 之一，适用人群不断在增长。
   优势：

9. 快速。在适量级的内存的 Mongodb 的性能是非常迅速的，它将热数据存储在物理内存中，使得热数据的读写变得十分快，
10. 高扩展！
11. 自身的 Failover 机制（失效转移）
12. json 的存储格式
    缺点：主要是无事物机制！(4.0 以后已加入事务机制)

分析一下 Mysql 和 Mongodb 应用场景

1. 如果需要将 mongodb 作为后端 db 来代替 mysql 使用，即这里 mysql 与 mongodb 属于平行级别，那么，这样的使用可能有以下几种情况的考量:

- mongodb 所负责部分以文档形式存储，能够有较好的代码亲和性，json 格式的直接写入方便。(如日志之类)
- 从 data models 设计阶段就将原子性考虑于其中，无需事务之类的辅助。开发用如 nodejs 之类的语言来进行开发，对开发比较方便。
- mongodb 本身的 failover 机制，无需使用如 MHA 之类的方式实现。

2. 将 mongodb 作为类似 redis，memcache 来做缓存 db，为 mysql 提供服务，或是后端日志收集分析。
   考虑到 mongodb 属于 nosql 型数据库，sql 语句与数据结构不如 mysql 那么亲和 ，也会有很多时候将 mongodb 做为辅助 mysql 而使用的类 redis memcache 之类的缓存 db 来使用。
   亦或是仅作日志收集分析。

## 数据一致性，高可用性，性能的矛盾

1）要想让数据有高可用性，就得写多份数据
2）写多份的问题会导致数据一致性的问题
3）数据一致性的问题又会引发性能问题
强一致性必然导致性能短板, 而弱一致性则有很好的性能但是存在数据安全(灾备数据丢失)/一致性(脏读/脏写等)的问题.
目前 Node.js 业内流行的主要是与 Mongodb 配合, 在数据一致性方面属于短板.

## 事务

事务在分布式的问题中可以称为 "两阶段提交"

第一阶段：

协调者会问所有的参与者结点，是否可以执行提交操作。
各个参与者开始事务执行的准备工作：如：为资源上锁，预留资源，写 undo/redo log……
参与者响应协调者，如果事务的准备工作成功，则回应“可以提交”，否则回应“拒绝提交”。

第二阶段：

如果所有的参与者都回应“可以提交”，那么，协调者向所有的参与者发送“正式提交”的命令。参与者完成正式提交，并释放所有资源，然后回应“完成”，协调者收集各结点的“完成”回应后结束这个 Global Transaction。
如果有一个参与者回应“拒绝提交”，那么，协调者向所有的参与者发送“回滚操作”，并释放所有资源，然后回应“回滚完成”，协调者收集各结点的“回滚”回应后，取消这个 Global Transaction。
异常:

如果第一阶段中，参与者没有收到询问请求，或是参与者的回应没有到达协调者。那么，需要协调者做超时处理，一旦超时，可以当作失败，也可以重试。
如果第二阶段中，正式提交发出后，如果有的参与者没有收到，或是参与者提交/回滚后的确认信息没有返回，一旦参与者的回应超时，要么重试，要么把那个参与者标记为问题结点剔除整个集群，这样可以保证服务结点都是数据一致性的。
第二阶段中，如果参与者收不到协调者的 commit/fallback 指令，参与者将处于“状态未知”阶段，参与者完全不知道要怎么办。

## 事务的四大特征 ACID

原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）

- 原子性（Atomicity)
  要么全部成功,要么全部失败.不可能只执行一部分操作.
- 一致性（Consistency）
  系统(数据库)总是从一个一致性的状态转移到另一个一致性的状态,不会存在中间状态.
- 隔离性（Isolation）
  通常来说:一个事务在完全提交之前,对其他事务是不可见的.也有例外情况
- 持久性（Durability）
  一旦事务提交,那么就永远是这样子了,哪怕系统崩溃也不会影响到这个事务的结果

## CAS

compare and swap

先比较，看是否是旧值，再交换成新值

## ABA 问题

CAS 不能防止 ABA 问题。
ABA 问题。（一个值从 A 变成 B，又更新回 A，普通 CAS 会误判通过检测。利用版本号机制可以解决 ABA 问题。）
