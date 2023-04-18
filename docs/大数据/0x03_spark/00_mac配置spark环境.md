# 安装 Scala

```
brew install scala
```

配置 Scala 的环境变量

```
export SCALA_HOME=/usr/local/opt/scala
export PATH=$PATH:$SCALA_HOME/bin
```

# 安装 spark

官网下载指定版本解压

```
/usr/local/opt/spark-2.4.5-bin-hadoop2.6
```

配置环境变量

```
export SPARK_HOME=/usr/local/opt/spark-2.4.5-bin-hadoop2.6
export PATH="${SPARK_HOME}/bin:$PATH"
```

打开终端，输入`spark-shell`，打印 spark 则说明配置成功

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.5
      /_/
```
