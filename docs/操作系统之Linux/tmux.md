https://www.ruanyifeng.com/blog/2019/10/tmux.html

# 会话管理

## 新建会话

```bash
tmux new -s <session-name>
```

## 分离会话

按下`Ctrl+b d`或者输入`tmux detach`命令，就会将当前会话与窗口分离。

## 会话查看

```
tmux ls
```

## 会话接入

```
# 使用会话编号
$ tmux attach -t 0

# 使用会话名称
$ tmux attach -t <session-name>
```

## 杀死会话

```
# 使用会话编号
$ tmux kill-session -t 0

# 使用会话名称
$ tmux kill-session -t <session-name>
```

## 切换会话

```

# 使用会话编号
$ tmux switch -t 0
# 使用会话名称
$ tmux switch -t <session-name>
```

## 重命名会话

```
tmux rename-session -t 0 <new-name>
```
