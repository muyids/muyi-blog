# Strace 命令介绍

可用于诊断、调试和教学的 Linux 用户空间跟踪器。

用他来监控用户空间进程 和 内核 的交互，比如系统调用、信号传递、进程状态变更等。

# 常用选项

从一个示例命令来看：

```shell
strace -tt -T -v -f -e trace=file -o /data/log/strace.log -s 1024 -p 23489
```

- -tt : 每行输出的前面，显示毫秒级的时间
- -T 显示每次系统调用所花费的时间
- -v 对于某些相关调用，把完整的画境变量，文件 stat 结构等打印出来
- -f 最终目标进程，以及 目标进程 创建的所有子进程
- -e 控制要跟踪的事件 和 跟踪行为，比如指定要跟踪的 系统调用名称
- -o 把 strace 的输出单独写到 指定的文件
- -s 当系统调用的某个参数是字符串时，最多输出指定长度的内容，默认是 32 个字节
- -p 指定要跟踪的进程 pid， 要同时跟踪多个 pid，重复多次 -p 选项即可

# 系统调用函数分类说明

## 进程管理

| 函数名  | 说明                 |
| ------- | -------------------- |
| fork    | 创建一个新进程       |
| clone   | 按指定条件创建子进程 |
| execve  | 运行可执行文件       |
| pause   | 进程将处于阻塞状态   |
| wait    | 等待子进程终止       |
| waitpid | 等待指定子进程终止   |
|         |                      |

## 文件和设备访问

| 函数名   | 说明           |
| -------- | -------------- |
| open     | 打开文件       |
| creat    | 创建新文件     |
| close    | 关闭文件描述符 |
| read     | 读文件         |
| write    | 写文件         |
| pread    | 对文件随机读   |
| pwrite   | 对文件随机写   |
| poll     | I/O 多路转换   |
| truncate | 截断文件       |

## 文件系统操作

| 函数名   | 说明                   |                                                         |
| -------- | ---------------------- | ------------------------------------------------------- |
| access   | 确定文件的可存取性     |                                                         |
| Chmod    | 确定文件的可存取性     |                                                         |
| Chown    | 改变文件的属主或用户组 |                                                         |
| chroot   | 改变根目录             |                                                         |
| stat     | 获取文件状态信息       |                                                         |
| lstat    | 获取文件状态信息       |                                                         |
| Getdents | 读取目录项             |                                                         |
| mkdir    | 创建目录               |                                                         |
| link     | 创建链接               |                                                         |
| fcntl    | 用来管理文件描述符     | https://blog.csdn.net/rikeyone/article/details/88828154 |

## 内存管理

| 函数名   | 说明                                                                                     | 说明                                                            |
| -------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| mmap     | 映射虚拟内存页                                                                           |                                                                 |
| sync     | 将内存缓冲区数据写回硬盘                                                                 |                                                                 |
| Brk/sbrk | brk 机制，mmap 主要控制虚拟空间 mmap 区域管理，而 brk 机制主要管理的是一个进行的堆空间。 | https://blog.csdn.net/weixin_42730667/article/details/121113433 |

## socket 控制

| 函数名     | 说明                    |
| ---------- | ----------------------- |
| Socketcall | socket 系统调用         |
| Socket     | 建立 socket             |
| bind       | 绑定 socket 到端口      |
| connect    | 连接远程主机            |
| send       | 通过 socket 发送信息    |
| sendto     | 发送 UDP 信息           |
| sendmsg    | 参见 send               |
| listen     | 监听 socket 端口        |
| select     | 对多路同步 I/O 进行轮询 |
|            |                         |

# 故障案例一

调试

strace -e open,openat -ff -s 1023 -tt ./console plugin:activate ExtraTools 2>&1 | tee b.log

strace -ff -s 1023 -tt ./console plugin:deactivate ExtraTools 2>&1 | tee b.log

```
strace -o output.txt -T -tt -e trace=all -p 28979
```
