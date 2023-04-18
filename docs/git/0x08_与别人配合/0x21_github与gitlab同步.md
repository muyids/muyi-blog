## 场景

工作中经常有跟 开源项目 共同开发的需要

## 一、初始化仓库

操作步骤：

1、gitlab 创建新仓库

2、将 github 项目作为 upstream 远程

git remote add upstream https://github.com/user/repo.git

3、从 upstream 远程拉代码

git pull upstream main

4、推到 gitlab

git push origin master

参考：<https://stackoverflow.com/questions/50973048/forking-git-repository-from-github-to-gitlab>

## 二、分支同步

upstream 中的代码修改 怎么同步到 gitlab

```shell
git pull --unshallow
# 自行替换要同步的上游仓库地址
git remote add upstream https://github.com/upstream/upstream.git
git fetch upstream

# 可以自定义要同步的分支
git checkout -b master origin/master
git merge --no-edit upstream/master
git push origin master
<!-- 作者：Goooler
链接：https://www.zhihu.com/question/28676261/answer/1828601410
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。 -->
```

## 三、创建自己的开发分支

```
git checkout -b my-dev
```

## gitlab 已有项目更新到 github 最新

从 upstream 远程拉代码

```
git pull upstream master
git pull upstream unomi-1.6.x
```

推到 gitlab

```
git push origin master
git push origin unomi-1.6.x
```
