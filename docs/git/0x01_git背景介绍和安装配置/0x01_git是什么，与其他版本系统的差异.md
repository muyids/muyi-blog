# Git 是什么？

相信大家都有用过 Git，还有其他一些版本控制系统，比如 CVS、Subversion、Perforce。

这些版本控制系统的使用方式都大同小异、 但在对信息的存储和认知方式上却有很大差异。

# 直接记录快照，而非差异比较

**基于差异（delta-based）** 的版本控制：存储每个文件与初始版本的差异

<img src="https://git-scm.com/book/en/v2/images/deltas.png" alt="存储每个文件与初始版本的差异。"  />

**快照流** 式的小型文件系统：存储项目随时间改变的快照

![Git 存储项目随时间改变的快照。](https://muyids.oss-cn-beijing.aliyuncs.com/img/snapshots.png)

这是 Git 与几乎所有其它版本控制系统的重要区别

# 近乎所有操作都是本地执行

# Git 保证完整性

# Git 一般只添加数据

# 三个阶段：工作区、暂存区以及 Git 目录

![工作区、暂存区以及 Git 目录。](https://muyids.oss-cn-beijing.aliyuncs.com/img/areas.png)

![img](https://muyids.oss-cn-beijing.aliyuncs.com/img/2013443-20201124171944798-1651933558.png)

文件的三种状态：

- **已修改（modified）**
- **已暂存（staged）**
- \*已提交（committed）\*\*

基本的 Git 工作流程如下：

1. 在工作区中修改文件。
2. 将你想要下次提交的更改选择性地暂存，这样只会将更改的部分添加到暂存区。
