摘自

作者：小知
链接：https://zhuanlan.zhihu.com/p/388735310
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

docker 配置 mysql 主从复制

1）创建主服务器所需目录

```apacheconf
mkdir -p /Users/dw/mysqlData/master/cnf
mkdir -p /Users/dw/mysqlData/master/data
```

2）定义主服务器配置文件

```
vim /Users/dw/mysqlData/master/cnf/mysql.cnf
[mysqld]
## 设置server_id,注意要唯一
server-id=1
## 开启binlog
log-bin=mysql-bin
## binlog缓存
binlog_cache_size=1M
## binlog格式(mixed、statement、row,默认格式是statement)
binlog_format=mixed
```

3）创建并启动 mysql 主服务

```

docker run -itd -p 8306:3306 --name master -v /Users/dw/mysqlData/master/cnf:/etc/mysql/conf.d -v /Users/dw/mysqlData/master/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7

```

4）添加复制 master 数据的用户 reader，供从服务器使用

```
[root@aliyun /]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                               NAMES
6af1df686fff        mysql:5.7           "docker-entrypoint..."   5 seconds ago       Up 4 seconds        0.0.0.0:3306->3306/tcp, 33060/tcp   master
[root@aliyun /]# docker exec -it master /bin/bash
root@41d795785db1:/# mysql -u root -p123456
mysql> GRANT REPLICATION SLAVE ON *.* to 'reader'@'%' identified by 'reader';
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)
```

5）创建从服务器所需目录，编辑配置文件

```text
mkdir -p /Users/dw/mysqlData/slave/cnf
mkdir -p /Users/dw/mysqlData/slave/data

vim /Users/dw/mysqlData/slave/cnf/mysql.cnf

[mysqld]
## 设置server_id,注意要唯一
server-id=2
## 开启binlog,以备Slave作为其它Slave的Master时使用
log-bin=mysql-slave-bin
## relay_log配置中继日志
relay_log=edu-mysql-relay-bin
## 如果需要同步函数或者存储过程
log_bin_trust_function_creators=true
## binlog缓存
binlog_cache_size=1M
## binlog格式(mixed、statement、row,默认格式是statement)
binlog_format=mixed
## 跳过主从复制中遇到的所有错误或指定类型的错误,避免slave端复制中断
## 如:1062错误是指一些主键重复,1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
```

6）创建并运行 mysql 从服务器

```
docker run -itd -p 8307:3306 --name slaver -v /Users/dw/mysqlData/slave/cnf:/etc/mysql/conf.d -v /Users/dw/mysqlData/slave/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7
```

7）在从服务器上配置连接主服务器的信息

首先主服务器上查看`master_log_file`、`master_log_pos`两个参数，然后切换到从服务器上进行主服务器的连接信息的设置

主服务上执行：

```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000005 |      591 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

docker 查看主服务器容器的 ip 地址

```text
[root@aliyun /]# docker inspect --format='{{.NetworkSettings.IPAddress}}' master
172.17.0.2
```

从服务器上执行：

```text
[root@aliyun /]# docker exec -it slaver /bin/bash
root@fe8b6fc2f1ca:/# mysql -u root -p123456

mysql> change master to master_host='172.17.0.2',master_user='reader',master_password='reader',master_log_file='mysql-bin.000003',master_log_pos=591;
```

8）从服务器启动 I/O 线程和 SQL 线程

```
mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> mysql> show slave status \G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 172.17.0.2
                  Master_User: reader
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000003
          Read_Master_Log_Pos: 591
               Relay_Log_File: edu-mysql-relay-bin.000002
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000003
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
```
