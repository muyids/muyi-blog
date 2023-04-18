**atomic**

原理通过 unsafe 类调用 native 的 cas

- AtomicInteger
- AtomicDouble
- AtomicLong
- AtomicReference
- LongAcc

**Lock**

- AQS

  juc 的基石

- Lock

- Condition

- LockSupport

  Park 和 unpark

- ReadWriteLock

  读写锁；

- ReentrantLock

  可重入锁

**工具类**

相当于 bluebird 异步任务的编排

- CountDownLatch

- CyclicBarrier

- Semaphore

- Callable --> promisify

  相当于 nodejs 里的 promise

- FutureTask

  可以获得 Callable 的异步执行结果

**集合**

- ConcurrentHashMap

  1.7 和 1.8 的加锁方式

- CopyOnWriteArrayList

  写的时候先 copy 一份出来

- BlockingQueue

- BlockingDeque

  线程池+阻塞队列

**线程池**

- Executors

---

实际场景：**运动会**

- 名单：CopyOnWriteArrayList
- 准备：ConcurrentHashMap <String,Model>
- 跑道：Semaphore
- 发令员：CountDownLatch
- 冲线：AtomicInteger
- 领奖：CyclicBarrier

---

应用举例：

- ConcurrentSkipListMap 用来存一致性 hash 的环；
- Countdownlatch 一个服务需要多个模块（线程）时，都启动才宣布服务启动；
- atomicinteger 做在线数量统计；
- ScheduledThreadPoolExecutor 做定时任务；
- ReentrantLock 做可中断锁，避免死锁；
- 交换器 Exchanger 很少用，只适用于两个线程在同步点交换数据的场景
