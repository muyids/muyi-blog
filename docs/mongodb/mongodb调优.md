---
title: mongodb基础
date: 2016-06-10T00:00:00+08:00
categories: [数据库, mongodb]
tags: [数据库, mongodb]
---

总结了`MongoDB 性能优化`的几个点，遇到 mongodb 的性能问题时，可以按照如下步骤排查，希望能够有所帮助。

<!--more-->

## 查看 Process 信息

```
db.currentOp()
```

- 强制结束请求

`db.currentOp()`找出一直没结束的请求的 opid（currentOp.opid 字段)，然后 db.killOp(opid)来杀掉对应的请求。

## 找出慢语句 - 优化器 profile

一般来说查询语句太慢和性能问题瓶颈有着直接的关系，找出这些慢语句对于定位线上产品问题至关重要

- 在 MySQL 中，慢查询日志是经常作为我们优化数据库的依据
- 在 MongoDB 中是否有类似的功能呢？答案是肯定的，那就是 MongoDB Database Profiler。
  `db.getProfilingLevel()`命令来获取当前的 Profile 级别

profile 的级别可以取 0，1，2 三个值，他们表示的意义如下：

- 0 – 不开启
- 1 – 记录慢命令 (默认为>100ms)
- 2 – 记录所有命令

有两种方式可以控制 Profiling 的开关和级别

- 第一种是直接在启动参数里直接进行设置。
  启动 MongoDB 时加上–profile=级别 即可。
- 在客户端调用 db.setProfilingLevel(级别) 命令来实时配置，Profiler 信息保存在 system.profile 中。我们可以通过 db.getProfilingLevel()命令来获取当前的 Profile 级别，类似如下操作： - db.setProfilingLevel(2);
  查询慢 sql

```
db['system.profile'].find()
```

与 MySQL 的慢查询日志不同，MongoDB Profile 记录是直接存在系统 db 里的，记录位置 system.profile ，所以，我们只要查询这个 Collection 的记录就可以获取到我们的 Profile 记录了。列出执行时间长于某一限度(5ms)的 Profile 记录：

```
db.system.profile.find( { millis : { $gt : 5 } } )
```

查看最新的 Profile 记录：

```
db.system.profile.find().sort({$natural:-1}).limit(1)
```

## 使用 explain 分析

通过使用 [explain](http://docs.mongodb.org/manual/reference/method/cursor.explain/) 来对这些慢语句进行诊断。此外还可以 mtools 来分析日志。

explain 在写代码阶段就可以做性能分析，开发阶段用

```
db.usermodels.find({}).explain()
```

MongoDB 提供了一个 explain 命令让我们获知系统如何处理查询请求。利用 explain 命令，我们可以很好地观察系统如何使用索引来加快检索，同时可以针对性优化索引。

```
db.t5.ensureIndex({name:1})
db.t5.ensureIndex({age:1})
db.t5.find({age:{$gt:45}}, {name:1}).explain()
	  {
	      "cursor" : "BtreeCursor age_1",
	      "nscanned" : 0,
	      "nscannedObjects" : 0,
	      "n" : 0,
	      "millis" : 0,
	      "nYields" : 0,
	      "nChunkSkips" : 0,
	      "isMultiKey" : false,
	      "indexOnly" : false,
	      "indexBounds" : {
	      "age" : [
	                    [45,1.7976931348623157e+308]
	                ]
	       }
	  }
```

字段说明:

- cursor: 返回游标类型(BasicCursor 或 BtreeCursor)
- nscanned: 被扫描的文档数量
- n: 返回的文档数量
- millis: 耗时(毫秒)
- indexBounds: 所使用的索引

## 创建索引

分析完之后需要创建新的索引 (index) 来提升查询的性能。别忘了在 MongoDB 中可以在后台创建索引以避免 collections 锁和系统崩溃。

## 使用稀疏索引来减少空间占用

如果使用 sparse documents，并重度使用关键字 $exists，可以使用 sparse indexes 来减少空间占用提升查询的性能。

## 分析 mongodb 性能瓶颈

连接数，CPU，IOPS 等，保证资源充分利用

## 读写分离

如果读写都在主节点的话，从节点就一直处在空置状态，这是一种浪费。
对于报表或者搜索这种读操作来说完全可以在从节点实现，因此要做的是在 connection string 中设置成 secondarypreferred。

## 扬长避短

利用 mongodb 的写入优势，
避免其他鸡肋功能的使用，如聚合计算、ttl、固定集合等

## 题外话

当 mongodb 性能充分使用，使用如下方法：

- 修改查询逻辑，优化 schema；
- 增加缓存
