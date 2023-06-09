## 高效的分布式锁

考虑几点：

1. 互斥：同一时刻只有一个线程获取到锁
2. 防止死锁：线程获取锁后，系统故障无法释放锁，需要设置锁的过期时间自动释放
3. 性能：减少锁的等待时间
   1. 锁的颗粒度尽量小
   2. 锁的范围尽量小
4. 可重入：同 ReentrantLock：同一个线程可以重复拿到同一个资源的锁

#### Redis 分布式锁的缺点

在哨兵模式或者主从模式下，如果 master 实例宕机的时候，可能导致多个客户端同时完成加锁。

## SETNX + EXPIRE

`SETNX + EXPIRE` 两条指令结合使用：

- 先拿 setnx 来争抢锁
- 抢到之后，再用 expire 给锁加一个过期时间防止锁忘记了释放
  存在问题：

- 两条指令结合使用，不满足事务性；
- 如果 expire 未成功执行，锁只能主动释放，如果业务代码不成功，锁存在永远得不到释放的情况。

## SET NX EX

命令 `SET resource-name anystring NX EX max-lock-time` 是一种在 Redis 中实现锁的简单方法。

相当于把 `setnx` 和 `expire` 合成一条指令来用，支持事务性

## lua 脚本

使用 lua 脚本的好处:

- 减少网络开销：本来 5 次网络请求的操作，可以用一个请求完成
- 原子操作：Redis 会将整个脚本作为一个整体执行，中间不会被其他命令插入
