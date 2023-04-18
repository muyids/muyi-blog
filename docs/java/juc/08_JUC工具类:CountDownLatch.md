CountDownLatch

**功能介绍**

闭锁（倒计时锁）

1. 正数计数器初始化一个值 n
2. 线程调用 await()方法阻塞**当前线程**
3. **任何线程**都可以调用 countDown()方法，每调用一次计数器减 1
4. 计数器减到 0 时**所有调用 await()方法阻塞的线程**被唤醒重新继续执行
   **应用场景**

可以实现多个线程等待一个线程，也可以实现一个线程等待多个线程执行完再执行；

```java
/**
* 放学了，等待学生走完后，值日生开始值日
**/
public class CountDownLatchDemo {
    public static void main(String[] args) throws InterruptedException {
        int students = 6;
        CountDownLatch countDownLatch = new CountDownLatch(students);
        for (int i = 0; i < students; i++) {
            new Thread(() -> {
                System.out.println(Thread.currentThread().getName()+"同学离开教室");
                countDownLatch.countDown();
            }, "t" + i).start();
        }
        countDownLatch.await();
        System.out.println("值日生开始值日");
    }
}
```

**实现原理**

- 维护内部类 Sync，Sync 继承自 AbstractQueuedSynchronizer
- AbstractQueuedSynchronizer 中有一个变量 private volatile int state;保证了 state 变量的可见性
- 构造 Sync(state)执行 setState(state)操作
- await()等待的是 state == 0
