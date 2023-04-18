# python 环境配置

- anaconda3 安装

- python 安装

# 安装 anaconda3

```
wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# 安装命令：
chmod 777 Miniconda3-latest-Linux-x86_64.sh #给执行权限
bash Miniconda3-latest-Linux-x86_64.sh #运行
```

配置环境变量

```
# anaconda3
export ANACONDA3_HOME=/usr/local/anaconda3

export PATH=$PATH:$ANACONDA3_HOME/bin
```

# conda 创建虚拟环境

```
conda create -n py39
```

## 激活虚拟环境

```
conda activate py39
```

## 虚拟环境配置

```
conda install python=3.9
```
