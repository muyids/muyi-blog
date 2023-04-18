---
title: LRU算法简介
date: 2019-08-21T00:00:00+08:00
draft: false
categories: [算法]
tags: [算法]
---

`LRU(Least Recently Used)`近期最少使用算法是一种常用的`缓存淘汰策略`

<!--more-->

### 原理

LRU（Least recently used，最近最少使用）算法根据数据的历史访问记录来进行淘汰数据，
其核心思想是“如果数据最近被访问过，那么将来被访问的几率也更高”。

### 实现

最常见的实现是使用一个链表保存缓存数据，详细算法实现如下：

1. 新数据插入到链表头部；
2. 每当缓存命中（即缓存数据被访问），则将数据移到链表头部；
3. 当链表满的时候，将链表尾部的数据丢弃。

### 分析

【命中率】

当存在热点数据时，LRU 的效率很好，但偶发性的、周期性的批量操作会导致 LRU 命中率急剧下降，缓存污染情况比较严重。

【复杂度】

实现简单。

【代价】

命中时需要遍历链表，找到命中的数据块索引，然后需要将数据移到头部。当数据量较大时，遍历链表效率较低。

## 实现

有一种叫做有序字典的数据结构，综合了哈希表和链表，在 Python 中为 `OrderedDict`,在 Java 中为 `LinkedHashMap`,
在 javascript 中的实现为`Map`

### python

```
from collections import OrderedDict
class LRUCache(OrderedDict):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self:
            return - 1

        self.move_to_end(key)
        return self[key]
    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last = False)

# LRUCache 对象会以如下语句构造和调用:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

复杂度分析

- 时间复杂度：对于 put 和 get 操作复杂度是 O(1)O(1)，
  因为有序字典中的所有操作：get/in/set/move_to_end/popitem（get/containsKey/put/remove）都可以在常数时间内完成。
- 空间复杂度：O(capacity)，因为空间只用于有序字典存储最多 capacity + 1 个元素。

### java

java 中最简单的 LRU 算法实现，就是利用 jdk 的 LinkedHashMap，覆写其中的 removeEldestEntry(Map.Entry)方法即可

如果你去看 LinkedHashMap 的源码可知，LRU 算法是通过双向链表来实现，当某个位置被命中，通过调整链表的指向将该位置调整到头位置，
新加入的内容直接放在链表头，如此一来，最近被命中的内容就向链表头移动，需要替换时，链表最后的位置就是最近最少使用的位置。

### golang

使用双向链表 + collection 实现有序字典的数据结构

### javascript

#### 内置有序字典 Map

使用[**javascript ES6 Map 中 keys 的有序性**](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Map/keys)来实现

一个 Map 对象在迭代时会根据对象中元素的插入顺序来进行

- get 操作

如果元素存在，先 delete 再 set, 元素便会成置为最新使用；如果不存在，返回-1

- put 操作

如果元素存在，先 delete 再 set, 元素便会成置为最新使用；
如果容器超限，进行删除末尾元素操作，使用 Map{}.keys().next()得到迭代器的第一个元素，为使用时间最远的元素，进行删除

```javascript
/**
 * @param {number} capacity
 */
var LRUCache = class {
  constructor(capacity) {
    this.cache = new Map();
    this.capacity = capacity;
  }
  /**
   * @param {number} key
   * @return {number}
   */
  get(key) {
    let cache = this.cache;
    let temp = cache.get(key);
    if (temp) {
      cache.delete(key);
      cache.set(key, temp);
      return temp;
    } else {
      return -1;
    }
  }
  /**
   * @param {number} key
   * @param {number} value
   * @return {void}
   */
  put(key, value) {
    let cache = this.cache;
    if (cache.has(key)) {
      cache.delete(key);
    } else if (cache.size >= this.capacity) {
      cache.delete(cache.keys().next().value);
    }
    cache.set(key, value);
  }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * var obj = new LRUCache(capacity)
 * var param_1 = obj.get(key)
 * obj.put(key,value)
 */
```

### 双向链表 + hash 表

hash 表作为元素的存储集合，双向链表用于元素的增删，维护最近最少使用的原则

```javascript
function DLinkedNode() {
  this.key = null;
  this.value = null;
  this.prev = null;
  this.next = null;
}

/**
 * @param {number} capacity
 */
var LRUCache = function (capacity) {
  this.cache = new Map();
  this.size = 0;
  this.capacity = capacity;

  this.head = new DLinkedNode();
  this.tail = new DLinkedNode();
  //一个双向链表已经建立
  this.head.next = this.tail;
  this.tail.prev = this.head;
};
/**
 * @param {number} key
 * @return {number}
 */
LRUCache.prototype.get = function (key) {
  let node = this.cache.get(key);
  if (!node) return -1;

  // move the accessed node to the head;
  //使用过的放在头部
  this.moveToHead(node);
  return node.value;
};

/**
 * @param {number} key
 * @param {number} value
 * @return {void}
 */
LRUCache.prototype.put = function (key, value) {
  let node = this.cache.get(key);
  if (!node) {
    let newNode = new DLinkedNode();
    newNode.key = key;
    newNode.value = value;

    this.cache.set(key, newNode);
    this.addNode(newNode);
    this.size++;

    if (this.size > this.capacity) {
      //双向链表中要删除, 哈希 cache 中也要删除
      let tailNode = this.popTail();
      this.cache.delete(tailNode.key);
      //计数减一
      this.size = this.size--;
    }
  } else {
    // update the value
    node.value = value;
    this.moveToHead(node);
  }
};

LRUCache.prototype.addNode = function (node) {
  //Always add the new node right after head
  //添加到队头
  //假如 head  head.next 指向 nodeB
  //把 node 的 prev 和 next 指针 分别指向 head,  nodeB 这两个 节点
  node.prev = this.head;
  node.next = this.head.next;

  //上面我们仅仅修改了node的指针, 并没有修改 head 的 next 指针指向, 和 nodeB 的 prev 的指针指向
  //形成双向链表
  this.head.next.prev = node;
  this.head.next = node;
};

LRUCache.prototype.removeNode = function (node) {
  /**
   * Remove an existing node from the linked list.
   */
  //从双向链表中, 删除 node, 先记录下 它的前驱和后继指向的对象
  let prev = node.prev;
  let next = node.next;

  //把两个节点联系起来
  prev.next = next;
  next.prev = prev;
};
LRUCache.prototype.moveToHead = function (node) {
  /**
   * Move certain node in between to the head.
   */
  this.removeNode(node);
  this.addNode(node);
};
// 一个需要注意的是，在双向链表实现中，这里使用一个伪头部和伪尾部标记界限，这样在更新的时候就不需要检查是否是 null 节点;
// this.tail 是伪尾部
LRUCache.prototype.popTail = function (node) {
  /**
   * Pop the current tail.
   */
  let res = this.tail.prev;
  this.removeNode(res);
  return res;
};
```

**更多 LRU 算法介绍：**

## LRU-K

### 原理

LRU-K 中的 K 代表最近使用的次数，因此 LRU 可以认为是 LRU-1。
LRU-K 的主要目的是为了解决 LRU 算法“缓存污染”的问题，其核心思想是将“最近使用过 1 次”的判断标准扩展为“最近使用过 K 次”。

### 实现

相比 LRU，LRU-K 需要多维护一个队列，用于记录所有缓存数据被访问的历史。
只有当数据的访问次数达到 K 次的时候，才将数据放入缓存。
当需要淘汰数据时，LRU-K 会淘汰第 K 次访问时间距当前时间最大的数据。详细实现如下：

1. 数据第一次被访问，加入到访问历史列表；
2. 如果数据在访问历史列表里后没有达到 K 次访问，则按照一定规则（FIFO，LRU）淘汰；
3. 当访问历史队列中的数据访问次数达到 K 次后，将数据索引从历史队列删除，将数据移到缓存队列中，并缓存此数据，缓存队列重新按照时间排序；
4. 缓存数据队列中被再次访问后，重新排序；
5. 需要淘汰数据时，淘汰缓存队列中排在末尾的数据，即：淘汰“倒数第 K 次访问离现在最久”的数据。

LRU-K 具有 LRU 的优点，同时能够避免 LRU 的缺点，实际应用中 LRU-2 是综合各种因素后最优的选择，
LRU-3 或者更大的 K 值命中率会高，但适应性差，需要大量的数据访问才能将历史访问记录清除掉。

### 分析

【命中率】

LRU-K 降低了“缓存污染”带来的问题，命中率比 LRU 要高。

【复杂度】

LRU-K 队列是一个优先级队列，算法复杂度和代价比较高。

【代价】

由于 LRU-K 还需要记录那些被访问过、但还没有放入缓存的对象，因此内存消耗会比 LRU 要多；当数据量很大的时候，内存消耗会比较可观。

LRU-K 需要基于时间进行排序（可以需要淘汰时再排序，也可以即时排序），CPU 消耗比 LRU 要高。

## Two queues（2Q）

### 原理

Two queues（以下使用 2Q 代替）算法类似于 LRU-2，不同点在于 2Q 将 LRU-2 算法中的访问历史队列（注意这不是缓存数据的）改为一个 FIFO 缓存队列，
即：2Q 算法有两个缓存队列，一个是 FIFO 队列，一个是 LRU 队列。

### 实现

当数据第一次访问时，2Q 算法将数据缓存在 FIFO 队列里面，当数据第二次被访问时，
则将数据从 FIFO 队列移到 LRU 队列里面，两个队列各自按照自己的方法淘汰数据。详细实现如下：

1. 新访问的数据插入到 FIFO 队列；
2. 如果数据在 FIFO 队列中一直没有被再次访问，则最终按照 FIFO 规则淘汰；
3. 如果数据在 FIFO 队列中被再次访问，则将数据移到 LRU 队列头部；
4. 如果数据在 LRU 队列再次被访问，则将数据移到 LRU 队列头部；
5. LRU 队列淘汰末尾的数据。

**注:**
上图中 FIFO 队列比 LRU 队列短，但并不代表这是算法要求，实际应用中两者比例没有硬性规定。

### 分析

【命中率】

2Q 算法的命中率要高于 LRU。

复杂度】

需要两个队列，但两个队列本身都比较简单。

【代价】

FIFO 和 LRU 的代价之和。

2Q 算法和 LRU-2 算法命中率类似，内存消耗也比较接近，但对于最后缓存的数据来说，2Q 会减少一次从原始存储读取数据或者计算数据的操作。

## Multi Queue（MQ）

### 原理

MQ 算法根据访问频率将数据划分为多个队列，不同的队列具有不同的访问优先级，其核心思想是：优先缓存访问次数多的数据。

### 实现

MQ 算法将缓存划分为多个 LRU 队列，每个队列对应不同的访问优先级。访问优先级是根据访问次数计算出来的，例如
详细的算法结构图如下，Q0，Q1....Qk 代表不同的优先级队列，Q-history 代表从缓存中淘汰数据，但记录了数据的索引和引用次数的队列：
如上图，算法详细描述如下：

1. 新插入的数据放入 Q0；
2. 每个队列按照 LRU 管理数据；
3. 当数据的访问次数达到一定次数，需要提升优先级时，将数据从当前队列删除，加入到高一级队列的头部；
4. 为了防止高优先级数据永远不被淘汰，当数据在指定的时间里访问没有被访问时，需要降低优先级，将数据从当前队列删除，加入到低一级的队列头部；
5. 需要淘汰数据时，从最低一级队列开始按照 LRU 淘汰；每个队列淘汰数据时，将数据从缓存中删除，将数据索引加入 Q-history 头部；
6. 如果数据在 Q-history 中被重新访问，则重新计算其优先级，移到目标队列的头部；
7. Q-history 按照 LRU 淘汰数据的索引。

### 分析

【命中率】

MQ 降低了“缓存污染”带来的问题，命中率比 LRU 要高。

【复杂度】

MQ 需要维护多个队列，且需要维护每个数据的访问时间，复杂度比 LRU 高。

【代价】

MQ 需要记录每个数据的访问时间，需要定时扫描所有队列，代价比 LRU 要高。

注：虽然 MQ 的队列看起来数量比较多，但由于所有队列之和受限于缓存容量的大小，因此这里多个队列长度之和和一个 LRU 队列是一样的，因此队列扫描性能也相近。

## LRU 类算法对比

由于不同的访问模型导致命中率变化较大，此处对比仅基于理论定性分析，不做定量分析。

对比

- 命中率 LRU-2 > MQ(2) > 2Q > LRU
- 复杂度 LRU-2 > MQ(2) > 2Q > LRU
