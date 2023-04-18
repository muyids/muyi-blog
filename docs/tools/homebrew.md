## 安装

https://zhuanlan.zhihu.com/p/111014448

苹果电脑 常规安装脚本（推荐 完全体 几分钟安装完成）：

/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

## 初步介绍几个 brew 命令

本地软件库列表：brew ls
查找软件：brew search google（其中 google 替换为要查找的关键字）
查看 brew 版本：brew -v 更新 brew 版本：brew update
安装 cask 软件：brew install --cask firefox 把 firefox 换成你要安装的

## 安装 mysql

brew install mysql@5.7

brew install --cask mysqlworkbench

重设密码
brew services start mysql@5.7
$(brew --prefix mysql@5.7)/bin/mysqladmin -u root password 123456

## 安装 httpd

brew install httpd
DocumentRoot is /usr/local/var/www.
