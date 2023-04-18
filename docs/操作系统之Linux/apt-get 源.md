# apt-get 源

## 换源

apt-get 的源换成阿里或 163 的

### 备份原始的 Ubuntu 源列表

```
cp /etc/apt/sources.list /etc/apt/sources.list.backup
```

### 修改源列表文件

```
gedit /etc/apt/sources.list
```

### 把里面的列表替换成下面的列表

**注意：各 ubuntu 的版本对应的 atp-get 的源不一样，不能填错，否则用 apt-get 安装软件报各种奇怪的错。**

以下为$Ubuntu12.04$的$apt-get$源，如果是其它版本，请将版本名（$precise$ ）替换成正确的，对应关系如下：

```
ubuntu16.04 - xenial
ubuntu15.10 - willy
ubuntu14.04 - trusty
ubuntu12.04 - precise
```

#### 查看$Ubuntu$版本

```
cat /proc/version
```

【阿里云】

```
deb http://mirrors.aliyun.com/ubuntu/ precise main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ precise-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ precise-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ precise-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ precise-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ precise main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ precise-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ precise-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ precise-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ precise-backports main restricted universe multiverse
```

```

echo "deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list
```

### 更新软件源

```
apt-get update
```

发现是 bullseye 系统

```

```

# **apt-get 源的常识**

# 安装 vim

```
apt-get install -y vim
```

# 安装 clickhouse

```
apt-get install clickhouse-client
```

连接

```

clickhouse-client -h xxx -u xxx -p
```
