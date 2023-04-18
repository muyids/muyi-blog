---
title: influxdb的使用
date: 2018-09-07T04:53:00+08:00
draft: false
categories: [数据库]
tags: [数据库]
---

`influxdb`是目前比较流行的时间序列数据库。

<!--more-->

_何谓时间序列数据库？_

什么是时间序列数据库，最简单的定义就是数据格式里包含 Timestamp 字段的数据，比如某一时间环境的温度，CPU 的使用率等。
但是，有什么数据不包含 Timestamp 呢？几乎所有的数据其实都可以打上一个 Timestamp 字段。时间序列数据的更重要的一个属性是如何去查询它，包括数据的过滤，计算等等。

## Influxdb

Influxdb 是一个开源的分布式时序、时间和指标数据库，使用 go 语言编写，无需外部依赖。

它有三大特性：

- 时序性（Time Series）：与时间相关的函数的灵活使用（诸如最大、最小、求和等）；
- 度量（Metrics）：对实时大量数据进行计算；
- 事件（Event）：支持任意的事件数据，换句话说，任意事件的数据我们都可以做操作。

同时，它有以下几大特点：

- schemaless(无结构)，可以是任意数量的列；
- min, max, sum, count, mean, median 一系列函数，方便统计；
- Native HTTP API, 内置 http 支持，使用 http 读写；
- Powerful Query Language 类似 sql；
- Built-in Explorer 自带管理工具。

## Influxdb 安装

在讲解具体的安装步骤之前，先说说 influxdb 的两个 http 端口：8083 和 8086

- port 8083：管理页面端口，访问 localhost:8083 可以进入你本机的 influxdb 管理页面；
- port 8086：http 连接 influxdb client 端口，一般使用该端口往本机的 influxdb 读写数据。

### OS X

brew update
brew install influxdb

### docker

```
docker run -d --restart=always \
	 -p 8083:8083 -e INFLUXDB_ADMIN_ENABLED=true \
	 -p 8086:8086 \
      -v /var/lib/influxdb:/var/lib/influxdb \
      influxdb
```

### RedHat & CentOS

wget https://dl.influxdata.com/influxdb/releases/influxdb-1.0.2.x86_64.rpm
sudo yum localinstall influxdb-1.0.2.x86_64.rpm
安装完之后，如何启动呢？

- sudo service influxdb start
- /etc/init.d/influxdb restart
  如何在命令行使用

安装完毕之后，如何在命令行使用呢？

```shell
influx
```

influx -precision rfc3339

## influxdb 基本操作

名词解释

在具体的讲解 influxdb 的相关操作之前先说说 influxdb 的一些专有名词，这些名词代表什么。

influxdb 相关名词

- database：数据库；
- measurement：数据库中的表；
- points：表里面的一行数据。

influxDB 中独有的一些概念

Point 由时间戳（time）、数据（field）和标签（tags）组成。

- time：每条数据记录的时间，也是数据库自动生成的主索引；
- fields：各种记录的值；
- tags：各种有索引的属性。

还有一个重要的名词：series

所有在数据库中的数据，都需要通过图表来表示，series 表示这个表里面的所有的数据可以在图标上画成几条线（注：线条的个数由 tags 排列组合计算出来）

### influxdb 基本操作

数据库与表的操作
可以直接在 web 管理页面做操作，当然也可以命令行。

#### 创建数据库

create database "db_name"

#### 显示所有的数据库

show databases

#### 删除数据库

drop database "db_name"

#### 使用数据库

use db_name

#### 显示该数据库中所有的表

show measurements

#### 创建表，直接在插入数据的时候指定表名

insert test,host=127.0.0.1,monitor_name=test count=1

#### 删除表

drop measurement "measurement_name"

#### 增

向数据库中插入数据。
通过命令行

- use testDb
- insert test,host=127.0.0.1,monitor_name=test count=1
  通过 http 接口

      curl -i -XPOST 'http://127.0.0.1:8086/write?db=testDb' --data-binary 'test,host=127.0.0.1,monitor_name=test count=1'

读者看到这里可能会观察到插入的数据的格式貌似比较奇怪，这是因为 influxDB 存储数据采用的是 Line Protocol 格式。那么何谓 Line Protoco 格式？

Line Protocol 格式：写入数据库的 Point 的固定格式。

在上面的两种插入数据的方法中都有这样的一部分：

test,host=127.0.0.1,monitor_name=test count=1

其中：

- test：表名；
- host=127.0.0.1,monitor_name=test：tag；
- count=1：field

想对此格式有详细的了解参见[官方文档](https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/)

#### 查

查询数据库中的数据。

通过命令行
select _ from test order by time desc
通过 http 接口
curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=testDb" --data-urlencode "q=select _ from test order by time desc"
influxDB 是支持类 sql 语句的，具体的查询语法都差不多，这里就不再做详细的赘述了。

#### 数据保存策略（Retention Policies）

influxDB 是没有提供直接删除数据记录的方法，但是提供数据保存策略，主要用于指定数据保留时间，超过指定时间，就删除这部分数据。

- 查看当前数据库 Retention Policies

  show retention policies on "db_name"

- 创建新的 Retention Policies
  create retention policy "rp_name" on "db_name" duration 3w replication 1 default

  - rp_name：策略名；
  - db_name：具体的数据库名；
  - 3w：保存 3 周，3 周之前的数据将被删除，influxdb 具有各种事件参数，比如：h（小时），d（天），w（星期）；
  - replication 1：副本个数，一般为 1 就可以了；
  - default：设置为默认策略

- 修改 Retention Policies
  alter retention policy "rp_name" on "db_name" duration 30d default
- 删除 Retention Policies
  drop retention policy "rp_name"

#### 用户管理

可以直接在 web 管理页面做操作，也可以命令行。

- 显示用户
  show users
- 创建用户
  create user "username" with password 'password'
- 创建管理员权限用户
  create user "username" with password 'password' with all privileges
- 删除用户
  drop user "username"
