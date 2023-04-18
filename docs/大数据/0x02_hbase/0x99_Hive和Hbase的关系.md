# 大数据技术生态

## 核心问题

大数据技术本质上无非解决 4 个核心问题：

- **存储，**海量的数据怎样有效的存储？主要包括 hdfs、Kafka；
- **计算，**海量的数据怎样快速计算？主要包括 MapReduce、Spark、Flink 等；
- **查询，**海量数据怎样快速查询？主要为 Nosql 和 Olap，Nosql 主要包括 Hbase、 Cassandra 等，其中 olap 包括[kylin](https://www.zhihu.com/search?q=kylin&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A156227565})、impla 等，其中 Nosql 主要解决随机查询，Olap 技术主要解决关联查询；
- **挖掘，**海量数据怎样挖掘出隐藏的知识？也就是当前火热的机器学习和深度学习等技术，包括 TensorFlow、caffe、[mahout](https://www.zhihu.com/search?q=mahout&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A156227565})等；

## Hbase 和 Hive 的关系

Hbase 和 Hive 在大数据架构中处在不同位置，Hbase 主要解决实时数据查询问题，Hive 主要解决数据处理和计算问题，一般是配合使用。

**一、区别：**

1. Hbase： Hadoop database 的简称，也就是基于 Hadoop 数据库，是一种 NoSQL 数据库，主要适用于海量明细数据（十亿、百亿）的随机实时查询，如日志明细、交易清单、轨迹行为等。
2. Hive：Hive 是 Hadoop[数据仓库](https://www.zhihu.com/search?q=数据仓库&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A185664626})，严格来说，不是数据库，主要是让开发人员能够通过 SQL 来计算和处理 HDFS 上的结构化数据，适用于离线的[批量数据计算](https://www.zhihu.com/search?q=批量数据计算&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A185664626})。

- 通过元数据来描述 Hdfs 上的[结构化文本](https://www.zhihu.com/search?q=结构化文本&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A185664626})数据，通俗点来说，就是定义一张表来描述 HDFS 上的结构化文本，包括各列数据名称，数据类型是什么等，方便我们处理数据，当前很多 SQL ON Hadoop 的计算引擎均用的是 hive 的元数据，如 Spark SQL、Impala 等；
- 基于第一点，通过 SQL 来处理和计算 HDFS 的数据，Hive 会将 SQL 翻译为 Mapreduce 来处理数据；
  在大数据架构中，Hive 和 HBase 是协作关系，数据流一般如下图：

1. 通过 ETL 工具将数据源抽取到 HDFS 存储；
2. 通过 Hive 清洗、处理和计算原始数据
3. HIve 清洗处理后的结果，如果是面向海量数据随机查询场景的可存入 Hbase
4. 数据应用从 HBase 查询数据；
