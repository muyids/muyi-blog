**本地事务 @Transactional 的问题**

分析下面的代码

```java
@Transactional
@GetMapping("/add/saveToDB")
public String saveToDB(Long id) {
  System.out.println("下单,商品id:" + id);

  // 本地数据库插入操作
  OrderDO orderDO = this.orderService.insert();
  // 远程方法调用
  String res = stockService.reduceToDB(id);
  // 抛出异常 -> 事务回滚
  int k = 1 / 0;
  System.out.println("下单,商品id:" + id + ";订单id:" + orderDO.getId());
  return LocalDateTime.now().format(DateTimeFormatter.ISO_DATE) + ":" + res;
}
```

运行结果：

1、本地数据库插入操作回滚

2、远程方法调用执行成功

我们需要使用 Seata 进行分布式事务配置

**Seata Client 快速开始**

(1)启动 Seata Server 端，使用 DB+nacos 作为配置中心和注册中心（上一步已完成）

(2)配置微服务整合 seata

<1>添加 pom 依赖

<2>各业务系统添加 undo_log 表

```sql
-- 注意此处0.7.0+ 增加字段 context
CREATE TABLE `undo_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(100) NOT NULL,
  `context` varchar(128) NOT NULL,
  `rollback_info` longblob NOT NULL,
  `log_status` int(11) NOT NULL,
  `log_created` datetime NOT NULL,
  `log_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_undo_log` (`xid`,`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

<3>配置 yml

```yaml
spring:
  cloud:
    alibaba:
      seata:
      	# 配置事务分组(查看nacos配置Data ID过滤service.vgroupMapping.*)
        tx-service-group: my_test_tx_group
seata:
  registry:
    type: nacos
    nacos:
      server-addr: 127.0.0.1:8848
      application: seata-server
      username: nacos
      password: nacos
      group: SEATA_GROUP
  config:
    type: nacos
    nacos:
      server-addr: 127.0.0.1:8848
      username: nacos
      password: nacos
```

<4>添加@GlobalTransactional 注解

```java
//    @Transactional
    @GlobalTransactional
    @GetMapping("/add/saveToDB")
    public String saveToDB(Long id) {
        System.out.println("下单,商品id:" + id);
        // 本地数据库插入操作
        OrderDO orderDO = this.orderService.insert();
        // 远程方法调用
        String res = stockService.reduceToDB(id);
        // 抛出异常
        int k = 1 / 0;
        System.out.println("下单,商品id:" + id + ";订单id:" + orderDO.getId());
        return LocalDateTime.now().format(DateTimeFormatter.ISO_DATE) + ":" + res;
    }
```
