谈谈你对 AQS 的理解。AQS 如何实现可重入锁？

**前言**

`AQS`是`JUC`最重要的基石

**AQS 的概念**

- 抽象队列同步器 AbstractQueuedSynchronizer（以下简称同步器），并发包的作者（Doug Lea）期望它能够成为实现大部分同步需求的基础
- 用来构建锁或者其他同步组件的基础框架
- 两大核心属性：
  - 成员变量 state：表示同步状态
  - 内置的 FIFO 队列：实现资源获取线程的排队工作

**前置知识**

- Lock 接口

- 公平锁和非公平锁

- 可重入锁

- LockSupport
- 自旋锁
- 数据结构之双向链表
- 模板设计模式
  **Lock 接口是什么**

不同于 synchronized 关键字是 JVM 底层的锁机制实现，依赖于底层 C++实现；Lock 接口是 JUC 中 API 级别实现。

Lock 接口中定义了常用的锁方法：

![2021-09-08 pm2.41.10](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-08%20pm2.41.10.png)

其中有 4 个获取锁的方法，其中 lock 和 tryLock 是较为常用的：

- lock() : 一直等，直到拿到锁
- tryLock() : 只尝试一次，拿不到就放弃
- tryLock(long time, TimeUnit unit) : 给定的时间内等待，超时就放弃
- lockInterruptibly() : 通常情况下不会放弃，但如果外部有一个线程或方法将获取锁的方法中断，就不在获取锁了
  释放锁：unlock()

创建监听器：newCondition(): 实现精准唤醒

**可重入锁**

可以对一个对象多次执行 lock()加锁和 unlock()释放锁；

sychronized 和 reentrantLock 都是可重入锁

**常用组件**

- 重入锁 原来写游戏时候锁血量用

- 写分布式缓存时候 用过 readWriteLock 来保证性能和 数据一致性
- countDownLatch 在艺龙机票查询几十个供应商时候用，一个请求拆分成多个
- SemaPhore 在写分布式缓存的时候 在首次加载资源的时候限制突发量的，只允许前 10 个线程来加载几个

CountdownLatch 和 cyclicBarrier 区别

- cdl 是主线程分成多个子线程最后回到主线程
- cycB 是主线程分成多个子线程最后回调一个分线程
- cyclicBarrier 可以循环调用

ReadWriteLock 读写锁

**ReentrantLock**

这里经常有一个扩展问题，**Sychronized 和 ReentrantLock 的区别**，我们一般会从以下方面回答

- sychronized 是⼀个关键字，ReentrantLock 是⼀个类
- sychronized 的底层是 JVM 层⾯的锁，ReentrantLock 是 API 层⾯的锁
- sychronized 会⾃动的加锁与释放锁，ReentrantLock 需要程序员⼿动加锁与释放锁
- sychronized 是⾮公平锁，ReentrantLock 可以选择公平锁或⾮公平锁
- sychronized 锁的是对象，锁信息保存在对象头中，ReentrantLock 通过代码中 int 类型的 state 标识来标识锁的状态
- sychronized 底层有⼀个锁升级的过程
- synchronized 适合**锁的少量代码**，lock 适合**大量锁**的代码

**手写一个 ReentrantLock**

**AQS 尾分叉**

**ReadWriteRock 读写锁**，使用场景可分为读/读、读/写、写/写，除了读和读之间是共享的，其它都是互斥的，接着会讨论下怎样实现互斥锁和同步锁的， 想了解对方对 AQS，CAS 的掌握程度，技术学习的深度。

**Semaphore 拿到执行权的线程之间是否互斥**，Semaphore、CountDownLatch、CyclicBarrier、Exchanger 为 java 并发编程的 4 个辅助类，面试中常问的 CountDownLatch CyclicBarrier 之间的区别，面试者肯定是经常碰到的， 所以问起来意义不大，Semaphore 问的相对少一些，有些知识点如果没有使用过还是会忽略，Semaphore 可有多把锁，可允许多个线程同时拥有执行权，这些有执行权的线程如并发访问同一对象，会产生线程安全问题。

作者：Mingdeng Yue
链接：https://www.zhihu.com/question/60949531/answer/579002882
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
**CountDownLatch 和 Semaphore 的区别和底层原理**

CountDownLatch 表示计数器，可以给 CountDownLatch 设置⼀个数字，⼀个线程调⽤

CountDownLatch 的 await()将会阻塞，其他线程可以调⽤ CountDownLatch 的 countDown()⽅法来对

CountDownLatch 中的数字减⼀，当数字被减成 0 后，所有 await 的线程都将被唤醒。

对应的底层原理就是，调⽤ await()⽅法的线程会利⽤ AQS 排队，⼀旦数字被减为 0，则会将 AQS 中

排队的线程依次唤醒。

Semaphore 表示信号量，可以设置许可的个数，表示同时允许最多多少个线程使⽤该信号量，通

过 acquire()来获取许可，如果没有许可可⽤则线程阻塞，并通过 AQS 来排队，可以通过 release()

⽅法来释放许可，当某个线程释放了某个许可后，会从 AQS 中正在排队的第⼀个线程开始依次唤

醒，直到没有空闲许可。

思考下面的问题怎么回答

- ReentrantLock 中的公平锁和⾮公平锁的底层实现
- ReentrantLock 中 tryLock()和 lock()⽅法的区别
- CountDownLatch 和 Semaphore 的区别和底层原理
- Sychronized 和 ReentrantLock 的区别
  总结

1. AQS 抽象队列同步器，是 java 的线程同步框架，是 JDK 中很多锁工具的核心实现框架
2. AQS 中维护了一个信号量 state 和一个线程组成的双向链表队列
