# 版本控制系统（Version Control System - VCS）发展历程

核心三要素：

- **版本控制**

- 主动提交

- 中央仓库

# 本地版本控制系统

<img src="https://muyids.oss-cn-beijing.aliyuncs.com/img/local.png" alt="本地版本控制图解" style="zoom:50%;" />

# 集中式的版本控制系统

集中化的版本控制系统（Centralized Version Control Systems，简称 CVCS）

![image-20230218205640623](https://muyids.oss-cn-beijing.aliyuncs.com/img/20230218205640623.png)

如 CVS、Subversion 以及 Perforce 等

## 好处和缺点

好处：

- 每个人都可以在一定程度上看到项目中的其他人正在做些什么
- 管理员可以轻松掌控每个开发者的权限
  坏处：

- 中央服务器的单点故障，将造成项目整个变更历史的丢失

# 分布式的版本控制系统

分布式版本控制系统（Distributed Version Control System，简称 DVCS）

<img src="https://muyids.oss-cn-beijing.aliyuncs.com/img/distributed.png" alt="分布式版本控制图解" style="zoom: 67%;" />

## 优点与缺点

优点：

- 本地操作，速度更快
- 无需联网便可以提交代码、查看历史
  缺点：

- 本地保存完整仓库，占用存储较高
- 初次获取项目比较耗时

# Git 简史

Linux 开源社区自己的版本系统

目标：

- 速度
- 简单的设计
- 对非线性开发模式的强力支持（允许成千上万个并行开发的分支）
- 完全分布式
