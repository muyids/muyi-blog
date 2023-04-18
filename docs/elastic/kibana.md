Kibana 是一款开源的数据分析和可视化平台，它是 `Elastic Stack` 成员之一，设计用于和 `Elasticsearch` 协作。您可以
使用 Kibana 对 Elasticsearch 索引中的数据进行搜索、查看、交互操作。您可以很方便的利用图表、表格及地图对
数据进行多元化的分析和呈现。

官网：https://www.elastic.co/cn/products/kibana

# 安装配置

## 解压安装包

```shell script
tar -xvf kibana-6.5.4-linux-x86_64.tar.gz
```

## 修改配置文件

```shell script
vim config/kibana.yml
server.host: "0.0.0.0" #对外暴露服务的地址
elasticsearch.hosts: ["http://129.0.4.37:9200", "http://129.0.4.38:9200", "http://129.0.4.39:9200"]
kibana.index: ".kibana"
```

## 启动

```shell script
./bin/kibana --allow-root
```

## 通过浏览器进行访问

```shell script
http://129.0.4.37:5601/app/home#/
```
