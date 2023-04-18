## Prometheus

prometheus 是时序型数据库

配置文件`prometheus.yml`：

```yaml
global:
  scrape_interval: 5s
```

docker 镜像

```
docker pull prom/prometheus
```

运行

```
docker run -p 9090:9090 --name prometheus \
-v /Users/dw/workspace/muyids/dockerfile/prometheus_01.yml:/etc/prometheus/prometheus.yml \
-d prom/prometheus
```

界面

http://127.0.0.1:9090/

```
CREATE USER 'exporter'@'localhost' IDENTIFIED BY '123456' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';
```

```
docker run -d \
  -p 9104:9104 \
  --network my-mysql-network  \
  -e DATA_SOURCE_NAME="exporter:123456@(localhost:3306)/" \
  prom/mysqld-exporter
```

**spring boot atuator 数据采集**

pom.xml 添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

spring boot 开放 prometheus 端点

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "prometheus"
  metrics:
    tags:
      application: ${spring.application.name}
```

配置 prometheus.yml

```yaml
scrape_configs:
  # 采集任务名称
  - job_name: "mall-tiny-grafana"
    # 采集时间间隔
    scrape_interval: 5s
    # 采集超时时间
    scrape_timeout: 10s
    # 采集数据路径
    metrics_path: "/actuator/prometheus"
    # 采集服务的地址
    static_configs:
      - targets: ["your-springboot-host:8080"]
```

docker 启动

```shell
docker run -p 9090:9090 --name prometheus \
-v /Users/dw/workspace/muyids/dockerfile/prometheus_02.yml:/etc/prometheus/prometheus.yml \
-d prom/prometheus
```

**Grafana**

<1>docker 启动

```shell
docker pull grafana/grafana
docker run -p 3000:3000 --name grafana -d grafana/grafana
```
