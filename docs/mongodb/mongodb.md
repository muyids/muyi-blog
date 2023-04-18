---
title: mongodb基本操作
date: 2015-08-20T00:00:00+08:00
categories: [数据库, mongodb]
tags: [数据库, mongodb]
---

## 常用命令

### 启动和关闭

- 启动

```
$ mongod -f /etc/mongod.conf
```

使用配置文件启动，启动参数详情看配置文件

- 停止服务

```shell script
> use admin
switched to db admin
> db.shutdownServer()
server should be down...
```

- 关闭客户端

```
$ exit
```

### 连接

```
$ mongo --help
$ mongo --host xxx:3717 --authenticationDatabase admin -u root -p
```

### db

- 查看

  show dbs

- 选择
  use test_db
- 查看当前数据库中的所有集合

  show collections

- 查看当前数据库

  show db

- 删除数据库
  use mydb;
  db.dropDatabase();
- 重命名 db
  - 无 rename 操作
    进行如下操作，修改 dbname
  1.  db.copyDatabase("db_to_rename", "db_renamed", "localhost")
  2.  use db_to_rename
  3.  db.dropDatabase();

### 创建用户

```
	db.createUser(
	    {
	      user: "dongwei",
	      pwd: "test123",
	      customData: { sex : "boy"},
	      roles: [
	         { role: "readWrite", db: "nut_log" }
	      ]
	    }
	)
```

### 集合

- db、collection 名字规则

  - 必须以下划线和字母开头
  - 不能包含‘$’
  - 不能是空串
  - 不能包含空字符
  - 不能以“system.”开头
  - 貌似也不能包含‘-’

- 新建

  > db.createCollection("log_event")

- 删除集合
  > db.blog.drop()
- 重命名
  > db.blog.renameCollection("Blog")
- 删除所有数据
  > db.blog.remove()

### insert

```
db.blog.insert({文档})
```

### remove

```
db.blog.remove({条件})
```

### update

```shell script
db.collection.update(criteria, objNew, upsert, multi )
```

- criteria : update 的查询条件，类似 sql update 查询内 where 后面的
- objNew : update 的对象和一些更新的操作符（如$,$inc...）等，也可以理解为 sql update 查询内 set 后面的
- upsert : 这个参数的意思是，如果不存在 update 的记录，是否插入 objNew，true 为插入，默认是 false，不插入。
- multi : mongodb 默认是 false,只更新找到的第一条记录，如果这个参数为 true,就把按条件查出来多条记录全部更新。
  **例子**

- 为 user 集合中的每一条记录添加一个名为 ex 的字段，并赋值为 vip

```
db.user.update({},{$set:{"ex":"vip"}},false,true)
```

- 删除 user 集合中的 age 字段

```
db.user.update({},{$unset:{"age": ""}},{multi:true})
```

### find

- find()指定返回的键
- 查询条件 $lt $gt $lte $gte
- 别的查询键 $or $in $nin $not 等
- 查询数组相关：$all $size $slice
- 正则表达式：支持 Perl 兼容的正则表达式(PCRE)
- 对查询结果的处理 $limit $skip $sort (其中$skip 适合跳过少量文档，否则性能影响)
- 查询某个字段是否存在 { 字段 : { $exists: true } }
- 以上不能满足，还有$where，更复杂的查询是 mapreduce(下文介绍)
  聚合(mongodb 本身的聚合操作可能可以好好依赖一下，比如 olap 里复杂的查询和本地聚合操作可以大量借用 mapreduce？)
- count() distinct()
- group() 类似 group by,且可以附带一个 finalize 函数对结果修剪
- mapreduce 可以做复杂的聚合查询，并行化到多个服务器，当然 mapreduce 和 group 都不适合实时场景

```
db.stu.find({ score:{ $gt:90 } },{ name:1}).sort({age: 1}).limit(10)
```

### skip()语句

```
db.collection.find().skip(N)
```

**当 N 比较大的时候，比如大于一千万，效率很低，使用{\_id: {$gt: ObjectId}}替代**

### 数组

#### 增加数据

```
db.transfer.update({"_id" : ObjectId("5be95c974f0c47045d7862e9")}, {"$push":{"trade_err": "hello"}}
```

### 删除字段

```
db.transfer.update({},{$unset:{'trade_err':''}}, false, true)
```
