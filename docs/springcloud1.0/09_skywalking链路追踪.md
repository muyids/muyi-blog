**链路追踪**

对于大型微服务架构系统，通常会有下面一些问题：

- 如何串联整个调用链路，快速定位问题
- 如何缕清各个微服务间的依赖关系
- 如何进行各个微服务接口的性能分析
- 如何跟踪整个业务流程的调用处理顺序
  **链路追踪框架对比**

1. Zipkin : twitter 开源的调用链分析工具，目前基于 spring cloud sleuth 得到了广泛应用，特点是轻量，使用部署简单
2. Pinpoint：韩国人开源的基于字节码注入的调用链分析，以及应用监控分析工具。特点是支持多种插件，UI 功能强大，接入端无代码侵入
3. SkyWalking：本土开源的**基于字节码注入的调用链分析**，以及应用监控分析工具。特点是支持多种插件，UI 功能强大，接入端无代码侵入。目前已加入 Apache 孵化器
4. CAT：美团点评开源的基于编码和配置的调用链分析，应用监控分析，日志采集，监控报警等一系列的监控平台工具。

#### **skywalking**

**功能特性**

1. 多种监控手段，可以通过语言探针和 service mesh 获得监控数据
2. 支持多种语言探针，包括 Java，nodejs
3. 轻量高效，无需大数据平台和大量的服务器资源
4. 模块化，UI、存储、集群管理都有多种机制可选
5. 支持告警
6. 优秀的可视化解决方案
   **环境搭建**

![2021-10-14 pm5.23.45](https://muyids.oss-cn-beijing.aliyuncs.com/2021-10-14%20pm5.23.45.png)

几大组件：

<1>skywalking oapservice 集群：负责处理监控数据，比如接收 skywalking agent 的监控数据，并存储在数据库中

；接受 skywalking webapp 的前端请求，从数据库查询数据，并返回数据给前端。通常以集群形式存在；

<2>skywalking agent：与业务系统绑定在一起，负责收集各种监控数据

<3>skywalking webapp：前端页面，用于展示数据

<4>数据库：存储监控数据，如 mysql， elasticsearch 等

**服务端安装启动**

下载地址：

https://skywalking.apache.org/downloads/

下载解压后，修改 webapp 端口地址 webapp/webapp.yml 中 server.port: 8080 为 8858 端口

启动服务：

运行 `./bin/startup.sh`

输出日志：

SkyWalking OAP started successfully!
SkyWalking Web Application started successfully!
OAP 和 Web 服务启动成功，运行日志在 logs 目录下

访问：http://127.0.0.1:8858/

**接入微服务**

配置 agent

```bash
-javaagent:/usr/local/apache-skywalking-apm-bin-es7-8.7.0/agent/skywalking-agent.jar
-Dskywalking.agent.namespace=cloud
-Dskywalking.agent.service_name=stock-service
```

进行业务请求

**查看 webapp**

访问：http://127.0.0.1:8858/

右上角选择 自动刷新

**仪表盘**
