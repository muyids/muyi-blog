**Seata Server(TC)环境搭建**

参考部署指南：[http://seata.io/zh-cn/docs/ops/deploy-guide-beginner.html](http://seata.io/zh-cn/docs/ops/deploy-guide-beginner.html)

**Server 端存储模式（store.mode）**

支持三种：

- file：单机模式，全局事务会话信息**内存中读取**并持久化本地文件 root.data，性能较高（默认）
- **DB：高可用模式**，全局事务会话信息通过**db 共享**，性能差一些
- redis：性能较高，存在事务信息丢失风险，server1.3 版本以上

**存储模式 DB 的配置**

1. 修改`config/file.conf`配置文件

   ```yaml
   mode = "db"
     ## database store property
     db {
       ## the implement of javax.sql.DataSource, such as DruidDataSource(druid)/BasicDataSource(dbcp)/HikariDataSource(hikari) etc.
       datasource = "druid"
       ## mysql/oracle/postgresql/h2/oceanbase etc.
       dbType = "mysql"
       driverClassName = "com.mysql.jdbc.Driver"
       ## if using mysql to store the data, recommend add rewriteBatchedStatements=true in jdbc connection param
       url = "jdbc:mysql://127.0.0.1:3306/seata?rewriteBatchedStatements=true"
       user = "root"
       password = "123456"
       minConn = 5
       maxConn = 100
       globalTable = "global_table"
       branchTable = "branch_table"
       lockTable = "lock_table"
       queryLimit = 100
       maxWait = 5000
     }
   ```

2. 创建数据库

   ```sql
   create database seata;
   ```

3. 建表

   参考资源目录，下载建表 SQL 并执行 https://github.com/seata/seata/edit/1.4.0/script/server/db/mysql.sql

**DB 存储模式+Nacos(注册&配置中心)部署**

![2021-10-16 pm4.32.54](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-16%20pm4.32.54.png)

参考高可用配置：[http://seata.io/zh-cn/docs/ops/deploy-ha.html](http://seata.io/zh-cn/docs/ops/deploy-ha.html)

1. 修改`config/registry.conf`配置文件

   ```yaml
   registry {
   type = "nacos"
   }
   config {
   type = "nacos"
   }
   ```

2. nacos 导入 config 配置

   - 下载 seata 开源项目，修改`seata/script/config-center/config.txt`文件

   - 运行`cd seata/script/config-center/nacos/ && sh nacos-config.sh`

**启动 seata server**

打开 seata-server 的安装路径`/usr/local/seata/seata-server-1.4.2`

运行：`sh bin/seata-server.sh`

报错： seata errorCode 0, state 08001 -> 因为 mysql 驱动版本配置的是低版本，不兼容 8.0 以上 mysql 导致， 修改配置文件中的 mysql 驱动版本

```yaml
store.db.driverClassName=com.mysql.cj.jdbc.Driver
store.db.url=jdbc:mysql://127.0.0.1:3306/seata?useUnicode=true&rewriteBatchedStatements=true
```
