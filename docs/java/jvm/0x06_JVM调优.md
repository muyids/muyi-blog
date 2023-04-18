如何进行 jvm 调优？jvm 参数有哪些？怎么查看一个 java 进程的 jvm 参数？

谈谈你了解的 jvm 参数。如果一个 java 程序每运行一段时间后，就非常卡顿，你准备如何优化？

**jvm 调优**

主要就是通过定制 jvm 运行参数来提高 java 应用程序的运行速度

**jvm 参数**

大致可以分为三类：

**1.标准指令**：-开头，所有 HotSpot 都支持的参数。可以用 java -help 打印出来

**2.非标准指令**：-X 开头，通常是跟特定的 HotSpot 版本对应，可以用 java -X 打印出来。常用配置的几项：

```
 -Xms    设置初始 Java 堆大小
 -Xmx    设置最大 Java 堆大小
 -Xss    设置 Java 线程堆栈大小
```

**3.不稳定参数**：-XX 开头，跟特性 HotSpot 版本对应，变化非常大。缺少详细的文档资料。在 JDK1.8 版本下，有几个常用的不稳定指令:

java -XX:+PrintCommandLineFlags : 查看当前命令的不稳定指令

```
$ java -XX:+PrintCommandLineFlags -version
 -XX:InitialHeapSize=268435456 -XX:MaxHeapSize=4294967296 -XX:+PrintCommandLineFlags -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseParallelGC
 java version "1.8.0_251"
 Java(TM) SE Runtime Environment (build 1.8.0_251-b08)
 Java HotSpot(TM) 64-Bit Server VM (build 25.251-b08, mixed mode)
```

java -XX:+PrintFlagsInitial : 查看所有不稳定指令的默认值

```
 ➜  ~ java -XX:+PrintFlagsInitial -version
 [Global flags]
      intx ActiveProcessorCount                      = -1                                  {product}
     uintx AdaptiveSizeDecrementScaleFactor          = 4                                   {product}
     ......
     uintx AdaptiveTimeWeight                        = 25                                  {product}
      bool AdjustConcurrency                         = false                               {product}
      intx AliasLevel                                = 3                                   {C2 product}
     ......
     bool UseSerialGC      (串行化GC)              = false                               {product}
     ....
     bool UseTLAB    （Thread Local Allocate Buffer）   = true                       {pd product}
     ...
```

java -XX:+PrintFlagsFinal : 查看所有不稳定指令最终生效的实际值

可以通过 grep 命令查看常用配置项，比如 `java -XX:+PrintFlagsFinal -version | grep GC`

**实际场景调优**

我们根据经验修改 jvm 参数后，怎么确定我们的调优效果？

在我们的 java 安装 bin 目录下自带一些工具，比如我的安装目录

```
 /Library/Java/JavaVirtualMachines/jdk1.8.0_251.jdk/Contents/Home/bin
 ➜ ls
 appletviewer   jarsigner      javafxpackager jcmd           jhat           jmc            jstack         keytool        policytool     schemagen      unpack200
 extcheck       java           javah          jconsole       jinfo          jps            jstat          native2ascii   rmic           serialver      wsgen
 idlj           javac          javap          jdb            jjs            jrunscript     jstatd         orbd           rmid           servertool     wsimport
 jar            javadoc        javapackager   jdeps          jmap           jsadebugd      jvisualvm      pack200        rmiregistry    tnameserv      xjc
```

**jvm 调优常用手段**

**1、java 自带工具**

**`jvisualvm`**

其他自带工具还有：

- jps ： 查看 java 进程

- jstack + 进程号 ：打印进程堆栈

**2、阿里的 arthas**

文档：https://arthas.aliyun.com/doc/

使用：`java -jar arthas-boot.jar`

选择要查看的进程 id，输入命令查看对应信息

常用命令：

dashboard（用的最多的）

观察 GC 的次数是否过于频繁，并且堆内存没有明显变化，说明 GC 效率很低，堆内存中可能存在较多大对象；

thread 查看线程信息

线程死锁：`thread -b`

死锁代码：

```java
 class HoldLockThread implements Runnable {
     String lockA;
     String lockB;
     public HoldLockThread(String lockA, String lockB) {
         this.lockA = lockA;
         this.lockB = lockB;
     }
     @Override
     public void run() {
         synchronized (lockA) {
             System.out.println(Thread.currentThread().getName() + "\t lockA get lockB");
             synchronized (lockB) {
                 System.out.println(Thread.currentThread().getName() + "\t lockB get lockA");
             }
         }
     }
 }
 public class DeadLockDemo {
     public static void main(String[] args) {
         String lockA = "lockA";
         String lockB = "lockB";
         new Thread(new HoldLockThread(lockA, lockB), "threadAAAA").start();
         new Thread(new HoldLockThread(lockB, lockA), "threadBBBB").start();
     }
 }
```

**`thread -b`排查：**

```
 [arthas@3553]$ thread -b
 "threadAAAA" Id=11 BLOCKED on java.lang.String@65432efb owned by "threadBBBB" Id=12
     at com.muyids.cloud.ago.juc.lock.HoldLockThread.run(DeadLockDemo.java:17)
     -  blocked on java.lang.String@65432efb
     -  locked java.lang.String@3336057 <---- but blocks 1 other threads!
     at java.lang.Thread.run(Thread.java:748)
```
