## 分支

### 查看本地分支

```shell script
git branch
```

### 查看远程分支

```shell script
git branch -r
```

### 查看所有分支

```shell script
git branch -a
```

### 创建分支（通过远程分支）

切换远程分支

```shell script
$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master

$ git checkout -b myRelease origin/Release
Branch myRelease set up to track remote branch Release from origin.
Switched to a new branch 'myRelease'
```

PS: 作用是`checkout`远程的`Release`分支，在本地起名为`myRelease`分支，并切换到本地的`myRelase`分支

### 创建分支（通过本地分支）

```shell script
$ git checkout -b xxx
```

### 删除分支

删除本地分支

```shell script
git branch -d branch_name
```

### 合并分支

合并前要先切回要并入的分支

以下表示要把`issue1234`分支合并入`master`分支

```shell script
$ git checkout master
$ git merge issue1234
Merge made by recursive.
 README |    1 +
 1 files changed, 1 insertions(+), 0 deletions(-)
```

### 创建远程分支

```shell script
$ git push origin local_branch
```

## commit

### 撤消上一次 commit 的内容

**该操作会彻底回退到某个版本，本地的源码也会变为上一个版本的内容**

```shell script
git reset --hard <commit-id>
```

### 合并提交记录

假设需要合并前三个提交记录，执行命令

```shell script
git rebase -i HEAD~3
```

pick 是 rebase 时的指令，具体我们还可以使用如下指令：

- 选择 pick 指令，git 会应用这个提交，以同样的提交信息（commit message）保存提交
- 选择 reword 指令，git 会应用这个提交，但需要重新编辑提交信息
- 选择 edit 指令，git 会应用这个提交，但会因为 amending 而终止
- 选择 squash 指令，git 会应用这个提交，但会与之前的提交合并
- 选择 fixup 指令，git 会应用这个提交，但会丢掉提交日志
- 选择 exec 指令，git 会在 shell 中运行这个命令
