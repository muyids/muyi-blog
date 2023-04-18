# Skywalking 概述

## APM 系统

### 分布式链路追踪

### 什么是 OpenTracing

### 主流开源 APM 产品

## 什么是 skywalking

# 安装

- 安装 Backend
- 安装 UI

## 1.下载

https://skywalking.apache.org/downloads/

下载 SkyWalking APM，选择 8.4.0 版本

https://www.apache.org/dyn/closer.cgi/skywalking/8.4.0/apache-skywalking-apm-8.4.0.tar.gz

## 2.修改配置文件

解压后，进入 config 目录下，修改服务端配置文件 application.yml 中的数据源配置

进入 webapp 目录下，修改前端 webapp.yml 中的端口配置

## 3.启动服务

进入 bin 目录下，oapServiceNoInit 脚本启动后端服务，webappService 脚本启动前端服务，或者使用 startup.sh 脚本同时启动后端+前端

# agent

```
java -javaagent:/usr/local/apache-skywalking-apm-bin/agent/skywalking-agent.jar -jar out/artifacts/YourProject.jar
```

jar 包可以使用 mvn 打包

```
jar：mvn clean install -Dmaven.test.skip=true
# 说明：clean是清除之前的jar包，install是打包到本地，-Dmaven.test.skip=true是忽略测试代码；

war：mvn clean package -Dmaven.test.skip=true
```
