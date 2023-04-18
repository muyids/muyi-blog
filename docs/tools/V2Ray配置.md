## **配置代理**

下面开始进行配置，以 zsh 为例。

```
~vim ~/.zshrc
```

按下**i**，进入编辑模式，并添加如下配置：

```
# proxy list# 注意这里的端口号，要写成你自己的alias proxy='export all_proxy=socks5://127.0.0.1:7891'alias unproxy='unset all_proxy'
```

按下**:wq**保存后退出。
输入下面的命令进行更新：

```
~ source ~/.zshrc
```

在终端中执行命令，查看当前的 IP 地址：

```
~curl cip.cc
```

可以看到当前的 IP 地址。
接着输入:

```
~proxy~curl cip.cc
```
