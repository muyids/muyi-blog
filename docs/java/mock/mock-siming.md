## 1.HashMap 扩容时候为什么要扩容到原来的 2 倍

- 做除余的时候 2 的倍数可以直接使用&进行快速计算

  例如: `19%16`可以写成`19&(16-1)`，位运算更高效

- 扩容的时候只移动大约一半的数据，不会造成扩容之后碰撞更加严重的情况

  看源码，得知通过计算`(n - 1) & hash`来确定 key 的索引位置，当 HashMap 的容量 n 是 2 的次幂时，`n - 1`的二进制都是 1，如 15 的二进制后四位为 1111，&操作的后几位均一致，只有扩容后的第一位会有 0 和 1 的区别，如果是 0 的话索引没变，是 1 的话索引变成“原索引+oldCap；相当于只移动了一半的数据

总结，HashMap 以 2 倍扩容，目的就是减少 hash 碰撞，使元素分配均匀。

## 2.hashmap 扩容时每个 entry 需要再计算一次 hash 吗？

1）在 jdk7 中是需要进行重新 hash 的，但是在 jdk8 中做了一定的优化
2）只需要看原来的 hash 值在扩容后新增的那一位是 1 还是 0，如果是 0 的话索引没变，是 1 的话索引变成“原索引+oldCap

## 2.如何用 TreeMap 实现一致性 hash？

TreeMap：基于红黑树实现的，key 是有序的, Treemap.ceilingEntry 可以找到最近的节点

```java
/**
 * 输入一个要存储的value
 *
 * @param value
 * @return
 */
public static String getRealServerNode(String value) {
    // 1.传递来一个字符串, 得到它的hash值
    Integer vnode = value.hashCode() % 1024; // 210
    // 2.找到对应节点最近的key的节点值
    Map.Entry<Integer, String> node = virtualNodeMap.ceilingEntry(vnode); // 删除前210，删除后211
    String realNode = node.getValue();
    return realNode;
}
```

## 3.Executors 创建线程的弊端

说明：Executors 各个方法的弊端：
1）newFixedThreadPool 和 newSingleThreadExecutor:
主要问题是堆积的请求处理队列可能会耗费非常大的内存，甚至 OOM。
2）newCachedThreadPool 和 newScheduledThreadPool:
主要问题是线程数最大数是 Integer.MAX_VALUE，可能会创建数量非常多的线程，甚至 OOM。

## Java-五种线程池，四种拒绝策略，四种阻塞队列

三种阻塞队列：
BlockingQueue<Runnable> workQueue = null;
workQueue = new ArrayBlockingQueue<>(5);//基于数组的先进先出队列，有界
workQueue = new LinkedBlockingQueue<>();//基于链表的先进先出队列，无界
workQueue = new SynchronousQueue<>();//无缓冲的等待队列，无界
四种拒绝策略：
RejectedExecutionHandler rejected = null;
rejected = new ThreadPoolExecutor.AbortPolicy();//默认，队列满了丢任务抛出异常
rejected = new ThreadPoolExecutor.DiscardPolicy();//队列满了丢任务不异常
rejected = new ThreadPoolExecutor.DiscardOldestPolicy();//将最早进入队列的任务删除，之后再尝试加入队列
rejected = new ThreadPoolExecutor.CallerRunsPolicy();//如果添加到线程池失败，那么主线程会自己去执行该任务
五种线程池：
ExecutorService threadPool = null;
threadPool = Executors.newCachedThreadPool();//有缓冲的线程池，线程数 JVM 控制
threadPool = Executors.newFixedThreadPool(3);//固定大小的线程池
threadPool = Executors.newScheduledThreadPool(2);
threadPool = Executors.newSingleThreadExecutor();//单线程的线程池，只有一个线程在工作
threadPool = new ThreadPoolExecutor();//默认线程池，可控制参数比较多
线程池推荐用：ThreadPoolExecutor executor;

## 4.四种阻塞队列的区别

1、ArrayBlockingQueue：基于数组的先进先出队列，有界
2、LinkedBlockingQueue：基于链表的先进先出队列，无界。静态工厂方法 Executors.newFixedThreadPool()使用了这个队列
3、SynchronousQueue : 无缓冲的等待队列，无界; 适合生产者通知消费者的情况; 跟 Redis 的`lpush + brpop`的使用场景很像； 每个插入操作必须等到另一个线程调用移除操作，否则插入操作一直处于阻塞状态，静态工厂方法 Executors.newCachedThreadPool（5）使用了这个队列。

关于上面几种阻塞队列的吞吐量比较：

![1901623982655_.pic](https://muyids.oss-cn-beijing.aliyuncs.com/1901623982655_.pic.jpg)

4、PriorityBlockingQueue : 一个具有优先级的无限阻塞队列。

底层是堆

## 9.线程池拒绝策略

RejectedExecutionHandler rejected = null;

- rejected = new ThreadPoolExecutor.AbortPolicy();//默认，队列满了丢任务抛出异常
- rejected = new ThreadPoolExecutor.DiscardPolicy();//队列满了丢任务不异常；静默丢弃
- rejected = new ThreadPoolExecutor.DiscardOldestPolicy();// 丢弃队列最前面的任务，然后重新提交被拒绝的任务。
- rejected = new ThreadPoolExecutor.CallerRunsPolicy(); // 由调用线程（主线程）处理该任务

## 5.类加载过程

加载:查找并且加载类的二进制数据
链接：
验证:确保被加载类的正确性
准备:为类的静态变量分配内存，并将其初始化为默认值
解析:把类中的符号引用转换为直接引用
初始化:执行构造方法

## 6.java gc 时候的 safe point 如何确定

## 7.tomcat 如何实现热加载

(1) 一种是类似于 Servlet 这种类的热部署即在 WEB-INF/class 目录下的类：实现方式可以概括为在容器启动的时候起一条后台线程，定时的检测类文件的时间戳变化，如果类的时间戳变掉了，则调用容器的 reload 的方法，将类重新载入。
(2)为了实现 JSP 的加载部署，tomcat 实现了另一个加载器即 org.apache.jasper.servlet.JasperLoader.JSP 属于一次消费品，每次访问都会重新加载（网上说的，这个源代码下次再研究下，在这先记录下）
(3)在读源码的时候身边研究了下$CATALINA_HOME/conf/web.xml，这个配置文件是 tomcat 内置的配置文件，主要配置了两个 Servlet. 具体的配置如下：

## 8.范型 PECS，范型自限定

范型 PECS ：如果要从集合中读取类型 T 的数据，并且不能写入，可以使用 ? extends 通配符；(Producer Extends)
如果要从集合中写入类型 T 的数据，并且不需要读取，可以使用 ? super 通配符；(Consumer Super)
如果既要存又要取，那么就不要使用任何通配符。
从集合中取元素, 使用<? extends T>通配符
向集合中放元素, 使用<? super T>通配符

## 10.如何查看线程死锁

使用 jstack 命令
mysql 死锁使用 mysql 命令
解除正在死锁的状态有两种方法：
第一种： 1.查询是否锁表
show OPEN TABLES where In_use > 0; 2.查询进程（如果您有 SUPER 权限，您可以看到所有线程。否则，您只能看到您自己的线程）
show processlist 3.杀死进程 id（就是上面命令的 id 列）
kill id

第二种： 1.查看下在锁的事务
SELECT \* FROM INFORMATION_SCHEMA.INNODB_TRX; 2.杀死进程 id（就是上面命令的 trx_mysql_thread_id 列）
kill 线程 ID
例子：
查出死锁进程：SHOW PROCESSLIST
其它关于查看死锁的命令：
1：查看当前的事务

SELECT _ FROM INFORMATION_SCHEMA.INNODB_TRX;
2：查看当前锁定的事务
SELECT _ FROM INFORMATION_SCHEMA.INNODB_LOCKS;
3：查看当前等锁的事务
SELECT \* FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;

---

## 1 redis 的 IO 模型和 Dubbo 的 IO 模型区别

​ redis6.0 以后的 IO 模型：单 work 线程，多 IO 线程
DUBBO 是基于 netty 的 ，基于 java nio 的，一个或者多个 selector 管理多个。 channel
linux 使用的 epoll。

## 2 redis5 大类型的底层数据结构

1）string
int 编码
raw 编码。字符串 44 以上时，升级到此类型
embstr 编码 字符串 42 时候
2）list
ziplist
_ 试图往列表新添加一个字符串值，且这个字符串的长度超过 server.list_max_ziplist_value （默认值为 64 ）。
_ ziplist 包含的节点超过 server.list_max_ziplist_entries （默认值为 512 ）。膨胀为 linkedlist
linkedlist
3）hash
ziplist
hashtable
4）set
intset
hashtable
5）zset
ziplist 元素数量大于 128 或 member 的长度大于 64 字节满足其一升级为 skiplist
skiplist
Ziplist 一个压缩列表可以包含任意多个节点(entry),每个节点可以保存一个字节数组或者一个整数值.

## 3 redis 淘汰策略

1. noeviction：当内存使用超过配置的时候会返回错误，不会驱逐任何键
2. allkeys-lru：加入键的时候，如果过限，首先通过 LRU 算法驱逐最久没有使用的键
3. volatile-lru：加入键的时候如果过限，首先从设置了过期时间的键集合中驱逐最久没有使用的键
4. allkeys-random：加入键的时候如果过限，从所有 key 随机删除
5. volatile-random：加入键的时候如果过限，从过期键的集合中随机驱逐
6. volatile-ttl：从配置了过期时间的键中驱逐马上就要过期的键
7. volatile-lfu：从所有配置了过期时间的键中驱逐使用频率最少的键
8. allkeys-lfu：从所有键中驱逐使用频率最少的键

## 3 redis 扩容时机，以及扩容原理

1、哈希表中保存的 key 数量超过了哈希表的大小（可以看出 size 既是哈希表大小，同时也是扩容阈值） 100->128, 500->512
2、当前没有子进程在执行 aof 文件重写或者生成 RDB 文件；或者保存的节点数与哈希表大小的比例超过了安全阈值（默认值为 5）
扩容原理
渐进式 rehash

## 4 redission 的 watchdog 是什么

## 5 redis 集群，为什么是 16384？哨兵模式，选举过程，会有脑裂问题么？raft 算法，优缺点

redis 集群中 每秒会随机选取 5 个节点，找出最久没有通信的节点发送 ping 消息，而 slot 每次心跳的时候都会被发送（是个 bitmap）。如果 solt 大于 16384 的活会造成消息体过大。

如果 master 挂了，奇数个哨兵节点发起投票，选出被投票最多的那个从节点

如下配置可以减少异步复制和脑裂导致的数据丢失
min-slaves-to-write 1
min-slaves-max-lag 10

raft 算法的优缺点
此文章总结的 raft https://blog.csdn.net/daaikuaichuan/article/details/98627822
Raft 和 Paxos 的区别和优缺点？
只适用于 permissioned systems (私有链)，只能容纳故障节点(CFT)，不容纳作恶节点。
Raft 的 leader 有限制，拥有最新日志的节点才能成为 leader，multi-paxos 中对成为 Leader 的限制比较低，任何节点都可以成为 leader。
Raft 中 Leader 在每一个任期都有 Term 号。

## 6 Redis 字符串实现 SDS 和 c 区别，空间预分配，惰性空间释放

空间预分配用于优化 SDS 的字符串增长操作： 当 SDS 的 API 对一个 SDS 进行修改， 并且需要对 SDS 进行空间扩展的时候， 程序不仅会为 SDS 分配修改所必须要的空间， 还会为 SDS 分配额外的未使用空间。
其中， 额外分配的未使用空间数量由以下公式决定：
如果对 SDS 进行修改之后， SDS 的长度（也即是 len 属性的值）将小于 1 MB ， 那么程序分配和 len 属性同样大小的未使用空间， 这时 SDS len 属性的值将和 free 属性的值相同。 举个例子， 如果进行修改之后， SDS 的 len 将变成 13 字节， 那么程序也会分配 13 字节的未使用空间， SDS 的 buf 数组的实际长度将变成 13 + 13 + 1 = 27 字节（额外的一字节用于保存空字符）。
如果对 SDS 进行修改之后， SDS 的长度将大于等于 1 MB ， 那么程序会分配 1 MB 的未使用空间。 举个例子， 如果进行修改之后， SDS 的 len 将变成 30 MB ， 那么程序会分配 1 MB 的未使用空间， SDS 的 buf 数组的实际长度将为 30 MB + 1 MB + 1 byte 。
通过空间预分配策略， Redis 可以减少连续执行字符串增长操作所需的内存重分配次数。
惰性空间释放
惰性空间释放用于优化 SDS 的字符串缩短操作： 当 SDS 的 API 需要缩短 SDS 保存的字符串时， 程序并不立即使用内存重分配来回收缩短后多出来的字节， 而是使用 free 属性将这些字节的数量记录起来， 并等待将来使用。

## 6 Redis 主从复制原理

异步复制， 快照全量复制，增量复制。
每个实例都有 offset， 如果 slave 实例的 offset，还在 master 的缓冲区内，则使用增量复制，否则使用全量复制

---

## 1 什么是 restful 风格

什么是伪共享，为何会出现，如何避免

cpu 缓存行单位 64Byte
在对象内部补齐缺少位数
java8 注解@Contened

## 3 SpringBoot @Component 和 @Bean 注解的区别

@Component（@Controller、@Service、@Repository）通常是通过类路径扫描来自动侦测以及自动装配到 Spring 容器中。
而@Bean 注解通常是我们在标有该注解的方法中定义产生这个 bean 的逻辑。
@Component 作用于类，@Bean 作用于方法。

## 5 Spring Bean 的作用域之间有什么区别？

singleton
全局只有一个实例
prototype
每次调用产生一个新的实例
在 web 使用的时候还有三个作用域，但是必须在 web.xml 中注册一个 RequestContextListener ， 目的是为了设置每次请求开始和结束都可以使 spring 得到相应的事件。
request
每次请求产生一个 bean
session
每个用户 session 可以产生一个新的 bean，不同用户之间的 bean 互相不影响
globalSession
作用和 session 类似，只是使用 portlet 的时候使用。

## 6 Spring 框架中都用到了哪些设计模式？

单例 工厂 代理 模版方法 适配器(AOP 时)

## 6 Spring 几种 AOP 方式的区别

传统 proxy 被代理类必须继承接口
cglib ：CGLIB 代理主要通过对字节码的操作，为对象引入间接级别，以控制对象的访问。我们知道 Java 中有一个动态代理也是做这个事情的，那我们为什么不直接使用 Java 动态代理，而要使用 CGLIB 呢？答案是 CGLIB 相比于 JDK 动态代理更加强大，JDK 动态代理虽然简单易用，但是其有一个致命缺陷是，只能对接口进行代理。
aspectj 使用最广泛的 aop，使用注解@Aspect ，AspectJ 静态编译织入。前面两种都是说的在代码运行时动态的生成 class 文件达到动态代理的目的，那我们现在回到静态代理，静态代理唯一的缺点就是我们需要对每一个方法编写我们的代理逻辑，造成了工作的繁琐和复杂。AspectJ 就是为了解决这个问题，在编译成 class 字节码的时候在方法周围加上业务逻辑。复杂的工作由特定的编译器帮我们做。
asm ：主要是操作 PO 字节 dng 码的

## 7 SpringBoot 启动过程

@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
@Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })

## 7 Spring 启动流程

初始化环境—>加载配置文件—>实例化 Bean—>调用 Bean 显示信息
每一个对象都是一个 beanDefinition
1 BeanDefinition 定义
2 构造方法推断 选出一个对象的构造方法
3 实例化。构造方法反射得到对象
4 属性填充 给属性进行自动填充
5 初始化 对其他属性赋值校验
6 初始化后 aop 生成代理对象
1 获取最牛工厂 ApplicationContext 接口能获取到 AutowireCapableBeanFactory，就是最右上角那个，然后它向下转型就能得到 DefaultListableBeanFactory 了。

2 Spring 中的 Bean 是什么？你要知道 Bean 在代码层面上可以简单认为是 BeanDefinition 的实例。BeanDefinition 中保存了我们的 Bean 信息，比如这个 Bean 指向的是哪个类、是否是单例的、是否懒加载、这个 Bean 依赖了哪些 Bean 等等。如果该 Bean 采用工厂方法生成，指定工厂名称。

3 一句话就是：有些实例不是用反射生成的，而是用工厂模式生成的。void setFactoryBeanName(String factoryBeanName);

4 Bean 中的属性值，后面给 bean 注入属性值用到 MutablePropertyValues getPropertyValues();
5 以上就是 BeanDefinition 的解析，其实可以认为是一个图纸，规定了 bean 是反射或者工厂来产生，自己是不是单例等等。
6 allowBeanDefinitionOverriding allowBeanDefinitionOverriding 属性为 null，如果在同一配置文件中重复了，会抛错，但是如果不是同一配置文件中，会发生覆盖。允许循环依赖 allowCircularReferences。

AOP 发生在初始化后
另一种方式
1 创建 ApplicationContext 对象
扫描某个包下面的类 得到 BeanDefinition，并把 BeanDefinition 存到一个 Map 里
然后筛选出非懒加载的单例 Bean，多例 Bean 不需要在启动时候加载，多例 Bean 会在每次获取 Bean 的时候利用 BeanDefinition 去创建
单例 Bean 创建完成后，Spring 会发布一个容器启动事件
Spring 容器启动结束
通过@BeanPostProcessor 来实现依赖注入
@BeanFactoryPostProcessor

7 Spring 事物

---

## 1 对象头都有什么，为什么对象指针可以被压缩，

markWord
类指针 压缩 4Byte 不压缩 8Byte
对象指针
对齐标记

## 2 CMS GC 回收分为哪几个阶段？分别做了什么事情？

1. 标记阶段，首先初始标记(Initial-Mark),这个阶段是停顿的(Stop the World Event)，并且会触发一次普通 Mintor GC。对应 GC log:GC pause (young) (inital-mark)
2. Root Region Scanning，程序运行过程中会回收 survivor 区(存活到老年代)，这一过程必须在 young GC 之前完成。
3. Concurrent Marking，在整个堆中进行并发标记(和应用程序并发执行)，此过程可能被 young GC 中断。在并发标记阶段，若发现区域对象中的所有对象都是垃圾，那个这个区域会被立即回收(图中打 X)。同时，并发标记过程中，会计算每个区域的对象活性(区域中存活对象的比例)。
4. Remark, 再标记，会有短暂停顿(STW)。再标记阶段是用来收集 并发标记阶段 产生新的垃圾(并发阶段和应用程序一同运行)；G1 中采用了比 CMS 更快的初始快照算法:snapshot-at-the-beginning (SATB)。
5. Copy/Clean up，多线程清除失活对象，会有 STW。G1 将回收区域的存活对象拷贝到新区域，清除 Remember Sets，并发清空回收区域并把它返回到空闲区域链表中。

## 3 Concurrent Model Failure 和 ParNew promotion failed 什么情况下会发生？

1. CMS 收集器无法处理浮动垃圾，可能出现“Concurrent Mode Failure”失败而导致另一次 Full GC 的产生。

## 4 cms 的收集过程，G1 收集器原理，怎么实现预测停顿的，region 的大小与结构

cms 的收集过程 https://www.cnblogs.com/webor2006/p/11110263.html
G1 的另一个显著特点他能够让用户设置应用的暂停时间，为什么 G1 能做到这一点呢？也许你已经注意到了，G1 回收的第 4 步，它是“选择一些内存块”，而不是整代内存来回收，这是 G1 跟其它 GC 非常不同的一点，其它 GC 每次回收都会回收整个 Generation 的内存(Eden, Old), 而回收内存所需的时间就取决于内存的大小，以及实际垃圾的多少，所以垃圾回收时间是不可控的；而 G1 每次并不会回收整代内存，到底回收多少内存就看用户配置的暂停时间，配置的时间短就少回收点，配置的时间长就多回收点，伸缩自如。 (阿里面试)

## 5 JVM 内存结构，GC Root 从哪找

gc root
栈中的本地变量
静态变量
本地方法栈中的变量
正在运行的线程

---

## 1 springCloud 有哪些组件

注册中心 & 配置中心
Eureka：闭源
nacos: 阿里基于 Eureka 开发的分支。强弱一致性可调整，适合注册中心，和配置中心
zookeeper: 强一致性（过半节点 ack），适合配置中心
网关
zuul: 闭源
gateway: 更适合做业务网关，继承自 zuul2.带鉴权功能与 springCloud 结合性好，社区活跃，未来前景最好。并且在在网关层直接可以和 sentinel 配合实现限流
Nginx+Lua：更适合做门户网关，性能最高，最成熟稳定，能使用在几乎任何场景。但是 nginx+lua 是一种有状态的服务部署方式，不符合云原生的规范。并且 lua 脚本在 java 团队普及度不高，重新定制功能不便
rpc 框架
Ribbon+feign: 与 springCloud 生态融合较好，开发效率更高。http 层的调用支持协议单一性能不如 dubbo，但是 Ribbon Hystrix Feign 在服务治理中，配合 Spring Cloud 做微服务，使用上有很多优势，社区也比较活跃，看将来更新发展。
负载均衡：
随机· 规则轮询· 空闲策略· 响应时间策略
容错机制：
使用 Hystrix
路由、流量调度、ABtest
Ribbon 主要通过扩展 AbstractLoadBalancerRule 负载均衡的方法来实现，在负载均衡的部分还要进行改造升级。
ribbon 负载均衡的原理是什么， 拦截器，拦截带有 ribbon 注解的方法，讲方法转换到 IP 地址
IRule，ILoadBalance
OpenFeign:

resttemplate：

Dubbo: 支持协议多，适合各种场景，性能上 dubbo 可以根据配置灵活使用
负载均衡：
随机 · 权重轮询 · 最少活跃调用数 · 一致性 Hash 策略。
容错机制：
Dubbo 提供了一整套 FailOver、FailFast、Failsafe、FailBack、Aviailable、Broadcast、Forking 策略，以及 Mock
路由、流量调度、ABtest：
Dubbo 通过界面化、校本化配置路由规则，可以实现灰度发布、动态流量调度、容量计算等，方案成熟

gRPC:

为什么选用 Ribbon+feign 而不选用 Dubbo，
1 与现在的 Spring 生态结合度好
2 我们以 http 的方式进行全链路追踪
3 dubbo rpc 的方式调用不好调试
4 dubbo 不是跨语言的，feign 是 restful 风格的 http 调用

降级限流
Hystrix : 请求合并，熔断限流降级，服务隔离
Sentinel ： 熔断限流降级

在限制的手段上，Sentinel 和 Hystrix 采取了完全不一样的方法。
Hystrix 通过线程池的方式，来对依赖(在我们的概念中对应资源)进行了隔离。这样做的好处是资源和资源之间做到了最彻底的隔离。缺点是除了增加了线程切换的成本，还需要预先给各个资源做线程池大小的分配。
Sentinel 对这个问题采取了两种手段:
通过并发线程数进行限制
和资源池隔离的方法不同，Sentinel 通过限制资源并发线程的数量，来减少不稳定资源对其它资源的影响。这样不但没有线程切换的损耗，也不需要您预先分配线程池的大小。当某个资源出现不稳定的情况下，例如响应时间变长，对资源的直接影响就是会造成线程数的逐步堆积。当线程数在特定资源上堆积到一定的数量之后，对该资源的新请求就会被拒绝。堆积的线程完成任务后才开始继续接收请求。
通过响应时间对资源进行降级
除了对并发线程数进行控制以外，Sentinel 还可以通过响应时间来快速降级不稳定的资源。当依赖的资源出现响应时间过长后，所有对该资源的访问都会被直接拒绝，直到过了指定的时间窗口之后才重新恢复。

监控中心
springBoot admin
日志系统

消息队列

分布式缓存

链路追踪
Skywalking
pinPoint

NetFlix Sleuth

微服务的架构原理是什么？
面向 SOA， 更加细小的的拆分服务，将功能分解到各个服务当中，从而降低系统的耦合性，并提供更加灵活的服务支持

## 2.常用的六大设计模式原则

1)单一职责原则 2)里氏替换原则 3)依赖倒转原则 4)接口隔离原则 5)迪米特法则 一个对象应该对其他对象保持最少的了解。 6)开闭原则

## 3 DDD 和六边形架构

https://www.yuque.com/docs/share/8a9e3fb6-e4c4-40a7-bc81-10aaa0f8109a

如何明确领域

## 4 公司架构

高等数字
基础数字
机构线
内容库
公立线
passport 账号体系
学生端
外研优学
作业服务
学生自主练习
教师端
外研优学教师
备授课平台
家长端
外研优学家长
外研之声

---

## TCP 的滑动窗口协议有什么用

1 保证消息顺序
2 提升吞吐量

## 2. tcp 3 次握手和 4 次挥手

## io 模型了解么？多路复用，selete，poll，epoll，epoll 的结构，怎么注册事件，et 和 lt 模式

epoll
epoll 是在 2.6 内核中提出的，是之前的 select 和 poll 的增强版本。相对于 select 和 poll 来说，epoll 更加灵活，没有描述符限制。epoll 使用一个文件描述符管理多个描述符，将用户关系的文件描述符的事件存放到内核的一个事件表中，这样在用户空间和内核空间的 copy 只需一次。
基本原理：

epoll 支持水平触发和边缘触发，最大的特点在于边缘触发，它只告诉进程哪些 fd 刚刚变为就绪态，并且只会通知一次。还有一个特点是，epoll 使用“事件”的就绪通知方式，通过 epoll_ctl 注册 fd，一旦该 fd 就绪，内核就会采用类似 callback 的回调机制来激活该 fd，epoll_wait 便可以收到通知。

epoll 的优点：

没有最大并发连接的限制，能打开的 FD 的上限远大于 1024（1G 的内存上能监听约 10 万个端口）。

效率提升，不是轮询的方式，不会随着 FD 数目的增加效率下降。只有活跃可用的 FD 才会调用 callback 函数；即 Epoll 最大的优点就在于它只管你“活跃”的连接，而跟连接总数无关，因此在实际的网络环境中，Epoll 的效率就会远远高于 select 和 poll。

内存拷贝，利用 mmap()文件映射内存加速与内核空间的消息传递；即 epoll 使用 mmap 减少复制开销。

epoll 对文件描述符的操作有两种模式：LT（level trigger）和 ET（edge trigger）。LT 模式是默认模式，LT 模式与 ET 模式的区别如下：

LT 模式：当 epoll_wait 检测到描述符事件发生并将此事件通知应用程序，应用程序可以不立即处理该事件。下次调用 epoll_wait 时，会再次响应应用程序并通知此事件。

ET 模式：当 epoll_wait 检测到描述符事件发生并将此事件通知应用程序，应用程序必须立即处理该事件。如果不处理，下次调用 epoll_wait 时，不会再次响应应用程序并通知此事件。

ET 模式在很大程度上减少了 epoll 事件被重复触发的次数，因此效率要比 LT 模式高。epoll 工作在 ET 模式的时候，必须使用非阻塞套接口，以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。

---

1 CyclicBarrier 和 CountDownLatch
CyclicBarrier 等待多个线程到达同一个条件，再开始下一件事情，new Runnable 处理，主线程不处理。
CountDownLatch 等待其他线程执行完主线程再进行后续逻辑

2 多线程如何防止死锁
资源互斥， 资源抢占，线程持有资源不释放，相互等待
从上述其一下手，
使用 tryLock，设置过期时间
3 CopyOnWriteArrayList 是如何保证线程安全的
写的时候加上一把重入锁，并且 copy 一份数据数据，把新的数组最后一位+1，在此位加入这次 add 的数据。
读的时候无锁

4 DelayQueue 实现原理，LinkedBlockingqueue ArrayBlockingqueue
优先级队列+Aqs， offer 和 take 是两把锁，ArrayBlockingqueue offer 和 take 是一把锁
5 ConcurrentHashMap 是如何让多线程同时参与扩容？
每个线程同时都只扩容一个题桶区间
6 AQS 是如何唤醒下一个线程的？
Head 当前线程，在 waitStatu 为-1 时，把指针指向下一个 node
7 AQS 是如何实现公平非公平的
公平 node 放在队尾， 非公平抢一次头 node，抢到了就抢到了锁，没抢到放到队尾
