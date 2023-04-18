#### **kafka 消费不到消息的原因？**

可能情况

1、服务是不是正常的；topic 的 leader partition 是不是正常，磁盘有没有满；consumer 没连上

2、auto.offset.reset 配置

​ earliest 和 latest 区别，如果当前分区没有已提交 offset 的情况，earliest 从头消费；latest 会从最新的消息消费，如果没有最新的，那就没有消息

3、当前 group.id 已经消费到最新的 offset 了，也没有消息

常用配置

```
// 消费者组
group.id

// 是否开启自动提交 ; 我们生产一般配置的手动提交
enable.auto.commit
// 关乎kafka数据的读取，是一个非常重要的设置。常用的二个值是latest和earliest，默认是latest
// earliest 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，从头开始消费
// latest 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，消费新产生的该分区下的数据
auto.offset.reset
```
