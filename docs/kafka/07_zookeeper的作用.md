Kafka 中大部分组件都应用了 ZooKeeper

- Controller 选举

- Broker 注册: `/brokers/ids/[0...N]` 记录了 Broker 服务器列表记录，这个**临时节点**的节点数据是 ip 端口之类的信息。

- Topic 注册: `/brokers/topics/xxx`记录了 Topic 的分区信息和 Broker 的对应关系
- partition 的领导者选举
- 生产者负载均衡: 生产者需要将消息发送到对应的 Broker 上，生产者通过 Broker 和 Topic 注册的信息，以及 Broker 和 Topic 的对应关系和变化注册事件 Watcher 监听，从而实现一种动态的负载均衡机制。

- 消息消费进度 Offset 记录：消费者对指定消息分区进行消息消费的过程中，需要定时将分区消息的消费进度 Offset 记录到 ZooKeeper 上，以便消费者进行重启或者其他消费者重新阶段该消息分区的消息消费后，能够从之前的进度开始继续系消费

---

#### **kafka 的 zookeeper 存储结构**

![kafka的zookeeper存储结构](https://muyids.oss-cn-beijing.aliyuncs.com/kafka-zookeeper-storage.png)

#### **Kafka Controller 选举**

Kafka 控制器，其实就是一个 Kafka 系统的 Broker。它除了具有一般 Broker 的功能之外，还具有选举主题分区 Leader 节点的功能。在启动 Kafka 系统时，其中一个 Broker 会被选举为控制器，负责管理主题分区和副本状态，还会执行分区重新分配的管理任务。

选举控制器的核心思路是：各个代理节点公平竞争抢占 Zookeeper 系统中创建/controller 临时节点，最先创建成功的代理节点会成为控制器，并拥有**选举主题分区 Leader 节点**的功能

#### Broker 注册

Broker 是分布式部署并且相互之间相互独立，但是需要有一个注册系统能够将整个集群中的 Broker 管理起来，此时就使用到了 Zookeeper。

在 Zookeeper 上会有一个专门用来进行 Broker 服务器列表记录的节点：`/brokers/ids`

每个 Broker 在启动时，都会到 Zookeeper 上进行注册，即到/brokers/ids 下创建属于自己的节点，如`/brokers/ids/[0...N]`。

Kafka 使用了全局唯一的数字来指代每个 Broker 服务器，不同的 Broker 必须使用不同的 Broker ID 进行注册，创建完节点后，**每个 Broker 就会将自己的 IP 地址和端口信息记录到该节点**中去。其中，Broker 创建的节点类型是临时节点，一旦 Broker 宕机，则对应的临时节点也会被自动删除。

#### Topic 注册

在 Kafka 中，同一个 Topic 的消息会被分成多个分区并将其分布在多个 Broker 上，这些分区信息及与 Broker 的对应关系也都是由 Zookeeper 在维护，由专门的节点来记录，如：`/brokers/topics`

Kafka 中每个 Topic 都会以`/brokers/topics/[topic]`的形式被记录，如`/brokers/topics/login`和`/brokers/topics/search`等。Broker 服务器启动后，会到对应 Topic 节点（`/brokers/topics`）上注册自己的`Broker ID`并写入针对该 Topic 的分区总数

如`/brokers/topics/login/3->2`，这个节点表示 Broker ID 为 3 的一个 Broker 服务器，对于"login"这个 Topic 的消息，提供了 2 个分区进行消息存储，同样，这个分区节点也是临时节点。

#### **生产者负载均衡**

由于同一个 Topic 消息会被分区并将其分布在多个 Broker 上，因此，生产者需要将消息合理地发送到这些分布式的 Broker 上，那么如何实现生产者的负载均衡，Kafka 支持传统的四层负载均衡，也支持 Zookeeper 方式实现负载均衡。

(1) 四层负载均衡，根据生产者的 IP 地址和端口来为其确定一个相关联的 Broker。通常，一个生产者只会对应单个 Broker，然后该生产者产生的消息都发往该 Broker。这种方式逻辑简单，每个生产者不需要同其他系统建立额外的 TCP 连接，只需要和 Broker 维护单个 TCP 连接即可。但是，其无法做到真正的负载均衡，因为实际系统中的每个生产者产生的消息量及每个 Broker 的消息存储量都是不一样的，如果有些生产者产生的消息远多于其他生产者的话，那么会导致不同的 Broker 接收到的消息总数差异巨大，同时，生产者也无法实时感知到 Broker 的新增和删除。
