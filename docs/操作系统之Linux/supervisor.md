## 前言

守护进程管理工具有很多，比如 nodejs 的进程管理工具 PM2、forever，也有 linux 的`daemontools`、`supervisor`等，本文写一下 supervisor 的基本使用

## 安装

安装可以使用一下 命令:

```
sudo apt-get install supervisor
```

安装成功后,supervisor 就会默认启动

### 添加进程

将每个进程的配置文件单独拆分,放在`/etc/supervisor/conf.d/`目录下, 以`.conf`作为扩展名,例如`test.conf`定义的一个简单的 HTTP 服务器:

```
[program:test]
command=python -m SimpleHTTPServer
```

重启 supervisor,让配置文件生效,然后启动 test 进程:

```
supervisorctl reload
supervisorctl start test
```

如果要停止进程,就用 stop

### 配置

通过这个例子讲解

```
[program:meta.txn.recover.on.error]
command=/cas/bin/meta.txn.recover.on.error ; 被监控的进程路径
numprocs=1                    ; 启动几个进程
directory=/cas/bin            ; 执行前要不要先cd到目录去，一般不用
autostart=true                ; 随着supervisord的启动而启动
autorestart=true              ; 自动重启。。当然要选上了
startretries=10               ; 启动失败时的最多重试次数
exitcodes=0                 ; 正常退出代码（是说退出代码是这个时就不再重启了吗？待确定）
stopsignal=KILL               ; 用来杀死进程的信号
stopwaitsecs=10               ; 发送SIGKILL前的等待时间
redirect_stderr=true          ; 重定向stderr到stdout
stdout_logfile=logfile        ; 指定日志文件
```

### 常用命令

- supervisorctl start programxxx，启动某个进程
- supervisorctl restart programxxx，重启某个进程
- supervisorctl stop groupworker: ，重启所有属于名为 groupworker 这个分组的进程(start,restart 同理)
- supervisorctl stop all，停止全部进程，注：start、restart、stop 都不会载入最新的配置文件。
- supervisorctl reload，载入最新的配置文件，停止原有进程并按新的配置启动、管理所有进程。
- supervisorctl update，根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响而重启。
