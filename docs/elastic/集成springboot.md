## API 地址

https://www.elastic.co/guide/en/elasticsearch/client/index.html

elasticsearch 版本查看

### **Check Version using Curl from Command Line**

```json
GET /
{
  "name": "cluster-dev01-es-default-2",
  "cluster_name": "cluster-dev01",
  "cluster_uuid": "W2qQ9vVzQg6YcyByn3c-QQ",
  "version": {
    "number": "7.17.1",
    "build_flavor": "default",
    "build_type": "docker",
    "build_hash": "e5acb99f822233d62d6444ce45a4543dc1c8059a",
    "build_date": "2022-02-23T22:20:54.153567231Z",
    "build_snapshot": false,
    "lucene_version": "8.11.1",
    "minimum_wire_compatibility_version": "6.8.0",
    "minimum_index_compatibility_version": "6.0.0-beta1"
  },
  "tagline": "You Know, for Search"
}
```

7.17.1 版本

https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/7.17/index.html

高版本 API

https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/7.17/migrate-hlrc.html

```
 pom.xml
 <properties>
   <java.version>1.8</java.version>
   <elasticsearch.version>7.17.1</elasticsearch.version>
 </properties>
```
