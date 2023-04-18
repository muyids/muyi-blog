# Python 环境配置

# anaconda3 安装

## 安装 anaconda3

```
brew install --verbose --cask anaconda
brew install anaconda3
```

## 配置环境变量

```
# anaconda3
export ANACONDA3_HOME=/usr/local/anaconda3

export PATH=$PATH:$ANACONDA3_HOME/bin
```

## conda 创建虚拟环境

```
conda create -n py39
```

### 激活虚拟环境

```
conda activate py39
```

### 虚拟环境配置

```
conda install python=3.9
```

​

# pip 配置国内源

`cat .pip/pip.conf`

​

```
[global]
index-url = http://pypi.douban.com/simple
extra-index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host =
    pypi.douban.com            #添加豆瓣源为可信主机，要不然可能报错
    pypi.tuna.tsinghua         #清华
timeout = 120
```
