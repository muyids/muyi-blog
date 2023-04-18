**前言**

CyclicBarrier 底层是基于 ReentrantLock 和 AbstractQueuedSynchronizer 来实现的, 在理解的时候最好和 CountDownLatch 放在一起理解

**什么是 CyclicBarrier**

循环栅栏

**使用示例**

```java
/**
 * 七龙珠 : 集齐七颗龙珠可以召唤神龙
 */
@Slf4j
public class CyclicBarrierDemo {
    public static final int NUMBER = 7;

    public static void main(String[] args) {
        CyclicBarrier cyclicBarrier = new CyclicBarrier(NUMBER, () -> {
            log.info("神龙出现");
        });
        // 集齐七龙珠的过程
        for (int i = 0; i < NUMBER; i++) {
            new Thread(() -> {
                try {
                    log.info("{}龙珠被收集了", Thread.currentThread().getName());
                    // 等待
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }, "t" + i).start();
        }
    }
}
```

**CountDownLatch 和 CyclicBarrier 对比**

- CountDownLatch 减计数，CyclicBarrier 加计数。

- CountDownLatch 是一次性的，CyclicBarrier 可以重用。
- CountDownLatch 和 CyclicBarrier 都有让多个线程等待同步然后再开始下一步动作的意思，但是 CountDownLatch 的下一步的动作实施者是主线程，具有不可重复性；而 CyclicBarrier 的下一步动作实施者还是“其他线程”本身，具有往复多次实施动作的特点
