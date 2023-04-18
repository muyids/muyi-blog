信号量，就好像初始化一定数量的许可证，每个线程先获取许可证，只有获取成功了才可以继续执行，没有获取成功的就只能等待其他线程执行完释放许可后再被唤醒去获取许可；

```java
@Slf4j
public class SemaphoreDemo {

    // 车位数
    public static final int CNT = 3;
    public static void main(String[] args) {
        // 停车场
        Semaphore semaphore = new Semaphore(CNT);
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                try {
                    // 获取入库信号（信号量-1）
                    semaphore.acquire();
                    log.info("{}号车入库", Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    TimeUnit.SECONDS.sleep(new Random().nextInt(5));
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                // 车辆出库，信号量+1
                semaphore.release();
                log.info("---------{}号车出库", Thread.currentThread().getName());
            }, "t" + i).start();
        }
    }
}
```

- 信号量限制的是并发、资源
- 限流算法的一种，其他两种是漏桶算法和令牌桶算法
