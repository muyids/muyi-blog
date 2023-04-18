# 背景

最近公司的 3 节点 kafka 集群，发现有 2 个节点所在的刀箱交换机有故障风险，会随机性的出现端口 up/down 的情况。 因此需要临时将这 2 个 broker 迁移出来，等交换机修复后再迁移回去。

**下面是实验模拟的整个过程（扩容+缩容）**

原先的 3 节点的 kafka 假设为 node1、node2、node3

准备 2 台空闲点的服务器（这里假设为 node4 和 node5）

系统版本：CentOS7

    node1  192.168.2.187
    node2  192.168.2.188
    node3  192.168.2.189
    node4  192.168.2.190
    node5  192.168.2.191

kafka 的扩容操作分为 2 步：

1. zk 节点扩容
2. kafka 节点扩容

# 首先在 node4 node5 上把相关的软件部署好：

```shell
cd /root/
tar xf zookeeper-3.4.9.tar.gz
tar xf kafka_2.11-0.10.1.0.tar.gz
tar xf jdk1.8.0_101.tar.gz

mv kafka_2.11-0.10.1.0  zookeeper-3.4.9   jdk1.8.0_101   /usr/local/

cd /usr/local/
ln -s zookeeper-3.4.9   zookeeper-default
ln -s kafka_2.11-0.10.1.0  kafka-default
ln -s jdk1.8.0_101    jdk-default
```

# 第一部分：zk 节点的扩容：

1. 在 node4 上执行：

```shell
mkdir /usr/local/zookeeper-default/data/
vim  /usr/local/zookeeper-default/conf/zoo.cfg  在原有的基础上，增加最后的2行配置代码：
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper-default/data/
clientPort=2181
maxClientCnxns=2000
maxSessionTimeout=240000
server.1=192.168.2.187:2888:3888
server.2=192.168.2.188:2888:3888
server.3=192.168.2.189:2888:3888
server.4=192.168.2.190:2888:3888
server.5=192.168.2.191:2888:3888

## 清空目录防止有脏数据
rm -fr /usr/local/zookeeper-default/data/*
## 添加对应的myid文件到zk数据目录下
echo 4 > /usr/local/zookeeper-default/data/myid
```

2. 启动 node4 的 zk 进程:

```shell
/usr/local/zookeeper-default/bin/zkServer.sh start
/usr/local/zookeeper-default/bin/zkServer.sh  status   类似如下效果：
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper-default/bin/../conf/zoo.cfg
Mode: follower
/usr/local/zookeeper-default/bin/zkCli.sh

echo stat | nc 127.0.0.1 2181  结果类似如下:
Zookeeper version: 3.4.9-1757313, built on 08/23/2016 06:50 GMT
Clients:
 /127.0.0.1:50072[1](queued=0,recved=6,sent=6)
 /127.0.0.1:50076[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/2/13
Received: 24
Sent: 23
Connections: 2
Outstanding: 0
Zxid: 0x10000009a
Mode: follower
Node count: 63
```

3. 在 node5 上执行：

```shell
vim  /usr/local/zookeeper-default/conf/zoo.cfg  增加最后的2行代码：
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper-default/data/
clientPort=2181
maxClientCnxns=2000
maxSessionTimeout=240000
server.1=192.168.2.187:2888:3888
server.2=192.168.2.188:2888:3888
server.3=192.168.2.189:2888:3888
server.4=192.168.2.190:2888:3888
server.5=192.168.2.191:2888:3888
## 清空目录防止有脏数据
rm -fr /usr/local/zookeeper-default/data/*
## 添加对应的myid文件到zk数据目录下
echo 5 > /usr/local/zookeeper-default/data/myid
```

4. 启动 node5 的 zk 进程:

```shell
/usr/local/zookeeper-default/bin/zkServer.sh start
/usr/local/zookeeper-default/bin/zkServer.sh  status

echo stat | nc  127.0.0.1 2181  结果类似如下:
Zookeeper version: 3.4.9-1757313, built on 08/23/2016 06:50 GMT
Clients:
 /127.0.0.1:45582[0](queued=0,recved=1,sent=0)
Latency min/avg/max: 0/0/0
Received: 3
Sent: 2
Connections: 1
Outstanding: 0
Zxid: 0x10000009a
Mode: follower
Node count: 63
也可以使用 echo mntr   | nc  127.0.0.1 2181  这个结果更详细，类似如下：
zk_version3.4.9-1757313, built on 08/23/2016 06:50 GMT
zk_avg_latency0
zk_max_latency194
zk_min_latency0
zk_packets_received101436
zk_packets_sent102624
zk_num_alive_connections4
zk_outstanding_requests0
zk_server_statefollower
zk_znode_count141
zk_watch_count190
zk_ephemerals_count7
zk_approximate_data_size10382
zk_open_file_descriptor_count35
zk_max_file_descriptor_count102400
```

5. 当我们确认 新加的 2 个 zk 节点没问题后，我们需要去修改之前的老的 3 台 zk 的配置，然后重启这 3 个 zk

修改 node1 node2 node3 的 zk 配置，如下：

```shell
vim  /usr/local/zookeeper-default/conf/zoo.cfg  增加最后的2行代码：
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/usr/local/zookeeper-default/data/
clientPort=2181
maxClientCnxns=2000
maxSessionTimeout=240000
server.1=192.168.2.187:2888:3888
server.2=192.168.2.188:2888:3888
server.3=192.168.2.189:2888:3888
server.4=192.168.2.190:2888:3888
server.5=192.168.2.191:2888:3888
```

注意重启的时候，我们先重启 follower 节点（例如我这里 follower 是 node2、node3，leader 是 node1）

```shell
/usr/local/zookeeper-default/bin/zkServer.sh stop
/usr/local/zookeeper-default/bin/zkServer.sh status

/usr/local/zookeeper-default/bin/zkServer.sh start
/usr/local/zookeeper-default/bin/zkServer.sh status
```

# 第二部分：kafka 节点的扩容：

1. node4 (192.168.2.190)上修改:

```shell
mkdir -pv /usr/local/kafka-default/kafka-logs
vim /usr/local/kafka-default/config/server.properties  修改后的文件如下:
broker.id=4   # 注意修改这里
listeners=PLAINTEXT://:9094,TRACE://:9194
advertised.listeners=PLAINTEXT://192.168.2.190:9094
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
log.dirs=/usr/local/kafka-default/kafka-logs
num.partitions=3
num.recovery.threads.per.data.dir=1
log.retention.hours=24
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=192.168.2.187:2181,192.168.2.188:2181,192.168.2.189:2181,192.168.2.190:2181,192.168.2.191:2181  # 注意修改这里
zookeeper.connection.timeout.ms=6000
default.replication.factor=2
compression.type=gzip
offsets.retention.minutes=2880
controlled.shutdown.enable=true
delete.topic.enable=true
```

2. 启动 node4 的 kafka 程序：

```shell
/usr/local/kafka-default/bin/kafka-server-start.sh -daemon /usr/local/kafka-default/config/server.properties
```

3. node5(192.168.2.191)上修改

```shell
mkdir -pv /usr/local/kafka-default/kafka-logs
vim /usr/local/kafka-default/config/server.properties  修改后的文件如下:
broker.id=5   # 注意修改这里
listeners=PLAINTEXT://:9094,TRACE://:9194
advertised.listeners=PLAINTEXT://192.168.2.191:9094
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
log.dirs=/usr/local/kafka-default/kafka-logs
num.partitions=3
num.recovery.threads.per.data.dir=1
log.retention.hours=24
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=192.168.2.187:2181,192.168.2.188:2181,192.168.2.189:2181,192.168.2.190:2181,192.168.2.191:2181   # 注意修改这里
zookeeper.connection.timeout.ms=6000
default.replication.factor=2
compression.type=gzip
offsets.retention.minutes=2880
controlled.shutdown.enable=true
delete.topic.enable=true
```

4. 启动 node5 的 kafka 程序：

```shell
/usr/local/kafka-default/bin/kafka-server-start.sh -daemon /usr/local/kafka-default/config/server.properties
```

5. 测试是否有问题

这里我们可以自己先用 `kafka-console-producer.sh` 和 `kafka-console-consumer.sh` 自测下是否正常工作，然后看看 kafka-manager 上是否有需要重新均衡的副本。。

# 第三部分：对存在风险 broker 节点的数据迁移

（我这里需要这么操作，单纯的扩容不需要这个步骤）

这里我们可以使用 kafka-manager 这个 web 平台来做 topic 的迁移操作，很简单，这里就不截图了。
