---
title: 使用redis统计独立用户访问量
date: 2019-06-29T00:00:00+08:00
categories: [redis, 系统设计]
tags: [redis, 系统设计]
---

有数亿的用户，那么对于某个网页，怎么使用 Redis 来统计一个网站的用户访问数呢

<!--more-->

## Hash

当用户访问的时候，我们可以使用 HINCRBY 命令，key 可以选择 URI 与对应的日期进行拼凑，field 可以使用用户的 id, increment 为 1，每访问一次加 1，这样可以得到该用户当天访问该页面的次数；也可以用 HSET 置为 1，标记用户当日活跃。

统计每个页面的日活用户数，用 HLEN 命令得到，例 `HLEN index.html0829`

优点：简单，容易实现，查询也是非常方便，数据准确性非常高。
缺点：占用内存过大。随着 key 的增多，性能也会下降。小网站还行，数亿 PV 的网站肯定受不了

## SetBit

使用`SETBIT`命令，设置用户活跃，`SETBIT index.html0928 int($user_id) 1`。
使用`BITCOUNT`命令，得到当日活跃用户数， `BITCOUNT key [start end]` -> 返回的是二进制中 1 的个数
使用`GETBIT`命令，查询某一用户当日是否活跃，`GETBIT key offset`

一个亿用户占用存储空间为 10^8bit / 8(8 位一个字节) / 1024（1024 字节为 1K） / 1024（1024k 为 1M） 大约 11.92M

优点: 占用内存更小，查询方便，可以指定查询某个用户。

缺点:

1. 由于要求 userId 到 int 值的映射，数据可能略有瑕疵，对于非登陆的用户，可能不同的 key 映射到同一个 id，否则需要维护一个非登陆用户的映射，有额外的开销。
2. 如果用户非常的稀疏，那么占用的内存可能比方法一更大。

## HyperLogLog

如果所需要的数量不用那么准确，可以使用概率算法。在 Redis 中，已经封装了`HyperLogLog`算法，他是一种基数评估算法。这种算法的特征，一般都是数据不存具体的值，而是存用来计算概率的一些相关数据。

当用户访问网站的时候，我们可以使用`PFADD`命令，设置对应的命令，最后我们只要通过`PFCOUNT`就能顺利计算出最终的结果，因为这个只是一个概率算法，所以可能存在 0.81%的误差。

优点: 占用内存极小，对于一个 key，只需要 12kb。对于超多用户的特别适用。
缺点: 无法查询指定用户是否登录。
