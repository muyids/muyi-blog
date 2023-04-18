# 国内源 brew 安装

```shell
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

推荐选择 中科大国内源

![image-20220515002954347](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515002954347.png)

brew install 访问 阿里国内源

![image-20220515002936242](https://muyids.oss-cn-beijing.aliyuncs.com/img/image-20220515002936242.png)

先安装 brew ，方便下面安装其他软件

# 安装 switch hosts

```sh
brew install --cask switchhosts
```

安装 switch hosts 后，配置 github520 可以加速 github 访问，加快其他软件安装进度

使用自动方式，定时更新 github hosts

https://github.com/521xueweihan/GitHub520#22-%E8%87%AA%E5%8A%A8%E6%96%B9%E5%BC%8F

# shell 配置

- shell 选择
  - zsh - 更强大的 shell
- shell 终端 选择
  - tabby.sh - 现代化的 shell 终端
- vim 配置

## zsh 配置

### 安装 zsh

### 插件配置

#### 配置插件 zsh-autosuggestions

1. 把插件仓库克隆到`$ZSH_CUSTOM/plugins` (默认位置是 ~/.oh-my-zsh/custom/plugins)

```ruby
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

1. 设置`~/.zshrc`，把`zsh-autosuggestions`添加到 Oh My Zsh 要加载的插件列表中

```shell
plugins=(git zsh-autosuggestions)
```

#### 配置插件 autojump

安装

```
brew install autojump
```

.zshrc 增加下面一行

```
[ -f /usr/local/etc/profile.d/autojump.sh ] && . /usr/local/etc/profile.d/autojump.sh
```

## 自定义 shell 命令

### 重新定义 rm

```shell
trash()
{
    set -x
    files=()
    Timestamp=`date "+%Y%m%d.%H%M%S"`
    for file in "$@"
    do
        if [[ ${file:0:1} != "-" ]]
        then
            files=("${files[@]}" "${file}")
        fi
    done
    mkdir -p ~/.tmp/$Timestamp
    mv "${files[@]}" ~/.tmp/$Timestamp
}
alias rm=trash
```

# 配置编程环境

## python 环境配置

- anaconda3 安装
- pycharm 安装
  1、安装 anaconda3

```
brew install --verbose --cask anaconda
brew install anaconda3
```

1、配置环境变量

```
# anaconda3
export ANACONDA3_HOME=/usr/local/anaconda3

export PATH=$PATH:$ANACONDA3_HOME/bin
```

1、conda 创建虚拟环境

```
conda create -n py39
```

1、激活虚拟环境

```
conda activate py39
```

1、虚拟环境配置

```
conda install python=3.9
```

​

## java 环境配置

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

## nodejs 环境配置

1、node 安装

```
brew install node@12
```

1.1、npm 配置国内源

```
npm config set registry https://registry.npm.taobao.org
```

检查配置，返回设置的源：

```
npm config get registry
```

2、node 版本管理工具 n 安装

```
npm install n -g
```

n 配置国内源

```
# nodejs n version management
export N_NODE_MIRROR=https://npm.taobao.org/mirrors/node
```

## golang 环境配置

```
brew install go
```

# 效率软件安装

## 安装截图软件 snipaste

```
brew install --cask snipaste
```
