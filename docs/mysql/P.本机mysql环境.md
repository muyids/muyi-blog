#### 大纲

- 文件目录

- 服务启动停止

- 密码修改

#### **文件目录**

安装目录

/usr/local/Cellar/mysql/8.0.22

配置文件位置

/usr/local/etc/my.cnf

数据文件位置

/usr/local/var/mysql

#### **服务启动停止**

brew services stop mysql

#### **密码修改**

```sql
brew services stop mysql
mysqld_safe --skip-grant-tables

---重启窗口--

mysql -uroot -p

use mysql;

flush privileges;

ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';

flush privileges;
```
