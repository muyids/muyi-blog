# 环境配置

## mac 配置

- maven 安装
- idea # java 代码开发 IDE

```shell
brew install maven
```

多版本 java 配置

```
# java安装
```

maven 仓库配置

```sh

```

## windows 配置

### 下载 jdk

解压到指定目录

### 配置环境变量

JAVA_HOME 环境变量配置

1、添加系统变量 JAVA_HOME，赋值为 jdk 安装目录

1、增加 Path 变量

```shell
%JAVA_HOME%\bin
```

1、在系统变量里新建一个 CLASSPATH，赋值如下：

```shell
.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar
```
