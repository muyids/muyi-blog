**ReentrantLock**

ReentrantLock 是什么？用来解决什么问题的？其实现的是 **可重入锁、独占锁**，同时可以根据传参来选择是**公平或者非公平锁**。

重入锁是什么呢？

> 就是可以对一个对象多次加锁，体现在代码上就是可以多次执行 lock()和 unlock()操作；

独占锁又是啥？

> 当一个线程获取到资源，也就是获取到锁的时候，其他所有需要获取锁的线程都会阻塞，直到线程释放锁

公平锁和非公平锁又有什么区别呢？

> 所谓的公平就是先来先得，不允许插队；非公平呢，就是不管别的线程在不在排队，后面来的线程抢占到资源，也可以直接执行

ReentrantLock 实现了上面的这几个特性，那什么场景下适合使用 ReentrantLock 呢

**应用场景**

**场景 1：同步执行（同 synchronized）**

如果已经有线程在执行，则进行排队等待；

这种情况常用于对资源的争抢（如：文件操作，同步消息发送，有状态的操作等）

场景代码：

```java
@Slf4j
public class Reentrant02 {
    //    private ReentrantLock lock = new ReentrantLock(); // 参数默认false，不公平锁
    private ReentrantLock lock = new ReentrantLock(true); //公平锁

    public void run() {
        try {
            lock.lock(); // 阻塞获取锁
            // 模拟操作
            log.info(Thread.currentThread().getName() + " get lock");
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        } finally {
            lock.unlock();
        }
    }
    public static void main(String[] args) {
        Reentrant02 lock = new Reentrant02();
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                lock.run();
            }, "t" + i).start();
        }
    }
}
```

**场景 2：尝试等待执行**

场景 1 中如果排队等待时间过长，总不能一直等下去吧，于是有了尝试等待执行的场景

场景代码：

```java
@Slf4j
public class Reentrant03 {

    private ReentrantLock lock = new ReentrantLock();

    public void run() {

        try {
            if (lock.tryLock(3, TimeUnit.SECONDS)) {
                // 模拟操作
                try {
                    log.info(Thread.currentThread().getName() + " do work");
                    TimeUnit.SECONDS.sleep(5);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                }
            } else {
                log.info(Thread.currentThread().getName() + " abort");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        Reentrant03 lock = new Reentrant03();
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                lock.run();
            }, "t" + i).start();
        }
    }
}
```

**场景 3：尝试执行**（同分布式锁）

尝试执行就是我们发现有线程已经在执行了，就直接放弃执行，可以**防止重复执行**，这跟分布式锁的应用场景很像吧，只是分布式锁适用于多机部署场景，如果对同一资源的操作都路由到同一台服务器处理，我们不就可以用 ReentranLock 来限制一下并发资源抢占了

总结一下：此场景适合用于进行**非重要任务防止重复执行**的情况（如：清除无用临时文件，检查某些资源的可用性，数据备份操作等）

具体场景列举两个：

a、用在定时任务时，如果任务执行时间可能超过下次计划执行时间，确保该有状态任务只有一个正在执行，忽略重复触发。
b、用在界面交互时点击执行较长时间请求操作时，防止多次点击导致后台重复执行（忽略重复触发）。
场景代码：

```java
public class Reentrant01 {
    private ReentrantLock lock = new ReentrantLock();

    public void run() {
        // 如果已经被lock，则立即返回false不会等待，达到忽略操作的效果
        if (lock.tryLock()) {
            try {
                // 模拟操作
                log.info(Thread.currentThread().getName() + " get lock");
                try {
                    TimeUnit.SECONDS.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            } finally {
                lock.unlock();
            }
        }
    }
    public static void main(String[] args) {
        Reentrant01 reentrant01 = new Reentrant01();
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                reentrant01.run();
            }, "t" + i).start();
        }
    }
}
```

**场景 4：可中断执行**

发现有线程在执行，等待，当正在进行的操作发生中断时，释放锁，进行下一个操作

场景代码：

```java
@Slf4j
public class Reentrant04 {
    private ReentrantLock lock = new ReentrantLock();
    public void run() {
        try {
            lock.lockInterruptibly();
            // 模拟操作
            try {
                // t3线程报中断
                if ("t3".equals(Thread.currentThread().getName())){
                    throw new InterruptedException();
                }
                log.info(Thread.currentThread().getName() + " do work");
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
    public static void main(String[] args) {
        Reentrant04 reentrant01 = new Reentrant04();
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                reentrant01.run();
            }, "t" + i).start();
        }
    }
}
```

**场景 5：可重入**

- 可以对同一资源多次加锁&解锁
- lock(), unlock()配对使用，加一次就要解一次
  场景代码：

```java
@Slf4j
public class Reentrant05 {

    public static void main(String[] args) {
        ReentrantLock lock = new ReentrantLock();
        // 可重入锁；注意点 lock(), unlock()配对使用
        new Thread(() -> {
            lock.lock();
            try {
                log.info(Thread.currentThread().getName() + "=====外层=====");
                lock.lock();
                try {
                    log.info(Thread.currentThread().getName() + "=====内层=====");
                } finally {
                    lock.unlock();
                }
            } finally {
                lock.unlock();
            }
        }, "t1").start();

        // 若t1：lock()次数>unlock()次数，t2不执行；lock()次数<unlock()次数，t1抛异常
        new Thread(() -> {
            lock.lock();
            try {
                log.info(Thread.currentThread().getName() + "=== 调用");
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                lock.unlock();
            }
        }, "t2").start();
    }
}
```
