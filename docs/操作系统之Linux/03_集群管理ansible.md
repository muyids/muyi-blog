# 概念

Ansible 是一种由 Python 开发的自动化运维工具，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了**批量系统配置**、**批量程序部署**、**批量运行命令**等功能，是一款**轻量级的配置自动化工具**。

Ansible 是基于模块工作的，本身没有批量部署的能力。真正具有批量部署的是 ansible 所运行的模块，ansible 只是提供一种框架。主要包括：

​ (1) **连接插件 connection plugins**：负责和被管控端实现通信；

​ (2) **host inventory**：指定操作的主机，是一个配置文件里面定义管控的主机;

​ (3) **各种模块核心模块、 command 模块、自定义模块**；

​ (4) 借助于**插件**完成记录日志邮件等功能；

​ (5) **playbook**：剧本执行多个任务时，可以让被管控端一次性运行多个任务;

# Ansible 特性

​ (1) no agents：**不需要在被管控主机上安装任何客户端**；

​ (2) no server：**无服务器端**，使用时直接运行命令即可；

​ (3) modules in any languages：**基于模块工作**，可使用任意语言开发模块；

​ (4) yaml，not code：**使用 yaml 语言定制剧本 playbook**；

​ (5) ssh by default：**基于 SSH 工作**；

​ (6) strong multi-tier solution：**可实现多级指挥**；

# Ansible 优点

​ (1) **轻量级**，无需在客户端安装 agent，更新时，只需在操作机上进行一次更新即可；

​ (2) 批量任务执行可以写成脚本，而且不用分发到远程就可以执行；

​ (3) 使用 python 编写，维护更简单，ruby 语法过于复杂；

​ (4) 支持 sudo；

# Ansible 架构

![image-20220506150017048](https://muyids.oss-cn-beijing.aliyuncs.com/img/202205061500474.png)

**_Ansible 的架构_**，主要分为以下几部分内容：

- **ansible**：核心，提供一种框架
- **Connection Plugins**：连接插件,负责和被操作端实现通信，可通过多种方式与被操作端连接，例如：local、ssh、zeromq，默认使用 ssh；
- **Host Inventory**：主机清单，指定被操作主机;
- **Core Modules**：各种模块核心模块，Ansible 已自带
- **Custom Modules**：自定义模块，如果核心模块无法满足需求，可通过各种编程语言（Shell，Python 或 GoLang 等）开发模块使用。
- **Plugins**：借助于插件完成记录日志、邮件等功能；
- **Playbook**：剧本，当执行多个任务时，可以对服务器角色及应用部署进行编排。

**实现原理：ansible 通过单个模块或者 playbook 转换成 python 程序经过 ssh 协议，推送到各个主机上**

# Ansible 任务执行流程

![image-20220506150300148](https://muyids.oss-cn-beijing.aliyuncs.com/img/202205061503519.png)

# 安装使用

## 前置要求

需要依赖 Python 环境

## 安装

在 master 主机上安装 ansible，以我本地的 mac 为例

```shell
brew install ansible
```

## 配置文件

配置文件默认位置

# 批量执行 shell 命令（最常用）

ansible -i /etc/ansible/hosts check17662042 -m shell -a "chmod 755 /var/log/messages"

**批量杀掉远端服务器应用进程**

```shell
ansible test -m shell -a "ps -ef | grep zabbix |grep -v grep |awk '{print \$2}' | xargs kill -9"
```
