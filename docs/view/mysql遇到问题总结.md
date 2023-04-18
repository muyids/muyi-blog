#### 一、sql 优化手段

1、使用 mysql 命令查看当前 mysql 服务器状态

​ show status; -- 服务器状态

​ show processlist; -- 当前执行中的进程情况

2、

#### 一、mysql 死锁

死锁是怎么发生的？

排查、如何解决？

事后补救？

**场景**：

线程 A 持有锁 a，等待资源 b; 线程 B 持有锁 b，等待资源 a；

互相等待，不释放；

**解决方案：**

查看死锁日志：show engine innodb status;

找出死锁 sql；

分析加锁情况；

模拟死锁案发现场；

分析单条 sql 执行占用资源情况: SHOW PROCESSLIST;

#### 一、innodb 1000 万数据量、1 亿数据量索引会建几层，怎么算的？
