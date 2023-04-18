---
title: 布隆过滤器
date: 2018-07-02T00:00:00+08:00
categories: [数据结构]
tags: [数据结构]
---

布隆过滤器是一种巧妙的`概率型数据结构`，可以用来告诉你`某样东西一定不存在或者可能存在`

<!--more-->

## 什么是布隆过滤器

布隆过滤器是一种数据结构，比较巧妙的概率型数据结构，特点是高效地插入和查询，可以用来告诉你 **某样东西一定不存在或者可能存在**。

相比于传统的 List、Set、Map 等数据结构，它更高效、占用空间更少，但是缺点是其返回的结果是概率性的，而不是确切的。

## 为何要用布隆过滤器

我们考虑这样一个场景，你有一个网站并且拥有很多访客，每当有用户访问时，你想知道这个 ip 是不是第一次访问你的网站。

### hash 表

为了完成这个功能，你很容易就会想到下面这个解决方案：
把访客的 ip 存进一个 hash 表中，每当有新的访客到来时，先检查哈希表中是否有该访客的 ip，如果有则说明该访客不是第一次访问。
hash 表的存取时间复杂度都是 O(1),效率很高，但是假设你的网站已经被 1 亿个用户访问过，每个 ip 的长度是 15，那么你一共需要`15 * 100000000 = 1500000000Bytes = 1.4G`，这还没考虑 hash 冲突的问题（hash 表中的槽位越多，越浪费空间，槽位越少，效率越低）

如果把 ip 转换成无符号的 int 型值来存储，一个 ip 需要占用 4 个字节就行了，这时 1 亿个 ip 占用的空间是`4 * 100000000 = 400000000Bytes = 380M`，空间消耗降低了很多。

那还有没有在不影响存取效率的前提下更加节省空间的办法呢?

### BitSet

32 位无符号 int 型能表示的最大值是`4294967295`，所有的 ip 都在这个范围内，我们可以用一个 bit 位来表示某个 ip 是否出现过，
如果出现过，就把代表该 ip 的 bit 位置为 1，那么我们最多需要 429496729 个 bit 就可以表示所有的 ip 了。举个例子比如 10.0.0.1 转换成 int 是 167772161，那么把长度为`4294967295`的 bit 数组的第`167772161`个位置置为 1 即可，当有 ip 访问时，只需要检查该标志位是否为 1 就行了。
4294967295bit = 536870912Byte = 512M

**BitSet 的局限性**

- 当样本分布极度不均匀的时候，BitSet 会造成很大空间上的浪费。

  举个例子，比如你有 10 个数，分别是 1、2、3、4、5、6、7、8、99999999999；那么你不得不用 99999999999 个 bit 位去实现你的 BitSet,而这个 BitSet 的中间绝大多数位置都是 0，并且永远不会用到，这显然是极度不划算的。

- 当元素不是整型的时候，BitSet 就不适用了。

  你拿到的是一堆 url，然后如果你想用 BitSet 做去重的话，先得把 url 转换成 int 型，在转换的过程中难免某些 url 会计算出相同的 int 值，于是 BitSet 的准确性就会降低。

那针对这两种情况有没有解决办法呢？

- 第一种分布不均匀的情况可以通过 hash 函数，将元素都映射到一个区间范围内，减少大段区间闲置造成的浪费，这很简单，取模就好了，难的是取模之后的值保证不相同，即不发生 hash 冲突。
- 第二种情况，把字符串映射成整数是必要的，那么唯一要做的就是保证我们的 hash 函数尽可能的减少 hash 冲突，一次不行我就多 hash 几次，hash 还是容易碰撞，那我就扩大数组的范围，使 hash 值尽可能的均匀分布，减少 hash 冲突的概率。
  基于这种思想，BloomFilter 诞生了。

## 实现原理

**Bloom Filter**是一种空间效率很高的随机数据结构，Bloom filter 可以看做是对 bit-map 的扩展, 它的原理是：

当一个元素被加入集合时，通过  K  个  Hash 函数将这个元素映射成一个位阵列（Bit array）中的 K 个点，把它们置为  1。检索时，我们只要看看这些点是不是都是 1 就（大约）知道集合中有没有它了：

如果这些点有任何一个 0，则被检索元素一定不在；如果都是 1，则被检索元素很可能在。

**核心思想**

- 多个 hash，增大随机性，减少 hash 碰撞的概率
- 扩大数组范围，使 hash 值均匀分布，进一步减少 hash 碰撞的概率。

## 构成

布隆过滤器包括两部分

- 随机映射函数
- 二进制向量数组

## 删除数据

- 如果是频繁删除的场景，需要增加一维数组，用来计数，记录当前位置被命中的次数
- 删除一次，计数器减一，当计数器为 0 时，布隆过滤器数组对应的位置置为 0

## 碰撞几率计算

## 应用场景

- **解决缓存穿透问题**
  缓存穿透是指查询一个一定不存在的数据，由于缓存是不命中时被动写的，并且出于容错考虑，如果从存储层查不到数据则不写入缓存，这将导致这个不存在的数据每次请求都要到存储层去查询，失去了缓存的意义。在流量大时，可能 DB 就挂掉了，要是有人利用不存在的 key 频繁攻击我们的应用，这就是漏洞。
- 爬虫 URL 地址去重
  A,B 两个文件，各存放 50 亿条 URL，每条 URL 占用 64 字节，内存限制是 4G，让你找出 A,B 文件共同的 URL。如果是三个乃至 n 个文件呢？
  分析 ：如果允许有一定的错误率，可以使用 Bloom filter，4G 内存大概可以表示 340 亿 bit。将其中一个文件中的 url 使用 Bloom filter 映射为这 340 亿 bit，然后挨个读取另外一个文件的 url，检查是否与 Bloom filter，如果是，那么该 url 应该是共同的 url（注意会有一定的错误率）。
- K-V 系统快速判断某个 key 是否存在
  典型的例子有 Google 著名的分布式数据库 Bigtable 以及 Hbase 使用了布隆过滤器来查找不存在的行或列，以减少磁盘查找的ＩＯ次数
- 黑名单
  比如检查垃圾邮件地址，假定我们存储一亿个电子邮件地址，我们先建立一个十六亿二进制（比特），即两亿字节的向量，然后将这十六亿个二进制全部设置为零。对于每一个电子邮件地址 X，我们用八个不同的随机数产生器（F1,F2, ...,F8） 产生八个信息指纹（f1, f2, ..., f8）。再用一个随机数产生器 G 把这八个信息指纹映射到 1 到十六亿中的八个自然数 g1, g2, ...,g8。现在我们把这八个位置的二进制全部设置为一。当我们对这一亿个 email 地址都进行这样的处理后。一个针对这些 email 地址的布隆过滤器就建成了。

## 大 Value 拆分

Redis 因其支持 setbit 和 getbit 操作，且纯内存性能高等特点，因此天然就可以作为布隆过滤器来使用。
但是**布隆过滤器的不当使用极易产生大 Value**，增加 Redis 阻塞风险，因此生成环境中建议对体积庞大的布隆过滤器进行拆分。
拆分的形式方法多种多样，但是本质是不要将 Hash(Key) 之后的请求分散在多个节点的多个小 bitmap 上，
而是应该拆分成多个小 bitmap 之后，对一个 Key 的所有哈希函数都落在这一个小 bitmap 上。