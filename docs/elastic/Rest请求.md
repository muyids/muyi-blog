# 聚合查询

```json
// 先检索
{
    "query": {
        "term": { "properties.gender": "男" }
    }
}

// 聚合查询
{
  "aggs": {
      "stat_gender": {
         "terms": {
              "field": "properties.gender.keyword"
          }
      }
  },
  "size": 0
}

=> 返回结果
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "stat_gender": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "女",
          "doc_count": 88061
        },
        {
          "key": "男",
          "doc_count": 80164
        },
        {
          "key": "未知",
          "doc_count": 176
        }
      ]
    }
  }
}
```

​

### **聚合为桶**

```shell
{
  "aggs" : {
    "types_count" : { "value_count" : { "field" : "_id" } }
  }
}
{
  "aggs" : {
    "popular_colors" : { "terms" : { "field" : "color" } }
  }
}

{
  "aggs" : {
    "popular_colors" : { "terms" : { "field" : "_source._id" } }
  }
}

POST /context-profile/_search?size=0
// https://www.elastic.co/guide/en/elasticsearch/reference/7.12/search-aggregations-metrics-scripted-metric-aggregation.html
{
  "query": {
    "match_all": {}
  },
  "aggs": {
    "profit": {
      "scripted_metric": {
      	"init_script": "state.transactions = []",
        "map_script": "state.transactions.add( doc._version.value == 7 ? 1 : 0)",
        "combine_script": "double profit = 0; for (t in state.transactions) { profit += t } return profit",
        "reduce_script": "double profit = 0; for (a in states) { profit += a } return profit"
      }
    }
  }
}

init_script:  定义参数：数组变量
map_script： 对每个分片中的每条数据，进行一样的操作。 操作在每个分片中进行。上一步是在每个分片上，初始化数组。
combine_script： 同样是在每个分片中操作， 统计每个分片中，数组的和。
reduce_script： 最后把各个分片中统计的结果进行返回一个节点，然后进行求和，返回的结果
{
  "query": {
    "match_all": {}
  },
  "aggs": {
    "profit": {
      "scripted_metric": {
      	"init_script": "state.transactions = []",
        "map_script": "state.transactions.add(doc.hasVariable('_source') == 7 ? 1 : 0)",
        "combine_script": "double profit = 0; for (t in state.transactions) { profit += t } return profit",
        "reduce_script": "double profit = 0; for (a in states) { profit += a } return profit"
      }
    }
  }
}

```

首先，按照汽车的颜色 color 来划分桶，按照颜色分桶，最好是使用 TermAggregation 类型，按照颜色的名称来分桶。

```json
GET /car/_search
{
    "size" : 0,
    "aggs" : {
        "popular_colors" : {
            "terms" : {
                "field" : "color"
            }
        }
    }
}
```

分析：

```text
size：查询条数，这里设置为 0，因为不关心搜索到的数据，只关心聚合结果，提高效率
aggs：声明这是一个聚合查询，是 aggregations 的缩写
  popular_colors：给这次聚合起一个名字，可任意指定
    terms：聚合的类型，这里选择 terms，是根据词条内容（这里是颜色）划分
      field：划分桶时依赖的字段
```

```
{
    "size": 0,
    "aggs": {
        "properties": {
            "nested": {
                "path": "properties"
            }
        },
        "aggs": {
            "value_count": {
                "field": "gender"
            }
        }
    }
}
```

# 分组统计

### 通过 Elasticsearch 实现聚合检索 (分组统计)

https://www.jianshu.com/p/8a9275d2c07d

默认情况下, Elasticsearch 对 text 类型的字段(field)禁用了 fielddata ；
text 类型的字段在创建索引时会进行分词处理, 而聚合操作必须基于字段的原始值进行分析 ；
所以如果要对 text 类型的字段进行聚合操作, 就需要存储其原始值

—— 创建 mapping 时指定 fielddata=true, 以便通过反转倒排索引(即正排索引)将索引数据加载至内存中

**对 text 类型的字段开启 fielddata 属性：**

将要分组统计的 text field(即 tags)的 fielddata 设置为 true:

```bash
PUT test_index/_mapping/
{
    "properties": {
        "_source.properties.gender": {
            "type": "text",
            "fielddata": true
        }
    }
}
```

```
{
  "size": 0,
    "query": {
        "match": {  "_source.properties.gender": "男" }
    },
  "aggs": {
    "group_by_tags": {
      "terms": {
        "field": "_source.properties.gender"
      }
    }
  }
}
先分组再统计

求平均数
{
  "size": 0,
  "aggs": {
    "group_by_tags": {
      "terms": {
        "field": "_version"
      },
      "aggs": {
            "avg_version": {
                "avg": { "field": "_version" }
            }
        }
    }
  }
}
求个数

{
  "size": 0,
  "aggs": {
    "group_by_tags": {
      "terms": {
        "field": "_version"
      },
      "aggs": {
            "avg_version": {
                "avg": { "field": "_version" }
            }
        }
    }
  }
}

{
  "size": 0,
  "aggs": {
    "group_by_tags": {
      "terms": {
        "field": "_source.properties.gender"
      },
      "aggs": {
            "avg_version": {
                "value_count": { "field": "_source.properties.gender" }
            }
        }
    }
  }
}

```

### Elasticsearch 教程(11) elasticsearch 桶聚合 Query DSL

https://blog.csdn.net/winterking3/article/details/105048017

# 更新字段

插入新字段

PUT： /context-profile/\_mapping

## 更新某个字段的值

**没有验证通过**

在 elasticsearch 索引存储里，如果要更新索引的某条记录里的某个索引，怎么实现呢？
可以使用`script`脚本功能。

```shell
POST index_test/_doc/5605830/_update
{
  "script" : "ctx._source.thumb='http://img.test.com/2020/04/08/test.jpg'"
}
```

这就类似于 sql 的：

```sql
UPDATE index_test SET thumb='http://img.test.com/2020/04/08/test.jpg' WHERE id=5605830;
```

查询

GET: /context-profile/\_doc/zhdc_ningbo_hyc_2022-04-18_BPID_557

```json
{
  "_index": "context-profile",
  "_type": "_doc",
  "_id": "zhdc_ningbo_hyc_2022-04-18_BPID_557",
  "_version": 7,
  "_seq_no": 2043,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "_class": "com.xxx.data.unomi.api.Profile",
    "properties": {
      "gender": "男"
    },
    "systemProperties": {},
    "segments": [],
    "consents": {},
    "itemId": "zhdc_ningbo_hyc_2022-04-18_BPID_557",
    "itemType": "profile",
    "systemMetadata": {}
  }
}
```

```
POST /context-profile/_doc/zhdc_ningbo_hyc_2022-04-18_BPID_557/_update
{
  "script" : "ctx._source.properties.age=30"
}
```

### 对嵌套列表对象字段进行批量更新

https://www.5axxw.com/questions/content/wrn9qp

### 查询

post：

/context-propertytype/\_search

```
Query json
```

### 删除

post：

/context-propertytype/\_delete_by_query

```
{
  "query": {
        "bool": {
            "filter": [
                {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "defaultValue": {
                                        "query": "test"
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}
```

### too many scroll contexts 问题

1、查询 es 集群的`open_context`使用情况

```csharp
[GET] _nodes/stats/indices/search
```

参数解释

```cpp
        "search" : {
           "open_contexts" : 0,         //正在打开的查询上下文个数
           "query_total" : 0,           //查询出来的总数据条数
           "query_time_in_millis" : 0,  //查询阶段所耗费的时间
           "query_current" : 0,         //当前正在查询个数
           "fetch_total" : 0,           //Fetch操作的次数
           "fetch_time_in_millis" : 0,  //Fetch阶段总耗时时间
           "fetch_current" : 0,         //正在fetch的次数
           "scroll_total" : 0,          //通过scroll api查询数据总条数
           "scroll_time_in_millis" : 0, //通过scroll api总耗时时间
           "scroll_current" : 0,        //当前滚动API调用次
           "suggest_total" : 0,         //通过suggest api获取的推荐总数量
           "suggest_time_in_millis" : 0,//suggest总耗费时间
           "suggest_current" : 0        //正在执行suggest api的个数
         },
```

2、max_open_scroll_context 参数调大

```cpp
curl -X PUT http://ip:9200/_cluster/settings -H 'Content-Type: application/json' -d'{
    "persistent" : {
        "search.max_open_scroll_context": 5000
    },
    "transient": {
        "search.max_open_scroll_context": 5000
    }
}
'
```
