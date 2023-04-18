AQS 在并发工具类中的使用

**前言**

java 程序员应该都知道 AQS 在 JUC 编程中的重要地位，可以说是基石一样的存在，那么 AQS 到底重要在什么地方呢？有什么应用场景呢？本文我们来探讨一下 AQS 的使用，如果你看了觉得有什么需要补充或改进的，欢迎留言评论

**并发工具类**

AQS 是一个抽象类，那么 juc 中有哪些并发工具类继承实现了他呢，让我们打开 juc.locks 下的 AbstractQueuedSynchronizer.java 文件

![2021-09-09 am8.24.09](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-09%20am8.24.09.png)

JUC 中使用了 AQS 的并发工具类有：

- ReentrantLock
- ReentrantReadWriteLock
- Semaphore
- CountDownLatch
