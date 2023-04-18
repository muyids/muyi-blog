Java 线程锁机制是怎样的？偏向锁、轻量级锁、重量级锁有什么区别？锁机制是如何升级的？

**前言**

Java 中的锁无非就是 JVM 提供的**synchronized**关键字和 JDK 中的 Lock 接口实现；

我们这里讨论更为底层的 synchronized。

### **synchronized 是干什么的呢？**

他就是用来解决**多个线程间相同资源访问的同步性问题**的；说白了就是保证线程安全的。

那他是怎么保证的呢？他通过修饰方法或代码块，使其在同一时间，只能被一个线程访问。

### **synchronized 是怎么用的呢？**

按规定，他有如下几种使用方式

1. 修饰普通同步方法 ：锁的是对象

   ```java
   synchronized void lock(){
   }
   ```

2. 修饰静态同步方法：修饰静态方法锁定的是这个类的所有对象

   ```java
   synchronized static void lock(){
   }
   ```

3. 修饰一个对象（也叫修饰一个代码块）：跟修饰普通同步方法一样。锁的是对象

   ```java
   void lock(){
       synchronized (this){
       }
   }
   ```

4. 修饰一个类：跟修饰静态方法是一样的，所有对象共用一把锁

   ```java
   void lock(){
       synchronized (Synchronized01.class){
       }
   }
   ```

   总而言之

5. 不管 synchronized 加在方法上还是对象上；只要作用的是非静态的，锁的是对象；作用的是静态的或者类，锁的就是该类的所有对象
6. 每个对象只有一个锁（lock）与之相关联，谁拿到这个锁谁就可以运行它所控制的那段代码
   **底层原理**

修饰一下就能保证同一时间只有一个线程访问了？**底层原理**是怎么做到的？

synchronized 是**通过持有和释放 monitor 对象实现**的，每一个对象都有对应的 monitor 对象

但是对于同步代码块和对象，实现方式又有所区别

_代码块_：通过 **monitorenter 和 monitorexit 指令**实现；当我们用 synchronized 去修饰代码块，编译的时候就会在代码块开头和结尾插入 monitorenter 和 monitorexit 指令（编译后的指令码我们可以通过`javap -c xx.class`查看）；执行 monitorenter 的时候，尝试获取对象的锁，如果锁的计数器为 0，获取 monitor 成功，计数器+1，执行 monitorexit，则-1 释放

_方法_：通过 ACC_SYNCHRONIZED 区分是否是同步方法，如果是，则执行前，先持有 monitor 对象

**对象头**

主要分为三部分：

1. MarkWord 标记字段: 32bit/64bit，重点关注，包含对象的 hashcode、分代年龄、轻量级锁指针、重量级锁指针、GC 标记、偏向锁线程 ID、偏向锁时间戳
2. Class Pointer：类型指针
3. 数组长度

**mark word 详解**

![2021-06-21 am10.09.30](https://muyids.oss-cn-beijing.aliyuncs.com/2021-06-21%20am10.09.30.png)

**锁的四种状态**

升级过程：无锁 -> 偏向锁 -> 轻量级锁 -> 重量级锁

- 无锁

  性能：不加锁，性能最高

  工作原理：

  - ① 无竞争
  - ② 存在竞争，非锁方式同步线程 CAS

- 偏向锁

  性能：不需要线程切换，效率较高

  工作原理：

  - 对象认识这个线程，这个对象的锁偏爱这个线程；
  - 通过 mark work 标记位判断是否偏向锁（是否偏向锁值为 1，锁标志位值为 01）
  - 读取 mark work 前 23 位*线程 ID*确认当前想要获得对象锁的线程

- 轻量级锁

  性能：

  工作原理：

  - 如果当前不只有一个线程想要获取该对象，偏向锁会升级为轻量级锁

  - 升级过程：当第一个拿到偏向锁的线程执行时，遇到有新的进程在询问统一代码块的锁时就有可能会升级成轻量级锁，为什么说是有可能呢？因为偏向锁不会自动释放，此时第 2 个线程询问锁时会出现 2 种情况：

    1. 第一个线程已经执行完毕，那么 CAS 操作将 Mark Word 设置为 Null，第二个线程获取偏向锁，此时不会升级成轻量级锁
    2. 第一个线程未执行完毕，此时第二个线程获取锁失败，那么会进行**自旋**，当自旋达到一定次数后，就会升级成轻量级锁
       [引自](https://blog.csdn.net/wmq880204/article/details/86511234)

  - 当一个线程想要获取某个对象的锁时，假如看到锁标志位为 00， 那么就知道是轻量级锁；这时，线程会在自己的**线程虚拟机栈**中开辟一块 **Lock Record** 空间； Lock Record 存放的是 Mark Word 的副本、owner 对象的指针（指向该对象）；对象头前 30bit 记录了指向 Lock Record 的指针；完成了线程和对象的绑定，线程抢到了该对象的锁；

- 重量级锁

  性能：最差

  工作原理：

  - 当上述轻量级锁升级过程中的第 2 种情况下，**自旋等待的线程数超过 1 个，轻量级锁升级为重量级锁**，通过 monitor 对线程进行管控

**实战演练**

理论是这么讲的，网上资料也很多，我们怎么去验证对不对呢？

先给大家引入一个 jar 包`jol-core(Java Object Layout: Core) `，他可以用来解析 java object 的对象信息

```xml
<dependency>
    <groupId>org.openjdk.jol</groupId>
    <artifactId>jol-core</artifactId>
    <version>0.10</version>
</dependency>
```

我们先来看一下最简单的 object 对象信息如何

![2021-09-07 pm11.09.38](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-07%20pm11.09.38.png)

头四个字节的 markword 字段，最后两位标记位是 01，表示当前对象是**无锁状态**

那么什么时候会升级成**偏向锁**呢？

这里我们先介绍两个 JVM 参数：

- -XX:UseBiasedLocking: 是否打开偏向锁，默认是不打开的
- -XX:BiasedLockingStartupDelay: 默认 4 秒
  JVM 为什么要设置这两个参数呢？

> 因为 java 在一开始启动的时候，要初始化很多对象，如果一开始都要打开偏向锁，会消耗很多资源，所以默认不打开，延迟 4 秒以后才打开

![2021-09-07 pm11.20.46](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-07%20pm11.20.46.png)

我们设置休眠 5S 以后初始化对象 obj2，发现 obj2 果然被设置成了偏向锁状态

当然我们也可以修改这两个参数的设置，比如：

- 关闭偏向锁的延迟：-XX:BiasedLockingStartupDelay=0
- 关闭偏向锁：-XX:-UseBiasedLocking=false，程序默认会进入无锁状态
  **升级到轻量级锁**，我参考了上面轻量级锁的升级过程，开两个线程发现第二个线程总是直接升级成重量级锁，最终也没有出现一次，要是你能实现欢迎在下面评论留言

**升级到重量级锁**，那就简单了，自旋等待的线程数超过 1 个这条件还是很好满足的，我们直接开 100 个线程试一下

```java
public class Jol01 {
    // 临界区
    static int i = 0;
    void add() {
        synchronized (this) {
            try {
                TimeUnit.MICROSECONDS.sleep(1); // 等待一下下，确保同步方法被触发
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            i++;
        }
    }
    public static void main(String[] args) {
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        Jol01 obj = new Jol01();
        System.out.println(ClassLayout.parseInstance(obj).toPrintable());
        for (int i = 1; i <= 100; i++) {
            new Thread(() -> {
                obj.add();
                if (Thread.currentThread().getName().equals("t100")) {
                    System.out.println(Thread.currentThread().getName() + "get Info \n" + ClassLayout.parseInstance(obj).toPrintable());
                }
            }, "t" + i).start();
        }
    }
}
```

前两位 10，表示锁升级为重量级锁

![2021-09-07 pm11.44.09](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-07%20pm11.44.09.png)

#### **总而言之**

1. Java 对象头 mark word 记录锁状态，是无锁、偏向锁、轻量级锁还是重量级锁
2. **锁机制本质**是 **根据资源竞争的激烈程度** 进行**锁升级**的过程
