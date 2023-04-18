**带着问题去思考**

- 为什么有了 ReentrantLock 还需要 ReentrantReadWriteLock
- ReentrantReadWriteLock 底层实现原理?
- ReentrantReadWriteLock 底层读写状态如何设计的? 高 16 位为读锁，低 16 位为写锁
- 读锁和写锁的最大数量是多少?
- 本地线程计数器 ThreadLocalHoldCounter 是用来做什么的?
- 缓存计数器 HoldCounter 是用来做什么的?
- 写锁的获取与释放是怎么实现的?
- 读锁的获取与释放是怎么实现的?
- RentrantReadWriteLock 为什么不支持锁升级?
- 什么是锁的升降级? RentrantReadWriteLock 为什么不支持锁升级?
  **出现原因**

我们之前不是已经有了 ReentrantLock 了吗，为什么还需要 ReentrantReadWriteLock？

ReentrantLock 只允许单个线程执行受保护的程序，而在大部分应用中都是**读的操作次数远远大于写操作次数**，使用 ReentrantLock 锁会严重影响整体性能；ReentrantReadWriteLock 可以实现并发访问的情况下，读可以多线程同时访问，而写只有一个线程可以执行。他允许多读，但是不允许读和写同时发生。

**实现方式**

读写锁，支持共享方式多个线程同时获取资源，也支持排他方式只能有一个线程能够获取，用读锁的时候表示支持其他读锁访问，写锁的时候就只允许一个线程访问；

ReentrantReadWriteLock 实现的互斥场景如下：

- 读-读不互斥：读读之间不阻塞

- 读-写互斥：读会阻塞写，写也会阻塞读

- 写-写互斥：写写阻塞

**应用举例**

```java
private final ReentrantReadWriteLock readWriteLock = new ReentrantReadWriteLock();
private final Lock readLock = readWriteLock.readLock();
private final Lock writeLock = readWriteLock.writeLock();
public String read() {
  readLock.lock();
  try {
    // 执行读
    log.info("执行读");
    try {
      TimeUnit.MILLISECONDS.sleep(10);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    return "xxx";
  } finally {
    readLock.unlock();
  }
}

public void write() {
  writeLock.lock();
  try {
    //执行写
    try {
      TimeUnit.MILLISECONDS.sleep(10);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    log.info("执行写.....");
  } finally {
    writeLock.unlock();
  }
}
```

## 缓存计数器 HoldCounter 是用来做什么的?（chatgpt）
