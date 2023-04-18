# 部署与运行

下载：https://www.elastic.co/downloads/beats

```shell script
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.9.0-linux-x86_64.tar.gz
tar -xvf filebeat-7.9.0-linux-x86_64.tar.gz
cd /app/filebeat-7.9.0-linux-x86_64
```

# 读取 nginx 日志写入 es

// nginx.yml

```shell script
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /data/logs/nginx/*.log
  tags: ["nginx"]
setup.template.settings:
  index.number_of_shards: 3 #指定索引的分区数
output.elasticsearch: #指定ES的配置
  hosts: ["129.0.4.37:9200","129.0.4.38:9200","129.0.4.39:9200"]
```
