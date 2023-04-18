**大纲**

- == 和 equal() 的区别
- 说说集合类

---

1. hashmap 原理
2. 集合的底层数据结构

#### hashmap 原理

- 数组和链表组成
- 线程不安全
- 核心点：put 和 get 过程，扩容方式
- JDK1.7 和 1.8 的主要区别：头插法，尾插法，头插容易导致链表死循环，1.8 后
  加入红黑树提升性能

#### 集合的底层数据结构

<1>HashMap : 初始容量 16，负载因子 0.75，扩容 2 倍，16 << 1 = 32

算法改变：

jdk1.7：位桶+链表

Put（key, value）操作，先通过 hashcode()和 key 计算下标 index 位置，索引位置为空，直接插入数组；不为空，与原来的 key 进行 equals 比较，相同就替换，不同就形成链表（哈希碰撞）

扩容机制：需要重新计算 hash 码值

缺点：查询慢，扩容慢，效率低

jdk1.8: 位桶+链表/红黑树

hashmap 是数组、链表、红黑树的组合形式，当链表超过 8 且元素总长度超过 64，转换为红黑树的存储

扩容机制：原长度+当前索引位置（比如，原来长度是 16，当前 hash 值在 3 号下标位置，就直接放到 19 号位置）

优点：除了添加（红黑树需要旋转保证平衡），其他效率都有提高，红黑树是有序的

hashset 的底层是 hashMap

hashMap 是线程不安全的，可存 null 的 key 和 value，hashtable 是线程安全的，不可以存 null 的 key 和 value

<2> collection 接口：

Collections 辅助工具类, hashmap 不同步线程不安全，hashtable 同步线程安全，concurrenthashmap 线程安全

<3>ArrayList 底层是 Object[]类型的动态数组，初始容量 10，扩容 增加 50%，扩容时采用 Arrays.arrayCopy()复制到新数组

优化：提前支出 arrayList 容量大小

<4>LinkedList: 双向的循环链表

随机访问：get,update --> arrayList ；

新增、删除：add,remove --> LinkedList (ArrayList 要移动数组)

<5> vector: 和 arrayList 相同，唯一不同的地方是 vector 线程安全，是强同步类，效率低

## HashMap

### 结构：数组+链表+红黑树

### 原理

HashMap 是基于 hashing 的原理，通过`put(k,v)`存储对象到 HashMap 中，通过 get(k)方式获取对象。

当使用`put(k,v)`传递 key、value 的时候，首先调用`hashCode()`方法，计算 bucket 位置来存储 Node 对象。

#### put(k,v)过程

1. 对 key 求 Hash 值，计算下标。
2. 如果没有碰撞存入桶中，碰撞则放入 bucket 的链表或者红黑树中。
3. 如果链表超过阈值（默认链表数超过 8，总 Entry 数超过 64）则转换为红黑树，链表长度<6 则转换回链表。
4. key 结点存在则替换旧值。
5. 如果桶满（容量\*加载因子），就要 resize（扩容 2 倍后重排）。

### get(k)过程

1. 首先将 key hash 之后取得所定位的桶。
2. 如果桶为空则直接返回 null 。
3. 否则判断桶的第一个位置(有可能是链表、红黑树)的 key 是否为查询的 key，是就直接返回 value。
4. 如果第一个不匹配，则判断它的下一个是红黑树还是链表。
5. 红黑树就按照树的查找方式返回值。不然就按照链表的方式遍历匹配返回值。

### 优化

减少碰撞。原理是如果两个不相等的对象返回不同的 hashcode 的话，那么碰撞的几率就会小些。

这就意味着存链表结构减小，这样取值的话就不会频繁调用 equal 方法，从而提高 HashMap 的性能（扰动即 Hash 方法内部的算法实现，目的是让不同对象返回不同 hashcode）。

使用不可变的、声明作 final 对象，并且采用合适的 equals() 和 hashCode() 方法，将会减少碰撞的发生。

### 多线程 HashMap 死循环问题

因为如果两个线程都发现 HashMap 需要重新调整大小了，它们会同时试着调整大小。
在调整大小的过程中，存储在链表中的元素的次序会反过来。
因为在 resize 过程中，移动到新的 bucket 位置的时候，HashMap 并不会将元素放在链表的尾部，而是放在头部，使用的是队头插入方法。
这是为了避免尾部遍历（tail traversing）。如果条件竞争发生了，那么就死循环了，这也是导致 CPU 飙升的原因，所以多线程的环境下不使用 HashMap，而是使用`concurrentHashMap`。

## LinkedHashMap

LinkedHashMap 的实现就是 HashMap+LinkedList 的实现方式，以 HashMap 维护数据结构，以 LinkList 的方式维护数据插入顺序。
LinkedHashMap 通过维护一个运行所有条目的双向链表，LinkedHashMap 保证了元素的迭代顺序。迭代顺序可以是插入顺序或者是访问顺序。

## TreeMap

- 是一个有序的 key-value 集合，它是通过红黑树实现的。
- 继承于 AbstractMap，所以它是一个 Map，即一个 key-value 集合。
- 实现了`NavigableMap`接口，意味着它支持一系列的导航方法。比如返回有序的 key 集合。
- 实现了`Cloneable`接口，意味着它能被克隆。
- 实现了`java.io.Serializable`接口，意味着它支持序列化。
- 基于`红黑树（Red-Black tree）`实现。该映射根据其键的自然顺序进行排序，或者根据创建映射时提供的 Comparator 进行排序，具体取决于使用的构造方法。
- 基本操作 `containsKey、get、put 和 remove` 的时间复杂度是 log(n) 。

## HashTable 与 HashMap 的区别

- HashTable 线程安全，HashMap 线程不安全。
- HashTable 不可存储 null 值，HashMap 可以存储 null 值。
- HashMap 去掉了 HashTable 的 contains ⽅方法，但是加上了 `containsValue()和containsKey()`方法。

## ConcurrentHashMap

1.7：Segment + HashEntry + Unsafe

1.8: 移除 Segment，使锁的粒度更小，Synchronized + CAS + Node + Unsafe

结构：HashEntry +红黑树+CAS+Synchronized

数据结构：Node（链表）、TreeNode（红黑树）、TreeBin（红黑树容器）

put(k,v)流程：

- 如果没有初始化就调用 initTable()。
- 如果 hash 没有冲突就直接 CAS 插入。
- 如果还在进行扩容就继续扩容（多线程进行）。
- 如果存在 hash 冲突，就加锁来保证线程安全，这里有两种情况，一种是链表形式就直接遍历到尾端插入，一种是红黑树就按照红黑树结构插入。
- 插入最后一个元素如果该链表的数量大于阈值 8，就要先转换成黑红树的结构，break 再一次进入循环。
- 如果添加成功就调用 addCount（）方法统计 size，并且检查是否需要扩容。

### get(k)流程：

- 计算 hash 值，定位到该 table 索引位置，如果是首节点符合就返回。
- 如果遇到扩容的时候，会调用标志正在扩容节点 ForwardingNode 的 find 方法，查找该节点，匹配就返回。
