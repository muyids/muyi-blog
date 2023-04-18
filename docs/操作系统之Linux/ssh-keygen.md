---
title: 使用ssh-keygen配置自动登录
date: 2017-12-01T00:00:00+08:00
categories: [shell, linux]
tags: [shell, linux]
---

ssh 是一个专为远程登录会话和其他网络服务提供安全性的协议。ssh-keygen 可用来生成 ssh 公钥认证所需的公钥和私钥文件

<!--more-->

# 背景

1. 使用 git clone 拉取 git 仓库代码时, 提示：

   Permission denied (publickey).
   fatal: Could not read from remote repository.

2. 登录远程 Linux 主机，每次都要 ssh 输入密码，可否自动登录？

# 命令介绍

- ssh-keygen

  产生公钥与私钥对.

- ssh-copy-id
  将本机的公钥复制到远程机器的 authorized_keys 文件中，ssh-copy-id 也能让你有到远程机器的 home,~/.ssh,和~/.ssh/authorized_keys 的权利

# 设置 git 仓库权限

1. 查看~/.ssh, 或使用 ssh-keygen 产生公钥私钥对

   $ ssh-keygen

2. 添加到 git 仓库 SSH key

   将~/.ssh/id_rsa.pub 中的公钥添加到 git 仓库 SSH key。

# 设置 ssh 自动登录

1. 查看~/.ssh, 或使用 ssh-keygen 产生公钥私钥对

   mac$ ssh-keygen

2. 用 ssh-copy-id 将公钥复制到远程机器中

   ```
   	ssh-copy-id -i ~/.ssh/id_rsa.pub [-p xxx]  user@remote-host-ip
   ```

   **注意**
   ssh-copy-id 将 key 写到远程机器的 ~/.ssh/authorized_key 文件中

3. 在~/.ssh 目录下创建文件 config，添加远程主机授权

   ```
   	Host 主机名
       HostName 远程主机IP
       User root
       PreferredAuthentications publickey
       IdentityFile ~/.ssh/id_rsa
   ```

4. 登陆远程主机

```
	ssh 主机名
```
