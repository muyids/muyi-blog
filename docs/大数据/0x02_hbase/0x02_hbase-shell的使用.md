# hbase shell 的使用

## COMMAND GROUPS

通过 help 命令查看

### Group name: general

​

Commands: processlist, status, table_help, version, whoami

​

### Group name: ddl

Commands: alter, alter_async, alter_status, clone_table_schema, create, describe, disable, disable_all, drop, drop_all, enable, enable_all, ex

ists, get_table, is_disabled, is_enabled, list, list_regions, locate_region, show_filters

​

### Group name: namespace

Commands: alter_namespace, create_namespace, describe_namespace, drop_namespace, list_namespace, list_namespace_tables

​

### Group name: dml

Commands: append, count, delete, deleteall, get, get_counter, get_splits, incr, put, scan, truncate, truncate_preserve

​

### Group name: tools

Commands: assign, balance_switch, balancer, balancer_enabled, catalogjanitor_enabled, catalogjanitor_run, catalogjanitor_switch, cleaner_chore

\_enabled, cleaner_chore_run, cleaner_chore_switch, clear_block_cache, clear_compaction_queues, clear_deadservers, clear_slowlog_responses, close

\_region, compact, compact_rs, compaction_state, compaction_switch, decommission_regionservers, flush, flush_master_store, get_balancer_decisions

, get_balancer_rejections, get_largelog_responses, get_slowlog_responses, hbck_chore_run, is_in_maintenance_mode, list_deadservers, list_decommi

ssioned_regionservers, list_liveservers, list_unknownservers, major_compact, merge_region, move, normalize, normalizer_enabled, normalizer_switc

h, recommission_regionserver, regioninfo, rit, snapshot_cleanup_enabled, snapshot_cleanup_switch, split, splitormerge_enabled, splitormerge_swit

ch, stop_master, stop_regionserver, trace, unassign, wal_roll, zk_dump

​

### Group name: replication

Commands: add_peer, append_peer_exclude_namespaces, append_peer_exclude_tableCFs, append_peer_namespaces, append_peer_tableCFs, disable_peer,

disable_table_replication, enable_peer, enable_table_replication, get_peer_config, list_peer_configs, list_peers, list_replicated_tables, remove

_peer, remove_peer_exclude_namespaces, remove_peer_exclude_tableCFs, remove_peer_namespaces, remove_peer_tableCFs, set_peer_bandwidth, set_peer_

exclude_namespaces, set_peer_exclude_tableCFs, set_peer_namespaces, set_peer_replicate_all, set_peer_serial, set_peer_tableCFs, show_peer_tableC

Fs, update_peer_config

​

### Group name: snapshots

Commands: clone_snapshot, delete_all_snapshot, delete_snapshot, delete_table_snapshots, list_snapshots, list_table_snapshots, restore_snapshot

, snapshot

​

### Group name: configuration

Commands: update_all_config, update_config, update_rsgroup_config

​

### Group name: quotas

Commands: disable_exceed_throttle_quota, disable_rpc_throttle, enable_exceed_throttle_quota, enable_rpc_throttle, list_quota_snapshots, list_q

uota_table_sizes, list_quotas, list_snapshot_sizes, set_quota

​

### Group name: security

Commands: grant, list_security_capabilities, revoke, user_permission

​

### Group name: procedures

Commands: list_locks, list_procedures

​

### Group name: visibility labels

Commands: add_labels, clear_auths, get_auths, list_labels, set_auths, set_visibility

​

### Group name: rsgroup

Commands: add*rsgroup, alter_rsgroup_config, balance_rsgroup, get_namespace_rsgroup, get_rsgroup, get_server_rsgroup, get_table_rsgroup, list*

rsgroups, move_namespaces_rsgroup, move_servers_namespaces_rsgroup, move_servers_rsgroup, move_servers_tables_rsgroup, move_tables_rsgroup, remo

ve_rsgroup, remove_servers_rsgroup, rename_rsgroup, show_rsgroup_config

​

### Group name: storefiletracker

Commands: change_sft, change_sft_all

​

## SHELL USAGE:

​

Quote all names in HBase Shell such as table and column names. Commas delimit

command parameters. Type after entering a command to run it.

Dictionaries of configuration used in the creation and alteration of tables are

Ruby Hashes. They look like this:

​

{'key1' => 'value1', 'key2' => 'value2', ..

## 表相关操作

### 查看当前 hbase 中有那些表

```shell
> list
```

### 创建表

创建表

> 格式:
> create ‘表名’,‘列族 1’,‘列族 2’ …
> 或者
> create ‘表名’,{NAME=>‘列族 1’},{NAME=>‘列族 2’} …
> 注意：

- 必须指定列族

- 如果不指定列族，直接使用 `create ${table}` 会报错

> ERROR: Table must have at least one column family

举例：

```
create 'test','f1','f2'
create 'test1',{NAME=>'f1'},{NAME=>'f2'}

```

### 删除表

删除表结构和表中数据

> 格式:
> drop ‘表名’
> 注意：在删除 hbase 表之前, 必须要先禁用表

- 禁用表: disable ‘表名’
- 启动表: enable ‘表名’
- 判断表是否启用: is_enabled ‘表名’
- 判断表是否禁用: is_disabled ‘表名’
  举例：

```shell
hbase:003:0> is_enabled 'test'
true
Took 0.0059 seconds
=> true
hbase:004:0> disable 'test'
Took 0.3629 seconds
hbase:005:0> drop 'test'
Took 0.3456 seconds
hbase:006:0> desc 'test'
ERROR: Table test does not exist.

For usage try 'help "describe"'

Took 0.0059 seconds
```

### 修改表结构

用来增加或删除列族

格式：

> 增加列族:
> alter ‘表名’ ,NAME=>‘新的列族’
> 删除列族:
> alter ‘表名’,‘delete’=>‘旧的列族’
> 举例：

举例：

```shell
alter 'test1',NAME='f3'
alter 'test1',delete='f2'
```

### 表信息查看

#### 查看表是否存在

```
exists
```

#### 查看表的结构

> 格式：
>
> describe ‘表名’

举例：

```shell
hbase:016:0> describe 'test1'
Table test1 is ENABLED
test1, {TABLE_ATTRIBUTES => {METADATA => {'hbase.store.file-tracker.impl' => 'DEFAULT'}}}
COLUMN FAMILIES DESCRIPTION
{NAME => 'f1', INDEX_BLOCK_ENCODING => 'NONE', VERSIONS => '1', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', MIN_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', IN_MEMORY => 'false', COMPRESSION => 'NONE', BLOCKCACHE => 'true', BLOCKSIZE => '65536 B (64KB)'}
```

- KEEP_DELETED_CELLS : 保持删除的单元格，默认为 false
- INDEX_BLOCK_ENCODING ：索引压缩算法
- REPLICATION_SCOPE

#### 查看表中有多少数据

> 格式：
>
> count ‘表名’

举例：

```shell
hbase:008:0> count 'test1'
1 row(s)
Took 0.0318 seconds
=> 1
```

## 记录相关操作

### 向表中插入数据

> 格式:
> put ‘表名’,‘rowkey 名称’,‘列族名:列名’,‘值’
> 举例：

```shell
put 'test1','rk00001','f1:name','dw'
put 'test1','rk00001','f1:age','31'
put 'test1','rk00001','f2:address','beijing'
```

### 删除数据

> 格式:
> delete ‘表名’,‘rowkey 名称’,‘列族:列名’

### 修改数据

修改数据的操作 与 添加数据的操作是一致的, 只需要保证 rowkey 一样 就是修改数据

> 格式:
> put ‘表名’,‘rowkey 名称’,‘列族名:列名’,‘值’
> 举例：

```shell
put 'test1','rk00001','f1:name','dw'
put 'test1','rk00001','f1:age','31'
put 'test1','rk00001','f2:address','beijing'
```

### 数据查询

插入准备数据

```shell
put 'test1','rk0001','f1:name','zhangsan'
put 'test1','rk0001','f1:age','20'
put 'test1','rk0001','f1:birthday','2020-10-10'
put 'test1','rk0001','f2:sex','nan'
put 'test1','rk0001','f2:address','beijing'
put 'test1','rk0002','f1:name','lisi'
put 'test1','rk0002','f1:age','25'
put 'test1','rk0002','f1:birthday','2005-10-10'
put 'test1','rk0002','f2:sex','nv'
put 'test1','rk0002','f2:address','shanghai'

put 'test1','rk0003','f1:name','王五'
put 'test1','rk0003','f1:age','28'
put 'test1','rk0003','f1:birthday','1993-10-25'
put 'test1','rk0003','f2:sex','nan'
put 'test1','rk0003','f2:address','tianjin'

put 'test1','0001','f1:name','zhaoliu'
put 'test1','0001','f1:age','25'
put 'test1','0001','f1:birthday','1995-05-05'
put 'test1','0001','f2:sex','nan'
put 'test1','0001','f2:address','guangzhou'
```

#### 基于 rowkey 查询

适用于从表中获取一条数据的场景

> 格式:
> get ‘表名’,‘rowkey 名称’, [‘列族’ | ‘列族:列名’ …]
> 说明:
> [] 表示是可选
> 举例：

```shell
get 'test1','rk00001'
get 'test1','rk00001','f1'
get 'test1','rk00001','f1:name',
get 'test1','rk00001','f1:name','f2'
```

#### 全表扫描 和 范围查询

> 格式:
> scan '表名' , {COLUMNS=>['列族' | '列族:列名' ....],
> STARTROW=>'起始 rowkey 值' ,ENDROW=>'结束 rowkey 值',
> FORMATTER=>'toString',LIMIT=>N}
> 注意：

- 此处 [] 是格式要求, 必须存在
- 范围检索是左闭右开，包头不包尾
  举例：

```shell
# 全表扫描
scan 'test1'
scan 'test1',{FORMATTER=>'toString'}
scan 'test1',{FORMATTER=>'toString',LIMIT=>2}
scan 'test1',{COLUMN=>'f1'}
scan 'test1',{COLUMN=>'f1',FORMATTER=>'toString',LIMIT=>2}
scan 'test1',{COLUMN=>['f1','f2:address'],FORMATTER=>'toString',LIMIT=>2}
# 范围查询
scan 'test1',{STARTROW=>'rk0001',ENDROW=>'rk0002'}
```

#### filter 过滤器

作用：补充 hbase 的查询方式，指定查询条件，对查询结果进行筛选

```
格式:
	scan '表名',{FILTER=>"过滤器(比较运算符,'比较器表达式')"}

在hbase中常用的过滤器:
	rowkey过滤器:
		RowFilter:  实现根据某一个rowkey过滤数据
		PrefixFilter: rowkey前缀过滤器
	列族过滤器:
		FamilyFilter: 列族过滤器
	列名过滤器:
		QualifierFilter : 列名过滤器, 显示对应列的数据
	列值过滤器:
		ValueFilter: 列值过滤器, 找到符合条件的列值
		SingleColumnValueFilter: 在指定列族和列名下, 查询符合对应列值数据的整行数据
		SingleColumnValueExcludeFilter : 在指定列族和列名下, 查询符合对应列值数据的整行数据，结果不包含过滤字段
	其他过滤器:
		PageFilter : 用于分页过滤器
比较运算符:  >  <  >= <= != =

比较器:
	BinaryComparator: 用于进行完整的匹配操作
	BinaryPrefixComparator : 匹配指定的前缀数据
	NullComparator : 空值匹配操作
	SubstringComparator: 模糊匹配

比较器表达式:
	BinaryComparator         binary:值
	BinaryPrefixComparator   binaryprefix:值
	NullComparator           null
	SubstringComparator      substring:值

参考地址:
	http://hbase.apache.org/2.2/devapidocs/index.html
	从这个地址下, 找到对应过滤器, 查看其构造, 根据构造编写filter过滤器即可

案例:
	需求一: 找到在列名中包含 字母 e 列名有哪些
	scan 'test01',{FILTER=>"QualifierFilter(=,'substring:e')"}
	需求二: 查看rowkey以rk开头的数据
	scan 'test01',{FILTER=>"PrefixFilter('rk')"}
	scan 'test01',{FILTER=>"RowFilter(=,'binaryprefix:rk')"}
	需求三: 查询 年龄大于等于25岁的数据
	scan 'test01',{FILTER=>"SingleColumnValueFilter('f1','age',>=,'binary:25')"}
	scan 'test01',{FILTER=>"SingleColumnValueExcludeFilter('f1','age',>=,'binary:25')"}

```

## Shell 高级操作

### 查看当前登录用户

```
whoami
```

```shell
hbase:015:0> whoami
mac (auth:SIMPLE)
    groups: staff, everyone, localaccounts, _appserverusr, admin, _appserveradm, _lpadmin, com.apple.sharepoint.group.1, _appstore, _lpoperator, _developer, _analyticsusers, com.apple.access_ftp, com.apple.access_screensharing, com.apple.access_ssh, com.apple.access_remote_ae
```
